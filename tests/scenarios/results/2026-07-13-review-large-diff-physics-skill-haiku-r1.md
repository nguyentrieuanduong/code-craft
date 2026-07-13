# review-large-diff-physics — skill-haiku-r1

- Date: 2026-07-13
- Model: claude-haiku-4-5-20251001
- Skill file: skills/code-review/SKILL.md
- Scenario: tests/scenarios/code-review/01-large-diff-physics.md

## Checks

| Result | Check |
|---|---|
| PASS | ran_command pattern='git (diff|log|show)' |
| PASS | output_matches pattern='(?i)spec' |
| FAIL | output_matches pattern='(?i)split|too (large|big)|diff size|400' |

## Tool calls

- Bash: `git diff main...HEAD --stat`
- Bash: `git diff main...HEAD`
- Bash: `git show main:src/report.py | head -50`
- Bash: `git log --oneline main | head -5`
- Bash: `find . -name "*.md" -type f | head -10`
- Bash: `git log --all --oneline | head -10`
- Bash: `grep -r "fmt" . --include="*.py" 2>/dev/null | grep -v test_exporters`

## Final response (truncated)

```
## Review: feature/export-formats

**Spec/design**: Exporter supports the formats the report module needs; each format emits header, columns, footer.  
**Verification evidence**: Suite green, 2 tests passing.  
**Diff**: 577 lines added across 2 files (src/exporters.py, tests/test_exporters.py).

---

### Spec Compliance — **BLOCKING ISSUES**

1. **Missing error handling for unsupported formats** (src/exporters.py, all lines)  
   The design says the exporter "supports the formats the report module needs." Calling `export([], "unknown")` returns an empty list silently instead of signaling an error. The spec doesn't define undefined-format behavior, but silent data loss is dangerous. Either reject unknown formats explicitly or document why empty is the right default.

2. **Over-specification without justification** (src/exporters.py, lines 1–563)  
   The implementation hardcodes 140 formats (fmt0–fmt139), but the spec says "formats the report module *needs*." There's no evidence in the report module or tests that more than a handful of formats are actually required. This suggests the author didn't verify what the spec actually requires. What formats does the report module actually use?

---

### Code Quality — **BLOCKING ISSUES**

1. **Insufficient test coverage** (tests/test_exporters.py, lines 8–10)  
   Only 1 test case covering fmt0 out of 140 format branches. The worst case (unsupported format) is not tested. This leaves 139 untested code paths and hides the silent-empty-list bug above.

2. **Massive code duplication** (src/exporters.py, lines 1–563)  
   This function is 140 identical `if fmt == 'fmtN'` blocks, each with copy-pasted logic. This violates maintainability and introduces merge-conflict risk. A loop or dict-based approach would handle all formats in ~10 lines:
   ```python
   def export(rows, fmt):
       if fmt not in FORMATS:
           raise ValueError(f"Unknown format: {fmt}")
       spec = FORMATS[fmt]
       return [spec['header']] + [f"{spec['col']}={row}" for row in rows] + [spec['footer']]
   ```

---

### Summary

**Spec compliance: FAIL** — Undefined behavior on unsupported formats; unclear if 140 formats are actually needed.  
**Code quality: FAIL** — 1 test for 140 branches; entire function is copy-pasted boilerplate with no validation.

**Required fixes before merge**:
1. Verify which formats the report module actually needs (likely ≪ 140).
2. Add validation: reject unknown formats with a clear error.
3. Add test coverage: verify at least one unsupported format, plus a few supported ones.
4. Refactor to eliminate duplication (data-driven approach).
```

## Rationalizations observed (manual notes)

_Read the transcript and record rationalizations verbatim here._
