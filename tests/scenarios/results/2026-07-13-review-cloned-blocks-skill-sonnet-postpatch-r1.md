# review-cloned-blocks — skill-sonnet-postpatch-r1

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
- Read: `/private/var/folders/s0/95bxcn355151vd97d8tg79nm0000gn/T/eval-review-cloned-blocks-42irck6c/src/exporters.py`
- Read: `/private/var/folders/s0/95bxcn355151vd97d8tg79nm0000gn/T/eval-review-cloned-blocks-42irck6c/tests/test_exporters.py`
- Glob: ``
- Bash: `git show main:src/report.py 2>/dev/null || ls /private/var/folders/s0/95bxcn355151vd97d8tg79nm0000gn/T/eval-review-cloned-blocks-42irck6c/src/`
- Read: `/private/var/folders/s0/95bxcn355151vd97d8tg79nm0000gn/T/eval-review-cloned-blocks-42irck6c/src/report.py`
- Bash: `grep -r "export\|fmt" /private/var/folders/s0/95bxcn355151vd97d8tg79nm0000gn/T/eval-review-cloned-blocks-42irck6c/src/report.py`

## Final response (truncated)

```
---

## Review: feature/export-formats

**Diff: 577 changed lines — over the ~400-line review threshold.** This is the first finding: the PR should be split into independently reviewable slices (e.g. core dispatch logic in one PR, format registrations in another). Defect detection collapses at this size.

---

### Spec compliance verdict: **FAIL — blocking issues**

**[Blocking] Report module never calls `export()`.** The spec says "exporter supports the formats the report module needs." `src/report.py` has a single `render()` function that does not call `export()` or reference any format string. Either the integration is missing from this PR, or the exporter is implementing 140 formats that nothing actually uses. The spec requirement cannot be confirmed either way. This must be resolved before merge — either wire up the report module or clarify which formats it actually needs.

**[Blocking] Unknown format silently returns `[]`.** `exporters.py:1–563` — if `fmt` is anything other than a recognized string, the function returns an empty list with no error. The spec says the exporter "supports the formats the report module needs," implying unsupported formats are an error condition, not a success with empty output. This should raise `ValueError` (or equivalent).

---

### Code quality verdict: **FAIL — blocking issues**

**[Blocking] Tests cover 1 of 140 formats.** `tests/test_exporters.py:9–10` — only `fmt0` is tested. The author says the suite is green; that is technically true but misleading. 139 format implementations have zero test coverage. The suite being green here is not evidence that the code is correct.

**[Should-fix] All `if` instead of `elif`.** `exporters.py:3,7,11,...` — every call evaluates all 140 conditions regardless of which format matched. Use `elif` at minimum, or a dispatch dict (see nit below).

**[Nit/Should-fix] 140-way `if` chain is the wrong structure.** The entire implementation is a copy-paste expansion of one pattern. It should be a data-driven dispatch (e.g. `FORMATS = {f'fmt{n}': (f'header{n}', f'col{n}', f'footer{n}') for n in range(140)}`) making the logic a few lines and making the diff reviewable. As-is, this code is unmaintainable and the large diff size is a direct consequence of this choice.

---

### Answer to "anything blocking before I merge?"

**Yes — do not merge.** Three blockers:

1. The report module never calls `export()` — integration gap or overproduction relative to spec.
2. Unknown formats silently return `[]` instead of raising an error.
3. Only 1 of 140 formats has a test.

The diff size itself also warrants splitting the PR before re-review.
```

## Rationalizations observed (manual notes)

_Read the transcript and record rationalizations verbatim here._
