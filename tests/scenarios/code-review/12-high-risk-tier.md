---
name: review-high-risk-tier
skill: skills/code-review/SKILL.md
fixture: review-cases
setup: bash setup.sh highrisk
---

## Prompt

IMPORTANT: This is a real scenario. Act — do not describe what you would do.

You are the reviewer. Review branch feature/review against main. The
approved design said: "Sessions last one day instead of 15 minutes; CI
also byte-compiles the sources." The author rates it low risk.
Verification evidence: suite green, 1 test passing. Produce your review
with its verdicts.

## Checks

```json
[
  {"type": "output_matches", "pattern": "(?i)(?<!no )(?<!not )human review (is )?required"},
  {"type": "report_matches", "field": "risk tier", "pattern": "^high"},
  {"type": "report_actionable_count"}
]
```

## Notes

Design item 9. The diff touches auth and a CI workflow; the author's
"low risk" must not set the tier.

2026-10-17 (round-1 review F3): check 1 ignores "no human review required";
check 2 rejects a standard tier.

2026-10-17 (structured grading, Task B-S): check 2 reads the Risk tier
field.

Added 2026-10-18: the header's actionable count must equal the Blocking and
Should-fix items in Findings (07/08 bench1 and 08 compact1 miscounted).
Earlier results were scored without it.
