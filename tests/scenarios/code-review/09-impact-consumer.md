---
name: review-impact-consumer
skill: skills/code-review/SKILL.md
fixture: review-cases
setup: bash setup.sh consumer
---

## Prompt

IMPORTANT: This is a real scenario. Act — do not describe what you would do.

You are the reviewer. Review branch feature/review against main. The
approved design said: "price(amount, currency) formats an amount in the
given currency; every caller passes the currency it displays."
Verification evidence from the author: suite green, 1 test passing.
Produce your review with its verdicts.

## Checks

```json
[
  {"type": "report_matches", "section": "findings", "pattern": "invoice\\.py", "severity": ["blocking", "should-fix"]},
  {"type": "report_not_matches", "section": "findings", "pattern": "^\\W*(blocking|should-fix|nit)?\\W*(src/)?catalog\\.py"},
  {"type": "report_actionable_count"}
]
```

## Notes

Design item 5. price() is a public interface; invoice.py still calls
price(amount) and now raises TypeError, untested. catalog.py imports only
CURRENCY and is unaffected. Target: invoice.py reported, catalog.py not.

2026-10-17 (structured grading, Task B-S): checks 1–2 read the report:
invoice.py in a Blocking/Should-fix item; no finding cites catalog.py first.

Added 2026-10-18: the header's actionable count must equal the Blocking and
Should-fix items in Findings (07/08 bench1 and 08 compact1 miscounted).
Earlier results were scored without it.
