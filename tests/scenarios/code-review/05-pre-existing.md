---
name: review-pre-existing
skill: skills/code-review/SKILL.md
fixture: review-cases
setup: bash setup.sh preexisting
---

## Prompt

IMPORTANT: This is a real scenario. Act — do not describe what you would do.

You are the reviewer. Review branch feature/review against main. The
approved design said: "Add to_fahrenheit(celsius), converting Celsius to
Fahrenheit." Verification evidence from the author: suite green, 2 tests
passing. Produce your review with its verdicts.

## Checks

```json
[
  {"type": "ran_command", "pattern": "git (diff|log|show)"},
  {"type": "output_matches", "pattern": "(?i)pre-?existing[^\\n]{0,200}(kelvin|273)|(kelvin|273)[^\\n]{0,200}pre-?existing"},
  {"type": "output_matches", "pattern": "(?i)\\b(0|no|zero) actionable findings?"}
]
```

## Notes

Design item 2, pre-existing. to_kelvin() (+273, not +273.15) sits in the
diff's context lines but predates the branch and is outside its scope.
Target: labeled Pre-existing, not counted, no blocker.
