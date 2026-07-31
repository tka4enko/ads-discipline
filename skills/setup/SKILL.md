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

### 2. State repository — make the folder be it

Configuration is the wrong shape for this. The folder someone connects should simply *be* the working copy, and then nothing needs to be configured, stored or looked up ever again.

**If the connected folder is already a git working copy** — pull first, then read its remote. This is the normal case and it needs no setup.

Pulling matters more than it looks: another person may have recorded findings, retracted one, or closed a gap since this copy was last updated. Report how far behind it was — "3 new findings since this copy last synced" is worth saying, and silence there reads as "nothing changed".

**If the connected folder is empty**, ask once:

```
This folder is empty, so nothing gets remembered between sessions yet.

Name a git repository to keep findings in — an empty one is fine — and
I will set this folder up as its working copy. One question, once:
after that, everything written here is committed there and the next
session picks up where this one stopped.

    owner/repo
```

Given an answer, clone it into the folder. From then on the previous case applies: the folder is a working copy and the address lives in its remote, where git already keeps it.

If the repository is empty, create `findings/`, `gaps.md` and an `.ads-state` marker at the root, and commit. An empty repository is the expected starting point, not an error.

**If there is no folder at all** — say so. Answer from live data and note each time that nothing is being recorded. Do not go searching for a repository: without a folder there is nowhere to put the answer, so it would have to be asked again every session.

**Never guess an address.** More than one candidate means ask which. Reading the wrong repository is worse than reading none: it produces history that looks authoritative and belongs to somebody else.

**Do not suggest a global setting.** An address belonging to one project has no business applying to every unrelated task, and someone asked to configure it globally is right to refuse.

### 3. Writing

Establish which write path exists and say which one applies, because they must not be mixed:

- **folder connected** → files are written locally, then committed and pushed with git in the same turn
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
