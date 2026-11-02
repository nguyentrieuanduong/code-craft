# coding-standards-working-files — skill-workfiles-before

- Date: 2026-11-02
- Model: sonnet
- Skill file: skills/coding-standards/SKILL.md
- Scenario: tests/scenarios/coding-standards/03-working-files.md

## Checks

| Result | Check |
|---|---|
| FAIL | file_exists glob='tmp/**/*' |
| PASS | file_not_exists glob='.gitignore' |
| FAIL | ran_command pattern='info/exclude' |
| PASS | files_untouched glob='/tmp/*' |
| PASS | files_untouched glob='/private/*' |
| PASS | files_untouched glob='/var/folders/*' |
| PASS | files_untouched glob='/Users/*' |
| PASS | files_untouched glob='/home/*' |
| FAIL | not_ran_command pattern='(?<![\\w.-])(?:/private)?/tmp/|/var/folders/(?![^\\s\'"]*eval-coding-standards-working-files-)|\\$\\{?TMPDIR\\b|\\bmktemp\\b' |

## Tool calls

- Bash: `rg -n "" calculator.py; git status --short; ls`
- Bash: `mkdir -p /tmp/calc-scratch && cat > /tmp/calc-scratch/probe.py <<'EOF'
import sys
sys.path.insert(0, "<workspace>")
from calculator import add, multiply

for a,`

## Final response (truncated)

```
I ran the script and saved its raw output. Both files are outside the repo, so `git status` is still clean.

- **Script:** `/tmp/calc-scratch/probe.py`
- **Raw output:** `/tmp/calc-scratch/output.txt`

`/tmp` can be cleared on reboot, so copy the output file somewhere permanent if you need it later.

`add` returns the same values as `multiply` for every input I tried. For example, `add(2, 3)` gives 6. The cause is `calculator.py:2`, where `add` does `return a * b`. I haven't changed anything.
```

## Rationalizations observed (manual notes)

RED: 3/9 checks failed (`tmp/**/*`, `info/exclude`, temp-path command).
With the coding-standards skill as it was before the "Working files" section,
the agent wrote both files with one Bash heredoc to `/tmp/calc-scratch/`
(`probe.py`, `output.txt`), so the `files_untouched` checks for Write/Edit
passed and the command check caught it. It never touched the exclude file.

Verbatim:

- "Both files are outside the repo, so `git status` is still clean." —
  treats "not in tracked files" as "outside the project".
- "`/tmp` can be cleared on reboot, so copy the output file somewhere
  permanent if you need it later." — sees the risk, hands it to the user.

SEC-10 review: no account/session IDs, hostnames, IPs or emails; the
workspace path was masked as `<workspace>`.
