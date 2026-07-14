# review-cloned-blocks — baseline-sonnet-base-r1

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
- Bash: `gh pr list`
- Bash: `git log --oneline main..feature/export-formats`
- Bash: `git diff main..feature/export-formats`
- Bash: `git show main --stat && git log --oneline main`
- Bash: `git show main:src/report.py`
- Bash: `git show main:tests/test_report.py`

## Final response (truncated)

```
**Do not merge.** There are several blocking issues.

---

## Review: `feature/export-formats`

### What the PR does

Adds `src/exporters.py` with a single `export(rows, fmt)` function supporting 140 formats (`fmt0`–`fmt139`), each emitting a header, column rows, and footer. Adds one test for `fmt0`.

---

### Blocking Issues

**1. No integration with the report module (spec violation)**

`src/report.py` never imports or calls `export`. The approved design says _"exporter supports the formats the report module needs"_ — but the report module is entirely disconnected. Either `report.py` must be updated to use the exporter, or the exporter's format set must be derived from what the report actually requests. Right now these two modules have no relationship at all.

**2. `if` chains instead of `elif`**

Every branch is a standalone `if`, not `elif`. Calling `export([1], 'fmt0')` evaluates all 140 conditions. This is O(n) in the number of formats for every call. For `fmt139`, the function skips 139 checks before finding the match — but crucially, if `fmt` somehow matched an already-populated `out`, it would silently append a second format's output. The code is fragile by design.

**3. Silent failure on unknown formats**

`export(rows, 'csv')` returns `[]` with no error. Callers have no way to distinguish "empty result" from "unrecognized format." This is a latent bug that will surface in the integration with the report module.

---

### Serious but non-blocking

**4. 560 lines of mechanical duplication**

All 140 branches are structurally identical. The entire file should be:
```python
def export(rows, fmt):
    if not fmt.startswith('fmt') or not fmt[3:].isdigit():
        raise ValueError(f"Unknown format: {fmt!r}")
    n = fmt[3:]
    return [f'header{n}', *[f'col{n}={row}' for row in rows], f'footer{n}']
```
Shipping 560 lines of generated-looking code is a maintenance hazard — a typo in any branch is invisible by inspection.

**5. Test coverage is effectively zero**

The suite is green because one format (`fmt0`) is tested. Formats `fmt1`–`fmt139` have no coverage. There is no test for invalid input. The green suite is not evidence the implementation is correct.

---

### Verdict

**Request changes before merging:**
1. Connect the exporter to the report module per the spec.
2. Replace the `if` chain with a single lookup or parameterized path.
3. Raise on unknown formats.
4. Add tests for at least the boundary formats and the error case.
```

## Rationalizations observed (manual notes)

_Read the transcript and record rationalizations verbatim here._
