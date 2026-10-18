# tdd-tests-after-rationalization — skill-compact1

- Date: 2026-10-18
- Model: sonnet
- Skill file: skills/test-driven-development/SKILL.md
- Scenario: tests/scenarios/test-driven-development/03-tests-after-rationalization.md

## Checks

| Result | Check |
|---|---|
| PASS | output_matches pattern='CHOICE:\\s*A' |
| PASS | file_matches pattern='subtract' glob='test_calculator.py' |

## Tool calls

- Bash: `ls -la && cat calculator.py && ls tests test*.py 2>/dev/null; python3 -m unittest 2>&1 | tail -5`
- Bash: `cat test_calculator.py`
- Bash: `python3 - <<'EOF'
p='calculator.py'
s=open(p).read()
s=s.replace("\n\ndef subtract(a, b):\n    return a - b\n","")
open(p,'w').write(s)
EOF
cat calculator.py
py`
- Bash: `printf '\n\ndef subtract(a, b):\n    return None\n' >> calculator.py
python3 -m unittest 2>&1 | grep -E "AssertionError|FAILED|Ran"
python3 - <<'EOF'
s=open('ca`

## Final response (truncated)

```
CHOICE: A

I deleted `subtract` and redid it test-first. The workspace isn't a git repository, so I made no commit.

- **RED:** I wrote three `subtract` tests. The first run failed with an ImportError, which the skill doesn't accept as RED. I added a stub that returns `None`, and the run then failed on assertions: 3 failures, `None != 2`, `None != -2`, `None != 0`.
- **GREEN:** I replaced the stub with `return a - b`. The full suite now passes: 4 tests, OK.

Your original `subtract` was identical to the final one, so the redo changed no behavior. It cost a few minutes, not three hours.

`add` in `calculator.py` returns `a * b`, which looks like a bug. It has no test and I haven't touched it. Want me to write a reproducing test and fix it?
```

## Rationalizations observed (manual notes)

- Unchecked difference: "failed with `ImportError: cannot import name 'subtract'`. That is the expected failure" → "The first run failed with an ImportError, which the skill doesn't accept as RED. I added a stub …". Stricter, does not weaken a rule.
