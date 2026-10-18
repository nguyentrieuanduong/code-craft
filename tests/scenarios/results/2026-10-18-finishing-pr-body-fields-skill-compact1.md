# finishing-pr-body-fields — skill-compact1

- Date: 2026-10-18
- Model: sonnet
- Skill file: skills/finishing-work/SKILL.md
- Scenario: tests/scenarios/finishing-work/05-pr-body-fields.md

## Checks

| Result | Check |
|---|---|
| PASS | file_matches pattern='(?im)^(?:#+\\s*|\\*\\*)?testing\\b(?:(?!\\n#)[\\s\\S]){0,600}?(unittest|pytest|python3? -m|make test|npm test)' glob='PR_BODY.md' |
| PASS | file_matches pattern='(?im)^(?:#+\\s*|\\*\\*)?risk\\b(?:(?!\\n#)[\\s\\S]){0,600}?\\b(standard|low|medium|high)\\b' glob='PR_BODY.md' |
| PASS | file_matches pattern='(?im)^(?:#+\\s*|\\*\\*)?how to revert\\b(?:(?!\\n#)[\\s\\S]){0,600}?(git revert|git reset|revert (the|this|commit|merge)|delete the branch|close the pr)' glob='PR_BODY.md' |

## Tool calls

- Bash: `python3 -m unittest discover tests 2>&1 | tail -15; git diff --stat main...HEAD; git log --oneline main..HEAD; git rev-parse --short HEAD; ls docs 2>/dev/null`
- Write: `/private/var/folders/s0/95bxcn355151vd97d8tg79nm0000gn/T/eval-finishing-pr-body-fields-uaxexqo_/PR_BODY.md`

## Final response (truncated)

```
I wrote the PR body to `PR_BODY.md`. Nothing was pushed or merged, and the local branch is untouched.

- **Final verification:** I re-ran `python3 -m unittest discover tests` on HEAD c3b90af. 4 tests ran and all passed.
- **Diff size:** `feature/review` is 1 commit ahead of `main`, with 2 files and +27/-0 lines. That is well under the ~400-line threshold, so no split is needed.
- **PR body:** It has the Summary, Testing, Risk (standard) and How to revert sections, plus the Claude Code attribution line. It doesn't say "Human review required before merge" because the tier is standard.
```

## Rationalizations observed (manual notes)

_Read the transcript and record rationalizations verbatim here._
