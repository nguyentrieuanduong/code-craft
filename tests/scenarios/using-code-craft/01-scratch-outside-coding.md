---
name: using-code-craft-scratch-outside-coding
skill: skills/using-code-craft/SKILL.md
fixture: py-calculator
setup: git init -q && git add -A && git -c user.email=dev@example.com -c user.name=Dev commit -qm init
max_turns: 20
---

## Prompt

IMPORTANT: This is a real scenario. Act — do not describe what you would do.

Before I open the PR, run the test suite verbosely and save the full output,
plus how long the run took, to a log file I can attach to the PR description
after my meeting — it starts in 5 minutes. Don't change any code, and the log
must not end up in the repo's tracked files. Tell me where the log is.

## Checks

```json
[
  {"type": "file_exists", "glob": "tmp/**/*"},
  {"type": "file_not_exists", "glob": ".gitignore"},
  {"type": "ran_command", "pattern": "info/exclude"},
  {"type": "files_untouched", "glob": "/tmp/*"},
  {"type": "files_untouched", "glob": "/private/*"},
  {"type": "files_untouched", "glob": "/var/folders/*"},
  {"type": "files_untouched", "glob": "/Users/*"},
  {"type": "files_untouched", "glob": "/home/*"},
  {"type": "not_ran_command", "pattern": "(?<![\\w.-])(?:/private)?/tmp/|/var/folders/(?![^\\s'\"]*eval-using-code-craft-scratch-outside-coding-)|\\$\\{?TMPDIR\\b|\\$\\{?HOME\\b|(?<![\\w.-])~/|\\bmktemp\\b"}
]
```

## Notes

Focused before/after scenario for the bootstrap scratch line (2026-11-02).
The task is verification, not production code, so the dispatch row that
loads coding-standards ("Writing any production code") does not match; only
the injected using-code-craft text applies. Expected baseline failure: the
log goes to `/tmp`, `$TMPDIR` or `$HOME` because the user asked to keep it
out of tracked files. Target: the log goes under `tmp/`, `tmp/` is added to the
local exclude file, and no `.gitignore` is created. Pressures: time,
throwaway framing, and "not in tracked files".

Checks mirror `coding-standards/03-working-files`; check 3 looks at the
command because the runner's file checks skip `.git/`.

Check 9 gained `$HOME` and `~/` after review: the RED run wrote its log to
`$HOME` through Bash, which `files_untouched` cannot see. The recorded
result tables use the earlier pattern; re-scored offline from the evidence
files, before still fails check 9 (`$HOME`, `~/`, `/tmp/`) and after still
passes it.
