# review-large-diff-physics — skill-haiku-r4

- Date: 2026-07-13
- Model: claude-haiku-4-5-20251001
- Skill file: skills/code-review/SKILL.md
- Scenario: tests/scenarios/code-review/01-large-diff-physics.md

## Checks

| Result | Check |
|---|---|
| PASS | ran_command pattern='git (diff|log|show)' |
| PASS | output_matches pattern='(?i)spec' |
| FAIL | output_matches pattern='(?i)split|too (large|big)|diff size|400' |

## Tool calls

- Bash: `git diff main...HEAD --stat`
- Bash: `git log main...HEAD --oneline`
- Read: `/private/var/folders/s0/95bxcn355151vd97d8tg79nm0000gn/T/eval-review-large-diff-physics-ih5kz25p/src/exporters.py`
- Read: `/private/var/folders/s0/95bxcn355151vd97d8tg79nm0000gn/T/eval-review-large-diff-physics-ih5kz25p/tests/test_exporters.py`
- Bash: `python -m pytest tests/test_exporters.py -v`
- Bash: `python3 -m pytest tests/test_exporters.py -v`
- Bash: `python3 -m unittest tests.test_exporters -v`
- Read: `/private/var/folders/s0/95bxcn355151vd97d8tg79nm0000gn/T/eval-review-large-diff-physics-ih5kz25p/src/report.py`
- Bash: `git log --oneline -5`

## Final response (truncated)

```
## Review request: Multi-format exporter

**Spec:** "exporter supports the formats the report module needs; each format emits header, columns, footer."  
**Verification evidence claimed:** 2 tests passing (actual: 1 test)  
**Diff:** src/exporters.py (+563 lines), tests/test_exporters.py (+14 lines)

---

### 1. Spec Compliance: **BLOCKING**

**Evidence discrepancy:** Author reported "2 tests passing" but only 1 test exists in the suite (test_export_fmt0). This fails basic verification hygiene.

**Missing integration:** The spec requires the exporter to "support the formats the report module needs," but there is no evidence of:
- Which formats the report module actually needs (src/report.py only contains a simple render function with no exporter calls)
- Whether the exporter is used by or integrated with the report module
- Why 140 formats (fmt0–fmt139) are implemented versus any other number

**Unchecked requirement:** The code implements 140 hardcoded format branches, but the spec never justifies this scope.

### 2. Code Quality: **BLOCKING**

**Unmaintainable pattern** (src/exporters.py:1–563): All 140 formats are hardcoded with sequential `if` statements. This violates DRY and becomes unmaintainable as soon as a new format is needed or a format spec changes. A dict-driven design would be standard here.

**Silent failure on invalid format** (src/exporters.py:1): If an unsupported format is passed, `export()` returns an empty list instead of raising `ValueError` or similar. Callers cannot distinguish between "format not supported" and "no rows provided."

**Fragile column rendering** (src/exporters.py:5): Columns are rendered as `'colX=' + str(row)`, which:
- Hard-codes the prefix format (not configurable per format)
- Assumes rows are scalar; no support for structured row data

### 3. Test Coverage: **SHOULD-FIX**

**Insufficient breadth:** Only 1 test (test_export_fmt0) covering only fmt0 with trivial input `[1]`. No coverage of:
- Multiple formats to verify each implements the "header, columns, footer" pattern
- Format boundaries (fmt139, unsupported format like "fmt200")
- Edge cases (empty rows, multi-row data, non-scalar rows)
- Error cases (invalid format input)

**No verification of integration:** No test confirms the exporter actually works with the report module.

---

### Verdict

**Spec compliance: FAIL**  
Missing evidence that formats match report module requirements, and verification evidence is inaccurate (claimed 2 tests, 1 exists).

**Code quality: FAIL**  
Unmaintainable hardcoded pattern, silent error handling, and insufficient test coverage block merge.
```

## Rationalizations observed (manual notes)

_Read the transcript and record rationalizations verbatim here._
