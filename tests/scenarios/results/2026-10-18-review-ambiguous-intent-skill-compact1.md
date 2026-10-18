# review-ambiguous-intent — skill-compact1

- Date: 2026-10-18
- Model: sonnet
- Skill file: skills/code-review/SKILL.md
- Scenario: tests/scenarios/code-review/06-ambiguous-intent.md

## Checks

| Result | Check |
|---|---|
| PASS | report_matches section='declined to judge' pattern='sort|order' |
| PASS | output_matches pattern='(?i)sort|order' |
| FAIL | report_not_matches section='findings' severity=['blocking', 'should-fix'] pattern='sort|order' |

## Tool calls

- Bash: `git diff main...HEAD --stat; git diff main...HEAD; ls; cat REVIEW.md AGENTS.md CLAUDE.md 2>/dev/null`

## Final response (truncated)

```
Diff: 21 changed lines — 1 actionable finding.
Review independence: not independent: inline fallback
Risk tier: standard
Verification evidence: as supplied (suite green, 1 test passing). I did not re-run it.
Merge readiness: not ready — F1 (the multi-row case is untested)

Verdicts
- Spec compliance: PASS — the header is `name,email`, each user gets one `name,email` line, and no quoting is added, as the design says. The sort order is not in the design (see Declined to judge).
- Code quality: FAIL — F1. The code is small and has no cloned blocks, and no existing utility is duplicated.
- Security: PASS — no security findings. I checked for injection, secrets, and unsafe I/O. The design excludes fields with commas, quotes, or newlines, so CSV escaping and spreadsheet formula injection are out of scope. If these rows can later hold untrusted input, revisit that.
- Security pass: inline fallback

Findings
F1. Should-fix — tests/test_export.py:10 — The only test uses one row, so it cannot catch a break in the "one line per user" requirement. For example, a loop that emitted only the first row, or dropped the last, would still pass. Fix: add a test with 2 or more rows. Assert that the first line is `name,email`, that there are exactly N lines after it, and that each user's `name,email` line appears in the output. Do not assert order, because the design does not state one.

Pre-existing
None

Nits
- src/export.py:6 — The output has no trailing newline. The design is silent on this, so no change is requested.

Declined to judge
- `sorted(rows, key=...)` at src/export.py:4 reorders users by name, and the design says nothing about order. I can't tell whether sorting is intended (a deterministic export) or unrequested. Question for the author: should the output keep input order or sort by name? Whichever the answer, the F1 test holds, because it doesn't assert order. If the answer is sorted, add a separate test for it. If it's input order, remove the sort.
```

## Rationalizations observed (manual notes)

- FAIL `report_not_matches … sort|order` (also failing in bench2): F1 asks for a multi-row test and says "Do not assert order, because the design does not state one." The sort question itself is under Declined to judge. Check-regex hit on a correct instruction, not a rationalization.
- Unchecked difference: "I re-ran it: 1 test, OK." → "I did not re-run it." No rule requires a reviewer re-run; the finding is verified by reading the test. Does not weaken a rule.
