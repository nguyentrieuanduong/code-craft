# code-craft Skill Suite

A skill suite for junior developers and smaller models (e.g. Claude Sonnet/Haiku).
It encodes the discipline of a top-tier engineer as explicit rules, hard gates, and
checklists — so quality comes from process, not raw capability.

Sources, in priority order: [superpowers](https://github.com/obra/superpowers),
Everything Claude Code (ECC), anthropics/skills conventions, AWS AI-DLC workflows,
plus the maintainer's personal coding style.

## The workflow

Skills are ordered. Do not skip stages. Each stage ends with a **hard gate** that
must pass before the next stage starts.

```
1. using-code-craft              <- always active: dispatch + ordering
2. brainstorming                 <- understand + design (GATE: user approves design)
3. writing-plans                 <- bite-sized plan   (GATE: user approves plan)
4. executing-plans               <- run the plan step by step
     |- dispatching-parallel-agents <- when 2+ plan tasks are independent
     |- test-driven-development  <- inside every implementation step
     |- systematic-debugging     <- whenever anything unexpected happens
     |- coding-standards         <- style rules for all code written
     |- security-baseline        <- blocking constraints for all code written
5. verification-before-completion <- GATE: evidence before any "done" claim
6. code-review                   <- request review, handle feedback rigorously
7. finishing-work                <- merge / PR / keep / discard, user chooses
```

## The skills

| Skill | Purpose |
|-------|---------|
| [using-code-craft](using-code-craft/SKILL.md) | Meta-skill: check for an applicable skill before ANY action; enforce workflow ordering |
| [brainstorming](brainstorming/SKILL.md) | Turn a vague request into an approved design; adaptive depth; no code before approval |
| [writing-plans](writing-plans/SKILL.md) | Turn an approved design into a numbered, placeholder-free implementation plan |
| [executing-plans](executing-plans/SKILL.md) | Execute the plan exactly, checkbox by checkbox; resumable after interruption |
| [dispatching-parallel-agents](dispatching-parallel-agents/SKILL.md) | Orchestrate concurrent subagents for independent plan tasks, with review between waves |
| [test-driven-development](test-driven-development/SKILL.md) | RED → GREEN → REFACTOR; no production code without a failing test first |
| [systematic-debugging](systematic-debugging/SKILL.md) | Four-phase root-cause process; no fixes before investigation |
| [verification-before-completion](verification-before-completion/SKILL.md) | Run the command, read the output, then claim — never before |
| [coding-standards](coding-standards/SKILL.md) | Stateless, immutable, declarative, lazy-init, boundary error handling, structured logging |
| [security-baseline](security-baseline/SKILL.md) | Eight blocking security rules; violations stop the work |
| [code-review](code-review/SKILL.md) | Requesting and receiving code review with technical rigor |
| [finishing-work](finishing-work/SKILL.md) | Verify tests, then present the four ways to conclude a branch |

## Design principles of this suite

1. **Hard gates, not suggestions.** A gate is written as a rule the model cannot
   rationalize around. If the gate fails, the work stops.
2. **Forbidden rationalizations.** Weaker models talk themselves out of process under
   pressure. Each skill lists the exact excuses ("too simple to test", "I'm
   confident it passes") and forbids them by name.
3. **Evidence before claims.** Every success statement must be backed by a
   freshly-run command whose output was actually read.
4. **Bite-sized steps.** Plans decompose into 2–5 minute steps with exact files,
   code, and test commands. Small steps leave no room for drift.
5. **Resumable state.** Long workflows persist state to files (plans with
   checkboxes) so work survives context loss and session restarts.
6. **Mechanical enforcement over trust.** A Claude Code plugin
   (`.claude-plugin/`, `hooks/`) injects the dispatch skill at every session
   start (including after compaction) and blocks linter-config tampering,
   secret-shaped writes, `git --no-verify`, and force-pushes to main at the
   tool layer. Instructions request; hooks enforce.
7. **Trigger-only descriptions.** A skill's `description` says only *when* to
   use it, never *what* to do — weaker models otherwise follow the one-line
   summary and skip the skill body (Skill Discovery Optimization).

## Beyond Claude Code

- `AGENTS.md` at the repo root bootstraps harnesses without hook support;
  the enforcement rules become self-enforced instructions there.
- `docs/tool-mapping.md` translates the skills' harness-agnostic action names
  to each harness's tools. Porting = extending that table, never editing skills.
- `docs/model-routing.md` — which model tier runs which stage, and how to
  escalate on failure.
