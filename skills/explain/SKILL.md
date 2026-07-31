---
name: explain
description: Explain an advertising term, metric, status or account behaviour to someone without a marketing background — using their own data. Use for "what does this mean", "why is it like this", "what is X", "is this normal or not".
---

# Explain

The user is learning as they go. The job is not to recite a textbook definition but to explain this specific thing against their numbers, so that next time they recognise it themselves.

Read `${CLAUDE_PLUGIN_ROOT}/CONVENTIONS.md` first and follow it.

## Answer structure

Four parts, always in this order:

**1. What it is** — one or two sentences, no jargon. If the term cannot be explained without another term, explain that one first.

**2. What it looks like in our account** — substitute real numbers from the data. If the data is missing, say so plainly and file a gap. Do not fall back to generic illustrations.

**3. Why this usually happens** — several competing causes, each labelled HYPOTHESIS until tested against data. Several, not one: the user must see that explanations compete.

**4. What it changes** — which decision depends on this number and what to look at next. If it changes nothing, say that too; it is worth knowing.

## Rules

**Never dress a heuristic as a measurement.** "CPL is usually higher on cold audiences" is a HYPOTHESIS about the market, not a measurement of their account. The difference must be visible in the wording.

**Do not simplify into something false.** "There's a nuance here, we'll come back to it when it matters" beats a convenient untruth that has to be un-taught later.

**Read the API, not memory.** Platform rules change — Meta retuned learning-phase exit thresholds in spring 2026. Where a field exists (`learning_stage_info`, `dynamic_lp_*_threshold`, `primary_status_reasons`), take the value from there. Where the field is unavailable for that object, say "unknown" rather than substituting a general rule.

**Separate "this is how the platform works" from "this is how it is here."** The first is verifiable in documentation, the second only in data.

## Three levels of trust when explanation turns into advice

Label the source every time:

1. **Your own history** — "this was tested in project-a, exp-2026-03-14, here's the outcome"
2. **The platform recommends it** — always with the note that the platform has a conflict of interest, plus our accumulated track record of its past recommendations if we have one
3. **General heuristic** — the weakest level; usable only as raw material for a hypothesis to test

## Side effect

If an explanation runs into missing data, that is a finding, not a dead end. File it through the `gaps` skill: a question the user asked themselves points at what the system lacks more accurately than any pre-written checklist.
