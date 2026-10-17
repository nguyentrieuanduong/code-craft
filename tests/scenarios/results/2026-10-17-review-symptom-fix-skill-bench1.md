# review-symptom-fix — skill-bench1

- Date: 2026-10-17
- Model: sonnet
- Skill file: skills/code-review/SKILL.md
- Scenario: tests/scenarios/code-review/11-symptom-fix.md

## Checks

| Result | Check |
|---|---|
| PASS | output_matches pattern='(?i)root cause|symptom' |
| PASS | report_matches section='findings' severity=['blocking', 'should-fix'] pattern='tax\\.py' |
| PASS | report_matches section='pre-existing' pattern='legacy|report_export' |
| PASS | report_not_matches section='pre-existing' pattern='^\\W*(src/)?tax\\.py' |

## Tool calls

- Bash: `git diff main...HEAD --stat; git diff main...HEAD; git log main..HEAD --oneline; ls; cat REVIEW.md AGENTS.md CLAUDE.md 2>/dev/null`
- Bash: `cd /private/var/folders/s0/95bxcn355151vd97d8tg79nm0000gn/T/eval-review-symptom-fix-zmuaa_v3; git show main --stat | head; find src tests legacy -type f | xargs`

## Final response (truncated)

```
Diff: 8 changed lines — 3 actionable findings.
Review independence: not independent: inline fallback
Risk tier: standard (discount/tax arithmetic only; no auth, billing, secrets, CI, migration or release files touched)
Verification evidence: as supplied (suite green, 2 tests). I re-ran `python3 -m unittest discover -s tests` and got 2 tests, OK.
Merge readiness: not ready — symptom-only fix; the tax crash from the stated scope is unfixed.

Verdicts
- Spec compliance: FAIL — `with_tax` still crashes on `'%'` rates, and the discount path now returns a wrong amount instead of crashing.
- Code quality: FAIL — a blanket `except ValueError` hides bad input, and the test locks in the wrong behavior.
- Security: PASS — no security findings
- Security pass: inline fallback

Findings
1. Blocking — src/discount.py:5-7 — This is a symptom fix. The root cause is that `parse_percent` (src/percent.py:2) calls `float("10%")` and never strips the `%`. The patch catches `ValueError` in `discounted`, so `discounted(100, "10%")` returns 100 and the 10% discount is silently dropped. Garbage like `"abc"` also returns the full price with no error. The same handler hides a real input bug as a billing-amount error. Fix: make `parse_percent` accept an optional trailing `%` (`text.strip().rstrip("%")`), and let genuinely invalid input raise. Remove the `try/except`.
2. Blocking — tests/test_discount.py:12-14 — `test_percent_sign_no_longer_crashes` asserts `discounted(100, "10%") == 100`, which encodes the wrong behavior. A correct fix would fail this test, so the "suite green" evidence supports the bug. Fix: assert `== 90`, and add a test that invalid text such as `"abc"` raises `ValueError`.
3. Blocking — src/tax.py:2 — The approved scope says "discount and tax", but `with_tax(100, "8%")` still raises `ValueError`. `with_tax` also re-implements the parsing that `parse_percent` does, so the bug exists twice. Fix: have `with_tax` call `parse_percent`, which the root-cause fix then covers, and add a `with_tax` test with `"8%"`.

Bug class: percent text parsed with a bare `float(text) / 100`. I searched the repo and found three instances: percent.py, tax.py and legacy/report_export.py. The first two are in scope.

Pre-existing
- legacy/report_export.py:2 — `margin_column` uses the same `float(rate_text) / 100` and crashes on `"%"`. It is not in the claimed scope. Track it, and have it use `parse_percent` once that is fixed.

Nits
- tests/test_discount.py:8 — the class name `CaseTest` is non-descriptive.

Declined to judge
- None
```

## Rationalizations observed (manual notes)

None observed. Root cause and bug class named: "Bug class: percent text parsed with a bare `float(text) / 100`. I searched the repo and found three instances".
