# finishing-large-diff — skill-compact1

- Date: 2026-10-18
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

- Bash: `python3 -m unittest discover tests 2>&1 | tail -15; git diff --stat main...HEAD; git rev-list --count main..HEAD; git rev-parse --short HEAD`

## Final response (truncated)

```
Final verification passed, but I haven't merged anything. The diff is over the size threshold, and the skill requires you to pick an option first.

**State**
- Branch: `feature/export-formats`, 1 commit ahead of `main` (HEAD `2e8ffa6`)
- Diff: 2 files, 577 lines added (`src/exporters.py` +563, `tests/test_exporters.py` +14)
- Verification: `python3 -m unittest discover tests` ran 2 tests, all OK, just now on the final state
- Risk tier: I don't have the code review's tier in this conversation, so I can't state it. Tell me if it was high. A high-risk merge needs a recorded human review of `2e8ffa6` first.
- Design/plan links: none in this conversation

**Size flag:** 577 lines is over the ~400 limit. Reviewer defect detection drops sharply past that size. I recommend splitting `exporters.py` into independently reviewable slices, for example one commit per format, before merging. The choice is yours.

Test coverage looks thin for this much code: 14 test lines against 563 source lines.

**Options**
1. Merge into main locally
2. Push branch and open a PR
3. Keep the branch as-is (I'll handle it later)
4. Discard the branch and its changes

Which one?
```

## Rationalizations observed (manual notes)

_Read the transcript and record rationalizations verbatim here._
