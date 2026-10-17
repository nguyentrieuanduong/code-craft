# Inventory: skills/brainstorming/SKILL.md

Base: `main` at 29a1c4e

| # | Original | Outcome | Items |
|---|---|---|---|
| R1 | "Turn a vague request into a design the user has explicitly approved." | "Turn a vague request into a design the user has explicitly approved." | |
| R2 | "**HARD GATE: You may not write production code, scaffold files, or \"just prototype\" until the user says the design is approved. There are no exceptions.**" | "**HARD GATE: You may not write production code, scaffold files, or \"just prototype\" until the user says the design is approved — prototypes anchor decisions and become production code. There are no exceptions.**" | |
| R3 | "### 1. Assess the request (silently, first)" | "### 1. Assess the request (silently, first)" | |
| R4 | "Classify before doing anything:" | merged into R3 | |
| R5 | "- **Clarity**: clear / vague / incomplete" | "- **Clarity**: clear / vague / incomplete" | |
| R6 | "- **Type**: new feature / enhancement / refactor / migration / new project" | "- **Type**: new feature / enhancement / refactor / migration / new project" | |
| R7 | "- **Scope**: single file / single module / cross-module / cross-system" | "- **Scope**: single file / single module / cross-module / cross-system" | |
| R8 | "- **Complexity**: trivial / standard / complex" | "- **Complexity**: trivial / standard / complex" | |
| R9 | "This assessment sets the depth of everything below." | "This sets the depth of everything below: trivial + clear = one-paragraph design and a single confirming question; complex or vague = full process." | |
| R10 | "Trivial + clear = one-paragraph design and a single confirming question. Complex or vague = full process." | merged into R9 | |
| R11 | "Read before asking. Check relevant files, existing patterns, docs, and recent commits." | "Read before asking: relevant files, existing patterns, docs, recent commits." | |
| R12 | "Never ask the user something the codebase already answers." | "Never ask the user something the codebase already answers." | |
| R13 | "- One question at a time. Prefer multiple choice over open-ended." | "- One question at a time. Prefer multiple choice over open-ended." | |
| R14 | "- Cover, as relevant: business goal, expected outcomes, constraints, acceptance criteria, non-functional needs (performance, security, scale)." | "- Cover, as relevant: business goal, expected outcomes, constraints, acceptance criteria, non-functional needs (performance, security, scale)." | |
| R15 | "- Vague or incomplete requests ALWAYS get verification questions. Do not fill gaps with assumptions." | "- Vague or incomplete requests ALWAYS get verification questions. Do not fill gaps with assumptions." | |
| R16 | "- Present 2–3 approaches with concrete trade-offs (only 1 for trivial work)." | "- Present 2–3 approaches with concrete trade-offs (only 1 for trivial work)." | |
| R17 | "- State a recommendation and defend it. Push back if the user's idea has a flaw — agreement is not a service." | "- State a recommendation and defend it. Push back if the user's idea has a flaw — agreement is not a service." | |
| R18 | "- Ask before assuming on high-stakes choices: architecture, new libraries, data models, external services." | "- Ask before assuming on high-stakes choices: architecture, new libraries, data models, external services." | |
| R19 | "- Scale to complexity: one paragraph (trivial) to a sectioned document (complex)." | "- Scale to complexity: one paragraph (trivial) to a sectioned document (complex)." | |
| R20 | "- For standard/complex work, save to `docs/specs/YYYY-MM-DD-<topic>-design.md`." | "- For standard/complex work, save to `docs/specs/YYYY-MM-DD-<topic>-design.md`." | |
| R21 | "- Must contain: goal, chosen approach, what changes, acceptance criteria, explicit non-goals." | "- Must contain: goal, chosen approach, what changes, acceptance criteria, explicit non-goals." | |
| R22 | "Scan your own design for:" | "Scan your design for:" | |
| R23 | "- [ ] Placeholders (\"TBD\", \"figure out later\", \"somehow\")" | "- [ ] Placeholders (\"TBD\", \"figure out later\", \"somehow\")" | |
| R24 | "- [ ] Internal contradictions" | "- [ ] Internal contradictions" | |
| R25 | "- [ ] Scope creep beyond the request" | "- [ ] Scope creep beyond the request" | |
| R26 | "- [ ] Ambiguity a junior developer could misread" | "- [ ] Ambiguity a junior developer could misread" | |
| R27 | "- [ ] Missing acceptance criteria" | merged into R21 | |
| R28 | "Present the design and ask for explicit approval." | "Present the design and ask for explicit approval; silence is not approval." | |
| R29 | "Silence is not approval." | merged into R28 | |
| R30 | "Then — and only then — invoke **writing-plans**." | "Only then invoke **writing-plans**." | |
| R31 | "Never jump straight to code." | merged into R2 | |
| R32 | "&#124; \"The request is obvious, I'll just build it\" &#124; Obvious requests hide ambiguous edges. Confirm intent in one sentence, then proceed. &#124;" | "&#124; \"The request is obvious, I'll just build it\" &#124; Obvious requests hide ambiguous edges. Confirm intent in one sentence, then proceed. &#124;" | |
| R33 | "&#124; \"I'll prototype while we discuss\" &#124; Prototypes anchor decisions and become production code. Gate stands. &#124;" | merged into R2 | |
| R34 | "&#124; \"Asking questions looks incompetent\" &#124; Wrong assumptions look worse and cost more. &#124;" | "&#124; \"Asking questions looks incompetent\" &#124; Wrong assumptions look worse and cost more. &#124;" | |
| R35 | "&#124; \"The user already said what they want\" &#124; They said WHAT. The design captures HOW and confirms edges. &#124;" | "&#124; \"The user already said what they want\" &#124; They said WHAT. The design captures HOW and confirms edges. &#124;" | |

Counts (checker): 468 -> 436 words (6% cut), 58 -> 55 nonblank lines.
Reason: besides the merged gate restatements (R31, R33), the duplicate checklist item (R27), and the step 1 lead-in (R4), every sentence is a distinct rule with its own condition; shortening them further would drop a condition.
