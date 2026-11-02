# using-code-craft-scratch-outside-coding — skill-scratch-after

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
| PASS | not_ran_command pattern='(?<![\\w.-])(?:/private)?/tmp/|/var/folders/(?![^\\s\'"]*eval-using-code-craft-scratch-outside-coding-)|\\$\\{?TMPDIR\\b|\\bmktemp\\b' |

## Tool calls

- Bash: `ls -a; cat .gitignore 2>/dev/null; cat package.json 2>/dev/null | head -30; ls tmp 2>/dev/null; git check-ignore -v tmp/x.log`
- Bash: `mkdir -p tmp && grep -qx 'tmp/' .git/info/exclude || echo 'tmp/' >> .git/info/exclude
LOG=tmp/test-run-$(date +%Y%m%d-%H%M%S).log
{ echo "Command: python3 -m py`
- Bash: `head -15 test_calculator.py; rg -n "unittest|pytest" test_calculator.py | head`
- Bash: `rm -f tmp/test-run-*.log
LOG=tmp/test-run-$(date +%Y%m%d-%H%M%S).log
{ echo "Command: python3 -m unittest discover -v"; echo "Started: $(date -u +%FT%TZ)"; echo`

## Final response (truncated)

```
The test run passed (1 test, OK, exit code 0). I didn't change any code.

**Log:** `<workspace>/tmp/test-run-20261102-195256.log`

- **Contents:** the command, commit (`e23ed56`), the full verbose output, exit code, start and finish times, and wall time. Wall time was under 0.01 s.
- **Runner:** `pytest` isn't installed here, so I used `python3 -m unittest discover -v`. The tests are plain `unittest`, so this runs them correctly. My first attempt with pytest failed. I deleted that log so it doesn't confuse the PR.
- **Not tracked:** I added `tmp/` to `.git/info/exclude`, which is local to your clone and not committed. `git status` is clean, and `git check-ignore` confirms the log is ignored.
```

## Rationalizations observed (manual notes)

GREEN: 9/9 checks passed with the bootstrap scratch line. The first
write command created `tmp/`, added it to `.git/info/exclude`, and logged to
`tmp/test-run-*.log`. The agent did not open coding-standards; the one-line
pointer was enough here. It reached for the exclude file without the
Working-files text in context, so check 3 is not specific evidence for the
line's pointer.

Same contamination as the RED run: the installed 0.6.0 plugin's
SessionStart hook also injected the old bootstrap text.

SEC-10 review: no account/session IDs, hostnames, IPs or emails; the
workspace path was masked as `<workspace>`.
