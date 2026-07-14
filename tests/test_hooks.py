#!/usr/bin/env python3
"""Regression tests for the enforcement hooks.

Each hook is exercised as a subprocess with real hook JSON on stdin,
exactly as Claude Code invokes it. Exit 2 = blocked/flagged, 0 = allowed.

Run: python3 -m unittest discover tests
"""
import contextlib
import io
import json
import os
import random
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from typing import Any

HOOKS = Path(__file__).resolve().parent.parent / "hooks"


def run_hook(script, payload):
    return subprocess.run(
        [sys.executable, str(HOOKS / script)],
        input=json.dumps(payload),
        capture_output=True,
        text=True,
    )


def bash(command):
    return {"tool_input": {"command": command}}


def codex_command(tool_name: str, command: str) -> dict[str, object]:
    return {
        "tool_name": tool_name,
        "tool_input": {"command": command},
    }


def codex_patch(path: Path, replacement: str) -> dict[str, object]:
    patch = (
        "*** Begin Patch\n"
        f"*** Update File: {path}\n"
        "@@\n"
        "-old\n"
        f"+{replacement}\n"
        "*** End Patch\n"
    )
    return codex_command("apply_patch", patch)


def _gen_value(rng: random.Random, depth: int) -> Any:
    scalars: tuple[Any, ...] = (
        None,
        True,
        False,
        0,
        -1,
        3.14,
        "",
        "plain text",
        "*** Update File:",
        "*** Add File: truncated",
        "*** Delete File: ",
    )
    if depth >= 6:
        return rng.choice(scalars)

    shape = rng.randrange(5)
    if shape == 0:
        value: Any = rng.choice(scalars)
    elif shape == 1:
        value = [
            _gen_value(rng, depth + 1)
            for _ in range(rng.randrange(4))
        ]
    elif shape == 2:
        value = {
            rng.choice(("command", "input", "file_path", f"k{index}")): _gen_value(
                rng,
                depth + 1,
            )
            for index in range(rng.randrange(4))
        }
    elif shape == 3:
        value = (
            "*** Begin Patch\n"
            f"*** Update File: {rng.choice(('app.py', '.eslintrc.js', ''))}\n"
        )
    else:
        value = (
            _gen_value(rng, depth + 1),
            _gen_value(rng, depth + 1),
        )

    if depth == 0 and rng.choice((True, False)):
        return {"tool_input": value}
    return value


class GuardBashTest(unittest.TestCase):
    BLOCKED = (
        "git commit --no-verify -m 'wip'",
        "git push --no-verify",
        "git push -f origin main",
        "git push --force origin main",
        "git push origin main -f",
        "git push origin main --force",
        "git push origin +main",
        "git push -f origin HEAD:master",
        "git push --force-with-lease origin main",
        "npm test && git push --force origin main",
    )
    ALLOWED = (
        "git push origin main",
        "git push -f origin feature",
        "git push --force-with-lease origin feature",
        "git push origin feature:dev",
        "git commit -m 'document --no-verify guard'",
        'echo "git push -f origin main"',
        "git log --oneline",
    )

    def test_blocked_commands(self):
        for command in self.BLOCKED:
            with self.subTest(command=command):
                result = run_hook("guard-bash.py", bash(command))
                self.assertEqual(result.returncode, 2, result.stderr)
                self.assertIn("BLOCKED", result.stderr)

    def test_allowed_commands(self):
        for command in self.ALLOWED:
            with self.subTest(command=command):
                result = run_hook("guard-bash.py", bash(command))
                self.assertEqual(result.returncode, 0, result.stderr)

    def test_codex_bash_blocks_hook_bypass(self):
        payload = codex_command("Bash", "git commit --no-verify -m 'wip'")
        result = run_hook("guard-bash.py", payload)
        self.assertEqual(result.returncode, 2, result.stderr)
        self.assertIn("BLOCKED", result.stderr)

    def test_codex_bash_allows_routine_command(self):
        result = run_hook("guard-bash.py", codex_command("Bash", "ls"))
        self.assertEqual(result.returncode, 0, result.stderr)


class GuardInstallsTest(unittest.TestCase):
    ASKED = (
        "npm install left-pad",
        "npm i express",
        "npm install --save-dev typescript",
        "pnpm add lodash",
        "yarn add react",
        "pip install requests",
        "pip3 install flask",
        "python -m pip install numpy",
        "sudo pip install requests",
        "pip install --upgrade requests",
        "uv add httpx",
        "uv pip install rich",
        "cargo add serde",
        "go get github.com/pkg/errors",
        "cd app && npm install foo",
    )
    ALLOWED = (
        "npm install",
        "npm ci",
        "npm run build",
        "pnpm install",
        "yarn install",
        "pip install -r requirements.txt",
        "pip install -e .",
        "pip install .",
        "uv sync",
        "cargo build",
        "go mod tidy",
        'echo "pip install requests"',
        "git commit -m 'pip install docs'",
    )

    def test_asks_for_new_packages(self):
        for command in self.ASKED:
            with self.subTest(command=command):
                result = run_hook("guard-installs.py", bash(command))
                self.assertEqual(result.returncode, 0, result.stderr)
                decision = json.loads(result.stdout)["hookSpecificOutput"]
                self.assertEqual(decision["permissionDecision"], "ask")
                self.assertIn("SEC-09", decision["permissionDecisionReason"])

    def test_allows_routine_commands(self):
        for command in self.ALLOWED:
            with self.subTest(command=command):
                result = run_hook("guard-installs.py", bash(command))
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertEqual(result.stdout.strip(), "")


class ScanSecretsTest(unittest.TestCase):
    def test_blocks_api_key_in_content(self):
        payload = {"tool_input": {"content": "key = 'sk-" + "a" * 24 + "'"}}
        result = run_hook("scan-secrets.py", payload)
        self.assertEqual(result.returncode, 2, result.stderr)

    def test_blocks_password_in_new_string(self):
        payload = {"tool_input": {"new_string": 'password = "hunter2hunter2"'}}
        result = run_hook("scan-secrets.py", payload)
        self.assertEqual(result.returncode, 2, result.stderr)

    def test_allows_clean_content(self):
        payload = {"tool_input": {"content": "api_key = os.environ['API_KEY']"}}
        result = run_hook("scan-secrets.py", payload)
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_codex_patch_blocks_secret_shaped_content(self):
        value = "sk-" + "a" * 24
        payload = codex_patch(Path("settings.py"), f'API_KEY = "{value}"')
        result = run_hook("scan-secrets.py", payload)
        self.assertEqual(result.returncode, 2, result.stderr)
        self.assertIn("BLOCKED", result.stderr)

    def test_codex_patch_allows_clean_content(self):
        payload = codex_patch(
            Path("settings.py"),
            "API_KEY = os.environ['API_KEY']",
        )
        result = run_hook("scan-secrets.py", payload)
        self.assertEqual(result.returncode, 0, result.stderr)


class ProtectConfigsTest(unittest.TestCase):
    def test_blocks_existing_linter_config(self):
        with tempfile.TemporaryDirectory() as tmp:
            config = Path(tmp) / ".eslintrc.json"
            config.write_text("{}")
            result = run_hook(
                "protect-configs.py", {"tool_input": {"file_path": str(config)}}
            )
            self.assertEqual(result.returncode, 2, result.stderr)

    def test_allows_creating_missing_config(self):
        with tempfile.TemporaryDirectory() as tmp:
            config = Path(tmp) / ".eslintrc.json"
            result = run_hook(
                "protect-configs.py", {"tool_input": {"file_path": str(config)}}
            )
            self.assertEqual(result.returncode, 0, result.stderr)

    def test_allows_ordinary_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            source = Path(tmp) / "app.py"
            source.write_text("x = 1\n")
            result = run_hook(
                "protect-configs.py", {"tool_input": {"file_path": str(source)}}
            )
            self.assertEqual(result.returncode, 0, result.stderr)

    def test_codex_patch_blocks_existing_linter_config(self):
        with tempfile.TemporaryDirectory() as tmp:
            config = Path(tmp) / ".eslintrc.js"
            config.write_text("module.exports = {};\n")
            result = run_hook(
                "protect-configs.py",
                codex_patch(config, "module.exports = { rules: {} };"),
            )
            self.assertEqual(result.returncode, 2, result.stderr)
            self.assertIn("BLOCKED", result.stderr)

    def test_codex_patch_allows_ordinary_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            source = Path(tmp) / "app.py"
            source.write_text("old\n")
            result = run_hook(
                "protect-configs.py",
                codex_patch(source, "new"),
            )
            self.assertEqual(result.returncode, 0, result.stderr)


class AuditDebugPrintsTest(unittest.TestCase):
    def check(self, name, body):
        with tempfile.TemporaryDirectory() as tmp:
            source = Path(tmp) / name
            source.write_text(body)
            return run_hook(
                "audit-debug-prints.py", {"tool_input": {"file_path": str(source)}}
            )

    def test_flags_standalone_print(self):
        result = self.check("app.py", "print('debug')\n")
        self.assertEqual(result.returncode, 2, result.stderr)

    def test_flags_embedded_print(self):
        result = self.check("app.py", "x = fn(); print(x)\n")
        self.assertEqual(result.returncode, 2, result.stderr)

    def test_flags_console_log(self):
        result = self.check("app.ts", "const x = 1; console.log(x);\n")
        self.assertEqual(result.returncode, 2, result.stderr)

    def test_allows_logging(self):
        result = self.check("app.py", "logger.info('event', extra={'x': 1})\n")
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_codex_patch_flags_debug_print_without_rolling_back(self):
        with tempfile.TemporaryDirectory() as tmp:
            source = Path(tmp) / "app.ts"
            body = "const x = 1; console.log(x);\n"
            source.write_text(body)
            result = run_hook(
                "audit-debug-prints.py",
                codex_patch(source, "const x = 1; console.log(x);"),
            )
            self.assertEqual(result.returncode, 2, result.stderr)
            self.assertIn("WARNING", result.stderr)
            self.assertEqual(source.read_text(), body)

    def test_codex_patch_allows_clean_content(self):
        with tempfile.TemporaryDirectory() as tmp:
            source = Path(tmp) / "app.ts"
            source.write_text("logger.info('event');\n")
            result = run_hook(
                "audit-debug-prints.py",
                codex_patch(source, "logger.info('event');"),
            )
            self.assertEqual(result.returncode, 0, result.stderr)


class HookPayloadBoundaryTest(unittest.TestCase):
    def test_generated_payloads_hold_invariants(self):
        from hooks import hook_payload

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
            for path in paths:
                self.assertIsInstance(path, Path)
            self.assertEqual(out.getvalue(), "")
            self.assertEqual(err.getvalue(), "")


class SessionStartTest(unittest.TestCase):
    def _run(self, env: dict[str, str]) -> subprocess.CompletedProcess[str]:
        process_env = os.environ.copy()
        process_env.pop("PLUGIN_ROOT", None)
        process_env.pop("CLAUDE_PLUGIN_ROOT", None)
        process_env.update(env)
        return subprocess.run(
            [sys.executable, str(HOOKS / "session-start.py")],
            capture_output=True,
            text=True,
            env=process_env,
            check=True,
        )

    def _assert_contract(self, stdout: str) -> str:
        output = json.loads(stdout)["hookSpecificOutput"]
        self.assertEqual(output["hookEventName"], "SessionStart")
        context = output["additionalContext"]
        self.assertIn("<code-craft-bootstrap>", context)
        self.assertIn("using-code-craft", context)
        return context

    def test_codex_plugin_root_takes_precedence(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            skill_dir = root / "skills" / "using-code-craft"
            skill_dir.mkdir(parents=True)
            skill_dir.joinpath("SKILL.md").write_text(
                "# using-code-craft\n\ncodex-root-marker\n",
                encoding="utf-8",
            )
            result = self._run(
                {
                    "PLUGIN_ROOT": str(root),
                    "CLAUDE_PLUGIN_ROOT": str(HOOKS.parent),
                }
            )
            context = self._assert_contract(result.stdout)
            self.assertIn("codex-root-marker", context)

    def test_claude_plugin_root_remains_supported(self):
        result = self._run({"CLAUDE_PLUGIN_ROOT": str(HOOKS.parent)})
        self._assert_contract(result.stdout)


if __name__ == "__main__":
    unittest.main()
