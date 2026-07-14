"""Contracts for packaging code-craft as a native Codex plugin."""

import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
from importlib.util import find_spec
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent
RUNTIME_REFERENCES = {
    "tool-mapping": Path("skills/using-code-craft/references/tool-mapping.md"),
    "anti-patterns": Path("skills/using-code-craft/references/anti-patterns.md"),
    "evidence": Path("skills/using-code-craft/references/evidence.md"),
    "model-routing": Path("skills/dispatching-parallel-agents/references/model-routing.md"),
}
SKILL_LINKS = {
    Path("skills/using-git-worktrees/SKILL.md"): (
        "../using-code-craft/references/tool-mapping.md",
    ),
    Path("skills/dispatching-parallel-agents/SKILL.md"): (
        "references/model-routing.md",
    ),
    Path("skills/writing-plans/SKILL.md"): (
        "../using-code-craft/references/anti-patterns.md",
    ),
    Path("skills/releasing-safely/SKILL.md"): (
        "../using-code-craft/references/anti-patterns.md",
    ),
    Path("skills/code-review/SKILL.md"): (
        "../using-code-craft/references/evidence.md",
    ),
    Path("skills/finishing-work/SKILL.md"): (
        "../using-code-craft/references/evidence.md",
    ),
}
ROOT_RUNTIME_LINK = re.compile(
    r"docs/(?:tool-mapping|anti-patterns|evidence|model-routing)\.md"
)
MARKDOWN_LINK = re.compile(r"\[[^]]+\]\(([^)]+)\)")
PLUGIN_VALIDATOR = (
    Path.home()
    / ".codex/skills/.system/plugin-creator/scripts/validate_plugin.py"
)
CODEX_CLI = shutil.which("codex")


def _read_json(relative_path: str) -> dict[str, object]:
    path = REPO_ROOT / relative_path
    with path.open(encoding="utf-8") as stream:
        value = json.load(stream)
    if not isinstance(value, dict):
        raise AssertionError(f"expected object in {relative_path}")
    return value


class RuntimeReferencePackagingTest(unittest.TestCase):
    def test_runtime_references_are_packaged_with_skills(self) -> None:
        for name, relative_path in RUNTIME_REFERENCES.items():
            with self.subTest(reference=name):
                path = REPO_ROOT / relative_path
                self.assertTrue(path.is_file(), f"missing packaged reference: {relative_path}")
                self.assertTrue(path.read_text(encoding="utf-8").strip())

    def test_skill_links_resolve_to_readable_runtime_references(self) -> None:
        for skill_relative, links in SKILL_LINKS.items():
            skill_path = REPO_ROOT / skill_relative
            content = skill_path.read_text(encoding="utf-8")
            for link in links:
                with self.subTest(skill=skill_relative, link=link):
                    self.assertIn(link, content)
                    target = (skill_path.parent / link).resolve()
                    self.assertTrue(target.is_file(), f"unresolved skill link: {link}")
                    self.assertTrue(target.read_text(encoding="utf-8").strip())

    def test_root_docs_are_short_noncyclic_compatibility_pointers(self) -> None:
        for name, canonical_relative in RUNTIME_REFERENCES.items():
            with self.subTest(reference=name):
                pointer = REPO_ROOT / "docs" / f"{name}.md"
                content = pointer.read_text(encoding="utf-8")
                self.assertLessEqual(len(content.splitlines()), 10)
                links = MARKDOWN_LINK.findall(content)
                self.assertEqual(len(links), 1, f"expected one compatibility link in {pointer}")
                resolved = (pointer.parent / links[0]).resolve()
                self.assertEqual(resolved, (REPO_ROOT / canonical_relative).resolve())
                self.assertTrue(resolved.is_file())

    def test_skills_do_not_link_to_root_runtime_docs(self) -> None:
        for skill_path in sorted((REPO_ROOT / "skills").glob("*/SKILL.md")):
            with self.subTest(skill=skill_path.parent.name):
                content = skill_path.read_text(encoding="utf-8")
                self.assertIsNone(ROOT_RUNTIME_LINK.search(content))


class CodexPluginManifestTest(unittest.TestCase):
    def test_plugin_manifest_has_complete_installable_metadata(self) -> None:
        manifest = _read_json(".codex-plugin/plugin.json")
        required = {
            "name",
            "version",
            "skills",
            "hooks",
            "interface",
            "author",
            "license",
        }
        self.assertTrue(required.issubset(manifest))
        self.assertEqual(manifest["name"], "code-craft")

        interface = manifest["interface"]
        self.assertIsInstance(interface, dict)
        default_prompt = interface.get("defaultPrompt")
        self.assertIsInstance(default_prompt, list)
        self.assertTrue(default_prompt)
        self.assertTrue(all(isinstance(item, str) and item for item in default_prompt))

        for field in ("skills", "hooks"):
            with self.subTest(field=field):
                relative = manifest[field]
                self.assertIsInstance(relative, str)
                target = (REPO_ROOT / relative).resolve()
                self.assertTrue(target.is_relative_to(REPO_ROOT.resolve()))
                self.assertTrue(target.exists(), f"missing manifest path: {relative}")

        claude_manifest = _read_json(".claude-plugin/plugin.json")
        self.assertEqual(manifest["version"], claude_manifest["version"])

    def test_marketplace_points_to_the_repository_plugin(self) -> None:
        marketplace = _read_json(".agents/plugins/marketplace.json")
        plugins = marketplace.get("plugins")
        self.assertIsInstance(plugins, list)
        self.assertEqual(len(plugins), 1)
        plugin = plugins[0]
        self.assertIsInstance(plugin, dict)
        self.assertEqual(plugin.get("name"), "code-craft")
        self.assertNotIn("description", plugin)
        self.assertEqual(plugin.get("source"), {"source": "local", "path": "./"})

    def test_codex_hooks_manifest_has_the_five_planned_commands(self) -> None:
        manifest = _read_json("hooks/codex-hooks.json")
        hooks = manifest.get("hooks")
        self.assertIsInstance(hooks, dict)
        expected_matchers = {
            "SessionStart": ["startup|resume|clear|compact"],
            "PreToolUse": ["Edit|Write", "Bash"],
            "PostToolUse": ["Edit|Write"],
        }
        commands: list[dict[str, object]] = []
        for event, matchers in expected_matchers.items():
            with self.subTest(event=event):
                groups = hooks.get(event)
                self.assertIsInstance(groups, list)
                self.assertEqual([group.get("matcher") for group in groups], matchers)
                for group in groups:
                    commands.extend(group["hooks"])

        self.assertEqual(len(commands), 5)
        for command in commands:
            self.assertEqual(command.get("type"), "command")
            self.assertIsInstance(command.get("command"), str)
            self.assertIsInstance(command.get("commandWindows"), str)
            self.assertEqual(command.get("timeout"), 30)
        serialized = json.dumps(manifest)
        self.assertNotIn("guard-installs.py", serialized)

    def test_suite_version_and_skill_count_are_release_ready(self) -> None:
        claude_manifest = _read_json(".claude-plugin/plugin.json")
        self.assertEqual(claude_manifest.get("version"), "0.3.0")
        skill_files = sorted((REPO_ROOT / "skills").glob("*/SKILL.md"))
        self.assertEqual(len(skill_files), 15)

    @unittest.skipUnless(
        PLUGIN_VALIDATOR.is_file() and find_spec("yaml") is not None,
        "Codex plugin validator or its authoring-only PyYAML dependency unavailable",
    )
    def test_validator_rejects_only_its_stale_hooks_schema(self) -> None:
        completed = subprocess.run(
            [sys.executable, str(PLUGIN_VALIDATOR), str(REPO_ROOT)],
            check=False,
            capture_output=True,
            text=True,
        )
        self.assertEqual(completed.returncode, 1)
        output = f"{completed.stdout}\n{completed.stderr}"
        error_lines = [
            line.strip()
            for line in output.splitlines()
            if line.strip().startswith("- ")
        ]
        self.assertEqual(
            error_lines,
            ["- plugin.json field `hooks` is not accepted by plugin validation"],
        )


@unittest.skipUnless(CODEX_CLI, "Codex CLI unavailable")
class CodexPluginInstallTest(unittest.TestCase):
    def _run(
        self,
        codex_home: str,
        *arguments: str,
    ) -> object:
        env = os.environ.copy()
        env["CODEX_HOME"] = codex_home
        completed = subprocess.run(
            [CODEX_CLI, "plugin", *arguments, "--json"],
            check=False,
            capture_output=True,
            env=env,
            text=True,
            timeout=30,
        )
        self.assertEqual(completed.returncode, 0, completed.stderr)
        return json.loads(completed.stdout)

    def test_repo_marketplace_installs_and_removes_plugin(self) -> None:
        with tempfile.TemporaryDirectory() as codex_home:
            self._run(
                codex_home,
                "marketplace",
                "add",
                str(REPO_ROOT.resolve()),
            )
            self._run(codex_home, "add", "code-craft@code-craft")

            listed = self._run(codex_home, "list")
            self.assertIsInstance(listed, dict)
            installed_plugins = listed.get("installed")
            self.assertIsInstance(installed_plugins, list)
            installed = [
                plugin
                for plugin in installed_plugins
                if isinstance(plugin, dict) and plugin.get("name") == "code-craft"
            ]
            self.assertEqual(len(installed), 1)
            self.assertEqual(installed[0].get("version"), "0.3.0")

            removed = self._run(codex_home, "remove", "code-craft@code-craft")
            self.assertIn("code-craft", json.dumps(removed))

            listed_after_remove = self._run(codex_home, "list")
            self.assertIsInstance(listed_after_remove, dict)
            remaining = listed_after_remove.get("installed")
            self.assertIsInstance(remaining, list)
            self.assertFalse(
                any(
                    isinstance(plugin, dict)
                    and plugin.get("name") == "code-craft"
                    for plugin in remaining
                )
            )


if __name__ == "__main__":
    unittest.main()
