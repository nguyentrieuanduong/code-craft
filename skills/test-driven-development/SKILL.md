---
name: test-driven-development
description: >-
  Use whenever writing or changing production code: features, bug fixes,
  refactors. Don't use for throwaway exploration scripts explicitly marked as
  such by the user.
---

# Test-Driven Development

**IRON LAW: NO PRODUCTION CODE WITHOUT A FAILING TEST FIRST.**

If you wrote production code before its test: delete the code, write the test,
start over. Keeping it "since it's already written" violates the law.

## Step 0: Detect the real test runner

Before anything, find how THIS project runs tests (package scripts, Makefile,
pyproject, CI config). Do not guess. `npm test`, `pytest`, `go test`, and
`bun test` are different worlds — use the project's actual command, and reuse
that exact command for every RED/GREEN check.

## The cycle

### RED — write one failing test

- ONE test, testing real behavior (not implementation details, not mocks of
  the thing under test).
- Clear name describing the behavior: `test_expired_token_is_rejected`, not
  `test_case_2`.
- **Run it. Watch it fail. Read the failure.** It must fail because the
  behavior is missing — not from a typo, import error, or syntax error.
  A test failing for the wrong reason is not RED.

### GREEN — minimal code to pass

- Write the least code that makes this one test pass. YAGNI ruthlessly: no
  extra parameters, no speculative branches, no "while I'm here".
- **Run the full suite.** The new test passes, every other test still passes,
  output is pristine (no warnings you introduced, no stray prints).

### REFACTOR — only on green

- Remove duplication, improve names, extract helpers ONLY if reused,
  domain-significant, or clearly improving readability (smallest sufficient
  abstraction).
- Run the suite again after refactoring. Still green or you revert.

Commit at GREEN (or after refactor). One cycle ≈ one commit.

## What to test (coverage of behavior, not lines)

1. **Happy path** — the documented, intended behavior.
2. **Worst cases** — incorrect input, invalid configuration, boundary values,
   simulated crash/failure of a dependency. Every feature gets at least one.
3. **Integration tests when external services are involved** — make everything
   as real as possible: fakes, local containers (testcontainers), or dedicated
   test services. Avoid mocking the external system's client; mock-heavy
   integration tests verify your mocks, not your code.
4. **Bug fixes start with a reproducing test** that fails before the fix and
   passes after. No reproducing test = the bug is not understood yet.

## Forbidden rationalizations

| Excuse | Reality |
|--------|---------|
| "Too simple to test" | Simple code breaks too, and tests document intent. 30 seconds of test, write it. |
| "I'll write tests after" | Tests written after pass by construction and verify nothing. |
| "I already manually tested it" | Manual tests vanish. The next change re-breaks it silently. |
| "Deleting my untested code is wasteful" | Untested code is a liability, not an asset. Delete it. |
| "Mocking everything makes tests fast" | Fast tests of mocks prove nothing about production. |
| "The test fails, but the code is right" | Then the test is wrong — fix the test with the same rigor as code. Never skip it. |
