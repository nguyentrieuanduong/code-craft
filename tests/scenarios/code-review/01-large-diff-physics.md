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
from the author: suite green, 2 tests passing. Produce your review with its
verdicts.

## Checks

```json
[
  {"type": "ran_command", "pattern": "git (diff|log|show)"},
  {"type": "output_matches", "pattern": "(?i)spec"},
  {"type": "output_matches", "pattern": "(?i)split|too (large|big)|diff size|400"},
  {"type": "output_not_matches", "pattern": "(?im)^(?!.*\\b(no|not|non)\\b[^\\n]{0,20}blocking).*\\bblocking[^\\n]{0,80}(split|too (large|big)|size)"},
  {"type": "output_matches", "pattern": "(?i)duplicat|clone|copy|repeat|identical"}
]
```

## Notes

The diff is ~580 changed lines of near-identical blocks. Check 3 encodes
R3's review-side physics (defect detection collapses past ~400 changed LOC —
a diff this size gets called out, with a split suggested): expected RED
under current wording, GREEN after. Checks 1–2 are current behavior (read
the actual diff, judge against the spec).

2026-10-17 (design item 4): check 4 added — past ~400 lines the review
assesses and recommends a split; size alone is never a Blocking finding.

2026-10-17: check 5 copies 02-cloned-blocks' check so one benchmark run
covers both regressions; 02 stays in the corpus for full campaigns.

2026-10-17 (round-1 review F8): check 4 also excludes "Not blocking".

2026-10-17 (round-2 review F8): check 4 ignores a line that negates "blocking"
("No blocking findings…", "not a blocking finding").
