#!/usr/bin/env python3
"""Regression tests for the scenario eval runner (no claude calls).

Covers scenario parsing, transcript parsing, every check type, and the
shipped corpus + fixtures. Run: python3 -m unittest discover tests
"""
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "scenarios"))
import run as runner  # noqa: E402

SAMPLE_SCENARIO = """---
name: sample
skill: skills/test-driven-development/SKILL.md
fixture: py-calculator
setup: echo ready
---

## Prompt

Do the thing.

## Checks

```json
[{"type": "output_matches", "pattern": "done"}]
```

## Notes

None.
"""


def transcript(tool_uses=(), final_text=""):
    return {"tool_uses": list(tool_uses), "final_text": final_text}


class ParseScenarioTest(unittest.TestCase):
    def write(self, text):
        handle = tempfile.NamedTemporaryFile(
            "w", suffix=".md", delete=False, dir=tempfile.gettempdir()
        )
        handle.write(text)
        handle.close()
        return Path(handle.name)

    def test_parses_all_fields(self):
        scenario = runner.parse_scenario(self.write(SAMPLE_SCENARIO))
        self.assertEqual(scenario["name"], "sample")
        self.assertEqual(scenario["fixture"], "py-calculator")
        self.assertEqual(scenario["setup"], "echo ready")
        self.assertEqual(scenario["prompt"], "Do the thing.")
        self.assertEqual(scenario["checks"][0]["type"], "output_matches")

    def test_rejects_unknown_check_type(self):
        bad = SAMPLE_SCENARIO.replace("output_matches", "bogus_check")
        with self.assertRaises(ValueError):
            runner.parse_scenario(self.write(bad))

    def test_rejects_missing_prompt(self):
        bad = SAMPLE_SCENARIO.replace("## Prompt", "## Preamble")
        with self.assertRaises(ValueError):
            runner.parse_scenario(self.write(bad))

    def test_parses_folded_setup(self):
        source = SAMPLE_SCENARIO.replace(
            "setup: echo ready",
            "setup: >-\n  echo ready",
        )
        self.assertEqual(
            runner.parse_scenario(self.write(source))["setup"],
            "echo ready",
        )

    def test_rejects_invalid_frontmatter(self):
        invalid = (
            SAMPLE_SCENARIO.replace("name: sample", "name: one\nname: two"),
            SAMPLE_SCENARIO.replace("name: sample", "name: sample\nextra: true"),
            SAMPLE_SCENARIO.replace(
                "setup: echo ready", "setup: echo ready\nmax_turns: true"
            ),
        )
        for source in invalid:
            with self.subTest(source=source):
                with self.assertRaises(ValueError):
                    runner.parse_scenario(self.write(source))


class ScenarioCliTest(unittest.TestCase):
    def run_cli(self, *arguments):
        with tempfile.TemporaryDirectory() as results_dir:
            return subprocess.run(
                [
                    sys.executable,
                    str(runner.SCENARIOS_DIR / "run.py"),
                    *arguments,
                    "--claude-bin",
                    "true",
                    "--results-dir",
                    results_dir,
                ],
                capture_output=True,
                text=True,
                check=False,
            )

    def test_model_run_requires_selector(self):
        completed = self.run_cli()
        self.assertEqual(completed.returncode, 2)
        self.assertIn("require scenario paths or explicit --all", completed.stderr)

    def test_allow_many_requires_numeric_budget(self):
        completed = self.run_cli("--all", "--allow-many", "many")
        self.assertEqual(completed.returncode, 2)
        self.assertIn("--allow-many", completed.stderr)

    def test_budget_below_planned_calls_is_rejected(self):
        scenario = str(runner.find_scenarios()[0])
        completed = self.run_cli(
            scenario,
            "--arm",
            "both",
            "--reps",
            "2",
            "--allow-many",
            "1",
        )
        self.assertEqual(completed.returncode, 2)
        self.assertIn("planned model calls: 4; budget: 1", completed.stderr)

    def test_repetitions_must_be_positive(self):
        scenario = str(runner.find_scenarios()[0])
        completed = self.run_cli(scenario, "--reps", "0")
        self.assertEqual(completed.returncode, 2)
        self.assertIn("--reps must be >= 1", completed.stderr)


class ParseTranscriptTest(unittest.TestCase):
    def test_falls_back_to_last_assistant_text_without_result(self):
        lines = [
            json.dumps(
                {
                    "type": "assistant",
                    "message": {
                        "content": [
                            {"type": "text", "text": "first pass"},
                            {
                                "type": "tool_use",
                                "name": "Bash",
                                "input": {"command": "ls"},
                            },
                        ]
                    },
                }
            ),
            json.dumps(
                {
                    "type": "assistant",
                    "message": {
                        "content": [{"type": "text", "text": "second pass"}]
                    },
                }
            ),
        ]
        parsed = runner.parse_transcript("\n".join(lines))
        self.assertEqual(parsed["final_text"], "second pass")

    def test_rate_limit_detected_in_final_or_stderr(self):
        self.assertTrue(
            runner.looks_rate_limited(
                "You've hit your limit · resets 10:40pm", ""
            )
        )
        self.assertTrue(runner.looks_rate_limited("", "HTTP 429 rate-limited"))
        self.assertFalse(runner.looks_rate_limited("all green", ""))

    def test_extracts_tools_and_result(self):
        lines = [
            json.dumps(
                {
                    "type": "assistant",
                    "message": {
                        "content": [
                            {"type": "text", "text": "running"},
                            {
                                "type": "tool_use",
                                "name": "Bash",
                                "input": {"command": "python3 -m unittest"},
                            },
                        ]
                    },
                }
            ),
            "not json",
            json.dumps({"type": "result", "result": "all green"}),
        ]
        parsed = runner.parse_transcript("\n".join(lines))
        self.assertEqual(
            parsed["tool_uses"],
            [("Bash", {"command": "python3 -m unittest"})],
        )
        self.assertEqual(parsed["final_text"], "all green")


class EvaluateCheckTest(unittest.TestCase):
    def setUp(self):
        self.workspace = Path(tempfile.mkdtemp())
        (self.workspace / ".plans").mkdir(parents=True)
        (self.workspace / ".plans" / "p.md").write_text(
            "# Plan\n- [ ] 1.1 run `python3 -m unittest`\n"
        )
        (self.workspace / "calculator.py").write_text("def add(): pass\n")

    def check(self, spec, transcript_):
        return runner.evaluate_check(spec, transcript_, self.workspace)

    def test_output_matches(self):
        t = transcript(final_text="CHOICE: A")
        self.assertTrue(
            self.check({"type": "output_matches", "pattern": "CHOICE:\\s*A"}, t)
        )
        self.assertFalse(
            self.check({"type": "output_matches", "pattern": "CHOICE:\\s*B"}, t)
        )
        self.assertTrue(
            self.check(
                {"type": "output_not_matches", "pattern": "CHOICE:\\s*B"}, t
            )
        )

    def test_file_checks(self):
        t = transcript()
        self.assertTrue(
            self.check({"type": "file_exists", "glob": ".plans/*.md"}, t)
        )
        self.assertFalse(
            self.check({"type": "file_exists", "glob": "docs/specs/*.md"}, t)
        )
        self.assertTrue(
            self.check({"type": "file_not_exists", "glob": "*.rs"}, t)
        )
        self.assertTrue(
            self.check(
                {
                    "type": "file_matches",
                    "glob": ".plans/*.md",
                    "pattern": "unittest",
                },
                t,
            )
        )
        self.assertTrue(
            self.check(
                {
                    "type": "file_not_matches",
                    "glob": ".plans/*.md",
                    "pattern": "TBD",
                },
                t,
            )
        )

    def test_anywhere_matches_via_output_or_file(self):
        spec = {
            "type": "anywhere_matches",
            "glob": ".plans/*.md",
            "pattern": "(?i)pre-?mortem",
        }
        self.assertTrue(
            self.check(spec, transcript(final_text="ran the premortem"))
        )
        self.assertFalse(self.check(spec, transcript(final_text="nope")))
        (self.workspace / ".plans" / "p.md").write_text(
            "## Pre-mortem\nchecked anti-patterns\n"
        )
        self.assertTrue(self.check(spec, transcript(final_text="nope")))

    def test_command_checks(self):
        t = transcript(
            tool_uses=[("Bash", {"command": "python3 -m unittest discover"})]
        )
        self.assertTrue(
            self.check({"type": "ran_command", "pattern": "unittest"}, t)
        )
        self.assertTrue(
            self.check({"type": "not_ran_command", "pattern": "git merge"}, t)
        )
        self.assertFalse(
            self.check({"type": "not_ran_command", "pattern": "unittest"}, t)
        )

    def test_test_written_before_source(self):
        spec = {
            "type": "test_written_before_source",
            "test_glob": "test_*.py",
            "source_glob": "calculator.py",
        }
        ws = str(self.workspace)
        test_first = transcript(
            tool_uses=[
                ("Edit", {"file_path": f"{ws}/test_calculator.py"}),
                ("Edit", {"file_path": f"{ws}/calculator.py"}),
            ]
        )
        source_first = transcript(
            tool_uses=[
                ("Edit", {"file_path": f"{ws}/calculator.py"}),
                ("Write", {"file_path": f"{ws}/test_calculator.py"}),
            ]
        )
        no_test = transcript(
            tool_uses=[("Edit", {"file_path": f"{ws}/calculator.py"})]
        )
        self.assertTrue(self.check(spec, test_first))
        self.assertFalse(self.check(spec, source_first))
        self.assertFalse(self.check(spec, no_test))

    def test_files_untouched(self):
        spec = {"type": "files_untouched", "glob": "calculator.py"}
        ws = str(self.workspace)
        untouched = transcript(
            tool_uses=[("Write", {"file_path": f"{ws}/.plans/p.md"})]
        )
        touched = transcript(
            tool_uses=[("Edit", {"file_path": f"{ws}/calculator.py"})]
        )
        self.assertTrue(self.check(spec, untouched))
        self.assertFalse(self.check(spec, touched))


class RepLabelTest(unittest.TestCase):
    def test_no_rep_keeps_base_label(self):
        self.assertEqual(runner.rep_label("haiku", None), "haiku")
        self.assertIsNone(runner.rep_label(None, None))

    def test_rep_suffix_keeps_filenames_distinct(self):
        self.assertEqual(runner.rep_label("haiku", 3), "haiku-r3")
        self.assertEqual(runner.rep_label(None, 3), "r3")


class DisallowedToolsTest(unittest.TestCase):
    def test_both_plan_mode_tools_blocked(self):
        # EnterPlanMode alone is enough to leak plan drafts into
        # ~/.claude/plans/ (observed 2026-07-14 baseline runs); ExitPlanMode
        # alone leaves runs ending without a result event. Both must stay.
        blocked = runner.DISALLOWED_TOOLS.split(",")
        self.assertIn("EnterPlanMode", blocked)
        self.assertIn("ExitPlanMode", blocked)


class CorpusTest(unittest.TestCase):
    def test_all_shipped_scenarios_parse(self):
        scenarios = runner.find_scenarios()
        self.assertGreaterEqual(len(scenarios), 11)
        for path in scenarios:
            with self.subTest(scenario=str(path)):
                parsed = runner.parse_scenario(path)
                self.assertTrue(parsed["checks"])
                skill = runner.REPO_ROOT / parsed["skill"]
                self.assertTrue(skill.is_file(), f"missing skill {skill}")
                if parsed["fixture"]:
                    fixture = (
                        runner.SCENARIOS_DIR / "fixtures" / parsed["fixture"]
                    )
                    self.assertTrue(fixture.is_dir(), f"missing {fixture}")


class FixtureTest(unittest.TestCase):
    def build(self, variant):
        workspace = Path(tempfile.mkdtemp())
        setup = (
            runner.SCENARIOS_DIR / "fixtures" / "feature-branch" / "setup.sh"
        )
        subprocess.run(
            ["bash", str(setup), variant],
            cwd=workspace,
            check=True,
            capture_output=True,
        )
        return workspace

    def suite_passes(self, workspace):
        result = subprocess.run(
            [sys.executable, "-m", "unittest", "discover", "tests"],
            cwd=workspace,
            capture_output=True,
        )
        return result.returncode == 0

    def test_small_variant_is_green(self):
        self.assertTrue(self.suite_passes(self.build("small")))

    def test_broken_variant_fails(self):
        self.assertFalse(self.suite_passes(self.build("broken")))

    def test_large_variant_diff_exceeds_400_lines(self):
        workspace = self.build("large")
        self.assertTrue(self.suite_passes(workspace))
        stat = subprocess.run(
            ["git", "diff", "--shortstat", "main...HEAD"],
            cwd=workspace,
            capture_output=True,
            text=True,
            check=True,
        )
        insertions = int(
            next(
                part.strip().split()[0]
                for part in stat.stdout.split(",")
                if "insertion" in part
            )
        )
        self.assertGreater(insertions, 400)


if __name__ == "__main__":
    unittest.main()
