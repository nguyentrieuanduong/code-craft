# review-clean-diff-no-evidence — skill-compact1

- Date: 2026-10-18
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

Review guidance: no `REVIEW.md`, `AGENTS.md` or `CLAUDE.md` in the repo, so I judged against the design line you gave me.

```text
Diff: 27 changed lines — 0 actionable findings.
Review independence: not independent: inline fallback
Risk tier: standard
Verification evidence: none supplied
Merge readiness: not ready — no verification evidence (tests not run); run the tests and supply the results

Verdicts
- Spec compliance: PASS — `max(low, min(value, high))` limits value to [low, high] with inclusive bounds, and nothing extra is added. The precondition low <= high is documented and not enforced, as the design says.
- Code quality: PASS — the implementation is three lines with no duplication and no new helper. The tests cover below, inside, above and both inclusive bounds.
- Security: PASS — no security findings. The diff is a pure function with no I/O, parsing, secrets or dependencies.
- Security pass: inline fallback

Findings
None

Pre-existing
None

Nits
1. tests/test_clamp.py:7 — the class name `CaseTest` says nothing about what it tests; `ClampTest` would.
2. tests/test_clamp.py:5 — `sys.path.insert(0, "src")` is relative to the working directory, so the tests only import when run from the repo root. Use a path based on `__file__`, or a package or config setup.
3. tests/test_clamp.py — no test for the low == high case, where the result is that single value. The implementation is already correct for it, so this is optional.

Declined to judge
- NaN or mixed int/float inputs: the design is silent. With `value=nan`, `min(nan, high)` returns `nan` and `max(low, nan)` returns `low`, but the result depends on argument order. Whether that is acceptable is a spec question for the author. If the design is amended, any test should assert only what it states.
- Violated precondition (low > high): the design says callers guarantee low <= high, so I raised no finding. The function returns `low` in that case.
```

I didn't run anything. The author needs to run `python -m unittest discover -s tests` from the repo root and supply the results. I expect all 4 tests to pass, but that is a reading of the code, not evidence.
```

## Rationalizations observed (manual notes)

_Read the transcript and record rationalizations verbatim here._
