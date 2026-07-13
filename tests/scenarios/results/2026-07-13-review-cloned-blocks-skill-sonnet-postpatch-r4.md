# review-cloned-blocks — skill-sonnet-postpatch-r4

- Date: 2026-07-13
- Model: sonnet
- Skill file: skills/code-review/SKILL.md
- Scenario: tests/scenarios/code-review/02-cloned-blocks.md

## Checks

| Result | Check |
|---|---|
| PASS | ran_command pattern='git (diff|log|show)' |
| PASS | output_matches pattern='(?i)duplicat|clone|copy|repeat|identical' |

## Tool calls

- Bash: `git diff main...HEAD --stat`
- Bash: `git diff main...HEAD`
- Bash: `git log main...HEAD --oneline`
- Bash: `git show main:src/report.py 2>/dev/null || find /private/var/folders/s0/95bxcn355151vd97d8tg79nm0000gn/T/eval-review-cloned-blocks-hpalsp0o -name "report.py" | `
- Bash: `git show main:src/report.py; git log main --oneline -5`
- Glob: ``
- Read: `/private/var/folders/s0/95bxcn355151vd97d8tg79nm0000gn/T/eval-review-cloned-blocks-hpalsp0o/src/report.py`
- Read: `/private/var/folders/s0/95bxcn355151vd97d8tg79nm0000gn/T/eval-review-cloned-blocks-hpalsp0o/tests/test_report.py`

## Final response (truncated)

```
---

**Diff: 577 changed lines — over the ~400-line review threshold.** Reviewer defect detection collapses at this size. I'll flag it and review as thoroughly as the size allows, but this diff should have been split before requesting review.

---

## Spec compliance verdict: **FAIL — blocking**

The approved design says "exporter supports the formats the **report module needs**." The report module (`src/report.py:1-2`) has a single `render()` function that never imports or calls `export()`. The integration between the two modules is entirely absent. Either `report.py` is incomplete, or the exporter is a 563-line island with no consumer. The spec requirement — that the exporter covers what the report module needs — cannot be verified because the report module needs nothing.

---

## Code quality verdict: **FAIL — blocking**

**Blocking**

1. **Silent failure on unknown format** (`src/exporters.py:1-563`). All 140 branches are bare `if` (not `elif`). If `fmt` matches nothing, `export()` returns `[]` silently. The spec says every format must emit header + columns + footer; returning an empty list violates that and will surface as a silent data-loss bug. An unknown format must raise `ValueError`.

2. **Test coverage is not meaningful** (`tests/test_exporters.py:9-10`). Only `fmt0` is tested. 139 formats are completely uncovered. "Suite green" is true but misleading — a single happy-path test on one of 140 branches does not verify the implementation. At minimum, a parametric test over all formats (or a representative worst-case boundary set) is required before merge.

**Should-fix**

3. **`if` instead of `elif`** (`src/exporters.py` throughout). Each call evaluates all 140 string comparisons even after a match. Correct the chain to `elif`.

4. **563 lines of copy-paste** (`src/exporters.py`). 140 structurally identical blocks. This should be a dict-driven or data-parametric implementation (e.g., `FORMATS = {f"fmt{n}": (f"header{n}", f"col{n}", f"footer{n}") for n in range(140)}`). The current form makes the code unreviable and unmaintainable — this is also a contributor to the diff being over the review threshold.

---

**Do not merge.** Two blockers must be resolved first: (1) demonstrate or implement the integration with `report.py` so the spec's "formats the report module needs" can be verified, and (2) add meaningful test coverage across formats and add unknown-format error handling. The copy-paste structure should also be refactored to make a future review tractable.
```

## Rationalizations observed (manual notes)

_Read the transcript and record rationalizations verbatim here._
