---
name: using-code-craft
description: >-
  Meta-skill that governs all development work. Use at the start of EVERY
  conversation and before EVERY response involving code, features, bugs, or
  design. Enforces checking for an applicable skill before acting and following
  the mandatory workflow ordering. Don't use for pure conversation with no
  engineering task.
---

# Using code-craft

## The rule

**Before ANY action or response, check whether a skill applies. If one applies,
you MUST use it.** This check happens before clarifying questions, before file
exploration, before writing a single line of code.

User instructions (CLAUDE.md, direct requests) override skills. Nothing else does.

## Dispatch table

| Situation | Skill to invoke |
|-----------|-----------------|
| "Build X", "add feature", "create...", any behavior change | brainstorming |
| Design approved, need implementation steps | writing-plans |
| Plan approved, time to implement | executing-plans |
| Writing any production code | test-driven-development + coding-standards + security-baseline |
| Bug, test failure, unexpected behavior, "it doesn't work" | systematic-debugging |
| About to say "done", "passes", "fixed", "works" | verification-before-completion |
| Task or feature complete, before merge | code-review |
| All tasks complete, branch ready | finishing-work |

## Mandatory ordering

```
brainstorming -> writing-plans -> executing-plans -> verification -> code-review -> finishing-work
```

- You may not write production code while in brainstorming or writing-plans.
- You may not skip brainstorming because the request "seems clear".
  A trivial request gets a trivial (one-paragraph) design — but it gets one.
- Process skills (brainstorming, systematic-debugging) come BEFORE
  implementation skills. "Fix this bug" means systematic-debugging first.

## Rationalizations that are forbidden

If you catch yourself thinking any of these, stop — the rule stands:

| Excuse | Reality |
|--------|---------|
| "This is a simple question, no skill needed" | Simple questions become implementation work. Check first. |
| "I need context before checking skills" | Skill check comes first. The skill tells you what context to gather. |
| "Using the full workflow is overkill here" | Depth is adaptive INSIDE each skill. Skipping the skill is not adaptive, it's undisciplined. |
| "The user is in a hurry" | Hurried work that must be redone is slower. Gates exist to prevent rework. |
| "I already know how to do this" | The skill encodes failure modes you cannot see from inside the task. |

## Scaling, not skipping

Every stage runs, but its depth scales with the task:

- **Trivial** (typo, one-line fix): brainstorming = one sentence confirming intent;
  plan = 1–3 steps; still TDD, still verify.
- **Standard** (feature in one module): short design with 1–2 clarifying
  questions; plan with per-step tests.
- **Complex** (cross-cutting, new architecture, data migration): full
  brainstorming with alternatives and trade-offs; comprehensive plan; per-unit
  review.
