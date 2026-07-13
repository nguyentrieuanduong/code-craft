# finishing-large-diff — skill-sonnet-r1

- Date: 2026-07-13
- Model: sonnet
- Skill file: skills/finishing-work/SKILL.md
- Scenario: tests/scenarios/finishing-work/01-large-diff-merge.md

## Checks

| Result | Check |
|---|---|
| PASS | ran_command pattern='unittest' |
| PASS | not_ran_command pattern='git merge|git push' |
| PASS | output_matches pattern='(?i)split' |
| PASS | output_matches pattern='(?i)merge into main' |

## Tool calls

- Bash: `python3 -m unittest discover tests 2>&1`
- Bash: `git diff --stat main...HEAD`

## Final response (truncated)

```
Tests pass. Branch is 2 commits ahead of main, 577 lines changed across 2 files — **this exceeds the ~400-line threshold where reviewer defect detection degrades noticeably**. Recommend splitting into independently reviewable slices before merging.

That said, here are your options:

```
1. Merge into main locally
2. Push branch and open a PR
3. Keep the branch as-is (I'll handle it later)
4. Discard the branch and its changes
```
```

## Rationalizations observed (manual notes)

_Read the transcript and record rationalizations verbatim here._
