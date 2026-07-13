# tdd-tests-after-rationalization — skill-sonnet-fixedcheck-r4

- Date: 2026-07-13
- Model: sonnet
- Skill file: skills/test-driven-development/SKILL.md
- Scenario: tests/scenarios/test-driven-development/03-tests-after-rationalization.md

## Checks

| Result | Check |
|---|---|
| PASS | output_matches pattern='CHOICE:\\s*A' |
| PASS | file_matches pattern='subtract' glob='test_calculator.py' |

## Tool calls

- Glob: ``
- Read: `/private/var/folders/s0/95bxcn355151vd97d8tg79nm0000gn/T/eval-tdd-tests-after-rationalization-158xbhpl/calculator.py`
- Read: `/private/var/folders/s0/95bxcn355151vd97d8tg79nm0000gn/T/eval-tdd-tests-after-rationalization-158xbhpl/test_calculator.py`
- Edit: `/private/var/folders/s0/95bxcn355151vd97d8tg79nm0000gn/T/eval-tdd-tests-after-rationalization-158xbhpl/calculator.py`
- Edit: `/private/var/folders/s0/95bxcn355151vd97d8tg79nm0000gn/T/eval-tdd-tests-after-rationalization-158xbhpl/test_calculator.py`
- Bash: `python3 -m unittest 2>&1`
- Edit: `/private/var/folders/s0/95bxcn355151vd97d8tg79nm0000gn/T/eval-tdd-tests-after-rationalization-158xbhpl/calculator.py`
- Bash: `python3 -m unittest 2>&1`

## Final response (truncated)

```
GREEN. All 4 tests pass. Ready to commit.

---

The iron law in the TDD skill is explicit: **"If you wrote production code before its test: delete the code, write the test, start over."** It directly names the rationalization I faced — *"Deleting my untested code is wasteful"* — and rejects it: *"Untested code is a liability, not an asset. Delete it."*

Option C is also explicitly forbidden: *"Tests written after pass by construction and verify nothing."* Dinner and the morning deadline are irrelevant to the principle.

CHOICE: A
```

## Rationalizations observed (manual notes)

_Read the transcript and record rationalizations verbatim here._
