---
name: verification-before-completion
description: >-
  Use BEFORE any claim of success, completion, or correctness: "done", "tests
  pass", "fixed", "builds", "works". Requires running a fresh command and
  reading its full output before the claim. Also defines the full verification
  loop to run when a feature is complete. Skipping verification is lying, not
  optimism.
---

# Verification Before Completion

**Claiming without verifying is lying, even when the claim turns out true.**

## The gate (before ANY success claim)

1. **Identify** the command that would prove the claim.
2. **Run it fresh** — complete, not partial, not from memory of an earlier run.
3. **Read the full output** — not just the exit code, not just the last line.
4. **Confirm output matches the claim.**
5. Only then, make the claim — and show the evidence.

Skip any step and the claim is unsupported. Do not make it.

| Claim | Required fresh evidence |
|-------|------------------------|
| "Tests pass" | Full suite run, output read, 0 failures counted |
| "It builds" | Build command run to completion, exit 0 seen |
| "Linter is clean" | Lint command run, zero warnings in output |
| "Bug is fixed" | Reproducing test run: failed before, passes now |
| "Feature works" | Feature exercised end-to-end (run the app, hit the endpoint, open the UI) |

## Red-flag words

If you are about to write any of these in a success statement, stop — you have
not verified:

> "should work" · "probably passes" · "seems fine" · "I'm confident" ·
> "ought to" · "likely" · any satisfaction expressed without a command run

State uncertainty directly instead: "I have not run X yet" is honest;
"it should work" is not.

## The full verification loop (feature complete / pre-review)

Run every phase. Any failure = NOT READY; fix and rerun from the failed phase.

- [ ] **Build** — project's build command, exit 0
- [ ] **Types** — type-checker (`tsc --noEmit`, `mypy`, ...) clean
- [ ] **Lint** — zero errors; report remaining warnings honestly
- [ ] **Tests** — full suite with coverage; happy path AND worst cases present
- [ ] **Security scan** — no hardcoded secrets/keys, no debug prints/console.log,
      security-baseline rules hold
- [ ] **Diff review** — read `git diff` in full: leftover debug code? missing
      boundary error handling? accidental file? scope creep?

Report the result per phase with the actual numbers (tests run/passed,
warnings count), not adjectives.

## Forbidden rationalizations

| Excuse | Reality |
|--------|---------|
| "I ran the tests earlier" | Code changed since. Earlier runs prove nothing about now. |
| "Only this file changed, partial test run is enough" | Cross-module breakage is exactly what full suites catch. |
| "The change is trivial, verification is overkill" | Trivial changes cause outages precisely because nobody verifies them. |
| "Exit code 0 means it passed" | Suites can pass with 0 tests collected. Read the counts. |
