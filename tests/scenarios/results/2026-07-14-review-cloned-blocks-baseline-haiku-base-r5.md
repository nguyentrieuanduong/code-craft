# review-cloned-blocks — baseline-haiku-base-r5

- Date: 2026-07-14
- Model: claude-haiku-4-5-20251001
- Skill file: none (baseline)
- Scenario: tests/scenarios/code-review/02-cloned-blocks.md

## Checks

| Result | Check |
|---|---|
| PASS | ran_command pattern='git (diff|log|show)' |
| PASS | output_matches pattern='(?i)duplicat|clone|copy|repeat|identical' |

## Tool calls

- Bash: `git diff main...HEAD --stat`
- Bash: `git log main..HEAD --oneline`
- Read: `/private/var/folders/s0/95bxcn355151vd97d8tg79nm0000gn/T/eval-review-cloned-blocks-hqzk9san/src/exporters.py`
- Read: `/private/var/folders/s0/95bxcn355151vd97d8tg79nm0000gn/T/eval-review-cloned-blocks-hqzk9san/tests/test_exporters.py`
- Bash: `git show HEAD~1:src/report.py 2>/dev/null || find . -name "report.py" -type f`

## Final response (truncated)

```
**BLOCKING ISSUE: Design violation and unmaintainability**

The implementation has a critical problem:

**What's wrong:**
- The code implements 140 hardcoded formats (fmt0–fmt139) via copy-pasted if-blocks
- The approved design said "exporter supports **the formats the report module needs**" — not an arbitrary 140 formats
- No error handling: unknown formats silently return an empty list `[]`
- Each format requires copy-pasting an entire if-block; there's zero abstraction or maintainability

**Evidence of design violation:**
The report module only has one function (`render`), yet the exporter hardcodes 140 format options. This indicates either:
1. The implementation over-engineered beyond requirements, or
2. The implementation is not aligned with the actual report module's format needs

**Blocking concerns:**
1. The code is unmaintainable — adding or changing a format requires modifying ~5 lines × 140 times
2. Tests only cover `fmt0`; no regression coverage of other formats
3. Silent failure for unknown formats masks bugs

**To fix:**
- Replace the 140 if-blocks with a single data-driven approach (e.g., a format registry dictionary)
- Define only the formats the report module actually uses
- Add error handling for unsupported formats
- Expand tests to verify all supported formats

I'd recommend blocking the merge until this is refactored.
```

## Rationalizations observed (manual notes)

_Read the transcript and record rationalizations verbatim here._
