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
  {"type": "output_matches", "pattern": "invoice\\.py"},
  {"type": "output_not_matches", "pattern": "(?i)catalog\\.py[^\\n]{0,80}(must|needs? to|should) (be )?(updat|chang)"}
]
```

## Notes

Design item 5. price() is a public interface; invoice.py still calls
price(amount) and now raises TypeError, untested. catalog.py imports only
CURRENCY and is unaffected. Target: invoice.py reported, catalog.py not.
