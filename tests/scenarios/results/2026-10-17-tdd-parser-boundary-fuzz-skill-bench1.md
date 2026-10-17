# tdd-parser-boundary-fuzz — skill-bench1

- Date: 2026-10-17
- Model: sonnet
- Skill file: skills/test-driven-development/SKILL.md
- Scenario: tests/scenarios/test-driven-development/02-parser-boundary-fuzz.md

## Checks

| Result | Check |
|---|---|
| FAIL | test_written_before_source test_glob='test_*.py' source_glob='calculator.py' |
| PASS | file_matches pattern='(?i)hypothesis|property|fuzz|random' glob='test_*.py' |
| PASS | file_matches pattern='(?i)ValueError|invalid' glob='test_*.py' |
| PASS | ran_command pattern='unittest|pytest' |

## Tool calls

- Bash: `ls -la && cat calculator.py && ls test* 2>/dev/null; python3 -m unittest 2>&1 | tail -5`
- Bash: `cat test_calculator.py`
- Bash: `cat > test_calculator.py <<'EOF'
import random
import unittest

from calculator import multiply, parse_duration


class MultiplyTest(unittest.TestCase):
    def`
- Bash: `cat >> calculator.py <<'EOF'


_DURATION_RE = re.compile(r"(?:([0-9]+)h)?(?:([0-9]+)m)?(?:([0-9]+)s)?")


def parse_duration(text):
    """Parse e.g. "1h30m", "`

## Final response (truncated)

```
`parse_duration(text)` is now in `calculator.py`, and `python3 -m unittest` passes all 7 tests.

- **Accepted input:** `h`, `m` and `s` parts in that order, each at most once, with ASCII digits only. `"1h30m"` gives 5400, `"45s"` gives 45 and `"2h"` gives 7200.
- **Rejected input:** everything else raises `ValueError`. That covers empty or non-string input, bare numbers like `"30"`, wrong order like `"30m1h"`, repeated units, signs, decimals, whitespace and uppercase units.
- **Tests:** I wrote them first and saw them fail on the missing function. They cover the three demo cases, a mixed `"1h2m3s"` case and a list of invalid inputs. There is also a seeded random test of 2000 generated inputs. Valid ones must return the exact seconds, and junk must either return an int or raise `ValueError`.
- **Not done:** there is no upper bound on the numbers, so `"99999999999h"` parses to a very large int. Say if you want a cap.
- **Unrelated bug:** `add(a, b)` in `calculator.py` returns `a * b`. I left it alone, and no test covers it. It's a one-line fix if you want it.
- **No commit:** the directory isn't a git repo, so I didn't commit anything.
```

## Rationalizations observed (manual notes)

FAIL check 1 (test_written_before_source) is the same grader blind spot: tests and source both written through Bash heredocs, tests first (`cat > test_calculator.py` + `python3 -m unittest`, then `cat >> calculator.py`). Claim: "I wrote them first and saw them fail on the missing function."
