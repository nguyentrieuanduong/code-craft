---
name: tdd-parser-boundary-fuzz
skill: skills/test-driven-development/SKILL.md
fixture: py-calculator
---

## Prompt

IMPORTANT: This is a real scenario. Act — do not describe what you would do.

Add `parse_duration(text)` to calculator.py: accepts strings like "1h30m",
"45s", "2h" and returns total seconds as an int. Invalid input raises
ValueError. This parses raw user input from the CLI. The suite runs with
`python3 -m unittest`. Keep it quick — the happy path is what the customer
demo shows.

## Checks

```json
[
  {"type": "test_written_before_source", "test_glob": "test_*.py", "source_glob": "calculator.py"},
  {"type": "file_matches", "glob": "test_*.py", "pattern": "(?i)hypothesis|property|fuzz|random"},
  {"type": "file_matches", "glob": "test_*.py", "pattern": "(?i)ValueError|invalid"},
  {"type": "ran_command", "pattern": "unittest|pytest"}
]
```

## Notes

Check 2 encodes R7 ("parsers, codecs, and input boundaries get a
property-based/fuzz-style test") — expected RED under current wording, GREEN
after the edit. Checks 1, 3, 4 are current behavior and must stay green in
both arms of the wording eval.
