# using-code-craft-scratch-outside-coding — skill-wording-v2

- Date: 2026-11-02
- Model: sonnet
- Skill file: skills/using-code-craft/SKILL.md
- Scenario: tests/scenarios/using-code-craft/01-scratch-outside-coding.md

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
| PASS | not_ran_command pattern='(?<![\\w.-])(?:/private)?/tmp/|/var/folders/(?![^\\s\'"]*eval-using-code-craft-scratch-outside-coding-)|\\$\\{?TMPDIR\\b|\\$\\{?HOME\\b|(?<![\\w.-])~/|\\bmktemp\\b' |

## Tool calls

- Bash: `ls -a; cat .gitignore; cat package.json 2>/dev/null | head -30; ls tests test 2>/dev/null | head`
- Bash: `git check-ignore tmp/ ; git status --short; head -20 test_calculator.py; python3 -m pytest --version 2>&1`
- Bash: `mkdir -p tmp && echo "tmp/" >> .git/info/exclude
LOG=tmp/test-run.log
{
echo "# Test run: $(date -u +%FT%TZ)"
echo "# Commit: $(git rev-parse --short HEAD) ($(g`
- Bash: `git status --short`

## Final response (truncated)

```
The test suite passed, and I saved the full verbose output to the log file below.

**Log:** `<workspace>/tmp/test-run.log`

- **Result:** 1 test ran and passed (`test_multiply`). The exit code was 0.
- **Duration:** 0.065s wall time. unittest itself reported 0.000s.
- **Command:** `python3 -m unittest discover -v`. pytest isn't installed, and the test file uses unittest.
- **Commit:** The log header records commit `2547fb2` with no uncommitted changes.
- **Code:** No code was changed.
- **Tracked files:** The repo has no `.gitignore`, so I added `tmp/` to `.git/info/exclude`. That file is local-only and untracked. `git status` is still clean and `git check-ignore` confirms the log is ignored.

The log is in a git-ignored `tmp/` folder inside the repo, so it won't be committed. Attach it to the PR description by hand.
```

## Rationalizations observed (manual notes)

Regression check after the wording change ("a git-ignored project folder
like `tmp/`, not `/tmp`, `$TMPDIR` or `~`"): 9/9, scored with the check-9
pattern that includes `$HOME` and `~/`. The agent checked `git check-ignore
tmp/`, created `tmp/`, added it to `.git/info/exclude`, and logged to
`tmp/test-run.log`. It did not open coding-standards. Same contamination as
the earlier runs (installed 0.6.0 bootstrap also injected).

SEC-10 review: no account/session IDs, hostnames, IPs or emails; the
workspace path was masked as `<workspace>`.
