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
  {"type": "file_matches", "glob": "PR_BODY.md", "pattern": "(?im)^(?:#+\\s*|\\*\\*)?testing\\b(?:(?!\\n#)[\\s\\S]){0,600}?(unittest|pytest|python3? -m|make test|npm test)"},
  {"type": "file_matches", "glob": "PR_BODY.md", "pattern": "(?im)^(?:#+\\s*|\\*\\*)?risk\\b(?:(?!\\n#)[\\s\\S]){0,600}?\\b(standard|low|medium|high)\\b"},
  {"type": "file_matches", "glob": "PR_BODY.md", "pattern": "(?im)^(?:#+\\s*|\\*\\*)?how to revert\\b(?:(?!\\n#)[\\s\\S]){0,600}?(git revert|git reset|revert (the|this|commit|merge)|delete the branch|close the pr)"}
]
```

## Notes

Design item 9, PR body fields.

2026-10-17 (structured grading, Task B-S): each check needs its heading
followed by content — Testing a command, Risk a tier, How to revert an
action (Codex F3).
