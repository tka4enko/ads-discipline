---
name: gaps
description: Registry of data gaps — what is missing to reach a conclusion, where to get it, and what it would unlock. Use when asked "why can't you tell", "what data is missing", "what should we connect", or whenever another skill hits a missing source.
---

# Data gaps

The system is required to know what it does not know and to name it. This skill maintains the measurement debt: questions that cannot be answered yet, each priced.

Read `${CLAUDE_PLUGIN_ROOT}/CONVENTIONS.md` first and follow it.

## When a gap is filed

The moment any skill hits CANNOT SAY. Immediately — a gap not written down is forgotten, and a month later the same question hits the same wall from scratch.

## Record format in `gaps.md`

```yaml
- id: gap-001
  question: "What does acquiring a customer from paid social cost in project-a?"
  missing: "Meta spend by month, project-a business portfolio"
  source: "Meta MCP connector → mcp.facebook.com/ads, OAuth to the portfolio"
  effort: "~15 min; no developer app, no App Review, no tokens"
  unblocks: "CAC per channel instead of CPL; comparing channels by money rather than by cost per form fill"
  blocks: [orient, daily, plan]
  status: open
```

`unblocks` is mandatory. A gap with no answer to "what decision does this enable" does not get filed — it means the data is wanted out of curiosity, not for a decision.

## What the skill does

**List** open gaps sorted by how many decisions they block, not by how easy they are to close.

**Ask rather than assume.** If it is unknown whether the data exists at all, ask. Be specific — name the source, the period, and the payoff:

> Do you have a Meta spend export for 2025, in any form, even a spreadsheet? If so we can compute the baseline today instead of waiting on connectors.

A bad question is "do you have historical data?". A good one names what, from where, and what it buys.

**Offer the cheap path when one exists.** Data is often reachable more cheaply than it looks: a one-off manual export instead of a connector, a neighbouring period instead of the exact one. Always flag it — data obtained by a workaround yields SIGNAL at most, never FACT.

**Close the gap** when the source lands: change the status, record the date, and **recompute the conclusions that depended on it**. A gap closed without recomputation leaves stale "cannot say" answers in the system.

## Do not

- File gaps for data wanted "just in case"
- Estimate effort optimistically — if a source needs a token with multi-week approval, write that
- Close a gap silently on partial data. Spend for 3 months out of 12 is a new gap, not a closed one
