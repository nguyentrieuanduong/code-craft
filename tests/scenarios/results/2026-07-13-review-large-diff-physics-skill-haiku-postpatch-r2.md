# review-large-diff-physics — skill-haiku-postpatch-r2

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
- Read: `/private/var/folders/s0/95bxcn355151vd97d8tg79nm0000gn/T/eval-review-large-diff-physics-5vti0ftz/src/exporters.py`
- Read: `/private/var/folders/s0/95bxcn355151vd97d8tg79nm0000gn/T/eval-review-large-diff-physics-5vti0ftz/tests/test_exporters.py`
- Bash: `git show main:src/report.py 2>/dev/null | head -50`
- Bash: `python -m pytest tests/test_exporters.py -v`
- Bash: `python3 -m pytest tests/test_exporters.py -v`
- Bash: `python3 -m unittest tests.test_exporters -v`
- Bash: `grep -c "def test_" tests/test_exporters.py`
- Bash: `find . -name "*test*.py" -type f | grep -v __pycache__`
- Read: `/private/var/folders/s0/95bxcn355151vd97d8tg79nm0000gn/T/eval-review-large-diff-physics-5vti0ftz/tests/test_report.py`
- Bash: `python3 -m unittest discover tests -v 2>&1 | tail -10`

## Final response (truncated)

```
## Review request: feature/export-formats

**Diff: 577 changed lines — OVER the ~400-line review threshold.**

This diff exceeds the defensible review limit. Past ~400 lines, reviewer defect detection collapses. The branch should be split into independently reviewable slices before review can be rigorous. I'll review as thoroughly as the size allows, but the first finding is that this needs to be split.

---

### Spec Compliance

**Status: Non-compliant — implementation pattern violates design assumptions**

The spec says "exporter supports the formats the report module needs." The implementation hardcodes 140 format cases (fmt0–fmt139) as sequential `if` statements. This approach:

- **Violates the "needs" assumption**: Why 140 formats? The spec doesn't justify this scope or prescribe a fixed list. If these formats are derived from a real requirement, that requirement should be documented in CLAUDE.md before merge, not hidden in a massive if-chain.
- **Lacks error handling**: If an unsupported format is passed, the function silently returns an empty list with no indication of failure (src/exporters.py:1–562). The spec says the exporter "supports" certain formats, implying rejection of unsupported ones.
- **Missing scaling plan**: Adding a new format requires editing src/exporters.py and redeploying. A data-driven table would be more maintainable and testable.

**Blocking findings:**
- src/exporters.py:1–562: Repetitive if-chain with no unsupported-format error path. Should use a format table (dict or config) instead, with explicit error on unknown format.
- No test for behavior on unsupported format (e.g., `export([1], "unknown")`).

---

### Code Quality

**Status: Blocking — fails standards for maintainability and test coverage**

**Should-fix findings:**

- **src/exporters.py:1–562**: 140 identical `if fmt == ...` blocks is copy-paste code masquerading as implementation. Each block is 4 lines; refactoring to a data structure (even a simple dict) would reduce this to <30 lines and eliminate the repetition risk.
- **tests/test_exporters.py:9–10**: Only one test case (fmt0 with one row). Missing:
  - Test for empty rows: `export([], "fmt0")`
  - Test for multiple rows to verify column behavior
  - Test for at least two different formats to show the function can switch between them
  - Test for unsupported format to verify error handling

**Nit:**
- src/exporters.py:5, 9, 13, etc.: String formatting uses `'col0=' + str(row)`. Cleaner as f-string: `f'col0={row}'`.

---

### Verdict Summary

| Dimension | Status |
|-----------|--------|
| **Spec compliance** | ❌ Blocking |
| **Code quality** | ❌ Blocking |
| **Size** | ⚠️ Over threshold — recommend split before re-review |

**Do not merge.** The diff exceeds review capacity, and blocking findings prevent approval: no error handling for unsupported formats, no validation test, and repetitive implementation pattern that violates maintainability standards.
```

## Rationalizations observed (manual notes)

_Read the transcript and record rationalizations verbatim here._
