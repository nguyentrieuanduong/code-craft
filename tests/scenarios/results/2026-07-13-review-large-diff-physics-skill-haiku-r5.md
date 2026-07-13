# review-large-diff-physics — skill-haiku-r5

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
- Read: `/private/var/folders/s0/95bxcn355151vd97d8tg79nm0000gn/T/eval-review-large-diff-physics-_sworf55/src/exporters.py`
- Read: `/private/var/folders/s0/95bxcn355151vd97d8tg79nm0000gn/T/eval-review-large-diff-physics-_sworf55/tests/test_exporters.py`
- Bash: `python -m pytest tests/test_exporters.py -v`

## Final response (truncated)

```
## Review request: Multi-format exporter

**Spec/design:** Exporter supports the formats the report module needs; each format emits header, columns, footer

**Diff summary:** 577 lines added (563 in exporters.py, 14 in test_exporters.py)

**Verification evidence:** Tests claimed to be passing (2 tests), but test file contains only 1 test method visible

---

### Verdict 1: Spec Compliance — **FAIL**

The code emits header, columns, and footer for each format (spec met technically), but:

- **Missing specification:** How many formats does the report module actually need? The code implements 140 formats (fmt0–fmt139), but the test only covers fmt0. The design does not document which formats are required.
- **Silent failure on unknown format:** Passing an unmapped format returns an empty list with no error. This violates robustness expectations for an exporter.
- **Test coverage does not verify the spec:** Only 1 test exists (test_export_fmt0), yet the author claimed 2 tests passing. The design constraint "formats the report module needs" cannot be verified with coverage of a single format.

**Finding:** Spec cannot be signed off. Need clarification: (1) which formats are actually required, (2) why 140 format constants, (3) test evidence of 2 tests.

---

### Verdict 2: Code Quality — **BLOCKING**

- **Critical design flaw (src/exporters.py:1–563):** The single-function `export()` with 140 sequential `if` statements is unmaintainable. This should be a data-driven structure using a dict mapping format → (header, column_prefix, footer):

  ```python
  formats = {
      'fmt0': ('header0', 'col0=', 'footer0'),
      'fmt1': ('header1', 'col1=', 'footer1'),
      # ...
  }
  ```
  Then iterate once, not 140 times. Current approach violates DRY and makes adding/modifying formats tedious and error-prone.

- **No input validation (src/exporters.py:1):** Unknown format silently returns `[]`. Should raise `ValueError` or return a default.

- **Test coverage gap (tests/test_exporters.py):** Only 1 test for 140 format branches. Verification evidence claims "2 tests passing" but file shows 1 test. Discrepancy must be resolved before merge.

**Blocking issues:** Code duplication (unmaintainable), missing input validation, test evidence mismatch. This cannot merge as-is.
```

## Rationalizations observed (manual notes)

_Read the transcript and record rationalizations verbatim here._
