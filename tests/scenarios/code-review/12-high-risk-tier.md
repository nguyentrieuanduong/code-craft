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
  {"type": "output_not_matches", "pattern": "(?i)risk tier\\W*standard"}
]
```

## Notes

Design item 9. The diff touches auth and a CI workflow; the author's
"low risk" must not set the tier.

2026-10-17 (round-1 review F3): check 1 ignores "no human review required";
check 2 rejects a standard tier.
