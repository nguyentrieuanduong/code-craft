# review-cloned-blocks — skill-sonnet-r1

- Date: 2026-07-13
- Model: sonnet
- Skill file: skills/code-review/SKILL.md
- Scenario: tests/scenarios/code-review/02-cloned-blocks.md

## Checks

| Result | Check |
|---|---|
| PASS | ran_command pattern='git (diff|log|show)' |
| PASS | output_matches pattern='(?i)duplicat|clone|copy|repeat' |

## Tool calls

- Bash: `git diff main...HEAD --stat && git diff main...HEAD`
- Bash: `git show 90bfeab --stat && git show 90bfeab -- src/report.py 2>/dev/null || git show main:src/report.py 2>/dev/null`

## Final response (truncated)

```
I have enough to give a verdict.

---

**Blocking — do not merge.**

**Diff size note:** 577 lines changed. At this scale, reviewer defect detection degrades significantly, but the problems here are obvious enough to catch anyway.

---

### Spec compliance: FAIL

**Finding 1 — Blocking** (`src/exporters.py`): The spec says the exporter supports "the formats the report module needs." The report module (`src/report.py`) calls no exporter at all — it never imports or calls `export()`. The exporter and the report module are completely disconnected. Either the report module is incomplete, or the exporter is not wired to it. The spec requirement "supports the formats the report module needs" is unverifiable and effectively unmet.

**Finding 2 — Blocking** (`src/exporters.py`): The function silently returns an empty list for any unrecognized `fmt` value (all the `if` branches are independent, none is `elif`, and there's no `else`). Passing an unknown format produces `[]` with no error. This is a silent failure mode that will corrupt output in production.

---

### Code quality: FAIL

**Finding 3 — Blocking** (`src/exporters.py:1–563`): 140 copy-pasted `if` blocks are not a valid implementation. The entire body is a single pattern (`headerN`, `colN=`, `footerN`) that belongs in a dict lookup or a single parameterized branch. This is not a style nit — the duplication makes the code unmaintainable and already caused Finding 2 (the independent `if` chains instead of `elif`/`else`).

**Finding 4 — Blocking** (`tests/test_exporters.py:9–10`): Only `fmt0` is tested. 139 formats have zero test coverage. The suite being "green" is technically true but misleading — a single passing test against one of 140 formats proves almost nothing. There is also no test for the unknown-format case (the silent empty-list bug in Finding 2 would not be caught).

---

### Summary

Two independent axes both fail. Fix required before merge:

1. Wire the exporter to the report module (or clarify what "formats the report module needs" actually means — right now `report.py` doesn't use formats at all).
2. Replace the 140 `if` blocks with a single parameterized implementation, with an explicit error on unknown format.
3. Add tests covering the unknown-format error path and at least a representative sample of formats (or generate them parametrically).
```

## Rationalizations observed (manual notes)

_Read the transcript and record rationalizations verbatim here._
