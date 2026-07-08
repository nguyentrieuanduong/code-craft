# Tool mapping per harness

Skills name **actions**, never harness-specific tools. This table translates.
When porting to a new harness, extend this file — never edit skill bodies.

| Action in skills | Claude Code | Cursor | Codex CLI | Gemini CLI |
|------------------|-------------|--------|-----------|------------|
| Read a file | `Read` tool | built-in file read | `cat` via shell | `read_file` |
| Edit / write a file | `Edit` / `Write` tools | built-in edit | `apply_patch` | `write_file` / `replace` |
| Run a command | `Bash` tool | terminal tool | `shell` | `run_shell_command` |
| Dispatch a subagent | `Agent` tool (`subagent_type`) | not available — do the work inline | not available — do the work inline | not available — do the work inline |
| Track task state | `TaskCreate` / `TaskUpdate` | plan checkboxes in the plan file | plan checkboxes in the plan file | plan checkboxes in the plan file |
| Ask the user a question | plain response (or AskUserQuestion) | plain response | plain response | plain response |
| Search the codebase | `grep`/`find` via Bash, or Explore agent | built-in search | `rg` via shell | `search_file_content` / `glob` |

## Fallback rule

If the harness lacks a capability (usually subagents), perform the work
inline in the current context, in the same order the skill prescribes. The
plan file's checkboxes replace any task tool: they are the durable state.

## Enforcement parity

| Enforcement | Claude Code | Other harnesses |
|-------------|-------------|-----------------|
| Bootstrap injection | SessionStart hook (`hooks/hooks.json`) | `AGENTS.md` / `GEMINI.md` read at startup |
| Config protection, secret scan, git guard, print audit | PreToolUse/PostToolUse hooks | self-enforced rules listed in `AGENTS.md` |
