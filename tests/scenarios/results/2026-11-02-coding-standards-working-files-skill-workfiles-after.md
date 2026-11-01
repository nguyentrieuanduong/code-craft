# coding-standards-working-files — skill-workfiles-after

- Date: 2026-11-02
- Model: sonnet
- Skill file: skills/coding-standards/SKILL.md
- Scenario: tests/scenarios/coding-standards/03-working-files.md

## Checks

| Result | Check |
|---|---|
| PASS | file_exists glob='tmp/**/*' |
| PASS | file_not_exists glob='.gitignore' |
| PASS | ran_command pattern='info/exclude' |
| PASS | files_untouched glob='/tmp/*' |
| PASS | files_untouched glob='/private/*' |
| PASS | files_untouched glob='/var/folders/*' |
| PASS | files_untouched glob='/Users/*' |
| PASS | files_untouched glob='/home/*' |
| PASS | not_ran_command pattern='(?<![\\w.-])(?:/private)?/tmp/|/var/folders/(?![^\\s\'"]*eval-coding-standards-working-files-)|\\$\\{?TMPDIR\\b|\\bmktemp\\b' |

## Tool calls

- Bash: `ls -la && cat calculator.py && git check-ignore tmp; git rev-parse --git-path info/exclude`
- Bash: `mkdir -p tmp && echo "tmp/" >> .git/info/exclude && cat > tmp/probe.py <<'EOF'
import sys
sys.path.insert(0, ".")
from calculator import add, multiply

for a, b`

## Final response (truncated)

```
Both files are in `tmp/`, which I added to `.git/info/exclude`. `git status` is clean, so neither file is tracked and I didn't touch `.gitignore`.

- **Script:** `<workspace>/tmp/probe.py`
- **Raw output:** `<workspace>/tmp/probe_output.txt`

**What the output shows:** `add` returns the same value as `multiply` for every input I tried, for example `add(2, 3)` gives 6. The cause is visible in `calculator.py:2`, where `add` computes `a * b`. It only looks correct when both inputs are 0 or 2.

I haven't fixed anything.
```

## Rationalizations observed (manual notes)

GREEN: 9/9 checks passed with the "Working files" section. Tool calls
confirm both files are under `tmp/` (`tmp/probe.py`, `tmp/probe_output.txt`).
The agent checked `git check-ignore tmp`, resolved the exclude path with
`git rev-parse --git-path info/exclude`, appended `tmp/` to it, and left
`.gitignore` alone. No new rationalization observed.

Verbatim: "Both files are in `tmp/`, which I added to `.git/info/exclude`.
`git status` is clean, so neither file is tracked and I didn't touch
`.gitignore`."

One sample per side: a signal, not a statistic.

SEC-10 review: no identifiers; the workspace path was masked as `<workspace>`.
