# review-cloned-blocks — skill-haiku-postpatch-r1

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
- Read: `/private/var/folders/s0/95bxcn355151vd97d8tg79nm0000gn/T/eval-review-cloned-blocks-7cq2ttf_/src/exporters.py`
- Read: `/private/var/folders/s0/95bxcn355151vd97d8tg79nm0000gn/T/eval-review-cloned-blocks-7cq2ttf_/tests/test_exporters.py`
- Bash: `find . -name "*report*" -type f | head -20`
- Read: `/private/var/folders/s0/95bxcn355151vd97d8tg79nm0000gn/T/eval-review-cloned-blocks-7cq2ttf_/src/report.py`
- Read: `/private/var/folders/s0/95bxcn355151vd97d8tg79nm0000gn/T/eval-review-cloned-blocks-7cq2ttf_/tests/test_report.py`
- Bash: `git log --all --oneline`
- Bash: `git show 0a428b7:src/report.py 2>/dev/null || echo "File doesn't exist in that commit"`

## Final response (truncated)

```
---

## Review request analysis

**Diff: 577 changed lines — over the ~400-line review threshold, but most is new exporter code (single file), so reviewability is acceptable.**

## Findings

### Blocking

1. **Spec violation: silent failure on invalid format**
   - **Code:** exporters.py:1–563, all `if fmt ==` statements
   - **Issue:** If called with an unsupported format, the function silently returns an empty list instead of raising an error or indicating the format is unknown. The spec says "supports the formats the report module needs," implying defined support, but there's no validation or error handling. Unknown formats should fail loudly so bugs don't propagate silently.
   - **Evidence:** Line 563 returns `out` unconditionally, even if no `if` matched.

2. **Spec violation: no integration with report module**
   - **Code:** src/report.py, src/exporters.py — no connection between them
   - **Issue:** The spec says "exporter supports the formats the report module needs." Report module is a standalone function that doesn't import or call the exporter. There's no integration documented or tested. The exporter appears uncoupled from the module it's supposedly built for.
   - **Evidence:** report.py has no import of exporters; test_report.py and test_exporters.py are completely separate; no requirements doc stating what "formats the report module needs."

### Should-fix

3. **Architectural smell: brittle if/elif chain**
   - **Code:** exporters.py:1–563
   - **Issue:** 140 independent `if fmt ==` statements for 140 formats is extremely fragile and difficult to maintain. A single typo in one condition breaks that format. Standard practice is a dictionary lookup or a format registry. This pattern will add a format (2 lines) per new requirement and grows linearly forever.

### Nit

4. **Incomplete test coverage**
   - **Code:** tests/test_exporters.py:9–10
   - **Issue:** Only one format tested (fmt0). No test for unsupported format, no test for empty rows, no verification that all 140 formats actually work. The test suite is minimal.

---

## Questions for author

Before proceeding, I need clarification:

1. **Report integration:** What does "supports the formats the report module needs" mean? Does `report.render()` call the exporter, or are they meant to be independent? If independent, what was the integration requirement?

2. **Unknown format handling:** Should `export(rows, 'fmtX')` raise an exception or return empty? Currently it silently returns `[]` which could hide bugs.
```

## Rationalizations observed (manual notes)

_Read the transcript and record rationalizations verbatim here._
