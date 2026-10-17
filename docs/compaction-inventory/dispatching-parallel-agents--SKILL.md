# Inventory: skills/dispatching-parallel-agents/SKILL.md

Base: `main` at 29a1c4e

| # | Original | Outcome | Items |
|---|---|---|---|
| R1 | "You are the orchestrator: you own the plan, dispatch fresh subagents for independent tasks, review their output, and never let unreviewed work pile up." | "You are the orchestrator: you own the plan, dispatch fresh subagents for independent tasks, review their output, and never let unreviewed work pile up." | |
| R2 | "## The independence test (all three, or run sequentially)" | "## The independence test (all three, or run sequentially)" | |
| R3 | "1. **No shared files** — two agents editing one file will overwrite each other." | "1. **No shared files** — two agents editing one file will overwrite each other." | |
| R4 | "2. **No data dependency** — task B never consumes task A's output." | "2. **No data dependency** — task B never consumes task A's output." | |
| R5 | "3. **No ordering requirement** — either could land first and the build stays green." | "3. **No ordering requirement** — either could land first and the build stays green." | |
| R6 | "Interface boundaries count as dependencies: if task B imports what task A defines, B waits for A." | "Interface boundaries count as dependencies: if task B imports what task A defines, B waits for A." | |
| R7 | "When in doubt, sequential — a wrong parallel guess costs more than the time saved." | "When in doubt — \"close enough\" included — sequential: a wrong parallel guess (a merge conflict or broken interface later) costs more than the time saved." | |
| R8 | "- **One task per subagent, fresh context.** Never reuse an agent across tasks; leftover context from task 1 pollutes task 2." | "- **One task per subagent, fresh context.** Never reuse an agent across tasks; leftover context from task 1 pollutes task 2." | |
| R9 | "- **The brief is self-contained.** The subagent has read nothing: include the goal, exact file paths, the plan step's code blocks, the test command, the constraints (TDD, coding-standards, security-baseline apply), and the report format below. If the brief needs \"as discussed above\", it is not ready." | "- **The brief is self-contained.** The subagent has read nothing: include the goal, exact file paths, the plan step's code blocks, the test command, the constraints (TDD, coding-standards, security-baseline apply), and the report format below. If the brief needs \"as discussed above\", it is not ready." | |
| R10 | "- **Pick the model tier per task** (`references/model-routing.md`): cheap for mechanical steps with exact code blocks, standard for integration, capable for anything ambiguous." | "- **Pick the model tier per task** (`references/model-routing.md`): cheap for mechanical steps with exact code blocks, standard for integration, capable for anything ambiguous." | |
| R11 | "Always specify the model explicitly." | "Always specify the model explicitly." | |
| R12 | "- Dispatch all independent tasks in one batch, then wait." | "- Dispatch all independent tasks in one batch, then wait." | |
| R13 | "Each subagent implements, tests (TDD), commits, self-reviews, and reports:" | "Each subagent implements, tests (TDD), commits, self-reviews, and reports:" | |
| R14 | STATUS fenced block (`STATUS: DONE &#124; DONE_WITH_CONCERNS &#124; NEEDS_CONTEXT &#124; BLOCKED` … `Concerns: …`) | "(same fenced block, byte for byte)" | |
| R15 | "## Review between waves — never skip" | "## Review between waves — never skip" | |
| R16 | "A subagent's report describes what it intended, not what it did." | "A subagent's report — even \"DONE\" — is a claim of what it intended, not evidence of what it did." | |
| R17 | "For each completed task, before dispatching the next wave:" | "For each completed task, before dispatching the next wave:" | |
| R18 | "1. Read the actual diff (`git show <commits>`) — not just the report." | "1. Read the actual diff (`git show <commits>`) — not just the report." | |
| R19 | "2. Check spec compliance against the plan step, then code quality (coding-standards, security-baseline)." | "2. Check spec compliance against the plan step, then code quality (coding-standards, security-baseline)." | |
| R20 | "3. Run the full suite — parallel work merges can break what each task passed alone." | "3. Run the full suite — parallel work merges can break what each task passed alone." | |
| R21 | "4. Failures → dispatch a fix subagent with the review findings; re-review. Mark the plan checkbox only after review passes." | "4. Failures → dispatch a fix subagent with the review findings; re-review. Mark the plan checkbox only after review passes." | |
| R22 | "&#124; \"Tasks look independent, close enough\" &#124; \"Close enough\" means a merge conflict or broken interface later. Apply the three-part test. &#124;" | merged into R7 | |
| R23 | "&#124; \"The subagent said DONE, moving on\" &#124; Reports are claims. The diff and a fresh test run are evidence. &#124;" | merged into R16 | |
| R24 | "&#124; \"Parallelize everything, it's faster\" &#124; Dependent tasks done in parallel are done twice. Only genuine independence wins time. &#124;" | "&#124; \"Parallelize everything, it's faster\" &#124; Dependent tasks done in parallel are done twice. Only genuine independence wins time. &#124;" | |
| R25 | "&#124; \"I'll review all tasks at the end\" &#124; Ten unreviewed tasks compound errors. Review each wave before the next. &#124;" | "&#124; \"I'll review all tasks at the end\" &#124; Ten unreviewed tasks compound errors. Review each wave before the next. &#124;" | |

Counts (checker): 479 -> 456 words (4% cut), 53 -> 53 nonblank lines.
Reason: each remaining sentence is a distinct rule (the three-part test, the brief contents, model routing, the STATUS block, the four review steps); the only restatements were the two table rows E6 names, now folded into R7 and R16.
