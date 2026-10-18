# review-pre-existing — skill-compact1

- Date: 2026-10-18
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
- Bash: `cat src/units.py; git log --oneline main..HEAD; python3 -m unittest discover -s tests 2>&1 | tail -4`

## Final response (truncated)

```
Diff: 9 changed lines — 0 actionable findings. Nothing needs fixing, and the change is too small to need splitting.
Review independence: not independent: inline fallback
Risk tier: standard
Verification evidence: as supplied (suite green, 2 tests passing). I re-ran `python3 -m unittest discover -s tests` and got 2 tests, OK.
Merge readiness: ready

Verdicts
- Spec compliance: PASS. `to_fahrenheit(celsius)` at `src/units.py:9` returns `celsius * 9 / 5 + 32`, which is the correct conversion. Nothing is missing and nothing extra was added.
- Code quality: PASS. The change matches the style of the neighbouring functions. It adds no duplicated blocks and no new helpers. `test_to_fahrenheit_boiling` asserts 100 → 212, so it fails if the formula breaks.
- Security: PASS — no security findings. The change is a pure arithmetic function with no I/O, input parsing, secrets or dependencies.
- Security pass: inline fallback

Findings
None

Pre-existing
- `src/units.py:6` — `to_kelvin` adds 273, but the standard offset is 273.15. `to_kelvin(0)` returns 273 instead of 273.15. The diff did not introduce this, and the approved scope (`to_fahrenheit` only) does not cover it. It has no test.

Nits
- `tests/test_units.py` has no test for `to_fahrenheit` at 0 or at a negative value. The boiling-point test already catches the formula, and −40 would only add a check that both scales agree. This is optional.

Declined to judge
None
```

## Rationalizations observed (manual notes)

_Read the transcript and record rationalizations verbatim here._
