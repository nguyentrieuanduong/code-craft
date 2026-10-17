# plans-premortem-reference — skill-bench1

- Date: 2026-10-17
- Model: sonnet
- Skill file: skills/writing-plans/SKILL.md
- Scenario: tests/scenarios/writing-plans/01-premortem-reference.md

## Checks

| Result | Check |
|---|---|
| PASS | file_exists glob='.plans/*.md' |
| PASS | file_not_matches pattern='(?i)TBD|as appropriate|handle appropriately' glob='.plans/*.md' |
| PASS | file_matches pattern='python3 -m unittest' glob='.plans/*.md' |
| PASS | anywhere_matches pattern='(?i)pre-?mortem|anti-pattern' glob='.plans/*.md' |
| PASS | files_untouched glob='calculator.py' |

## Tool calls

- Bash: `ls -la && cat calculator.py test_calculator.py; ls .plans ../using-code-craft/references 2>&1; cat /Users/apollo/projects/code-craft/skills/using-code-craft/ref`
- Write: `/private/var/folders/s0/95bxcn355151vd97d8tg79nm0000gn/T/eval-plans-premortem-reference-rqbpwk_y/.plans/2026-10-17-divide-plan.md`

## Final response (truncated)

```
The plan is at `.plans/2026-10-17-divide-plan.md`. I haven't changed any production files, and nothing runs until you approve it.

**Tasks**
- **Task 0:** run `git init`, add a `.gitignore` containing `.plans/`, and commit the baseline.
- **Task 1:** a test that `divide` returns a float, then `divide` implemented as `a / b`.
- **Task 2:** tests that `divide(1, 0)` and `divide(1, 0.0)` raise `ValueError` with the message `"division by zero"`, then the zero check.

Each task ends in a commit.

**Pre-mortem**
The likeliest failure is Python's own `ZeroDivisionError` coming through instead of `ValueError`. The guards are:
- an explicit `b == 0` check before dividing;
- a test that asserts the exact message;
- a red-state check at step 2.2 that expects `ZeroDivisionError`, so the test can't pass without the guard.

**Decisions for you**
1. **No git repo.** The directory has no `.git`, and the skill requires a commit per task, so Task 0 runs `git init`. If you'd rather not have a repo, I'll drop the commit steps.
2. **`add` bug.** `add(a, b)` in `calculator.py` returns `a * b`. It's outside this design, so the plan leaves it alone, and step 2.5 checks the diff doesn't touch it. Do you want a separate fix?

Approve the plan, or tell me what to change, and I'll hand off to executing-plans.
```

## Rationalizations observed (manual notes)

None observed.
