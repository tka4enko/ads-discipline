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

Before any forward-looking answer — a budget, a plan, a forecast, "should we try X" — look for the previous attempt. In the account, across every ad account in the portfolio, and in `findings/`.

**An empty result from a benchmark or insights tool is not evidence that no history exists.** It means that tool has no data. The account is a separate question and answering it costs one query.

Where a prior attempt exists, **its measured numbers are the starting point, not a market estimate.** A remembered industry range describes somebody else's account; a past campaign in this portfolio describes this one, on this offer, against these competitors.

Where the prior attempt was **stopped**, ask why before planning a repeat. Abandonment is information: it usually means the cost was unacceptable, the leads were unusable, or attention moved. Each of those leads somewhere different, and none of them is answered by a budget number.

State the precedent in the answer even when it is inconvenient, and especially when it is worse than the estimate you were about to give.

## 10. Say what is missing before it bites

Nobody reads setup documentation, and nobody should have to. When this session cannot reach something it needs, say so **at the point it matters**, with the exact action — not "connect the CRM" but which menu, roughly how long, and what it would unblock.

The same applies to configuration that was never done. A session with no state repository named should say so the first time history would have helped, and print the line to add. Silence here does not read as "nothing is wrong"; it reads as "there was nothing to find", which is a different and much more expensive mistake.

`setup` exists for the deliberate version of this check. Do not wait for it to be invoked.

## 11. Where the state lives

```
tka4enko/project-a-ads
```

Everything this system has established lives there — `findings/`, `gaps.md`, `docs/`. Read it before answering anything the account cannot answer on its own: what was already established, what was already retracted, what is already known to be missing.

Reach it whichever way this session can:

- **the connected folder** is a working copy of that repository — read the files directly
- **the GitHub connector** reads the same repository without a local copy
- **neither** — say so. Answer from live data only and state that the history was unavailable, so the reader knows the answer may repeat work or contradict a decision already made

Do not go looking through other repositories. This is the only one.

## 11. Writing something down is not finishing

The connected folder is the working copy of the state repository. Writing a file there puts it on one disk, in one place, until the next overwrite. It is not saved and no other session will find it.

There are two ways to write, and which one applies depends on what this session has.

**With the folder connected** — write the file, then immediately run:

```
bin/save.sh "what was recorded and why"
```

That pulls, commits and pushes. If it fails the script says so loudly. Treat a failed push as the write having failed, not succeeded, and say so in the answer.

**With the GitHub connector instead** — commit through the connector directly. There is no local file and no script: the write is the commit. This is the simpler path and the right one for anyone who does not want git on their machine.

Never use both in one session. Writing a local file *and* committing through the connector produces two versions of the same record.

Do not batch this up for later. The reason to save immediately is not tidiness: a session that ends with uncommitted work leaves the next one reading a stale archive and confidently repeating it.

**Every record names who wrote it.** More than one person writes here, and a finding whose author is unknown cannot be asked about. One line at the top: who, and from which surface.

## 12. Learning runs both ways

**The system learns:** confirmed rules go into `playbook.md` — only through a human, only on ≥3 independent confirmations, none of them flagged unreliable, with a 6-month expiry.

**The human learns:** `explain` unpacks terms against their own numbers; `gaps` shows what is missing and what it would unlock.

Neither side learns from the other's guesses.

## 13. Say which skill is running

When a skill takes over, name it in the first line: `ads:sharpen` — and then the answer.

Not for tidiness. Several plugins here answer similar questions, and an answer whose author is unknown cannot be judged, compared or fixed. If a skill produced a bad recommendation and nobody can tell which one ran, the fault has nowhere to go.

The same applies to interrogation: before the first question, say what is being established and roughly how many questions it will take. Being asked three questions without knowing why reads as stalling; being told "establishing what counts as a result here, about three questions" does not.
