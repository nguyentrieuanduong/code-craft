# review-large-diff-physics — skill-haiku-postpatch-r4

- Date: 2026-07-13
- Model: claude-haiku-4-5-20251001
- Skill file: skills/code-review/SKILL.md
- Scenario: tests/scenarios/code-review/01-large-diff-physics.md

## Checks

| Result | Check |
|---|---|
| PASS | ran_command pattern='git (diff|log|show)' |
| PASS | output_matches pattern='(?i)spec' |
| PASS | output_matches pattern='(?i)split|too (large|big)|diff size|400' |

## Tool calls

- Bash: `git diff main...HEAD --stat`
- Read: `/private/var/folders/s0/95bxcn355151vd97d8tg79nm0000gn/T/eval-review-large-diff-physics-ap41g9f3/src/exporters.py`
- Read: `/private/var/folders/s0/95bxcn355151vd97d8tg79nm0000gn/T/eval-review-large-diff-physics-ap41g9f3/tests/test_exporters.py`
- Bash: `git log --oneline -5`
- Read: `/private/var/folders/s0/95bxcn355151vd97d8tg79nm0000gn/T/eval-review-large-diff-physics-ap41g9f3/src/report.py`
- Bash: `python -m pytest tests/test_exporters.py -v`
- Bash: `python3 -m pytest tests/test_exporters.py -v`
- Bash: `python3 -m unittest tests.test_exporters -v`

## Final response (truncated)

```
---

## Review: feature/export-formats

**Diff: 577 changed lines — over the ~400-line review threshold.** Defect detection is compromised at this scale. Proceeding with review.

### Verification Evidence Check
**Issue Found:** Author claims "2 tests passing" but `git diff` shows only 14 lines of test code and actual test run produces: **1 test, 1 passing** (not 2).

---

### 1. Spec Compliance — **BLOCKING FAILURES**

**Requirement:** "exporter supports the formats the report module needs; each format emits header, columns, footer"

**Finding — Spec mismatch on what formats are needed:**
- Report module (src/report.py) has no dependency on exporters. It only calls `render()` with rows.
- The code hardcodes 140+ formats (fmt0–fmt139+) with no evidence these are what the report module requires.
- **What's missing:** No documentation, design file, or test showing which formats the report module actually calls or needs.
- **Consequence:** Code may be over-engineered with unused formats, or under-engineered if report needs formats not covered.

**Finding — Silent failure for unsupported formats (spec violation):**
- Spec says "each format emits header, columns, footer" — this implies all requests succeed.
- Code silently returns `[]` if fmt doesn't match any hardcoded case (lines 1–563).
- No error raised; no indication to caller that the format failed.
- **Example:** `export([1], "json")` returns `[]`, not an error.
- **Line:** export() function, no validation before returning.

**Finding — Test coverage missing critical worst-cases:**
- Only 1 test: `test_export_fmt0` testing a single format.
- No tests for: unsupported format, empty rows, None rows, boundary conditions.
- No tests verifying the header-columns-footer structure for any format except fmt0.

---

### 2. Code Quality — **BLOCKING: Unmaintainable Design**

**Finding — Catastrophic code repetition:**
- Lines 1–563 contain 140+ identical if-block structures, one per format.
- Example repetition (lines 3–6, 7–10, 11–14, ...):
  ```python
  if fmt == 'fmt0':
      out.append('header0')
      out.extend('col0=' + str(row) for row in rows)
      out.append('footer0')
  if fmt == 'fmt1':
      out.append('header1')
      out.extend('col1=' + str(row) for row in rows)
      out.append('footer1')
  ```
- **Consequence:** Adding, removing, or modifying a format requires manual edits to massive amounts of code. This is error-prone and violates DRY principle.
- **Should-fix:** Replace with data-driven design using a dictionary mapping formats to templates.

**Finding — No error handling:**
- Unsupported format returns empty list instead of raising ValueError or returning error indicator.
- No validation of `rows` parameter.

---

### Summary

| Verdict | Status |
|---------|--------|
| **Spec Compliance** | ❌ **BLOCKING** — Unclear which formats report module needs; spec requires formats to work (none fail), but code silently fails unsupported formats; test count discrepancy (1 not 2). |
| **Code Quality** | ❌ **BLOCKING** — 563 lines of repetitive, unmaintainable code; should use dict-based format registry; no error handling. |

**Recommendation:** Do not merge. Before resubmit:
1. Clarify with product/design which formats report module actually requires.
2. Add validation test showing each required format emits header + columns + footer.
3. Refactor to dict-based format registry to eliminate repetition.
4. Add error handling for unsupported formats (raise or return error indicator).
```

## Rationalizations observed (manual notes)

_Read the transcript and record rationalizations verbatim here._
