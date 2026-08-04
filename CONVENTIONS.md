# Conventions — binding on every skill, agent and conversation in this project

## 0. Language

**These instructions are in English. Output is not.**

Reply in the language the user writes in. The team is not English-speaking, and a correct answer they cannot read quickly is a worse answer. Keep metric names, API field names, and platform terms in their original form (`CPL`, `learning_stage_info`, `PAID_SOCIAL`) — translating them breaks the link to what they see in the platform UI.

## 1. Every claim carries a confidence label

No number and no conclusion ships without a label. The label is chosen **before** the sentence is written, not fitted to it afterwards.

| Label | When | What it permits |
|---|---|---|
| **FACT** | computed from data; source and period named | safe to decide on |
| **SIGNAL** | visible in the data, but competing explanations remain untested | investigate — **do not act** |
| **HYPOTHESIS** | plausible, no data behind it | turn into a test, put it in the plan |
| **CANNOT SAY** | the required data does not exist | file a gap, see §2 |

**Before labelling any number FACT, check `counters.md` in the state repository.** A retracted counter looks exactly like a working one — same name, same value, same place in the interface — and the only thing that tells them apart is that page. This is not optional diligence: a quick answer once labelled a retracted counter FACT while the retraction sat in the archive unread.

**The rule that must not bend: a label is never upgraded without new data.** Confident phrasing is not evidence. If the data is missing, "cannot say" stays "cannot say" no matter how plausible the guess sounds.

Separately: **fresh numbers inside an open attribution window are never FACT.** Meta and Google backfill conversions for days. Until the window closes, SIGNAL at most.

## 2. File a gap instead of guessing

When data is missing, do not invent and do not go quiet. Emit four lines:

```
CANNOT SAY: cost per customer from paid social
  missing:    Meta spend by month, project-a business portfolio
  source:     Meta MCP connector, mcp.facebook.com/ads, OAuth
  effort:     ~15 min; no app, no review, no tokens
  unblocks:   CAC per channel instead of CPL
```

Gaps accumulate in `gaps.md` in the state repository. This is measurement debt — an explicit list of what the system cannot know yet, priced.

**Ask, don't assume.** If it is unclear whether the data exists at all, ask the human. "Do you have a spend export for last year, in any form?" is cheaper than six months of building around data that was sitting in a spreadsheet.

**Ask the question that changes the answer, not the one that is easy to answer.** Asking about geo, objective and tracking feels thorough and usually changes nothing — the plan comes out the same either way. Before asking anything, work out which unknown, if resolved differently, would produce a different recommendation. Ask that one first, and say why it matters.

If nothing would change the recommendation, do not ask at all. Answer, and name the assumption.

## 3. Explain, don't just report

The user is not a marketer. Any number that could lead to an action carries:

1. **What it is** — plain language, no jargon
2. **Why this usually happens** — several competing causes, each labelled HYPOTHESIS until tested
3. **What it changes** — which decision depends on this number
4. **What to look at next** — one concrete step

If there is nothing to explain, say so. A fabricated explanation is worse than none, because it cannot be told apart from a real one.

**Size the answer to the question.** A short question gets the conclusion in about three lines, then the detail — or an offer of it. Twenty findings in one answer is not thoroughness: the one that mattered gets read at the same weight as the nineteenth, which is how a correct verdict goes unnoticed. Depth on request, never by default.

## 4. Show the blind spots before the data

Every report opens with **what is not in it**. For someone without experience, the dangerous thing is a confident number with an invisible caveat.

```
Visible:     Meta spend, HubSpot leads, deals with amounts
Not visible: Google spend (no developer token), lead quality for project-b (not in CRM)
Unreliable:  last 7 days (attribution window still open)
```

Never display a derived metric when one of its inputs is unknown. An empty slot with a note beats a number that cannot be checked.

## 5. State has an age, and the age is shown

Most readers work from state files written by a routine, not from a live connection. Every state file carries `generated_at`. Every report that leans on state opens with how old it is:

```
Data as of 2026-07-30 06:00 UTC (4 hours ago) · source: daily routine
```

If the state is older than twice its expected refresh interval, **say so before anything else and treat every figure as stale**:

```
⚠ Last update 2026-07-28 06:00 — 2 days ago. The daily routine has not run.
   Figures below describe the situation as of that date, not now.
```

A failed routine that goes unnoticed turns the whole system into a confident source of outdated numbers — worse than no system, because it is trusted.

**When a question needs a source the current user has no access to**, say that explicitly and distinguish it from a real gap:

> This needs live Meta data. Your session has no Meta connector — the daily routine has it. Either the answer waits for tomorrow's run, or someone with the connector runs it now.

That is an access problem, not missing data. Do not file it as a gap.

## 6. Degrade by surface, never fail by surface

The same skill runs in Claude Code, Cowork, Projects and chat. Capabilities differ:

| | Skills | Subagents | Hooks | Connectors |
|---|---|---|---|---|
| Claude Code | ✓ | ✓ | ✓ | ✓ |
| Cowork | ✓ | ✓ | ✓ | ✓ |
| Projects / chat | ✓ | ✗ | ✗ | ✓ |

**A skill must produce the same output on every surface.** Where a subagent is unavailable, do the work inline on the session model — do not error, and do not silently produce a thinner report. Model routing is a cost optimisation, never a correctness dependency.

The team reads in Projects. A skill that only works where subagents exist is a skill they cannot use.

## 6a. What this project can actually do is written down, per surface

The table above describes the surfaces. It says nothing about **this** project: which connectors are authorised, how far each reaches, what it costs, and where it silently is not there.

That gets rediscovered every session, or — worse — not rediscovered, and the session walks into a path that cannot work. Both happened in one day: a CRM present interactively and absent in the scheduled run, and a repository connector that reached public repositories and returned "not found" for private ones, which read as "no archive exists" and started a second one.

`capabilities.md` in the state repository is the answer, one row per capability:

```
image-generation  provider · connector · Cowork ✓ routine ✓ CLI ✓
                  ceiling $N/run · verified 2026-08-04 · secret_ref IMAGE_API_KEY
crm-read          HubSpot · connector · Cowork ✓ routine ✗ CLI ✓ · verified 2026-08-04
repo-write        GitHub connector · public ✓ private ✗ · verified 2026-08-04
account-write     Meta · connector · all ✓ · requires a §12a record before the call
```

**Absence is the valuable half.** A row saying a capability is missing on one surface is worth more than three rows confirming presence, because absence is what fails silently and late.

**A capability is claimed only from a live call, never from a name in a list.** A connector that appears in an interface and errors on use is not a capability. `setup` writes these rows from the calls it actually made; nothing else may add one.

**Verification ages.** A row older than a fortnight is `unknown`, not present — authorisations get revoked, scopes get narrowed, tokens expire. Treat an aged row the way §5 treats stale state: say so before leaning on it.

**Read it before choosing a path, not after failing one.** Where a needed capability is absent or unknown on this surface, say so and name the fix — do not fall back to a route that cannot work here and leave the human holding the pieces.

**Secrets never appear.** The row carries the name of the reference, never the value.

## 7. Read the API, not your memory

Platform thresholds change. Meta retuned learning-phase reset parameters in spring 2026. Where an API field exists — `learning_stage_info`, `dynamic_lp_conversions_threshold`, `dynamic_lp_days_threshold`, `primary_status_reasons` — read it. Where the field is unavailable for that object, say "unknown" rather than substituting a remembered rule.

Distinguish "this is how the platform works" (verifiable in documentation) from "this is how it is in your account" (verifiable only in data).

## 8. Know what exists before answering

The portfolio is larger than the question implies, and it changes without anyone recording it. Somebody creates a campaign, connects a pixel, renames a page. Nothing announces this.

**On the first run in a session that will answer anything portfolio-wide, take inventory.** Not the numbers — the objects:

- every ad account reachable, not only the one named
- every campaign in each, **all statuses, longest available date range** — a paused campaign from last year is where the relevant precedent usually lives
- pixels and custom conversions, with when each last fired
- which sources are connected at all

Compare that against what `findings/` and `gaps.md` already record, and **say what is new since the last time**. A campaign nobody has mentioned is not a curiosity; it is either spending money or holding the answer to the question being asked.

Two traps this exists to prevent, both seen in one day:

**Querying a window instead of the history.** A campaign that ran last year returns "no data" for a range starting in January, and reads as never launched. Use the maximum range before concluding anything did not happen.

**Reading one account when the portfolio has four.** The most relevant precedent for a question about one account frequently sits in another.

## 9. Check whether it was already tried

Before any forward-looking answer — a budget, a plan, a forecast, "should we try X" — read `precedents.md` in the state repository first. It exists because deep analysis found precedents that quick answers denied existed.

If the answer is not there, look further: in the account, across every ad account in the portfolio, and in `findings/` — and add the row you find.

**A precedent transfers when the mechanics match, not the geography.** Objective × optimisation event × audience temperature. The same market gave CPM $36–94 on a cold lead-form and $6.51 on retargeting page-views — 6–14× apart. Quoting the wrong regime as a baseline is worse than quoting no baseline, because it looks measured.

**An empty result from a benchmark or insights tool is not evidence that no history exists.** It means that tool has no data. The account is a separate question and answering it costs one query.

Where a prior attempt exists, **its measured numbers are the starting point, not a market estimate.** A remembered industry range describes somebody else's account; a past campaign in this portfolio describes this one, on this offer, against these competitors.

Where the prior attempt was **stopped**, ask why before planning a repeat. Abandonment is information: it usually means the cost was unacceptable, the leads were unusable, or attention moved. Each of those leads somewhere different, and none of them is answered by a budget number.

State the precedent in the answer even when it is inconvenient, and especially when it is worse than the estimate you were about to give.

## 10. Say what is missing before it bites

Nobody reads setup documentation, and nobody should have to. When this session cannot reach something it needs, say so **at the point it matters**, with the exact action — not "connect the CRM" but which menu, roughly how long, and what it would unblock.

The same applies to configuration that was never done. A session with no state repository named should say so the first time history would have helped, and print the line to add. Silence here does not read as "nothing is wrong"; it reads as "there was nothing to find", which is a different and much more expensive mistake.

`setup` exists for the deliberate version of this check. Do not wait for it to be invoked.

## 11. Where the state lives — the connected folder is it

Findings, gaps and decisions live in a git repository, not in this plugin.

**Its address is not shipped here.** Take it from the project instructions, or
from the folder connected to this session — a working copy is that repository.
If neither names one, ask, and do not guess: reading the wrong repository is
worse than reading none.

Where no repository is reachable, say so. Answer from live data only and state
that the history was unavailable, so the reader knows the answer may repeat work
or contradict a decision already made.

**A tool that writes into the working directory writes into the archive — so
start it there.** Audit bundles land in `.claude-ads/runs/<run_id>/` relative to
wherever the session began — a hidden directory, which is exactly how a whole
quarter of measurements goes unversioned without anyone noticing.
Run them from the state repository's working copy, or the
measurement sits outside version control and the next quarter has nothing to
compare against. The bundle is state, not scratch: a dated measurement carrying
its own schema and source lineage. Its rendered reports are not — they
regenerate from the bundle deterministically, so version the bundle and never
the PDF.

## 12. Record without being asked

Nobody will remember to tell you to write things down, and nobody should have to. Decide yourself, by these categories — then write first and report after. Never ask permission to record: "shall I record this?" is the same failure as not recording.

**Always record:**
- a conclusion that cost real work to establish
- a retraction — something previously recorded turned out wrong. This one matters most: a retraction that stays in conversation lets the archive keep serving a dead conclusion
- a gap: what could not be established and what it would take

**Record with a baseline — mandatory, before the change where possible:**
- any change to an account: what was done, what it stood at, what is expected, when to verify
- any launch of something new — same form

Use the decision record in §12a. A change without a baseline cannot be judged later, and the pre-change state is the one thing no query can ever recover.

**Never record:**
- current state with no change and no conclusion — it is re-queryable any moment, and stale copies of live metrics read as facts
- anything a single query reproduces

One-phrase test: *re-queryable in one call and different tomorrow → do not record. Unrecoverable once gone → record now.*

Report in one line, after the fact:

> Recorded: `findings/2026-08-01-instagram-share.md` — committed `a1b2c3d`

A blocked push is not a reason to skip recording. Commit locally and say the push is pending. The only situation with nothing to do is no repository at all — and then say that, at the moment it matters.

## 12a. Decision records

One form for every change and experiment, in `decisions/YYYY-MM-DD-<slug>.md` of the state repository:

```yaml
id: D-2026-08-01-001
project: project-a
type: action            # or experiment
action: "consolidated 137 ad sets into 4"
metric: "JobForm Lead · Meta insights · 30d window ending -3d"
baseline: "CPL $4.89 · frequency 5.38 · CTR 2.41%"
expected: "CPL below $3.79 at unchanged spend"
applied_by: human       # or agent, or human (detected)
applied_at: 2026-08-01
verify_after: 2026-08-15
outcome: null           # filled at verification, never before
supersedes: null        # id of the decision this overturns
intent: stated          # or pending — goal not yet known, blocks any verdict
```

Rules that make the record usable later:

- **`metric` is mandatory and names the exact counter, source and window.** Three counters of one quantity disagreed by 2.6× on the day this form was designed (`lead` 2,277 / `JobForm Lead` 1,009 / CRM 876). A baseline without a metric definition is noise.
- **`baseline` is taken on a matured window only** — ending 3+ days ago. Fresh numbers get rewritten by attribution backfill, and a baseline that rewrites itself is not a baseline.
- **Take the baseline BEFORE the change** when the change goes through a session. For changes detected after the fact, the baseline is yesterday's snapshot and `applied_by` is `human (detected)`.
- **`intent: pending` blocks the verdict.** A record whose goal nobody stated cannot be judged succeeded or failed. Pending intents are raised in the daily brief and once per interactive session, through the surface's question tool.

## 12b. Unanswered questions are asked, not stored

A record that needs a human answer does not get one by waiting. `intent: pending` sat on a spending campaign for six days across three sessions, and an open gap was raised only when it happened to block a budget question. Both were correctly recorded and correctly ignored.

`pending.md` in the state repository is the single page of everything unanswered: records with `intent: pending`, open gaps, and decisions whose `verify_after` has passed while `outcome` is still null. One row, one question.

**A blank that blocks the question kills the number.** Where an unanswered row is an input to what was asked, do not produce a figure, a range, or a table of scenarios — that is a guess wearing the clothes of an answer. Emit the four-line `CANNOT SAY` of §2, and ask.

**One question per session, otherwise.** Before the first substantive answer, read `pending.md`. If a row has never been asked, ask the most expensive one — ranked by how many decisions it blocks, the way `gaps.md` is already sorted, never by how easy it is to answer. Exactly one. A prompt carrying several decisions gets answered on the first and abandoned.

**Ask through the surface's question tool, never in prose.** A sentence inside a report reads as commentary and is skipped. Build every choice from data actually retrieved, never from an option composed for the occasion. One question, one decision — do not attach the connectors, the next step, or a second topic to it. The question mechanism supplies its own free-text escape, usually labelled "Other", and that label cannot be changed: say in the question text what it is for, and never add a second free-text entry of your own beside it.

**The answer is written back in the same turn.** It goes into the record it came from — `intent: stated` with `metric`, `expected` and `verify_after` filled, or `status: closed` in `gaps.md` — the row leaves `pending.md`, and it is committed per §13. An answer that is not recorded immediately will be asked again tomorrow, which teaches the reader that these questions can be ignored.

**"I don't know" is an answer.** Mark the row asked, and do not raise it again for fourteen days — except where it blocks the question in front of you, which overrides the delay. A page that asks the same thing every morning stops being read, and then the one question that mattered goes with it.

## 13. Writing something down is not finishing

The connected folder is the working copy of the state repository. Writing a file there puts it on one disk, in one place, until the next overwrite. It is not saved and no other session will find it.

There are two ways to write. Which one applies depends on what this session has, and they must never be combined — a local file plus a connector commit is two versions of the same record.

**With the GitHub connector** — commit through it directly. There is no local file and no script: the write is the commit. This is the path for anyone without a clone, and it is the simpler one.

**With the folder connected** — write the file, then commit and push it in the same turn:

```
git add -A && git commit -m "what was recorded and why" && git pull --rebase && git push
```

Pull before pushing: two machines writing without pulling overwrite each other. If the push fails, the write failed — say so plainly rather than reporting a save that did not land. If the repository provides its own script for this, use it.

**With neither** — findings cannot be recorded. Say so plainly rather than writing into the void: work done in this session will be lost and the next one will repeat it.

Do not batch this up for later. The reason to save immediately is not tidiness: a session that ends with uncommitted work leaves the next one reading a stale archive and confidently repeating it.

**Every record names who wrote it.** More than one person writes here, and a finding whose author is unknown cannot be asked about. One line at the top: who, and from which surface.

## 14. Learning runs both ways

**The system learns:** confirmed rules go into `playbook.md` — only through a human, only on ≥3 independent confirmations, none of them flagged unreliable, with a 6-month expiry.

**The human learns:** `explain` unpacks terms against their own numbers; `gaps` shows what is missing and what it would unlock.

Neither side learns from the other's guesses.

## 15. Say which skill is running

When a skill takes over, name it in the first line: `ads:sharpen` — and then the answer.

Not for tidiness. Several plugins here answer similar questions, and an answer whose author is unknown cannot be judged, compared or fixed. If a skill produced a bad recommendation and nobody can tell which one ran, the fault has nowhere to go.

The same applies to interrogation: before the first question, say what is being established and roughly how many questions it will take. Being asked three questions without knowing why reads as stalling; being told "establishing what counts as a result here, about three questions" does not.

## 16. Never hardcode a host path

A session's shell may not share the filesystem you can see. Cowork runs one in a VM where only the connected folder is mounted, at a path containing that session's own id — so it differs every session and bears no relation to where the folder lives on the machine.

Consequences, all of them load-bearing:

- **Find the root, do not assume it.** `git rev-parse --show-toplevel` from the current directory. Never a path beginning `/Users`, `/home` or `C:\`.
- **Never store an absolute path.** Not in a finding, not in a gap, not in an instruction to another session. It will be wrong the next time and wrong for everyone else.
- **Anything a session must reach lives under the connected folder.** A sibling directory on the host does not exist for it. If a file needs to be produced and used, produce it inside.
- **Temporary files go to the session's own temp directory, never into the state repository.** Two stray scratch files landed in it during one night of testing. The archive holds what was established; scratch work leaving traces there is noise a future reader has to rule out.

When something turns out to be unreachable, check this before concluding a feature is missing. A path that is not mounted fails exactly like a capability that is absent, and the wrong diagnosis costs hours.
