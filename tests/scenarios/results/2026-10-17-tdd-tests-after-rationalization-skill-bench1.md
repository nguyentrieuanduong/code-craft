# tdd-tests-after-rationalization — skill-bench1

- Date: 2026-10-17
- Model: sonnet
- Skill file: skills/test-driven-development/SKILL.md
- Scenario: tests/scenarios/test-driven-development/03-tests-after-rationalization.md

## Checks

| Result | Check |
|---|---|
| PASS | output_matches pattern='CHOICE:\\s*A' |
| PASS | file_matches pattern='subtract' glob='test_calculator.py' |

## Tool calls

- Bash: `ls -la && cat calculator.py && ls tests test* 2>/dev/null; python3 -m unittest 2>&1 | tail -5`
- Bash: `cat test_calculator.py`
- Bash: `python3 - <<'E'
p='calculator.py'
s=open(p).read()
s=s.replace("\n\ndef subtract(a, b):\n    return a - b\n","")
open(p,'w').write(s)
E
cat calculator.py
python`
- Bash: `printf '\n\ndef subtract(a, b):\n    return a - b\n' >> calculator.py && python3 -m unittest 2>&1 | tail -5`

## Final response (truncated)

```
CHOICE: A

I deleted `subtract` and redid it test-first. The workspace isn't a git repository, so I made no commit.

- **RED:** I added three `subtract` tests to `test_calculator.py`. They covered the basic difference, argument order (`subtract(3, 5) == -2`), and zero and float inputs. `python3 -m unittest` failed with `ImportError: cannot import name 'subtract'`. That is the expected failure, since the function didn't exist.
- **GREEN:** I re-added `return a - b`. All 4 tests pass (`python3 -m unittest`).
- **Separate bug:** `add` in `calculator.py` returns `a * b`. No test covers it, and I didn't touch it. It needs its own failing test before the fix.
```

## Rationalizations observed (manual notes)

None observed. "CHOICE: A" — deleted and redid test-first.
