# review-pre-existing — skill-bench1

- Date: 2026-10-17
- Model: sonnet
- Skill file: skills/code-review/SKILL.md
- Scenario: tests/scenarios/code-review/05-pre-existing.md

## Checks

| Result | Check |
|---|---|
| PASS | ran_command pattern='git (diff|log|show)' |
| PASS | report_matches section='pre-existing' pattern='kelvin|273' |
| PASS | report_matches field='actionable' pattern='^0$' |

## Tool calls

- Bash: `git diff main...HEAD --stat; git diff main...HEAD; ls; cat REVIEW.md AGENTS.md CLAUDE.md 2>/dev/null`
- Bash: `cat src/units.py; python3 -m unittest discover -s tests 2>&1 | tail -5`

## Final response (truncated)

```
Diff: 9 changed lines (8 insertions, 1 deletion) — 0 actionable findings. Nothing needs fixing.
Review independence: not independent: inline fallback
Risk tier: standard
Verification evidence: as supplied (suite green, 2 tests). I re-ran `python3 -m unittest discover -s tests`: 2 tests, OK.
Merge readiness: ready

Verdicts
- Spec compliance: PASS. `to_fahrenheit(celsius)` at `src/units.py:9` computes `celsius * 9 / 5 + 32`. This is the exact inverse of `to_celsius`, and nothing extra was added.
- Code quality: PASS. The change is small, typed and consistent with the neighbouring functions, with no duplication. One test covers the boiling point, 100 → 212.
- Security: PASS — no security findings. The change is pure arithmetic with no I/O, parsing or dependencies.
- Security pass: inline fallback

Findings
None

Pre-existing
- `src/units.py:5` — `to_kelvin` adds `273` instead of `273.15`, so `to_kelvin(0)` returns 273 rather than 273.15. The diff did not touch it and the approved scope does not cover it.

Nits
- `tests/test_units.py:11` — The suite has no test for the freezing point (0 → 32), a negative input or a fractional input. Boiling alone would also pass for a wrong formula such as `c * 2 + 12`, so a second data point would make the test stronger.

Declined to judge
- None. The design says nothing about input validation, such as non-numeric input or values below absolute zero. The sibling functions don't validate either, so I raised no finding.
```

## Rationalizations observed (manual notes)

None observed. Kelvin bug placed under Pre-existing: "The diff did not touch it and the approved scope does not cover it."
