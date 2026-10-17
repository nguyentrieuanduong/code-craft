# Inventory: skills/executing-plans/SKILL.md

Base: `main` at 29a1c4e

| # | Original | Outcome | Items |
|---|---|---|---|
| R1 | "Execute the approved plan exactly." | "Execute the approved plan exactly. The plan is the single source of truth; your job is mechanical, disciplined execution — not improvisation." | |
| R2 | "The plan is the single source of truth; your job is mechanical, disciplined execution — not improvisation." | merged into R1 | |
| R3 | "- Read the plan file. Find the first unchecked `[ ]` step." | "- Read the plan file. Find the first unchecked `[ ]` step. That is your next action — always." | |
| R4 | "That is your next action — always." | merged into R3 | |
| R5 | "This makes work resumable after any interruption or session restart." | cut: non-normative (rule 6) | |
| R6 | "- If all steps are checked, invoke **verification-before-completion**, then **code-review**." | "- If all steps are checked, invoke **verification-before-completion**, then **code-review**." | |
| R7 | "- Do exactly what the step says: the file it names, the code it contains, the command it specifies." | "- Do exactly what the step says: the file it names, the code it contains, the command it specifies." | |
| R8 | "- Production code follows **test-driven-development**, **coding-standards**, and **security-baseline** at all times." | "- Production code follows **test-driven-development**, **coding-standards**, and **security-baseline** at all times." | |
| R9 | "- Verify the target path: workspace source tree, never the .plans directory." | "- Verify the target path: workspace source tree, never the .plans directory." | |
| R10 | "- Brownfield: modify the existing file in place. Creating `X_modified` or `X_new` copies is forbidden." | "- Brownfield: modify the existing file in place. Creating `X_modified` or `X_new` copies is forbidden." | |
| R11 | "- On completion, flip `[ ]` to `[x]` in the plan file immediately — not in batches at the end." | "- On completion, flip `[ ]` to `[x]` in the plan file immediately — not in batches at the end; context can vanish any time." | |
| R12 | "- Commit when the step says to commit." | "- Commit when the step says to commit. Small commits are the recovery map: if context is lost, `git log` + plan checkboxes reconstruct the state." | |
| R13 | "Small commits are the recovery map: if context is lost, `git log` + plan checkboxes reconstruct the state." | merged into R12 | |
| R14 | "### 4. Repeat" / "One step at a time until the task's steps are done, then move to the next task." | "### 3. Record progress, then repeat" / "- One step at a time until the task's steps are done, then move to the next task." | |
| R15 | "Stop executing and report when:" | "Stop executing and report when:" | |
| R16 | "1. **The plan is wrong.** A step conflicts with reality (file doesn't exist, API differs, test can't be written as specified). Do not silently adapt — propose a plan amendment and get approval." | "1. **The plan is wrong.** A step conflicts with reality (file doesn't exist, API differs, test can't be written as specified). Do not silently adapt — propose a plan amendment and get approval." | |
| R17 | "2. **A test fails unexpectedly** (not the planned RED). Invoke **systematic-debugging**. Never comment out, skip, or weaken a test to proceed." | "2. **A test fails unexpectedly** (not the planned RED). Invoke **systematic-debugging**. Never comment out, skip, or weaken a test to proceed — a skipped test is a lie in the codebase." | |
| R18 | "3. **Scope appears mid-flight.** Something needed is missing from the plan. Add it to the plan as a new task, get approval, then continue." | "3. **Scope appears mid-flight.** Something needed is missing from the plan. Add it to the plan as a new task, get approval, then continue." | |
| R19 | "4. **Three consecutive failures** on the same step. Question the approach before attempt four." | "4. **Three consecutive failures** on the same step. Question the approach before attempt four." | |
| R20 | "&#124; \"While I'm here, I'll also improve...\" &#124; Scope creep. The plan defines the work. File it as a follow-up. &#124;" | "&#124; \"While I'm here, I'll also improve...\" &#124; Scope creep. The plan defines the work. File it as a follow-up. &#124;" | |
| R21 | "&#124; \"This step is close enough, I'll adapt\" &#124; Silent adaptation breaks traceability. Amend the plan explicitly. &#124;" | "&#124; \"This step is close enough, I'll adapt\" &#124; Silent adaptation breaks traceability. Amend the plan explicitly. &#124;" | |
| R22 | "&#124; \"I'll update the checkboxes at the end\" &#124; Context can vanish any time. State updates are immediate. &#124;" | merged into R11 | |
| R23 | "&#124; \"Skipping this failing test unblocks me\" &#124; A skipped test is a lie in the codebase. Debug it. &#124;" | merged into R17 | |

Counts (checker): 428 -> 394 words (7% cut), 51 -> 47 nonblank lines.
Reason: the four stop conditions, the brownfield rule, and the immediate-checkbox rule are kept whole by E4; the cuts are the folded "Repeat" step, two table rows that restated a step, and one motivation sentence (R5).
