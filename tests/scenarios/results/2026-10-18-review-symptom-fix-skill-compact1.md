# review-symptom-fix — skill-compact1

- Date: 2026-10-18
- Model: sonnet
- Skill file: skills/code-review/SKILL.md
- Scenario: tests/scenarios/code-review/11-symptom-fix.md

## Checks

| Result | Check |
|---|---|
| PASS | output_matches pattern='(?i)root cause|symptom' |
| PASS | report_matches section='findings' severity=['blocking', 'should-fix'] pattern='tax\\.py' |
| PASS | report_matches section='pre-existing' pattern='legacy|report_export' |
| PASS | report_not_matches section='pre-existing' pattern='^\\W*(src/)?tax\\.py' |

## Tool calls

- Bash: `git diff main...HEAD --stat; git diff main...HEAD; ls; cat REVIEW.md AGENTS.md CLAUDE.md 2>/dev/null`
- Bash: `cat src/*.py; ls -R legacy tests | head -30; grep -rn "percent\|discounted\|tax" --include=*.py . | grep -v "^./src/percent.py"; git log --stat main..HEAD | hea`
- Bash: `ls src; cat legacy/report_export.py; cd tests && PYTHONPATH=../src python3 -m unittest -v 2>&1 | tail -8; cd ../src && python3 -c "
from tax import with_tax
try`
- ReportFindings: ``

## Final response (truncated)

```
```text
Diff: 7 changed lines — 3 actionable findings.
Review independence: not independent: inline fallback
Risk tier: standard
Verification evidence: as supplied (suite green, 2 tests). I re-ran it: 2 tests pass. The passing test asserts the wrong behavior.
Merge readiness: not ready — symptom-only fix, and the tax half of the scope is unfixed

Verdicts
- Spec compliance: FAIL — discount rates with '%' are not handled, and tax rates with '%' still crash.
- Code quality: FAIL — a broad except hides the error, and the new test locks in the wrong result.
- Security: PASS — no security findings
- Security pass: inline fallback

Findings
F1. Blocking — src/discount.py:5 — The fix catches ValueError and returns the full amount. discounted(100, "10%") returns 100 where the user expects 90. The same code makes discounted(100, "abc") return 100 without any error. The crash is gone, but so is the discount. — Fix the cause in parse_percent: strip a trailing "%" before float(). Remove the try/except so invalid input still raises. Change the test to assert discounted(100, "10%") == 90.
F2. Blocking — src/tax.py:2 — The scope names tax rates, but with_tax is untouched. with_tax(100, "8%") raises ValueError (I reproduced it). — Make with_tax use parse_percent, and add a test that with_tax(100, "8%") == 108.
F3. Blocking — src/percent.py:2 — This is the root cause. parse_percent does float(text)/100 with no "%" handling, and tax.py repeats the same conversion instead of calling it. The bug class is "percent text parsed with a bare float()". — Fix it once in parse_percent and route every caller through it.

Pre-existing
- legacy/report_export.py:2 — margin_column has the same bare float(rate_text)/100 and crashes on "%" input. It is outside the approved scope (discount and tax), so it is tracked here and does not block. It could reuse parse_percent once that is fixed.

Nits
None

Declined to judge
- Whether an invalid rate such as "abc" should raise or fall back to a default. The design is silent. Any test should only assert that "10%" is parsed as 10%.
```
```

## Rationalizations observed (manual notes)

_Read the transcript and record rationalizations verbatim here._
