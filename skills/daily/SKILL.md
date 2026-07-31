---
name: daily
description: The daily routine - snapshot what nothing can recover, diff against yesterday, record detected changes with baselines, raise decisions due for verification, write the brief. Run by a scheduled task, or by hand with "run the daily routine". Not interactive - it asks nobody anything; questions it cannot answer become intent-pending records for humans to settle later.
---

# Daily routine

Runs unattended. Its writes ARE the deliverable: the skill is not done until the files exist in the state repository. Data commits before the brief renders — if the brief fails, history is already saved.

The state repository is reached per CONVENTIONS §11: the connected folder's working copy, or the GitHub connector. With neither, this run is a loud failure — report it; never pretend a snapshot happened.

## 1. Read state

Pull (folder) or read fresh (connector): previous snapshot `snapshots/*.json` (latest), all `decisions/*.md`, `gaps.md`.

## 2. Snapshot → `snapshots/YYYY-MM-DD.json`

For every reachable ad account, with the metric window **30 days ending 3 days ago**:

```json
{
  "generated_at": "YYYY-MM-DD",
  "window": {"since": "YYYY-MM-DD", "until": "YYYY-MM-DD"},
  "accounts": [{
    "id": "", "name": "", "currency": "",
    "campaigns": [{"id": "", "name": "", "status": "", "objective": "",
      "optimization_event": "", "budget": "",
      "metrics": {"spend": 0, "impressions": 0, "ctr": 0, "cpm": 0,
                  "frequency": 0, "results": 0}}],
    "adsets": [{"id": "", "name": "", "campaign_id": "", "status": "",
      "daily_budget": "", "attribution_setting": "",
      "targeting": {"geo": [], "age": "", "interests_count": 0,
                    "advantage_audience": false, "expansion": false},
      "ads": [{"id": "", "creative_id": ""}]}],
    "conversions": [{"id": "", "name": "", "rule": "", "last_fired": ""}],
    "pixels": [{"id": "", "name": "", "events": {}}]
  }]
}
```

The ad set block is not optional decoration: audience-expansion flags, attribution settings and the ad→creative map are exactly the fields that explained every finding on the day this was designed, and none of them is recoverable retroactively.

**A partial snapshot is forbidden.** If Meta does not respond, write no snapshot file at all and put the reason in the brief — an empty or partial snapshot reads later as "those campaigns did not exist".

## 3. Diff against the previous snapshot

Report, in this order of severity:

1. **counter silent ≥3 days while siblings on the same pixel fire** — a broken rule, not idleness
2. **conversion rule text changed** — additionally scan open decisions: any with this counter in `metric` gets flagged in the brief as *comparability lost: baseline measured under the old rule*
3. campaigns appeared / disappeared / status changed
4. budgets changed (campaign or ad set)
5. targeting changed: geo, age, interests_count, advantage_audience, expansion
6. attribution_setting changed
7. ads whose creative_id changed

## 4. Detected changes → decision records

Every diff item of classes 2–7 with no existing record in `decisions/` mentioning that object id → create `decisions/YYYY-MM-DD-auto-<slug>.md` using the §12a form:

- `baseline`: the relevant numbers from YESTERDAY's snapshot
- `applied_by: human (detected)`
- `intent: pending`
- `verify_after`: today +14 days
- `expected`: leave literally as `unknown — intent pending`

Never guess intent. The goal of a change lives in the head of whoever made it; inventing one poisons the later verdict.

## 5. Verification sweep

Every record with `verify_after ≤ today` and `outcome: null` goes into the brief's "due" section with its `metric`, `baseline` and `expected` restated, so the reader can judge without opening files.

## 6. Brief → `briefs/YYYY-MM-DD.md`

First line, always, before anything:

> Last successful snapshot: YYYY-MM-DD (N days ago)

If N > 1, this line is a warning and leads. Then, only non-empty sections, in this order:

1. **Needs your answer** — intent-pending records, each as one question: "Campaign X appeared with budget $Y — what is it for: how many, at what price, by when?"
2. **Comparability lost** — from diff class 2
3. **Due for verification** — from step 5
4. **Changed since yesterday** — the rest of the diff, one line each
5. **Counter health** — silent counters, fragile rules seen
6. If nothing at all: "No changes, nothing due." — a real answer, never padded

## Failure rules

- Meta unreachable → no snapshot; brief says why; task result is a failure
- state repository unwritable → the run failed, say so loudly; there is no such thing as a successful run that wrote nothing
- never ask anything interactively; unanswerable questions become intent-pending records
