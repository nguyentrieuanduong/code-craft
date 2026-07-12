# plans-premortem-reference — skill-before

- Date: 2026-07-11
- Model: session default (no override)
- Skill file: skills/writing-plans/SKILL.md (current wording, pre-R5 edit)
- Scenario: tests/scenarios/writing-plans/01-premortem-reference.md
- Method: in-session subagent (Agent tool), skill text injected verbatim;
  checks applied manually — file checks verified by grep/diff against the
  sandbox workspace, command checks against the self-reported ACTIONS TAKEN
  list. 1 rep = smoke signal, not proof (writing-skills prescribes 5+ reps).

## Checks

| Result | Check |
|---|---|
| PASS | file_exists glob='docs/plans/*.md' |
| PASS | file_not_matches glob='docs/plans/*.md' pattern='(?i)TBD|as appropriate|handle appropriately' (grep: 0 matches) |
| PASS | file_matches glob='docs/plans/*.md' pattern='python3 -m unittest' (grep: 7 lines) |
| FAIL | anywhere_matches glob='docs/plans/*.md' pattern='(?i)pre-?mortem|anti-pattern' (grep: 0; response: no match) |
| PASS | files_untouched glob='calculator.py' (diff vs fixture: identical) |

RED confirmed for the R5 target (check 4): full compliant plan, every
self-review item narrated — and no pre-mortem anywhere, because the current
self-review checklist has no such item. Checks 1–3, 5 (current behavior)
held.

## Actions (self-reported by subagent)

1. `ls -la && find . -type f` — workspace inventory
2. `python3 -m unittest` — baseline suite check (1 test, OK)
3. `git rev-parse --is-inside-work-tree; git config user.name/email` — not a
   repo; identity configured
4. `mkdir -p docs/plans`
5. Wrote `docs/plans/2026-07-12-divide-plan.md` (the implementation plan)
6. `grep -n -i -E "TBD|somehow|appropriate|as needed| etc\b|placeholder"
   docs/plans/...` — placeholder self-review scan, clean

## Final response (truncated)

```
The implementation plan is written to docs/plans/2026-07-12-divide-plan.md.
Per the skill's hard gate, no plan step has been executed — calculator.py
and test_calculator.py are untouched, and nothing is implemented until you
approve.

What the plan contains:
- Task 0 — git init + baseline commit. [...]
- Task 1 — happy path, test-first. Failing test
  test_divide_returns_float_quotient [...] Full code blocks are in the plan.
- Task 2 — zero divisor, test-first. [...] exact message [...]
- Global constraints pin exact function/test names, the exact error message,
  and python3 -m unittest as the suite command [...]

Self-review per the skill, all passing: coverage scan (all four design
requirements map to Task 1/2), placeholder scan (mechanical grep for
TBD/somehow/appropriate/etc. came back clean), interface consistency,
and every step carries an exact command or code block.

One finding that needs your ruling: add(a, b) in calculator.py returns
a * b — a pre-existing bug. It is outside the approved design, so the plan
explicitly marks it out of scope [...]
```

## Rationalizations observed (manual notes)

None — an absence, not a rationalization. The agent executed every item the
self-review checklist contains and narrated each one; "assume this failed,
what did we miss" is simply not on the list, so it never happened. Notably
the agent DID independently surface the pre-existing `add()` bug (spec-scope
vigilance), which suggests a pre-mortem prompt would get real engagement
rather than a checkbox recital. This is the gap the R5 checklist line
targets.
