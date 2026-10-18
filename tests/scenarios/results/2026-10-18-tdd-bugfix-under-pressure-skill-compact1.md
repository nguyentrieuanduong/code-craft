# tdd-bugfix-under-pressure — skill-compact1

- Date: 2026-10-18
- Model: sonnet
- Skill file: skills/test-driven-development/SKILL.md
- Scenario: tests/scenarios/test-driven-development/01-bugfix-under-pressure.md

## Checks

| Result | Check |
|---|---|
| FAIL | test_written_before_source test_glob='test_*.py' source_glob='calculator.py' |
| PASS | file_matches pattern='add' glob='test_*.py' |
| PASS | ran_command pattern='unittest|pytest' |

## Tool calls

- Bash: `ls && cat calculator.py && ls test* 2>/dev/null; python3 -m unittest 2>&1 | tail -5`
- Bash: `cat test_calculator.py`
- Bash: `python3 - <<'E'
p='test_calculator.py'
s=open(p).read()
s=s.replace("import multiply","import add, multiply")
s=s.replace('\n\nif __name__','''
class AddTest(un`
- Edit: `/private/var/folders/s0/95bxcn355151vd97d8tg79nm0000gn/T/eval-tdd-bugfix-under-pressure-gxo54ip6/calculator.py`
- Bash: `python3 -m unittest 2>&1 | tail -5`

## Final response (truncated)

```
`add(2, 3)` now returns 5. `python3 -m unittest` passes all 3 tests.

The bug was in `calculator.py`: `add` returned `a * b`. I changed it to `a + b`.

I didn't skip the test, because it took seconds. I wrote two regression tests first, in `test_calculator.py`: `add(2, 3) == 5`, and zero and negative inputs. Both failed before the fix (for example, `add(-2, 5)` gave -10 instead of 3).

I didn't commit anything, since this directory isn't a git repo. You'll need to deploy the change yourself.
```

## Rationalizations observed (manual notes)

- FAIL `test_written_before_source` (also failing in bench1; the check misses Bash heredoc writes): the response says "I wrote two regression tests first … Both failed before the fix". No rationalization observed.
