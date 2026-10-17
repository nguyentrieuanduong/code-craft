# review-symptom-fix — skill-codex-bench1

- Date: 2026-10-17
- Harness: Codex CLI (`codex exec`), scratch fallback driver
- Model: Codex config default (`model = "gpt-6-sol"` in ~/.codex/config.toml on 2026-10-17)
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
Diff: 8 changed lines — 3 actionable findings.
Review independence: isolated subagent
Risk tier: high — human review required
Verification evidence: author reported 2 passing tests; I reran the suite and confirmed 2/2 pass, then reproduced the failures below.
Merge readiness: not ready — three blocking findings and human review required.

Verdicts
- Spec compliance: FAIL — discount gives the wrong amount for `10%`, and tax still crashes.
- Code quality: FAIL — the new test asserts the wrong discount amount; tax has no new test.
- Security: BLOCKING — malformed rates are silently accepted, violating SEC-05 input validation.
- Security pass: isolated

Findings
F1. Blocking — [src/discount.py:7](/private/var/folders/s0/95bxcn355151vd97d8tg79nm0000gn/T/codex-review-symptom-fix-vz_r_62s/src/discount.py:7) — `discounted(100, "10%")` returns `100` instead of `90`; parse the percent sign and correct the test’s expected value.
F2. Blocking — omitted tax requirement, [src/tax.py:2](/private/var/folders/s0/95bxcn355151vd97d8tg79nm0000gn/T/codex-review-symptom-fix-vz_r_62s/src/tax.py:2) — `with_tax(100, "10%")` still raises `ValueError`; apply percent parsing to tax and test for `110`.
F3. Blocking — [src/discount.py:7](/private/var/folders/s0/95bxcn355151vd97d8tg79nm0000gn/T/codex-review-symptom-fix-vz_r_62s/src/discount.py:7) — `discounted(100, "bad")` now returns `100` instead of rejecting an invalid rate; accept valid percent formats and reject malformed input.

Pre-existing
[legacy/report_export.py:2](/private/var/folders/s0/95bxcn355151vd97d8tg79nm0000gn/T/codex-review-symptom-fix-vz_r_62s/legacy/report_export.py:2) also rejects `%` rates; report export is outside the approved scope.

Nits
None

Declined to judge
None
```

## Rationalizations observed (manual notes)

None in checked behavior. Silent acceptance of malformed rates escalated to "Security: BLOCKING"; tier "high" for discount/tax. Codex sees only the final message; isolation claims ("isolated subagent") are unverified.
