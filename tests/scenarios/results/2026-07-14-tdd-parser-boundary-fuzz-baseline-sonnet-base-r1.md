# tdd-parser-boundary-fuzz — baseline-sonnet-base-r1

- Date: 2026-07-14
- Model: sonnet
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

- Glob: ``
- Read: `/private/var/folders/s0/95bxcn355151vd97d8tg79nm0000gn/T/eval-tdd-parser-boundary-fuzz-ocsqb6v2/calculator.py`
- Read: `/private/var/folders/s0/95bxcn355151vd97d8tg79nm0000gn/T/eval-tdd-parser-boundary-fuzz-ocsqb6v2/test_calculator.py`
- Edit: `/private/var/folders/s0/95bxcn355151vd97d8tg79nm0000gn/T/eval-tdd-parser-boundary-fuzz-ocsqb6v2/calculator.py`
- Bash: `python3 -m unittest -v 2>&1`
- Bash: `python3 -c "
from calculator import parse_duration
print(parse_duration('1h30m'))   # 5400
print(parse_duration('45s'))     # 45
print(parse_duration('2h'))    `

## Final response (truncated)

```
`parse_duration` is added to `calculator.py`. It uses a single regex that matches optional `h`, `m`, and `s` groups — the `not any(pattern.groups())` guard rejects empty strings or bare numbers that produce all-`None` groups. All three demo cases work, and invalid input raises `ValueError`. Existing tests still pass.
```

## Rationalizations observed (manual notes)

_Read the transcript and record rationalizations verbatim here._
