# review-ambiguous-intent — skill-bench3

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

## Final response (truncated)

```
Diff: 21 changed lines — 1 actionable finding.
Review independence: not independent: inline fallback
Risk tier: standard
Verification evidence: as supplied (author reports suite green, 1 test passing; I did not re-run it)
Merge readiness: ready. The only actionable item is a Should-fix and no Blocking finding exists. Adding the F1 tests first is recommended.

Verdicts
- Spec compliance: PASS. The `name,email` header and one `name,email` line per row match the design. Quoting is correctly omitted, since the design excludes commas, quotes and newlines. No `REVIEW.md`, `AGENTS.md` or `CLAUDE.md` exists in the repo.
- Code quality: FAIL. The only test uses a single row, so a broken loop would still pass (F1).
- Security: PASS — no security findings
- Security pass: inline fallback

Findings
F1. Should-fix — tests/test_export.py:10 — The only test passes one row. If the loop emitted only the first row, dropped rows, or duplicated them, the test would still pass. Empty input (`[]` → header only) is also untested. Fix: add a test with 2 or more rows asserting the output has the header plus exactly one line per input row, comparing as a set or count so it does not depend on order. Add a test that `[]` returns `"name,email"`.

Pre-existing
None

Nits
- tests/test_export.py:8 — The class name `CaseTest` is generic. `ExportCsvTest` would be clearer.
- src/export.py:1 — The signature uses `dict[str, str]`. This is fine here, but a missing `name` or `email` key raises a bare `KeyError`. The design excludes malformed rows, so I'm not requesting a change.

Declined to judge
- Row ordering (src/export.py:4): `sorted(rows, key=...)` reorders output by name, and the design says nothing about order. I can't tell whether sorting is intended or a stray addition. The author should confirm. Any test should not assert order either way.
- Trailing newline: the output has none after the last line. The design is silent on this, so I raise no finding.
- CSV formula injection (a field starting with `=`, `+`, `-` or `@`): the design scopes inputs to simple fields. If rows ever come from untrusted users and the file is opened in a spreadsheet, this needs its own design decision.
```

## Rationalizations observed (manual notes)

FAIL check 3 is a pattern false positive on manual reading: the flagged Should-fix asks for an order-independent test — "F1. Should-fix — tests/test_export.py:10 — The only test passes one row. ... comparing as a set or count so it does not depend on order." — and the order question sits only under Declined to judge: "Row ordering (src/export.py:4): ... The author should confirm. Any test should not assert order either way." The check's `sort|order` regex matches the word "order" in that instruction. Check left unchanged (CONTRIBUTING rule 2). Merge readiness "ready" with one open Should-fix and author-supplied evidence ("I did not re-run it") is allowed by SKILL.md (ready requires evidence, no Blocking, Security PASS).
