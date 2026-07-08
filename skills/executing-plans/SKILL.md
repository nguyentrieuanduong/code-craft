---
name: executing-plans
description: >-
  Use after a plan is approved to implement it step by step. Enforces exact
  plan-driven execution, checkbox state tracking for resumability, and stop
  conditions when reality diverges from the plan. Don't use without an approved
  plan file.
---

# Executing Plans

Execute the approved plan exactly. The plan is the single source of truth;
your job is mechanical, disciplined execution — not improvisation.

## Process

### 1. Load state

- Read the plan file. Find the first unchecked `[ ]` step. That is your next
  action — always. This makes work resumable after any interruption or
  session restart.
- If all steps are checked, invoke **verification-before-completion**, then
  **code-review**.

### 2. Execute one step

- Do exactly what the step says: the file it names, the code it contains,
  the command it specifies.
- Production code follows **test-driven-development**, **coding-standards**,
  and **security-baseline** at all times.
- Verify the target path: workspace source tree, never the docs/plans directory.
- Brownfield: modify the existing file in place. Creating `X_modified` or
  `X_new` copies is forbidden.

### 3. Record progress

- On completion, flip `[ ]` to `[x]` in the plan file immediately — not in
  batches at the end.
- Commit when the step says to commit. Small commits are the recovery map:
  if context is lost, `git log` + plan checkboxes reconstruct the state.

### 4. Repeat

One step at a time until the task's steps are done, then move to the next task.

## Stop conditions — halt and consult the user

Stop executing and report when:

1. **The plan is wrong.** A step conflicts with reality (file doesn't exist,
   API differs, test can't be written as specified). Do not silently adapt —
   propose a plan amendment and get approval.
2. **A test fails unexpectedly** (not the planned RED). Invoke
   **systematic-debugging**. Never comment out, skip, or weaken a test to
   proceed.
3. **Scope appears mid-flight.** Something needed is missing from the plan.
   Add it to the plan as a new task, get approval, then continue.
4. **Three consecutive failures** on the same step. Question the approach
   before attempt four.

## Forbidden rationalizations

| Excuse | Reality |
|--------|---------|
| "While I'm here, I'll also improve..." | Scope creep. The plan defines the work. File it as a follow-up. |
| "This step is close enough, I'll adapt" | Silent adaptation breaks traceability. Amend the plan explicitly. |
| "I'll update the checkboxes at the end" | Context can vanish any time. State updates are immediate. |
| "Skipping this failing test unblocks me" | A skipped test is a lie in the codebase. Debug it. |
