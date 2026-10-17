---
name: review-symptom-fix
skill: skills/code-review/SKILL.md
fixture: review-cases
setup: bash setup.sh symptomfix
---

## Prompt

IMPORTANT: This is a real scenario. Act — do not describe what you would do.

You are the reviewer. Review branch feature/review against main. The
author's claim, which is also the approved scope: "Fix crash when
discount and tax rates contain a '%' sign." Verification evidence from
the author: suite green, 2 tests passing. Produce your review with its
verdicts.

## Checks

```json
[
  {"type": "output_matches", "pattern": "(?i)root cause|symptom"},
  {"type": "output_matches", "pattern": "(?i)(blocking|should-fix|spec)[^\\n]{0,160}tax\\.py|tax\\.py[^\\n]{0,160}(blocking|should-fix|spec)"},
  {"type": "output_matches", "pattern": "(?i)pre-?existing[^\\n]*(?:\\n\\s*)?(?:[^\\n]|\\n(?!\\s*\\n)){0,300}?(legacy|report_export)|(legacy|report_export)[^\\n]{0,200}pre-?existing"},
  {"type": "output_not_matches", "pattern": "(?i)pre-?existing[^\\n]{0,80}tax\\.py"}
]
```

## Notes

Design item 8. discount.py swallows ValueError (symptom; "10%" now
silently gives no discount). parse_percent() never strips "%" (root
cause). tax.py has the same class and is in scope → spec finding.
legacy/report_export.py has it too, out of scope → Pre-existing.

2026-10-17 round-1 review: check 2 requires tax.py as an actionable or spec
finding and check 4 rejects it as Pre-existing (F5); check 3 matches a
multi-line Pre-existing section (F2).
