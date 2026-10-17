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
  {"type": "report_matches", "section": "findings", "pattern": "tax\\.py", "severity": ["blocking", "should-fix"]},
  {"type": "report_matches", "section": "pre-existing", "pattern": "legacy|report_export"},
  {"type": "report_not_matches", "section": "pre-existing", "pattern": "^\\W*(src/)?tax\\.py"}
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

2026-10-17 (round-2 review F5): check 2 requires tax.py on a Blocking or
Should-fix finding line (or a failed spec verdict); check 4 rejects tax.py as
an item of a multi-line Pre-existing section.

2026-10-17 (structured grading, Task B-S): checks 2–4 read the report:
tax.py in a Blocking/Should-fix item, legacy under Pre-existing, no
Pre-existing item led by tax.py.
