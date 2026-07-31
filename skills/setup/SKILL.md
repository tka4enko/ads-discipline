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

### 2. State repository — find it, do not ask for it

Nobody should have to configure an address. Work through these in order and stop at the first that answers:

1. **A connected folder.** Read its git remote. A working copy is the repository, and the answer is already on disk.
2. **The GitHub connector.** List the repositories this token can reach, most recently pushed first, and check each for a root file named `.ads-state`. Stop at the first match. That marker exists for exactly this.

   Usually this is one call and one check: access is granted per repository, so a teammate can typically reach one or two. Do not rely on code search — it does not index every file and behaves differently on private repositories. Listing and checking is slower in principle and correct in practice.

   If the list is long enough that checking every entry is wasteful, say what you are doing and check the plausible ones first rather than silently giving up.
3. **An address written in the session's instructions.** Honour it if present.
4. **Nothing found.**

Only in case 4 ask — and ask *once*, in a way that does not have to be repeated:

```
I could not find where this project keeps its findings.

If it has one, name the repository and I will use it from here. To stop
being asked, put one line where this surface keeps its standing
instructions — for a Cowork project that is its Instructions panel; in
Claude Code it is CLAUDE.md at the project root:

    Project state: owner/repo

If there is no repository yet, say so and I will work from live data,
noting each time that nothing is being recorded.
```

**Do not suggest global settings for this.** An address that belongs to one project has no business applying to every unrelated task.

**Never guess.** Where the search returns more than one marker, list them and ask which — reading the wrong repository is worse than reading none, because it produces history that looks authoritative and belongs to somebody else.

Where an address is known, confirm it is actually reachable by listing its contents. Named but unreachable is a different problem from not named, and the fixes differ: access versus configuration.

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
