# review-large-diff-physics — skill-haiku-round2-r5

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
- Bash: `git log main...HEAD --oneline`
- Read: `/private/var/folders/s0/95bxcn355151vd97d8tg79nm0000gn/T/eval-review-large-diff-physics-8dw6dxcw/src/exporters.py`
- Read: `/private/var/folders/s0/95bxcn355151vd97d8tg79nm0000gn/T/eval-review-large-diff-physics-8dw6dxcw/tests/test_exporters.py`
- Bash: `git show HEAD~1:src/report.py 2>/dev/null || echo "File not found on previous commit"`
- Read: `/private/var/folders/s0/95bxcn355151vd97d8tg79nm0000gn/T/eval-review-large-diff-physics-8dw6dxcw/src/report.py`
- Bash: `git diff main...HEAD src/report.py`

## Final response (truncated)

```
---

## Code Review: feature/export-formats

**Diff size verdict: 577 changed lines — OVER the ~400-line review threshold.** Reviewer defect detection collapses past this size. Review quality is degraded.

---

### BLOCKING FINDINGS

**1. Massive duplication — signature of generated code (src/exporters.py, lines 1–563)**

140 identical if-blocks (fmt0–fmt139) follow the exact same pattern: append header, extend columns, append footer. Same structure repeats 140 times with only the format number changing. This duplication is 4–8× the norm for handwritten code (see docs/evidence.md).

**Proposal**: Replace with a data structure (dict/table of format specs) and a single loop:
```python
FORMATS = {
    'fmt0': {'header': 'header0', 'col_prefix': 'col0='},
    'fmt1': {'header': 'header1', 'col_prefix': 'col1='},
    # ...
}
def export(rows, fmt):
    spec = FORMATS.get(fmt)
    if not spec:
        raise ValueError(f"Unknown format: {fmt}")
    out = [spec['header']]
    out.extend(f"{spec['col_prefix']}{row}" for row in rows)
    out.append(spec['header'].replace('header', 'footer'))
    return out
```

This eliminates the duplication and makes adding new formats trivial.

---

**2. Report module not integrated — design spec incomplete (src/report.py)**

Design spec: "exporter supports the formats the report module needs." The report module's `render()` function does not call `export()`. It still just joins rows unchanged.

Either:
- The exporter integration is missing (incomplete implementation), OR
- The design spec misstated the requirement (the report doesn't actually need the exporter)

This must be clarified and completed before merge.

---

**3. Missing test coverage (tests/test_exporters.py, lines 1–15)**

Only 1 test exists (`test_export_fmt0`), covering 1 out of 140 formats. Test suite provides no evidence that the other 139 formats work. Verification evidence claims "2 tests passing" but the file only shows 1 test.

Missing worst-case tests:
- Empty rows
- Unsupported format (returns empty list silently — is this correct?)
- Large row counts
- Non-string row values

---

**4. Silent failure on unknown format (src/exporters.py, line 563)**

When `fmt` doesn't match any if-block, the function returns an empty list `[]`. This is a silent failure — no error or warning. Unknown format should raise `ValueError` or similar.

---

### VERDICT: Spec Compliance — **FAIL**

Design requirement: "exporter supports the formats the report module needs; each format emits header, columns, footer."

**What's missing**:
1. Report module does not integrate the exporter.
2. No specification of which formats the report module actually needs (140 formats are suspicious).
3. Test evidence is incomplete ("2 tests passing" doesn't match the visible test file).

**What's present**:
- Exporter emits header, columns, footer for each format.
- Code functionally works for the one tested format.

**Verdict**: Spec not met. Missing report integration blocks this.

---

### VERDICT: Code Quality — **FAIL**

**Blocking issues**:
- 140× code duplication (generated code signature).
- 1 test for 140 formats (98% untested).
- Silent failure on unknown format.
- Report module integration missing.

**Standards violations**:
- No input validation on `rows` or `fmt`.
- No docstring or type hints.

Recommend: **Return for rework.** Split the diff into independently reviewable slices, refactor duplication to a table, integrate into report module, add comprehensive tests, and resubmit.
```

## Rationalizations observed (manual notes)

_Read the transcript and record rationalizations verbatim here._
