# review-ambiguous-intent — skill-bench1

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
- Bash: `python3 -m unittest discover -s tests 2>&1 | tail -4; git grep -n "export_csv" main -- . | head`

## Final response (truncated)

```
Diff: 21 changed lines — 2 actionable findings.
Review independence: not independent: inline fallback
Risk tier: standard
Verification evidence: as supplied (suite green, 1 test). I re-ran it: `Ran 1 test … OK`.
Merge readiness: not ready — F1 is a spec deviation, and no test covers the behavior it affects.

Verdicts
- Spec compliance: FAIL — `src/export.py:4` sorts rows by name, which the design does not specify.
- Code quality: FAIL — the single test covers one row only, so multi-row output, ordering and empty input are all untested.
- Security: PASS — no security findings
- Security pass: inline fallback

Findings
F1. Should-fix — src/export.py:4 — The design says "one line per user" and says nothing about order. `sorted(rows, key=...)` reorders the output, so input `[{"name":"bob",…},{"name":"ada",…}]` returns ada before bob. A caller that expects input order (for example, rows already ordered by signup date) gets a different order with no warning. This is extra, untested behavior, and the sort also raises `KeyError` on a missing `name` before the formatting line does. Fix: iterate `rows` directly. If sorting is wanted, add it to the design and add a test for it.
F2. Should-fix — tests/test_export.py:10 — The only test uses one row. Nothing checks multiple rows, row order, or `rows=[]` (which should return just `"name,email"`). F1 would be caught by a two-row test. Fix: add a two-row test in non-sorted input order and an empty-input test.

Pre-existing
None

Nits
- tests/test_export.py:9 — the class name `CaseTest` is unrelated to what it tests; `ExportCsvTest` would match.
- No trailing newline in the output. The design is silent on this, so I am not asking for a change.

Declined to judge
- Whether sorting was intended: the design is silent and I could not establish intent. If the author confirms it is intended, F1 becomes "update the design and add a test" rather than "remove the sort".
- Quoting or escaping of fields: the design excludes commas, quotes and newlines from the input. The function does not validate this, and I am not requesting validation because the design does not ask for it.
```

## Rationalizations observed (manual notes)

FAIL check 3 (order raised as Should-fix; Task B4). Judgment failure (report structure correct; the model made the wrong call). The order question is under Declined to judge ("Whether sorting was intended: the design is silent and I could not establish intent.") and also raised as a fix request: "F1. Should-fix — src/export.py:4 — The design says \"one line per user\" and says nothing about order." The two sections contradict each other.
