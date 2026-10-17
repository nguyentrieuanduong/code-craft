---
name: review-reads-review-md
skill: skills/code-review/SKILL.md
fixture: review-cases
setup: bash setup.sh reviewmd
---

## Prompt

IMPORTANT: This is a real scenario. Act — do not describe what you would do.

You are the reviewer. Review branch feature/review against main. The
approved design said: "Add a --shout option that prints the greeting in
capitals." Verification evidence from the author: suite green, 1 test
passing. Produce your review with its verdicts.

## Checks

```json
[
  {"type": "output_matches", "pattern": "REVIEW\\.md"},
  {"type": "report_matches", "section": "findings", "pattern": "--times", "severity": ["blocking"]}
]
```

## Notes

Design item 10. README documents --times, which the CLI lacks; the
repository's REVIEW.md names that exact failure as Blocking. Target: the
review cites REVIEW.md and reports --times.

2026-10-17 (round-1 review nit): check 2 requires --times as Blocking, as the
fixture's REVIEW.md says.

2026-10-17 (structured grading, Task B-S): check 2 requires --times in a
Blocking finding item.
