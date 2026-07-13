# Model routing

Match model capability to task complexity. The suite is designed so cheaper
models can execute most of the work safely — plans make execution mechanical,
gates catch what slips.

## Tiering

| Tier | Models (example) | Use for |
|------|------------------|---------|
| Cheap | Haiku | Mechanical plan steps with exact code blocks, formatting/import fixes, running tests, file exploration, transcription |
| Standard | Sonnet | Implementing plan tasks, multi-file integration, refactors, reviewing small diffs |
| Capable | Opus | Brainstorming/architecture, writing plans, debugging after a cheap model stalled, final whole-branch review |

## Rules

1. **Always specify the model explicitly** when dispatching a subagent — an
   omitted model inherits the session default, often the most expensive one.
2. **Escalate on failure, never retry sideways.** Cheap model fails a step
   twice → hand the same step to the next tier with the failure context.
   Three failures at the capable tier → stop, question the approach
   (systematic-debugging circuit breaker).
3. **Turn count beats token price.** If a cheap model needs 3× the turns,
   it costs more than the standard model doing it once. Use the cheap tier
   only where the plan leaves nothing to decide.
4. **Reviews get a floor of the standard tier.** Spec-compliance and code
   quality judgments below that tier miss too much to be worth running.
5. **Planning and design get the capable tier when available.** A strong plan
   is what makes cheap execution safe; economizing on planning inverts the
   whole model.

## Measured Haiku floor (5-rep eval campaign, 2026-07-13)

With skills injected, Sonnet holds all 12 eval scenarios at 5/5. Haiku
holds 9/12 at 5/5; three scenarios plateau at 4/5 after two wording-patch
rounds (each round improved monotonically from 0/5–3/5 — see
`tests/scenarios/results/2026-07-13-campaign-haiku-summary.md`):

- **review-large-diff-physics** — ~1 rep in 5 omits the diff-size verdict.
- **tdd-parser-boundary-fuzz** — ~1 rep in 5 skips the generated-input test.
- **plans-no-placeholders-under-pressure** — ~1 rep in 5 writes the plan
  file without fenced code blocks.

These are single-rep drops of rules the skills state imperatively; further
wording escalation showed diminishing returns and risks bloat. Treat them
as the Haiku capability floor: rule 4 above (reviews floor at the standard
tier) already covers the first; for parser work and plan writing on the
cheap tier, have the standard tier spot-check that the fuzz test and the
plan's code blocks exist.

## Interaction with the suite

- `writing-plans` quality determines how far down-tier execution can go:
  placeholder-free plans with code blocks are what Haiku-class models can
  execute reliably.
- `verification-before-completion` and the enforcement hooks are
  tier-independent backstops — they catch weaker-model slips mechanically.
