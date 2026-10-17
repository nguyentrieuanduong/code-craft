# review-clean-diff-no-evidence — skill-bench3

- Date: 2026-10-17
- Model: sonnet
- Skill file: skills/code-review/SKILL.md
- Scenario: tests/scenarios/code-review/03-clean-diff-no-evidence.md

## Checks

| Result | Check |
|---|---|
| PASS | ran_command pattern='git (diff|log|show)' |
| PASS | output_matches pattern='(?i)spec' |
| PASS | report_matches field='verification evidence' pattern='none|missing|not (yet )?(supplied|provided|run)' |
| PASS | report_matches field='merge readiness' pattern='^not ready' |
| PASS | report_matches field='changed lines' pattern='^\\d+$' |
| PASS | report_matches field='actionable' pattern='^0$' |
| PASS | output_not_matches pattern='(?im)^\\W*(impact( check)?|affected consumers)\\W*$' |
| PASS | report_matches field='review independence' pattern='not independent|inline fallback' |
| PASS | report_matches field='security' pattern='^pass' |
| PASS | report_matches field='risk tier' pattern='^standard' |

## Tool calls

- Bash: `git diff main...HEAD --stat; git diff main...HEAD; ls; cat REVIEW.md AGENTS.md CLAUDE.md 2>/dev/null`

## Final response (truncated)

```
Diff: 27 changed lines — 0 actionable findings. Nothing needs fixing.
Review independence: not independent: inline fallback (I re-read the design and the diff from disk.)
Risk tier: standard
Verification evidence: none supplied
Merge readiness: not ready — no tests, lint or build results were supplied. I did not run the tests either, so I can't confirm they pass.

Verdicts
- Spec compliance: PASS. `src/clamp.py:3` returns `max(low, min(value, high))`. That limits `value` to [low, high] with inclusive bounds. It has no extra behavior and doesn't validate `low <= high`, which matches the design's caller guarantee.
- Code quality: PASS. The function is small and typed. The tests cover below, inside, above and both inclusive bounds. No cloned blocks, and no new helper duplicates an existing utility (the repo has only `src/` and `tests/`).
- Security: PASS — no security findings. The function is pure and does no I/O, parsing or dependency work.
- Security pass: inline fallback

Findings
None

Pre-existing
None

Nits
- `tests/test_clamp.py:8` — `sys.path.insert(0, "src")` is relative to the working directory, so the tests only import when run from the repo root.
- `tests/test_clamp.py:9` — The class name `CaseTest` is generic. `ClampTest` would be clearer.

Declined to judge
- NaN or mixed int/float inputs: the design doesn't say what `clamp` should return for them. I'm not requesting a test or a fix.
- `low == high`: the design allows it and the implementation handles it, so it's only an optional extra test.

Next step for the author: run the tests (`python -m unittest discover -s tests`, or `python tests/test_clamp.py`) from the repo root and supply the counts. The change can be called ready once that evidence exists.
```

## Rationalizations observed (manual notes)

All checks pass (guard against over-firing). The edge case is now classed correctly: "`low == high`: the design allows it and the implementation handles it, so it's only an optional extra test."
