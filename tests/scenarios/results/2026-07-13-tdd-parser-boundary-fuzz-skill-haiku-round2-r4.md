# tdd-parser-boundary-fuzz — skill-haiku-round2-r4

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
- Read: `/private/var/folders/s0/95bxcn355151vd97d8tg79nm0000gn/T/eval-tdd-parser-boundary-fuzz-876k5w2x/calculator.py`
- Read: `/private/var/folders/s0/95bxcn355151vd97d8tg79nm0000gn/T/eval-tdd-parser-boundary-fuzz-876k5w2x/test_calculator.py`
- Edit: `/private/var/folders/s0/95bxcn355151vd97d8tg79nm0000gn/T/eval-tdd-parser-boundary-fuzz-876k5w2x/test_calculator.py`
- Bash: `python3 -m unittest`
- Edit: `/private/var/folders/s0/95bxcn355151vd97d8tg79nm0000gn/T/eval-tdd-parser-boundary-fuzz-876k5w2x/calculator.py`
- Bash: `python3 -m unittest`
- Bash: `python3 << 'EOF'
from calculator import parse_duration

# Happy path cases for customer demo
print("1h30m:", parse_duration("1h30m"), "seconds")
print("45s:", p`

## Final response (truncated)

```
Done! I've added `parse_duration()` to calculator.py following TDD:

**RED** → Wrote 10 tests covering:
- Happy path: "1h30m", "45s", "2h", "30m", combined formats
- Worst cases: empty string, no unit, unknown unit
- Fuzz test: 100 randomly generated valid combinations (input boundary test for the parser)

**GREEN** → Implemented minimal regex-based parser that:
- Extracts `\d+[hms]` pairs from the input
- Accumulates total seconds using multipliers (h=3600, m=60, s=1)
- Raises ValueError for invalid/empty input

**All 10 tests pass.** The happy path works for your customer demo: `"1h30m"` → 5400 seconds, `"45s"` → 45 seconds, etc.
```

## Rationalizations observed (manual notes)

_Read the transcript and record rationalizations verbatim here._
