---
name: finishing-work
description: >-
  Use when all plan tasks are complete, verification passed, and review is
  done — the branch is ready to conclude.
---

# Finishing Work

The work is done. Concluding it is a decision that belongs to the user.

## Step 1 — Final verification

Run the FULL test suite one last time (not a partial run, not from memory).

If anything fails, the conclusion process ENDS here: report the failure with
the test output, hand off to systematic-debugging, and skip Steps 2–3
entirely — no state report, no options menu. Do NOT fix the failure inline,
however small: a conclusion-time patch skips the design, plan, TDD, and
review gates every other change on the branch went through. A branch does
not get presented for conclusion with failing tests — and "fixed just now,
unreviewed" is failing.

## Step 1.5 — Diff-size check

Run `git diff --stat main...HEAD`. If changed lines exceed ~400, flag it in
the report and recommend splitting into independently reviewable slices
before merging — reviewer defect detection collapses past that size (see
docs/evidence.md). Still present the Step 3 options; the split is a
recommendation, the choice stays with the user. At or under the threshold
the check is silent: report the size in Step 2, but say nothing about
thresholds or splitting.

## Step 2 — Report state

Summarize in a few lines: branch name, commits ahead of main, diff size
(files / lines changed), design/plan links, verification evidence (numbers).

## Step 3 — Present exactly four options

```
1. Merge into main locally
2. Push branch and open a PR
3. Keep the branch as-is (I'll handle it later)
4. Discard the branch and its changes
```

Do not pre-select. Do not merge, push, or delete anything before the user
answers.

## Executing the choice

**Option 1 — merge locally**
- Merge into main, run the full suite ON THE MERGE RESULT, verify green.
- Only then delete the feature branch (and its worktree if one was used).

**Option 2 — push + PR**
- `git push -u origin <branch>`, create the PR with summary + test plan.
- Keep the local branch/worktree intact.

**Option 3 — keep as-is**
- Do nothing. State where the branch lives and how to resume.

**Option 4 — discard**
- Destructive and irreversible. Require the user to type `discard` to
  confirm before deleting anything.
- Only force-delete branches/worktrees created for this work — never
  pre-existing ones.

## Forbidden rationalizations

| Excuse | Reality |
|--------|---------|
| "Merging is obviously what they want" | Maybe — but merges touch shared state. Ask. |
| "Tests passed an hour ago" | The final run is on the final state. Run it again. |
| "It's a one-line fix, I'll just patch it here" | An unreviewed fix at conclusion time skips every quality gate the branch just passed. Route it through systematic-debugging like any other defect. |
| "The branch is stale, I'll clean it up" | Unfamiliar branches may hold someone's in-progress work. Never delete unasked. |
