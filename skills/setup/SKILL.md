---
name: setup
description: Check what this session is missing and print exactly how to fix it — which connectors respond, whether a state repository is named and reachable, and what each missing piece would unblock. Run this first on a new machine, a new surface, or when an answer says it cannot see something. Use for "what do I need to connect", "why can't you see my account", "am I set up", "where do I put the repository".
---

# Setup

Run first, on a new machine or a new surface. Nothing else in this plugin announces what it is missing; this does.

The output is a checklist the reader can act on without knowing how any of it works. No diagnosis, no advice about advertising — only what is connected, what is not, and the exact next action for each gap.

## Procedure

**Verify, do not assume.** For each source below, make a real call. A connector that appears in a list but errors on use is not connected, and saying otherwise is worse than saying nothing.

### 1. Data sources

| Source | How to check | If missing |
|---|---|---|
| **Meta Ads** | list ad accounts | Settings → Connectors → Meta Ads. Needs access to the ad accounts, granted in Meta Business Manager by whoever owns them |
| **CRM** | one aggregate query, counts only | Settings → Connectors. Access granted by the CRM owner |
| **Google Ads** | attempt a call | Usually absent: the API needs a developer token, which takes weeks. Report as a known long-lead gap, not a setup mistake |

For Meta, report **how many ad accounts are reachable and their names**. One account visible where the portfolio has four is the most common silent failure, and it produces confident answers built on a quarter of the picture.

### 2. State repository

This plugin ships no repository address. Find it in this order:

1. the project instructions for this session
2. a connected folder — a working copy is the repository
3. neither

**If neither, say so and print the line to add**, with the placeholder visible rather than guessed:

```
No state repository is named for this session.

Add to your project instructions (Cowork: Project → Instructions;
Claude Code: CLAUDE.md at the project root):

    Project state: owner/repo
    findings/, gaps.md and docs/ live there — what has been established
    and what was retracted. Read it before answering; record new
    findings there.

Until then answers use live data only, and will not know what has
already been established, tried, or ruled out.
```

**Never guess a repository.** Reading the wrong one is worse than reading none: it produces history that looks authoritative and belongs to someone else.

If an address is named, confirm it is actually reachable — list its contents. Named but unreachable is a different problem from not named, and the fix differs: access versus configuration.

### 3. Writing

Establish which write path exists and say which one applies, because they must not be mixed:

- **folder connected** → files are written locally and committed with the repository's own save script
- **git connector, write access** → commits go through the connector, no local file
- **neither** → findings cannot be recorded. Say this plainly: work done in this session will be lost, and the next session will repeat it

## Output

One block, in this order, and nothing else:

```
READY
  Meta Ads      4 ad accounts: <names>
  CRM           connected
  State         owner/repo — 5 findings, gaps.md
  Writing       git connector, write

MISSING
  Google Ads    developer token not issued. Weeks of lead time.
                Unblocks: the Google channel, and cost per customer
                across channels instead of cost per lead within one.

NEXT
  1. <the single most valuable action, with where to click>
```

**Order MISSING by what it unblocks, not by how easy it is to fix.** A five-minute connector that unblocks nothing goes below a three-week token that unblocks a whole channel.

**If everything is connected, say so in one line and stop.** Do not invent optional improvements to fill the block.

## Do not

- Report a source as connected because it appears in a menu — call it
- Guess a repository address, a business name or an account id
- Continue into analysis. This skill answers "am I set up" and stops. The reader asked what to connect, not what their campaigns are doing
