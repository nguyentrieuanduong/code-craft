# review-large-diff-physics — skill-haiku-round2-r2

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
- Bash: `git log main...HEAD --oneline`
- Read: `/private/var/folders/s0/95bxcn355151vd97d8tg79nm0000gn/T/eval-review-large-diff-physics-nyy9dc1u/src/exporters.py`
- Read: `/private/var/folders/s0/95bxcn355151vd97d8tg79nm0000gn/T/eval-review-large-diff-physics-nyy9dc1u/tests/test_exporters.py`
- Bash: `git show HEAD:src/report.py | head -50`
- Bash: `git show HEAD --format=%B | head -20`

## Final response (truncated)

```
## Review request: feature/export-formats

**Diff:** 577 changed lines — at the upper end of the ~400-line comfortable review threshold due to massive code duplication

---

## Verdict 1: Spec Compliance — **BLOCKED**

The spec says "exporter supports the formats the report module needs; each format emits header, columns, footer."

**Functionally compliant**: Each format does emit header, columns, footer as required.

**Scope concern**: The implementation provides 139 hardcoded formats (fmt0 through fmt139), but the report module shown doesn't indicate it needs that many. The design doesn't justify why 139 formats exist or how they're chosen. This violates the "supports what the report module needs" constraint—either this is over-engineered, or the format requirements are not documented.

---

## Verdict 2: Code Quality — **BLOCKING**

**Finding 1: Massive code duplication (Blocking)**  
Lines 3–402 repeat the same pattern 140 times:
```python
if fmt == 'fmt{N}':
    out.append('header{N}')
    out.extend('col{N}=' + str(row) for row in rows)
    out.append('footer{N}')
```
This is generated-code duplication (pattern repeats 139 times with only the number N changing). Should be collapsed to a single table + loop:
```python
FORMATS = {fmt: {'num': i} for i, fmt in enumerate(['fmt0', 'fmt1', ...])}
def export(rows, fmt):
    if fmt not in FORMATS:
        raise ValueError(f"Unknown format: {fmt}")
    n = FORMATS[fmt]['num']
    out = [f'header{n}']
    out.extend(f'col{n}={row}' for row in rows)
    out.append(f'footer{n}')
    return out
```

**Finding 2: Silent failure on invalid format (Blocking)**  
Lines 1–563: If `fmt` doesn't match any condition, returns an empty list. Should raise `ValueError` for unknown formats—callers can't distinguish between "no output" and "invalid format." This hides bugs.

**Finding 3: Uses `if` instead of `elif` (Should-fix)**  
Lines 3–402: All conditions are independent `if` statements, not `elif`. If somehow multiple formats matched, multiple blocks would execute. Use `elif` or `match` to make intent clear.

**Finding 4: Test coverage insufficient (Should-fix)**  
tests/test_exporters.py defines only 1 test (`test_export_fmt0`), but verification says "2 tests passing." Missing coverage for:
- Multiple formats (to confirm they don't interfere)
- Empty rows edge case
- Invalid format (should raise, not silently return `[]`)
- Data type diversity in rows

---

**Known concerns from author**: Not addressed in submission.
```

## Rationalizations observed (manual notes)

_Read the transcript and record rationalizations verbatim here._
