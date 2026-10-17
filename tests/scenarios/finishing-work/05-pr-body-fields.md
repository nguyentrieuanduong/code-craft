---
name: finishing-pr-body-fields
skill: skills/finishing-work/SKILL.md
fixture: review-cases
setup: bash setup.sh clean
---

## Prompt

IMPORTANT: This is a real scenario. Act — do not describe what you would do.

You are on branch feature/review: plan tasks complete, verification
passed (`python3 -m unittest discover tests`), review done with 0
actionable findings, risk tier standard. I choose option 2. This sandbox
has no remote and no network: instead of pushing, write the PR body you
would use to PR_BODY.md and stop.

## Checks

```json
[
  {"type": "file_matches", "glob": "PR_BODY.md", "pattern": "(?i)\\btesting\\b"},
  {"type": "file_matches", "glob": "PR_BODY.md", "pattern": "(?i)\\brisk\\b"},
  {"type": "file_matches", "glob": "PR_BODY.md", "pattern": "(?i)how to revert"}
]
```

## Notes

Design item 9, PR body fields.
