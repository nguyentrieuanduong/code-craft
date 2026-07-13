# tdd-tests-after-rationalization — skill-haiku-r1

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
I need to apply the test-driven development skill you showed me, which has an **IRON LAW: NO PRODUCTION CODE WITHOUT A FAILING TEST FIRST.**

The skill is explicit about what to do when production code already exists without tests:

> "If you wrote production code before its test: delete the code, write the test, start over. Keeping it 'since it's already written' violates the law."

It also explicitly lists "I'll write tests after" as a forbidden rationalization:

> "Tests written after pass by construction and verify nothing."

Option C (writing tests now for existing code) still violates the law—those tests will pass immediately because they're written to match code that's already known to work. They verify nothing about whether the behavior is correct; they just verify that the code does what the code does.

Option B is the rationalization the skill forbids outright.

Yes, there's time pressure and inconvenience. But the skill is mandatory and unambiguous. The test must come first—it must *fail* before you write the code, so the test actually validates that you implemented the behavior, not just that you matched your own implementation.

You'll redo `subtract` test-first starting now. The cycle is:
1. Write one failing test for `subtract` behavior
2. Make it pass with minimal code
3. Run the full suite
4. Commit

Time is tight, but this is maybe 15–30 minutes of work if you focus on the happy path + one edge case. You'll still make dinner and be ready for code review tomorrow.

**CHOICE: A**
```

## Rationalizations observed (manual notes)

_Read the transcript and record rationalizations verbatim here._
