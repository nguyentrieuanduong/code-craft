# Inventory: skills/writing-plans/SKILL.md

Base: `main` at 29a1c4e

| # | Original | Outcome | Items |
|---|---|---|---|
| R1 | "Turn an approved design into a plan so explicit that a junior developer — or a smaller model — can execute it without making a single decision." | "Turn an approved design into a plan so explicit that a junior developer — or a smaller model — can execute it without making a single decision." | |
| R2 | "**HARD GATE: The plan must be approved by the user before any step executes. No production file changes before the plan file exists and the user has approved it.**" | "**HARD GATE: The plan must be approved by the user before any step executes. No production file changes before the plan file exists and the user has approved it.**" | |
| R3 | "The plan is a FILE, not a chat message: the first action of this skill is creating `.plans/YYYY-MM-DD-<topic>-plan.md`." | "The plan is a FILE, not a chat message: the first action of this skill is creating `.plans/YYYY-MM-DD-<topic>-plan.md`." | |
| R4 | "Time pressure never waives it — offering to \"skip the plan and just code\" is a skill violation, not an option to present." | merged into R28 | quote:skip the plan and just code |
| R5 | "`.plans/` is a gitignored working directory: plan files are never committed." | "`.plans/` is a gitignored working directory: plan files are never committed." | |
| R6 | "Save to `.plans/YYYY-MM-DD-<topic>-plan.md`:" | merged into R3 | |
| R7 | Plan structure fenced block (`# Plan: <topic>` … `- [ ] 1.5 Commit: \"<message>\"`) | "(same fenced block, byte for byte)" | |
| R8 | "1. **Map files first.** Every file gets one responsibility. Follow existing codebase patterns — check before inventing." | "1. **Map files first.** Every file gets one responsibility. Follow existing codebase patterns — check before inventing." | |
| R9 | "2. **Right-size tasks.** A task is the smallest unit that carries its own test cycle and can be reviewed independently. Each step takes 2–5 minutes." | "2. **Right-size tasks.** A task is the smallest unit that carries its own test cycle and can be reviewed independently. Each step takes 2–5 minutes." | |
| R10 | "3. **No placeholders.** \"TBD\", \"similar to above\", \"handle appropriately\", and \"etc.\" are banned." | "3. **No placeholders.** \"TBD\", \"similar to above\", \"handle appropriately\", \"appropriate\", \"somehow\", and \"etc.\" are banned." | |
| R11 | "Every step contains its actual content: fenced code blocks (``` … ```) with the real code, real commands, real names." | "Every step contains its actual content: fenced code blocks (``` … ```) with the real code, real commands, real names." | |
| R12 | "A plan whose steps describe code instead of containing it is placeholders by definition — if you could paste the step into an editor and run it, it's done; otherwise keep writing." | "A step that describes code instead of containing it is a placeholder — if you could paste it into an editor and run it, it's done; otherwise keep writing." | |
| R13 | "4. **Every task ends in a commit.** One task ≈ one small feature or 1–3 related functions." | "4. **Every task ends in a commit.** One task ≈ one small feature or 1–3 related functions." | |
| R14 | "Commit messages 5–20 words." | "Commit messages 5–20 words." | |
| R15 | "5. **Brownfield: modify in place.** List existing files to change by exact path. Never plan `Foo_new.py` or `Foo_v2.py` copies of existing files." | "5. **Brownfield: modify in place.** List existing files to change by exact path. Never plan `Foo_new.py` or `Foo_v2.py` copies of existing files." | |
| R16 | "6. **Story traceability.** Each task names the design requirement it satisfies, so nothing in the design is silently dropped." | "6. **Story traceability.** Each task names the design requirement it satisfies." | |
| R17 | "- [ ] Coverage scan: every design requirement maps to at least one task" | "- [ ] Coverage scan: every design requirement maps to at least one task" | |
| R18 | "- [ ] Placeholder scan: search the plan for \"TBD\", \"somehow\", \"appropriate\", \"etc.\"" | "- [ ] Placeholder scan: search the plan for every word rule 3 bans" | |
| R19 | "- [ ] Type/interface consistency: task N's outputs match task N+1's inputs" | "- [ ] Type/interface consistency: task N's outputs match task N+1's inputs" | |
| R20 | "- [ ] Every step has an exact command or code block" | "- [ ] Every step has an exact command or code block" | |
| R21 | "- [ ] Constraints section uses exact values, not descriptions of values" | "- [ ] Constraints section uses exact values, not descriptions of values" | |
| R22 | "- [ ] Pre-mortem: assume execution failed — name the likeliest failure and add its guard to the plan (check `../using-code-craft/references/anti-patterns.md` §1–3 for candidates when the repo has it); record the pre-mortem in the plan" | "- [ ] Pre-mortem: assume execution failed — name the likeliest failure and add its guard to the plan (check `../using-code-craft/references/anti-patterns.md` §1–3 for candidates when the repo has it); record the pre-mortem in the plan" | |
| R23 | "After approval, invoke **executing-plans**." | "After approval, invoke **executing-plans**." | |
| R24 | "The plan file is the single source of truth — execution updates its checkboxes, never improvises around it." | "The plan file is the single source of truth — execution updates its checkboxes, never improvises around it." | |
| R25 | "&#124; \"I'll figure out details during implementation\" &#124; Details deferred are decisions made under pressure. Decide now. &#124;" | "&#124; \"I'll figure out details during implementation\" &#124; Details deferred are decisions made under pressure. Decide now. &#124;" | |
| R26 | "&#124; \"The plan is obvious from the design\" &#124; Then it takes 5 minutes to write. Write it. &#124;" | "&#124; \"The plan is obvious from the design\" &#124; Then it takes 5 minutes to write. Write it. &#124;" | |
| R27 | "&#124; \"Code blocks in a plan are wasted effort\" &#124; They are the effort. Execution becomes mechanical, which is the point. &#124;" | "&#124; \"Code blocks in a plan are wasted effort\" &#124; They are the effort. Execution becomes mechanical, which is the point. &#124;" | |
| R28 | "&#124; \"The user is in a hurry — I'll offer to skip the plan\" &#124; The skill exists exactly for when pressure is high. A 5-minute plan file is the fast path; unplanned code is the slow one. &#124;" | "&#124; \"The user is in a hurry — I'll offer to skip the plan\" &#124; Time pressure never waives the plan file; offering to \"skip the plan and just code\" is a skill violation, not an option to present. A 5-minute plan file is the fast path; unplanned code is the slow one. &#124;" | |

Counts (checker): 657 -> 638 words (2% cut), 75 -> 71 nonblank lines.
Reason: the plan-structure block (kept byte for byte), the asserted pre-mortem link, and six numbered rules carry most of the words; the only restatements were the time-pressure sentence (moved into the R28 row), the second save path (R6), and the second banned-word list (R18).
