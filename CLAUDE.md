# code-craft

A skill suite for junior developers and lower-capability models (e.g. Claude
Sonnet/Haiku) that encodes disciplined development as explicit rules, hard
gates, checklists, and forbidden-rationalization tables — so output quality
approaches a top-tier model's through process rather than capability.

### Sources

Merged from `references/` (gitignored, clone locally), in priority order:

1. `superpowers` — workflow skills, hard gates, rationalization tables
2. `ECC` — verification loop, TDD gates, security checklists
3. `skills` — SKILL.md format conventions, safety-guardrail patterns
4. `aidlc-workflows` — adaptive depth, plan-driven codegen, security baseline, state/resume

Plus the maintainer's personal coding style (`~/.claude/skills/coding-style`),
folded into `skills/coding-standards`.

### Current state

Second iteration: hardened for weaker models and other harnesses.

- 11 skills in `skills/` (Anthropic SKILL.md format). Descriptions are
  trigger-only (SDO); `using-code-craft` compressed for always-loading;
  coding-standards and TDD carry good/bad example pairs.
- Claude Code plugin: `.claude-plugin/plugin.json` + `hooks/` — SessionStart
  bootstrap injection plus enforcement hooks (linter-config protection,
  secret scan, git --no-verify/force-push guard, debug-print audit). All
  hook scripts are python3-stdlib, tested via stdin payloads.
- Cross-harness: `AGENTS.md`, `GEMINI.md`, `docs/tool-mapping.md`,
  `docs/model-routing.md`.
[settings.json](../../.claude/settings.json)
- `using-code-craft` — meta-dispatch, mandatory workflow ordering
- `brainstorming` → `writing-plans` → `executing-plans` — planning pipeline with approval gates
- `test-driven-development`, `systematic-debugging`, `verification-before-completion` — execution discipline
- `coding-standards` (maintainer's taste), `security-baseline` — always-on constraints
- `code-review`, `finishing-work` — conclusion pipeline

`skills/README.md` documents the workflow ordering and the suite's design
principles.

### Possible next steps

- Pressure-test on a real Sonnet/Haiku session (superpowers method: baseline
  without skill, record rationalizations verbatim, patch the tables, re-test)
- Publish to a plugin marketplace (marketplace.json)
- Add optional skills: writing-skills (meta), dispatching-parallel-agents, git-worktrees

### Workflow

Commit each time you create a file or complete a major update — token limits
can interrupt work at any time, and small commits let the next session resume
from `git log`.
