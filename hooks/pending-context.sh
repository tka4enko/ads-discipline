#!/usr/bin/env bash
# SessionStart hook. Puts the unanswered questions in front of the model before
# the human's first word, so nothing depends on a skill being invoked.
#
# Never fails a session: every path that cannot produce an answer exits 0 with
# empty stdout, which the hook contract treats as "nothing to add".
set -uo pipefail

root="$(git rev-parse --show-toplevel 2>/dev/null)" || exit 0
[ -n "$root" ] || exit 0

# The marker, not the path: a session may be opened in any repository, and
# injecting another project's file would be worse than injecting nothing.
[ -f "$root/.ads-state" ] || exit 0

# Two pages, one channel. Both exist because their contents were being
# rediscovered every session, or not rediscovered and silently assumed.
pending="$(cat "$root/pending.md" 2>/dev/null)" || pending=""
capabilities="$(cat "$root/capabilities.md" 2>/dev/null)" || capabilities=""
[ -n "${pending//[[:space:]]/}${capabilities//[[:space:]]/}" ] || exit 0

CAPABILITIES="$capabilities" PENDING="$pending" python3 -c '
import json, os, sys

parts = []

capabilities = os.environ.get("CAPABILITIES", "")
if capabilities.strip():
    parts.append(
        "What this project can actually do, per surface (capabilities.md). "
        "Follow CONVENTIONS §6a: read this before choosing a path, not after "
        "failing one. A capability absent or unverified on this surface is not "
        "available — say so and name the fix rather than falling back to a "
        "route that cannot work here. A row older than a fortnight is unknown, "
        "not present.\n\n" + capabilities
    )

pending = os.environ.get("PENDING", "")
if pending.strip():
    parts.append(
        "Unanswered questions from the state repository (pending.md). "
        "These are blanks only the human can fill. Follow CONVENTIONS §12b: "
        "refuse the number when one of these blocks the question that was asked, "
        "otherwise ask exactly one of them, and write the answer back immediately."
        "\n\n" + pending
    )

if not parts:
    sys.exit(0)

print(json.dumps({"hookSpecificOutput": {
    "hookEventName": "SessionStart",
    "additionalContext": "\n\n---\n\n".join(parts),
}}))
' 2>/dev/null || exit 0
