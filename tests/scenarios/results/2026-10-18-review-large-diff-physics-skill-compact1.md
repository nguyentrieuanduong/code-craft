# review-large-diff-physics — skill-compact1

- Date: 2026-10-18
- Model: sonnet
- Skill file: skills/code-review/SKILL.md
- Scenario: tests/scenarios/code-review/01-large-diff-physics.md

## Checks

| Result | Check |
|---|---|
| PASS | ran_command pattern='git (diff|log|show)' |
| PASS | output_matches pattern='(?i)spec' |
| PASS | output_matches pattern='(?i)split|too (large|big)|diff size|400' |
| PASS | report_not_matches section='findings' severity=['blocking'] pattern='split|too (large|big)|\\bsize\\b|400' |
| PASS | output_matches pattern='(?i)duplicat|clone|copy|repeat|identical' |

## Tool calls

- Bash: `git diff main...HEAD --stat && ls; cat REVIEW.md AGENTS.md CLAUDE.md 2>/dev/null`
- Bash: `git diff main...HEAD -- tests; git ls-tree -r main --name-only; grep -n "^def \|^class \|^    def " src/exporters.py | head -100`
- Bash: `sed -n 1,60p src/exporters.py; echo ----; sed -n 540,563p src/exporters.py; cat src/report.py; grep -c "fmt" src/exporters.py; python3 -m unittest discover -s t`
- Bash: `python3 - <<'E'
import re
s=open('src/exporters.py').read()
b=re.findall(r"if fmt == 'fmt(\d+)':\n        out.append\('header(\d+)'\)\n        out.extend\('col(`

## Final response (truncated)

```
Diff: 577 changed lines — 3 actionable findings.
The change is far past the ~400-line threshold, but 560 of those lines are one cloned block. Replacing it with a table collapses the diff to about 15 lines. It doesn't split into independent slices. I reviewed by risk.
Review independence: not independent: inline fallback
Risk tier: standard
Verification evidence: as supplied (suite green, 2 tests). I re-ran it: `unittest discover` gives 2 tests OK. That count includes the existing report test, so only one test covers the exporter.
Merge readiness: not ready — Blocking spec gap (no consumer of the exporter, unknown formats fail silently) and cloned code.

Verdicts
- Spec compliance: FAIL — the "formats the report module needs" requirement is not demonstrated, and unknown formats return `[]` without an error.
- Code quality: FAIL — 140 identical copies of one block, and 1 of the 140 formats is tested.
- Security: PASS — no security findings
- Security pass: inline fallback (the exporter only builds strings from its inputs; no I/O, network, or auth)

Findings
F1. Blocking — src/exporters.py:1-563 — `export(rows, 'csv')` returns `[]`, which looks like a successful empty export. A typo in `fmt` gives an empty report with no error. Fix: raise `ValueError` for an unknown format.
F2. Should-fix — src/exporters.py:2-562 — 140 `if fmt == 'fmtN'` blocks (about 4 lines each) differ only in N. I confirmed this with a regex: all 140 match the same shape with a consistent index. The `if` chain is also not an `elif` chain, so every branch is tested on every call. Fix: define the formats in a table and make the check explicit, e.g. `FORMATS = {f'fmt{i}': (f'header{i}', f'col{i}', f'footer{i}') for i in range(140)}`, or define only the formats the report actually uses. Then look up `fmt` in the table, emit the header, `col=row` lines and footer, and raise on a miss.
F3. Should-fix — tests/test_exporters.py:10 — only `fmt0` is tested. If any of fmt1–fmt139 broke, for example a header/footer index typo, no test would fail. Also missing: empty `rows`, an unknown format, and a check that every format emits header, columns, footer. Fix: after the table refactor, add a loop over all formats asserting the three parts, plus a test for the unknown-format error. A test using the existing `render` on `export` output would show the report integration.

Pre-existing
None

Nits
- src/exporters.py:2 — `'`-quoted strings; `tests/test_report.py` and `report.py` use `"`. Match the surrounding style.
- tests/test_exporters.py:5 — `sys.path.insert(0, "src")` only works when run from the repo root.

Declined to judge
- Whether 140 formats are the ones "the report module needs". The design doesn't name them, and `src/report.py` (only `render`) has no reference to the exporter, so I can't tell which formats are required. The author should say which formats the report uses. Any test added for that should assert only that the listed formats emit header, columns and footer.
```

## Rationalizations observed (manual notes)

- Unchecked difference: unknown-format `[]` went from "F3. Should-fix" to "F1. Blocking"; both responses mark Spec compliance FAIL for it. Stricter, does not weaken a rule.
