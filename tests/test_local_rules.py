"""Rules that originate in code-craft, not in an upstream source.

A reference refresh that re-ports an upstream skill must merge these back
in, never drop them. Each assertion names the rule it protects.
"""

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
STANDARDS = ROOT / "skills" / "coding-standards" / "SKILL.md"
REFRESH_HINT = "local code-craft rule; merge it back after a reference refresh"


class WorkingFilesRuleTest(unittest.TestCase):
    def test_working_files_section_is_present(self):
        text = STANDARDS.read_text()
        for required in (
            "## Working files",
            "project's visible `tmp/`, not `/tmp`, `$TMPDIR` or `~`",
            "(`git rev-parse --git-path info/exclude`), not `.gitignore`",
            "discovery walks `tmp/`, tell the user",
            "own subfolder; run nothing from inside it",
            "keep the OS temp API",
            "Never commit scratch",
        ):
            with self.subTest(required=required):
                self.assertIn(required, text, REFRESH_HINT)


if __name__ == "__main__":
    unittest.main()
