# Inventory: skills/using-git-worktrees/SKILL.md

Base: `main` at 29a1c4e

| # | Original | Outcome | Items |
|---|---|---|---|
| R1 | "Ensure work happens in an isolated workspace. Prefer your platform's native worktree tools. Fall back to manual git worktrees only when no native tool is available." | "Ensure work happens in an isolated workspace: detect existing isolation first, then use native worktree tools, and fall back to manual git worktrees only when no native tool is available. Never fight the harness." | |
| R2 | "**Core principle:** Detect existing isolation first. Then use native tools. Then fall back to git. Never fight the harness." | merged into R1 | |
| R3 | "**Cross-links:** Cleanup of worktrees (delete branch, remove worktree) lives in `finishing-work`." | "Cleanup of worktrees (delete branch, remove worktree) lives in `finishing-work`." | |
| R4 | "Parallel subagents that touch overlapping files must enter their own worktree — see `dispatching-parallel-agents`." | "Parallel subagents that touch overlapping files must enter their own worktree — see `dispatching-parallel-agents`." | |
| R5 | "**Before creating anything, check if you are already in an isolated workspace.**" | "**Before creating anything, check if you are already in an isolated workspace.**" | |
| R6 | Fenced block `GIT_DIR=$(cd \"$(git rev-parse --git-dir)\" …` (three assignments) | "(same fenced block, byte for byte)" | |
| R7 | "**Submodule guard:** `GIT_DIR != GIT_COMMON` is also true inside git submodules. Before concluding \"already in a worktree,\" verify you are not in a submodule:" | "**Submodule guard:** `GIT_DIR != GIT_COMMON` is also true inside git submodules. Before concluding \"already in a worktree,\" verify you are not in a submodule:" | |
| R8 | Fenced block `# If this returns a path, you're in a submodule …` / `git rev-parse --show-superproject-working-tree 2>/dev/null` | "(same fenced block, byte for byte)" | |
| R9 | "**If `GIT_DIR != GIT_COMMON` (and not a submodule):** You are already in a linked worktree. Skip to Step 2 (Project Setup). Do NOT create another worktree." | "**If `GIT_DIR != GIT_COMMON` (and not a submodule):** You are already in a linked worktree. Skip to Step 2 (Project Setup). Do NOT create another worktree." | |
| R10 | "Report with branch state:" | "Report with branch state:" | |
| R11 | "- On a branch: \"Already in isolated workspace at `<path>` on branch `<name>`.\"" | "- On a branch: \"Already in isolated workspace at `<path>` on branch `<name>`.\"" | |
| R12 | "- Detached HEAD: \"Already in isolated workspace at `<path>` (detached HEAD, externally managed). Branch creation needed at finish time.\"" | "- Detached HEAD: \"Already in isolated workspace at `<path>` (detached HEAD, externally managed). Branch creation needed at finish time.\"" | |
| R13 | "**If `GIT_DIR == GIT_COMMON` (or in a submodule):** You are in a normal repo checkout." | "**If `GIT_DIR == GIT_COMMON` (or in a submodule):** You are in a normal repo checkout." | |
| R14 | "Has the user already indicated their worktree preference in your instructions? If not, ask for consent before creating a worktree:" | "If your instructions already declare a worktree preference, honor it without asking. Otherwise ask for consent before creating a worktree:" | |
| R15 | "> \"Would you like me to set up an isolated worktree? It protects your current > branch from changes.\"" | "> \"Would you like me to set up an isolated worktree? It protects your current > branch from changes.\"" | |
| R16 | "Honor any existing declared preference without asking." | merged into R14 | |
| R17 | "If the user declines consent, work in place and skip to Step 2." | "If the user declines consent, work in place and skip to Step 2." | |
| R18 | "**You have two mechanisms. Try them in this order.**" | "**You have two mechanisms. Try them in this order.**" | |
| R19 | "The user has asked for an isolated workspace (Step 0 consent). Do you already have a way to create a worktree? It might be a tool with a name like `EnterWorktree`, `WorktreeCreate`, a `/worktree` command, or a `--worktree` flag. If you do, use it and skip to Step 2." | "After Step 0 consent: if you have a native way to create a worktree — a tool named like `EnterWorktree` or `WorktreeCreate`, a `/worktree` command, or a `--worktree` flag — use it and skip to Step 2." | |
| R20 | "(See `../using-code-craft/references/tool-mapping.md` for the per-harness mapping of the \"create isolated workspace\" action.)" | "(See `../using-code-craft/references/tool-mapping.md` for the per-harness mapping of the \"create isolated workspace\" action.)" | |
| R21 | "Native tools handle directory placement, branch creation, and cleanup automatically." | "Native tools handle directory placement, branch creation, and cleanup automatically." | |
| R22 | "Using `git worktree add` when you have a native tool creates phantom state your harness can't see or manage." | "Using `git worktree add` when you have one is the #1 mistake: it creates phantom state your harness can't see or manage." | |
| R23 | "Only proceed to Step 1b if you have no native worktree tool available." | merged into R24 | |
| R24 | "**Only use this if Step 1a does not apply** — you have no native worktree tool available. Create a worktree manually using git." | "**Only use this if you have no native worktree tool** — never skip Step 1a by jumping straight to these git commands." | |
| R25 | "Follow this priority order. Explicit user preference always beats observed filesystem state." | "Follow this priority order. Explicit user preference always beats observed filesystem state." | |
| R26 | "1. **Check your instructions for a declared worktree directory preference.** If the user has already specified one, use it without asking." | "1. **Check your instructions for a declared worktree directory preference.** If the user has already specified one, use it without asking." | |
| R27 | "2. **Check for an existing project-local worktree directory:**" + indented bash block (`ls -d .worktrees 2>/dev/null     # Preferred (hidden)` / `ls -d worktrees 2>/dev/null      # Alternative`) | "2. **Check for an existing project-local worktree directory:**" + the same indented bash block, byte for byte | |
| R28 | "If found, use it. If both exist, `.worktrees` wins." | "If found, use it. If both exist, `.worktrees` wins." | |
| R29 | "3. **If there is no other guidance available**, default to `.worktrees/` at the project root." | "3. **If there is no other guidance available**, default to `.worktrees/` at the project root." | |
| R30 | "#### Safety Verification (project-local directories only)" / "**MUST verify directory is ignored before creating worktree:**" | "#### Safety Verification (project-local directories only)" / "**MUST verify directory is ignored before creating worktree:**" | |
| R31 | Fenced block `git check-ignore -q .worktrees 2>/dev/null &#124;&#124; git check-ignore -q worktrees 2>/dev/null` | "(same fenced block, byte for byte)" | |
| R32 | "**If NOT ignored:** Add to .gitignore, commit the change, then proceed." | "**If NOT ignored:** Add to .gitignore, commit the change, then proceed — otherwise worktree contents get committed and pollute git status." | |
| R33 | "**Why critical:** Prevents accidentally committing worktree contents to repository." | merged into R32 | |
| R34 | Fenced block `# Determine path based on chosen location` … `cd \"$path\"` | "(same fenced block, byte for byte)" | |
| R35 | "**Sandbox fallback:** If `git worktree add` fails with a permission error (sandbox denial), tell the user the sandbox blocked worktree creation and you're working in the current directory instead. Then run setup and baseline tests in place." | "**Sandbox fallback:** If `git worktree add` fails with a permission error (sandbox denial), tell the user the sandbox blocked worktree creation and you're working in the current directory instead. Then run setup and baseline tests in place." | |
| R36 | "Auto-detect and run appropriate setup:" | "Auto-detect and run appropriate setup (skip what does not apply):" | |
| R37 | Fenced block `# Node.js` … `if [ -f go.mod ]; then go mod download; fi` | "(same fenced block, byte for byte)" | |
| R38 | "Run tests to ensure workspace starts clean:" | "Never skip this. Run tests to ensure workspace starts clean:" | |
| R39 | Fenced block `# Use project-appropriate command` / `npm test / cargo test / pytest / go test ./...` | "(same fenced block, byte for byte)" | |
| R40 | "**If tests fail:** Report failures, ask whether to proceed or investigate." | "**If tests fail:** Report failures and ask whether to proceed or investigate; never proceed without explicit permission — otherwise new bugs are indistinguishable from pre-existing ones." | |
| R41 | "**If tests pass:** Report ready." | "**If tests pass:** Report ready." | |
| R42 | Report fenced block `Worktree ready at <full-path>` … `Ready to implement <feature-name>` | "(same fenced block, byte for byte)" | |
| R43 | "&#124; Already in linked worktree &#124; Skip creation (Step 0) &#124;" | merged into R9 | |
| R44 | "&#124; In a submodule &#124; Treat as normal repo (Step 0 guard) &#124;" | merged into R13 | |
| R45 | "&#124; Native worktree tool available &#124; Use it (Step 1a) &#124;" | merged into R19 | |
| R46 | "&#124; No native tool &#124; Git worktree fallback (Step 1b) &#124;" | merged into R24 | |
| R47 | "&#124; `.worktrees/` exists &#124; Use it (verify ignored) &#124;" | merged into R28 | |
| R48 | "&#124; `worktrees/` exists &#124; Use it (verify ignored) &#124;" | merged into R27 | code:worktrees/ |
| R49 | "&#124; Both exist &#124; Use `.worktrees/` &#124;" | merged into R28 | |
| R50 | "&#124; Neither exists &#124; Check instruction file, then default `.worktrees/` &#124;" | merged into R29 | |
| R51 | "&#124; Directory not ignored &#124; Add to .gitignore + commit &#124;" | merged into R32 | |
| R52 | "&#124; Permission error on create &#124; Sandbox fallback, work in place &#124;" | merged into R35 | |
| R53 | "&#124; Tests fail during baseline &#124; Report failures + ask &#124;" | merged into R40 | |
| R54 | "&#124; No package.json/Cargo.toml &#124; Skip dependency install &#124;" | merged into R36 | |
| R55 | "Fighting the harness — **Problem:** Using `git worktree add` when the platform already provides isolation. **Fix:** Step 0 detects existing isolation. Step 1a defers to native tools." | merged into R22 | |
| R56 | "Skipping detection — **Problem:** Creating a nested worktree inside an existing one. **Fix:** Always run Step 0 before creating anything" | merged into R5 | |
| R57 | "Skipping ignore verification — **Problem:** Worktree contents get tracked, pollute git status. **Fix:** Always use `git check-ignore` before creating project-local worktree" | merged into R30 | code:git check-ignore |
| R58 | "Assuming directory location — **Problem:** Creates inconsistency, violates project conventions. **Fix:** Follow priority: explicit instructions > existing project-local directory > default" | merged into R25 | |
| R59 | "Proceeding with failing tests — **Problem:** Can't distinguish new bugs from pre-existing issues. **Fix:** Report failures, get explicit permission to proceed" | merged into R40 | |
| R60 | "**Never:** Create a worktree when Step 0 detects existing isolation" | merged into R9 | |
| R61 | "**Never:** Use `git worktree add` when you have a native worktree tool (e.g., `EnterWorktree`). This is the #1 mistake — if you have it, use it." | merged into R22 | |
| R62 | "**Never:** Skip Step 1a by jumping straight to Step 1b's git commands" | merged into R24 | |
| R63 | "**Never:** Create worktree without verifying it's ignored (project-local)" | merged into R30 | |
| R64 | "**Never:** Skip baseline test verification" | merged into R38 | |
| R65 | "**Never:** Proceed with failing tests without asking" | merged into R40 | |
| R66 | "**Always:** Run Step 0 detection first" | merged into R5 | |
| R67 | "**Always:** Prefer native tools over git fallback" | merged into R1 | |
| R68 | "**Always:** Follow directory priority: explicit instructions > existing project-local directory > default" | merged into R25 | |
| R69 | "**Always:** Verify directory is ignored for project-local" | merged into R30 | |
| R70 | "**Always:** Auto-detect and run project setup" | merged into R36 | |
| R71 | "**Always:** Verify clean test baseline" | merged into R38 | |

Counts (checker): 1188 -> 796 words (32% cut), 173 -> 117 nonblank lines.
