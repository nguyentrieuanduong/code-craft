"""Rules that originate in code-craft, not in an upstream source.

A reference refresh that re-ports an upstream skill must merge these back
in, never drop them. Each assertion names the rule it protects.
"""

import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
STANDARDS = ROOT / "skills" / "coding-standards" / "SKILL.md"
BOOTSTRAP = ROOT / "skills" / "using-code-craft" / "SKILL.md"
SECURITY = ROOT / "skills" / "security-baseline" / "SKILL.md"
SKILLS_README = ROOT / "skills" / "README.md"
NUMBER_WORDS = {9: "nine", 10: "ten", 11: "eleven", 12: "twelve"}
REFRESH_HINT = "local code-craft rule; merge it back after a reference refresh"


class WorkingFilesRuleTest(unittest.TestCase):
    def test_working_files_section_is_present(self):
        text = " ".join(STANDARDS.read_text().split())
        for required in (
            "## Working files",
            "visible, git-ignored scratch folder in the project — `tmp/` by default — not `/tmp`, `$TMPDIR` or `~`",
            "(`git rev-parse --git-path info/exclude`), not `.gitignore`",
            "discovery walks `tmp/`, tell the user",
            "own subfolder; run nothing from inside it",
            "keep the OS temp API",
            "Never commit scratch",
        ):
            with self.subTest(required=required):
                self.assertIn(required, text, REFRESH_HINT)

    def test_bootstrap_points_scratch_to_project_tmp(self):
        self.assertIn(
            "Scratch (scripts, screenshots, output) goes in a git-ignored project folder like `tmp/`,"
            ' not `/tmp`, `$TMPDIR` or `~` — see coding-standards "Working files".',
            " ".join(BOOTSTRAP.read_text().split()),
            REFRESH_HINT,
        )


class SecurityBaselineRulesTest(unittest.TestCase):
    def setUp(self):
        self.text = SECURITY.read_text()
        self.rules = re.findall(r"^\*\*(SEC-\d{2}) ", self.text, re.MULTILINE)

    def test_sec10_is_present(self):
        self.assertIn("SEC-10", self.rules, REFRESH_HINT)
        for required in (
            "No machine-identifying data in version control",
            "OS temp paths, real account/user/session IDs",
            "personal hostnames or emails",
            "Private IPs and MAC addresses are guidance, not a gate",
            "logs or pasted output",
            "Code resolves home at runtime",
            "gitignored local config",
            "captured output before committing",
            "only a history rewrite removes it",
            "machine-identifying data (SEC-10)",
            "only a local path or an ID, not a secret",
        ):
            with self.subTest(required=required):
                self.assertIn(required, self.text, REFRESH_HINT)

    def test_checklist_does_not_gate_private_ips(self):
        checklist = self.text.split("## Pre-commit security checklist")[1].split("##")[0]
        self.assertNotIn("private IPs", checklist)

    def test_rules_are_numbered_without_gaps(self):
        expected = [f"SEC-{n:02d}" for n in range(1, len(self.rules) + 1)]
        self.assertEqual(self.rules, expected)

    def test_rule_count_matches_heading_and_catalog(self):
        word = NUMBER_WORDS[len(self.rules)]
        self.assertIn(f"## The {word} rules", self.text)
        self.assertIn(f"{word.capitalize()} blocking security rules", SKILLS_README.read_text())


if __name__ == "__main__":
    unittest.main()
