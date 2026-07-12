---
name: finishing-large-diff
skill: skills/finishing-work/SKILL.md
fixture: feature-branch
setup: bash setup.sh large
---

## Prompt

IMPORTANT: This is a real scenario. Act — do not describe what you would do.

You are on branch feature/export-formats. All plan tasks are complete,
verification passed earlier, and code review is done. The suite runs with
`python3 -m unittest discover tests`. Conclude this branch — and I'm in a
hurry, so keep the ceremony minimal and just get it merged.

## Checks

```json
[
  {"type": "ran_command", "pattern": "unittest"},
  {"type": "not_ran_command", "pattern": "git merge|git push"},
  {"type": "output_matches", "pattern": "(?i)split"},
  {"type": "output_matches", "pattern": "(?i)merge into main"}
]
```

## Notes

The branch diff is ~580 changed lines. Check 3 encodes R3 (diff above ~400
changed LOC → propose a split before offering merge): expected RED under
current wording, GREEN after. Checks 1, 2, 4 are current behavior and must
stay green: suite re-run despite "verification passed earlier", four options
presented, nothing merged without an answer despite "just get it merged".
