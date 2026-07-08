---
name: systematic-debugging
description: >-
  Use for ANY bug, test failure, error, or unexpected behavior. Four-phase
  root-cause process: investigate, analyze patterns, hypothesize, then fix.
  IRON LAW: no fix proposed before investigation is complete. Don't use for
  designing new features (use brainstorming).
---

# Systematic Debugging

**IRON LAW: NO FIXES BEFORE PHASE 1 IS COMPLETE.**

A fix proposed before the root cause is understood is a guess. Guesses that
happen to work hide the real defect until it returns, worse.

## Phase 1 — Root cause investigation

- **Read the error. All of it.** Stack traces, log lines, exit codes. The
  answer is usually in text you skimmed.
- **Reproduce consistently.** Find the minimal trigger. If you cannot
  reproduce it, you cannot verify a fix.
- **Check recent changes.** `git diff`, `git log` — what changed around when
  it broke?
- **Trace the data flow.** Follow the actual values from input to failure
  point. Read the code that runs, not the code you assume runs.

## Phase 2 — Pattern analysis

- Find a working example of the same pattern elsewhere in the codebase.
- Diff the broken case against the working one — line by line if needed.
- Understand every dependency the failing path touches.

## Phase 3 — Hypothesis and test

- Form ONE specific hypothesis: "X fails because Y causes Z."
- Test it with the smallest possible probe — a log line, a REPL call,
  an isolated snippet. Change ONE variable at a time.
- Hypothesis wrong? Back to Phase 1 with the new information. Do not stack
  a second guess on a failed one.
- In multi-component systems, add diagnostic instrumentation at each boundary
  (request in / response out) before touching any component's logic.

## Phase 4 — Implement the fix

- Write a failing test that reproduces the bug (per test-driven-development).
- Implement the single fix the hypothesis points to.
- Run the full suite. Verify the reproducing test passes AND nothing else broke.
- Only then invoke verification-before-completion and claim it's fixed.

## The 3-failure circuit breaker

If three fixes have failed: **stop fixing.** Three failed fixes mean the mental
model is wrong — question the architecture and your assumptions before attempt
four. State plainly to the user what you know, what you've ruled out, and what
you now suspect.

## Forbidden rationalizations

| Excuse | Reality |
|--------|---------|
| "I see the problem, it's obviously X" | Obvious-at-a-glance diagnoses are wrong often enough to require Phase 1 anyway. |
| "Let me just try changing this" | Shotgun debugging destroys the evidence trail and adds new variables. |
| "Adding a try/except makes the error go away" | Suppressing a symptom is not fixing a defect. Let errors surface. |
| "It works now, I don't know why" | Then it will break later and you won't know why. Find the mechanism. |
| "Restarting/clearing cache fixed it" | State-dependent bugs return. Identify what state and why. |
