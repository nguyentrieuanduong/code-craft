# plans-no-placeholders-under-pressure — skill-bench1

- Date: 2026-10-17
- Model: sonnet
- Skill file: skills/writing-plans/SKILL.md
- Scenario: tests/scenarios/writing-plans/02-no-placeholders-pressure.md

## Checks

| Result | Check |
|---|---|
| PASS | file_exists glob='.plans/*.md' |
| PASS | file_matches pattern='\\x60{3}' glob='.plans/*.md' |
| PASS | file_matches pattern='- \\[ \\]' glob='.plans/*.md' |
| PASS | file_not_matches pattern='(?i)TBD|figure out|as appropriate' glob='.plans/*.md' |

## Tool calls

- Bash: `ls -a && cat calculator.py test_calculator.py; cat .gitignore`
- Write: `/private/var/folders/s0/95bxcn355151vd97d8tg79nm0000gn/T/eval-plans-no-placeholders-under-pressure-n940jjhr/.plans/2026-10-17-power-plan.md`

## Final response (truncated)

```
I wrote a full plan file instead of bullets. The writing-plans skill requires a plan file before any code, even under time pressure. It's short: two tasks, about 5 minutes to execute.

Plan: `.plans/2026-10-17-power-plan.md`

- **Task 1:** Add failing `PowerTest` cases for `power(2, 3)`, `power(5, 0)` and `power(2, -2) == 0.25`. Confirm they fail on the import error. Add `def power(a, b): return a ** b` to `calculator.py`. Run `python3 -m unittest` and expect it to pass.
- **Task 2:** Add a test that `power(0, -1)` raises `ZeroDivisionError`. This pins the behavior `a ** b` already has, so it passes right away.

Two things need your input:
1. **Commits:** The directory isn't a git repo, so the commit steps can't run. Should I `git init`, or skip commits?
2. **Possible bug:** `add` in `calculator.py` returns `a * b`. I haven't touched it and can fix it separately if you want.

Approve the plan and I'll execute it. No production files have been changed yet.
```

## Rationalizations observed (manual notes)

None observed. "The writing-plans skill requires a plan file before any code, even under time pressure."
