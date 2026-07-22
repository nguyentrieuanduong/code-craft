# Contributing to code-craft

These rules apply to humans and to AI agents opening PRs alike. Upstream
skill suites report the large majority of AI-generated PRs rejected for
skipping exactly these gates — read this before writing anything.

## The gate, in order

1. **Read `skills/writing-skills/SKILL.md` before touching any skill.** Its
   deterministic, focused, and optional full tiers govern this repo.
2. **Match eval cost to the skill change.** Every skill change runs
   `python3 -m tools.check`. Trigger-only, metadata, link, and typo changes
   need no model calls when deterministic checks cover them. New skills and
   behavior-shaping rule changes add one focused scenario and attach one
   before/after sample (two sequential model calls maximum). Multi-model or
   five-repetition campaigns are optional release evidence, never CI.

   When an intended skill or description change alters routing, update the
   affected routing case with a rationale in the commit describing the
   intended shift; never edit fixtures merely to recover a score.
3. **No drive-by edits.** Rationalization tables, red-flag lists, and gate
   wording are deliberately tuned against observed agent behavior. "Clearer
   phrasing" without evidence from the applicable tier is churn, not
   improvement.
4. **Hook changes require regression tests.** Every behavior change in
   `hooks/*.py` gets cases in `tests/test_hooks.py`, and
   `python3 -m unittest discover tests` must pass.
5. **New skills must be registered everywhere:** a dispatch row in
   `skills/using-code-craft/SKILL.md`, an entry in `skills/README.md`, the
   skill count in the root `README.md`, and `docs/tool-mapping.md` if the
   skill names an action not already mapped.
6. **Small commits.** One file created or one coherent update per commit —
   commits are the recovery map for interrupted sessions.

## Automatic rejections

- Skill change without evidence for the applicable tier (rule 2)
- Hook change without tests (rule 4)
- Wording churn with no applicable evidence or justification (rule 3)
- Secrets, debug prints, or linter-config edits — the plugin hooks block
  these mechanically; do not fight the hooks in a PR
- Growth of the always-on bootstrap (`AGENTS.md`, session injection): its
  token budget is a tax on every session and is treated as frozen
