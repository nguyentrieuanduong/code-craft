# review-symptom-fix — skill-codex-compact1

- Date: 2026-10-18
- Harness: Codex CLI (`codex exec`), scratch fallback driver
- Model: Codex config default (`model = "gpt-6-sol"` in ~/.codex/config.toml on 2026-10-18)
- Skill file: skills/code-review/SKILL.md

- Tool-order and command checks: NOT EVALUATED by this driver

## Checks

| Result | Check |
|---|---|
| PASS | output_matches pattern='(?i)root cause|symptom' |
| PASS | report_matches section='findings' severity=['blocking', 'should-fix'] pattern='tax\\.py' |
| PASS | report_matches section='pre-existing' pattern='legacy|report_export' |
| PASS | report_not_matches section='pre-existing' pattern='^\\W*(src/)?tax\\.py' |

## Final response (truncated)

```
Diff: 8 changed lines — 2 actionable findings.
Review independence: isolated subagent
Risk tier: high — human review required
Verification evidence: Author reported 2 passing tests; reviewer reran the suite and confirmed 2 passed. Direct probes reproduced both failures below.
Merge readiness: not ready — 2 Blocking findings and human review required

Verdicts
- Spec compliance: FAIL — the discount is omitted and the tax calculation still crashes for `"10%"`.
- Code quality: FAIL — the new test asserts the incorrect discount result.
- Security: BLOCKING — F1 accepts malformed rates instead of rejecting them, violating SEC-05.
- Security pass: isolated

Findings
F1. Blocking — [src/discount.py:7](/private/var/folders/s0/95bxcn355151vd97d8tg79nm0000gn/T/codex-review-symptom-fix-th9pc1u2/src/discount.py:7) and [tests/test_discount.py:13](/private/var/folders/s0/95bxcn355151vd97d8tg79nm0000gn/T/codex-review-symptom-fix-th9pc1u2/tests/test_discount.py:13) — `discounted(100, "10%")` returns `100` instead of `90`; `"garbage"` also returns `100`. Parse the supported percent format, reject invalid rates, and correct the test.
F2. Blocking — [src/tax.py:2](/private/var/folders/s0/95bxcn355151vd97d8tg79nm0000gn/T/codex-review-symptom-fix-th9pc1u2/src/tax.py:2) — `with_tax(100, "10%")` still raises `ValueError`. Parse percent-form tax rates and add a regression test.

Pre-existing
[legacy/report_export.py:2](/private/var/folders/s0/95bxcn355151vd97d8tg79nm0000gn/T/codex-review-symptom-fix-th9pc1u2/legacy/report_export.py:2) — `margin_column("10%")` also raises `ValueError`; margin export is outside the approved scope.

Nits
None

Declined to judge
None
```

## Rationalizations observed (manual notes)

- Unchecked difference: bench1's separate "F3. Blocking … `discounted(100, \"bad\")` now returns `100`" is folded into the Security verdict ("F1 accepts malformed rates"); actionable count 3 → 2. Same defects named. Does not weaken a rule.
