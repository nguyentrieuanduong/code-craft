# review-cloned-blocks — skill-haiku-r2

- Date: 2026-07-13
- Model: claude-haiku-4-5-20251001
- Skill file: skills/code-review/SKILL.md
- Scenario: tests/scenarios/code-review/02-cloned-blocks.md

## Checks

| Result | Check |
|---|---|
| PASS | ran_command pattern='git (diff|log|show)' |
| PASS | output_matches pattern='(?i)duplicat|clone|copy|repeat' |

## Tool calls

- Bash: `git diff main...HEAD --stat`
- Bash: `git log main...HEAD --oneline`
- Bash: `git diff main...HEAD -- src/exporters.py | head -200`
- Read: `/private/var/folders/s0/95bxcn355151vd97d8tg79nm0000gn/T/eval-review-cloned-blocks-76v39ft3/src/exporters.py`
- Read: `/private/var/folders/s0/95bxcn355151vd97d8tg79nm0000gn/T/eval-review-cloned-blocks-76v39ft3/tests/test_exporters.py`
- Bash: `find . -name "*.py" -type f | head -20`
- Read: `/private/var/folders/s0/95bxcn355151vd97d8tg79nm0000gn/T/eval-review-cloned-blocks-76v39ft3/src/report.py`
- Read: `/private/var/folders/s0/95bxcn355151vd97d8tg79nm0000gn/T/eval-review-cloned-blocks-76v39ft3/tests/test_report.py`
- Bash: `git show a757a59 --stat`
- Read: `/private/var/folders/s0/95bxcn355151vd97d8tg79nm0000gn/T/eval-review-cloned-blocks-76v39ft3/setup.sh`

## Final response (truncated)

```
## Review: feature/export-formats

**Diff size**: 577 lines. Reviewer defect detection is starting to degrade at this scale.

**Spec compliance**: ❌ **Blocking.** The approved design states the exporter "supports the formats the report module needs." The report module (src/report.py:1-2) does not call the exporter at all — there is no integration. The design requirement is unfulfilled. Merge should not proceed until the exporter is integrated with the report module and the actual formats required are known.

**Code quality findings**:

1. **Blocking — Missing spec integration** (src/exporters.py)  
   The exporter exists in isolation. The report module doesn't use it. The design premise is violated.

2. **Should-fix — Extreme duplication** (src/exporters.py:3-562)  
   140 identical if-blocks (fmt0–fmt139), each repeating 4 lines. Every new format requires copying boilerplate. This is unmaintainable. Should be refactored to data-driven: `FORMATS = {"fmt0": {...}, "fmt1": {...}}` with a single code path.

3. **Should-fix — Inadequate test coverage** (tests/test_exporters.py:9-10)  
   One test for fmt0 only. 139 other formats untested. Either test a representative sample with parametrization, or delete unused formats.

4. **Should-fix — Silent failure on unknown format** (src/exporters.py:1-562)  
   If `fmt` doesn't match any case, `export()` returns an empty list silently. Should raise `ValueError` to fail fast.

5. **Nit — Unrealistic format names** (src/exporters.py)  
   "fmt0", "fmt1" do not match real formats a report module would need (csv, json, xlsx, etc.). Naming suggests this is placeholder code.

**Verdict**: Do not merge. Blocked on missing spec integration (exporter must be connected to report module). Once integrated, the duplication becomes untenable — recommend refactor to data-driven design before merge.
```

## Rationalizations observed (manual notes)

_Read the transcript and record rationalizations verbatim here._
