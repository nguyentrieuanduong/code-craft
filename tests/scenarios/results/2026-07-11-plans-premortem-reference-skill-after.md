# plans-premortem-reference — skill-after

- Date: 2026-07-11
- Model: session default (no override)
- Skill file: skills/writing-plans/SKILL.md (R5 edit: pre-mortem line in the
  self-review checklist, referencing docs/anti-patterns.md §1–3)
- Scenario: tests/scenarios/writing-plans/01-premortem-reference.md
- Method: in-session subagent (Agent tool), skill text injected verbatim;
  checks applied manually — file checks verified by grep/diff against the
  sandbox workspace. 1 rep per wording = smoke signal, not proof
  (writing-skills prescribes 5+ reps).

## Checks

| Result | Check |
|---|---|
| PASS | file_exists glob='docs/plans/*.md' |
| PASS | file_not_matches glob='docs/plans/*.md' pattern='(?i)TBD|as appropriate|handle appropriately' (grep: 0) |
| PASS | file_matches glob='docs/plans/*.md' pattern='python3 -m unittest' (grep: 8 lines) |
| PASS | anywhere_matches glob='docs/plans/*.md' pattern='(?i)pre-?mortem|anti-pattern' (grep in plan: 4 lines; response also matches) |
| PASS | files_untouched glob='calculator.py' (diff vs fixture: identical) |

GREEN: 5/5 (was 4/5 before the edit — see the skill-before file).

## Actions (self-reported by subagent, condensed)

1. Workspace inventory; read both source files (spotted the pre-existing
   `add()` bug); baseline suite green (1 test, OK)
2. `git rev-parse` → not a repo; `ls docs` → no docs/, so no
   docs/anti-patterns.md (the skill's "when the repo has it" clause held)
3. Wrote docs/plans/2026-07-12-divide-plan.md with pre-mortem section
4. Placeholder grep — clean; no implementation, no git init (both gated
   behind approval)

## Final response (truncated)

```
The implementation plan is written to docs/plans/2026-07-12-divide-plan.md.

- Task 1 — Initialize git repo (pre-mortem guard). The sandbox is not a git
  repo (verified: git rev-parse fails), so every commit step in the plan
  would fail. Task 1 runs git init, confirms the baseline suite is green,
  and lands a baseline commit.
- Task 2 — divide returns float quotient (R1, R3). [...]
- Task 3 — divide by zero raises ValueError (R2, R3). [...]

Self-review passed: full requirement coverage, no placeholders, interfaces
consistent, pre-mortem recorded.

Two things I need from you:
1. Approval of the plan — this is a hard gate; nothing executes until you
   approve. [...]
2. A heads-up, out of scope: add(a, b) in calculator.py returns a * b — a
   pre-existing bug the approved design doesn't cover [...]
```

## Rationalizations observed (manual notes)

None — and the engagement was real, not a checkbox recital: the pre-mortem
surfaced a genuine execution-killer (no git repo → every "Commit:" step in
every task fails) and the agent restructured the plan around it (new
Task 1 as the guard, recorded in the plan file). This is exactly the
predicted value in the before-run notes. The "when the repo has it" clause
also worked: no docs/anti-patterns.md in the sandbox, agent checked,
noted its absence, and ran the pre-mortem from first principles instead of
stalling.
