# review-cloned-blocks — skill-haiku-round2-r1

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
- Bash: `git diff main...HEAD`
- Read: `/private/var/folders/s0/95bxcn355151vd97d8tg79nm0000gn/T/eval-review-cloned-blocks-r0b7smb7`

## Final response (truncated)

```
## Code Review: feature/export-formats

**Diff: 577 changed lines — OVER the ~400-line review threshold.** This signals either an error in the design/approach, or the diff should be split into independently reviewable slices. Proceeding with review anyway.

---

### Blocking Finding: Massive Code Duplication

**Evidence:** src/exporters.py lines 1–560 contain 140+ identical if-blocks (fmt0 through fmt139), each repeating the exact same pattern with only the format number changing:

```python
if fmt == 'fmtN':
    out.append('headerN')
    out.extend('colN=' + str(row) for row in rows)
    out.append('footerN')
```

This is the measured signature of generated code — duplication at ~8×. The implementation violates the foundational principle of avoiding cloned blocks.

**Fix required:** Replace the single massive function with a data-driven approach. Either:
- A dictionary of format specs: `FORMATS = {'fmt0': {...}, 'fmt1': {...}}` + loop
- Or a parameterized format string/template that the loop applies

This would reduce the file to ~20 lines and be maintainable. The current code is unmergeable.

---

### Should-Fix Finding: Minimal Test Coverage

**Evidence:** tests/test_exporters.py line 9–10 — only one format is tested (fmt0). No tests for:
- Non-existent format fallback/error handling
- Empty rows edge case
- Multi-row behavior (only tests one row)

---

### Spec Compliance

Once deduplication is done: each format correctly emits header, columns, footer ✓. The data structure you refactor into should ensure this invariant holds.

**Do not merge** until the duplication is eliminated. Request a revised diff with a single parameterized export function.
```

## Rationalizations observed (manual notes)

_Read the transcript and record rationalizations verbatim here._
