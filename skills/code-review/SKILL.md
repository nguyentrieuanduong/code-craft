---
name: code-review
description: >-
  Use when a task or feature is complete and needs review before merge, when
  asked to review code, and when handling review feedback. Don't use before
  verification-before-completion has passed.
---

# Code Review

Review happens after verification passes and before merge. It has two sides:
requesting it well, and receiving it well.

## Requesting review

Provide the reviewer a structured package:

```markdown
## Review request: <task/feature name>
- Spec/design: <link or path to the approved design>
- Plan tasks covered: <task numbers>
- Diff: <branch, plus files/lines changed from `git diff main...HEAD --stat`>
- Verification evidence: <test counts, build/lint results — actual numbers>
- Known concerns: <anything you are unsure about — hiding doubts wastes the review>
```

Ask for TWO separate verdicts (they fail independently):

1. **Spec compliance** — does the code do what the approved design says?
   Nothing missing, nothing extra?
2. **Code quality** — coding-standards followed, security-baseline held,
   tests meaningful (worst cases, real integrations), abstractions justified?

## Performing review (when you are the reviewer)

- **Step 0 — diff size verdict, before any code comment.** Run
  `git diff main...HEAD --stat` and OPEN the review with the number and its
  verdict: "Diff: N changed lines — within/over the ~400-line review
  threshold." Past ~400 changed lines, reviewer defect detection collapses
  (see docs/evidence.md): if over, the review's FIRST finding is that the
  diff is too large and should be split into independently reviewable
  slices. Then review as thoroughly as the size allows anyway. A review
  that never states the size verdict is incomplete.
- Read the design first, then the diff. Judge against the spec, not taste.
- Check what is NOT there: missing worst-case tests, missing boundary
  validation, silently dropped requirements.
- **Search the diff for cloned blocks.** Repeated or near-identical code is
  the measured signature of generated code (duplication up 4–8×, see
  docs/evidence.md): if the same shape appears more than twice, name the
  duplication as a finding and propose the loop/table/function that
  collapses it. Check this explicitly on every review — it hides in diffs
  that look busy but uniform.
- Cite evidence for every finding: file, line, and the rule or spec clause it
  violates. No vague "this could be better".
- Classify findings: **Blocking** (spec violation, security, broken tests) /
  **Should-fix** (standards violation) / **Nit** (optional).
- No filler praise. A short "spec-compliant, no blocking findings" beats a
  paragraph of compliments.

## Receiving review

- **Evaluate technically before implementing.** A reviewer's comment is a
  claim, not a command. Verify it against the code and the spec.
- Justified finding → fix it via the normal cycle (failing test where
  applicable, then fix).
- Unjustified finding → push back with evidence, respectfully and concretely.
  Blind compliance introduces as many bugs as blind refusal.
- Ambiguous finding → ask a clarifying question rather than guessing intent.
- Never mark a finding resolved without the fix verified (fresh test run).

## Forbidden rationalizations

| Excuse | Reality |
|--------|---------|
| "The reviewer is senior, just do what they say" | Seniors are wrong sometimes. Verify, then act. |
| "It's a nit, I'll skip responding" | Unaddressed comments erode trust. Respond to every one, even with 'declined because X'. |
| "Review will catch what I missed" | Review is a safety net, not a substitute for verification. Arrive clean. |
| "The diff is big, but I can review it all" | Nobody can — detection rates collapse past ~400 changed lines. State the size verdict first, recommend the split, then do your best. |
