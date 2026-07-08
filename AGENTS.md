# code-craft bootstrap (harness-agnostic)

This file is the entry point for agents whose harness reads `AGENTS.md`
(Codex, Copilot, OpenCode, and others) and cannot run the plugin hooks.

## Non-negotiable startup step

Read `skills/using-code-craft/SKILL.md` NOW, before responding to any
engineering request. It contains the dispatch table mapping situations to
skills. When a row matches, read that skill's `skills/<name>/SKILL.md` and
follow it. Skill wording is harness-agnostic — see `docs/tool-mapping.md` to
translate named actions ("dispatch a subagent", "run a command") to your
harness's tools.

## Without mechanical hooks, self-enforce these

The Claude Code plugin blocks the following automatically. On this harness
nothing blocks you, so the rules bind you directly:

1. Never modify linter/formatter configs to make checks pass — fix the code.
2. Never write secret-shaped strings (API keys, tokens, private keys,
   hardcoded passwords) into any file.
3. Never use `git commit --no-verify`, `git push --no-verify`, or force-push
   to main/master.
4. Never leave `print(...)` / `console.log(...)` in production code — use
   structured logging.

## Ordering

`brainstorming → writing-plans → executing-plans → verification-before-completion → code-review → finishing-work`

Every stage runs; depth scales with the task. No production code before an
approved design and plan.
