# code-craft bootstrap (Claude Code)

@AGENTS.md

Note: when the code-craft plugin is installed, the hooks in `hooks/hooks.json`
enforce the four rules from AGENTS.md mechanically and re-inject the dispatch
skill after compaction. Without the plugin, this file is the only loader —
follow AGENTS.md to the letter.

## Repo workflow (when developing this suite)

- Commit each time you create a file or complete a major update; small
  commits are the recovery map for interrupted sessions.
- Plans live in `.plans/` — a gitignored working directory. Never commit
  plan files.
- Project overview, sources, and roadmap live in [README.md](README.md).
