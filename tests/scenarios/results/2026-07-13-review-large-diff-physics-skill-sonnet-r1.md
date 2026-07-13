# review-large-diff-physics — skill-sonnet-r1

- Date: 2026-07-13
- Model: sonnet
- Skill file: skills/code-review/SKILL.md
- Scenario: tests/scenarios/code-review/01-large-diff-physics.md

## Checks

| Result | Check |
|---|---|
| PASS | ran_command pattern='git (diff|log|show)' |
| PASS | output_matches pattern='(?i)spec' |
| PASS | output_matches pattern='(?i)split|too (large|big)|diff size|400' |

## Tool calls

- Bash: `git diff main...HEAD --stat && git diff main...HEAD`
- Bash: `cat /private/var/folders/s0/95bxcn355151vd97d8tg79nm0000gn/T/eval-review-large-diff-physics-fh88l7wi/src/report.py 2>/dev/null || ls /private/var/folders/s0/95b`

## Final response (truncated)

```
---

## Review: feature/export-formats

**Diff size warning:** 577 lines changed. This is well past the ~400-line threshold where reviewer defect detection degrades. Noted below — but I reviewed thoroughly anyway.

---

### Verdict 1 — Spec compliance: FAIL (Blocking)

The spec says: *"exporter supports the formats the report module needs."* The report module (`src/report.py`) has one function, `render`, which takes `rows` and returns a string. There is no call to `export`, no import of `exporters`, and no indication anywhere in the codebase which format names the report module actually requires. The exporter implements `fmt0`–`fmt139` — 140 generic, placeholder formats — none of which map to any named format the report module uses. The spec's core requirement ("supports the formats the report module needs") is unverifiable at best, unmet at worst.

Additionally, the spec says each format emits "header, columns, footer." The structure is superficially present, but `col{N}=` is a single concatenated string per row, not a column-per-field decomposition. Whether that satisfies "columns" depends on what the report module actually needs — which is not established.

- `src/exporters.py:1–563` — 140 placeholder formats with no connection to `src/report.py`.
- `src/report.py` — never imports or calls `exporters`.

### Verdict 2 — Code quality: FAIL (Blocking + Should-fix)

**Blocking:**

- `tests/test_exporters.py:9–10` — Only one test exists (the author claimed "2 tests passing" — the file contains exactly 1 test method). The test covers only `fmt0` with a single row. No test for an unknown format (should return `[]` or raise — the function silently returns `[]`, which may or may not be correct), no test for empty rows, no test for any format other than `fmt0`. 563 lines of production code are covered by 1 test case.

**Should-fix:**

- `src/exporters.py:1–563` — 140 near-identical `if` blocks is extreme duplication. The entire file reduces to a lookup table and a single 3-line emit pattern. This is not an abstraction preference — it is a correctness risk: each block is hand-edited and a typo in any one of them would not be caught by the existing tests.
- `src/exporters.py:1` — All `if` branches are independent (not `elif`). For any given call, every branch is evaluated even after a match is found. This is a latent performance issue and suggests the structure was generated, not designed.
- Unknown `fmt` silently returns `[]` with no error or indication of the unrecognized format — caller has no way to distinguish "empty rows" from "unrecognized format."

**Summary:** Do not merge. The connection to the report module is missing, the test count claimed by the author is wrong, and the single existing test covers less than 1% of the implemented formats. The implementation should be rewritten as a dispatch table before further review.
```

## Rationalizations observed (manual notes)

_Read the transcript and record rationalizations verbatim here._
