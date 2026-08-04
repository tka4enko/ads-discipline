#!/usr/bin/env python3
"""Turn platform reads into the portable Claude Ads CSV export.

The session fetches numbers through a connector and writes them to a raw JSON
file; this script does the arithmetic and the validation. The split is
deliberate: a model that sums spend in prose has no audit trail and no way to
fail loudly, and every aggregation rule below exists because the consuming
adapter rejects the file otherwise.

Usage:
    build-export.py <raw.json> <out.csv>

Input JSON:
    {
      "platform": "meta",
      "account_id": "...",
      "account_name": "...",
      "currency": "USD",
      "conversion_action": "JobForm Lead",
      "rows": [
        {"date": "2026-07-01",
         "campaign_id": "...", "campaign_name": "...", "campaign_status": "active",
         "creative_id": "...", "creative_name": "...",
         "conversions": 3, "budget": "20.00", "spend": "12.34"}
      ]
    }

Rows sharing (date, campaign_id, creative_id) are summed here, because several
ads may run the same creative and the adapter rejects a repeated grain rather
than double-counting it silently.
"""

from __future__ import annotations

import csv
import json
import sys
from collections import OrderedDict
from datetime import date
from decimal import Decimal, InvalidOperation

COLUMNS = (
    "date",
    "account_id",
    "account_name",
    "campaign_id",
    "campaign_name",
    "campaign_status",
    "creative_id",
    "creative_name",
    "conversion_action",
    "conversions",
    "budget",
    "spend",
    "currency",
)

# Mirrors claude_ads_core.contracts.PLATFORMS. Kept explicit so a typo fails
# here with a readable message instead of deep inside the adapter.
PLATFORMS = {
    "google", "meta", "youtube", "linkedin", "tiktok", "microsoft",
    "apple", "amazon", "reddit", "pinterest", "snapchat", "x",
}

MAX_ROWS = 500_000


class ExportError(Exception):
    """The export cannot be produced without inventing or losing a number."""


def _text(value: object, field: str, where: str) -> str:
    if value is None:
        raise ExportError(f"{where}: {field} is missing")
    text = str(value).strip()
    if not text:
        raise ExportError(f"{where}: {field} must not be empty")
    return text


def _amount(value: object, field: str, where: str) -> Decimal:
    try:
        number = Decimal(str(value).strip())
    except (InvalidOperation, AttributeError) as exc:
        raise ExportError(f"{where}: {field} must be numeric, got {value!r}") from exc
    if not number.is_finite():
        raise ExportError(f"{where}: {field} must be finite")
    if number < 0:
        raise ExportError(f"{where}: {field} must not be negative")
    return number


def _plain(number: Decimal) -> str:
    """Decimal without exponent notation; 1E+2 is numeric but reads as a typo."""
    return format(number.normalize(), "f")


def build(raw: dict) -> list[dict[str, str]]:
    platform = _text(raw.get("platform"), "platform", "input")
    if platform.lower() not in PLATFORMS:
        raise ExportError(f"input: unsupported platform {platform!r}")

    account_id = _text(raw.get("account_id"), "account_id", "input")
    account_name = _text(raw.get("account_name"), "account_name", "input")
    action = _text(raw.get("conversion_action"), "conversion_action", "input")

    currency = _text(raw.get("currency"), "currency", "input")
    if len(currency) != 3 or not currency.isalpha() or currency != currency.upper():
        raise ExportError(f"input: currency must be three uppercase letters, got {currency!r}")

    rows = raw.get("rows")
    if not isinstance(rows, list) or not rows:
        raise ExportError("input: rows must be a non-empty list")
    if len(rows) > MAX_ROWS:
        raise ExportError(f"input: {len(rows)} rows exceeds the {MAX_ROWS} row limit")

    # (date, campaign_id, creative_id) -> accumulated row.
    grains: "OrderedDict[tuple[str, str, str], dict]" = OrderedDict()
    # Identity fields must not disagree between rows describing the same object,
    # because the adapter refuses the whole file when they do.
    campaign_identity: dict[str, tuple[str, str]] = {}
    creative_identity: dict[str, tuple[str, str]] = {}
    budgets: dict[tuple[str, str], Decimal] = {}

    for index, row in enumerate(rows):
        where = f"rows[{index}]"
        if not isinstance(row, dict):
            raise ExportError(f"{where}: must be an object")

        day = _text(row.get("date"), "date", where)
        try:
            date.fromisoformat(day)
        except ValueError as exc:
            raise ExportError(f"{where}: date must be ISO 8601, got {day!r}") from exc

        campaign_id = _text(row.get("campaign_id"), "campaign_id", where)
        campaign_name = _text(row.get("campaign_name"), "campaign_name", where)
        campaign_status = _text(row.get("campaign_status"), "campaign_status", where).lower()
        creative_id = _text(row.get("creative_id"), "creative_id", where)
        creative_name = _text(row.get("creative_name"), "creative_name", where)

        identity = (campaign_name, campaign_status)
        if campaign_identity.setdefault(campaign_id, identity) != identity:
            raise ExportError(
                f"{where}: campaign {campaign_id} already seen as "
                f"{campaign_identity[campaign_id]}, now {identity}"
            )
        creative_pair = (campaign_id, creative_name)
        if creative_identity.setdefault(creative_id, creative_pair) != creative_pair:
            raise ExportError(
                f"{where}: creative {creative_id} already seen as "
                f"{creative_identity[creative_id]}, now {creative_pair}"
            )

        budget = _amount(row.get("budget"), "budget", where)
        budget_key = (campaign_id, day)
        if budgets.setdefault(budget_key, budget) != budget:
            raise ExportError(
                f"{where}: campaign {campaign_id} has budget {budgets[budget_key]} "
                f"and {budget} on {day} — the adapter rejects both"
            )

        spend = _amount(row.get("spend"), "spend", where)
        conversions = _amount(row.get("conversions"), "conversions", where)

        key = (day, campaign_id, creative_id)
        merged = grains.get(key)
        if merged is None:
            grains[key] = {
                "date": day,
                "account_id": account_id,
                "account_name": account_name,
                "campaign_id": campaign_id,
                "campaign_name": campaign_name,
                "campaign_status": campaign_status,
                "creative_id": creative_id,
                "creative_name": creative_name,
                "conversion_action": action,
                "conversions": conversions,
                "budget": budget,
                "spend": spend,
                "currency": currency,
            }
        else:
            # Several ads can share one creative. Their spend belongs to the
            # same grain, so it is added rather than emitted twice.
            merged["conversions"] += conversions
            merged["spend"] += spend

    out = []
    for row in grains.values():
        row["conversions"] = _plain(row["conversions"])
        row["budget"] = _plain(row["budget"])
        row["spend"] = _plain(row["spend"])
        out.append(row)
    return sorted(out, key=lambda r: (r["date"], r["campaign_id"], r["creative_id"]))


def main(argv: list[str]) -> int:
    if len(argv) != 3:
        print(__doc__.strip().splitlines()[0], file=sys.stderr)
        print("usage: build-export.py <raw.json> <out.csv>", file=sys.stderr)
        return 2
    try:
        with open(argv[1], encoding="utf-8") as handle:
            raw = json.load(handle)
    except (OSError, json.JSONDecodeError) as exc:
        print(f"cannot read input: {exc}", file=sys.stderr)
        return 1
    try:
        rows = build(raw)
    except ExportError as exc:
        print(f"REFUSED: {exc}", file=sys.stderr)
        return 1

    with open(argv[2], "w", encoding="utf-8", newline="") as handle:
        # "\n", not the csv default "\r\n": these files get versioned, and a
        # carriage return turns every line of every diff into noise.
        writer = csv.DictWriter(handle, fieldnames=list(COLUMNS), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)

    merged = sum(1 for _ in raw["rows"]) - len(rows)
    print(f"wrote {len(rows)} rows to {argv[2]}")
    if merged:
        print(f"  {merged} input rows merged into an existing (date, campaign, creative) grain")
    print(f"  conversion_action: {raw['conversion_action']} — one action per file, by contract")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
