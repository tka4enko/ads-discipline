# ads-discipline

A Claude plugin that makes ad spend **verifiable** for people running paid
advertising without a full-time analyst: every number carries a source, every
change a baseline, every promise a verification date.

It does not optimise campaigns. It makes every claim about them checkable —
and every failure impossible to miss. Built against one failure mode: an
analyst who spent the budget, promised results, and left nothing that could
be verified.

## What it can do

**Tell knowledge from guesswork, in every answer.** Each figure is labelled
FACT / SIGNAL / HYPOTHESIS / CANNOT SAY; a label is never upgraded without new
data; fresh numbers inside an open attribution window are never FACT; no
invented benchmarks; no agreeing with you against the data.

**State what it does not know — before what it does.** Reports open with blind
spots: visible, not visible, unreliable. Missing data becomes four lines — what,
where from, at what effort, unblocking what — in a priced register of gaps.

**Check the measurement before the conclusions.** Whether conversion counters
still fire, compared against their neighbours on the same pixel; fragile rules
(exact-URL matches, temporary domains); optimisation events that contradict the
campaign's stated purpose; platform counts reconciled against the CRM.

**Remember — and know what it remembers.** Findings, decisions and gaps live in
a git repository; the next session starts from them, not from zero. A retracted
conclusion gets a forward pointer, so the archive never serves stale claims as
current. Before any plan it checks whether this was already tried: a measured
precedent in your own account beats a market estimate.

**Give a lever instead of a promise.** A daily snapshot of what nothing can
recover retroactively — targeting, attribution settings, counter rules. A
hand-made change in the ads manager gets detected, with its baseline taken from
yesterday's snapshot. A change without a stated goal gets a question, not
silence. Verification dates come due on their own.

**Interrogate until testable.** "Who is this campaign for" is asked with options
derived from the actual settings; a mismatch between a campaign's name and its
configuration is a finding; a goal is not accepted without a metric, a number,
a deadline — and the day of the month when it becomes clear the plan is missed.

**Explain without jargon**, on your own numbers: what a metric is, why it moves,
which decision depends on it, what to look at next.

**Install without expertise.** `ads:setup` verifies every source by calling it,
names the single next action for each gap, and asks its one blocking question
as a question — not as a sentence at the bottom of a report.

## What it deliberately does not do

- **Change campaigns.** It reads. Edits are made by people.
- **Decide.** It finds and verifies; decisions stay yours.
- **Replace checking.** It makes checking possible in one query — every claim
  names its source and period.

## Skills

| Skill | For |
|---|---|
| `ads:orient` | Which of these numbers can be believed today — connected sources, conversion counters still firing, what is unusable and why |
| `ads:sharpen` | Interrogates a campaign, goal, ICP or hypothesis until it is testable, using options derived from the account rather than open questions |
| `ads:explain` | Explains a term, metric or account behaviour to someone without a marketing background, using their own data |
| `ads:gaps` | Registry of what is missing, where to get it, and what each gap unblocks |

Three subagents ship alongside: a retrieval-only collector, a diagnoser, and a
judge for decisions whose cost of error is measured in months.

## Connectors

The plugin brings two, both official hosted MCP servers behind OAuth. Enabling
the plugin offers the connection; the first call prompts for authorisation.
No credentials travel with the plugin and none are stored in it.

| Connector | Gives | Also needs |
|---|---|---|
| **Meta Ads** — `mcp.facebook.com/ads` | Campaigns, spend, creatives, audiences, pixels, conversion rules | Access to the ad accounts, granted in Meta Business Manager by whoever owns them. OAuth binds to one business portfolio — connect once per portfolio |
| **HubSpot** — `mcp.hubspot.com/anthropic` | Contacts and deals by source: the independent count of what advertising produced | Access granted by the CRM owner |
| **GitHub** — `api.githubcopilot.com/mcp/` | Reads and writes findings and gaps without a local clone — a write through it is a commit | The repository named in your project instructions, and access to it |

**Why the CRM matters more than it looks.** Platform-reported conversions cannot
check themselves. A rule that stops matching a renamed page keeps returning a
plausible number, and only an outside count reveals it. Connect both or expect
to trust one source with no way to audit it.

**Google Ads is not included and cannot be.** Its API requires a developer token
issued per advertiser, which takes weeks. `ads:setup` reports it as a known
long-lead gap rather than a misconfiguration.

Run `ads:setup` at any point to see what is connected, what is not, and the
exact next action for each gap.

## Install

```
/plugin marketplace add tka4enko/ads-discipline
/plugin install ads@ads-discipline
```

In Claude Cowork, add the marketplace through the plugin manager and install
`ads` from it.

## State

The plugin holds no account data and names no repository. If you keep findings
and gaps in git, name that repository in your project instructions:

```
Project state: owner/repo
findings/, gaps.md and docs/ live there — what has been established and what
was retracted. Read it before answering; record new findings there.
```

Without it the skills still work; they simply answer from live data and say the
history was unavailable.

## Why the rules are shaped this way

Each one comes from a specific failure, not from theory.

A campaign was judged healthy against a benchmark invented mid-sentence. A
conversion counter matched a renamed thank-you page and silently stopped firing
while spend continued and every report kept showing a plausible number for
something else. A budget was planned from a market average while the same
portfolio held four measured tests of the same thing, in the same market, at
twice the estimated cost — abandoned, and nobody asked why.

None of those look like errors in the output. That is the problem the rules
address.

## License

MIT
