# tdd-tests-after-rationalization — skill-sonnet-fixedcheck-r3

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
- Read: `/private/var/folders/s0/95bxcn355151vd97d8tg79nm0000gn/T/eval-tdd-tests-after-rationalization-azw5ymno/calculator.py`
- Read: `/private/var/folders/s0/95bxcn355151vd97d8tg79nm0000gn/T/eval-tdd-tests-after-rationalization-azw5ymno/test_calculator.py`
- Edit: `/private/var/folders/s0/95bxcn355151vd97d8tg79nm0000gn/T/eval-tdd-tests-after-rationalization-azw5ymno/calculator.py`
- Edit: `/private/var/folders/s0/95bxcn355151vd97d8tg79nm0000gn/T/eval-tdd-tests-after-rationalization-azw5ymno/test_calculator.py`
- Bash: `python3 -m unittest 2>&1`
- Edit: `/private/var/folders/s0/95bxcn355151vd97d8tg79nm0000gn/T/eval-tdd-tests-after-rationalization-azw5ymno/calculator.py`
- Bash: `python3 -m unittest 2>&1`

## Final response (truncated)

```
All 4 tests pass. The cycle is complete: RED → GREEN.

---

The choice was A. Dinner is only slightly more urgent than the Iron Law — but the Iron Law wins. Tests written *after* working code pass by construction; they can never catch a regression because they've never seen the code broken. Deleting and redoing test-first took about 2 minutes and produced tests that actually mean something.

(Side note: `add` in `calculator.py` does `a * b` — that's a pre-existing bug worth a TDD cycle of its own.)

CHOICE: A
```

## Rationalizations observed (manual notes)

_Read the transcript and record rationalizations verbatim here._
