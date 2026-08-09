---
name: standards-inline-vs-implicit
skill: skills/coding-standards/SKILL.md
fixture: inline-vs-implicit
---

## Prompt

IMPORTANT: This is a real scenario. Act — do not describe what you would do.

settings.py is up for review before merge. The suite is green
(`python3 -m unittest`) and the author is waiting on you. Report what must
change before this merges, and what must not.

## Checks

```json
[
  {"type": "output_matches", "pattern": "(?i)truthy|truthiness|falsy|is None|zero"},
  {"type": "output_not_matches", "pattern": "(?i)(extract|split|expand|unroll)[^.]{0,80}(one-?liner|comprehension|generator expression|ternary|inline)"}
]
```

## Notes

PENDING RUN — written as the failing-test-first for the principle #1 rewording
(`Readability over cleverness` → `Cleverness bounded by readability`,
commit eb5672c). The before/after pair has not been executed yet; two model
calls owed under CONTRIBUTING.md rule 2:

```
python3 tests/scenarios/run.py tests/scenarios/coding-standards/01-inline-vs-implicit.md \
  --arm both --reps 1 --isolate
```

The fixture holds both halves of the principle side by side. `resolve_timeout`
and `resolve_retries` use `or` for defaulting, so a configured `0` silently
becomes 30 / 3 — hidden intent, and the shipped tests never pass 0.
`selected_stages` and `describe` are legitimate concise forms: a one-line
generator expression and a ternary, both readable in one pass.

Check 1 is the bug half and is expected green in both arms — the falsy-zero
default is a real defect models catch unaided.

Check 2 is the load-bearing one. Expected RED under the old wording, whose
title ("Readability over cleverness") reads as a standing instruction to
expand; expected GREEN after, where concision is explicitly endorsed and only
opacity is prohibited. A reviewer who demands the comprehension or ternary be
broken up is applying the polarity the rewording removes.
