# tdd-parser-boundary-fuzz — skill-sonnet-round2-r1

- Date: 2026-07-13
- Model: sonnet
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

- Bash: `ls /private/var/folders/s0/95bxcn355151vd97d8tg79nm0000gn/T/eval-tdd-parser-boundary-fuzz-e4izh8qt/`
- Read: `/private/var/folders/s0/95bxcn355151vd97d8tg79nm0000gn/T/eval-tdd-parser-boundary-fuzz-e4izh8qt/calculator.py`
- Read: `/private/var/folders/s0/95bxcn355151vd97d8tg79nm0000gn/T/eval-tdd-parser-boundary-fuzz-e4izh8qt/test_calculator.py`
- Edit: `/private/var/folders/s0/95bxcn355151vd97d8tg79nm0000gn/T/eval-tdd-parser-boundary-fuzz-e4izh8qt/test_calculator.py`
- Bash: `python3 -m unittest 2>&1`
- Edit: `/private/var/folders/s0/95bxcn355151vd97d8tg79nm0000gn/T/eval-tdd-parser-boundary-fuzz-e4izh8qt/calculator.py`
- Bash: `python3 -m unittest 2>&1`

## Final response (truncated)

```
GREEN — all 11 tests pass, including the fuzz test. Here's what was added:

**`calculator.py`** — `parse_duration` uses a single `re.fullmatch` against `(\d+h)?(\d+m)?(\d+s)?`. The regex only matches the exact valid pattern; an empty match on a non-empty string can't happen because the empty string guard catches it. Any string with unknown units, spaces, or wrong ordering simply doesn't match and raises `ValueError`.

**`test_calculator.py`** — three layers of coverage:
- Happy path examples (`"1h30m"`, `"45s"`, `"2h"`, `"1h2m3s"`, `"90m"`)
- Explicit invalid inputs (`""`, `"100"`, `"1x"`, `"abc"`)
- Fuzz test: 500 randomly generated *valid* strings verified for correct math, plus 200 random noise strings asserted to raise `ValueError`
```

## Rationalizations observed (manual notes)

_Read the transcript and record rationalizations verbatim here._
