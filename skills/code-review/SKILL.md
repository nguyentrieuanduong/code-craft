---
name: code-review
description: >-
  Use when a task or feature is complete and needs review before merge, when
  asked to review code, and when handling review feedback.
---

# Code Review

Review happens before merge. It has two sides: requesting it well, and
receiving it well.

An explicitly requested review runs even when verification evidence is
missing: review the diff, and name the missing evidence in the verdict
("Verification evidence: none supplied"). Merge readiness still requires
verification-before-completion — never call a diff ready to merge without
it.

## Requesting review

Provide the reviewer a structured package:

```markdown
## Review request: <task/feature name>
- Spec/design: <link or path to the approved design>
- Plan tasks covered: <task numbers>
- Diff: <branch, plus files/lines changed from `git diff main...HEAD --stat`>
- Verification evidence: <test counts, build/lint results — actual numbers, or "none yet">
- Known concerns: <anything you are unsure about — hiding doubts wastes the review>
```

Ask for TWO separate verdicts (they fail independently):

1. **Spec compliance** — does the code do what the approved design says?
   Nothing missing, nothing extra?
2. **Code quality** — coding-standards followed, security-baseline held,
   tests meaningful (worst cases, real integrations), abstractions justified?

## Performing review (when you are the reviewer)

- **Step 0 — size signal, before any code comment.** Run
  `git diff main...HEAD --stat` and OPEN the review with one summary
  line: "Diff: {changed_lines} changed lines — {count} actionable
  {finding_or_findings}." Use the measured line count; write "finding"
  for 1 and "findings" otherwise.
  Actionable means Blocking or Should-fix; write 0 when there are none and say plainly
  that nothing needs fixing. Past ~400 changed lines reviewer defect
  detection collapses (see `../using-code-craft/references/evidence.md`):
  say whether the change splits into independently reviewable slices and
  recommend the split when it does — a recommendation, not a Blocking
  finding. Generated, deleted, or mechanical bulk counts by its actual
  risk and reviewability, not its line count. A review that never states
  the size is incomplete.
- Read the design first, then the diff. Judge against the spec, not
  taste. Where the design is silent, judge by what a reasonable user
  would expect; when intent cannot be established, list the question
  under **Declined to judge** instead of inventing a blocker.
- Check what is NOT there: missing worst-case tests, missing boundary
  validation, silently dropped requirements.
- **Search the diff for cloned blocks.** Repeated or near-identical code is
  the measured signature of generated code (duplication up 4–8×, see
  `../using-code-craft/references/evidence.md`): if the same shape appears
  more than twice, name the
  duplication as a finding and propose the loop/table/function that
  collapses it. Check this explicitly on every review — it hides in diffs
  that look busy but uniform.
  Also flag any NEW private helper in the diff that duplicates a utility
  already existing elsewhere in the repo — cite the existing utility's
  path and propose importing it (promote it if private) instead of
  keeping the copy.
- **Verify every finding before presenting it.** Re-read the cited lines
  and check the claim against the diff and the repository. Each
  actionable finding states the responsible file and line (or the exact
  omitted requirement when no line exists), the observed or reproducible
  effect (input → wrong result), and its severity. A candidate you cannot
  make concrete is not a finding: drop it, or list it under **Declined to
  judge** without a fix request. No vague "this could be better".
- Classify findings: **Blocking** (spec violation, security, broken
  tests) and **Should-fix** (standards violation) are actionable and
  counted; **Nit** is optional, one line each, not counted.
  **Pre-existing** is a problem the diff did not introduce and its
  approved scope does not cover: report it in its own section; never
  count it or block on it.
- No filler praise. A short "spec-compliant, 0 actionable findings" beats
  a paragraph of compliments.

## Re-review (follow-up rounds)

- Review the diff since the last reviewed commit
  (`git diff <last-reviewed>..HEAD`) plus the previously open findings —
  not the whole branch again.
- Status each open finding by its ID: **addressed** (with the line that
  fixes it) or **still open**. Do not repost an unchanged finding as new,
  and do not reword or regrade a decided one.
- After three rounds without convergence, stop cycling: say the approach
  needs reassessment and propose discussing it with the author before
  another round.

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
| "The diff is big, but I can review it all" | Nobody can — detection collapses past ~400 changed lines. State the size, recommend a split where one exists, then review by risk. |
| "No test output, so I can't review yet" | Review what exists and name the missing evidence. Calling it merge-ready without evidence is the failure, not reviewing early. |
| "I'm fairly sure this is a bug" | Unverified is a guess. Name the line and the concrete effect, or list it under Declined to judge. |
| "This old bug is right there, I'll block on it" | The diff didn't introduce it. Label it Pre-existing so it gets tracked without blaming this change. |
| "One more round will catch the rest" | Rounds past three repeat themselves. Stop and reassess the approach with the author. |
