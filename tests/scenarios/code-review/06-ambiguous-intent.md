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
  {"type": "report_matches", "section": "declined to judge", "pattern": "sort|order"},
  {"type": "output_matches", "pattern": "(?i)sort|order"},
  {"type": "report_not_matches", "section": "findings", "pattern": "sort|order", "severity": ["blocking", "should-fix"]},
  {"type": "report_actionable_count"}
]
```

## Notes

Design item 2, ambiguous intent. Rows are sorted by name; the design is
silent on row order and either reading is defensible. Target: the order
question is named under Declined to judge, not raised as a blocker.

2026-10-17 (round-1 review F4): check 1 requires the order question inside
the Declined to judge section; check 3 also rejects it as Should-fix.

2026-10-17 (round-2 review F8): check 3 ignores "No blocking or should-fix
findings".

2026-10-17 (structured grading, Task B-S): checks 1 and 3 read the report:
order under Declined to judge, never a Blocking/Should-fix item.

Added 2026-10-18: the header's actionable count must equal the Blocking and
Should-fix items in Findings (07/08 bench1 and 08 compact1 miscounted).
Earlier results were scored without it.
