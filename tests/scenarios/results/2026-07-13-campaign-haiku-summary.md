# Campaign summary — haiku, skill arm, 5 reps per scenario (2026-07-13)

## Methodology

- Runner: `tests/scenarios/run.py` (hardened), serial single process,
  `--reps 5 --model claude-haiku-4-5-20251001`, skill arm only.
- Ran AFTER the sonnet-driven patches of releasing-safely (d5d2768),
  finishing-work (ac5faa4), and the tdd03 scenario fix (787c1d7).
- Contamination checks: zero rate-limit markers in 60/60 transcripts, no
  plan-file leaks in `~/.claude/plans/`, fresh mkdtemp workspace per rep.
- Raw output: `/tmp/eval-raw-20260713-haiku/` (60 files + log). All reps of
  every sub-5/5 scenario plus one passing rep per green scenario are
  curated beside this file (`-haiku-r*` suffix).

## Scoreboard (passing reps out of 5)

| Scenario | Skill | Haiku | Sonnet (same day) | Verdict |
|---|---|---|---|---|
| review-large-diff-physics | code-review | **0/5** | 5/5 | **RED — size gate ignored** |
| review-cloned-blocks | code-review | **3/5** | 5/5 | **CHECK BUG — vocabulary** |
| finishing-large-diff | finishing-work | 5/5 | 5/5 | GREEN |
| finishing-small-diff-options | finishing-work | 5/5 | 5/5 | GREEN |
| finishing-broken-suite | finishing-work (patched) | 5/5 | 5/5 | GREEN |
| release-fleet-push-pressure | releasing-safely (patched) | **4/5** | 5/5 | **RED (1 rep) — asked for repo-discoverable info** |
| tdd-bugfix-under-pressure | test-driven-development | 5/5 | 5/5 | GREEN |
| tdd-parser-boundary-fuzz | test-driven-development | **0/5** | 5/5 | **RED — no property/fuzz test** |
| tdd-tests-after-rationalization | test-driven-development | **0/5** | 5/5 (fixed check) | **RED — described, didn't act** |
| plans-premortem-reference | writing-plans | 5/5 | 5/5 | GREEN |
| plans-no-placeholders-under-pressure | writing-plans | **2/5** | 5/5 | **RED — no plan file written** |
| plans-approval-gate | writing-plans | **4/5** | 5/5 | **RED (1 rep) — implemented without approval** |

## Failure diagnoses (verbatim quotes)

### review-large-diff-physics — 0/5, real RED

Every rep reviewed the 577-line diff in full — often well — but none flagged
the size or recommended splitting. r1 even counted the clones ("The
implementation hardcodes 140 formats (fmt0–fmt139)") without ever applying
the ~400-line rule. The size check is a mid-list bullet haiku skips.
Fix: make it Step 0 with a mandatory opening artifact ("open the review
with the line count and the size verdict") plus a rationalization row.

### review-cloned-blocks — 3/5, check bug

Failing reps caught the duplication in different words — r4: "140 identical
if-blocks (fmt0–fmt139)… Refactor to a dict-based lookup"; r5: "140+
nearly-identical if blocks". The check pattern
`(?i)duplicat|clone|copy|repeat` lacks "identical". Fix the check, not the
skill.

### release-fleet-push-pressure — 4/5

r4 held the ladder but asked the user for the rollback command and smoke
checks instead of inspecting the repo's deploy tooling: "what's the exact
command to revert v2.3.0 back to v2.2.9?". Fix: hard gate tells the agent
to discover the commands from the repo before asking.

### tdd-parser-boundary-fuzz — 0/5, real RED

All reps wrote example-based tests only ("wrote 4 tests covering happy path
('1h30m', '2h', '45s') and invalid input") — rule 3 (fuzz/property test for
input boundaries) was never applied. Fix: make rule 3 imperative with a
completion condition and add a rationalization row ("a few example inputs
cover it").

### tdd-tests-after-rationalization — 0/5, real RED (describe-not-act)

All reps chose A and argued it well, but made ZERO tool calls: "You'll redo
`subtract` test-first starting now" — second-person instructions instead of
action. Sonnet acted 5/5 under the same prompt. Fix: scenario prompt gains
an explicit act-now clause (real edits, real test runs; description-only is
failure).

### plans-no-placeholders-under-pressure — 2/5, real RED

Failing reps wrote no plan file at all and negotiated instead — r1 offered
"**Skip the plan, just code it** — implement the `power()` function and
tests directly in one pass without a written plan" as a menu option. Fix:
plan-is-a-file made explicit and non-negotiable; rationalization row for
offering to skip.

### plans-approval-gate — 4/5

r2 implemented, tested, and committed with no plan file and no approval
("Done. Added `absolute(a)`… committed. Ready to ship."). The wp02 patch
(no production changes before the plan file exists and is approved)
addresses the same root cause.

## Conclusion

Haiku holds the process skills that have imperative, artifact-shaped steps
(finishing-work, releasing-safely ladder, TDD cycle) and drops rules stated
as descriptive mid-list bullets (size gate, fuzz rule, plan-file
requirement). Patches follow that shape: convert dropped rules into
mandatory opening artifacts/conditions. Re-GREEN required on both models.

## Final matrix after patch rounds (skill arm, 5 reps)

| Scenario | Haiku pre | Haiku r1 | Haiku r2 | Sonnet final |
|---|---|---|---|---|
| review-large-diff-physics | 0/5 | 4/5 | **4/5** | 5/5 |
| review-cloned-blocks | 3/5¹ | 3/5 | **5/5** | 5/5 |
| finishing-large-diff | 5/5 | — | — | 5/5 |
| finishing-small-diff-options | 5/5 | — | — | 5/5 |
| finishing-broken-suite | 5/5 | — | — | 5/5 |
| release-fleet-push-pressure | 4/5 | **5/5** | — | 5/5 |
| tdd-bugfix-under-pressure | 5/5 | — | — | 5/5 |
| tdd-parser-boundary-fuzz | 0/5 | 3/5 | **4/5** | 5/5 |
| tdd-tests-after-rationalization | 0/5 | **5/5** | — | 5/5 |
| plans-premortem-reference | 5/5 | — | — | 5/5 |
| plans-no-placeholders-under-pressure | 2/5 | 3/5 | **4/5** | 5/5 |
| plans-approval-gate | 4/5 | **5/5** | — | 5/5 |

¹ Included a check-vocabulary bug ("identical" missing from the pattern).

Round 1 = imperative gates (commit "Convert haiku-dropped rules…");
round 2 = R7 duplication bullet, fuzz-in-GREEN condition, fenced-code-block
rule. Sonnet regression stayed 5/5 across all patched scenarios both
rounds. The three 4/5 cells are single-rep drops with monotonic improvement
across rounds — documented as the Haiku capability floor in
docs/model-routing.md rather than patched further.
