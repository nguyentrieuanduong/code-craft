# review-cloned-blocks — skill-haiku-postpatch-r5

- Date: 2026-07-13
- Model: claude-haiku-4-5-20251001
- Skill file: skills/code-review/SKILL.md
- Scenario: tests/scenarios/code-review/02-cloned-blocks.md

## Checks

| Result | Check |
|---|---|
| PASS | ran_command pattern='git (diff|log|show)' |
| FAIL | output_matches pattern='(?i)duplicat|clone|copy|repeat|identical' |

## Tool calls

- Bash: `git diff main...HEAD --stat`
- Bash: `git log --oneline main...HEAD`
- Read: `/private/var/folders/s0/95bxcn355151vd97d8tg79nm0000gn/T/eval-review-cloned-blocks-5bj5a399/src/exporters.py`
- Read: `/private/var/folders/s0/95bxcn355151vd97d8tg79nm0000gn/T/eval-review-cloned-blocks-5bj5a399/tests/test_exporters.py`
- Bash: `git show HEAD~1:src/report.py | head -50`
- Bash: `python -m pytest tests/test_exporters.py -v`
- Bash: `grep -c "fmt" /private/var/folders/s0/95bxcn355151vd97d8tg79nm0000gn/T/eval-review-cloned-blocks-5bj5a399/src/exporters.py`
- Bash: `grep "fmt[0-9]" /private/var/folders/s0/95bxcn355151vd97d8tg79nm0000gn/T/eval-review-cloned-blocks-5bj5a399/src/exporters.py | wc -l`

## Final response (truncated)

```
## Code Review: feature/export-formats

**Diff: 577 changed lines — over the ~400-line review threshold.** Reviewer defect detection will be below ideal.

---

### **Spec Compliance: ✓ PASS**
- ✓ Supports all 140 formats (fmt0–fmt139) that report module needs
- ✓ Each format emits header, columns (from rows), footer pattern as designed

---

### **Findings**

**BLOCKING: Missing test coverage for 139 of 140 formats** — src/exporters.py:1–563, tests/test_exporters.py:9–10

The test suite covers only `fmt0` with a single row. There are no tests for:
- Any format other than fmt0
- Edge cases (empty rows, multiple rows, non-string row values)
- Error handling (what does `export([1], "fmt999")` or `export([1], "invalid_fmt")` return?)

With 140 distinct formats and the current structure, undetected bugs in fmt1–fmt139 are likely. At minimum, this is a regression risk; test coverage must match the interface.

**Should-fix: Control flow inefficiency** — src/exporters.py:1–563

Implementation uses a chain of 140 `if` statements instead of `elif` or dictionary lookup. This means all 140 conditionals execute for every call. Consider:

```python
handlers = {
    'fmt0': lambda rows: ['header0'] + [f'col0={r}' for r in rows] + ['footer0'],
    # ...
}
return handlers.get(fmt, [])(rows)
```

Also: no error signal for unsupported formats—`export([1], "fmt1000")` silently returns `[]`. Spec doesn't say this is intended behavior.

---

### **No blocking findings on spec compliance, but the test coverage gap is critical for merge readiness.** Recommend adding parametrized tests for all formats and edge cases before merge.
```

## Rationalizations observed (manual notes)

_Read the transcript and record rationalizations verbatim here._
