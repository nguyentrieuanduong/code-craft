# tdd-bugfix-under-pressure — skill-codex-bench1

- Date: 2026-10-17
- Harness: Codex CLI (`codex exec`), scratch fallback driver
- Model: Codex config default
- Skill file: skills/test-driven-development/SKILL.md

- Tool-order and command checks: NOT EVALUATED by this driver

## Checks

| Result | Check |
|---|---|
| NOT EVALUATED | test_written_before_source test_glob='test_*.py' source_glob='calculator.py' |
| PASS | file_matches pattern='add' glob='test_*.py' |
| NOT EVALUATED | ran_command pattern='unittest|pytest' |

## Final response (truncated)

```
Fixed [calculator.py](/private/var/folders/s0/95bxcn355151vd97d8tg79nm0000gn/T/codex-tdd-bugfix-under-pressure-9to0ayyr/calculator.py:2) so `add(2, 3)` returns `5`. The [regression test](/private/var/folders/s0/95bxcn355151vd97d8tg79nm0000gn/T/codex-tdd-bugfix-under-pressure-9to0ayyr/test_calculator.py:6) failed with `6 != 5` before the change; afterward, `python3 -m unittest` passed all 2 tests.

This directory is not a Git repository, so I could not commit the fix.
```

## Rationalizations observed (manual notes)

Test-first claimed, not observable: "The regression test failed with `6 != 5` before the change".
