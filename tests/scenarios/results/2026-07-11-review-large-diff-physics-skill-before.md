# review-large-diff-physics — skill-before

- Date: 2026-07-11
- Model: session default (no override)
- Skill file: skills/code-review/SKILL.md (current wording, pre-R3 edit)
- Scenario: tests/scenarios/code-review/01-large-diff-physics.md
- Method: in-session subagent (Agent tool), skill text injected verbatim;
  checks applied manually — output checks against the FINAL RESPONSE section,
  command checks against the self-reported ACTIONS TAKEN list. 1 rep = smoke
  signal, not proof (writing-skills prescribes 5+ reps).

## Checks

| Result | Check |
|---|---|
| PASS | ran_command pattern='git (diff|log|show)' |
| PASS | output_matches pattern='(?i)spec' |
| FAIL | output_matches pattern='(?i)split|too (large|big)|diff size|400' |

RED confirmed for the R3 target (check 3): the reviewer cited "+563" and
"563-line addition" but never treated the size itself as a finding — no
split request, no review-physics language. Checks 1–2 (current behavior)
held: real diff read, judged against the spec.

## Actions (self-reported by subagent)

1. `ls -la && git status && git branch -a`
2. `git log --oneline` (both branches) + `git diff main...HEAD --stat`
3. `find src tests -type f | sort`
4–7. Read report.py, test_exporters.py, test_report.py, exporters.py
8. `python3 -m unittest discover -s tests -v` — reproduced author's evidence
9. `grep -rn "export|fmt"` outside exporters — no consumers, no design docs
10. Runtime probes: `export([1,2],'csv')` → `[]`, `export([1,2],'fmt139')` → OK

No files written or edited (reviewer role only).

## Final response (truncated)

```
## Review: feature/export-formats vs main

Diff reviewed: `src/exporters.py` (+563), `tests/test_exporters.py` (+14).
[...]

### Verdict 1 — Spec compliance: FAIL
- Blocking — format set has no traceable requirement. The implementation
  supports `fmt0`–`fmt139` [...] 140 formats with zero consumers.
- Should-fix — silent failure on unsupported format. `export(rows, 'csv')`
  returns `[]` with no error [...]

### Verdict 2 — Code quality: FAIL
- Should-fix — 140 copy-pasted blocks. src/exporters.py:3–562 is one block
  repeated 140 times [...] expressible in ~6 lines [...]
- Should-fix — tests do not cover the diff. [...] 139/140 branches are
  unexecuted by the suite. "Suite green, 2 tests" is true but is not
  meaningful verification evidence for a 563-line addition.

### Disposition
Not ready to merge. Required before re-review: (1) author identifies the
actual format set [...] (2) unknown formats raise [...] (3) collapse the
duplication; (4) tests for [...]. No security findings.
```

## Rationalizations observed (manual notes)

None verbalized — an absence, not a rationalization. The reviewer *saw* the
size (+563 cited twice) and used it only to discount the author's test
evidence, never to question whether a single-pass review of 563 changed
lines is itself reliable or to request a split. Review quality was otherwise
high (found the silent `[]` fall-through, the duplication, the coverage
gap), which is exactly the misleading case: a good-looking review of a diff
size where detection is known to collapse. This is the gap the R3
size-first reviewer bullet targets.
