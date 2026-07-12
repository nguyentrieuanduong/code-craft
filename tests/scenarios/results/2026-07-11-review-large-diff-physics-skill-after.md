# review-large-diff-physics — skill-after

- Date: 2026-07-11
- Model: session default (no override)
- Skill file: skills/code-review/SKILL.md (R3 edit: size-first reviewer
  bullet + changed-LOC in the request-package Diff line)
- Scenario: tests/scenarios/code-review/01-large-diff-physics.md
- Method: in-session subagent (Agent tool), skill text injected verbatim;
  checks applied manually — output checks against the FINAL RESPONSE section,
  command checks against the self-reported ACTIONS TAKEN list. 1 rep per
  wording = smoke signal, not proof (writing-skills prescribes 5+ reps).

## Checks

| Result | Check |
|---|---|
| PASS | ran_command pattern='git (diff|log|show)' |
| PASS | output_matches pattern='(?i)spec' |
| PASS | output_matches pattern='(?i)split|too (large|big)|diff size|400' |

GREEN: 3/3 (was 2/3 before the edit — see the skill-before file).

## Actions (self-reported by subagent, condensed)

1. Sandbox/git state survey; `git diff main...HEAD --stat` first (577 lines)
2. Read design anchor (report.py on main and branch), both test files, full
   exporters.py; searched repo for any format requirement — none
3. `python3 -m unittest discover -s tests -v` — independently reproduced the
   author's "2 tests passing"
4. Runtime probes: `export([1],'csv')` → `[]` (silent), `export([],'fmt0')`
   → header/footer only
5. Wrote review.md in the sandbox with both verdicts

## Final response (truncated)

```
First, the size gate: git diff main...HEAD --stat shows 577 changed lines
(src/exporters.py +563, tests/test_exporters.py +14). That is past the
~400-line threshold where reviewer defect detection collapses — this should
be split into independently reviewable slices. I reviewed the full diff
anyway, which was feasible only because the 560 lines are one 4-line
pattern repeated 140 times; the split falls out of finding S1 naturally.

Verdict 1 — Spec compliance: FAIL. [140 formats with no consumer; core
design clause unsatisfied or undemonstrated]

Verdict 2 — Code quality: FAIL.
- B1 — 140 unconsumed formats implement no identifiable requirement
- S1 — one 4-line block repeated 140 times; dict + one code path replaces
  560 lines with ~a dozen
- S2 — unknown format fails silently: export([1], 'csv') → []
- S3 — tests cover 1 of 140 formats (0.7%), one happy-path row [...]

Disposition: not mergeable. Required before re-review: B1, S1, S2, S3. The
resulting diff should land under the 400-line threshold on its own.
```

## Rationalizations observed (manual notes)

None. The size-first bullet fired as the literal first review act (`--stat`
before reading any file), the collapse physics was stated to the author,
and the split recommendation was integrated with the duplication finding
rather than pasted as boilerplate. "Review as thoroughly as the size allows
anyway" prevented the opposite failure — refusing to review until split.
Substantive findings match the before run (silent `[]`, duplication,
coverage), so the added bullet did not displace the rest of the review.
