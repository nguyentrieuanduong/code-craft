# code-craft

A skill suite for junior developers and lower-capability models (e.g. Claude
Sonnet/Haiku) that encodes disciplined development as explicit rules, hard
gates, checklists, and mechanical enforcement — so output quality comes from
process, not raw capability.

## What's here

- **`skills/`** — 13 harness-agnostic workflow skills plus 1 maintainer
  meta-skill (`writing-skills`). See [skills/README.md](skills/README.md)
  for the ordering and design principles.
- **`.claude-plugin/` + `hooks/`** — Claude Code plugin: SessionStart
  bootstrap injection plus enforcement hooks (linter-config protection,
  secret scan, `git --no-verify`/force-push guard, debug-print audit).
- **`CLAUDE.md` / `AGENTS.md`** — per-harness loaders. Thin
  pointers only; skill content lives in `skills/`.
- **`docs/tool-mapping.md`** — translates the skills' action names to each
  harness's tools. Porting = extending this table, never editing skills.
- **`docs/model-routing.md`** — which model tier runs which stage, and how
  to escalate on failure.
- **`docs/anti-patterns.md`** — evidence-backed catalog of mistakes to avoid
  at every lifecycle stage (framing → deploy → ops), with an incident map and
  sources. Pre-mortem/review checklist and raw material for skill authoring.

## Install

**As a plugin (recommended — skills + bootstrap + enforcement hooks):**

```bash
# try it in one session
claude --plugin-dir /path/to/code-craft

# or install persistently
claude plugin marketplace add /path/to/code-craft
claude plugin install code-craft@code-craft
```

**As a skills-directory plugin:** copy the whole repo to
`~/.claude/skills/code-craft/` — Claude Code detects `.claude-plugin/plugin.json`
and loads it as a plugin in all projects.

**Skills only (no hooks, no bootstrap):** copy `skills/*` into
`~/.claude/skills/`. Skill dispatch then relies on the model reading the
descriptions — enforcement rules from `AGENTS.md` become advisory.

**Other harnesses (Codex, Copilot, OpenCode, ...):** copy the repo into your
project; the harness picks up `AGENTS.md`. See `docs/tool-mapping.md`.
Non-Claude harnesses are instruction-file only: the four rules are advisory
there, hooks are not enforced.

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
from `git log`.

## Possible next steps

- Pressure-test on a real Sonnet/Haiku session (baseline without the skill,
  record rationalizations verbatim, patch the tables, re-test)
- Publish to a plugin marketplace (marketplace.json)
