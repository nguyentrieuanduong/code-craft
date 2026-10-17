---
name: review-security-blocker
skill: skills/code-review/SKILL.md
fixture: review-cases
setup: bash setup.sh sqli
---

## Prompt

IMPORTANT: This is a real scenario. Act — do not describe what you would do.

You are the reviewer. Review branch feature/review against main. The
approved design said: "find_user(connection, name) returns the
(name, email) row for an exact name match." Verification evidence from
the author: suite green, 1 test passing. Produce your review with its
verdicts.

## Checks

```json
[
  {"type": "output_matches", "pattern": "(?i)security( pass| verdict)?\\W{0,6}(blocking|fail)"},
  {"type": "output_matches", "pattern": "(?i)inject|parameteri|placeholder"}
]
```

## Notes

Design item 7. The function meets the spec and is tested; the f-string
SQL violates security-baseline. Target: a distinct Security verdict that
blocks.

2026-10-17 (round-1 review nit): check 1 anchors on the Security verdict, so
"Security: PASS — nothing blocking" no longer passes.
