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
If anything fails, stop — back to systematic-debugging. A branch does not get
presented for conclusion with failing tests.

## Step 2 — Report state

Summarize in a few lines: branch name, commits ahead of main, design/plan
links, verification evidence (numbers).

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
| "The branch is stale, I'll clean it up" | Unfamiliar branches may hold someone's in-progress work. Never delete unasked. |
