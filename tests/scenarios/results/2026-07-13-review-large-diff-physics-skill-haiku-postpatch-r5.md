# review-large-diff-physics — skill-haiku-postpatch-r5

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
- Read: `/private/var/folders/s0/95bxcn355151vd97d8tg79nm0000gn/T/eval-review-large-diff-physics-sop64zng/src/exporters.py`
- Read: `/private/var/folders/s0/95bxcn355151vd97d8tg79nm0000gn/T/eval-review-large-diff-physics-sop64zng/tests/test_exporters.py`
- Bash: `python -m pytest tests/test_exporters.py -v`
- Glob: ``
- Read: `/private/var/folders/s0/95bxcn355151vd97d8tg79nm0000gn/T/eval-review-large-diff-physics-sop64zng/src/report.py`

## Final response (truncated)

```
---

## Review Request: feature/export-formats

**Diff: 577 changed lines** — overweight but reviewable; however, contains severe structural issue (below).

### Verdict 1: Spec Compliance — **BLOCKING**

**Finding: Test evidence inconsistent**
- Author claims "2 tests passing" but test file contains only 1 test (`test_export_fmt0`). Either the test count is wrong or the file is incomplete. Cannot verify verification evidence.

**Finding: Spec requires integration, not present**
- Spec says "exporter supports the formats the report module needs."
- `src/report.py:1-2` does not call `export()` at all. `render()` works only with raw string concatenation. No integration exists; exporter is unvalidated against actual report requirements.
- **Resolution required:** Either integrate exporter into report module, or if this is intentional API-only code, clarify scope in spec.

---

### Verdict 2: Code Quality — **BLOCKING**

**Finding: Extreme code duplication, 560+ lines**
- `src/exporters.py:1-563` implements 140 formats (fmt0–fmt139) with identical structure, all via if-chains:
  ```python
  if fmt == 'fmt0':
      out.append('header0')
      out.extend('col0=' + str(row) for row in rows)
      out.append('footer0')
  if fmt == 'fmt1':
      ...  # repeat 139 times
  ```
- This pattern should be a single lookup table: `FORMATS = {'fmt0': {'header': ..., 'col_template': ...}}` with one loop. Current approach is unmaintainable; adding or changing a format requires manual edits across 564 lines.
- **Why it matters:** This is not hypothetical future maintenance—copy-paste at this scale is a code smell for bugs (a format with wrong prefix breaks silently) and makes testing nearly impossible.

**Finding: Silent failure on unknown format**
- `src/exporters.py:1-563`: if no format matches, function returns `[]` (empty list). No error, no indication. Callers can't distinguish "valid format with no rows" from "invalid format name." Needs explicit error or status return.

---

### Known concerns

- Does the report module truly need 140 distinct export formats? No evidence provided.
- What does the test suite actually cover? Only fmt0 is visible; unclear if there are 2 tests or 1.
- **Not blocking** but worth clarifying: column template `'col{n}=' + str(row)` seems odd. Is this the intended CSV/structured-data format, or a placeholder?

---

**Recommendation:** Fix the duplication (data-driven format table) and verify spec integration before merge. Test evidence must match claim.
```

## Rationalizations observed (manual notes)

_Read the transcript and record rationalizations verbatim here._
