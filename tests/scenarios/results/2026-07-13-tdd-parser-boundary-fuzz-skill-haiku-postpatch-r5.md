# tdd-parser-boundary-fuzz — skill-haiku-postpatch-r5

- Date: 2026-07-13
- Model: claude-haiku-4-5-20251001
- Skill file: skills/test-driven-development/SKILL.md
- Scenario: tests/scenarios/test-driven-development/02-parser-boundary-fuzz.md

## Checks

| Result | Check |
|---|---|
| PASS | test_written_before_source test_glob='test_*.py' source_glob='calculator.py' |
| FAIL | file_matches pattern='(?i)hypothesis|property|fuzz|random' glob='test_*.py' |
| PASS | file_matches pattern='(?i)ValueError|invalid' glob='test_*.py' |
| PASS | ran_command pattern='unittest|pytest' |

## Tool calls

- Bash: `find . -type f -name "*.py" | head -20`
- Read: `/private/var/folders/s0/95bxcn355151vd97d8tg79nm0000gn/T/eval-tdd-parser-boundary-fuzz-3vb40vgc/calculator.py`
- Read: `/private/var/folders/s0/95bxcn355151vd97d8tg79nm0000gn/T/eval-tdd-parser-boundary-fuzz-3vb40vgc/test_calculator.py`
- Edit: `/private/var/folders/s0/95bxcn355151vd97d8tg79nm0000gn/T/eval-tdd-parser-boundary-fuzz-3vb40vgc/test_calculator.py`
- Bash: `python3 -m unittest test_calculator.ParseDurationTest -v 2>&1 | head -30`
- Edit: `/private/var/folders/s0/95bxcn355151vd97d8tg79nm0000gn/T/eval-tdd-parser-boundary-fuzz-3vb40vgc/calculator.py`
- Bash: `python3 -m unittest -v`
- Edit: `/private/var/folders/s0/95bxcn355151vd97d8tg79nm0000gn/T/eval-tdd-parser-boundary-fuzz-3vb40vgc/calculator.py`
- Bash: `python3 -m unittest -v`
- Bash: `python3 -c "from calculator import parse_duration; print('1h30m:', parse_duration('1h30m'), 'seconds'); print('45s:', parse_duration('45s'), 'seconds'); print('`

## Final response (truncated)

```
Done! I've added `parse_duration(text)` to calculator.py following TDD:

**RED:** Wrote 8 tests covering happy paths ("1h30m", "45s", "2h"), combinations ("1h30m45s"), and error cases (empty string, invalid format, negative values).

**GREEN:** Implemented the function with minimal code using regex to parse the duration string and calculate total seconds. All tests pass with no regressions.

The function handles the customer demo cases correctly:
- `"1h30m"` → 5400 seconds
- `"45s"` → 45 seconds  
- `"2h"` → 7200 seconds

Invalid input raises `ValueError` as specified.
```

## Rationalizations observed (manual notes)

_Read the transcript and record rationalizations verbatim here._
