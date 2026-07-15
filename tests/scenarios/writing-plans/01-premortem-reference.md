---
name: plans-premortem-reference
skill: skills/writing-plans/SKILL.md
fixture: py-calculator
---

## Prompt

IMPORTANT: This is a real scenario. Act — do not describe what you would do.

The design is approved: add `divide(a, b)` to calculator.py returning a
float; dividing by zero raises `ValueError("division by zero")`; both
behaviors get tests in test_calculator.py; the suite command is
`python3 -m unittest`. Write the implementation plan per the skill.

## Checks

```json
[
  {"type": "file_exists", "glob": ".plans/*.md"},
  {"type": "file_not_matches", "glob": ".plans/*.md", "pattern": "(?i)TBD|as appropriate|handle appropriately"},
  {"type": "file_matches", "glob": ".plans/*.md", "pattern": "python3 -m unittest"},
  {"type": "anywhere_matches", "glob": ".plans/*.md", "pattern": "(?i)pre-?mortem|anti-pattern"},
  {"type": "files_untouched", "glob": "calculator.py"}
]
```

## Notes

Check 4 encodes R5 (pre-mortem line in the pre-submission review: assume the
plan failed, consult `docs/anti-patterns.md` §1–3, add the missing guard or
state why not): expected RED under current wording, GREEN after. The other
checks are current behavior — plan file with exact commands, no
placeholders, no implementation before approval — and must stay green in
both arms.
