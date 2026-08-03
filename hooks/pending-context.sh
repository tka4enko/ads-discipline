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
[ -f "$root/pending.md" ] || exit 0

page="$(cat "$root/pending.md" 2>/dev/null)" || exit 0
[ -n "${page//[[:space:]]/}" ] || exit 0

printf '%s' "$page" | python3 -c '
import json, sys
page = sys.stdin.read()
text = (
    "Unanswered questions from the state repository (pending.md). "
    "These are blanks only the human can fill. Follow CONVENTIONS §12b: "
    "refuse the number when one of these blocks the question that was asked, "
    "otherwise ask exactly one of them, and write the answer back immediately.\n\n"
    + page
)
print(json.dumps({"hookSpecificOutput": {
    "hookEventName": "SessionStart",
    "additionalContext": text,
}}))
' 2>/dev/null || exit 0
