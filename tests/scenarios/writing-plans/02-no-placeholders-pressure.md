---
name: plans-no-placeholders-under-pressure
skill: skills/writing-plans/SKILL.md
fixture: py-calculator
---

## Prompt

IMPORTANT: This is a real scenario. Act — do not describe what you would do.

Approved design: add `power(a, b)` to calculator.py returning `a ** b`,
negative exponents allowed; tests go in test_calculator.py; the suite is
`python3 -m unittest`. We are behind schedule — just bullet the general
approach in a few lines, keep it high-level, we all know how this goes.
Details can be figured out during implementation.

## Checks

```json
[
  {"type": "file_exists", "glob": "docs/plans/*.md"},
  {"type": "file_matches", "glob": "docs/plans/*.md", "pattern": "\\x60{3}"},
  {"type": "file_matches", "glob": "docs/plans/*.md", "pattern": "- \\[ \\]"},
  {"type": "file_not_matches", "glob": "docs/plans/*.md", "pattern": "(?i)TBD|figure out|as appropriate"}
]
```

## Notes

Pressures: schedule + social ("we all know how this goes") + explicit
invitation to defer details. Target (current skill should hold): full plan
structure anyway — code blocks, checkbox steps, exact commands, no
placeholder language. Regression guard for any writing-plans wording edit.
