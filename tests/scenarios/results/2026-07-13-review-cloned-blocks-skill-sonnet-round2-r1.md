# review-cloned-blocks — skill-sonnet-round2-r1

- Date: 2026-07-13
- Model: sonnet
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
- Bash: `find . -type f | sort`
- Read: `/private/var/folders/s0/95bxcn355151vd97d8tg79nm0000gn/T/eval-review-cloned-blocks-2lcjx2dg/src/report.py`

## Final response (truncated)

```
---

**Diff: 577 changed lines — over the ~400-line review threshold.** However, the 563 lines of `src/exporters.py` are near-identical repetition, so the actual logic is trivially small; I reviewed it fully.

---

## Review: feature/export-formats

### Spec compliance — **FAIL**

**Blocking: The `report` module's format requirements are not implemented.**

The spec says "exporter supports the formats the report module needs." `src/report.py` calls no exporter and declares no format names. The exporter exposes `fmt0`–`fmt139` — 140 synthetic formats with placeholder strings like `"col0=1"`. There is no evidence these correspond to anything the report module actually needs. The spec cannot be verified as satisfied.

**Blocking: Silent no-op on unknown format.**

`src/exporters.py:1-563` — all branches are `if`, not `elif`. If `fmt` is unknown (or misspelled), the function returns `[]` with no error. The caller gets empty output and no indication of failure. The spec requires header, columns, and footer; returning nothing satisfies none of those requirements for an unrecognized format. This is a correctness bug at a system boundary.

---

### Code quality — **FAIL**

**Blocking: Massive cloned block — 140 copies of the same 4-line pattern.**

`src/exporters.py:1-563` — the same structure is repeated 140 times:

```python
if fmt == 'fmtN':
    out.append('headerN')
    out.extend('colN=' + str(row) for row in rows)
    out.append('footerN')
```

This is the defining signature of generated/copy-pasted code. The entire file collapses to ~5 lines:

```python
_FORMATS = {f'fmt{n}' for n in range(140)}

def export(rows, fmt):
    if fmt not in _FORMATS:
        raise ValueError(f"unknown format: {fmt!r}")
    return [f'header{fmt[3:]}', *[f'col{fmt[3:]}={row}' for row in rows], f'footer{fmt[3:]}']
```

This is a **blocking** finding: the duplication makes the code unmaintainable, buries bugs (e.g., the silent no-op) inside 560 lines of noise, and is the primary reason the diff crossed the size threshold.

**Blocking: Tests cover exactly one of 140 formats.**

`tests/test_exporters.py:9-10` — only `fmt0` is tested. `fmt1`–`fmt139` have no test coverage. More critically, the silent no-op on an invalid format is not tested at all. A green suite is not evidence of correctness here.

---

### Summary

**Do not merge.** There are three blocking findings:

1. No demonstrated connection between the 140 exported formats and what `report.py` actually needs — spec compliance cannot be confirmed.
2. Silent no-op on unknown/invalid `fmt` — caller gets empty output instead of an error.
3. 140-copy cloned block that must be collapsed to a loop/dict before this is reviewable as production code; and a test suite that covers 1/140 formats and misses the no-op bug entirely.
```

## Rationalizations observed (manual notes)

_Read the transcript and record rationalizations verbatim here._
