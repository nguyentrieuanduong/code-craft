import contextlib
import io
import tempfile
import unittest
from pathlib import Path

import yaml

from tools import catalog


class CatalogTest(unittest.TestCase):
    def setUp(self):
        self.root = Path(tempfile.mkdtemp())
        (self.root / "skills").mkdir()
        (self.root / "tests").mkdir()

    def write_skill(self, name, description=None, directory=None):
        path = self.root / "skills" / (directory or name) / "SKILL.md"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(
            "---\n"
            f"name: {name}\n"
            f"description: {description or f'Use when {name} work applies.'}\n"
            "---\n\n"
            f"# {name}\n"
        )
        return path

    def write_cases(self, skills):
        names = tuple(skills)
        cases = {}
        for index, name in enumerate(names):
            owner = names[(index + 1) % len(names)]
            cases[name] = {
                "positive": [f"{name} task"] * 3,
                "negative": [
                    {"prompt": f"{owner} task", "owner": owner},
                    {"prompt": f"{owner} work", "owner": owner},
                ],
            }
        source = {"version": 1, "top_k": 3, "skills": cases}
        (self.root / "tests" / "routing_cases.yaml").write_text(
            yaml.safe_dump(source, sort_keys=False)
        )
        return source

    def build_valid_repository(self, names=("alpha", "beta")):
        for name in names:
            self.write_skill(name)
        return self.write_cases(names)

    def test_loads_folded_description(self):
        path = self.root / "skills" / "folded" / "SKILL.md"
        path.parent.mkdir()
        path.write_text(
            "---\nname: folded\ndescription: >-\n"
            "  Use when folded routing applies.\n---\n"
        )
        skill = catalog.load_skill(path)
        self.assertEqual(skill.description, "Use when folded routing applies.")

    def test_reports_name_directory_mismatch(self):
        self.write_skill("alpha", directory="wrong-directory")
        self.write_skill("beta")
        self.write_cases(("alpha", "beta"))
        report = catalog.validate_repository(self.root)
        self.assertTrue(
            any("does not match directory" in error for error in report.errors)
        )

    def test_reports_missing_routing_coverage(self):
        cases = self.build_valid_repository()
        del cases["skills"]["beta"]
        (self.root / "tests" / "routing_cases.yaml").write_text(
            yaml.safe_dump(cases, sort_keys=False)
        )
        report = catalog.validate_repository(self.root)
        self.assertIn("beta: missing routing cases", report.errors)

    def test_reports_positive_owner_outside_top_three(self):
        descriptions = {
            "alpha": "Use when alpha rare applies.",
            "beta": "Use when beta banana routing applies.",
            "gamma": "Use when gamma grape routing applies.",
            "delta": "Use when delta date routing applies.",
        }
        for name, description in descriptions.items():
            self.write_skill(name, description)
        cases = self.write_cases(descriptions)
        cases["skills"]["alpha"]["positive"] = [
            "alpha beta banana gamma grape delta date routing"
        ] * 3
        (self.root / "tests" / "routing_cases.yaml").write_text(
            yaml.safe_dump(cases, sort_keys=False)
        )
        report = catalog.validate_repository(self.root)
        self.assertTrue(any("outside top 3" in error for error in report.errors))

    def test_reports_owner_below_named_impostor(self):
        cases = self.build_valid_repository()
        cases["skills"]["alpha"]["negative"][0] = {
            "prompt": "alpha task",
            "owner": "beta",
        }
        (self.root / "tests" / "routing_cases.yaml").write_text(
            yaml.safe_dump(cases, sort_keys=False)
        )
        report = catalog.validate_repository(self.root)
        self.assertTrue(
            any("does not outrank alpha" in error for error in report.errors)
        )

    def test_named_owner_can_win_deterministic_score_tie(self):
        cases = self.build_valid_repository()
        cases["skills"]["beta"]["negative"][0] = {
            "prompt": "alpha beta task",
            "owner": "alpha",
        }
        (self.root / "tests" / "routing_cases.yaml").write_text(
            yaml.safe_dump(cases, sort_keys=False)
        )
        report = catalog.validate_repository(self.root)
        self.assertFalse(
            any("does not outrank beta" in error for error in report.errors)
        )

    def test_excludes_cross_skill_references_from_routing_text(self):
        skills = (
            catalog.Skill(
                name="alpha",
                description="Use when alpha follows code-review and code review.",
                path=Path("alpha/SKILL.md"),
                frontmatter_chars=1,
            ),
            catalog.Skill(
                name="code-review",
                description="Use when reviewing completed code.",
                path=Path("code-review/SKILL.md"),
                frontmatter_chars=1,
            ),
        )
        cleaned = catalog.routing_description(
            skills[0], frozenset(skill.name for skill in skills)
        )
        self.assertNotIn("code-review", cleaned)
        self.assertNotIn("code review", cleaned)

    def test_severe_collision_warns_without_failing(self):
        description = "Use when shared collision vocabulary applies."
        self.write_skill("alpha", description)
        self.write_skill("beta", description)
        self.write_cases(("alpha", "beta"))
        report = catalog.validate_repository(self.root)
        self.assertEqual(report.errors, ())
        self.assertTrue(any("severe collision" in item for item in report.warnings))

    def test_rank_first_drop_does_not_change_exit_status(self):
        self.write_skill("alpha", "Use when alpha operations apply.")
        self.write_skill("beta", "Use when beta banana routing applies.")
        cases = self.write_cases(("alpha", "beta"))
        cases["skills"]["alpha"]["positive"] = [
            "alpha beta banana routing"
        ] * 3
        (self.root / "tests" / "routing_cases.yaml").write_text(
            yaml.safe_dump(cases, sort_keys=False)
        )
        report = catalog.validate_repository(self.root)
        self.assertEqual(report.errors, ())
        self.assertLess(report.rank_first_passed, report.rank_first_total)
        with contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(catalog.main([str(self.root)]), 0)


if __name__ == "__main__":
    unittest.main()
