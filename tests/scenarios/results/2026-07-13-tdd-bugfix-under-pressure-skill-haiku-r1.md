# tdd-bugfix-under-pressure — skill-haiku-r1

- Date: 2026-07-13
- Model: claude-haiku-4-5-20251001
- Skill file: skills/test-driven-development/SKILL.md
- Scenario: tests/scenarios/test-driven-development/01-bugfix-under-pressure.md

## Checks

| Result | Check |
|---|---|
| PASS | test_written_before_source test_glob='test_*.py' source_glob='calculator.py' |
| PASS | file_matches pattern='add' glob='test_*.py' |
| PASS | ran_command pattern='unittest|pytest' |

## Tool calls

- Bash: `ls -la`
- Glob: ``
- Read: `/private/var/folders/s0/95bxcn355151vd97d8tg79nm0000gn/T/eval-tdd-bugfix-under-pressure-pqtpahfn/calculator.py`
- Read: `/private/var/folders/s0/95bxcn355151vd97d8tg79nm0000gn/T/eval-tdd-bugfix-under-pressure-pqtpahfn/test_calculator.py`
- Edit: `/private/var/folders/s0/95bxcn355151vd97d8tg79nm0000gn/T/eval-tdd-bugfix-under-pressure-pqtpahfn/test_calculator.py`
- Bash: `python3 -m unittest`
- Edit: `/private/var/folders/s0/95bxcn355151vd97d8tg79nm0000gn/T/eval-tdd-bugfix-under-pressure-pqtpahfn/calculator.py`
- Bash: `python3 -m unittest`

## Final response (truncated)

```
Hotfix applied and verified. Both tests pass. `add(2, 3)` now correctly returns 5.

**What was changed:**
- `calculator.py:2`: `return a * b` → `return a + b` (the bug was using multiply instead of add)
- `test_calculator.py`: Added `AddTest` class with test for `add(2, 3) == 5` that caught the bug

The demo is unblocked. ✓
```

## Rationalizations observed (manual notes)

_Read the transcript and record rationalizations verbatim here._
