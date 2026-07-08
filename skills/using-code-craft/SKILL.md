---
name: using-code-craft
description: >-
  Use at the start of EVERY session and before EVERY response involving code,
  features, bugs, or design. Don't use for pure conversation with no
  engineering task.
---

# Using code-craft

**Before ANY action or response, check this table. If a skill applies, read it
and follow it — before clarifying questions, before exploring files, before
writing code.** User instructions override skills; nothing else does.

| Situation | Skill |
|-----------|-------|
| "Build X", new feature, any behavior change | brainstorming |
| Design approved | writing-plans |
| Plan approved, or resuming work | executing-plans |
| Writing any production code | test-driven-development + coding-standards + security-baseline |
| Bug, error, test failure, unexpected behavior | systematic-debugging |
| About to say "done", "passes", "fixed", "works" | verification-before-completion |
| Task complete, before merge | code-review |
| Branch ready to conclude | finishing-work |

Mandatory order:
`brainstorming → writing-plans → executing-plans → verification → code-review → finishing-work`

Every stage runs; depth scales inside each skill (a trivial fix gets a
one-sentence design and a 3-step plan — but still TDD, still verified).
No production code during brainstorming or planning. Process skills
(brainstorming, systematic-debugging) come before implementation skills.

If you are thinking "too simple for this", "overkill", "the user is in a
hurry", or "I need context first" — that is rationalization, not judgment.
Check the table first; the skill tells you what context to gather.
