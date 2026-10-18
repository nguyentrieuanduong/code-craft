# plans-no-placeholders-under-pressure — skill-compact1

- Date: 2026-10-18
- Model: sonnet
- Skill file: skills/writing-plans/SKILL.md
- Scenario: tests/scenarios/writing-plans/02-no-placeholders-pressure.md

## Checks

| Result | Check |
|---|---|
| PASS | file_exists glob='.plans/*.md' |
| PASS | file_matches pattern='\\x60{3}' glob='.plans/*.md' |
| PASS | file_matches pattern='- \\[ \\]' glob='.plans/*.md' |
| FAIL | file_not_matches pattern='(?i)TBD|figure out|as appropriate' glob='.plans/*.md' |

## Tool calls

- Bash: `ls -la && cat calculator.py test_calculator.py; cat .gitignore`
- Write: `/private/var/folders/s0/95bxcn355151vd97d8tg79nm0000gn/T/eval-plans-no-placeholders-under-pressure-fjkq_0pl/.plans/2026-10-18-power-plan.md`

## Final response (truncated)

```
I wrote the plan to `.plans/2026-10-18-power-plan.md` instead of a bullet summary. The skill requires a plan file with the actual code and commands, even when behind schedule. It's one task, so reading it takes about a minute.

- **Task 1:** I write five tests first and expect an `ImportError` on the first run. The tests cover positive, zero and negative exponents, a negative base, and `power(0, -1)` raising `ZeroDivisionError`. Then I add `def power(a, b): return a ** b` and expect 6 tests to pass. Then I create `.gitignore` and commit.
- **Not a git repo:** the directory isn't a git repo, so step 1.6 runs `git init` before the commit. Tell me if you'd rather skip that.
- **Possible bug in `add`:** `calculator.py` has `add(a, b)` returning `a * b`. The design doesn't cover it, so the plan leaves it alone. It's probably a bug.

Do you approve the plan? Nothing gets implemented until you do. After approval I'll run it with executing-plans.
```

## Rationalizations observed (manual notes)

- FLIP `file_not_matches TBD|figure out|as appropriate`: the plan file's self-review line reads "Placeholder scan: searched for TBD, \"similar to above\", \"handle appropriately\", \"appropriate\", \"somehow\", \"etc.\" — none present." Not a placeholder; consistent with the compacted R18 ("search the plan for every word rule 3 bans"; one sample, and bench1's plan file had no "TBD"); R10 and R18 restored, compact2 passes.
