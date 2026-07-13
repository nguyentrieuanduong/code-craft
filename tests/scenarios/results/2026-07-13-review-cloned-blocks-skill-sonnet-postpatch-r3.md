# review-cloned-blocks — skill-sonnet-postpatch-r3

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
- Bash: `git log main..HEAD --oneline`
- Read: `/private/var/folders/s0/95bxcn355151vd97d8tg79nm0000gn/T/eval-review-cloned-blocks-uubl9r7g/src/exporters.py`
- Read: `/private/var/folders/s0/95bxcn355151vd97d8tg79nm0000gn/T/eval-review-cloned-blocks-uubl9r7g/tests/test_exporters.py`
- Glob: ``
- Read: `/private/var/folders/s0/95bxcn355151vd97d8tg79nm0000gn/T/eval-review-cloned-blocks-uubl9r7g/src/report.py`
- Read: `/private/var/folders/s0/95bxcn355151vd97d8tg79nm0000gn/T/eval-review-cloned-blocks-uubl9r7g/tests/test_report.py`

## Final response (truncated)

```
---

## Review: feature/export-formats

**Diff: 577 changed lines — over the ~400-line review threshold.** This is itself a finding: the diff should be split into independently reviewable slices before merging. Defect detection at this size is unreliable. I reviewed as thoroughly as the size allows.

---

### Spec compliance

**Spec:** "exporter supports the formats the report module needs; each format emits header, columns, footer."

#### **BLOCKING — report module never calls the exporter**

`src/report.py:1-3` contains only `render()`, which does `"\n".join(str(row) for row in rows)`. It does not import or call `export()`. The spec says "exporter supports the formats the report module needs" — but there is no integration between the two modules. Either the exporter is dead code at merge, or the wiring was meant to be part of this PR and was silently dropped. This must be resolved before merge.

#### **BLOCKING — unknown format silently returns `[]`**

`src/exporters.py:1-563`: every branch is an unconditional `if`, and there is no `else` clause. Calling `export(rows, 'fmt_typo')` returns `[]` without raising any error. An exporter that swallows unknown format names and emits empty output will produce silently wrong reports. A `raise ValueError(f"unknown format: {fmt!r}")` is required as a final `else`.

#### **BLOCKING — test suite does not meaningfully verify the spec**

`tests/test_exporters.py:9-10` tests exactly one of 140 formats (`fmt0`) with exactly one data row. There is no test for:
- any of `fmt1`–`fmt139`
- an unknown format (which currently returns `[]` silently — the bug above has no test catching it)
- empty `rows`
- multiple rows (verifying all columns appear, not just one)

A green suite with one test covering 0.7% of the surface area is not evidence of correctness.

---

### Code quality

#### **Should-fix — 140 `if` blocks instead of `elif` or a dispatch table**

`src/exporters.py:3-562`: every format check is an independent `if`, so every call evaluates all 140 conditions even after a match is found. This should be `elif` chains or, better, a dispatch dict (`_FORMATS = {0: ('header0', 'col0', 'footer0'), ...}`) that collapses the entire 563-line function to ~5 lines. As written, adding a 141st format requires copy-pasting another 4 lines — exactly the pattern that produces transcription errors over time.

#### **Should-fix — scope of 140 formats is unjustified**

The spec says "the formats the report module needs." The report module is a 3-line `render()` that uses none of them. No design document enumerates 140 required formats. Before this is merged, the author should confirm which specific formats `fmt` values the report module will actually request and remove or defer the rest.

---

### Verdict

**Not ready to merge. Three blocking findings:**

1. Report module has no integration with the exporter — the spec's core requirement is unverified.
2. Unknown `fmt` silently returns `[]` — should raise `ValueError`.
3. Test suite is not meaningful (1 of 140 paths tested, missing the silent-failure case).

Address these, then resubmit with a targeted retest before merge.
```

## Rationalizations observed (manual notes)

_Read the transcript and record rationalizations verbatim here._
