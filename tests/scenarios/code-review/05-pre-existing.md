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
  {"type": "output_matches", "pattern": "(?i)pre-?existing[^\\n]*(?:\\n\\s*)?(?:[^\\n]|\\n(?!\\s*\\n)){0,300}?(kelvin|273)|(kelvin|273)[^\\n]{0,200}pre-?existing"},
  {"type": "output_matches", "pattern": "(?i)\\b(0|no|zero)\\W{0,4}actionable findings?"}
]
```

## Notes

Design item 2, pre-existing. to_kelvin() (+273, not +273.15) sits in the
diff's context lines but predates the branch and is outside its scope.
Target: labeled Pre-existing, not counted, no blocker.

2026-10-17 (round-1 review F2): check 2 matches a Pre-existing section whose
items sit on the lines below its label; check 3 accepts bold counts.
