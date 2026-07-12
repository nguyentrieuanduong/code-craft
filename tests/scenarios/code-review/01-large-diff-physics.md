---
name: review-large-diff-physics
skill: skills/code-review/SKILL.md
fixture: feature-branch
setup: bash setup.sh large
---

## Prompt

IMPORTANT: This is a real scenario. Act — do not describe what you would do.

You are the reviewer. Review branch feature/export-formats against main.
The approved design said: "exporter supports the formats the report module
needs; each format emits header, columns, footer." Verification evidence
from the author: suite green, 2 tests passing. Produce your review with the
two verdicts.

## Checks

```json
[
  {"type": "ran_command", "pattern": "git (diff|log|show)"},
  {"type": "output_matches", "pattern": "(?i)spec"},
  {"type": "output_matches", "pattern": "(?i)split|too (large|big)|diff size|400"}
]
```

## Notes

The diff is ~580 changed lines of near-identical blocks. Check 3 encodes
R3's review-side physics (defect detection collapses past ~400 changed LOC —
a diff this size gets called out, with a split suggested): expected RED
under current wording, GREEN after. Checks 1–2 are current behavior (read
the actual diff, judge against the spec).
