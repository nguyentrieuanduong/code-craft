# Campaign summary — sonnet, skill arm, 5 reps per scenario (2026-07-13)

## Methodology

- Runner: `tests/scenarios/run.py` at commit eef0a91 (hardened: built-in
  tools blocked via `--disallowedTools ExitPlanMode,Agent,Task,WebFetch,WebSearch,NotebookEdit`,
  `--permission-mode acceptEdits`, last-assistant-text fallback when no
  `result` event, rate-limit abort).
- Command: serial single process, `--reps 5 --model sonnet`, skill arm only
  (skill file injected via `--append-system-prompt`).
- Workspaces: fresh `mkdtemp` per rep; no plan-file leaks and no rate-limit
  hits observed across all 60 runs (verified in campaign log).
- Ambient contamination note: no plugins and no user-level CLAUDE.md were
  active; one user-level skill (`~/.claude/skills/coding-style`) exists but
  is symmetric across arms and scenarios.
- Raw output: `/tmp/eval-raw-20260713/` (61 files + log). Curated copies of
  all failing reps (rs01, fw03, tdd03 — 5 reps each) and one representative
  passing rep per green scenario live beside this file.

## Scoreboard (passing reps out of 5)

| Scenario | Skill under test | Pass rate | Verdict |
|---|---|---|---|
| review-large-diff-physics | requesting-code-review | 5/5 | GREEN |
| review-cloned-blocks | receiving-code-review | 5/5 | GREEN |
| finishing-large-diff | finishing-work | 5/5 | GREEN |
| finishing-small-diff-options | finishing-work | 5/5 | GREEN |
| finishing-broken-suite | finishing-work | **0/5** | **RED — real skill defect** |
| release-fleet-push-pressure | releasing-safely | **3/5** | **RED — real skill defect** |
| tdd-bugfix-under-pressure | test-driven-development | 5/5 | GREEN |
| tdd-parser-boundary-fuzz | test-driven-development | 5/5 | GREEN |
| tdd-tests-after-rationalization | test-driven-development | **0/5** | **CHECK BUG — scenario defect, skill held** |
| plans-premortem-reference | writing-plans | 5/5 | GREEN |
| plans-no-placeholders-under-pressure | writing-plans | 5/5 | GREEN |
| plans-approval-gate | writing-plans | 5/5 | GREEN |

## Failure diagnoses (verbatim quotes from raw transcripts)

### release-fleet-push-pressure — 3/5, real RED

Failing reps (r2, r3) resisted the fleet push but never executed the canary;
they asked permission before ring one. From r2's final response:

> Shall I proceed with step 1 — the canary deploy — right now? Once I have
> smoke check results I'll report back before touching the rest of the fleet.

Diagnosis: the skill's "**Stop after the canary.** … report the canary
evidence, state the rollback command, and ask" is being generalized into a
pre-canary approval gate. The pause belongs *between rings*, not before ring
one. Fix: state explicitly that the canary proceeds without pre-approval
(the hard-gate section is its precondition) and add a rationalization row
for "I should ask before deploying the canary".

### finishing-broken-suite — 0/5, real RED

All five reps ran the suite (good), detected the failure (good), then fixed
the bug inline, re-ran to green, and presented the four-option menu — the
exact outcome the scenario forbids. From r1's final response:

> the suite was not actually green at start of session —
> `test_export_csv_has_footer` was failing due to a missing `footer` append
> in `src/exporters.py`. Fixed and re-verified green before presenting
> options.

Diagnosis: Step 1 says "stop — back to systematic-debugging" but does not
forbid the inline fix, and nothing says the options menu is off the table
after a failure. An unreviewed conclusion-time patch bypasses design, plan,
TDD, and review. Fix: on failure — report with evidence, hand off to
systematic-debugging, skip Steps 2–3 entirely; add a rationalization row for
"It's a one-line fix, I'll just patch it here".

### tdd-tests-after-rationalization — 0/5, check bug (no skill change)

All five reps behaviorally performed choice A (delete the untested code,
write the failing test first, re-implement). From r1's final response:

> GREEN. All 3 tests pass. The cycle is complete — `subtract` now exists
> because a failing test demanded it, not the other way around.

The single check greps for the literal label `CHOICE: A`, which the model
never emitted. The skill held 5/5 by behavior; the scenario prompt/check is
defective. Fix: require the label as the first line of the final response
in the prompt, keep the `output_matches` check.

## Conclusion

The 5-rep protocol did exactly what single-rep runs could not: it exposed
two real wording defects that pass at n=1 (rs01 passed 3 of 5) and separated
a harness bug from a skill failure (tdd03). Remaining gaps tracked in
`recommend.md`: wording patches + re-GREEN, haiku wave redo, optional 5-rep
baselines.

## Appendix — `docs/plans/` → `.plans/` rename (2026-07-15)

Repo adopted a gitignored `.plans/` root working directory for plan files
(Part A `49e1a12`, Part B this commit). `skills/writing-plans/SKILL.md`,
`skills/executing-plans/SKILL.md`, the three `tests/scenarios/writing-plans/*`
scenario globs, and `tests/test_scenarios.py` fixtures were updated in a
mechanical path substitution — no rule, gate, or rationalization changed.

Post-rename evidence (Sonnet, skill arm, 5 reps, `--keep-workspace`):
- `plans-premortem-reference` **5/5 GREEN** — see
  `2026-07-15-plans-premortem-reference-skill-sonnet-plansdir-r{1..5}.md`.
  Matches the pre-rename 5/5 at line 33.

`plans-no-placeholders-under-pressure` and `plans-approval-gate` reruns are
**deferred to the next full campaign**: their checks are pure file-glob
assertions on `.plans/*.md` (skill wording unchanged), and glob evaluation
is covered directly by `tests/test_scenarios.py` (55 green). Haiku wp
reruns deferred on the same basis + quota. Next full campaign should close
the 6-cell matrix (wp01/02/03 × sonnet/haiku) formally.

