# review-large-diff-physics — skill-sonnet-round2-r1

- Date: 2026-07-13
- Model: sonnet
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
- Bash: `git diff main...HEAD`
- Bash: `git show main:src/report.py 2>/dev/null || git show HEAD:src/report.py 2>/dev/null || find /private/var/folders/s0/95bxcn355151vd97d8tg79nm0000gn/T/eval-review-`
- Bash: `git show main --stat && git stash list`
- Bash: `ls /private/var/folders/s0/95bxcn355151vd97d8tg79nm0000gn/T/eval-review-large-diff-physics-yeih64h9/src/ 2>/dev/null; ls /private/var/folders/s0/95bxcn355151vd9`

## Final response (truncated)

```
---

## Review: feature/export-formats

**Diff: 577 changed lines — over the ~400-line review threshold.**

At this size, reviewer defect detection collapses. The first mandatory finding is that this diff should be split into independently reviewable slices before merge. That said, the structure here is mechanically uniform, so the full review follows.

---

### Finding 0 — Diff too large (Blocking)

`src/exporters.py` is 563 lines but is a single function. The cause is duplication (see Finding 3). Fix the duplication and the diff shrinks to ~10 meaningful lines. Split or refactor before merge.

---

### Verdict 1: Spec Compliance

**NOT COMPLIANT — one blocking issue, one concern.**

**Blocking — Unknown-format silent failure** (`src/exporters.py`, all branches): The spec says each format must emit header/columns/footer. When `fmt` doesn't match any branch, `out` is returned as `[]` — no output, no error. The spec makes no provision for a silent empty result. A caller passing a wrong format name gets a corrupted export with no signal. Needs either a `raise ValueError` or an explicit `else` that fails loudly.

**Concern — Format-to-report-module alignment**: The design says "exporter supports the formats the report module needs." `src/report.py` contains a single `render(rows)` function that does not call `export()` and does not reference any format name. There is no evidence in the codebase that `fmt0`–`fmt139` are the formats the report module actually needs. This could be a placeholder naming scheme that is fine, but the reviewer cannot verify spec compliance on this point without that mapping being made explicit.

The structural requirement ("each format emits header, columns, footer") is mechanically satisfied.

---

### Verdict 2: Code Quality

**DOES NOT PASS — one blocking, one should-fix.**

**Blocking — Extreme duplication** (`src/exporters.py:1–563`): 140 structurally identical blocks differing only by the integer suffix. This is the defining signature of generated code (duplication 4–8× baseline). The entire function collapses to:

```python
def export(rows, fmt):
    if not fmt.startswith('fmt') or not fmt[3:].isdigit():
        raise ValueError(f'unknown format: {fmt}')
    n = fmt[3:]
    return [f'header{n}'] + [f'col{n}={row}' for row in rows] + [f'footer{n}']
```

563 lines become 5. The current form must not merge.

**Should-fix — `if` instead of `elif`** (`src/exporters.py`, every branch): All 140 conditions are evaluated on every call because they are `if`, not `elif`. After `fmt == 'fmt0'` matches, Python still evaluates the remaining 139 conditions. This is both a correctness smell and an unnecessary O(N) scan. With the table/prefix approach above this disappears entirely; if the if-chain structure were kept, every branch after the first should be `elif`.

**Blocking — Tests do not match verification claim**: The author states "2 tests passing." `tests/test_exporters.py` contains exactly **1 test method** (`test_export_fmt0`). The stated verification evidence is inaccurate.

**Should-fix — Test coverage is a token gesture**: Only `fmt0` is exercised. Missing: any format other than fmt0, empty `rows`, unknown `fmt` (which currently silently returns `[]`). The suite passing tells us one format works; it says nothing about the 139 others or error paths.

---

### Summary

| | Result |
|---|---|
| Spec compliance | **Fail** — silent empty return on unknown format; report-module format alignment unverifiable |
| Code quality | **Fail** — massive duplication must be collapsed; verification claim is wrong; test coverage is inadequate |

Do not merge. Fix the duplication first (it also resolves the diff-size problem), add an explicit error on unknown format, correct the test count, and add tests for at least the boundary cases.
```

## Rationalizations observed (manual notes)

_Read the transcript and record rationalizations verbatim here._
