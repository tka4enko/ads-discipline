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

**If state is unreachable — the folder is empty, or there is no folder at all — ask. Both cases get the same question; the cause differs, the decision does not.**

**Step 1 — get the list first.** Call the GitHub connector and retrieve the repositories it can reach. Do this *before* composing the question. Do not skip it because the answer seems obvious, and do not proceed on the assumption that no list is available.

**Step 2 — build the choices from that list, and from nothing else.**

Every choice is a repository address returned in step 1. Nothing else — no entry you composed yourself.

The question mechanism adds its own free-text escape, usually labelled "Other", and that label cannot be changed. So say what it is for in the question text: *if the right one is not listed, choose Other and type `owner/repo`.* Never add a second free-text entry of your own beside it — two of them is worse than a badly named one. Annotate each repository so the choice can be made without opening anything: whether it is empty, and whether it already contains `findings/` or `gaps.md`.

**One question, one decision.** Do not attach anything else to it — not the connectors, not Google Ads, not what to do next. Those belong in the status block, which comes after. A prompt carrying several decisions gets answered on the first one and abandoned.

**These are forbidden as choices, without exception:**

- "Point to a GitHub repo" — which one? The question is unanswered and gets asked again
- "Use this folder locally" — a folder is not a repository; nothing is recorded
- "Connect GitHub" — sends the person to a settings screen and returns them here
- "Use an existing repo" — the address is still missing afterwards

The test each must pass: **after this choice is selected, is the address known?** If the answer is no, the choice is a restatement of the question and must not appear.

**If step 1 returns nothing, or fails** — do not show a menu at all. A prompt whose only option is "Other" is a text box wearing a costume. Ask directly instead:

> I could not read your repositories from GitHub, so there is no list to choose
> from. Paste the address of the repository that should keep the findings —
> `owner/repo`. An empty one is fine.

Do not invent placeholder choices to fill a list, and do not offer connecting anything.

**The question text carries the consequence:**

> This folder is empty, so nothing found here survives the conversation. Which repository should keep the findings? An empty one is fine.

**With no folder connected at all**, the same question applies. Where the GitHub connector works, a repository is enough on its own — findings are written through it and no folder is needed. Where it does not, say that a folder has to be added before anything can be recorded, and name that as the single next action.

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
- **End by offering to work anyway.** "Should I start looking at the accounts knowing nothing gets saved?" makes the losing path the easy one, and it is the one people take. Where recording is impossible, the setup step is the answer and there is no alternative to put beside it
- Ask in prose when the surface has a question tool. A sentence in a report is read as commentary and skipped
- Offer to record something instead of recording it. The criteria in CONVENTIONS §12 are the decision; asking hands it back and the finding dies with the conversation
