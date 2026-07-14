# review-cloned-blocks — baseline-haiku-base-r2

- Date: 2026-07-14
- Model: claude-haiku-4-5-20251001
- Skill file: none (baseline)
- Scenario: tests/scenarios/code-review/02-cloned-blocks.md

## Checks

| Result | Check |
|---|---|
| PASS | ran_command pattern='git (diff|log|show)' |
| PASS | output_matches pattern='(?i)duplicat|clone|copy|repeat|identical' |

## Tool calls

- Skill: ``
- Bash: `gh pr list`
- Bash: `git log --oneline -10`
- Bash: `git diff main...feature/export-formats --stat`
- Bash: `git diff main...feature/export-formats`
- Bash: `git show 9741714:src/report.py | head -100`
- Bash: `grep -r "export(" --include="*.py" . | grep -v ".git" | grep -v "test_"`

## Final response (truncated)

```
## Review: feature/export-formats

**Status: ❌ BLOCKING — Do not merge**

### Overview
The branch adds a multi-format exporter as specified in the approved design. However, the implementation uses massive code duplication (140+ identical if statements) instead of a data-driven approach, making it unmaintainable and violating core software engineering principles.

### Critical Issues

**1. Severe Code Duplication**
- 563 lines of `export()` function contain 140 nearly-identical if statements (fmt0 through fmt139)
- Each block differs only in the format name and header/footer text
- Any bug in the export logic requires fixing 140+ identical places
- This is a maintenance nightmare waiting to happen

**2. No Data-Driven Design**
The code should use a dictionary to define formats:
```python
FORMATS = {f'fmt{i}': (f'header{i}', f'col{i}', f'footer{i}') for i in range(140)}

def export(rows, fmt):
    if fmt not in FORMATS:
        return []
    header, col_prefix, footer = FORMATS[fmt]
    out = [header]
    out.extend(f'{col_prefix}={row}' for row in rows)
    out.append(footer)
    return out
```
This is ~10 lines instead of 563.

**3. Inadequate Test Coverage**
- Only one test case (fmt0)
- No validation that other 139 formats work
- No edge cases tested (empty rows, invalid format, etc.)

**4. Design Disconnect**
The approved design said "exporter supports the **formats the report module needs**" — yet:
- 140 formats are implemented with no indication which are actually used
- Only fmt0 is tested
- No integration with the report module shown
- This suggests scope creep or misunderstanding of requirements

### Ask Before Merge
- **What formats does the report module actually need?** (likely far fewer than 140)
- **Is this over-engineered?** If only a handful of formats are needed, implement only those.
- **Can you refactor to data-driven design** to eliminate the duplication?
- **Add tests for all supported formats** and edge cases (empty rows, invalid fmt).
```

## Rationalizations observed (manual notes)

_Read the transcript and record rationalizations verbatim here._
