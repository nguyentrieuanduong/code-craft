# review-large-diff-physics — skill-haiku-postpatch-r3

- Date: 2026-07-13
- Model: claude-haiku-4-5-20251001
- Skill file: skills/code-review/SKILL.md
- Scenario: tests/scenarios/code-review/01-large-diff-physics.md

## Checks

| Result | Check |
|---|---|
| PASS | ran_command pattern='git (diff|log|show)' |
| PASS | output_matches pattern='(?i)spec' |
| PASS | output_matches pattern='(?i)split|too (large|big)|diff size|400' |

## Tool calls

- Bash: `git diff main...HEAD --stat`
- Bash: `git log main..HEAD --oneline`
- Bash: `git diff main...HEAD`
- Read: `/private/var/folders/s0/95bxcn355151vd97d8tg79nm0000gn/T/eval-review-large-diff-physics-9h33o0g9/src/exporters.py`
- Bash: `python -m pytest tests/test_exporters.py -v`
- Bash: `python3 -m pytest tests/test_exporters.py -v`
- Bash: `python3 -m unittest tests.test_exporters -v`
- Bash: `wc -l tests/test_exporters.py && grep -c "def test_" tests/test_exporters.py`

## Final response (truncated)

```
---

## Review: feature/export-formats

**Diff: 577 changed lines — over the ~400-line review threshold.** For a new module, this is substantial but reviewable since the code is highly repetitive. The large size is driven by the implementation strategy (140 sequential if-statements), which compounds the already large diff.

### Spec Compliance

**❌ BLOCKING — Verification evidence false:**
- Author claimed "2 tests passing" but `tests/test_exporters.py` contains only 1 test method (`test_export_fmt0`).
- Test run confirms: 1 test ran, not 2.
- **Evidence:** `tests/test_exporters.py` has 14 lines total, 1 `def test_` method (line 9–10). `python3 -m unittest` output: "Ran 1 test".

**⚠️ BLOCKING — Insufficient test coverage:**
- Spec: "exporter supports the formats the report module needs; each format emits header, columns, footer."
- Implementation: 140 format handlers (fmt0–fmt139), each following the same pattern (header → columns → footer).
- Test coverage: 1 test for 1 format out of 140.
- Missing: No tests for multiple formats, no boundary tests (fmt139 exists but untested), no tests for invalid format behavior.
- **Evidence:** `tests/test_exporters.py` lines 9–10 test only fmt0. No other format tests present.

**❌ BLOCKING — Silent failure for invalid format:**
- If `fmt` doesn't match any of fmt0–fmt139, the function returns an empty list (`out = []` with no handling).
- The spec requires "exporter supports the formats the report module needs" — unsupported formats should be detectable, not silently ignored.
- **Evidence:** `src/exporters.py` lines 1–2 initialize `out = []`; lines 3–562 are if-statements with no else clause; line 563 returns `out` (still empty if no match).

### Code Quality

**❌ BLOCKING — Unmaintainable code structure:**
- 560 lines of nearly identical code (lines 3–562): 140 copy-pasted if-blocks, each with 4 lines of nearly identical logic.
- This violates the DRY principle and creates extreme maintenance risk: adding a new format requires adding 4 more lines in the right place; changing output logic requires changes in 140 places.
- A data-driven design (e.g., dictionary of format definitions with a loop) would be ~50 lines and maintainable.
- **Evidence:** `src/exporters.py` lines 3–6 (fmt0 block) repeated 139 times with only the format name changing.

**Nit — Test imports system path:**
- `tests/test_exporters.py` line 3 uses `sys.path.insert(0, "src")` instead of proper package structure or relative imports.
- This works but is fragile; better to use `from src.exporters import export` if the package is properly structured, or use `-m pytest` from the root with proper `__init__.py` files.

### Verdict

| Dimension | Result |
|-----------|--------|
| **Spec Compliance** | ❌ BLOCKING |
| **Code Quality** | ❌ BLOCKING |

**Cannot merge.** This PR violates the spec (silent failure on unsupported formats, insufficient test coverage) and ships unmaintainable code (560 lines of repetition). The verification evidence is also false (claims 2 tests, delivers 1). 

Author should:
1. Fix verification claims (recount actual tests).
2. Add tests for multiple formats and edge cases (e.g., fmt139, invalid format).
3. Refactor the implementation to use a data-driven pattern (dict + loop) or similar to reduce from 560 to ~50 lines.
4. Add error handling for unsupported formats (raise exception or return explicit error marker).
```

## Rationalizations observed (manual notes)

_Read the transcript and record rationalizations verbatim here._
