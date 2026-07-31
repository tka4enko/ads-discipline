# ads-discipline

A Claude plugin for working on paid advertising accounts without a full-time
analyst — for people who have to act on numbers they cannot personally audit.

It is not a reporting tool. It exists to make an answer **checkable**.

## What it changes

Once installed, every answer follows a few rules that hold whether or not a
skill was invoked:

- **Each claim is labelled** — FACT, SIGNAL, HYPOTHESIS or CANNOT SAY. A label
  is never upgraded without new data, and confident phrasing is not evidence.
- **Missing data is named, not filled in** — what is missing, where it could
  come from, what it would cost, what it would unlock.
- **Blind spots come before numbers** — what is visible, what is not, what is
  unreliable, stated first.
- **No invented benchmarks.** A conventional threshold is called conventional,
  not measured.
- **It does not agree by default.** Where the data contradicts what you assume,
  it says so and shows the numbers.
- **It checks whether you already tried this.** Before any forward-looking
  answer, it looks for the earlier attempt — a measured precedent in your own
  account beats a remembered industry range, and an abandoned test is a question
  before it is a data point.

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
