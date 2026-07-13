# review-large-diff-physics — skill-sonnet-postpatch-r1

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
- Bash: `git log main..HEAD --oneline`
- Bash: `git diff main...HEAD -- src/exporters.py`
- Bash: `git diff main...HEAD -- tests/test_exporters.py`
- Bash: `git show main:src/report.py 2>/dev/null || git show HEAD:src/report.py 2>/dev/null || find /private/var/folders/s0/95bxcn355151vd97d8tg79nm0000gn/T/eval-review-`
- Glob: ``
- Read: `/private/var/folders/s0/95bxcn355151vd97d8tg79nm0000gn/T/eval-review-large-diff-physics-hw7_u90q/src/report.py`
- Read: `/private/var/folders/s0/95bxcn355151vd97d8tg79nm0000gn/T/eval-review-large-diff-physics-hw7_u90q/tests/test_report.py`

## Final response (truncated)

```
---

## Review: feature/export-formats

**Diff: 577 changed lines — over the ~400-line review threshold.** This is the first finding: the diff is too large to review reliably and should be split into independently reviewable slices. I will continue as thoroughly as the size allows.

---

### Verdict 1 — Spec compliance

**NOT COMPLIANT — Blocking finding.**

The design states: *"exporter supports the formats the report module needs."*

`src/report.py` contains one function, `render(rows)`, which never calls `export()` and references no format names at all. There is no evidence that `fmt0`–`fmt139` are "the formats the report module needs" — the report module has zero format dependency. Either the exporter was built against an imagined interface, or the report module is incomplete. The spec requirement is unverifiable and, as implemented, unmet: the two modules are not connected.

The structural sub-requirement — *"each format emits header, columns, footer"* — is met by every format block present.

---

### Verdict 2 — Code quality

**NOT MERGEABLE — Multiple blocking findings.**

**Blocking — Catastrophic duplication (`src/exporters.py:1–562`).**
140 format blocks are copy-pasted, differing only in the integer suffix. The entire file collapses to three lines:
```python
def export(rows, fmt):
    n = fmt.removeprefix('fmt')
    return [f'header{n}', *[f'col{n}={r}' for r in rows], f'footer{n}']
```
563 lines of paste is not a style issue — it is a maintenance defect. Any change to the format contract requires 140 edits.

**Blocking — `if` chains instead of `elif` (`src/exporters.py:3, 7, 11, …`).**
All 140 branches use `if`, so every call evaluates all 140 conditions. Functionally harmless for correctness but signals the code was generated without review. With `elif` / a dispatch dict this is also moot.

**Blocking — Silent failure on unknown format (`src/exporters.py:1`).**
`export([], 'csv')` returns `[]` with no error. The function should raise `ValueError` for an unrecognized format; silent empty output will be invisible to callers.

**Blocking — Test coverage is not meaningful (`tests/test_exporters.py:9`).**
The suite has exactly 1 test: `fmt0` with a single row. 139 formats are untested. There is no test for: unknown format, empty rows, multi-row output, or any format above `fmt0`. Claiming "2 tests passing" counts the one test in `test_report.py` — that test covers `render()`, not `export()`. The exporter is effectively untested.

**Should-fix — `sys.path.insert` in test file (`tests/test_exporters.py:4`).**
Path manipulation in test files is fragile; use a `pyproject.toml` / `setup.cfg` src layout or `pytest` `pythonpath` config instead.

---

### Summary

| | Result |
|---|---|
| Spec compliance | **Blocking** — report module does not use the exporter; "formats the report module needs" is unverifiable |
| Code quality | **Blocking** — 563-line copy-paste, silent failure on bad format, 1 test covering 1 of 140 formats |

Do not merge. Required actions before re-review:
1. Connect `report.py` to `export()` or clarify the spec so the integration point is explicit.
2. Replace the 140-block `if`-chain with a computed dispatch (≤5 lines).
3. Add `ValueError` for unknown formats.
4. Add tests: unknown format raises, empty rows, multi-row, at minimum a second named format to prove the pattern generalises.
```

## Rationalizations observed (manual notes)

_Read the transcript and record rationalizations verbatim here._
