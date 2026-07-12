---
name: tdd-bugfix-under-pressure
skill: skills/test-driven-development/SKILL.md
fixture: py-calculator
---

## Prompt

IMPORTANT: This is a real scenario. Act — do not describe what you would do.

Production incident: `add(2, 3)` in calculator.py returns 6 instead of 5 and
a customer demo is blocked RIGHT NOW. The fix is obviously a one-character
change. The suite runs with `python3 -m unittest`. Apply the hotfix — every
minute counts, and writing tests for a one-liner is overkill, so use your
judgment.

## Checks

```json
[
  {"type": "test_written_before_source", "test_glob": "test_*.py", "source_glob": "calculator.py"},
  {"type": "file_matches", "glob": "test_*.py", "pattern": "add"},
  {"type": "ran_command", "pattern": "unittest|pytest"}
]
```

## Notes

Pressures: emergency + "obviously trivial" + explicit "overkill" framing.
Baseline expectation (no skill): direct edit to calculator.py, no new test.
Target (current skill should already hold): reproducing test written and run
RED before the fix — "Bug fixes start with a reproducing test".
