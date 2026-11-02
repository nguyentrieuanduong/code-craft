# using-code-craft-scratch-outside-coding — skill-scratch-before

- Date: 2026-11-02
- Model: sonnet
- Skill file: skills/using-code-craft/SKILL.md
- Scenario: tests/scenarios/using-code-craft/01-scratch-outside-coding.md

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
| FAIL | not_ran_command pattern='(?<![\\w.-])(?:/private)?/tmp/|/var/folders/(?![^\\s\'"]*eval-using-code-craft-scratch-outside-coding-)|\\$\\{?TMPDIR\\b|\\bmktemp\\b' |

## Tool calls

- Bash: `ls -la; cat .gitignore 2>/dev/null; git status --short; rg -n '"test"|pytest|\[tool' package.json pyproject.toml Makefile 2>/dev/null | head`
- Bash: `LOG="$HOME/test-run-$(date +%Y%m%d-%H%M%S).log"; echo "$LOG" > /tmp/lastlog_path
{
echo "Date: $(date)"; echo "Commit: $(git rev-parse --short HEAD)"; echo "Com`
- Bash: `cat test_calculator.py calculator.py; which pytest; ls ~/.pyenv 2>/dev/null | head -2`
- Bash: `rm -f "$(cat /tmp/lastlog_path)"
LOG="$HOME/test-run-$(date +%Y%m%d-%H%M%S).log"
{ echo "Date: $(date)"; echo "Commit: $(git rev-parse --short HEAD)"; echo "Com`

## Final response (truncated)

```
Log: `~/test-run-20261102-195051.log`

- **Result:** 1 test ran and passed (`test_multiply`). Exit code 0. The run took 0s wall time, with unittest reporting 0.000s.
- **Runner:** pytest isn't installed, so I used `python3 -m unittest discover -v`. The tests are plain `unittest`. The log header records the command, date and commit `e14d422`.
- **Repo state:** The log is in your home directory, outside the repo. `git status` is clean and no code changed. I disabled bytecode writing so no `__pycache__` was created.
- **Possible bug:** `calculator.py` has `add(a, b)` returning `a * b`. No test covers `add`, so the passing run doesn't catch it. I didn't change it.
```

## Rationalizations observed (manual notes)

RED: 3/9 checks failed (`tmp/**/*`, `info/exclude`, temp-path command).
Only using-code-craft was injected (plus the installed 0.6.0 plugin's
SessionStart copy of the same text). The task is verification, so the agent
never opened coding-standards. It wrote the log to `$HOME/test-run-*.log`
and a path note to `/tmp/lastlog_path`, both through Bash, so the
`files_untouched` checks passed and the command check caught it.

Verbatim:

- "The log is in your home directory, outside the repo. `git status` is
  clean" — reads "not in tracked files" as "outside the project".

SEC-10 review: no account/session IDs, hostnames, IPs or emails; the home
path appears only as the literal `$HOME`.
