---
name: finishing-work
description: >-
  Use when all plan tasks are complete, verification passed, and review is
  done — the branch is ready to conclude.
---

# Finishing Work

Concluding the work is a decision that belongs to the user.

## Step 1 — Final verification

Run the FULL test suite one last time on the final state (not a partial run,
not from memory of an earlier pass).

If anything fails, the conclusion process ENDS here: report the failure with
the test output, hand off to systematic-debugging, and skip Steps 2–3
entirely — no state report, no options menu. Do NOT fix the failure inline,
however small (even one line): a conclusion-time patch skips the design,
plan, TDD, and review gates every other change on the branch went through. A
branch does not get presented for conclusion with failing tests — and "fixed
just now, unreviewed" is failing.

## Step 1.5 — Diff-size check

Run `git diff --stat main...HEAD`. If changed lines exceed ~400, flag it in
the report and recommend splitting into independently reviewable slices
before merging — reviewer defect detection collapses past that size (see
`../using-code-craft/references/evidence.md`). Still present the Step 3
options; the split is a
recommendation, the choice stays with the user. At or under the threshold
the check is silent: report the size in Step 2, but say nothing about
thresholds or splitting.

## Step 2 — Report state

Summarize in a few lines: branch name, commits ahead of main, diff size
(files / lines changed), risk tier from the code review (standard /
high), design/plan links, verification evidence (numbers).

## Step 3 — Present exactly four options

```
1. Merge into main locally
2. Push branch and open a PR
3. Keep the branch as-is (I'll handle it later)
4. Discard the branch and its changes
```

Do not pre-select, even when merging seems obvious — merges touch shared
state. Do not merge, push, or delete anything before the user answers.

## Executing the choice

**Option 1 — merge locally**
- **High risk:** do not merge until a human has reviewed the current
  diff (name the HEAD commit) and recorded a decision in this
  conversation. Approval of the design or the plan, or the user picking
  this option, is not that review. Say what is needed and stop.
- Merge into main, run the full suite ON THE MERGE RESULT, verify green.
- Only then delete the feature branch (and its worktree if one was used).

**Option 2 — push + PR**
- `git push -u origin <branch>`, create the PR with sections
  **Summary**, **Testing** (commands run and their results), **Risk**
  (tier and why), and **How to revert**.
- **High risk:** state "Human review required before merge" in the PR
  body; never describe the PR as merge-ready before that review.
- Keep the local branch/worktree intact.

**Option 3 — keep as-is**
- Do nothing. State where the branch lives and how to resume.

**Option 4 — discard**
- Destructive and irreversible. Require the user to type `discard` to
  confirm before deleting anything.
- Only force-delete branches/worktrees created for this work — never
  pre-existing ones.

A code change after a human review needs a renewed review before merge.

## Forbidden rationalizations

| Excuse | Reality |
|--------|---------|
| "The branch is stale, I'll clean it up" | Unfamiliar branches may hold someone's in-progress work. Never delete unasked. |
