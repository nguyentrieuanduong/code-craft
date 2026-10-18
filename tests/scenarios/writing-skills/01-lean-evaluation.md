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
  {"type": "output_not_matches", "pattern": "(?i)(?<!\\bno )(?<!\\bnot )(?<!n't )(?<!\\bnever )\\b(?:must|should|needs?(?: to)?|have to|has to|required to|ought to)\\b(?!\\s+(?:not|never)\\b)(?:(?!\\b(?:not|no|never|instead of|rather than)\\b)[^.;:!?\\n]){0,60}?(?:5\\+|\\bfive\\b|\\b5\\s+(?:rep|run|time)|full campaign)|(?:5\\+|\\bfive\\b|\\b5\\s+(?:rep|run|time)|full campaign)[^.;:!?\\n]{0,60}?\\b(?:is|are|must be|should be)\\s+(?!not\\b)(?:required|mandatory|needed|run)\\b|(?:^|[.;:!?\\n]|\\b(?:also|then|and|first)\\b)\\s*run\\s+(?:(?!\\b(?:not|no|never|instead of|rather than)\\b)[^.;:!?\\n]){0,60}?(?:5\\+|\\bfive\\b|\\b5\\s+(?:rep|run|time)|full campaign)"}
]
```

## Notes

A trigger-only description edit with deterministic routing coverage should
stay in the zero-model tier. The current wording requires pressure tests
and five-plus micro-test repetitions, so this is the focused RED case for
the cost-policy change.

Patterns changed 2026-10-18 (pinned by `PatternRegressionTest`): check 2 now
accepts "0 model calls", "no fresh subagents", and "… are unnecessary"; check 3
fails a demand for five-plus runs or a full campaign ("must/should/need to …",
"… are required", or an imperative "run …") unless a negation governs it
("must not", "no need to", "instead of"), so "Don't run a subagent fleet or
five-plus repetitions" passes and "Do not merge yet; you must run five
repetitions" fails. Earlier results were scored with the old patterns and are
kept as recorded.

Known limits of check 3 (review round 3, 2026-10-18; frozen by user decision —
read the transcript when it fails or passes unexpectedly): it fails correct
conditional restatements ("Only behavior changes need five repetitions.",
"Five-plus repetitions should be run only for behavior-shaping changes.") and
passes some demands ("Then, run five repetitions before merging.", "I recommend
five repetitions before merge."). It grades all five recorded responses correctly.
