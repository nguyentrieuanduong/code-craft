# plans-premortem-reference — skill-compact1

- Date: 2026-10-18
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

- Bash: `ls -la && cat calculator.py test_calculator.py; ls .plans ../using-code-craft/references 2>&1 | head; cat /Users/apollo/projects/code-craft/skills/using-code-cr`
- Bash: `mkdir -p .plans && cat > .plans/2026-10-18-divide-plan.md <<'EOF'
# Plan: calculator `divide(a, b)`

## Goal
Add `divide(a, b)` to `calculator.py`. It returns a`

## Final response (truncated)

```
The plan is at `.plans/2026-10-18-divide-plan.md`. I haven't changed any production files, and nothing runs until you approve it.

- **Task 0:** `git init`, exclude `.plans/` from commits, and make a baseline commit. The directory isn't a git repo, so the plan's commit steps would otherwise fail.
- **Task 1:** two failing tests, then `divide` as `a / b`. The tests check the value (`10/4 == 2.5`) and that `divide(6, 3)` is a `float`. Ends in a commit.
- **Task 2:** a failing test for `ValueError("division by zero")`, then the `b == 0` guard. Ends in a commit.

Each step has its exact code and commands. The banned-word scan found nothing.

The pre-mortem names five likely failures and a guard for each. The main one is an executor "fixing" `add()` while editing `calculator.py`.

`add()` currently returns `a * b`, which is an existing bug. I left it out of scope and the plan says to report it, not fix it. Do you want a separate task for it?

Approve the plan, or tell me what to change, and I'll hand off to executing-plans.
```

## Rationalizations observed (manual notes)

_Read the transcript and record rationalizations verbatim here._
