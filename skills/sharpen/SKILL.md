---
name: sharpen
description: Interrogate a campaign, goal, ICP or hypothesis until it is sharp enough to test — grounded in what the account actually says. Use for "who is this campaign even for", "what counts as a result here", before launching anything, setting a target, or whenever a statement sounds vague ("let's try a new audience", "we want more leads").
---

# Sharpen

The cheapest way to waste a budget is to launch something phrased vaguely. "Let's try a new audience" and "we want more leads" are untestable: a month later nobody can say whether it worked.

This skill is **interactive**. Never invoke it from a routine — there is nobody there to answer.

Read `${CLAUDE_PLUGIN_ROOT}/CONVENTIONS.md` first and follow it.

## Read before you ask

**Pull the object's real settings before the first question.** Objective, optimisation goal, targeting, custom audiences, automation flags, conversion event, budget, and when that conversion event last fired. Everything below is asked against that, not in the abstract.

**Never ask an open question the account can already answer.** The person answering is not a marketer. "Who is this campaign for?" is unanswerable; the same question with three concrete options drawn from the targeting is answerable in five seconds.

Derive the options. Two to four, plain language, no jargon. Where the settings and the name disagree, make that the choice:

> This ad set is named `Website Retargets`. Who does it actually reach?
>
> 1. Instagram followers and site visitors from the last 60 days — that is what the audiences say
> 2. Anyone in the US aged 20–45 — that is what actually happens, because audience expansion is on and the list is not binding
> 3. I don't know

Always include an honest "I don't know" option. It is a real answer, and it tells you more than a guessed one.

Ask in the user's language — the options above are written in English only because this file is. Their content comes from the account, not from a template.

**The gap between intent and settings is the finding.** A campaign named "Leads" optimising for link clicks, an ad set named "Retargets" with audience expansion on — these are not misunderstandings to correct politely. Record each one.

## How to interrogate

**One question at a time.** Twelve questions in one block produce twelve shallow answers. Ask, wait, follow the answer.

**Follow the weakest answer, not the checklist order.** If they named a metric but not where the target value came from, dig there — do not move on to the next bullet.

**Do not accept a generic first answer.** "Newlyweds 25–35 who value quality" describes everyone. Push: what separates these people from those who will **not** buy.

**Exit on the checklist, not on question count.** Stop when the artifact passes. That may take three questions or fifteen.

**The conversation must end in a file, and the file must be committed.** That is what separates sharpening from chatting. Not written down, did not happen; not committed, the next session will not find it.

**If the data to answer does not exist, do not invent it together.** File a gap and record in the artifact that the value was set without data behind it.

---

## Mode `campaign` → `campaigns/<account>-<campaign>.md`

For a campaign that already exists — running or paused. The point is not to judge its results; it is to establish what it is for, and whether it is set up to be judged at all.

Passes when all present:

- [ ] **who it actually reaches** — not who the name implies. If automation is allowed to leave the stated audience, the honest answer is the wider one
- [ ] **what counts as a result** — the specific conversion event, named. "Leads" is not an answer; `Lead / PageView contains "thanks"` is
- [ ] **that event fired recently** — check `last_fired_time` against the others on the same pixel. A conversion silent for weeks while its neighbours fire daily is broken, not idle
- [ ] **how many results per month, at what price** — the plan, with the number it came from
- [ ] **on which day of the month it becomes clear the plan is missing** — a date, computed from budget and pace
- [ ] **what happens on that day** — who does what

The last two exist because "we'll see how it goes" is how a budget disappears without anyone being able to name the moment it went wrong.

**If there is no conversion event on the campaign, stop.** Do not proceed to targets and pacing — there is nothing to count them in. Say so plainly, record it, and make attaching an event the only next step.

**Verify the event is alive before building anything on it.** This is not paranoia: a rule that stops matching (a renamed thank-you page, a redeployed domain) fails silently, the campaign keeps spending, and every report shows a plausible number for something else.

**Pending intents come first.** Read `pending.md` and settle what is open before interrogating anything new — the rule, the ranking and the write-back are §12b. Do not open a duplicate record: the detected one is the record.

---

## Mode `goal` → `goal.md`

Passes when all present:

- [ ] a metric with a number, not "more" or "better"
- [ ] a date by which we check
- [ ] a constraint: budget ceiling, cost-per-result ceiling, or minimum volume
- [ ] the current value — what we are measuring from
- [ ] **what happens if we miss it**

The last item is the reality test. If the answer is "well, we keep working", it is a wish, not a goal, and no budget should be planned against it.

**Record separately where the target number came from.** If it is not derived from the observed range, mark it as a promise rather than a plan. That line is exactly where planning ends and hoping begins.

---

## Mode `icp` → `icp.md`

Passes when all present:

- [ ] the segment is described by an **event or trigger**, not demographics — what happened in this person's life that made them start looking
- [ ] a **targetable signal on each platform**: on search, what they type; on social, which audience and what stops the scroll
- [ ] the alternative they compare against. Often not a competitor but "do nothing" or "ask a friend"
- [ ] the objection that kills the deal
- [ ] how this segment differs from the one that will **not** buy

Rule: **push from description to signal.** A description that yields no targeting parameter and no creative angle is useless, however accurate it feels.

---

## Mode `hypothesis` → `experiments/<date>-<project>-<topic>.yaml`

Passes when all present:

- [ ] metric, direction, threshold in percent
- [ ] baseline and how it was computed — what we compare against
- [ ] minimum data: how many conversions and how many days
- [ ] decision date
- [ ] what else changes in the same period — honestly, including other people's edits
- [ ] **`if_confirmed` and `if_refuted` filled in, and different from each other**

The last item is the strongest filter and costs nothing. Ask it directly:

> What will you do differently if this is confirmed? And if it is refuted?

If both answers are the same, or "nothing", **do not run the experiment.** It will change no decision while spending money and weeks of learning phase.

The second strongest question: **how many conversions per week does this object currently produce?** If the answer is three, a 50-conversion threshold means four months to a verdict — so either the threshold changes or something larger gets tested. Compute this before launch, not a month in.

---

## Do not

- Telegraph the answer in the phrasing of the question
- Accept "roughly" where a number is required
- Skip a checklist item because "it's obvious"
- Turn the interrogation into a lecture — explaining is the `explain` skill's job; here you only ask
