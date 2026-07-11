# Contributing to code-craft

These rules apply to humans and to AI agents opening PRs alike. Upstream
skill suites report the large majority of AI-generated PRs rejected for
skipping exactly these gates — read this before writing anything.

## The gate, in order

1. **Read `skills/writing-skills/SKILL.md` before touching any skill.** Its
   iron law governs this repo: no skill created or changed without a failing
   (baseline) test first.
2. **Skill wording changes require eval evidence.** Run the scenario
   baseline with the current wording, then with your edit, using fresh
   subagents as `writing-skills` prescribes. Include both results in the PR
   (convention: `tests/scenarios/results/`). PRs that change skill wording
   without before/after evidence are rejected without further review.
3. **No drive-by edits.** Rationalization tables, red-flag lists, and gate
   wording are deliberately tuned against observed agent behavior. "Clearer
   phrasing" that was never tested against an agent is churn, not
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

- Skill change without baseline/eval evidence (rule 2)
- Hook change without tests (rule 4)
- Wording churn with no behavioral justification (rule 3)
- Secrets, debug prints, or linter-config edits — the plugin hooks block
  these mechanically; do not fight the hooks in a PR
- Growth of the always-on bootstrap (`AGENTS.md`, session injection): its
  token budget is a tax on every session and is treated as frozen
