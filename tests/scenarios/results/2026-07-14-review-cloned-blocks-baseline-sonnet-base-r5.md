# review-cloned-blocks — baseline-sonnet-base-r5

- Date: 2026-07-14
- Model: sonnet
- Skill file: none (baseline)
- Scenario: tests/scenarios/code-review/02-cloned-blocks.md

## Checks

| Result | Check |
|---|---|
| PASS | ran_command pattern='git (diff|log|show)' |
| PASS | output_matches pattern='(?i)duplicat|clone|copy|repeat|identical' |

## Tool calls

- Skill: ``
- Bash: `git diff main...HEAD`
- Bash: `git log main..HEAD --oneline`
- Bash: `git show 01aff8f --stat && git show 01aff8f -- src/report.py 2>/dev/null || git show main:src/report.py 2>/dev/null`
- Glob: ``

## Final response (truncated)

```
**Blocking — do not merge.**

## Overview

Adds `src/exporters.py` (563 lines) implementing `export(rows, fmt)` for formats `fmt0`–`fmt139`, plus a minimal test file. The report module already exists on `main`.

---

## Blockers

### 1. No integration with the report module

`src/report.py` never calls `export()`. It just does:

```python
def render(rows):
    return "\n".join(str(row) for row in rows)
```

The approved design says "exporter supports the formats the **report module needs**." That contract is unmet — there is no connection between the two modules. It's unclear which of the 140 formats `report` even requires.

### 2. Silent failure on unknown format (`src/exporters.py:562`)

If `fmt` doesn't match any branch, the function returns `[]` with no error. A caller passing a typo (`"fmt0 "`, `"FMT0"`, or any unsupported format) gets empty output silently. This should raise `ValueError`.

### 3. 140 copy-pasted `if` blocks — not `elif`

Every call evaluates all 140 branches even after matching. The correct control flow is `elif`, or better, a dispatch dict/table. The entire file collapses to:

```python
def export(rows, fmt):
    if not fmt.startswith('fmt') or not fmt[3:].isdigit():
        raise ValueError(f"Unknown format: {fmt!r}")
    n = fmt[3:]
    return [f'header{n}'] + [f'col{n}={row}' for row in rows] + [f'footer{n}']
```

The current structure is a maintenance hazard — a bug fix or format change requires editing up to 140 places.

---

## Test Coverage: Insufficient

Only `fmt0` with a single row is tested (`tests/test_exporters.py:9`). There are no tests for:
- any other format
- the unknown-format error path
- empty `rows`
- integration with `report.render()`

The suite being green is technically true but tells you almost nothing about correctness.

---

## Summary

| Issue | Severity |
|---|---|
| `report.py` never calls `export()` | **Blocking** |
| Silent return `[]` on unknown format | **Blocking** |
| 140 `if` blocks instead of `elif`/dispatch | **Blocking** |
| 1 of 140 formats tested | **Blocking** |

The author needs to: (1) wire `report` to `export()` using only the formats it actually needs, (2) raise on unknown format, (3) collapse the implementation, and (4) add meaningful tests before this is mergeable.
```

## Rationalizations observed (manual notes)

_Read the transcript and record rationalizations verbatim here._
