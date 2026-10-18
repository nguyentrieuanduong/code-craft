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
  {"type": "report_matches", "field": "changed lines", "pattern": "^\\d+$"},
  {"type": "report_matches", "field": "actionable", "pattern": "^[12]$"},
  {"type": "report_matches", "section": "findings", "pattern": "paginate\\.py:\\d+", "severity": ["blocking", "should-fix"]},
  {"type": "output_matches", "pattern": "(?i)last (item|element)|off[- ]by[- ]one|size ?- ?1|4 items|four items"},
  {"type": "report_actionable_count"}
]
```

## Notes

Design item 2. page() returns size-1 items; the one test only checks
non-emptiness. Target: summary line with size and "1 actionable finding",
the finding located at paginate.py:<line> with its concrete effect.

2026-10-17 round-1 review: check 2 accepts bold labels and comma counts
(F7); check 3 accepts 1 or 2 findings, since flagging the weak test as a
second Should-fix is defensible (user decision).

2026-10-17 (structured grading, Task B-S): checks 2–4 read the report: line
count, 1 or 2 actionable, a Blocking/Should-fix item at paginate.py:N.

Added 2026-10-18: the header's actionable count must equal the Blocking and
Should-fix items in Findings (07/08 bench1 and 08 compact1 miscounted).
Earlier results were scored without it.
