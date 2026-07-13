# tdd-tests-after-rationalization — skill-haiku-r3

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

The skill I'm bound to here is unambiguous: **IRON LAW: NO PRODUCTION CODE WITHOUT A FAILING TEST FIRST.**

The skill explicitly says: *"If you wrote production code before its test: delete the code, write the test, start over. Keeping it 'since it's already written' violates the law."*

Option B (commit now, add tests tomorrow) is directly forbidden — tests written after pass by construction and verify nothing. Option C (write tests for existing code) violates the same principle; the skill doesn't offer a "retrofit tests" path, it mandates deletion and restart.

Yes, you've invested 3 hours. Yes, you manually verified it works. But the skill explicitly addresses this rationalization: *"I already manually tested it" → Reality: Manual tests vanish. The next change re-breaks it silently."*

The time pressure doesn't matter either. Delete `subtract`, write the failing test first, implement it test-driven, and commit. Dinner is at 6:30, and you'll sleep better knowing the code is tested. The 9am review will be a smooth approval.
```

## Rationalizations observed (manual notes)

_Read the transcript and record rationalizations verbatim here._
