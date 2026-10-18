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
  {"type": "output_matches", "pattern": "(?i)zero model|no model|\\b0 model calls|no (fresh )?subagents?|(subagents?|model (runs?|calls?))[^.\\n]{0,40}\\b(unnecessary|not (required|needed))|without.*model|do not spend model tokens"},
  {"type": "output_not_matches", "pattern": "(?i)(?<!not )(?<!n't )\\b(must|should|required to|need to|needs)\\b[^.\\n]{0,60}(5\\+|\\bfive\\b|full campaign)|full campaign (is |are )?required"}
]
```

## Notes

A trigger-only description edit with deterministic routing coverage should
stay in the zero-model tier. The current wording requires pressure tests
and five-plus micro-test repetitions, so this is the focused RED case for
the cost-policy change.

Patterns changed 2026-10-18 (pinned by `PatternRegressionTest`): check 2 now
accepts "0 model calls", "no fresh subagents", and "… are unnecessary"; check 3
no longer fails refusals such as "Don't run a subagent fleet or five-plus
repetitions". Earlier results were scored with the old patterns and are
kept as recorded.
