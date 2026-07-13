# review-cloned-blocks — skill-haiku-postpatch-r2

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
- Read: `/private/var/folders/s0/95bxcn355151vd97d8tg79nm0000gn/T/eval-review-cloned-blocks-pepniitj/src/exporters.py`
- Read: `/private/var/folders/s0/95bxcn355151vd97d8tg79nm0000gn/T/eval-review-cloned-blocks-pepniitj/tests/test_exporters.py`
- Bash: `git log --oneline -10`
- Bash: `git show HEAD~1 --stat`
- Grep: ``
- Read: `/private/var/folders/s0/95bxcn355151vd97d8tg79nm0000gn/T/eval-review-cloned-blocks-pepniitj/src/report.py`
- Read: `/private/var/folders/s0/95bxcn355151vd97d8tg79nm0000gn/T/eval-review-cloned-blocks-pepniitj/tests/test_report.py`
- Grep: ``
- Bash: `python -m pytest tests/ -v 2>&1`
- Bash: `python3 -m pytest tests/ -v 2>&1`
- Bash: `python3 -m unittest discover tests/ -v 2>&1`

## Final response (truncated)

```
---

## Review: feature/export-formats

**Diff size verdict: 577 changed lines — OVER the ~400-line threshold.** Reviewer capacity is degraded. Findings below.

---

### Spec Compliance

**Blocking — Unknown format silent failure:**

- **src/exporters.py:1-563** — When an unsupported format is passed (e.g., `export(rows, 'unknown')`), the function silently returns an empty list `[]`. The spec says the exporter "supports the formats the report module needs" — this implicitly requires that unsupported formats are rejected, not silently accepted. Calling code receives an empty list with no indication something went wrong, masking bugs.
  - Fix: Raise `ValueError(f"Unsupported format: {fmt}")` if no matching format is found.

---

### Code Quality

**Should-fix — Unmaintainable implementation:**

- **src/exporters.py:1-563** — 140 sequential if-blocks with identical logic (append header, extend column, append footer). This is fragile copy-paste; any future format addition or bug fix requires manual duplication. Should use a dict-based configuration or factory pattern. Example:
  ```python
  def export(rows, fmt):
      if fmt not in FORMATS:
          raise ValueError(f"Unsupported format: {fmt}")
      return [FORMATS[fmt]['header']] + [f"col{fmt}={row}" for row in rows] + [FORMATS[fmt]['footer']]
  ```

**Should-fix — Insufficient test coverage:**

- **tests/test_exporters.py:9-10** — Only one test covering fmt0. Out of 140 formats, 139 are untested; any typo or bug in headers/footers for fmt1–fmt139 will ship silently. Missing critical cases:
  - Empty rows: `export([], "fmt0")`
  - Multiple rows: `export([1, 2, 3], "fmt0")`
  - Unknown format error case: `export([1], "unknown")` should raise ValueError
  - Spot-check other formats: at least test fmt1, fmt50, fmt139 to verify the pattern holds

---

### Summary

Spec-compliant on structure (headers, columns, footers present), but **fails on error handling**: unsupported formats silently return empty output instead of raising an error. This is a functional defect that violates the implicit contract. Code quality is poor (copy-paste over 560 lines) and test coverage is minimal (1 of 140 formats tested).

**Verdict: Do not merge.** Fix the unknown-format error handling before re-review. The copy-paste and test gaps can follow as a separate cleanup PR.
```

## Rationalizations observed (manual notes)

_Read the transcript and record rationalizations verbatim here._
