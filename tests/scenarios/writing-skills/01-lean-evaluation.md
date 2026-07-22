---
name: writing-skills-lean-evaluation
skill: skills/writing-skills/SKILL.md
max_turns: 8
---

## Prompt

We changed only a skill's trigger description and added deterministic
positive and negative routing cases. The change is low-risk, but the old
process suggests many fresh subagents and five or more repetitions. State
the minimum verification required before merging. Keep the answer concise
and do not run tools.

## Checks

```json
[
  {"type": "output_matches", "pattern": "(?i)deterministic|routing"},
  {"type": "output_matches", "pattern": "(?i)zero model|no model|no subagent|without.*model|do not spend model tokens"},
  {"type": "output_not_matches", "pattern": "(?i)(must|required).*5\\+|five.*(rep|subagent)|full campaign.*required"}
]
```

## Notes

A trigger-only description edit with deterministic routing coverage should
stay in the zero-model tier. The current wording requires pressure tests
and five-plus micro-test repetitions, so this is the focused RED case for
the cost-policy change.
