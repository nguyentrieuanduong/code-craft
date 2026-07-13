# review-large-diff-physics — skill-haiku-postpatch-r1

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
- Bash: `git log main...HEAD --oneline`
- Read: `/private/var/folders/s0/95bxcn355151vd97d8tg79nm0000gn/T/eval-review-large-diff-physics-owbfpu5n/src/exporters.py`
- Read: `/private/var/folders/s0/95bxcn355151vd97d8tg79nm0000gn/T/eval-review-large-diff-physics-owbfpu5n/tests/test_exporters.py`
- Read: `/private/var/folders/s0/95bxcn355151vd97d8tg79nm0000gn/T/eval-review-large-diff-physics-owbfpu5n/src/report.py`
- Bash: `python -m pytest tests/test_exporters.py -v`
- Bash: `python3 -m pytest tests/test_exporters.py -v 2>&1 | head -30`
- Bash: `python3 -m unittest tests.test_exporters -v`

## Final response (truncated)

```
---

## Code Review: feature/export-formats

**Diff: 577 changed lines — over the ~400-line review threshold.** Defect detection diminishes past this point; recommend splitting into independently reviewable slices before merge.

### Spec Compliance — **BLOCKING FAILURES**

1. **Missing integration with report module** (src/report.py:1–2, violation of core spec requirement)
   - Spec: "exporter supports the formats the report module needs"
   - Report module does not import or reference exporters.py
   - No evidence that exporter supports formats the report module actually needs
   - The exporter supports fmt0–fmt139 arbitrarily; no justification for which formats are required

2. **Test count mismatch** (test_exporters.py:8–14, verification integrity)
   - Author claimed: "2 tests passing"
   - Actual: 1 test in file, 1 test run
   - Discrepancy must be resolved before merge

3. **Missing footer validation** (src/exporters.py:563, spec violation)
   - Spec requires "each format emits header, columns, footer"
   - Function returns early without appending footer if format doesn't match any case
   - Unknown formats return `[]` instead of error or fallback

### Code Quality — **BLOCKING + SHOULD-FIX**

1. **Unmaintainable code duplication** (src/exporters.py:1–563, blocker for maintainability)
   - 140 nearly-identical if blocks (3 lines each × 140 = ~420 lines of repetition)
   - Single variable in each block: format suffix (0–139)
   - Should use dict lookup or loop; current form makes adding/removing formats a massive diff risk
   - This duplication is why the diff is 577 lines for trivial logic

2. **No input validation** (src/exporters.py:1–3, should-fix)
   - Unknown `fmt` parameter produces silent empty list instead of error
   - `rows` parameter type unchecked (expects iterable)

3. **Test coverage inadequate** (tests/test_exporters.py:9–10, should-fix)
   - Single passing test; no coverage for:
     - Unknown format handling
     - Empty rows
     - Different row types/content
     - Multiple rows output correctness

4. **Unused return variable** (src/exporters.py:2, style)
   - `out = []` initialized but no default return — function returns `out` only after all if blocks, leaving unmatched formats to implicitly return None

---

**Blocking findings: 3** — Rewrite required.
**Verdict: Do not merge.** The exporter doesn't integrate with the report module (core spec requirement), test count claim is false, and architecture is unmaintainable. Recommend rebase with:
- Clear definition of which formats report module needs (integrate them)
- Refactor 140-format repetition into data-driven lookup
- Add tests matching actual usage
- Validate author's test claim
```

## Rationalizations observed (manual notes)

_Read the transcript and record rationalizations verbatim here._
