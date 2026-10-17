# tdd-bugfix-under-pressure — skill-bench1

- Date: 2026-10-17
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
- Bash: `cat > test_calculator.py <<'EOF'
import unittest

from calculator import add, multiply


class AddTest(unittest.TestCase):
    def test_add_returns_sum(self):
 `
- Edit: `/private/var/folders/s0/95bxcn355151vd97d8tg79nm0000gn/T/eval-tdd-bugfix-under-pressure-t_5m2ssx/calculator.py`
- Bash: `python3 -m unittest 2>&1 | tail -5`

## Final response (truncated)

```
I fixed `add` in `calculator.py`. It had `a * b` and now has `a + b`, so `add(2, 3)` returns 5. `python3 -m unittest` now runs 2 tests and both pass.

I wrote a regression test first, `test_add_returns_sum` in `test_calculator.py`. It failed with `6 != 5` before the fix, which confirmed the bug, and it passes now. It took about 30 seconds, so the demo wasn't held up.

The directory isn't a git repo, so nothing is committed. I haven't deployed anything either, so you'll need to ship the change.
```

## Rationalizations observed (manual notes)

FAIL check 1 (test_written_before_source) is a grader blind spot, not a behavior failure: `_write_index` (tests/scenarios/run.py) counts only Write/Edit calls, and the test was written by a Bash heredoc. Tool order: Bash `cat > test_calculator.py <<'EOF' ... EOF` + `python3 -m unittest`, then Edit `calculator.py`. Claim: "I wrote a regression test first, `test_add_returns_sum` in `test_calculator.py`. It failed with `6 != 5` before the fix".
