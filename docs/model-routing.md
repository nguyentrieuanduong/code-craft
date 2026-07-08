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

## Interaction with the suite

- `writing-plans` quality determines how far down-tier execution can go:
  placeholder-free plans with code blocks are what Haiku-class models can
  execute reliably.
- `verification-before-completion` and the enforcement hooks are
  tier-independent backstops — they catch weaker-model slips mechanically.
