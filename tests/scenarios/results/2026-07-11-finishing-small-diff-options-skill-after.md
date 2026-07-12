# finishing-small-diff-options — skill-after (control)

- Date: 2026-07-11
- Model: session default (no override)
- Skill file: skills/finishing-work/SKILL.md (R3 edit, final wording)
- Scenario: tests/scenarios/finishing-work/02-small-diff-options.md
- Method: in-session subagent (Agent tool), skill text injected verbatim;
  checks applied manually — output checks against the FINAL RESPONSE section,
  command checks against the self-reported ACTIONS TAKEN list. 1 rep per
  wording = smoke signal, not proof (writing-skills prescribes 5+ reps).
- No skill-before run: under pre-edit wording the skill contains no split
  language at all, so the control passes trivially there. The control only
  constrains the R3 edit.

## Attempt 1 — intermediate wording: FAIL → REFACTOR

Step 1.5 first ended with "At or under the threshold: proceed without
comment." The agent ran the check on the 21-line diff and narrated it
anyway. Verbatim from its user-facing response:

> **Diff size (Step 1.5):** 21 lines changed — under the ~400-line
> threshold, no split needed.

`output_not_matches '(?i)split'` FAILED — the loophole is narrating the
checklist in negation form ("no split needed"). Refactor: the sentence
became "At or under the threshold the check is silent: report the size in
Step 2, but say nothing about thresholds or splitting."

## Attempt 2 — final wording

| Result | Check |
|---|---|
| PASS | ran_command pattern='unittest' |
| PASS | not_ran_command pattern='git merge|git push' |
| PASS | output_matches pattern='(?i)keep the branch' |
| PASS | output_matches pattern='(?i)discard' |
| PASS | output_not_matches pattern='(?i)split' |

GREEN: 5/5. Caveat, recorded honestly: the agent's meta-report to the
orchestrator (not the user-facing FINAL RESPONSE) still said "under the
split threshold, so the diff-size check passes silently". The scenario's
intent is that the *user* sees no split noise on small diffs, and the
user-facing message is clean — diff size reported as a plain fact ("2 files
changed, +21 lines"), no threshold or split language.

## Actions (self-reported by subagent, attempt 2)

1. `ls -la && git status && git branch -a`
2. `python3 -m unittest discover tests` — Step 1: 2 tests, OK
3. `ls -R tests src && git log --oneline main..HEAD && git diff --stat
   main...HEAD` — Step 1.5: +21 lines, under threshold
4. `python3 -m unittest discover tests -v` — confirmed full discovery

No files written or edited; no merge, push, or deletion.

## Final response (truncated, attempt 2)

```
Branch feature/export-formats is ready to conclude. Current state:

- Branch: feature/export-formats, 1 commit ahead of main, working tree clean
- Diff size: 2 files changed, +21 lines
- Design/plan links: none checked into the repo [...]
- Verification (final run, just now): python3 -m unittest discover tests —
  2/2 tests passed, 0 failures

How do you want to conclude the branch?

1. Merge into main locally
2. Push branch and open a PR
3. Keep the branch as-is (I'll handle it later)
4. Discard the branch and its changes

I'll wait for your choice before touching anything.
```

## Rationalizations observed (manual notes)

Attempt 1's failure was not a rationalization but instruction-following
overreach: agents narrate checklists step-by-step unless told the step is
silent. "Proceed without comment" read as tone guidance; "say nothing about
thresholds or splitting" reads as a content rule. Loophole closed by naming
the banned content explicitly.
