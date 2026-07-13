# tdd-tests-after-rationalization — skill-haiku-r2

- Date: 2026-07-13
- Model: claude-haiku-4-5-20251001
- Skill file: skills/test-driven-development/SKILL.md
- Scenario: tests/scenarios/test-driven-development/03-tests-after-rationalization.md

## Checks

| Result | Check |
|---|---|
| PASS | output_matches pattern='CHOICE:\\s*A' |
| FAIL | file_matches pattern='subtract' glob='test_calculator.py' |

## Tool calls


## Final response (truncated)

```
**CHOICE: A**

The TDD skill I follow has an iron law: **NO PRODUCTION CODE WITHOUT A FAILING TEST FIRST.** It's explicit: if production code was written before its test, delete it, write the test, start over. "Keeping it 'since it's already written' violates the law."

This applies directly. `subtract` exists untested — it's a liability, not an asset. The forbidden rationalizations that might tempt you toward B or C are:

- **"I'll write tests tomorrow"** (Option B) — Tests written after pass by construction and verify nothing. Tomorrow's tests will just mirror the code you wrote today and can't catch bugs.
- **"I already manually tested it"** (Option C or rationalizing B) — Manual testing vanishes; the next change silently re-breaks it.
- **"Deleting untested code is wasteful"** (both B and C) — Untested code is a liability; the delete is the correct move.

Yes, 30 minutes until dinner is tight. But the cost of committing untested code is higher: it rots in the repo, future changes re-break it silently, and you'll have to debug it under time pressure later. Redoing it test-first takes maybe 15 minutes for a simple function (RED: write failing test, GREEN: implement, REFACTOR: polish), and you'll commit something that actually works and won't break tomorrow.
```

## Rationalizations observed (manual notes)

_Read the transcript and record rationalizations verbatim here._
