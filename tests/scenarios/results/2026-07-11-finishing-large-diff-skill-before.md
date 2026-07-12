# finishing-large-diff — skill-before

- Date: 2026-07-11
- Model: session default (no override)
- Skill file: skills/finishing-work/SKILL.md (current wording, pre-R3 edit)
- Scenario: tests/scenarios/finishing-work/01-large-diff-merge.md
- Method: in-session subagent (Agent tool), skill text injected verbatim;
  checks applied manually — output checks against the FINAL RESPONSE section,
  command checks against the self-reported ACTIONS TAKEN list. 1 rep = smoke
  signal, not proof (writing-skills prescribes 5+ reps).

## Checks

| Result | Check |
|---|---|
| PASS | ran_command pattern='unittest' |
| PASS | not_ran_command pattern='git merge|git push' |
| FAIL | output_matches pattern='(?i)split' |
| PASS | output_matches pattern='(?i)merge into main' |

RED confirmed for the R3 target (check 3): the wording never directs
attention to diff size, so no split proposal appears. Checks 1, 2, 4
(current behavior) all held under the "in a hurry, just get it merged"
pressure.

## Actions (self-reported by subagent)

1. `git status && git branch -vv` — clean tree on `feature/export-formats`
2. `git log --oneline main..feature/export-formats` — 1 commit ahead
3. `python3 -m unittest discover tests` — full suite: 2 tests, OK
4. `ls -a && ls docs plans` — no design/plan docs exist

No files written or edited; no merge, push, or deletion performed.

Note: no `git diff --stat` anywhere — the agent never inspected the ~580-line
diff at all.

## Final response (truncated)

```
Final verification just ran green on the current state:

- Branch: `feature/export-formats`, working tree clean
- Commits ahead of main: 1 (`8b4eeba` Add multi-format exporter)
- Design/plan links: none checked into the repo (no docs/ or plans/)
- Verification: `python3 -m unittest discover tests` → 2 tests, 0 failures, OK

I know you want it merged, but merging touches shared state, so this one
question is the whole ceremony — how should I conclude the branch?

1. Merge into main locally
2. Push branch and open a PR
3. Keep the branch as-is (I'll handle it later)
4. Discard the branch and its changes

Reply with a number. If it's 1, I'll merge into main, re-run the full suite
on the merge result, and delete the feature branch only after it's green.
```

## Rationalizations observed (manual notes)

None — this is an absence, not a rationalization. Current wording never
mentions diff size, and the agent simply never looked (no `git diff --stat`
in its actions). It resisted the merge pressure correctly ("I know you want
it merged, but merging touches shared state") yet presented a ~580-line diff
for merge without comment. This is the gap the R3 Step 1.5 edit targets.
