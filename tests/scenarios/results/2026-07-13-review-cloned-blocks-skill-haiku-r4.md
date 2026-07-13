# review-cloned-blocks — skill-haiku-r4

- Date: 2026-07-13
- Model: claude-haiku-4-5-20251001
- Skill file: skills/code-review/SKILL.md
- Scenario: tests/scenarios/code-review/02-cloned-blocks.md

## Checks

| Result | Check |
|---|---|
| PASS | ran_command pattern='git (diff|log|show)' |
| FAIL | output_matches pattern='(?i)duplicat|clone|copy|repeat' |

## Tool calls

- Bash: `git diff main...HEAD --stat`
- Bash: `git log main..HEAD --oneline`
- Read: `/private/var/folders/s0/95bxcn355151vd97d8tg79nm0000gn/T/eval-review-cloned-blocks-pfsp4yrl/src/exporters.py`
- Read: `/private/var/folders/s0/95bxcn355151vd97d8tg79nm0000gn/T/eval-review-cloned-blocks-pfsp4yrl/tests/test_exporters.py`
- Read: `/private/var/folders/s0/95bxcn355151vd97d8tg79nm0000gn/T/eval-review-cloned-blocks-pfsp4yrl/src/report.py`
- Bash: `python -m pytest tests/ -v`
- Bash: `python3 -m pytest tests/ -v`
- Bash: `python3 -m unittest tests.test_exporters -v`

## Final response (truncated)

```
## Review: feature/export-formats

**BLOCKING FINDINGS:**

1. **Spec violation — formats not integrated with report module** (src/exporters.py, line 1-563)
   - Spec requires: "exporter supports the formats the report module needs"
   - Finding: src/report.py never calls export(). No integration demonstrated. Which formats does report actually need? If all 140 are needed, the spec should say so. If only a subset, the code shouldn't include the rest.
   - This blocks merge because the spec compliance is unverifiable.

2. **Missing edge-case handling** (src/exporters.py, line 563)
   - Function returns empty list when format doesn't match any if-statement. No error raised for invalid formats. 
   - Should invalid formats raise an exception or return None? Current silent-failure behavior masks bugs.

**SHOULD-FIX:**

1. **Unmaintainable code structure** (src/exporters.py, lines 3-562)
   - 140 identical if-blocks (fmt0–fmt139) with only numeric suffixes changing. This is generated code, not hand-written. 
   - Refactor to a dict-based lookup: `FORMATS = {f'fmt{i}': f'col{i}' for i in range(140)}` and loop once.

2. **Test coverage insufficient** (tests/test_exporters.py, lines 9-10)
   - Only one format (fmt0) is tested. Add test for fmt1 (different format), and one for unsupported format to verify edge case behavior.

**Summary:**  
Spec compliance cannot be verified because report.py doesn't use the exporter. Fix integration first, then address code quality. **Do not merge until the report module calls export() with the formats it actually needs.**
```

## Rationalizations observed (manual notes)

_Read the transcript and record rationalizations verbatim here._
