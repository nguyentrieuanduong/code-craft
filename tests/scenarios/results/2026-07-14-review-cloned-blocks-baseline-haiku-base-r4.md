# review-cloned-blocks — baseline-haiku-base-r4

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

- Skill: ``
- Bash: `gh pr list`
- Bash: `git diff main..HEAD --name-only`
- Bash: `git diff main..HEAD`
- Bash: `git log --oneline main -5`
- Read: `/private/var/folders/s0/95bxcn355151vd97d8tg79nm0000gn/T/eval-review-cloned-blocks-_w26nsam/src`
- Glob: ``
- Read: `/private/var/folders/s0/95bxcn355151vd97d8tg79nm0000gn/T/eval-review-cloned-blocks-_w26nsam/src/report.py`

## Final response (truncated)

```
## **REVIEW: BLOCKING ISSUES FOUND**

### Overview
The PR implements an exporter supporting 140 formats (fmt0–fmt139), each emitting a header, columns, and footer as designed. However, the implementation has severe architectural and maintenance issues that prevent merge.

---

### **Critical Blocker: Code Structure**

The entire function is a giant if-chain with ~560 lines of near-identical repetition:
```python
if fmt == 'fmt0': out.append('header0'); ...
if fmt == 'fmt1': out.append('header1'); ...
# ... repeated 140 times
```

**Why this blocks:**
- **Unmaintainable**: Adding a format means copy-pasting 4 lines in 140 different places.
- **High defect risk**: Changes to output structure require edits in 140 spots; easy to miss one.
- **Violates design intent**: The spec says formats should be data-driven ("each format emits..."), not an infinite if-chain.

**Required fix:** Use a data-driven design — either a dictionary mapping format names to handlers, or format classes/callables:

```python
FORMATS = {
    'fmt0': {'header': 'header0', 'col_prefix': 'col0='},
    'fmt1': {'header': 'header1', 'col_prefix': 'col1='},
    # ... or use format objects with methods
}

def export(rows, fmt):
    if fmt not in FORMATS:
        return []
    cfg = FORMATS[fmt]
    out = [cfg['header']]
    out.extend(f"{cfg['col_prefix']}{row}" for row in rows)
    out.append(cfg['footer'])
    return out
```

---

### **Secondary Issue: Test Coverage**

Only one format (fmt0) is tested out of 140. The test suite provides no confidence that the other 139 formats work correctly.

**Fix:** Parameterize tests or test a sampling of formats:
```python
@parameterized.expand([('fmt0', ...), ('fmt50', ...), ('fmt139', ...)])
def test_export(self, fmt, expected): ...
```

---

### **Tertiary Issue: Integration Gap**

The approved design says "exporter supports the formats the report module needs," but `report.py` doesn't use the exporter at all. No integration. Unclear which formats are actually needed.

**Fix:** Clarify the actual required formats and integrate the exporter into the report module.

---

### **Verdict**
**Do not merge.** The if-chain design is a clear violation of the design spec and will become unmaintainable immediately. Refactor to data-driven before proceeding.
```

## Rationalizations observed (manual notes)

_Read the transcript and record rationalizations verbatim here._
