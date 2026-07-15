# code-craft

A skill suite for junior developers and lower-capability models (e.g. Claude
Sonnet/Haiku) that encodes disciplined development as explicit rules, hard
gates, checklists, and mechanical enforcement — so output quality comes from
process, not raw capability. The premise is measured, not aspirational:
[docs/evidence.md](docs/evidence.md) collects the numbers behind every gate
(TDD −40–90% pre-release defects, DORA's −7.2% delivery stability per +25%
AI adoption, the METR perception gap).

## What's here

- **`skills/`** — 14 harness-agnostic workflow skills plus 1 maintainer
  meta-skill (`writing-skills`). See [skills/README.md](skills/README.md)
  for the ordering and design principles.
- **`.claude-plugin/` + `hooks/`** — Claude Code plugin: SessionStart
  bootstrap injection plus enforcement hooks (linter-config protection,
  secret scan, `git --no-verify`/force-push guard, new-dependency vetting
  gate, debug-print audit).
- **`.codex-plugin/` + `.agents/plugins/`** — Codex native plugin: same
  skills and SessionStart bootstrap; three hard PreToolUse policies plus
  the advisory debug-print audit via `hooks/codex-hooks.json` (dependency
  vetting stays instruction-level via `security-baseline`).
- **`CLAUDE.md` / `AGENTS.md`** — per-harness loaders. Thin
  pointers only; skill content lives in `skills/`.
- **`skills/using-code-craft/references/tool-mapping.md`** — translates the
  skills' action names to each harness's tools. Porting = extending this
  table, never editing skills.
- **`skills/dispatching-parallel-agents/references/model-routing.md`** —
  which model tier runs which stage, and how to escalate on failure.
- **`skills/using-code-craft/references/anti-patterns.md`** —
  evidence-backed catalog of mistakes to avoid at every lifecycle stage
  (framing → deploy → ops), with an incident map and sources.
  Pre-mortem/review checklist and raw material for skill authoring.
- **`skills/using-code-craft/references/evidence.md`** — the empirical case
  for the suite: the measured AI-assisted failure mode and the study behind
  each mechanism. (Root `docs/*.md` remain as compatibility pointers.)
- **`tests/`** — hook regression tests plus `tests/scenarios/`, the skill
  eval harness: pressure-test corpus + headless runner implementing the
  writing-skills RED→GREEN cycle for skill wording.

## Install

### What gets installed?

Both recommended installations are plugins that bundle the shared `skills/` directory.
The plugin is the installable package; `skills/` is its shared workflow
payload.

| Harness | Recommended installation | Includes |
|---|---|---|
| Claude Code | Claude Code plugin | Shared skills, SessionStart bootstrap, Claude hooks |
| Codex CLI / desktop | Codex native plugin | Shared skills, SessionStart bootstrap, Codex hooks |
| Claude Code (fallback) | Skills only in `~/.claude/skills/` | Shared skills only; no bootstrap or hooks |
| Codex (fallback) | Skills only in `$HOME/.agents/skills/` | Shared skills only; no plugin bootstrap or hooks |

Full per-surface breakdown — including hooks, IDE, and fallback details — is in [Surface support](#surface-support) below.

Use skills-only installation only when the harness cannot load the native
plugin or when you explicitly do not want hooks.

**Claude Code plugin (recommended — skills + bootstrap + enforcement hooks):**

```bash
# try it in one session
claude --plugin-dir /path/to/code-craft

# or install persistently
claude plugin marketplace add /path/to/code-craft
claude plugin install code-craft@code-craft
```

**Claude Code plugin from a skills directory:** copy the whole repo to
`~/.claude/skills/code-craft/` — Claude Code detects `.claude-plugin/plugin.json`
and loads it as a plugin in all projects.

**Skills-only fallback (no hooks, no bootstrap):** copy `skills/*` into
`~/.claude/skills/`. Skill dispatch then relies on the model reading the
descriptions — enforcement rules from `AGENTS.md` become advisory.

For Codex's skills-only fallback, copy `skills/*` into
`$HOME/.agents/skills/`. Codex loads the shared workflows without the plugin's
SessionStart bootstrap or enforcement hooks.

**Codex native plugin (CLI / desktop — skills + bootstrap + hooks):**

```bash
# Codex CLI / desktop (native plugin: skills + bootstrap + hooks)
codex plugin marketplace add /absolute/path/to/code-craft
codex plugin add code-craft@code-craft
codex plugin list --json
# trust the five commands once:
#   /hooks
# upgrade / remove:
#   codex plugin marketplace upgrade code-craft
#   codex plugin remove code-craft@code-craft
```

**Other harnesses (Copilot, OpenCode, ...):** copy the repo into your
project; the harness picks up `AGENTS.md`. See `docs/tool-mapping.md`.
These harnesses are instruction-file only: the four rules are advisory
there, hooks are not enforced. On Codex, prefer the native plugin above;
SEC-09 dependency vetting on Codex stays instruction-level via
`security-baseline`.

### Surface support

| Surface | Installation | Skills | Bootstrap | Enforcement |
|---|---|---:|---:|---:|
| Codex CLI | Native plugin | Full | SessionStart hook | 3 hard PreToolUse policies + advisory PostToolUse audit after `/hooks` trust; SEC-09 via `security-baseline` |
| Codex desktop app | Native plugin | Full | SessionStart hook | 3 hard PreToolUse policies + advisory PostToolUse audit after hook trust; SEC-09 via `security-baseline` |
| Codex IDE extension | `$HOME/.agents/skills` fallback | Full | Advisory/global `AGENTS.md` | No plugin-hook parity |
| Claude Code | Existing Claude plugin | Full | SessionStart hook | 4 hard PreToolUse policies + advisory PostToolUse audit |

## Sources

code-craft ships as a self-contained suite — no local clone of upstream
repos is needed to use it. Credit to the sources it was merged from, in
priority order:

1. [superpowers](https://github.com/obra/superpowers) — workflow skills, hard gates, rationalization tables
2. [ECC](https://github.com/affaan-m/ECC) — verification loop, TDD gates, enforcement hooks, security checklists
3. [google/skills](https://github.com/google/skills) — SKILL.md format conventions, safety-guardrail patterns
4. [AI-DLC](https://github.com/awslabs/aidlc-workflows) — adaptive depth, plan-driven codegen, security baseline, state/resume

Plus the maintainer's personal coding style, folded into
`skills/coding-standards`.

## Contributing workflow

Commit each time you create a file or complete a major update — sessions can
be interrupted at any time, and small commits let the next session resume
from `git log`. Skill and hook changes are gated: see
[CONTRIBUTING.md](CONTRIBUTING.md) before editing anything under `skills/`
or `hooks/`.

## Eval status (2026-07-13/14 campaigns)

The full corpus ran at 5 reps per scenario on both target models (skill
arm, hardened headless runner). After two evidence-gated patch rounds:
Sonnet 12/12 scenarios at 5/5; Haiku 9/12 at 5/5 with three 4/5 residuals
documented as a capability floor in `docs/model-routing.md`. Baseline
(no-skill) arms at 5 reps score 0–1/5 on six of seven measured scenarios
on both models — the skill wording, not model capability, produces the
behavior. One scenario (review-cloned-blocks) is at ceiling: its fixture
is blatant enough that bare models pass; it stays as a regression check.
Campaign summaries with verbatim failure quotes live in
`tests/scenarios/results/` (`*-campaign-*-summary.md`).

## Possible next steps

- Subtler fixture for review-cloned-blocks (3–4 clones across files) so the
  scenario discriminates skill from baseline again
- Publish to a plugin marketplace (marketplace.json)
