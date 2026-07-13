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
3. **Input boundaries get a fuzz/property test — MANDATORY for anything
   parsing external input** (parsers, codecs, deserializers). Example-based
   tests alone do not complete such a function: add one test that throws
   many generated inputs at it — `hypothesis` if the project has it,
   otherwise a seeded `random` loop — asserting the invariant: valid shapes
   parse, everything else raises the documented error, nothing else
   escapes. A parser without this test is not done, whatever the example
   tests say.
4. **Integration tests when external services are involved** — make everything
   as real as possible: fakes, local containers (testcontainers), or dedicated
   test services. Avoid mocking the external system's client; mock-heavy
   integration tests verify your mocks, not your code.
5. **Bug fixes start with a reproducing test** that fails before the fix and
   passes after. No reproducing test = the bug is not understood yet.

## Example cycle

```python
# RED — one test, real behavior, named for the behavior
def test_expired_token_is_rejected():
    token = make_token(expires_at=NOW - timedelta(seconds=1))
    with pytest.raises(AuthError, match="expired"):
        authenticate(token)
# run: pytest tests/test_auth.py -k expired  -> FAILS: AuthError not raised

# GREEN — minimal code, nothing speculative
def authenticate(token: Token) -> Session:
    if token.expires_at < now():
        raise AuthError("token expired")
    return Session(user_id=token.user_id)
# run: pytest  -> all pass, output pristine. Commit.
```

```python
# ❌ NOT TDD — test written after, mirrors the implementation, cannot fail
def test_authenticate():
    session = authenticate(make_token())
    assert session is not None          # asserts existence, not behavior

# ❌ NOT an integration test — mocks the system under test's dependency away
mock_db.get_user.return_value = User(...)   # verifies the mock, not the code
# ✅ integration: run against a local container / fake server, real wire format
```

## Forbidden rationalizations

| Excuse | Reality |
|--------|---------|
| "Too simple to test" | Simple code breaks too, and tests document intent. 30 seconds of test, write it. |
| "I'll write tests after" | Tests written after pass by construction and verify nothing. |
| "I already manually tested it" | Manual tests vanish. The next change re-breaks it silently. |
| "Deleting my untested code is wasteful" | Untested code is a liability, not an asset. Delete it. |
| "Mocking everything makes tests fast" | Fast tests of mocks prove nothing about production. |
| "The test fails, but the code is right" | Then the test is wrong — fix the test with the same rigor as code. Never skip it. |
| "A few example inputs cover the parser" | Example tests hit the cases you thought of; parsers break on the ones you didn't. Generate inputs and assert the invariant. |
