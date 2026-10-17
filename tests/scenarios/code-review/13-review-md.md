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
  {"type": "output_matches", "pattern": "--times"}
]
```

## Notes

Design item 10. README documents --times, which the CLI lacks; the
repository's REVIEW.md names that exact failure as Blocking. Target: the
review cites REVIEW.md and reports --times.
