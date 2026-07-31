---
name: orient
description: Establish what the account can and cannot currently be trusted to tell you — which sources are connected, which conversion counters are still firing, which numbers are unusable and why. Use when asked "what's going on", "where are we", "what do we actually see", "is anything broken", or before trusting any performance figure. This is the measurement-health view; for pacing and delivery performance use a monitoring skill instead.
---

# Orient

The main screen — but not a performance report. It answers a narrower and more important question: **which of these numbers is allowed to be believed today.**

Performance skills assume the measurement works. This one checks that assumption, and it runs first for that reason: a confident figure computed from a dead counter is worse than no figure, because nothing about it looks wrong.

Read `${CLAUDE_PLUGIN_ROOT}/CONVENTIONS.md` first and follow it literally — especially the confidence labels and the blind-spots-first rule.

## Procedure

1. Read `portfolio.yaml` from the state repository — projects and accounts
2. Determine which sources are actually connected right now (Meta MCP, Google Ads MCP, GA4 MCP, HubSpot). Do not assume — verify with a call
3. Gather the raw numbers. **Degrade gracefully by surface:**
   - Where subagents are available (Claude Code, Cowork), delegate to the `collector` agent
   - Where they are not (Projects, chat — subagents are greyed out there), gather inline on the session model
   The output must be identical either way. A skill that only works on one surface is a skill the team cannot use.
4. Assemble the report in the order below

## Output structure

### Block 1 — Coverage. Always first

```
WHAT IS VISIBLE RIGHT NOW

              spend     leads    lead quality    revenue
project-a   ✗ Meta    ✓ CRM    ✓ CRM           ✓ CRM
project-b       ✗ Meta    ✗ GA4    ✗ not in CRM    ✗
landings      ✗ Meta    ✗ GA4    ✗ not in CRM    ✗

Not connected: Meta (3 business portfolios), Google Ads (no developer token), GA4
```

The holes must be seen before the numbers. Otherwise a partial picture reads as a complete one.

### Block 2 — Are the counters still alive

Before any number. A conversion rule that stops matching does not raise an error: the campaign keeps spending, the interface keeps showing a plausible figure for something else, and every report built on it is quietly wrong.

For each conversion event the account defines, read when it last fired, and compare it against **its neighbours on the same pixel**. Absolute silence means little on its own; silence while the events beside it fire daily is a broken rule.

```
COUNTERS · pixel <id>
  Product page A             fired today
  Product page B             fired today
  Blog                       fired today
  Lead  (URL contains "thanks")   last fired 60 days ago  ⚠

  The site is receiving traffic and the CRM is still creating contacts,
  so the action has not stopped. The rule has stopped matching it.
```

Also check, for every campaign that is spending:

- **is a conversion event attached at all** — an objective of link clicks or landing page views means nothing downstream is being counted
- **is the rule fragile** — exact URL match breaks on any appended parameter; a temporary or auto-generated domain breaks on the next deploy
- **does the optimisation event match the stated purpose** — a campaign named for leads that optimises for page views will never learn to produce leads

Any of these outranks every performance finding below. Report them here, not in Block 4.

### Block 3 — Numbers

Per project, where data exists. Every line carries a confidence label.

Where the loop is closed (spend, leads and quality all present), show the whole chain:
```
spend → leads → qualified → customers → revenue
```

Where it is broken, show what exists and **state explicitly what is missing from the chain**:
```
project-a · Jan–Jul 2026
  leads by channel (CRM)        FACT
  customers by channel (CRM)    FACT
  spend                         CANNOT SAY → gap-001
  → CPL and CAC cannot be computed
```

Never show CPL when either the numerator or the denominator is unknown.

### Block 4 — What needs attention

Ranked by cost of being wrong, not by size of deviation. Each item:

```
[label] One-line headline
  observed:  the numbers
  meaning:   in plain language
  action:    a concrete step, or "nothing yet — watching until <date>"
```

Order: money being spent right now → decisions that have matured → observations. Broken measurement does not appear here — it belongs in Block 2, above the numbers it invalidates.

**If there is nothing to report, say so.** "No deviations outside the normal range" is a valid and useful answer. Never invent items to fill the block.

### Block 5 — Gaps

The three most expensive open gaps from `gaps.md`, each with one line on what it would unlock. Full list via the `gaps` skill.

## Prohibited

- Presenting a HYPOTHESIS in the grammar of a FACT
- Showing a metric when one of its inputs is unknown
- Treating numbers inside an open attribution window as final
- Recommending that a channel be stopped or scaled when its spend is unknown
- Padding empty blocks for the sake of a complete-looking report
