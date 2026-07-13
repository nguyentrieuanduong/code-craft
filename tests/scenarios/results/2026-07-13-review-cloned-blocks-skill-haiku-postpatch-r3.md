# review-cloned-blocks — skill-haiku-postpatch-r3

- Date: 2026-07-13
- Model: claude-haiku-4-5-20251001
- Skill file: skills/code-review/SKILL.md
- Scenario: tests/scenarios/code-review/02-cloned-blocks.md

## Checks

| Result | Check |
|---|---|
| PASS | ran_command pattern='git (diff|log|show)' |
| PASS | output_matches pattern='(?i)duplicat|clone|copy|repeat|identical' |

## Tool calls

- Bash: `git diff main...HEAD --stat`
- Read: `/private/var/folders/s0/95bxcn355151vd97d8tg79nm0000gn/T/eval-review-cloned-blocks-gi1ve1qa/src/exporters.py`
- Read: `/private/var/folders/s0/95bxcn355151vd97d8tg79nm0000gn/T/eval-review-cloned-blocks-gi1ve1qa/tests/test_exporters.py`
- Bash: `git log --oneline -10`
- Bash: `git show 3775554 --stat`
- Read: `/private/var/folders/s0/95bxcn355151vd97d8tg79nm0000gn/T/eval-review-cloned-blocks-gi1ve1qa/src/report.py`
- Bash: `grep -r "export\|fmt" src/report.py tests/test_report.py 2>/dev/null | head -20`
- Read: `/private/var/folders/s0/95bxcn355151vd97d8tg79nm0000gn/T/eval-review-cloned-blocks-gi1ve1qa/tests/test_report.py`
- Bash: `grep -r "exporter\|export(" . --include="*.py" | grep -v ".pyc" | grep -v test_exporters`
- Bash: `python -m pytest tests/ -v 2>&1`
- Bash: `python3 -m unittest discover tests/ -v 2>&1`
- Bash: `python3 << 'EOF'
import sys
sys.path.insert(0, "src")
from exporters import export

# Test unknown format
result = export([1, 2, 3], "csv")
print(f"export([1, 2`

## Final response (truncated)

```
## Review: feature/export-formats

**Diff: 577 changed lines — over the ~400-line review threshold.** Detection rates decline at this size, so I'll focus on spec compliance and critical issues.

---

### Blocking Findings

**1. Silent failure on unknown formats** — src/exporters.py:1-3, 563
- Calling `export(rows, 'csv')` or any unrecognized format returns `[]` without error
- This enables silent data loss: a caller expecting CSV output gets an empty list with no indication of failure
- **Fix**: Validate `fmt` against the known formats and raise `ValueError(f"Unknown format: {fmt}")` for unknown formats, or document this behavior and update callers to check for empty output

**2. Missing/unclear integration with report module** — spec vs. code
- Spec: "exporter supports the formats the report module needs"
- Fact: `src/report.py` does not import or call the exporter — there is no integration
- No integration tests exist verifying the modules work together
- **Clarify**: Does the report module need to call the exporter? If yes, wire it up and add integration tests. If no, the spec statement is misleading and should be updated.

---

### Should-Fix Findings

**3. Unmaintainable code structure** — src/exporters.py:1-563
- 563 lines of near-identical copy-paste for 140 formats (fmt0–fmt139)
- Each format is 4 repeated lines differing only in the format number
- Violates maintainability: adding/fixing a format requires changes in 140 places; high risk of inconsistency
- **Fix**: Refactor to data-driven structure (e.g., dictionary of format specs), then generate the output in a loop

**4. Insufficient test coverage** — tests/test_exporters.py
- Only `fmt0` is tested; 139 formats are untested
- Cannot verify the pattern holds across all formats
- **Fix**: Add parametrized tests or spot-check 3–5 additional formats

---

### Summary

**Blocking**: Resolve silent failure and clarify integration scope before merge.
**Should-fix**: Refactor repetitive code and expand test coverage to catch future bugs; this code is difficult to verify by inspection.
```

## Rationalizations observed (manual notes)

_Read the transcript and record rationalizations verbatim here._
