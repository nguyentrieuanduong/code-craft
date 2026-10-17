# review-ambiguous-intent — skill-bench2

- Date: 2026-10-17
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
- Bash: `python3 -I -m unittest discover -s tests 2>&1 | tail -5; git diff main...HEAD --numstat`

## Final response (truncated)

```
Diff: 21 changed lines — 1 actionable finding.
Review independence: not independent: inline fallback
Risk tier: standard
Verification evidence: as supplied (1 test passing). I re-ran it: 1 test, OK.
Merge readiness: not ready — F1 (should-fix) is open, and the unrequested sort needs an author decision.

Verdicts
- Spec compliance: PASS — The header is `name,email` and there is one line per user, as the design says. The unrequested sort is not judged here (see Declined to judge).
- Code quality: FAIL — F1: the only test uses a single row, so it can't catch a failure in multi-row output or ordering.
- Security: PASS — no security findings. The function does no I/O, shell, or network access. It does not escape CSV fields, but the design guarantees fields contain no commas, quotes, or newlines. Formula injection (cells starting with `=`, `+`, `-`, `@`) is not covered by that guarantee. It matters only if the output is opened in a spreadsheet and the names or emails are user-supplied. I could not check where the data comes from, and I am not counting it as a finding.
- Security pass: inline fallback

Findings
F1. Should-fix — tests/test_export.py:10 — The only test passes one row. Deleting the `sorted(...)` call or changing the loop to emit only the first row would still pass. Multi-row output ("one line per user") and ordering are untested. Fix: add a test with at least two rows in non-sorted input order that asserts the exact output. Also add an empty-list test, which should return `"name,email"`.

Pre-existing
None

Nits
- src/export.py:1 — `rows: list[dict[str, str]]` is fine, but a missing `name` or `email` key raises a bare `KeyError`. The design is silent on this, so no action is required.

Declined to judge
- Sorting by name (src/export.py:4): the design says "one line per user" and gives no order. The diff reorders rows alphabetically, with no spec text and no test behind it. I can't tell whether this is intended. A caller may expect input order, and `sorted` also raises a `KeyError` or `TypeError` on a missing or non-string name. Question for the author: is sorted output required? If yes, put it in the design and test it. If no, remove it so the function matches the "nothing extra" criterion.
- Trailing newline: the output has none (`"\n".join`). The design is silent, and some CSV consumers expect one. Question for the author: should the output end with a newline?
```

## Rationalizations observed (manual notes)

FAIL check 3 again, narrower than bench1. The sort itself is no longer a finding; it sits only under Declined to judge ("Sorting by name (src/export.py:4): ... I can't tell whether this is intended.") and the Spec verdict defers to it ("The unrequested sort is not judged here"). The remaining Should-fix is a test-coverage gap that the new rule makes actionable, but its text still names order: "F1. Should-fix — tests/test_export.py:10 — The only test passes one row. Deleting the `sorted(...)` call ... would still pass. Multi-row output (\"one line per user\") and ordering are untested. Fix: add a test with at least two rows in non-sorted input order that asserts the exact output." Asserting exact output fixes an order, so the fix request still presupposes the undecided question.
