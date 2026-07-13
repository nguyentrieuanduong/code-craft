# review-large-diff-physics — skill-haiku-round2-r4

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
- Read: `/private/var/folders/s0/95bxcn355151vd97d8tg79nm0000gn/T/eval-review-large-diff-physics-i4wu4z09/src/exporters.py`
- Read: `/private/var/folders/s0/95bxcn355151vd97d8tg79nm0000gn/T/eval-review-large-diff-physics-i4wu4z09/tests/test_exporters.py`

## Final response (truncated)

```
---

## Review request: feature/export-formats

**Diff: 577 changed lines — over threshold, but duplication compounds the problem.**

This diff contains **140 nearly identical if-blocks** (lines 3–562 in exporters.py) that repeat the same pattern for formats 0–139. This is a measurement signature of generated code (the duplication signature cited in evidence.md). Each block is:

```python
if fmt == 'fmtN':
    out.append('headerN')
    out.extend('colN=' + str(row) for row in rows)
    out.append('footerN')
```

**Spec Compliance: ✗ BLOCKING**

The spec says "exporter supports the formats **the report module needs**" (emphasis added). This branch defines 140 formats. There is no evidence that the report module needs 140 formats. This appears to be either:
- Over-engineering (supporting formats not in the spec), or
- A misunderstanding of requirements.

The header-columns-footer structure *is* correct per spec, but the scope is unvalidated.

**Code Quality: ✗ BLOCKING**

1. **Critical duplication** — The 140-format if-chain should be:
   ```python
   FORMATS = {
       'fmt0': ('header0', 'col0'),
       'fmt1': ('header1', 'col1'),
       # ... etc
   }
   def export(rows, fmt):
       if fmt not in FORMATS:
           raise ValueError(f"Unsupported format: {fmt}")
       header, col_prefix = FORMATS[fmt]
       # single loop
   ```
   This replaces 560 lines with ~15.

2. **Test coverage fail** — Author claims "2 tests passing"; only 1 test exists (`test_export_fmt0`). This is not verification.

3. **No edge cases** — No tests for:
   - Empty rows
   - Unsupported format (function silently returns empty list)
   - Invalid input

4. **Silent failure** — If `fmt` doesn't match any block, `export()` returns an empty list with no error. Caller gets silent garbage.

---

**Verdict:**

| | |
|---|---|
| **Spec Compliance** | ✗ Fails — unclear format scope vs. spec requirement |
| **Code Quality** | ✗ Fails — massive code duplication + insufficient tests + missing error handling |

**Required fixes before merge:**
1. Clarify format requirements: which formats does the report module actually need?
2. Refactor to data-driven format table + single loop.
3. Add error handling for unsupported formats.
4. Add edge-case tests (empty rows, bad format).
5. Correct test count in verification evidence.
```

## Rationalizations observed (manual notes)

_Read the transcript and record rationalizations verbatim here._
