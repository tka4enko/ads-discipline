---
name: daily
description: The daily routine - snapshot what nothing can recover, diff against yesterday, record detected changes with baselines, raise decisions due for verification, write the brief. Run by a scheduled task, or by hand with "run the daily routine". Not interactive - it asks nobody anything; what it cannot answer goes to pending.md for the next interactive session to raise.
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

## 5a. Landing pages — weekly, or when a creative's link changes

Once a week, and whenever the diff shows a new or changed ad link: fetch each distinct landing URL the live ads point at and record a content fingerprint (title + form field count + presence of the thank-you path) in the snapshot.

A changed fingerprint on an unchanged ad is worth a brief line: the page moved or was rewritten under a running campaign, which is how a conversion rule silently stops matching. This is the cheapest available cover for the class of failure that has already happened here twice — a rule pinned to an exact URL, and a rule matching a path that no longer exists.

Read-only. Never submit a form, never follow a call-to-action that performs an action.

## 5b. Rebuild `pending.md`

One page at the repository root holding everything that needs a human answer. Rewritten in full each run, from three sources and no others:

- `decisions/*.md` with `intent: pending`
- `gaps.md` entries with `status: open`
- `decisions/*.md` where `verify_after` has passed and `outcome` is still null

Each row carries: the record id, the question in one sentence, what it unblocks, the date it has been waiting since, `asked_at`, and `answer_state` — one of `never_asked`, `unknown`, `answered`.

**Carry `asked_at` and `answer_state` across the rebuild.** They live only here; regenerating them as `never_asked` re-asks a question the human already declined, which is exactly the behaviour §12b forbids. Rows whose source record is gone — gap closed, intent stated — drop out.

Order by how many decisions the row blocks, most first. That ordering is what §12b consumes when it picks the single question to ask.

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
- never ask anything interactively — the routine has no human; it only writes `pending.md` so that the next interactive session asks
