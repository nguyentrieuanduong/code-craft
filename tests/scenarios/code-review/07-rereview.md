---
name: review-rereview-converges
skill: skills/code-review/SKILL.md
fixture: review-cases
setup: bash setup.sh rereview
---

## Prompt

IMPORTANT: This is a real scenario. Act — do not describe what you would do.

You are the reviewer, round 2. Review branch feature/review. Your round-1
findings are in notes/review-round-1.md; round 1 reviewed the commit
tagged review-round-1, and the author has pushed a fix commit since. The
design requires lowercase slugs with single dashes between words. Produce
the round-2 review.

## Checks

```json
[
  {"type": "ran_command", "pattern": "review-round-1"},
  {"type": "output_matches", "pattern": "(?i)F1[^\\n]{0,160}(addressed|fixed|resolved)"},
  {"type": "output_matches", "pattern": "(?i)F2[^\\n]{0,160}(still open|open|unresolved|not addressed|remains)"},
  {"type": "output_not_matches", "pattern": "(?i)runs of separators are not collapsed into a\\s+single dash"}
]
```

## Notes

Design item 3. Target: diff since review-round-1, F1 marked addressed,
F2 statused by ID as still open without reposting round 1's text.
