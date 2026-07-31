---
name: setup
description: Check what this session is missing and print exactly how to fix it — which connectors respond, whether a state repository is named and reachable, and what each missing piece would unblock. Run this first on a new machine, a new surface, or when an answer says it cannot see something. Use for "what do I need to connect", "why can't you see my account", "am I set up", "where do I put the repository".
---

# Setup

Run first, on a new machine or a new surface. Nothing else in this plugin announces what it is missing; this does.

The output is a checklist the reader can act on without knowing how any of it works. No diagnosis, no advice about advertising — only what is connected, what is not, and the exact next action for each gap.

## Procedure

**Work from the current directory, never a constructed path.** The connected folder is already the working directory. A path built from what the interface displays — `/Users/…`, `/home/…` — will not exist in a sandboxed shell, and the command fails with no output, which reads as an empty folder rather than a wrong path.

```
pwd                              where this actually is
ls -la                           what is in it
git rev-parse --show-toplevel    repository root, if any
git remote -v                    where it points
```

Never `cd` to a path taken from a label. If a specific directory is genuinely needed, discover it first and use what `pwd` returned.

**Verify, do not assume.** For each source below, make a real call. A connector that appears in a list but errors on use is not connected, and saying otherwise is worse than saying nothing.

### 1. Data sources

| Source | How to check | If missing |
|---|---|---|
| **Meta Ads** | list ad accounts | Settings → Connectors → Meta Ads. Needs access to the ad accounts, granted in Meta Business Manager by whoever owns them |
| **CRM** | one aggregate query, counts only | Settings → Connectors. Access granted by the CRM owner |
| **Google Ads** | attempt a call | Usually absent: the API needs a developer token, which takes weeks. Report as a known long-lead gap, not a setup mistake |
| **GitHub** | read something from a repository | Authorise it — the plugin already declares the connector, so it is listed but unapproved rather than absent. Do not tell anyone to add it |

**Check GitHub by using it, not by looking for its name.** More than one thing can provide GitHub access, and they are named differently. A failed clone proves the *credentials* are missing, not that no connector exists — report what the call actually did rather than inferring absence from an unrelated failure.

When it is present, say which repositories it reaches. That is what turns the state-repository question into a pick-list instead of a typing exercise.

For Meta, report **how many ad accounts are reachable and their names**. One account visible where the portfolio has four is the most common silent failure, and it produces confident answers built on a quarter of the picture.

### 2. State repository — make the folder be it

Configuration is the wrong shape for this. The folder someone connects should simply *be* the working copy, and then nothing needs to be configured, stored or looked up ever again.

**If the connected folder is already a git working copy** — pull first, then read its remote. This is the normal case and it needs no setup.

Pulling matters more than it looks: another person may have recorded findings, retracted one, or closed a gap since this copy was last updated. Report how far behind it was — "3 new findings since this copy last synced" is worth saying, and silence there reads as "nothing changed".

**If the connected folder is empty**, ask once — **always through the surface's question tool, never in prose.** A sentence in a report gets read as commentary and skipped. This has to be answered before anything else is worth doing, so it has to appear as a question.

Build the choices like this:

**With the GitHub connector** — list the repositories it can reach and offer them as choices. Each choice is a real address, so selecting one is a complete answer. Put the likeliest first: most recently pushed, and anything already containing `findings/` or an `.ads-state` marker.

**Without the connector** — the question still appears, with two choices only:

- *Type the address* — free text, `owner/repo`
- *No repository yet* — nothing is recorded, and every answer will say so

Do not offer "connect GitHub" as a choice. Selecting it produces no answer: it sends the person to a settings screen and ends the exchange, so they come back to the same question having gained nothing. Mention in the question text that connecting GitHub would turn this into a pick-list — as information, not as something selectable.

**Every choice must end the question.** After selecting it, the answer exists — either because the choice was the address, or because it settled the matter ("no repository yet" settles it: nothing gets recorded).

A choice that hands back a task fails this. "Use an existing repo" still needs the address afterwards. "Connect GitHub" sends the person elsewhere and returns them to the same prompt. Both read as a broken flow, and both are the same mistake: describing an intention instead of supplying an answer.

**Free text is always available.** The repository may not exist yet, or may live where the connector cannot see it. A prompt offering only fixed choices is worse than none — the person can see they are being asked and has no way to answer.

Put the consequence inside the question, not beneath it:

> This folder is empty, so nothing said here survives the conversation. Which repository should keep the findings? An empty one is fine — I will set the folder up as its working copy.

**If there is no folder at all** — say so. Answer from live data and note each time that nothing is being recorded. Do not go searching for a repository: without a folder there is nowhere to put the answer, so it would have to be asked again every session.

**Never guess an address.** More than one candidate means ask which. Reading the wrong repository is worse than reading none: it produces history that looks authoritative and belongs to somebody else.

**Do not suggest a global setting.** An address belonging to one project has no business applying to every unrelated task, and someone asked to configure it globally is right to refuse.

### 3. Writing

Establish which write path exists and say which one applies, because they must not be mixed:

- **folder connected** → files are written locally, then committed and pushed with git in the same turn
- **git connector, write access** → commits go through the connector, no local file
- **neither** → findings cannot be recorded. Say this plainly: work done in this session will be lost, and the next session will repeat it

## Output

**If something blocks work, it goes first — before the status block, not after it.** A question in the last line of a long report is a question nobody answers: the reader has already got what looks like an answer by then.

```
Before anything else: this folder is empty, so nothing said here gets
remembered. Name a repository to keep findings in — an empty one is fine —
and I will set the folder up as its working copy.

    owner/repo

Everything below is what I can see meanwhile.
```

Then the status block. One question, at the top, in its own paragraph, and nothing offered beside it.

Otherwise, one block, in this order, and nothing else:

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

**End on the question, not on a menu.** Where NEXT contains something that blocks recording, ask for exactly that and stop. Offering to continue without it turns the fix into an option, and it is the option nobody takes.

## Do not

- Report a source as connected because it appears in a menu — call it
- Guess a repository address, a business name or an account id
- Continue into analysis. This skill answers "am I set up" and stops. The reader asked what to connect, not what their campaigns are doing
