---
name: export
description: Turn live connector reads into the portable CSV export that an audit can consume. Use before running any paid-media audit that needs account data, when an audit reports zero evidence or insufficient coverage, or for "prepare the data for the audit", "export the account", "why does the audit say it has no data".
---

# Export

An audit tool reads **exports**, not your connector. A live connection and an
audit are two different things, and the gap between them is silent: the audit
does not say "you gave me nothing", it reports zero coverage and stops. That
already happened here once, and the run sat unread as `needs_input` for five
days.

This skill closes that gap. It produces one file, in the exact shape the
consuming adapter validates, from data pulled through the connector.

## What the format allows, and what it therefore forbids

Thirteen columns, one row per **(date, campaign, creative)**:

```
date, account_id, account_name, campaign_id, campaign_name, campaign_status,
creative_id, creative_name, conversion_action, conversions, budget, spend, currency
```

Four constraints decide everything else. They are not style — the adapter
rejects the whole file when any is broken:

- **One account per file.** One `account_id`, one `account_name`, one currency.
  A portfolio of four accounts is four files, never one.
- **One conversion action per file.** `conversion_action` is not part of the row
  grain, so two actions on the same day, campaign and creative collide. Pick the
  canonical counter and say which it is.
- **The grain is unique.** Several ads may run the same creative; their spend
  belongs to one row and must be summed before writing. Repeated grains are
  rejected, not merged, and not silently double-counted.
- **One budget per campaign per day.** Two different values for the same
  campaign-day fail the file.

## Procedure

**1. Choose the conversion action from `counters.md`, not from the interface.**

This is the step that makes the export worth trusting. The account will offer
several counters for one quantity; at least one of them is usually retracted and
looks identical to a working one. Take the canonical counter for the goal being
measured, and name it in the report. If `counters.md` has no row for this goal,
say so and stop — an export built on an unverified counter produces an audit
whose every number is wrong in the same direction.

**2. Pull the numbers, day by day, at ad level.**

Daily granularity, ad level, over a matured window ending at least three days
ago. Fresh days inside an open attribution window get rewritten, and an export
is a fixed artifact — it does not update itself later.

Then map each ad to its creative. Fetch creative fields **by id**: a listing
call returns only `id`, `name`, `status` and omits the rest, and an empty field
in a listing is not evidence that the field is empty.

**3. Write the raw pull to the session's temporary directory.**

Never into the state repository — it is working material, not a record.

```json
{
  "platform": "meta",
  "account_id": "...", "account_name": "...", "currency": "USD",
  "conversion_action": "<canonical counter from counters.md>",
  "rows": [
    {"date": "2026-07-01",
     "campaign_id": "...", "campaign_name": "...", "campaign_status": "ACTIVE",
     "creative_id": "...", "creative_name": "...",
     "spend": "12.34", "conversions": 3, "budget": "20.00"}
  ]
}
```

One entry per ad per day. Do not merge anything by hand — that is the script's
job, and it is the part that must be checkable.

**4. Build the file.**

```
python3 "${CLAUDE_PLUGIN_ROOT}/skills/export/scripts/build-export.py" <raw.json> <out.csv>
```

It sums the rows that share a grain, refuses anything it cannot compute without
guessing, and prints what it merged. A refusal names the offending row. Do not
work around a refusal by editing numbers: every rule it enforces is one the
adapter enforces afterwards.

Write the result beneath `.claude-ads/exports/` in the state repository, named
`<platform>-<account_id>-<start>_<end>.csv`. The directory is hidden, which is
how a quarter of measurements goes unversioned without anyone noticing — check
that it is not ignored.

**5. Report what the file contains and what it cannot.**

Account, window, row count, rows merged, the counter used, and the counter's
known fragility if `counters.md` records one. An export inherits every weakness
of the counter it was built from, and the audit downstream cannot see that.

## Where there is no shell

Some surfaces have no Bash. The rules above still hold and can be applied by
hand, but the arithmetic is then unverified: label the resulting numbers SIGNAL,
never FACT, and say plainly that the merge was done without the checker. Do not
skip the export and let the audit run empty — an audit with no evidence is worse
than no audit, because it produces a confident-looking report about nothing.

## What this does not do

It does not run the audit, score anything, or write findings. It produces one
input file. What the audit concludes from it arrives as SIGNAL and is only
raised to FACT under the usual rules — a schema-valid finding is not a true one,
which the consuming tool states about itself.
