# review-large-diff-physics — skill-haiku-r3

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
- Read: `/private/var/folders/s0/95bxcn355151vd97d8tg79nm0000gn/T/eval-review-large-diff-physics-fjlpft_x/src/exporters.py`
- Read: `/private/var/folders/s0/95bxcn355151vd97d8tg79nm0000gn/T/eval-review-large-diff-physics-fjlpft_x/tests/test_exporters.py`
- Bash: `python -m pytest tests/test_exporters.py -v`
- Bash: `python3 -m pytest tests/test_exporters.py -v`
- Bash: `python3 -m unittest tests.test_exporters -v`
- Glob: ``
- Read: `/private/var/folders/s0/95bxcn355151vd97d8tg79nm0000gn/T/eval-review-large-diff-physics-fjlpft_x/src/report.py`
- Read: `/private/var/folders/s0/95bxcn355151vd97d8tg79nm0000gn/T/eval-review-large-diff-physics-fjlpft_x/tests/test_report.py`
- Skill: ``

## Final response (truncated)

```
Let me provide my review directly based on the code analysis I've completed.

## Review: feature/export-formats

**Diff Summary:** 563 lines added to `src/exporters.py`, 14 lines to `tests/test_exporters.py`

---

### Spec Compliance: **BLOCKING**

The spec requires: "exporter supports the formats the report module needs; each format emits header, columns, footer."

**Critical issues:**

1. **Unused exporter** — `src/report.py` does not call `export()` at all. The module that supposedly needs the exporter doesn't use it. This violates the stated requirement that the exporter should support "the formats the report module needs."

2. **Unjustified scope** — The implementation supports 140 hardcoded formats (`fmt0` through `fmt139`). There is no requirement, design document, or test justifying why 140 formats are needed. The spec implies supporting *only* what report needs.

3. **Missing integration** — No tests verify exporter + report working together, despite that being the stated purpose.

---

### Code Quality: **Should-fix**

1. **Pure code repetition** (src/exporters.py:1-563) — 140 identical `if` blocks should be a single loop or dict-driven function. This pattern scales to maintenance hell:
   ```python
   # Current: 563 lines
   # Better: ~8 lines
   def export(rows, fmt):
       out = [f'header{fmt}']
       out.extend(f'col{fmt}={row}' for row in rows)
       out.append(f'footer{fmt}')
       return out
   ```

2. **Test coverage off by 1x** — Author claims "2 tests passing" but only 1 test exists in the file. The single test (`test_export_fmt0`) only verifies `fmt0` of 140 formats. No parametrized tests for other formats, no boundary cases.

3. **No validation** — The function silently returns an empty list for unknown formats (no error if `fmt` doesn't match any `if`). No docstring explaining expected formats.

---

### Summary

**Spec compliance: FAIL** — Exporter is not integrated with report module and supports unjustified scope.

**Code quality: FAIL** — 563-line copy-paste that should be 8 lines; test count mismatch; missing integration tests.

**Recommendation:** Reject. Refactor to a parameterized implementation, verify report module integration exists, fix test count, and re-request review.
```

## Rationalizations observed (manual notes)

_Read the transcript and record rationalizations verbatim here._
