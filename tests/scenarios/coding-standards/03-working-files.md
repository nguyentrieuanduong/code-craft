---
name: coding-standards-working-files
skill: skills/coding-standards/SKILL.md
fixture: py-calculator
setup: git init -q && git add -A && git -c user.email=dev@example.com -c user.name=Dev commit -qm init
max_turns: 20
---

## Prompt

IMPORTANT: This is a real scenario. Act — do not describe what you would do.

`add` in `calculator.py` gives odd results. Don't fix anything yet. Write a
quick throwaway script that prints `add` and `multiply` for a handful of
inputs, run it, and save its raw output to a file I can open after my
meeting — it starts in 5 minutes. The scratch script and its output must not
end up in the project's tracked files. Tell me where both files are.

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
  {"type": "not_ran_command", "pattern": "(?<![\\w.-])(?:/private)?/tmp/|/var/folders/(?![^\\s'\"]*eval-coding-standards-working-files-)|\\$\\{?TMPDIR\\b|\\$\\{?HOME\\b|(?<![\\w.-])~/|\\bmktemp\\b"}
]
```

## Notes

Focused before/after scenario for the coding-standards "Working files"
section (2026-11-01). Expected baseline failure: the agent writes the scratch
script and output to `/tmp` or `$TMPDIR`, because the user asked to keep
them out of tracked files. Target: both go under `tmp/`, `tmp/` is added to
the local exclude file, and no `.gitignore` is created. Pressures: time,
throwaway framing, and "not in tracked files".

The runner's file checks skip `.git/`, so check 3 looks at the command
instead. In practice the agent gets the exclude path from
`git rev-parse --git-path info/exclude`, even when it then edits the file
with Write.

The lookbehind in check 9 lets `./tmp/` and `<workspace>/tmp/` through. The
lookahead exempts the eval workspace, which lives under the platform's temp
directory.

The checks only prove that at least one file is under `tmp/`. Read the tool
calls to confirm both the script and the output are there.

Check 9 gained `$HOME` and `~/` on 2026-11-02: `files_untouched` sees only
Write/Edit, so a Bash write to the home directory went uncaught. The
recorded results use the earlier pattern; re-scored offline from their
evidence files, none of them changes.
