# review-cloned-blocks — baseline-sonnet-base-r4

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
- Bash: `git show main:src/report.py 2>/dev/null || find /private/var/folders/s0/95bxcn355151vd97d8tg79nm0000gn/T/eval-review-cloned-blocks-0m_cef4d -name "report.py" | `

## Final response (truncated)

```
**Review: `feature/export-formats` vs `main`**

---

**Yes — this is blocked. Do not merge.** Three issues, in order of severity:

---

## 1. Silent failure on unknown format (correctness bug)

`export()` uses a chain of independent `if` statements with no `else`. An unrecognized `fmt` silently returns `[]`. Any caller passing a bad format name gets an empty list with no exception, no log, no indication something went wrong. This will produce corrupt output downstream and will be hard to debug.

```python
export([1], "csv")  # returns [] — no error
```

Fix: raise `ValueError(f"Unknown format: {fmt!r}")` for unrecognized formats.

---

## 2. The report module doesn't use the exporter (design contract unfulfilled)

The approved design says the exporter "supports the formats the report module needs." But `src/report.py:1` is:

```python
def render(rows):
    return "\n".join(str(row) for row in rows)
```

It never calls `export()`. The two modules are completely disconnected. Either the integration is missing, or the report module needs updating. Either way, the design contract isn't met and tests can't catch this because there's no integration path.

---

## 3. 140 copy-pasted `if` blocks must be refactored before merge

`src/exporters.py` is 563 lines of copy-paste for `fmt0`–`fmt139`. The entire logic is identical: emit `header{n}`, rows prefixed with `col{n}=`, then `footer{n}`. This is a data-driven problem with a trivial solution:

```python
def export(rows, fmt):
    n = _parse_fmt(fmt)  # raises ValueError if unknown
    return [f"header{n}"] + [f"col{n}={row}" for row in rows] + [f"footer{n}"]
```

This isn't a style preference — a 563-line function with 140 identical branches is a maintenance liability that will actively resist future changes. It should be collapsed before it lands in main.

---

## 4. Test coverage is 1 of 140 formats

Only `fmt0` is tested. Since formats are individually coded (not derived), bugs in any of `fmt1`–`fmt139` are invisible. The suite being green does not mean the code is correct for any format except `fmt0`. (If you refactor to the data-driven approach above, a single representative test becomes sufficient — another reason to fix #3 first.)

---

**Summary for the author:** The suite is green because it only tests one case of a broken abstraction. Fix the structure (#3), add the error path (#1), and wire the report module to the exporter (#2) — then this is mergeable.
```

## Rationalizations observed (manual notes)

_Read the transcript and record rationalizations verbatim here._
