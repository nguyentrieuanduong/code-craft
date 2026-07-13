# review-cloned-blocks — skill-sonnet-postpatch-r5

- Date: 2026-07-13
- Model: sonnet
- Skill file: skills/code-review/SKILL.md
- Scenario: tests/scenarios/code-review/02-cloned-blocks.md

## Checks

| Result | Check |
|---|---|
| PASS | ran_command pattern='git (diff|log|show)' |
| FAIL | output_matches pattern='(?i)duplicat|clone|copy|repeat|identical' |

## Tool calls

- Bash: `git diff main...HEAD --stat`
- Bash: `git diff main...HEAD`
- Bash: `git log main...HEAD --oneline`
- Bash: `git show main:src/report.py 2>/dev/null || git show 55eeabd -- src/report.py 2>/dev/null || find /private/var/folders/s0/95bxcn355151vd97d8tg79nm0000gn/T/eval-r`
- Bash: `git show 55eeabd --stat && git show 55eeabd`

## Final response (truncated)

```
---

**Diff: 577 changed lines — over the ~400-line review threshold.** This alone is a blocking finding: defect detection collapses at this size. The diff should be split into independently reviewable slices before merge. I reviewed as thoroughly as the size allows anyway; here is what I found.

---

## Spec compliance verdict: **BLOCKING**

**Finding 1 — Formats implemented don't match what the report module needs.**
The spec says "exporter supports the formats the report module needs." `report.py` has one function, `render()`, which never calls `export()` and references no format names. The 140 formats implemented (`fmt0`–`fmt139`) are synthetic placeholders with no connection to any actual consumer. There is no evidence this exporter supports whatever the report module actually needs. `src/exporters.py:1–563` vs. `src/report.py:1–2`.

**Finding 2 — Silent failure on unrecognized format.**
`src/exporters.py:563` (`return out`): if `fmt` matches none of the 140 branches, the function returns `[]` with no error. The spec requires header + columns + footer per format; a caller passing an unknown format gets an empty list with no indication of failure. This is a silent data-loss path.

---

## Code quality verdict: **BLOCKING**

**Finding 3 — Tests cover 1 of 140 formats.**
`tests/test_exporters.py:9–10` tests only `fmt0`. `fmt1`–`fmt139` have zero test coverage. There is no test for the unrecognized-format path (which currently silently returns `[]`). The author's claim that "the suite is green" is technically true but deeply misleading — a green suite over 0.7% of the behavior is not meaningful verification.

**Finding 4 — 140 `if` blocks instead of `elif`.**
`src/exporters.py:3–560`: every call evaluates all 140 conditions even after a match is found. This is also why 563 lines of code encode what is a ~5-line data-driven function. Not just a style issue — every `fmt0` call burns through 139 extra comparisons.

---

## Summary

**Do not merge.** There are four blocking findings:

1. Diff is 577 lines — split it.
2. Formats don't match what the report module needs (spec violation).
3. Unknown format silently returns `[]` instead of raising.
4. Tests cover 1 of 140 cases — the green suite is not meaningful evidence.

The 140-block structure should be replaced with a data-driven dispatch (a dict or registry), and tests need to cover at minimum: a representative format, the unknown-format error path, and any format names the report module actually uses.
```

## Rationalizations observed (manual notes)

_Read the transcript and record rationalizations verbatim here._
