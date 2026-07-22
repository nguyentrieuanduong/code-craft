import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
WORKFLOW = ROOT / ".github" / "workflows" / "ci.yml"


class CiConfigTest(unittest.TestCase):
    def test_workflow_uses_only_deterministic_check(self):
        source = WORKFLOW.read_text()
        self.assertIn("python3 -m tools.check", source)
        for forbidden in (
            "claude",
            "ANTHROPIC_API_KEY",
            "tests/scenarios/run.py",
            "--allow-many",
            "subagent",
        ):
            with self.subTest(forbidden=forbidden):
                self.assertNotIn(forbidden, source)

    def test_command_guard_rejects_behavioral_runner(self):
        from tools import check

        with self.assertRaisesRegex(RuntimeError, "tests/scenarios/run.py"):
            check.assert_deterministic_commands(
                (("python3", "tests/scenarios/run.py", "--dry-run"),)
            )

    def test_command_guard_rejects_model_executable(self):
        from tools import check

        with self.assertRaisesRegex(RuntimeError, "claude"):
            check.assert_deterministic_commands((("claude", "-p", "test"),))


if __name__ == "__main__":
    unittest.main()
