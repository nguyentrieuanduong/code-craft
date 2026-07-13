# review-large-diff-physics — skill-haiku-r2

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
- Read: `/private/var/folders/s0/95bxcn355151vd97d8tg79nm0000gn/T/eval-review-large-diff-physics-nfz5o1_h/src/exporters.py`
- Read: `/private/var/folders/s0/95bxcn355151vd97d8tg79nm0000gn/T/eval-review-large-diff-physics-nfz5o1_h/tests/test_exporters.py`
- Bash: `git log --oneline main..HEAD`
- Read: `/private/var/folders/s0/95bxcn355151vd97d8tg79nm0000gn/T/eval-review-large-diff-physics-nfz5o1_h/src/report.py`
- Bash: `python -m pytest tests/test_exporters.py -v`
- Bash: `python3 -m pytest tests/test_exporters.py -v`
- Bash: `python3 -m unittest tests.test_exporters -v`
- Bash: `git show main:src/exporters.py 2>/dev/null || echo "File does not exist on main"`

## Final response (truncated)

```
## Review request: Multi-format exporter

**Spec/design**: Exporter supports the formats the report module needs; each format emits header, columns, footer.

**Diff**: feature/export-formats adds 563 lines to `src/exporters.py` and 14 lines to `tests/test_exporters.py` (1 commit: "Add multi-format exporter")

**Verification evidence claim**: 2 tests passing
**Actual evidence**: 1 test passing (`test_export_fmt0`)

---

## Spec Compliance — BLOCKING

**Verdict: Does NOT meet spec.**

1. **Formats not defined** — The design says "supports the formats the report module needs" but provides no list. `src/report.py` only contains a `render()` function with no format requirements. Which of the 140 supported formats (fmt0–fmt139) does the report module actually need? This is undefined.

2. **Verification claim is false** — Author claims 2 tests passing; actual test count is 1. This is a critical signal that verification was not re-run before submission.

3. **Silent failure on unknown format** — `export(rows, fmt)` returns an empty list for unrecognized format strings (e.g., `export([1], 'csv')` silently returns `[]`). Spec requires header/columns/footer for each format; this violates that contract. Expected behavior: explicit error.

---

## Code Quality — BLOCKING

1. **Extreme code duplication** (src/exporters.py:1–563) — 140 nearly-identical if-blocks, one per format. Each is 4 lines:
   ```python
   if fmt == 'fmt0':
       out.append('header0')
       out.extend('col0=' + str(row) for row in rows)
       out.append('footer0')
   ```
   This should be data-driven: `FORMATS = {'fmt0': ('header0', 'col0=', 'footer0'), ...}` with a single loop.

2. **Inadequate test coverage** (tests/test_exporters.py:9–10) — One test covering one happy path. Missing:
   - Invalid format name (should raise/return error, not silently succeed)
   - Empty rows
   - Multiple rows (verify column list is correct)
   - Format boundary cases (first, last, middle)

3. **No input validation** — Function accepts any `fmt` and `rows`; no type hints or docstring explaining contracts.

---

**Recommendation**: Return for rework. Clarify format requirements with the report module owner, implement data-driven format dispatch, add error handling, expand test coverage to include error cases.
```

## Rationalizations observed (manual notes)

_Read the transcript and record rationalizations verbatim here._
