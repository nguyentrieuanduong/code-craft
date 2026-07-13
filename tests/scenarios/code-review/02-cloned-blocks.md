---
name: review-cloned-blocks
skill: skills/code-review/SKILL.md
fixture: feature-branch
setup: bash setup.sh large
---

## Prompt

IMPORTANT: This is a real scenario. Act — do not describe what you would do.

You are the reviewer. Review branch feature/export-formats against main.
The approved design said: "exporter supports the formats the report module
needs; each format emits header, columns, footer." The author reports the
suite green and asks specifically: "anything blocking before I merge?"

## Checks

```json
[
  {"type": "ran_command", "pattern": "git (diff|log|show)"},
  {"type": "output_matches", "pattern": "(?i)duplicat|clone|copy|repeat|identical"}
]
```

## Notes

src/exporters.py is 140 near-identical four-line blocks — the measured
AI-code signature (GitClear: duplication up 4–8x). Check 2 encodes R7's
review-side duplication check ("search the diff for cloned blocks"):
expected RED-or-flaky under current wording (nothing directs the reviewer
at duplication), GREEN after.

2026-07-13: haiku r4/r5 caught the clones but phrased them as "140
identical if-blocks", missing the check's synonym list — added "identical"
to the pattern (check-vocabulary bug, same class as tdd03's label bug).
