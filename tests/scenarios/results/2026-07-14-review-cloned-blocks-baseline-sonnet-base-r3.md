# review-cloned-blocks — baseline-sonnet-base-r3

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
- Glob: ``
- Read: `/private/var/folders/s0/95bxcn355151vd97d8tg79nm0000gn/T/eval-review-cloned-blocks-qszqlzgy/src/report.py`

## Final response (truncated)

```
**Yes, there are blocking issues. Do not merge.**

---

## Review: `feature/export-formats`

### What the PR does

Adds `src/exporters.py` with a single `export(rows, fmt)` function supporting `fmt0`–`fmt139` (140 formats), each emitting a header, column lines, and a footer. Adds one test.

---

### Blockers

**1. Massive copy-paste masquerading as implementation (`src/exporters.py:1–563`)**

All 140 blocks are structurally identical — only the number changes. This should be ~5 lines:

```python
def export(rows, fmt):
    n = fmt.removeprefix('fmt')
    return [f'header{n}'] + [f'col{n}={row}' for row in rows] + [f'footer{n}']
```

563 lines of duplication is not reviewable, maintainable, or extensible. This alone blocks merge.

**2. `if` chains instead of `elif` — all 140 conditions evaluated every call**

Every call to `export()` falls through all 140 `if` comparisons, even after a match. For a format like `fmt0`, Python still tests `fmt == 'fmt1'` through `fmt == 'fmt139'`. Use `elif` at minimum, or better, the data-driven approach above.

**3. Silent failure on unknown format**

If `fmt` doesn't match any branch, the function returns `[]` with no error. The caller gets empty output and no indication anything went wrong. An unknown format should raise `ValueError`.

**4. The report module doesn't use the exporter**

The approved design says "exporter supports the formats the report module needs." `src/report.py` has `render(rows)` which does `"\n".join(str(row) for row in rows)` — it never calls `export()`. The integration doesn't exist.

**5. Test suite is green but meaningless**

Only `fmt0` is tested out of 140 formats. "Suite green" is technically true, but the claim implies coverage it doesn't have. At minimum, test an unknown format raises an error and spot-check a high-numbered format.

---

### Summary

The core logic is correct in spirit (header/columns/footer per format), but the implementation approach is wrong, the error contract is missing, the report integration is absent, and the tests don't cover the surface area claimed. Please rewrite `exporters.py` with a parameterized approach, add the missing error handling, wire it into `report.py`, and expand tests before this is ready to merge.
```

## Rationalizations observed (manual notes)

_Read the transcript and record rationalizations verbatim here._
