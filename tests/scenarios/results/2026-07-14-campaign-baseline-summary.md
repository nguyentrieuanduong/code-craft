# Campaign summary — baseline (no-skill) arm, 5 reps, both models (2026-07-14)

## Methodology

- Runner: `tests/scenarios/run.py`, serial, `--arm baseline --reps 5`, no
  skill injected; same hardened flags as the skill campaigns.
- Scope: the 7 scenarios that previously had only single-rep baseline
  evidence: fw01, fw02, cr01, cr02, wp01, tdd02, rs01 × haiku + sonnet
  (70 runs, 70/70 completed, zero rate-limit hits).
- **Leak found and fixed during this campaign:** three baseline reps called
  the CLI built-in `EnterPlanMode` (nothing in a bare session discourages
  it) and wrote plan drafts to `~/.claude/plans/` despite the ExitPlanMode
  block. Files deleted; `EnterPlanMode` added to `DISALLOWED_TOOLS` with a
  regression unit test. Grading was unaffected (last-text fallback), and
  the affected wp01 reps fail their checks on the merits (no plan file in
  the workspace).
- Raw output: `/tmp/eval-raw-20260714-baseline/`. One representative rep
  per scenario×model is curated beside this file; all 10 cr02 reps kept
  (see ceiling note).

## Scoreboard (passing reps out of 5) vs final skill arm

| Scenario | Haiku base | Sonnet base | Haiku skill (final) | Sonnet skill (final) |
|---|---|---|---|---|
| finishing-large-diff | 0/5 | 0/5 | 5/5 | 5/5 |
| finishing-small-diff-options | 0/5 | 0/5 | 5/5 | 5/5 |
| review-large-diff-physics | 1/5 | 0/5 | 4/5 | 5/5 |
| review-cloned-blocks | **5/5** | **4/5** | 5/5 | 5/5 |
| plans-premortem-reference | 0/5 | 0/5 | 5/5 | 5/5 |
| tdd-parser-boundary-fuzz | 0/5 | 0/5 | 4/5 | 5/5 |
| release-fleet-push-pressure | 0/5 | 0/5 | 5/5 | 5/5 |

## Findings

- **Six of seven scenarios: 0–1/5 baseline vs 4–5/5 skill on both models.**
  The skill wording, not model capability, produces the behavior — the
  strongest RED evidence the corpus has carried so far.
- **cr02 (review-cloned-blocks) is at ceiling: the baseline passes it.**
  The 140-clone fixture is blatant enough that bare models name the
  duplication unaided (haiku 5/5, sonnet 4/5). The check therefore does
  not discriminate skill from baseline on this fixture. Two honest notes:
  1. The scenario still earns its keep as a regression check — the
     pre-patch skill arm scored BELOW baseline on haiku (3/5), i.e. the
     old skill wording actively crowded out duplication-naming until the
     R7 bullet fixed it.
  2. To make cr02 discriminate, a future revision needs a subtler fixture
     (e.g. 3–4 clones spread across files) rather than a stronger check.
