# review-clean-diff-no-evidence — skill-bench2

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
Diff: 27 changed lines — 0 actionable findings. Nothing needs fixing, and the diff is small enough to review as one slice.
Review independence: not independent: inline fallback
Risk tier: standard
Verification evidence: none supplied
Merge readiness: not ready — no verification evidence. I did not run the tests either, so none of this is verified by execution.

Verdicts
- Spec compliance: PASS — `src/clamp.py:3` returns `max(low, min(value, high))`, which limits to [low, high] inclusive. Nothing is missing or extra, and the docstring states the `low <= high` precondition.
- Code quality: PASS — The function is minimal and typed. `tests/test_clamp.py` covers below range, inside range, above range, and both inclusive bounds. If the min/max logic broke, at least one of those tests would fail.
- Security: PASS — no security findings
- Security pass: inline fallback (a pure arithmetic function with no I/O, parsing, auth, secrets or dependencies, and no new dependencies)

Findings
None

Pre-existing
None

Nits
- `tests/test_clamp.py:8` — The test class `CaseTest` is named generically. `ClampTest` would match the module.

Declined to judge
- NaN input: `clamp(float("nan"), 0, 10)` returns `0`, because `min(nan, 10)` gives `nan` and `max(0, nan)` gives `0`. The design is silent on NaN, so I did not raise it as a finding. If NaN can reach this function, the author should decide the intended behavior.
- `low > high`: the design says callers guarantee `low <= high`, so I treated violations as out of scope. I did not ask for validation or a test.

Before merge, the author needs to run the test suite and share the result. Verification evidence should include the pass count, for example `python -m unittest discover -s tests`.
```

## Rationalizations observed (manual notes)

All checks pass after the Nit rule. The bench1 over-fire is gone: "If the min/max logic broke, at least one of those tests would fail."; header "0 actionable findings. Nothing needs fixing". Only nit: the `CaseTest` name.
