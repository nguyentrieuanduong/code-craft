---
name: review-ambiguous-intent
skill: skills/code-review/SKILL.md
fixture: review-cases
setup: bash setup.sh ambiguous
---

## Prompt

IMPORTANT: This is a real scenario. Act — do not describe what you would do.

You are the reviewer. Review branch feature/review against main. The
approved design said: "export_csv(rows) renders simple user rows as CSV
text: a `name,email` header row, then one line per user; fields contain no
commas, quotes, or newlines." Verification evidence
from the author: suite green, 1 test passing. Produce your review with its
verdicts.

## Checks

```json
[
  {"type": "output_matches", "pattern": "(?i)declined to judge[^\\n]*(?:\\n\\s*)?(?:[^\\n]|\\n(?!\\s*\\n)){0,300}?(sort|order)"},
  {"type": "output_matches", "pattern": "(?i)sort|order"},
  {"type": "output_not_matches", "pattern": "(?i)(?<!non-)(?<!not )(blocking|should-fix)[^\\n]{0,80}(sort|order)"}
]
```

## Notes

Design item 2, ambiguous intent. Rows are sorted by name; the design is
silent on row order and either reading is defensible. Target: the order
question is named under Declined to judge, not raised as a blocker.

2026-10-17 (round-1 review F4): check 1 requires the order question inside
the Declined to judge section; check 3 also rejects it as Should-fix.
