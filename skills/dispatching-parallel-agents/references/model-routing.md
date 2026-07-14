# Model routing

Match model capability to task complexity. The suite is designed so cheaper
models can execute most of the work safely — plans make execution mechanical,
gates catch what slips.

## Tiering

Tiers are generic — they route **configurations** (model plus
effort/reasoning setting), not model names. The Claude and OpenAI/Codex
columns are worked examples; on another harness, substitute its equivalent
configuration.

| Tier | Claude (example) | OpenAI/Codex (example) | Generic equivalent | Use for |
|------|------------------|------------------------|--------------------|---------|
| Cheap | Haiku — no effort control (4.5) | GPT-5.6 Luna (`gpt-5.6-luna`), effort low | Smallest/fastest qualified configuration | Mechanical plan steps with exact code blocks, formatting/import fixes, running tests, file exploration, transcription |
| Standard | Sonnet — effort high (default) | GPT-5.6 Terra (`gpt-5.6-terra`), effort medium | Default tier | Implementing plan tasks, multi-file integration, refactors, reviewing small diffs |
| Capable | Opus — effort xhigh for coding/agentic | GPT-5.6 Sol (`gpt-5.6-sol`), effort high/xhigh | Largest routine reasoning tier | Brainstorming/architecture, writing plans, debugging after a cheap model stalled, final whole-branch review |
| Frontier (optional) | Fable — effort high (default), xhigh/max by exception | GPT-5.6 Sol, effort max; API pro mode by measured exception | Highest available quality-first configuration | Hardest tasks only: debugging the capable tier stalled on, architecture of large/risky changes, eval-failure diagnosis, final review before irreversible steps |

Provider configuration notes (vendor guidance as of 2026-07-14, **not
measured by this repository's evals** — existing campaigns controlled the
model only, never effort; see the [Claude effort
guide](https://platform.claude.com/docs/en/build-with-claude/effort), the
[Codex model guide](https://learn.chatgpt.com/docs/models), and the
[GPT-5.6 API guide](https://developers.openai.com/api/docs/guides/latest-model)):

- The effort values above are vendor-recommended starting points; on
  Sonnet, medium is a step-down candidate only after eval here. Haiku 4.5
  exposes no effort parameter.
- The frontier tier is asymmetric by design: Claude ships a distinct
  frontier model, while OpenAI reuses Sol at higher compute — effort
  `max`, or API `reasoning.mode: "pro"` on the same slug (never a
  separate Pro slug).
- Multi-agent settings are orchestration, not a tier: OpenAI's Ultra
  delegates to subagents, and Claude Code's ultracode pairs xhigh with
  standing multi-agent permission. Route those by task independence, not
  capability.

The frontier tier is optional — the suite is designed to run fully on the
three tiers above it. Route to it by exception, not by default.

## Rules

1. **Pin the model and reasoning setting per dispatched agent when the
   harness supports it** (Claude Code's Agent tool takes a `model`
   argument; a Codex custom agent file can set `model` and
   `model_reasoning_effort`) — an omitted model inherits the session
   default, often the most expensive one. If only run- or session-level
   selection exists, group tasks into a homogeneous wave under one
   explicit configuration or run them inline; never claim a per-agent
   selection the harness cannot enforce.
2. **Escalate on failure, never retry sideways.** Cheap model fails a step
   twice → hand the same step to the next tier with the failure context.
   Three failures at the highest available tier → stop, question the
   approach (systematic-debugging circuit breaker).
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
