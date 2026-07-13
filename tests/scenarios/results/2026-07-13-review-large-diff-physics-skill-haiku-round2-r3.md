# review-large-diff-physics — skill-haiku-round2-r3

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
- Bash: `git log main...HEAD --oneline`
- Bash: `python -m pytest tests/test_exporters.py -v`
- Bash: `python3 -m pytest tests/test_exporters.py -v`
- Bash: `python3 -m unittest tests.test_exporters -v`
- Glob: ``
- Read: `/private/var/folders/s0/95bxcn355151vd97d8tg79nm0000gn/T/eval-review-large-diff-physics-9tq6hdkw/src/report.py`
- Read: `/private/var/folders/s0/95bxcn355151vd97d8tg79nm0000gn/T/eval-review-large-diff-physics-9tq6hdkw/tests/test_report.py`

## Final response (truncated)

```
## Review request: Multi-format exporter

**Diff size: 577 changed lines — OVER the ~400-line review threshold.** This diff should be split. Beyond ~400 lines, reviewer defect detection collapses. Continue with this review, but note the size verdict upfront.

---

### Spec Compliance — BLOCKING

The design specifies "exporter supports the formats the report module needs; each format emits header, columns, footer."

**Missing: Which formats does the report module actually need?**
- `report.py` does not call the exporter; no integration exists (src/report.py:1–2)
- The exporter supports 140 formats (fmt0–fmt139), but there's no evidence the report module needs any of them
- Claim verification fails: cannot confirm spec compliance without knowing the required formats

**Claim discrepancy**: Author stated "2 tests passing," but:
- Test diff contains only 1 test (test_export_fmt0)
- Test run shows 1 test executed
- 2 ≠ 1; verify what the actual test count is

**Blocking finding**: Spec compliance cannot be verified. Design must clarify which formats are required, and the code must integrate with or be validated against the report module.

---

### Code Quality — BLOCKING

**Massive code duplication** (src/exporters.py:1–563): The same 4-line block repeats 140 times with only the number changing. This is the measured signature of generated code.

```python
# Appears 140 times, pattern identical except number:
if fmt == 'fmt0':
    out.append('header0')
    out.extend('col0=' + str(row) for row in rows)
    out.append('footer0')
if fmt == 'fmt1':
    # ... same pattern, different number
```

This can collapse to a dict + loop. Example:

```python
FORMATS = {
    'fmt0': 'header0',
    'fmt1': 'header1',
    # ... etc
}

def export(rows, fmt):
    if fmt not in FORMATS:
        raise ValueError(f"Unknown format: {fmt}")
    out = [FORMATS[fmt]]
    out.extend(f'col{fmt[-1]}={row}' for row in rows)
    out.append(f'footer{fmt[-1]}')
    return out
```

**Blocking finding**: Refactor to eliminate duplication. 140 copy-pasted blocks are unmaintainable and violate basic coding standards.

**Should-fix**: Silent failure on unknown format. If `fmt` doesn't match any condition, the function returns `[]` with no error signal (src/exporters.py:1–563). Add validation:

```python
if fmt not in FORMATS:
    raise ValueError(f"Unknown format: {fmt}")
```

---

### Verdict

- **Spec compliance**: BLOCKED — clarify which formats are required and integrate with report module
- **Code quality**: BLOCKED — refactor to remove 140-line duplication; add error handling for invalid formats

Do not merge until both blockers are resolved.
```

## Rationalizations observed (manual notes)

_Read the transcript and record rationalizations verbatim here._
