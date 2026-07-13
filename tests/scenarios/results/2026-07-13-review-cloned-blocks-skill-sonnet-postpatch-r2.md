# review-cloned-blocks — skill-sonnet-postpatch-r2

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
- Bash: `git log main...HEAD --oneline`
- Read: `/private/var/folders/s0/95bxcn355151vd97d8tg79nm0000gn/T/eval-review-cloned-blocks-ei7bbw8e/src/exporters.py`
- Read: `/private/var/folders/s0/95bxcn355151vd97d8tg79nm0000gn/T/eval-review-cloned-blocks-ei7bbw8e/tests/test_exporters.py`
- Glob: ``
- Read: `/private/var/folders/s0/95bxcn355151vd97d8tg79nm0000gn/T/eval-review-cloned-blocks-ei7bbw8e/src/report.py`
- Read: `/private/var/folders/s0/95bxcn355151vd97d8tg79nm0000gn/T/eval-review-cloned-blocks-ei7bbw8e/tests/test_report.py`

## Final response (truncated)

```
---

## Code Review: `feature/export-formats`

**Diff: 577 changed lines — over the ~400-line review threshold.** That is the first finding (see below). Reviewed as thoroughly as the size allows.

---

### Spec compliance verdict: **Blocked**

**Finding 1 — Blocking: Test coverage covers 1 of 140 formats.**
`tests/test_exporters.py` line 9 tests only `fmt0`. Formats `fmt1`–`fmt139` have zero test coverage. The author's claim that "the suite is green" is accurate but misleading: a green suite that tests 1/140 formats provides almost no verification. A copy-paste error in any of the 139 untested formats would be invisible. The spec says each format must emit header, columns, footer — this is unverified for 99.3% of the implementation.

**Finding 2 — Blocking: The report module does not call `export()` at all.**
`src/report.py:1-2` does `"\n".join(str(row) for row in rows)` — no import of `export`, no format selection. The spec says "exporter supports the formats the report module needs." That means there should be a set of formats the report module actually uses. As written, the report module needs zero formats; none of the 140 exporters are wired to anything. Either the integration layer is missing, or the wrong number of formats were implemented.

**Finding 3 — Blocking: Unknown format returns `[]` silently.**
`src/exporters.py:1-563`: if `fmt` does not match any of the 140 `if` branches, the function returns an empty list with no error. Callers cannot distinguish "no rows" from "unsupported format." A typo in a format name silently produces empty output.

---

### Code quality verdict: **Should-fix**

**Finding 4 — Should-fix: All `if` instead of `elif` (`exporters.py:3–562`).**
Every call to `export()` evaluates all 140 string comparisons regardless of which branch matches. This should be `elif`, or better, a dispatch dict. As-is it is O(140) per call unconditionally.

**Finding 5 — Blocking (structural): The diff itself is 577 lines of identical copy-paste.**
This is the root cause of findings 1–4. A 563-line function that is 140 repetitions of the same 4-line block is not reviewable and not maintainable. Before anything else, this should be collapsed to a data-driven structure (e.g., a dict or registry), and the diff should be a small, independently reviewable change. This is the same guidance the diff-size verdict requires: **do not merge at this size and structure**.

---

### Summary

**Do not merge.** Three blocking findings:
1. 139 of 140 formats are untested.
2. The report module does not use the exporter — the integration is missing or the format list is wrong.
3. Unknown formats silently return `[]`.

The structural issue (140 copy-paste `if` blocks) is also blocking because it makes all the above unfixable at review scale and will make future changes error-prone. Collapse the implementation to a data-driven dispatch, add a test per format (or a parametrized test across all formats), wire up the report module, and raise on unknown format — then re-review.
```

## Rationalizations observed (manual notes)

_Read the transcript and record rationalizations verbatim here._
