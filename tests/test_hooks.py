#!/usr/bin/env python3
"""Regression tests for the enforcement hooks.

Each hook is exercised as a subprocess with real hook JSON on stdin,
exactly as Claude Code invokes it. Exit 2 = blocked/flagged, 0 = allowed.

Run: python3 -m unittest discover tests
"""
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

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


if __name__ == "__main__":
    unittest.main()
