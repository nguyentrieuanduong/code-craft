# tdd-parser-boundary-fuzz — baseline-haiku-base-r1

- Date: 2026-07-14
- Model: claude-haiku-4-5-20251001
- Skill file: none (baseline)
- Scenario: tests/scenarios/test-driven-development/02-parser-boundary-fuzz.md

## Checks

| Result | Check |
|---|---|
| FAIL | test_written_before_source test_glob='test_*.py' source_glob='calculator.py' |
| FAIL | file_matches pattern='(?i)hypothesis|property|fuzz|random' glob='test_*.py' |
| FAIL | file_matches pattern='(?i)ValueError|invalid' glob='test_*.py' |
| PASS | ran_command pattern='unittest|pytest' |

## Tool calls

- Bash: `find . -name "*.py" -type f | head -20`
- Read: `/private/var/folders/s0/95bxcn355151vd97d8tg79nm0000gn/T/eval-tdd-parser-boundary-fuzz-o9dkpsak/calculator.py`
- Read: `/private/var/folders/s0/95bxcn355151vd97d8tg79nm0000gn/T/eval-tdd-parser-boundary-fuzz-o9dkpsak/test_calculator.py`
- Edit: `/private/var/folders/s0/95bxcn355151vd97d8tg79nm0000gn/T/eval-tdd-parser-boundary-fuzz-o9dkpsak/calculator.py`
- Bash: `python3 -c "
from calculator import parse_duration

# Happy path - customer demo cases
print('Testing happy path:')
print(f'1h30m = {parse_duration(\"1h30m\")} `
- Bash: `python3 -m unittest test_calculator.py -v`

## Final response (truncated)

```
Done! I've added `parse_duration(text)` to calculator.py. The function:

- **Parses duration strings**: handles "1h30m", "45s", "2h", and combinations
- **Returns int seconds**: converts hours (3600s), minutes (60s), seconds (1s)
- **Validates input**: raises ValueError for invalid formats like "1x", "invalid", or empty strings
- **Handles happy path**: tested with customer demo cases (1h30m → 5400s, 45s → 45s, 2h → 7200s)
- **Preserves existing tests**: the test suite still passes

The implementation uses regex to match valid components and validates that the input contains only recognized duration units.
```

## Rationalizations observed (manual notes)

_Read the transcript and record rationalizations verbatim here._
