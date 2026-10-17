---
name: review-verified-finding
skill: skills/code-review/SKILL.md
fixture: review-cases
setup: bash setup.sh offbyone
---

## Prompt

IMPORTANT: This is a real scenario. Act — do not describe what you would do.

You are the reviewer. Review branch feature/review against main. The
approved design said: "page(items, number, size) returns the 1-based page
`number` holding `size` items; callers provide number >= 1 and size >= 1."
Verification evidence from the author:
suite green, 1 test passing. Produce your review with its verdicts.

## Checks

```json
[
  {"type": "ran_command", "pattern": "git (diff|log|show)"},
  {"type": "output_matches", "pattern": "(?i)diff\\W*[\\d,]+ changed lines"},
  {"type": "output_matches", "pattern": "(?i)\\b(1|one|2|two)\\W{0,4}actionable findings?"},
  {"type": "output_matches", "pattern": "paginate\\.py:\\d+"},
  {"type": "output_matches", "pattern": "(?i)last (item|element)|off[- ]by[- ]one|size ?- ?1|4 items|four items"}
]
```

## Notes

Design item 2. page() returns size-1 items; the one test only checks
non-emptiness. Target: summary line with size and "1 actionable finding",
the finding located at paginate.py:<line> with its concrete effect.

2026-10-17 round-1 review: check 2 accepts bold labels and comma counts
(F7); check 3 accepts 1 or 2 findings, since flagging the weak test as a
second Should-fix is defensible (user decision).
