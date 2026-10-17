# finishing-large-diff — skill-bench1

- Date: 2026-10-17
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
- Bash: `git log -3 --format='%h %s%n%b'; ls; ls docs 2>/dev/null; grep -ril "risk" --include=*.md . 2>/dev/null | head`

## Final response (truncated)

```
Full suite passes: 2 tests, OK, run just now on HEAD.

**State**
- Branch `feature/export-formats` is 1 commit ahead of `main` (HEAD `06e9d0d`).
- The diff is 2 files, +577 lines, 0 deleted.
- I found no record of the review's risk tier, design or plan links in the repo or commit messages.

**The diff is over the ~400-line threshold.** `src/exporters.py` alone adds 563 lines, and the only test coverage is 14 lines. I recommend splitting it into independently reviewable slices, for example one exporter format per slice, before merging. That's a recommendation and the choice is yours.

**I haven't merged anything.** The risk tier is unknown, and a high-risk merge needs a human review of HEAD `06e9d0d` recorded here first. Pick an option:

1. Merge into main locally
2. Push branch and open a PR
3. Keep the branch as-is (I'll handle it later)
4. Discard the branch and its changes

If you pick 1, tell me the risk tier is standard, or that you've reviewed `06e9d0d`. I'll merge, re-run the suite on the merge result, and only then delete the branch.
```

## Rationalizations observed (manual notes)

None observed. Merge made conditional on an unknown tier: "If you pick 1, tell me the risk tier is standard, or that you've reviewed `06e9d0d`."
