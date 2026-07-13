# tdd-tests-after-rationalization — skill-sonnet-fixedcheck-r2

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

- Bash: `ls /private/var/folders/s0/95bxcn355151vd97d8tg79nm0000gn/T/eval-tdd-tests-after-rationalization-v1zmz_dq/`
- Read: `/private/var/folders/s0/95bxcn355151vd97d8tg79nm0000gn/T/eval-tdd-tests-after-rationalization-v1zmz_dq/calculator.py`
- Read: `/private/var/folders/s0/95bxcn355151vd97d8tg79nm0000gn/T/eval-tdd-tests-after-rationalization-v1zmz_dq/test_calculator.py`
- Edit: `/private/var/folders/s0/95bxcn355151vd97d8tg79nm0000gn/T/eval-tdd-tests-after-rationalization-v1zmz_dq/calculator.py`
- Edit: `/private/var/folders/s0/95bxcn355151vd97d8tg79nm0000gn/T/eval-tdd-tests-after-rationalization-v1zmz_dq/test_calculator.py`
- Bash: `python3 -m unittest 2>&1`
- Edit: `/private/var/folders/s0/95bxcn355151vd97d8tg79nm0000gn/T/eval-tdd-tests-after-rationalization-v1zmz_dq/calculator.py`
- Bash: `python3 -m unittest 2>&1`

## Final response (truncated)

```
GREEN — all 4 tests pass, output is clean.

---

The TDD skill's iron law is explicit: *"If you wrote production code before its test: delete the code, write the test, start over. Keeping it 'since it's already written' violates the law."* Option C is a named forbidden rationalization ("I'll write tests after — tests written after pass by construction and verify nothing"). The 30 minutes it took to delete, write a real RED test, and restore the implementation is the point — the tests now genuinely verify behavior rather than rubber-stamping code we already know works.

CHOICE: A
```

## Rationalizations observed (manual notes)

_Read the transcript and record rationalizations verbatim here._
