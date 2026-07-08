---
name: writing-plans
description: >-
  Use after a design is approved and before any implementation begins. Don't
  use before brainstorming is complete.
---

# Writing Plans

Turn an approved design into a plan so explicit that a junior developer — or a
smaller model — can execute it without making a single decision.

**HARD GATE: The plan must be approved by the user before any step executes.**

## Plan structure

Save to `docs/plans/YYYY-MM-DD-<topic>-plan.md`:

```markdown
# Plan: <topic>

## Goal
<one paragraph, from the approved design>

## Global constraints
<exact values from the design: names, limits, versions, endpoints — never "as appropriate">

## Architecture
<file map: every file created or modified, one responsibility each>

## Tasks
### Task 1: <name>
- Files: <exact paths>
- Interfaces: <what this consumes and produces>
- Steps:
  - [ ] 1.1 Write failing test `<test name>` in <path> (code block)
  - [ ] 1.2 Run `<exact test command>` — expect FAIL: <reason>
  - [ ] 1.3 Implement <specific thing> in <path> (code block)
  - [ ] 1.4 Run `<exact test command>` — expect PASS
  - [ ] 1.5 Commit: "<message>"
```

## Rules

1. **Map files first.** Every file gets one responsibility. Follow existing
   codebase patterns — check before inventing.
2. **Right-size tasks.** A task is the smallest unit that carries its own test
   cycle and can be reviewed independently. Each step takes 2–5 minutes.
3. **No placeholders.** "TBD", "similar to above", "handle appropriately", and
   "etc." are banned. Every step contains its actual content: real code blocks,
   real commands, real names.
4. **Every task ends in a commit.** One task ≈ one small feature or 1–3 related
   functions. Commit messages 5–20 words.
5. **Brownfield: modify in place.** List existing files to change by exact
   path. Never plan `Foo_new.py` or `Foo_v2.py` copies of existing files.
6. **Story traceability.** Each task names the design requirement it satisfies,
   so nothing in the design is silently dropped.

## Self-review before presenting

- [ ] Coverage scan: every design requirement maps to at least one task
- [ ] Placeholder scan: search the plan for "TBD", "somehow", "appropriate", "etc."
- [ ] Type/interface consistency: task N's outputs match task N+1's inputs
- [ ] Every step has an exact command or code block
- [ ] Constraints section uses exact values, not descriptions of values

## Handoff

After approval, invoke **executing-plans**. The plan file is the single source
of truth — execution updates its checkboxes, never improvises around it.

## Forbidden rationalizations

| Excuse | Reality |
|--------|---------|
| "I'll figure out details during implementation" | Details deferred are decisions made under pressure. Decide now. |
| "The plan is obvious from the design" | Then it takes 5 minutes to write. Write it. |
| "Code blocks in a plan are wasted effort" | They are the effort. Execution becomes mechanical, which is the point. |
