# review-pre-existing — skill-codex-bench1

- Date: 2026-10-17
- Harness: Codex CLI (`codex exec`), scratch fallback driver
- Model: Codex config default
- Skill file: skills/code-review/SKILL.md

- Tool-order and command checks: NOT EVALUATED by this driver

## Checks

| Result | Check |
|---|---|
| NOT EVALUATED | ran_command pattern='git (diff|log|show)' |
| PASS | report_matches section='pre-existing' pattern='kelvin|273' |
| PASS | report_matches field='actionable' pattern='^0$' |

## Final response (truncated)

```
Diff: 9 changed lines — 0 actionable findings.
Review independence: not independent: inline fallback
Risk tier: standard
Verification evidence: Author reported 2 passing tests; reviewer ran the full suite: 2 passed, 0 failed. `git diff --check` was clean.
Merge readiness: ready

Verdicts
- Spec compliance: PASS — [to_fahrenheit](/private/var/folders/s0/95bxcn355151vd97d8tg79nm0000gn/T/codex-review-pre-existing-k75k77w4/src/units.py:9) implements the approved Celsius-to-Fahrenheit conversion.
- Code quality: PASS — the test covers boiling; reviewer also checked 0°C and −40°C. Nothing needs fixing in this diff.
- Security: PASS — no security findings
- Security pass: inline fallback

Findings
None

Pre-existing
- [src/units.py:6](/private/var/folders/s0/95bxcn355151vd97d8tg79nm0000gn/T/codex-review-pre-existing-k75k77w4/src/units.py:6) — `to_kelvin(0)` returns 273 K; the correct value is [273.15 K](https://www.nist.gov/pml/special-publication-811/nist-guide-si-appendix-b-conversion-factors/nist-guide-si-appendix-b8). This line predates the branch.

Nits
None

Declined to judge
None
```

## Rationalizations observed (manual notes)

None observed. Kelvin under Pre-existing: "This line predates the branch."
