# review-cloned-blocks — skill-haiku-r5

- Date: 2026-07-13
- Model: claude-haiku-4-5-20251001
- Skill file: skills/code-review/SKILL.md
- Scenario: tests/scenarios/code-review/02-cloned-blocks.md

## Checks

| Result | Check |
|---|---|
| PASS | ran_command pattern='git (diff|log|show)' |
| FAIL | output_matches pattern='(?i)duplicat|clone|copy|repeat' |

## Tool calls

- Skill: ``
- Bash: `git diff main...HEAD --stat`
- Bash: `git diff main...HEAD`
- Bash: `find . -name "*report*" -type f`
- Bash: `cd src && python -m pytest tests/test_exporters.py -v`
- Read: `/private/var/folders/s0/95bxcn355151vd97d8tg79nm0000gn/T/eval-review-cloned-blocks-v_o6hf9k/src/report.py`
- Read: `/private/var/folders/s0/95bxcn355151vd97d8tg79nm0000gn/T/eval-review-cloned-blocks-v_o6hf9k/tests/test_report.py`
- Bash: `git log --all --oneline`
- Bash: `git show 4baace2 --stat`
- Bash: `which python3 && cd src && python3 -m pytest ../tests/test_exporters.py -v 2>&1`
- Bash: `python3 -m unittest tests.test_exporters -v 2>&1`

## Final response (truncated)

```
## Code Review: feature/export-formats

**Diff size:** 577 lines added (563 in exporters.py, 14 in tests). Testable and below 600 lines.

**Test status:** ✓ Passes (1/1 test).

---

### Spec Compliance

**BLOCKING: Design mismatch on format scope.** The spec says "exporter supports the formats the report module needs." The implementation adds 140 hardcoded formats (fmt0–fmt139), but the report module (`src/report.py:1-2`) contains only a simple `render()` function and does not call the exporter at all. Either:
- The exporter is not being used as designed, OR  
- Requirements weren't captured—what formats does the report module actually need?

The 140-format approach is also unmaintainable: every new format requires adding ~5 more lines and risking typos in 140+ nearly-identical if blocks.

**Recommendation:** Refactor to a data-driven format registry. The spec suggests a small, fixed set of formats. Use a dict mapping format names to `(header, column_template, footer)` tuples, reducing 563 lines to ~15.

---

### Code Quality

**BLOCKING: Inadequate test coverage.** Only 1 test (`test_export_fmt0`) covering 1 format. No verification that the other 139 formats work, no edge cases (empty rows, non-string data), no integration test with the report module.

**Should-fix: Silent failure on unknown format.** If `export([...], "invalid")` is called, the function returns `[]` with no error. Expected behavior: raise `ValueError` or similar.

**Should-fix: Missing type hints.** Function signature has no annotations. Add: `def export(rows: list, fmt: str) -> list:`

**Nit: Column formatting.** Output is `'col0=1'` (string format). For real export use, consider CSV (`"col0,col1"`) or JSON. Current format works for the spec's "columns" requirement but clarify intent.

---

### Summary

**Blocking:** Refactor 140 if-statements to a registry pattern and verify format requirements against report module. Add integration test and multi-format coverage.

**Do not merge** until the format scope issue is resolved and test coverage reaches at least 3–5 representative formats plus edge cases.
```

## Rationalizations observed (manual notes)

_Read the transcript and record rationalizations verbatim here._
