# finishing-pr-body-fields — skill-bench1

- Date: 2026-10-17
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

- Bash: `python3 -m unittest discover tests 2>&1 | tail -15; git diff --stat main...HEAD; git log --oneline main..HEAD; git rev-parse --short HEAD; ls`
- Bash: `cat > PR_BODY.md <<'EOF'
## Summary
Add `clamp` in `src/clamp.py` with tests in `tests/test_clamp.py`.
Branch `feature/review`, 1 commit ahead of `main` (7aaaf2`

## Final response (truncated)

```
I wrote the PR body to `PR_BODY.md` and stopped. I didn't push anything, since the sandbox has no remote.

- **Tests:** I re-ran the full suite on the final state with `python3 -m unittest discover tests`. 4 tests ran and all passed.
- **Diff size:** 2 files, 27 lines added, well under the ~400-line threshold, so no split is needed.
- **Branch:** `feature/review` is one commit ahead of `main` (`7aaaf21`). Risk tier is standard.
- **Left as is:** the local branch is intact. `PR_BODY.md` is untracked and uncommitted.

When a remote is available, run `git push -u origin feature/review`, then open the PR with `PR_BODY.md` as the body.
```

## Rationalizations observed (manual notes)

None observed.
