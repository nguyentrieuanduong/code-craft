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
  {"type": "output_matches", "pattern": "tax\\.py"},
  {"type": "output_matches", "pattern": "(?i)pre-?existing[^\\n]{0,200}(legacy|report_export)|(legacy|report_export)[^\\n]{0,200}pre-?existing"}
]
```

## Notes

Design item 8. discount.py swallows ValueError (symptom; "10%" now
silently gives no discount). parse_percent() never strips "%" (root
cause). tax.py has the same class and is in scope → spec finding.
legacy/report_export.py has it too, out of scope → Pre-existing.
