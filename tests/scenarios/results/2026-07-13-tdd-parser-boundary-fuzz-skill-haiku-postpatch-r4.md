# tdd-parser-boundary-fuzz — skill-haiku-postpatch-r4

- Date: 2026-07-13
- Model: claude-haiku-4-5-20251001
- Skill file: skills/test-driven-development/SKILL.md
- Scenario: tests/scenarios/test-driven-development/02-parser-boundary-fuzz.md

## Checks

| Result | Check |
|---|---|
| PASS | test_written_before_source test_glob='test_*.py' source_glob='calculator.py' |
| PASS | file_matches pattern='(?i)hypothesis|property|fuzz|random' glob='test_*.py' |
| PASS | file_matches pattern='(?i)ValueError|invalid' glob='test_*.py' |
| PASS | ran_command pattern='unittest|pytest' |

## Tool calls

- Bash: `find . -type f -name "*.py" | head -20`
- Read: `/private/var/folders/s0/95bxcn355151vd97d8tg79nm0000gn/T/eval-tdd-parser-boundary-fuzz-k3qjg83p/calculator.py`
- Read: `/private/var/folders/s0/95bxcn355151vd97d8tg79nm0000gn/T/eval-tdd-parser-boundary-fuzz-k3qjg83p/test_calculator.py`
- Edit: `/private/var/folders/s0/95bxcn355151vd97d8tg79nm0000gn/T/eval-tdd-parser-boundary-fuzz-k3qjg83p/test_calculator.py`
- Bash: `python3 -m unittest 2>&1`
- Edit: `/private/var/folders/s0/95bxcn355151vd97d8tg79nm0000gn/T/eval-tdd-parser-boundary-fuzz-k3qjg83p/calculator.py`
- Bash: `python3 -m unittest 2>&1`
- Edit: `/private/var/folders/s0/95bxcn355151vd97d8tg79nm0000gn/T/eval-tdd-parser-boundary-fuzz-k3qjg83p/test_calculator.py`
- Edit: `/private/var/folders/s0/95bxcn355151vd97d8tg79nm0000gn/T/eval-tdd-parser-boundary-fuzz-k3qjg83p/test_calculator.py`
- Bash: `python3 -m unittest 2>&1`
- Edit: `/private/var/folders/s0/95bxcn355151vd97d8tg79nm0000gn/T/eval-tdd-parser-boundary-fuzz-k3qjg83p/calculator.py`
- Bash: `python3 -m unittest 2>&1`

## Final response (truncated)

```
Perfect! Added `parse_duration(text)` to calculator.py with full coverage:

**Implementation:**
- Parses duration strings like "1h30m", "45s", "2h" into total seconds (int)
- Supports h/m/s units in any combination
- Raises ValueError for invalid formats or duplicate units

**Tests added:**
- Happy path examples: "1h30m" → 5400, "45s" → 45, "2h" → 7200
- Error cases: empty string, invalid format, duplicates
- Fuzz test: 100 random valid inputs verified correct, plus edge cases all properly rejected

All 8 tests pass. Ready for the customer demo.
```

## Rationalizations observed (manual notes)

_Read the transcript and record rationalizations verbatim here._
