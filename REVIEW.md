# Reviewing code-craft

How changes to this repository fail, and where the checks live. Read with
[AGENTS.md](AGENTS.md) and [CONTRIBUTING.md](CONTRIBUTING.md).

- **Skills misroute or contradict a gate.** A description that says what
  to do instead of when, or wording that lets a gate be skipped. Routing:
  `python3 -m tools.check`. Behavior: the focused scenario CONTRIBUTING
  rule 2 requires.
- **Hooks get bypassed or block legitimate work.** Every hook change needs
  block *and* allow cases in `tests/test_hooks.py` (CONTRIBUTING rule 4).
- **Evaluations report false confidence.** A check pattern that passes on
  the wrong behavior, a fixture edited to recover a score, or one sample
  described as validation. See `tests/scenarios/README.md`.
- **Documentation misstates behavior.** README and skill text must match
  what the hooks and skills do; a claim about this repository's behavior
  with no code evidence, passing check, or recorded result is a finding.
- Nits: one line each, never blocking.
