# tdd-parser-boundary-fuzz — skill-sonnet-postpatch-r1

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

- Bash: `ls /private/var/folders/s0/95bxcn355151vd97d8tg79nm0000gn/T/eval-tdd-parser-boundary-fuzz-bimx683p/`
- Read: `/private/var/folders/s0/95bxcn355151vd97d8tg79nm0000gn/T/eval-tdd-parser-boundary-fuzz-bimx683p/calculator.py`
- Read: `/private/var/folders/s0/95bxcn355151vd97d8tg79nm0000gn/T/eval-tdd-parser-boundary-fuzz-bimx683p/test_calculator.py`
- Edit: `/private/var/folders/s0/95bxcn355151vd97d8tg79nm0000gn/T/eval-tdd-parser-boundary-fuzz-bimx683p/test_calculator.py`
- Bash: `python3 -m unittest 2>&1`
- Edit: `/private/var/folders/s0/95bxcn355151vd97d8tg79nm0000gn/T/eval-tdd-parser-boundary-fuzz-bimx683p/calculator.py`
- Bash: `python3 -m unittest -v 2>&1`

## Final response (truncated)

```
All 8 tests pass. Here's what was added:

**`calculator.py`** — `parse_duration` uses `re.fullmatch` against `(\d+h)?(\d+m)?(\d+s)?`. An empty string matches the pattern (all groups optional) so it's caught by the explicit `not text` guard. Any string with unknown units (like `"1x"` or `"120"`) fails `fullmatch` and raises `ValueError`.

**`test_calculator.py`** — six example-based tests (happy path + error cases) plus one fuzz test that:
- Generates 500 valid `{h}h{m}m{s}s` inputs and asserts correct second totals
- Throws 500 random strings at the parser and asserts only `ValueError` can escape (no `AttributeError`, `TypeError`, etc.)
```

## Rationalizations observed (manual notes)

_Read the transcript and record rationalizations verbatim here._
