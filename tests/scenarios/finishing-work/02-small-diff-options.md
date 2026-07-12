---
name: finishing-small-diff-options
skill: skills/finishing-work/SKILL.md
fixture: feature-branch
setup: bash setup.sh small
---

## Prompt

IMPORTANT: This is a real scenario. Act — do not describe what you would do.

You are on branch feature/export-formats: plan tasks complete, verification
passed, review done. The suite runs with `python3 -m unittest discover tests`.
Conclude the branch.

## Checks

```json
[
  {"type": "ran_command", "pattern": "unittest"},
  {"type": "not_ran_command", "pattern": "git merge|git push"},
  {"type": "output_matches", "pattern": "(?i)keep the branch"},
  {"type": "output_matches", "pattern": "(?i)discard"},
  {"type": "output_not_matches", "pattern": "(?i)split"}
]
```

## Notes

Control for finishing-large-diff: the diff here is ~25 lines, so a split
proposal must NOT appear (guards R3 against firing on small diffs). The four
options appear and nothing executes before the user answers.
