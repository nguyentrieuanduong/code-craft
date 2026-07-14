# Plan: complete Codex installation (release 0.3.0)

**Goal:** code-craft installs natively on Codex — all 15 skills with
self-contained runtime references, SessionStart bootstrap injection,
**three hard PreToolUse policies plus one advisory PostToolUse
debug-print audit** enforced after `/hooks` trust on both Claude and
Codex payload shapes, and SEC-09 dependency vetting via the
`security-baseline` workflow (instruction-level on Codex; hook-blocked
on Claude via `guard-installs.py`, unchanged). Single `0.3.0` release,
one PR.

**Non-goals:** GPT eval campaign; automatic user-config or execpolicy
mutation; mechanical Codex dependency-install prompts; phased 0.4.0;
fixing the installed `plugin-creator` validator.

## Settled decisions (approved by the user — do not reopen)

1. **P1 — Official manual + real `codex` CLI ingestion is the release
   gate.** The local `plugin-creator` validator's `hooks` rejection is a
   toolchain defect, filed in the PR description. Scope of the deviation
   is exactly one validator error (enforced by Task 2.7); every other
   validator requirement, including `interface.defaultPrompt`, is met.
2. **P2 — Debug-print audit stays advisory on both harnesses.** Advisory
   *in effect* (PostToolUse; edit not undone), not a return-code rewrite:
   it keeps stderr + exit 2. Contract: Codex "3 hard + 1 advisory",
   Claude "4 hard + 1 advisory".
3. **P3 — Authenticated live smoke is user-run.** Execution pauses at
   Task 3.11 for the user's transcript before finishing-work.
4. **P4 — Sonnet eval spot-check dropped from required acceptance.**
   Packaging test + scenario dry-run prove path substitution; the eval
   stays available as an optional user step.

## Verified design inputs (2026-07-14)

- Manifest `.codex-plugin/plugin.json`: `skills`, `hooks`, `interface`
  (incl. `defaultPrompt` array), metadata. Marketplace at
  `.agents/plugins/marketplace.json`; plugin entries carry
  `name`/`source`/`policy`/`category` only.
- Codex hook entries: single `command` string, optional `commandWindows`,
  int `timeout`. No `args`. Env: `PLUGIN_ROOT`/`PLUGIN_DATA` primary,
  `CLAUDE_PLUGIN_ROOT` compat. SessionStart accepts the current
  `hookSpecificOutput` shape. PreToolUse `permissionDecision` supports
  `deny`/`allow` only — irrelevant here: all Codex-wired policies block
  via `sys.exit(2)` + stderr. `guard-installs.py` (the only
  `"ask"`-emitter) is not wired on Codex.
- Local validator CLI: `python3 ~/.codex/skills/.system/plugin-creator/scripts/validate_plugin.py <root>`
  → exit 1 + `- <error>` lines on failure, exit 0 on pass.
- Repo: 15 SKILL.md; `.claude-plugin/plugin.json` at 0.2.0; four runtime
  docs in `docs/`; six consuming SKILL.md files (+ README, CONTRIBUTING,
  AGENTS.md, skills/README.md, two scenario fixtures).
- `.gitignore:2` has the unanchored `references/` rule. On 2026-07-14,
  the user removed the three scratch ignore entries; `recommend.md` and
  `recommends.md` are now untracked discussion files and MUST NOT be staged.
  From Task 1.0c onward: never `git add -A` or `git add .` — stage listed
  paths only.

## Task 0 — persist this plan (after user approval)

- [x] 0.1 `apply_patch` this Plan section (from `# Plan:` through
  `## Acceptance criteria`) into
  `docs/plans/2026-07-14-codex-installation-plan.md`.
- [x] 0.2 Commit: `Add Codex installation plan (0.3.0)`. Persisting the
  plan is not authorization to execute Task 1.

## Task 1 — self-contained runtime references

- [x] 1.0a Probe:
  `git check-ignore -v skills/using-code-craft/references/probe.md` and
  `git check-ignore -v references/probe.md` — expect both matched by
  `.gitignore:2:references/`.
- [x] 1.0b `apply_patch` `.gitignore` line 2 only:
  `references/` → `/references/` (working tree edit; nothing staged yet).
- [x] 1.0c *(Amended 2026-07-14 after the user removed the scratch
  ignore entries: worktree and index now match at the original
  `references/` rule. This step applies one contextual patch separately
  to the worktree and index, superseding 1.0b's lost edit.)*

  Precondition (else STOP and re-verify state):
  `git diff --cached -- .gitignore` is empty and worktree line 2 is
  exactly `references/`.

  Write this exact patch to `/tmp/gitignore-anchor.patch` with the
  harness's file-write tool (strip the two-space list indentation —
  every line must start at column 0):

  ```diff
  diff --git a/.gitignore b/.gitignore
  --- a/.gitignore
  +++ b/.gitignore
  @@ -1,3 +1,3 @@
   .idea/
  -references/
  +/references/
   .DS_Store
  ```

  ```bash
  git apply /tmp/gitignore-anchor.patch
  git apply --cached /tmp/gitignore-anchor.patch
  ```

  Do not use `git apply --index`; use the two independently preflighted
  commands above.

- [x] 1.0d Verify:
  - `git diff --cached -- .gitignore` → only the one-line anchor change;
  - `git diff -- .gitignore` → empty;
  - `recommend.md` and `recommends.md` remain untracked;
  - `git check-ignore skills/using-code-craft/references/probe.md`
    exits 1; `git check-ignore references/probe.md` exits 0.

- [x] 1.1 Add a failing packaging test in a new
  `tests/test_codex_plugin.py`:
  - All four canonical files exist at their packaged paths (1.2).
  - Every consuming `SKILL.md` links to the canonical path via a
    skill-relative path that resolves to a readable file.
  - Root `docs/*.md` compat pointers exist, ≤10 lines each, link to the
    packaged canonical file, no cycles.
  - No `SKILL.md` retains a `docs/<name>.md` runtime link.

- [x] 1.2 Relocate the four docs with `apply_patch` add/delete pairs
  (no `mkdir`, no `git mv` — harness rule). For each: add the new file
  with content byte-identical to the old, delete the old.

  | Delete | Add |
  |---|---|
  | `docs/tool-mapping.md` | `skills/using-code-craft/references/tool-mapping.md` |
  | `docs/anti-patterns.md` | `skills/using-code-craft/references/anti-patterns.md` |
  | `docs/evidence.md` | `skills/using-code-craft/references/evidence.md` |
  | `docs/model-routing.md` | `skills/dispatching-parallel-agents/references/model-routing.md` |

  Stage each old and new path explicitly (`git add <old> <new>` per
  pair — staging a deleted path records the deletion); `git status`
  must then show four `renamed:` entries (rename detection survives the
  small link edits from 1.4).

- [x] 1.3 Write four root compat pointers (template; per-file
  title/target adjusted):

  ```markdown
  # Anti-patterns

  Canonical runtime reference moved to
  [skills/using-code-craft/references/anti-patterns.md](../skills/using-code-craft/references/anti-patterns.md).
  This page preserves existing repository links.
  ```

- [x] 1.4 Update consuming `SKILL.md` links (verified list):

  | File:line | New link (skill-relative) |
  |---|---|
  | `skills/using-git-worktrees/SKILL.md:74` | `../using-code-craft/references/tool-mapping.md` |
  | `skills/dispatching-parallel-agents/SKILL.md:32` | `references/model-routing.md` |
  | `skills/writing-plans/SKILL.md:77` | `../using-code-craft/references/anti-patterns.md` |
  | `skills/releasing-safely/SKILL.md:15,56` | `../using-code-craft/references/anti-patterns.md` |
  | `skills/code-review/SKILL.md:40,49` | `../using-code-craft/references/evidence.md` |
  | `skills/finishing-work/SKILL.md:29` | `../using-code-craft/references/evidence.md` |

  If `evidence.md` cross-links `anti-patterns.md`, rewrite it as a
  same-directory link (`anti-patterns.md`).

- [x] 1.5 Bootstrap pointers: `AGENTS.md:11` and
  `skills/README.md:90,92` → packaged paths. `README.md`,
  `CONTRIBUTING.md`, `tests/scenarios/**/*.md` KEEP their `docs/*.md`
  links — they resolve through the compat pointers.
- [x] 1.6 Run 1.1's test — green.
- [x] 1.7 `python3 -m unittest discover tests` — full suite green.
- [x] 1.8 Commit (staging the anchor from 1.0c plus the
  planned files): `Root-anchor references ignore; move runtime docs to
  owner skills with compatibility pointers`.

## Task 2 — Codex plugin manifests, hooks manifest, version bump

- [ ] 2.1 Add failing tests to `tests/test_codex_plugin.py`:
  - `.codex-plugin/plugin.json` parses; contains `name`, `version`,
    `skills`, `hooks`, `interface`, `author`, `license`; the interface
    block contains a non-empty `defaultPrompt` array of strings; every
    referenced path resolves inside the repo; version matches
    `.claude-plugin/plugin.json`.
  - `.agents/plugins/marketplace.json` parses; declares one plugin named
    `code-craft` with `source.source == "local"`, `source.path == "./"`
    (test uses the same `"./"` literal); the plugin entry has NO
    `description` field.
  - `hooks/codex-hooks.json` parses; exactly five command entries
    (1 SessionStart + 3 hard PreToolUse + 1 advisory PostToolUse); every
    entry has single-string `command` and `commandWindows` and
    `timeout == 30`; no entry references `guard-installs.py`; matchers
    are `startup|resume|clear|compact`, `Edit|Write`, `Bash`,
    `Edit|Write` respectively.
  - `.claude-plugin/plugin.json` at `0.3.0`.
  - `skills/` contains exactly 15 `SKILL.md` files.

- [ ] 2.2 Create `.codex-plugin/plugin.json`:

  ```json
  {
    "name": "code-craft",
    "version": "0.3.0",
    "description": "Disciplined development skill suite for junior developers and smaller models: hard gates, checklists, and mechanical enforcement so output quality comes from process, not raw capability.",
    "author": { "name": "Duong Nguyen Trieu An" },
    "license": "MIT",
    "skills": "./skills/",
    "hooks": "./hooks/codex-hooks.json",
    "interface": {
      "displayName": "code-craft",
      "shortDescription": "Disciplined engineering workflows for Codex.",
      "longDescription": "Install the complete code-craft lifecycle: brainstorming, planning, TDD, systematic debugging, verification, review, finishing, release safety, plus SessionStart bootstrap and enforcement hooks.",
      "developerName": "Duong Nguyen Trieu An",
      "category": "Productivity",
      "capabilities": ["Read", "Write"],
      "defaultPrompt": [
        "Apply the code-craft workflow to this repository."
      ]
    }
  }
  ```

- [ ] 2.3 Create `.agents/plugins/marketplace.json` (entry fields match
  the official example — no `description`):

  ```json
  {
    "name": "code-craft",
    "interface": { "displayName": "Code Craft" },
    "plugins": [
      {
        "name": "code-craft",
        "source": { "source": "local", "path": "./" },
        "policy": {
          "installation": "AVAILABLE",
          "authentication": "ON_INSTALL"
        },
        "category": "Productivity"
      }
    ]
  }
  ```

- [ ] 2.4 Create `hooks/codex-hooks.json` (five commands; `hooks/hooks.json`
  is NOT edited):

  ```json
  {
    "hooks": {
      "SessionStart": [
        {
          "matcher": "startup|resume|clear|compact",
          "hooks": [
            {
              "type": "command",
              "command": "python3 \"$PLUGIN_ROOT/hooks/session-start.py\"",
              "commandWindows": "py -3 \"%PLUGIN_ROOT%\\hooks\\session-start.py\"",
              "timeout": 30
            }
          ]
        }
      ],
      "PreToolUse": [
        {
          "matcher": "Edit|Write",
          "hooks": [
            { "type": "command",
              "command": "python3 \"$PLUGIN_ROOT/hooks/protect-configs.py\"",
              "commandWindows": "py -3 \"%PLUGIN_ROOT%\\hooks\\protect-configs.py\"",
              "timeout": 30 },
            { "type": "command",
              "command": "python3 \"$PLUGIN_ROOT/hooks/scan-secrets.py\"",
              "commandWindows": "py -3 \"%PLUGIN_ROOT%\\hooks\\scan-secrets.py\"",
              "timeout": 30 }
          ]
        },
        {
          "matcher": "Bash",
          "hooks": [
            { "type": "command",
              "command": "python3 \"$PLUGIN_ROOT/hooks/guard-bash.py\"",
              "commandWindows": "py -3 \"%PLUGIN_ROOT%\\hooks\\guard-bash.py\"",
              "timeout": 30 }
          ]
        }
      ],
      "PostToolUse": [
        {
          "matcher": "Edit|Write",
          "hooks": [
            { "type": "command",
              "command": "python3 \"$PLUGIN_ROOT/hooks/audit-debug-prints.py\"",
              "commandWindows": "py -3 \"%PLUGIN_ROOT%\\hooks\\audit-debug-prints.py\"",
              "timeout": 30 }
          ]
        }
      ]
    }
  }
  ```

- [ ] 2.5 `apply_patch` `.claude-plugin/plugin.json`: version
  `0.2.0` → `0.3.0`. No other field changes.
- [ ] 2.6 Run 2.1 tests — green.
- [ ] 2.7 Validator gate (P1 scope enforcement), guarded by
  `@unittest.skipUnless(Path("~/.codex/skills/.system/plugin-creator/scripts/validate_plugin.py").expanduser().is_file(), ...)`:
  run the validator against the repo root; assert exit code 1 and that
  the output contains **exactly one** `- ` error line, exactly:
  `` - plugin.json field `hooks` is not accepted by plugin validation ``.
  Any second error line is a release failure.
- [ ] 2.8 Commit: `Add Codex plugin, marketplace, and hooks manifests;
  bump suite to 0.3.0`. This commit is structurally installable: every
  manifest-referenced path exists.

## Task 3 — payload normalizer, dual-payload policies, install test

Requirement: three hard PreToolUse policies (protect-configs,
scan-secrets, guard-bash) plus the advisory PostToolUse audit inspect
both Claude Edit/Write and Codex `apply_patch`/Bash payload shapes.
SessionStart resolves `PLUGIN_ROOT` first. `guard-installs.py` stays
Claude-only and untouched.

### 3A — RED: dual-payload + boundary tests

- [ ] 3.1 Add failing Codex-shaped fixtures to `tests/test_hooks.py`
  (keep Claude fixtures green):
  - `protect-configs`: `apply_patch` touching `.eslintrc.js` → exit 2 +
    stderr; clean file → exit 0.
  - `scan-secrets`: `apply_patch` containing an API-key-shaped string
    assembled at test time → exit 2 + stderr; clean patch → exit 0.
  - `guard-bash`: Codex Bash payload with `git commit --no-verify` →
    exit 2 + stderr; `ls` → exit 0.
  - `audit-debug-prints` (advisory-in-effect, per P2/E3): write a
    fixture file containing `console.log(...)` to a temp dir first, then
    invoke the hook with the matching `apply_patch` payload; assert
    **exit 2**, advisory stderr, **and the fixture file's content is
    unchanged after the hook exits** (PostToolUse does not roll back).
    Clean content → exit 0.

  Draft Codex payload shape (verify against Codex hook docs before
  committing; adjust fixture if the schema differs):

  ```json
  {
    "tool_input": {
      "command": "apply_patch",
      "input": "*** Begin Patch\n*** Update File: .eslintrc.js\n@@\n-old\n+new\n*** End Patch\n"
    }
  }
  ```

- [ ] 3.2 Add the mandated generated-input boundary test for the parser
  (`test-driven-development` contract), deterministic and stdlib-only:

  ```python
  class HookPayloadBoundaryTest(unittest.TestCase):
      def test_generated_payloads_hold_invariants(self):
          rng = random.Random(20260714)
          for _ in range(500):
              payload = _gen_value(rng, depth=0)
              out, err = io.StringIO(), io.StringIO()
              with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
                  cmd = hook_payload.command(payload)
                  text = hook_payload.proposed_text(payload)
                  paths = hook_payload.target_paths(payload)
              self.assertIsInstance(cmd, str)
              self.assertIsInstance(text, str)
              self.assertIsInstance(paths, tuple)
              self.assertEqual(len(paths), len(set(paths)))
              for p in paths:
                  self.assertIsInstance(p, Path)
              self.assertEqual(out.getvalue(), "")
              self.assertEqual(err.getvalue(), "")
  ```

  `_gen_value` is a bounded local generator (max depth 6): nested dicts,
  lists, scalars (str/int/float/bool/None), malformed patch-like strings
  (`"*** Update File:"` fragments, truncated headers), sometimes wrapped
  in `{"tool_input": ...}`, sometimes not. Invariants: no unexpected
  exception; `command()`/`proposed_text()` always return `str`;
  `target_paths()` always returns a deduplicated tuple of `Path`; no
  payload content reaches stdout/stderr.

- [ ] 3.3 `python3 -m unittest tests.test_hooks -v` — new Codex cases
  fail (policies only read Claude fields today); boundary test fails on
  import (`hook_payload` does not exist yet). Both are the RED state.

### 3B — GREEN: normalizer, policy refactor, SessionStart

- [ ] 3.4 Create `hooks/hook_payload.py` — typed per `coding-standards`,
  no payload logging:

  ```python
  """Payload normalizer for Claude Edit/Write and Codex apply_patch/Bash.

  Never log the payload — hooks may see secrets or PII.
  """
  from __future__ import annotations

  import re
  from pathlib import Path
  from typing import Any, Iterator, Mapping

  PATCH_HEADER = re.compile(
      r"^\*\*\* (?:Add|Update|Delete) File: (.+)$", re.MULTILINE
  )


  def _iter_strings(value: Any) -> Iterator[str]:
      if isinstance(value, str):
          yield value
      elif isinstance(value, Mapping):
          for item in value.values():
              yield from _iter_strings(item)
      elif isinstance(value, (list, tuple)):
          for item in value:
              yield from _iter_strings(item)


  def tool_input(payload: Any) -> Any:
      return payload.get("tool_input", {}) if isinstance(payload, Mapping) else {}


  def proposed_text(payload: Any) -> str:
      return "\n".join(_iter_strings(tool_input(payload)))


  def command(payload: Any) -> str:
      ti = tool_input(payload)
      if not isinstance(ti, Mapping):
          return ""
      return str(ti.get("command") or ti.get("cmd") or ti.get("input") or "")


  def target_paths(payload: Any) -> tuple[Path, ...]:
      ti = tool_input(payload)
      out: list[str] = []
      if isinstance(ti, Mapping) and ti.get("file_path"):
          out.append(str(ti["file_path"]))
      for text in _iter_strings(ti):
          out.extend(PATCH_HEADER.findall(text))
      return tuple(dict.fromkeys(Path(p) for p in out))
  ```

- [ ] 3.5 Refactor `protect-configs.py`, `scan-secrets.py`,
  `guard-bash.py`, `audit-debug-prints.py` to consume `hook_payload`.
  Preserve every policy constant, stderr message, exit code, and Claude
  behavior. `guard-installs.py` is NOT touched.
- [ ] 3.6 Update `hooks/session-start.py` root selection:

  ```python
  root = Path(
      os.environ.get("PLUGIN_ROOT")
      or os.environ.get("CLAUDE_PLUGIN_ROOT")
      or Path(__file__).resolve().parent.parent
  )
  ```

- [ ] 3.7 Add a SessionStart JSON regression test to
  `tests/test_hooks.py`:

  ```python
  class SessionStartTest(unittest.TestCase):
      def _run(self, env):
          return subprocess.run(
              [sys.executable, str(HOOKS_DIR / "session-start.py")],
              capture_output=True, text=True, env=env, check=True,
          )

      def _assert_contract(self, stdout):
          out = json.loads(stdout)["hookSpecificOutput"]
          self.assertEqual(out["hookEventName"], "SessionStart")
          self.assertIn("<code-craft-bootstrap>", out["additionalContext"])
          self.assertIn("using-code-craft", out["additionalContext"])

      def test_codex_plugin_root(self):     # primary Codex path
          self._assert_contract(self._run({"PLUGIN_ROOT": str(REPO_ROOT)}).stdout)

      def test_claude_plugin_root(self):    # backward compat
          self._assert_contract(self._run({"CLAUDE_PLUGIN_ROOT": str(REPO_ROOT)}).stdout)
  ```

- [ ] 3.8 `python3 -m unittest tests.test_hooks -v` — all Claude and
  Codex cases plus the boundary test green.

### 3C — automated Codex install test, full suite, single commit

- [ ] 3.9 Add to `tests/test_codex_plugin.py`, guarded by
  `@unittest.skipUnless(shutil.which("codex"), ...)`, with
  `tempfile.TemporaryDirectory()` as `CODEX_HOME` (no user credentials
  or state touched):

  ```text
  codex plugin marketplace add /absolute/path/to/code-craft --json
  codex plugin add code-craft@code-craft --json
  codex plugin list --json          # assert code-craft 0.3.0 present
  codex plugin remove code-craft@code-craft --json
  ```

  Assert all four exit 0 and the plugin appears/disappears in the JSON.
- [ ] 3.10 `python3 -m unittest discover tests` — full suite green.
- [ ] 3.11 Commit ALL Task 3 code and tests (nothing left uncommitted
  at the pause): `Add typed payload normalizer, dual-payload policies,
  PLUGIN_ROOT-first session start, Codex install test`.

### 3D — user-run authenticated smoke (release blocker; execution pauses)

- [ ] 3.12 **PAUSE FOR USER.** The executor stops after 3.11 and posts:

  1. In your authenticated Codex install:
     `codex plugin marketplace add /absolute/path/to/code-craft`
     then `codex plugin add code-craft@code-craft`.
  2. Restart Codex; `/hooks`; trust the five commands.
  3. New session: confirm `<code-craft-bootstrap>` context appears.
  4. Deny path (all three MUST block with exit-2 stderr):
     - Bash: `git commit --no-verify` → blocked.
     - Edit: writing to `.eslintrc.js` → blocked.
     - Edit: writing a file containing an API-key-shaped string → blocked.
  5. Advisory path: edit a `.ts` file adding `console.log(...)` —
     advisory feedback surfaces; the edit is NOT rolled back (expected).
  6. Allow path: a routine edit passes cleanly.
  7. Paste the transcript back to the current executor.

  If any hard policy does NOT block on Codex, the executor STOPS, opens
  `systematic-debugging`, and downgrades the README claim to match
  observed behavior before finishing-work.

## Task 4 — README and installation contract

- [ ] 4.1 Add a failing README test asserting these literal commands
  appear in `README.md`:

  ```text
  codex plugin marketplace add /absolute/path/to/code-craft
  codex plugin add code-craft@code-craft
  codex plugin list --json
  codex plugin marketplace upgrade code-craft
  codex plugin remove code-craft@code-craft
  ```

- [ ] 4.2 README Install section, after the Claude plugin block:

  ```bash
  # Codex CLI / desktop (native plugin: skills + bootstrap + hooks)
  codex plugin marketplace add /absolute/path/to/code-craft
  codex plugin add code-craft@code-craft
  codex plugin list --json
  # trust the five commands once:
  #   /hooks
  # upgrade / remove:
  #   codex plugin marketplace upgrade code-craft
  #   codex plugin remove code-craft@code-craft
  ```

- [ ] 4.3 Surface matrix (P2 wording):

  ```markdown
  | Surface | Installation | Skills | Bootstrap | Enforcement |
  |---|---|---:|---:|---:|
  | Codex CLI | Native plugin | Full | SessionStart hook | 3 hard PreToolUse policies + advisory PostToolUse audit after `/hooks` trust; SEC-09 via `security-baseline` |
  | Codex desktop app | Native plugin | Full | SessionStart hook | 3 hard PreToolUse policies + advisory PostToolUse audit after hook trust; SEC-09 via `security-baseline` |
  | Codex IDE extension | `$HOME/.agents/skills` fallback | Full | Advisory/global `AGENTS.md` | No plugin-hook parity |
  | Claude Code | Existing Claude plugin | Full | SessionStart hook | 4 hard PreToolUse policies + advisory PostToolUse audit |
  ```

- [ ] 4.4 Update "Other harnesses": Codex moves out of the
  instruction-file-only list; Copilot/OpenCode remain. SEC-09 on Codex
  is enforced via `security-baseline` (instruction-level).
- [ ] 4.5 Update "What's here": add `.codex-plugin/` next to
  `.claude-plugin/`; point the moved-doc bullets at the new
  `skills/<owner>/references/` paths.
- [ ] 4.6 Run 4.1 — green.
- [ ] 4.7 Commit: `Document Codex install surface; 3-hard + 1-advisory
  enforcement contract`.

## Task 5 — verify, review, finish

- [ ] 5.1 Stale runtime-reference scan (empty expected):

  ```bash
  rg -n 'docs/(tool-mapping|model-routing|anti-patterns|evidence)\.md' \
    skills AGENTS.md CLAUDE.md skills/README.md
  ```

- [ ] 5.2 `python3 -m unittest discover tests` — all green (33 original
  + packaging/manifest/hooks-schema/dual-payload/boundary/SessionStart;
  validator gate and install test skip cleanly where their tools are
  absent).
- [ ] 5.3 `python3 tests/scenarios/run.py --dry-run` — all 12 scenarios
  parse; skill and fixture paths resolve.
- [ ] 5.4 Compat-pointer shape: each of four `docs/*.md` is ≤10 lines
  and links to its packaged canonical target.
- [ ] 5.5 `git diff --check` — no whitespace errors.
- [ ] 5.6 Ignore safety: `git log -p .gitignore` shows only the anchor
  change on this branch; `git diff -- .gitignore` is empty; discussion
  files remain untracked.
- [ ] 5.7 `code-review` of the whole branch. First line states
  changed-line count and the ~400-line-threshold verdict; doc moves
  inflate counts — judge on content.
- [ ] 5.8 Wait for the Task 3.12 transcript; if any hard policy failed
  to block, revisit before continuing.
- [ ] 5.9 `finishing-work` options menu. No verification-only commit;
  evidence goes in the PR description (validator gate output showing the
  single known error, 3.9 install-test output, 3.12 transcript).

**Optional user step (dropped from the gate per P4):**
`writing-plans/01` and `releasing-safely/01` ×1 Sonnet skill arm for
extra path-substitution confidence.

## Acceptance criteria

- `git check-ignore skills/using-code-craft/references/tool-mapping.md`
  exits 1; `.gitignore` has no unstaged diff at branch tip; discussion
  files remain untracked.
- Four canonical runtime docs under `skills/<owner>/references/`; all
  consumers use skill-relative paths; root `docs/*.md` are ≤10-line
  compat pointers, no cycles; the Task 1 commit shows four renames.
- Both plugin manifests at `0.3.0`; `.claude-plugin/plugin.json` diff is
  version-only.
- `.codex-plugin/plugin.json` has `skills`, `hooks`, and a
  validator-complete `interface` block **including a `defaultPrompt`
  array**; the local validator reports **exactly one** error (`hooks`
  unknown field) — any second error is a release failure.
- `.agents/plugins/marketplace.json` entry carries
  `name`/`source`/`policy`/`category` only (no `description`),
  `source.path == "./"`, fixture literal matches.
- `hooks/codex-hooks.json` committed in Task 2 (every commit
  installable): five single-string commands + `commandWindows`, uniform
  30 s, no `guard-installs.py`; `hooks/hooks.json` diff empty.
- Dual-payload tests pass for all four policies; the Codex audit test
  asserts exit 2 + advisory stderr + no rollback of the written file;
  clean content exits 0.
- `hook_payload.py` fully type-annotated; seeded generated-input
  boundary test passes its five invariants.
- SessionStart contract test passes with both `PLUGIN_ROOT` and
  `CLAUDE_PLUGIN_ROOT`.
- Automated unauthenticated install test passes where `codex` is on
  PATH; skipped elsewhere. Nothing uncommitted at the 3.12 pause.
- Task 3.12 transcript confirms the three hard policies block on Codex;
  otherwise the README claim is downgraded to match.
- README matrix uses the P2 wording; no "hard blocking" claim for the
  debug-print audit anywhere.
- Unit suite + scenario dry-run green.
- PR description includes: P1 validator toolchain-defect note with the
  gate output, install-test output, and the 3.12 transcript.
