---
name: brainstorming
description: >-
  Use BEFORE any creative or implementation work: new features, behavior
  changes, refactors, new projects. Turns a request into an approved design
  through context exploration, clarifying questions, and alternatives with
  trade-offs. HARD GATE: no production code until the user approves the design.
  Don't use for pure bug fixes (use systematic-debugging).
---

# Brainstorming

Turn a vague request into a design the user has explicitly approved.

**HARD GATE: You may not write production code, scaffold files, or "just
prototype" until the user says the design is approved. There are no exceptions.**

## Process

### 1. Assess the request (silently, first)

Classify before doing anything:

- **Clarity**: clear / vague / incomplete
- **Type**: new feature / enhancement / refactor / migration / new project
- **Scope**: single file / single module / cross-module / cross-system
- **Complexity**: trivial / standard / complex

This assessment sets the depth of everything below. Trivial + clear =
one-paragraph design and a single confirming question. Complex or vague =
full process.

### 2. Explore context

Read before asking. Check relevant files, existing patterns, docs, and recent
commits. Never ask the user something the codebase already answers.

### 3. Ask clarifying questions

- One question at a time. Prefer multiple choice over open-ended.
- Cover, as relevant: business goal, expected outcomes, constraints,
  acceptance criteria, non-functional needs (performance, security, scale).
- Vague or incomplete requests ALWAYS get verification questions. Do not fill
  gaps with assumptions.

### 4. Propose approaches

- Present 2–3 approaches with concrete trade-offs (only 1 for trivial work).
- State a recommendation and defend it. Push back if the user's idea has a
  flaw — agreement is not a service.
- Ask before assuming on high-stakes choices: architecture, new libraries,
  data models, external services.

### 5. Write the design

- Scale to complexity: one paragraph (trivial) to a sectioned document (complex).
- For standard/complex work, save to `docs/specs/YYYY-MM-DD-<topic>-design.md`.
- Must contain: goal, chosen approach, what changes, acceptance criteria,
  explicit non-goals.

### 6. Self-review before presenting

Scan your own design for:

- [ ] Placeholders ("TBD", "figure out later", "somehow")
- [ ] Internal contradictions
- [ ] Scope creep beyond the request
- [ ] Ambiguity a junior developer could misread
- [ ] Missing acceptance criteria

### 7. Get approval

Present the design and ask for explicit approval. Silence is not approval.
Then — and only then — invoke **writing-plans**. Never jump straight to code.

## Forbidden rationalizations

| Excuse | Reality |
|--------|---------|
| "The request is obvious, I'll just build it" | Obvious requests hide ambiguous edges. Confirm intent in one sentence, then proceed. |
| "I'll prototype while we discuss" | Prototypes anchor decisions and become production code. Gate stands. |
| "Asking questions looks incompetent" | Wrong assumptions look worse and cost more. |
| "The user already said what they want" | They said WHAT. The design captures HOW and confirms edges. |
