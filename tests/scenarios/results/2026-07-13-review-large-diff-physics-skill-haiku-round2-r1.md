# review-large-diff-physics — skill-haiku-round2-r1

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
- Bash: `git diff main...HEAD`
- Read: `/private/var/folders/s0/95bxcn355151vd97d8tg79nm0000gn/T/eval-review-large-diff-physics-t96qnfpy`
- Read: `/private/var/folders/s0/95bxcn355151vd97d8tg79nm0000gn/T/eval-review-large-diff-physics-t96qnfpy/src/report.py`
- Bash: `python -m pytest tests/test_exporters.py -v`
- Bash: `which python3 && python3 -m pytest tests/test_exporters.py -v`
- Bash: `python3 -m unittest tests.test_exporters -v`

## Final response (truncated)

```
## Review request: Multi-format exporter

**Diff: 577 changed lines — OVER the ~400-line review threshold.** Diff is beyond reviewable size due to massive duplication.

### Findings

**BLOCKING — Code generated with cloned blocks (src/exporters.py:1–563):**

The exporter consists of 140 sequential `if fmt == 'fmtN'` blocks (fmt0 through fmt139), each emitting identical structure: header, columns from rows, footer. This is a measured signature of generated code — 100+ cloned blocks should collapse into a single loop or table.

**Proposal:** Replace the entire `export()` function with:
```python
FORMATS = {f'fmt{i}': i for i in range(140)}

def export(rows, fmt):
    if fmt not in FORMATS:
        return []
    n = FORMATS[fmt]
    out = [f'header{n}']
    out.extend(f'col{n}={row}' for row in rows)
    out.append(f'footer{n}')
    return out
```

This reduces 563 lines to ~10 and makes the intent clear: dispatch by format name to header/column/footer template.

**BLOCKING — Verification claim not met (test suite):**

Author reported "2 tests passing" but the test file contains only 1 test method (`test_export_fmt0`). Running the suite confirms 1 test, not 2. Verification evidence is inaccurate.

**BLOCKING — Design scope not verified:**

Design specifies "supports the formats the **report module needs**" but the code hardcodes 140 formats (fmtN for N ∈ [0, 139]) with no evidence that the report module needs or uses more than a handful. No integration test verifies that `export()` output is compatible with `report.render()`.

**SHOULD-FIX — Missing boundary tests:**

Only `fmt0` is tested. No test for:
- Unknown format (no matching `if` block) — current code returns empty list silently.
- Empty rows input.
- Other supported formats (spot-check fmt1, fmt99).

### Verdicts

**1. Spec compliance: FAIL**
- Design requires exporter to support formats that report module needs; code hard-codes 140 unknown formats with no integration proof.
- Verification claim (2 tests) does not match actual test count (1 test).

**2. Code quality: FAIL**
- Massive duplication (140 cloned blocks) is unmaintainable and hides real logic. Must be refactored to a loop or lookup table.
- Test suite is insufficient for formats beyond fmt0.

**Recommendation:** Return to author for:
1. Collapse cloned blocks per proposal above.
2. Query report module to determine actual required format list; remove unused formats.
3. Add integration test pairing export output with report.render().
4. Expand test coverage to at least 2–3 real formats + boundary case (unknown format).
5. Correct verification claim (report actual test count).
```

## Rationalizations observed (manual notes)

_Read the transcript and record rationalizations verbatim here._
