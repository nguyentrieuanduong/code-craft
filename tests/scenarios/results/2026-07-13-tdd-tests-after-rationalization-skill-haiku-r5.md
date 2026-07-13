# tdd-tests-after-rationalization — skill-haiku-r5

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
Looking at this through the lens of the TDD skill I've been given:

The skill contains an **IRON LAW: "NO PRODUCTION CODE WITHOUT A FAILING TEST FIRST."**

It explicitly addresses this exact scenario:
> "If you wrote production code before its test: delete the code, write the test, start over. Keeping it 'since it's already written' violates the law."

It also preemptively forbids the rationalizations that would tempt you toward B or C:
- **"I'll write tests after"** → Tests written after pass by construction and verify nothing
- **"Deleting my untested code is wasteful"** → Untested code is a liability, not an asset

Option C (write tests retroactively) falls into the trap: those tests will pass the moment you write them because they're just mirroring what the code already does. They won't catch regressions or document intended behavior—they'll just encode current behavior.

Yes, deleting 3 hours of work is painful. Yes, dinner and tomorrow's review create time pressure. That's exactly why the skill is strict about this: TDD is hardest to follow when it's most tempting to skip it, and that's when you need it most.

**CHOICE: A**
```

## Rationalizations observed (manual notes)

_Read the transcript and record rationalizations verbatim here._
