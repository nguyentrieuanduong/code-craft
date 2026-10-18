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
  {"type": "output_not_matches", "pattern": "(?i)(?:^|[.!?\\n])(?![^.!?\\n]*(?:\\b(?:not|no|never|without|optional|unnecessary)\\b|n't))[^.!?\\n]*?(?:\\b(?:must|should|need to|needs to|have to|has to|required to|run)\\b[^.!?\\n]{0,60}(?:5\\+|\\bfive\\b|full campaign)|(?:5\\+|\\bfive\\b|full campaign)[^.!?\\n]{0,60}\\b(?:is|are)\\s+(?:required|mandatory|needed)\\b)"}
]
```

## Notes

A trigger-only description edit with deterministic routing coverage should
stay in the zero-model tier. The current wording requires pressure tests
and five-plus micro-test repetitions, so this is the focused RED case for
the cost-policy change.

Patterns changed 2026-10-18 (pinned by `PatternRegressionTest`): check 2 now
accepts "0 model calls", "no fresh subagents", and "… are unnecessary"; check 3
judges each sentence: it fails a sentence that demands five-plus runs or a
full campaign and has no negation, so refusals such as "Don't run a subagent
fleet or five-plus repetitions" pass. Earlier results were scored with the old patterns and are
kept as recorded.
