# review-cloned-blocks — skill-after (regression)

- Date: 2026-07-11
- Model: session default (no override)
- Skill file: skills/code-review/SKILL.md (R3 edit; NO R7 duplication line —
  dropped per the skill-before result: already passing, no failing test)
- Scenario: tests/scenarios/code-review/02-cloned-blocks.md
- Method: in-session subagent (Agent tool), skill text injected verbatim;
  checks applied manually — output checks against the FINAL RESPONSE section,
  command checks against the self-reported ACTIONS TAKEN list. 1 rep per
  wording = smoke signal, not proof (writing-skills prescribes 5+ reps).

## Checks

| Result | Check |
|---|---|
| PASS | ran_command pattern='git (diff|log|show)' |
| PASS | output_matches pattern='(?i)duplicat|clone|copy|repeat' |

GREEN: 2/2. Purpose of this run: regression guard — confirm the R3
size-first bullet does not displace the duplication finding that current
wording already produces (skill-before run: 2/2).

## Actions (self-reported by subagent, condensed)

1. Sandbox/git survey; `git diff main...HEAD --stat` first (577 lines)
2. Read report.py, both test files, all 563 lines of exporters.py, setup.sh
3. Ran both test modules — verified author's "suite green" (2/2)
4. Evidence script: `export()` returns `[]` for 'csv'/None/'fmt140'; all
   140 branches verified uniform; `grep -c "if fmt =="` → 140
5. Wrote code-review.md in the sandbox

## Final response (truncated)

```
Yes — two blocking findings. Do not merge.

Diff size first: 577 changed lines — past the ~400-line mark where reviewer
defect detection collapses. Normally I'd ask you to split into
independently reviewable slices; here the size is caused entirely by
duplication (S1 below), so fixing that cures it.

Verdict 1 — Spec compliance: FAIL
- [Blocking] B1 — No traceable requirement for any of the 140 formats. [...]

Verdict 2 — Code quality: FAIL
- [Blocking] B2 — Unsupported format fails silently. [...] A typo'd format
  silently emits an empty export instead of erroring [...]
- [Should-fix] S1 — 563 lines of copy-paste. 140 stanzas identical modulo
  an integer [...] A table-driven version is ~6 lines [...]
- [Should-fix] S2 — Tests not meaningful. One test of 140 branches [...]
```

## Rationalizations observed (manual notes)

None. Duplication finding intact and load-bearing ("563 lines of
copy-paste", "140 stanzas identical modulo an integer") — the reviewer even
connected the two mechanisms: the size violation is *caused by* the
duplication, so one fix cures both. Decision from the before run stands:
no dedicated duplication line needed in the skill; this scenario remains in
the corpus as the tripwire if that ever regresses.
