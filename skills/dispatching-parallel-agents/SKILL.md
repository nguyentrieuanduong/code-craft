---
name: dispatching-parallel-agents
description: >-
  Use when an approved plan contains 2 or more INDEPENDENT tasks that share no
  files and no state, and the harness supports subagents. Don't use for
  dependent tasks, or on harnesses without subagents (execute inline instead).
---

# Dispatching Parallel Agents

You are the orchestrator: you own the plan, dispatch fresh subagents for
independent tasks, review their output, and never let unreviewed work pile up.

## The independence test (all three, or run sequentially)

1. **No shared files** — two agents editing one file will overwrite each other.
2. **No data dependency** — task B never consumes task A's output.
3. **No ordering requirement** — either could land first and the build stays green.

Interface boundaries count as dependencies: if task B imports what task A
defines, B waits for A. When in doubt, sequential — a wrong parallel guess
costs more than the time saved.

## Dispatching

- **One task per subagent, fresh context.** Never reuse an agent across tasks;
  leftover context from task 1 pollutes task 2.
- **The brief is self-contained.** The subagent has read nothing: include the
  goal, exact file paths, the plan step's code blocks, the test command, the
  constraints (TDD, coding-standards, security-baseline apply), and the report
  format below. If the brief needs "as discussed above", it is not ready.
- **Pick the model tier per task** (`references/model-routing.md`): cheap for
  mechanical steps with exact code blocks, standard for integration, capable
  for anything ambiguous. Always specify the model explicitly.
- Dispatch all independent tasks in one batch, then wait.

## Subagent contract

Each subagent implements, tests (TDD), commits, self-reviews, and reports:

```
STATUS: DONE | DONE_WITH_CONCERNS | NEEDS_CONTEXT | BLOCKED
Task: <name>  Commits: <hashes>
Verification: <exact command run + result counts>
Concerns: <anything the orchestrator must review>
```

## Review between waves — never skip

A subagent's report describes what it intended, not what it did. For each
completed task, before dispatching the next wave:

1. Read the actual diff (`git show <commits>`) — not just the report.
2. Check spec compliance against the plan step, then code quality
   (coding-standards, security-baseline).
3. Run the full suite — parallel work merges can break what each task
   passed alone.
4. Failures → dispatch a fix subagent with the review findings; re-review.
   Mark the plan checkbox only after review passes.

## Forbidden rationalizations

| Excuse | Reality |
|--------|---------|
| "Tasks look independent, close enough" | "Close enough" means a merge conflict or broken interface later. Apply the three-part test. |
| "The subagent said DONE, moving on" | Reports are claims. The diff and a fresh test run are evidence. |
| "Parallelize everything, it's faster" | Dependent tasks done in parallel are done twice. Only genuine independence wins time. |
| "I'll review all tasks at the end" | Ten unreviewed tasks compound errors. Review each wave before the next. |
