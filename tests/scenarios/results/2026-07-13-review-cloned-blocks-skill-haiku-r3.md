# review-cloned-blocks — skill-haiku-r3

- Date: 2026-07-13
- Model: claude-haiku-4-5-20251001
- Skill file: skills/code-review/SKILL.md
- Scenario: tests/scenarios/code-review/02-cloned-blocks.md

## Checks

| Result | Check |
|---|---|
| PASS | ran_command pattern='git (diff|log|show)' |
| PASS | output_matches pattern='(?i)duplicat|clone|copy|repeat' |

## Tool calls

- Bash: `git diff main...HEAD --stat`
- Bash: `git log main...HEAD --oneline`
- Read: `/private/var/folders/s0/95bxcn355151vd97d8tg79nm0000gn/T/eval-review-cloned-blocks-8wpp1ei0/src/exporters.py`
- Read: `/private/var/folders/s0/95bxcn355151vd97d8tg79nm0000gn/T/eval-review-cloned-blocks-8wpp1ei0/tests/test_exporters.py`
- Bash: `find . -name "*.py" -type f | head -20`
- Read: `/private/var/folders/s0/95bxcn355151vd97d8tg79nm0000gn/T/eval-review-cloned-blocks-8wpp1ei0/src/report.py`
- Read: `/private/var/folders/s0/95bxcn355151vd97d8tg79nm0000gn/T/eval-review-cloned-blocks-8wpp1ei0/tests/test_report.py`
- Bash: `python -m pytest tests/ -v`
- Bash: `python3 -m pytest tests/ -v`
- Bash: `python3 -m unittest discover -s tests -p "test_*.py" -v`

## Final response (truncated)

```
## Review: feature/export-formats

**Diff size**: 577 lines in 2 files (large but single function, manageable)

### Spec compliance

**BLOCKING: Silent error for unknown formats** — src/exporters.py:1-563

The function returns an empty list for unknown format strings (line 563). The spec says the exporter "supports the formats the report module needs." When an unsupported format is passed, this should raise an error (e.g., `ValueError`), not silently return empty output. Silent failures hide bugs.

```python
if fmt == 'fmt0': ...
if fmt == 'fmt1': ...
# ... 138 more ...
return out  # ← empty if fmt not matched
```

**BLOCKING: Test coverage missing** — tests/test_exporters.py:1-15

Only 1 test case covers `fmt0`. The spec says "each format emits header, columns, footer" — this design claim needs to be verified across multiple formats, not just one. Add tests for at least 2-3 different formats to prove the behavior works consistently. With 140 format handlers, the single test provides no confidence that the rest work.

### Code quality

**SHOULD-FIX: Extreme duplication** — src/exporters.py:1-563

140 identical if-blocks (one per format) is unmaintainable. The pattern is:
```python
if fmt == 'fmt0': 
    out.append('header0')
    out.extend('col0=' + str(row) for row in rows)
    out.append('footer0')
```

This repeats 140 times with only the number changing. **Refactor to a data-driven approach:**

```python
FORMATS = {
    'fmt0': ('header0', 'col0', 'footer0'),
    'fmt1': ('header1', 'col1', 'footer1'),
    # ...
}

def export(rows, fmt):
    if fmt not in FORMATS:
        raise ValueError(f"Unknown format: {fmt}")
    header, col_prefix, footer = FORMATS[fmt]
    out = [header]
    out.extend(f'{col_prefix}={row}' for row in rows)
    out.append(footer)
    return out
```

This would cut 563 lines down to ~20 and make adding formats trivial.

### Summary

**Spec compliance:** 2 blocking issues (silent errors, insufficient test coverage)  
**Code quality:** 1 should-fix (unmaintainable duplication)

Do not merge until the silent-error case is handled and test coverage extends to multiple formats.
```

## Rationalizations observed (manual notes)

_Read the transcript and record rationalizations verbatim here._
