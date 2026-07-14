"""Contracts for packaging code-craft as a native Codex plugin."""

import re
import unittest
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


if __name__ == "__main__":
    unittest.main()
