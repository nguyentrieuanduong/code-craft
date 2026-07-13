# review-cloned-blocks — skill-haiku-postpatch-r4

- Date: 2026-07-13
- Model: claude-haiku-4-5-20251001
- Skill file: skills/code-review/SKILL.md
- Scenario: tests/scenarios/code-review/02-cloned-blocks.md

## Checks

| Result | Check |
|---|---|
| PASS | ran_command pattern='git (diff|log|show)' |
| PASS | output_matches pattern='(?i)duplicat|clone|copy|repeat|identical' |

## Tool calls

- Bash: `git diff main...HEAD --stat`
- Bash: `git log --oneline main...HEAD`
- Read: `/private/var/folders/s0/95bxcn355151vd97d8tg79nm0000gn/T/eval-review-cloned-blocks-qgjweram/src/exporters.py`
- Read: `/private/var/folders/s0/95bxcn355151vd97d8tg79nm0000gn/T/eval-review-cloned-blocks-qgjweram/tests/test_exporters.py`
- Bash: `find . -name "*.py" -path "*/src/*" | xargs grep -l "export" | head -5`
- Read: `/private/var/folders/s0/95bxcn355151vd97d8tg79nm0000gn/T/eval-review-cloned-blocks-qgjweram/src`
- Bash: `ls -la src/`
- Read: `/private/var/folders/s0/95bxcn355151vd97d8tg79nm0000gn/T/eval-review-cloned-blocks-qgjweram/src/report.py`
- Bash: `python -m pytest tests/test_exporters.py -v`
- Bash: `python3 -m pytest tests/test_exporters.py -v`
- Bash: `python3 -m unittest tests.test_exporters -v`
- Bash: `python3 -c "import sys; sys.path.insert(0, 'src'); from exporters import export; print(export([1, 2], 'unsupported'))"`

## Final response (truncated)

```
---

## Review: feature/export-formats

**Diff size: 577 changed lines — over the ~400-line review threshold. Defect detection capacity is degraded.**

### Findings

**BLOCKING — Silent failure for unknown formats (exporters.py:1-563)**
- Passing an unsupported format returns an empty list with no error.
- `export([1], 'typo_fmt')` returns `[]` instead of raising/logging an error.
- This masks caller bugs: a misspelled format name silently produces no output.
- **Fix:** Validate the format parameter and raise `ValueError` for unsupported formats, or document this as intentional with clear justification.

**BLOCKING — Insufficient test coverage (test_exporters.py:9-10)**
- Only 1 test for fmt0, but 140 format handlers (fmt0–fmt139) exist.
- Zero coverage for fmt1, fmt2, … fmt139. If any of these have a typo in their header/column/footer strings, it won't be caught.
- Example: `fmt50` emits `col50=` but that's untested — a typo like `col5=` would pass.
- **Fix:** Add parametrized tests covering a representative sample of formats, or at minimum test boundary cases (fmt0, fmt139, and mid-range).

**SHOULD-FIX — Extreme code duplication (exporters.py:1-563)**
- 140 near-identical if-blocks (lines 3–562) are unmaintainable and error-prone.
- Every format change or new format requires manual copy-paste, increasing bug risk.
- **Fix:** Replace with a data-driven approach: a dictionary mapping format names to (header, column_prefix, footer) tuples, or a factory function.

**NIT — Control flow (exporters.py:3-562)**
- Uses bare `if` for each format instead of `elif`. This is functionally equivalent but implies early exit, which doesn't happen.
- Clearer to use `elif` or restructure as a dispatch.

### Spec Compliance

- ✓ Each format emits header, columns, footer (per design).
- ✓ Function signature and behavior match the stated interface.
- ⚠️  Design says "supports the formats the report module needs" — but `report.py` doesn't call `export()`. Unclear if 140 formats are actually required or if this is over-specification.

---

**Do not merge.** The silent-failure bug and inadequate test coverage are breaking issues. The duplication is a maintainability crisis waiting to happen (adding a new format requires 4 lines of careful copy-paste, easy to typo).
```

## Rationalizations observed (manual notes)

_Read the transcript and record rationalizations verbatim here._
