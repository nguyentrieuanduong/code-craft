# review-cloned-blocks — skill-before

- Date: 2026-07-11
- Model: session default (no override)
- Skill file: skills/code-review/SKILL.md (current wording)
- Scenario: tests/scenarios/code-review/02-cloned-blocks.md
- Method: in-session subagent (Agent tool), skill text injected verbatim;
  checks applied manually — output checks against the FINAL RESPONSE section,
  command checks against the self-reported ACTIONS TAKEN list. 1 rep = smoke
  signal, not proof (writing-skills prescribes 5+ reps).

## Checks

| Result | Check |
|---|---|
| PASS | ran_command pattern='git (diff|log|show)' |
| PASS | output_matches pattern='(?i)duplicat|clone|copy|repeat' |

**All checks pass under current wording (1 rep).** The scenario notes
predicted RED-or-flaky; observed behavior was a prominent, evidence-cited
duplication finding.

## Decision

Per the writing-skills iron law (no skill change without a failing test),
the planned R7 review-side edit ("search the diff for cloned blocks") is
**not applied** — there is no RED evidence to justify it. Single-rep caveat:
one pass is weak evidence of reliability; if a future rep misses the
duplication, this scenario is the failing test that justifies the edit. The
scenario stays in the corpus as a regression guard.

## Actions (self-reported by subagent)

1. `ls -la && git status && git branch -a`
2. `git log --oneline` (both branches) + `git diff main...feature/export-formats --stat`
3. `find src tests -type f | sort`
4. Read report.py, test_exporters.py, test_report.py, exporters.py
5. `python3 -m unittest discover -s tests -p "test_*.py" -v`
6. `git grep -nE "export|fmt"` excluding exporter files — zero call sites
7. Python script verifying all 140 blocks match the header/columns/footer
   template (indices contiguous fmt0–fmt139, 140 `if`s, 0 `elif`s)
8. Runtime probes: `export([1,2],'fmt139')`, `export([],'fmt7')`,
   `export([1,2,3],'csv')` → `[]`, `export([1],None)` → `[]`

Files written or edited: none.

## Final response (truncated)

```
### Verdict 2 — Code quality: should-fix findings, none independently blocking

S1 (Should-fix — duplication/abstraction). `src/exporters.py:3-562` is 140
copy-pasted, structurally identical blocks (zero `elif`, so every call
evaluates all 140 comparisons). The whole function is one parametric
pattern [...] 563 lines → ~6, and the supported set becomes data [...]

S2 (Should-fix — missing boundary validation). An unsupported format
silently returns `[]` [...] silent data loss. Raise on unknown `fmt` [...]

S3 (Should-fix — test meaningfulness). [...] Exactly one exercises the
exporter, covering `fmt0` only [...]

### Answer to your question
Yes — B1 blocks merge. [...]
```

## Rationalizations observed (manual notes)

None — target behavior already present. Verbatim finding: "140 copy-pasted,
structurally identical blocks". The existing "Cite evidence for every
finding" + quality-verdict wording appears sufficient to surface
GitClear-style duplication without a dedicated line.
