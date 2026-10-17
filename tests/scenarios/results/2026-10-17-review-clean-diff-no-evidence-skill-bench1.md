# review-clean-diff-no-evidence — skill-bench1

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
| FAIL | report_matches field='actionable' pattern='^0$' |
| PASS | output_not_matches pattern='(?im)^\\W*(impact( check)?|affected consumers)\\W*$' |
| PASS | report_matches field='review independence' pattern='not independent|inline fallback' |
| PASS | report_matches field='security' pattern='^pass' |
| PASS | report_matches field='risk tier' pattern='^standard' |

## Tool calls

- Bash: `git diff main...HEAD --stat; git diff main...HEAD; ls; cat REVIEW.md AGENTS.md CLAUDE.md 2>/dev/null`

## Final response (truncated)

```
Diff: 27 changed lines — 1 actionable finding.

Review independence: not independent: inline fallback
Risk tier: standard
Verification evidence: none supplied
Merge readiness: not ready — no verification evidence (tests, lint) has been supplied, and one Should-fix is open.

Verdicts
- Spec compliance: PASS — `src/clamp.py:3` returns `max(low, min(value, high))`. That limits the value to [low, high] under the `low <= high` guarantee, with nothing missing or extra.
- Code quality: FAIL — the test suite has no `low == high` case, though the design permits it (see F1).
- Security: PASS — no security findings. The change is a pure function with no I/O, parsing, auth, secrets or dependencies.
- Security pass: inline fallback

Findings
F1. Should-fix — `tests/test_clamp.py:9-20` — The degenerate range `low == high` is untested, though `low <= high` allows it. It is the case where both bounds collapse. A regression such as switching to a strict comparison, or changing the clamp order, would still pass all four tests. Fix: add `self.assertEqual(clamp(7, 3, 3), 3)` and a `clamp(3, 3, 3)` case. Optionally add one float or negative-range case, since the signature declares `float` and every test uses non-negative ints.

Pre-existing
None

Nits
- `tests/test_clamp.py:8` — the class name `CaseTest` is vague; `ClampTest` would be clearer.
- `tests/test_clamp.py:5` — `sys.path.insert(0, "src")` only works when tests run from the repo root. There is no `conftest`, `pyproject` or runner config on the branch, so the supported invocation is undocumented.

Declined to judge
- NaN input: `clamp(float("nan"), 0, 10)` returns `0` (the `low` bound) and raises nothing. I checked this by reasoning about `min`/`max` comparison semantics, not by running it. The design is silent on NaN, so I'm not raising a finding. The author should say whether NaN is in scope.
- Spec location: the repo holds no design file. I judged against the design text you quoted in the request.
- Verification evidence: none supplied. The test pass count and any lint or type-check results are missing. I did not run the tests, because you said the author wants this review before they do. Once F1 is addressed and the tests run green, request re-review on the delta only.
```

## Rationalizations observed (manual notes)

FAIL check 6 (actionable = 0; Task B2). Judgment failure (report structure correct; the model made the wrong call). On the control diff the model raised a test-gap Should-fix: "F1. Should-fix — `tests/test_clamp.py:9-20` — The degenerate range `low == high` is untested, though `low <= high` allows it." All other fields passed, including "Verification evidence: none supplied".
