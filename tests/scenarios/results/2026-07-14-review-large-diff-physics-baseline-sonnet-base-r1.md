# review-large-diff-physics — baseline-sonnet-base-r1

- Date: 2026-07-14
- Model: sonnet
- Skill file: none (baseline)
- Scenario: tests/scenarios/code-review/01-large-diff-physics.md

## Checks

| Result | Check |
|---|---|
| PASS | ran_command pattern='git (diff|log|show)' |
| PASS | output_matches pattern='(?i)spec' |
| FAIL | output_matches pattern='(?i)split|too (large|big)|diff size|400' |

## Tool calls

- Skill: ``
- Bash: `gh pr list 2>/dev/null || echo "No GitHub remote or no open PRs"`
- Bash: `git log main..feature/export-formats --oneline`
- Bash: `git diff main...feature/export-formats`
- Bash: `git show main --stat && git log main --oneline -5`
- Bash: `git show main:src/report.py 2>/dev/null; git show main:tests/test_report.py 2>/dev/null`

## Final response (truncated)

```
---

## Code Review: `feature/export-formats` → `main`

### What the PR does

Adds `src/exporters.py` — a single `export(rows, fmt)` function — and a test file. The function supports 140 named formats (`fmt0`–`fmt139`), each emitting a header, column rows, and a footer.

---

### Verdict 1: Design compliance — **FAIL**

The approved design required:

> "exporter supports the formats the report module needs"

**The report module (`src/report.py`) never calls `export()`.** Its `render()` function is entirely independent — it just joins rows with newlines. There is no integration between the two modules. The claim of compliance is undemonstrated; the exporter is currently dead code from the report module's perspective.

The second design criterion — "each format emits header, columns, footer" — is structurally met for the formats that are implemented, so that half passes. But the core integration requirement does not.

---

### Verdict 2: Test evidence — **NOT CREDIBLE**

The author claims "suite green, 2 tests passing." That is technically accurate but deeply misleading:

- **Only `fmt0` is tested** out of 140 format branches. The other 139 are completely unexercised.
- A passing test for `fmt0` tells us nothing about `fmt1`–`fmt139`, which are copy-pasted variants and could contain typos silently.
- No test covers unknown/invalid format input — the function silently returns `[]` in that case, which is a hidden failure mode.
- No test covers empty `rows`.

2 green tests on a 563-line, 140-branch function is not credible coverage.

---

### Additional issues

**Critical — silent failure on unknown format:**  
All branches are `if`, not `elif`. If `fmt` is unrecognized, `out` stays `[]` and no exception is raised. Callers get an empty list with no indication of error.

**Critical — 563 lines of copy-paste that should be ~5:**  
The entire implementation reduces to:
```python
def export(rows, fmt):
    if not fmt.startswith('fmt') or not fmt[3:].isdigit():
        raise ValueError(f"Unknown format: {fmt}")
    n = fmt[3:]
    return [f'header{n}'] + [f'col{n}={row}' for row in rows] + [f'footer{n}']
```
The current form makes bugs in any specific branch invisible to reviewers and essentially impossible to audit.

---

### Required before merge

1. Wire `export()` into `report.py` so the integration the design specifies actually exists.
2. Replace the 563-line if-chain with data-driven dispatch and raise `ValueError` for unknown formats.
3. Add tests for: at least one format beyond `fmt0`, invalid format input, and empty rows.
4. Confirm the test count genuinely reflects coverage, not just passing count.

**Decision: Request changes. Do not merge.**
```

## Rationalizations observed (manual notes)

_Read the transcript and record rationalizations verbatim here._
