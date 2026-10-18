#!/usr/bin/env python3
"""Regression tests for the scenario eval runner (no claude calls).

Covers scenario parsing, transcript parsing, every check type, and the
shipped corpus + fixtures. Run: python3 -m unittest discover tests
"""
import json
import shutil
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

    def test_test_written_before_source_sees_bash_writes(self):
        spec = {
            "type": "test_written_before_source",
            "test_glob": "test_*.py",
            "source_glob": "calculator.py",
        }
        ws = str(self.workspace)
        heredoc_test_first = transcript(tool_uses=[
            ("Bash", {"command": "cat > test_calculator.py <<'EOF'\nimport unittest\nEOF"}),
            ("Bash", {"command": "cat >> calculator.py <<'EOF'\ndef f(a) -> int:\n    return a > 1\nEOF"}),
        ])
        python_variable_test_first = transcript(tool_uses=[
            ("Bash", {"command": "cat test_calculator.py"}),
            ("Bash", {"command": "python3 - <<'E'\np='test_calculator.py'\ns=open(p).read()\nopen(p,'w').write(s)\nE"}),
            ("Edit", {"file_path": f"{ws}/calculator.py"}),
        ])
        heredoc_source_first = transcript(tool_uses=[
            ("Bash", {"command": "cat > calculator.py <<'EOF'\nx = 1\nEOF"}),
            ("Write", {"file_path": f"{ws}/test_calculator.py"}),
        ])
        unattributable = transcript(tool_uses=[
            ("Bash", {"command": "python3 - <<'E'\nimport os\nopen(os.path.join('.', 'test_calculator.py'), 'w').write('x')\nE"}),
            ("Edit", {"file_path": f"{ws}/calculator.py"}),
        ])
        both_in_one_command = transcript(tool_uses=[
            ("Bash", {"command": "echo a > test_calculator.py && echo b > calculator.py"}),
        ])
        reads_only = transcript(tool_uses=[
            ("Bash", {"command": "cat test_calculator.py calculator.py 2>&1 | head"}),
            ("Edit", {"file_path": f"{ws}/calculator.py"}),
        ])
        self.assertIs(self.check(spec, heredoc_test_first), True)
        self.assertIs(self.check(spec, python_variable_test_first), True)
        self.assertIs(self.check(spec, heredoc_source_first), False)
        self.assertIsNone(self.check(spec, unattributable))
        self.assertIsNone(self.check(spec, both_in_one_command))
        self.assertIs(self.check(spec, reads_only), False)

    def test_test_written_before_source_reads_shell_segments(self):
        spec = {
            "type": "test_written_before_source",
            "test_glob": "test_*.py",
            "source_glob": "calculator.py",
        }
        ws = str(self.workspace)
        source_edit = ("Edit", {"file_path": f"{ws}/calculator.py"})
        test_edit = ("Edit", {"file_path": f"{ws}/test_calculator.py"})
        test_write = ("Write", {"file_path": f"{ws}/test_calculator.py"})

        def bash(command):
            return ("Bash", {"command": command})

        source_first = (
            [bash("pip install -q pytest && python3 -m pytest test_calculator.py"), source_edit, test_edit],
            [bash("cp calculator.py /tmp/calculator.py.orig"), source_edit, test_edit],
            [bash("sed -E -i 's/a/b/' calculator.py"), test_write],
            [bash("perl -pi -e 's/a/b/' calculator.py"), test_write],
            [bash("python3 -c \"open('calculator.py','r+').write('x')\""), test_write],
            [bash("python3 - <<'E'\nopen('calculator.py', encoding='utf-8', mode='w').write('x')\nE"), test_write],
            [bash("echo x &> calculator.py"), test_write],
        )
        for tools in source_first:
            with self.subTest(command=tools[0][1].get("command")):
                self.assertIs(self.check(spec, transcript(tool_uses=tools)), False)
        heredoc_with_code_text = [
            bash("cat > test_calculator.py <<'EOF'\nfrom pathlib import Path\np = Path('out')\np.write_text('calculator.py')\nEOF"),
            source_edit,
        ]
        self.assertIs(self.check(spec, transcript(tool_uses=heredoc_with_code_text)), True)
        for command in (
            "# Fix the subtraction bug\nsed -i 's/a + b/a - b/' calculator.py",
            "cd /repo  # go\necho 'def f(): pass' > calculator.py",
            "echo ${#args[@]}\nsed -i 's/a/b/' calculator.py",
            "sed -i \\\n  's/a/b/' calculator.py",
            "echo '# header' > calculator.py",
            "cat <<'PY' | python3\nopen('calculator.py', 'w').write('x')\nPY",
            "sudo -u me tee calculator.py < /dev/null",
            "bash -c \"echo x > calculator.py\"",
        ):
            with self.subTest(command=command):
                self.assertIs(self.check(spec, transcript(tool_uses=[bash(command), test_write])), False)
        commented_test_first = [bash("# write the failing test\ncat > test_calculator.py <<'EOF'\nimport unittest\nEOF"), source_edit]
        self.assertIs(self.check(spec, transcript(tool_uses=commented_test_first)), True)
        quoted_arrow = [bash("git commit -m 'boundary => calculator.py'"), test_write]
        self.assertIs(self.check(spec, transcript(tool_uses=quoted_arrow)), True)

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


SAMPLE_REPORT = """## Review

**Diff:** 1,111 changed lines — 2 actionable finding(s).
**Review independence:** not independent: inline fallback
Risk tier: standard
Verification evidence: none supplied
Merge readiness: not ready — verification evidence missing

### Verdicts
- **Spec compliance:** FAIL — tax.py still crashes
- Code quality: PASS — fine
- Security: PASS — no security findings
- Security pass: inline fallback

### Findings
F1. **Blocking** — `src/discount.py:6` — swallows ValueError;
  "10%" silently gives no discount — strip the sign in parse_percent.
2. Should-fix — src/tax.py:2 — same unstripped '%' parse.

### Pre-existing
- `legacy/report_export.py:2` — same class as tax.py, out of scope.

Nits
None

Declined to judge: None
"""


class ParseReportTest(unittest.TestCase):
    def test_reads_fields_and_derived_counts(self):
        report = runner.parse_report(SAMPLE_REPORT)
        fields = report["fields"]
        self.assertEqual(fields["changed lines"], "1111")
        self.assertEqual(fields["actionable"], "2")
        self.assertEqual(fields["review independence"], "not independent: inline fallback")
        self.assertEqual(fields["verification evidence"], "none supplied")
        self.assertTrue(fields["merge readiness"].startswith("not ready"))
        self.assertTrue(fields["spec compliance"].startswith("fail"))
        self.assertEqual(fields["security pass"], "inline fallback")

    def test_splits_sections_into_items_with_severity(self):
        sections = runner.parse_report(SAMPLE_REPORT)["sections"]
        findings = sections["findings"]
        self.assertEqual([item["severity"] for item in findings], ["blocking", "should-fix"])
        self.assertIn("parse_percent", findings[0]["text"])
        self.assertTrue(findings[1]["text"].startswith("should-fix — src/tax.py:2"))
        self.assertTrue(sections["pre-existing"][0]["text"].startswith("legacy/report_export.py:2"))
        self.assertEqual(sections["nits"], [])
        self.assertEqual(sections["declined to judge"], [])

    def test_heading_style_findings_are_items(self):
        text = "Diff: 5 changed lines — 1 actionable finding.\n\n## Findings\n\n### F1. Blocking — src/a.py:2 — wrong\n\nRecommendation: fix it.\n\n## Nits\n\nNone\n"
        findings = runner.parse_report(text)["sections"]["findings"]
        self.assertEqual(findings[0]["severity"], "blocking")
        self.assertTrue(findings[0]["text"].startswith("blocking — src/a.py:2"))

    def test_zero_words_count_as_zero(self):
        report = runner.parse_report("Diff: 27 changed lines — no actionable findings.\n")
        self.assertEqual(report["fields"]["actionable"], "0")

    def test_text_without_report_has_no_fields_or_sections(self):
        report = runner.parse_report("Looks good to me, ready to merge.")
        self.assertEqual(report, {"fields": {}, "sections": {}})


class ReportCheckTest(unittest.TestCase):
    def check(self, spec, text=SAMPLE_REPORT):
        return runner.evaluate_check(spec, transcript(final_text=text), Path("/tmp"))

    def test_field_checks(self):
        self.assertTrue(self.check({"type": "report_matches", "field": "actionable", "pattern": "^[12]$"}))
        self.assertFalse(self.check({"type": "report_matches", "field": "merge readiness", "pattern": "^ready"}))
        self.assertTrue(self.check({"type": "report_not_matches", "field": "risk tier", "pattern": "high"}))
        self.assertFalse(self.check({"type": "report_matches", "field": "absent", "pattern": "."}))

    def test_report_actionable_count(self):
        spec = {"type": "report_actionable_count"}
        header = "Diff: 41 changed lines — {n} actionable finding{s}.\n\nFindings\n"
        miscounted = header.format(n=1, s="") + (
            "F2. Blocking (status: still open, 4th round) — src/slug.py:5 — a--b — use +\n"
            "F3. Should-fix — tests/test_slug.py:10 — no test fails — add tests\n"
        )
        consistent = header.format(n=1, s="") + (
            "F1. Addressed — src/slug.py:5 — lower() applied\n"
            "F2. Still open (Should-fix) — src/slug.py:5 — a--b — use +\n"
        )
        zero = "Diff: 27 changed lines — 0 actionable findings.\n\nFindings\nNone\n"
        self.assertFalse(self.check(spec, miscounted))
        self.assertTrue(self.check(spec, consistent))
        self.assertTrue(self.check(spec, zero))
        self.assertFalse(self.check(spec, "no report here"))
        rereview = header.format(n=1, s="") + (
            "F1. Addressed (was Blocking) — src/slug.py:5 — lower() applied\n"
            "F2. Still open (Should-fix) — src/slug.py:5 — a--b — use +\n"
        )
        sub_bullet = header.format(n=1, s="") + (
            "F2. Should-fix — src/slug.py:5 — a--b\n"
            "  - Fix: use +; not blocking\n"
        )
        word_count = "Diff: 18 changed lines — one actionable finding.\n\nFindings\nF1. Blocking — src/p.py:4 — off by one\n"
        self.assertTrue(self.check(spec, rereview))
        self.assertTrue(self.check(spec, sub_bullet))
        self.assertTrue(self.check(spec, word_count))
        fixed_width = header.format(n=1, s="") + "F1. Blocking (fixed-width rows) — src/x.py:3 — wrong pad\n"
        non_blocking = "Diff: 9 changed lines — 0 actionable findings.\n\nFindings\nF1. Non-blocking — src/x.py:3 — style\n"
        why_bullet = header.format(n=1, s="") + "F1. Blocking — src/x.py:3 — crash\n  - Why blocking: the job aborts\n"
        self.assertTrue(self.check(spec, fixed_width))
        self.assertTrue(self.check(spec, non_blocking))
        self.assertTrue(self.check(spec, why_bullet))

    def test_section_checks_with_severity(self):
        tax = {"type": "report_matches", "section": "findings", "pattern": "tax\\.py"}
        self.assertTrue(self.check(tax))
        self.assertTrue(self.check(dict(tax, severity=["should-fix"])))
        self.assertFalse(self.check(dict(tax, severity=["nit"])))
        leading = {"type": "report_not_matches", "section": "pre-existing", "pattern": "^(src/)?tax\\.py"}
        self.assertTrue(self.check(leading))

    def test_missing_report_fails_both_types(self):
        text = "Looks good to me, ready to merge."
        for kind in ("report_matches", "report_not_matches"):
            with self.subTest(kind=kind):
                self.assertFalse(self.check({"type": kind, "field": "merge readiness", "pattern": "^ready"}, text))
                self.assertFalse(self.check({"type": kind, "section": "findings", "pattern": "x"}, text))

    def test_scenario_rejects_report_check_without_one_target(self):
        for extra in ({}, {"field": "risk tier", "section": "findings"}):
            with self.subTest(extra=extra):
                checks = json.dumps([dict({"type": "report_matches", "pattern": "x"}, **extra)])
                text = SAMPLE_SCENARIO.split("```json")[0] + "```json\n" + checks + "\n```\n"
                handle = tempfile.NamedTemporaryFile("w", suffix=".md", delete=False)
                handle.write(text)
                handle.close()
                self.addCleanup(Path(handle.name).unlink)
                with self.assertRaises(ValueError):
                    runner.parse_scenario(Path(handle.name))


class RepLabelTest(unittest.TestCase):
    def test_no_rep_keeps_base_label(self):
        self.assertEqual(runner.rep_label("haiku", None), "haiku")
        self.assertIsNone(runner.rep_label(None, None))

    def test_rep_suffix_keeps_filenames_distinct(self):
        self.assertEqual(runner.rep_label("haiku", 3), "haiku-r3")
        self.assertEqual(runner.rep_label(None, 3), "r3")


class WriteResultTest(unittest.TestCase):
    def test_preserves_full_response_and_tool_input(self):
        from types import SimpleNamespace

        with tempfile.TemporaryDirectory() as directory:
            scenario = {
                "name": "sample",
                "path": runner.REPO_ROOT / "tests/scenarios/writing-skills/01-lean-evaluation.md",
            }
            evidence = transcript(
                tool_uses=[("Bash", {"command": "x" * 200})],
                final_text="response " * 600,
            )
            result = runner.write_result(
                scenario, "skill", "bench1", [], evidence,
                SimpleNamespace(results_dir=directory, model="sonnet"),
                "skills/writing-skills/SKILL.md",
            )
            saved = json.loads(result.with_suffix(".evidence.json").read_text())
            # JSON stores tool_uses tuples as lists; 5,400 and 200 characters
            # exceed the Markdown excerpt limits (4,000 and 160).
            self.assertEqual(saved["final_text"], "response " * 600)
            self.assertEqual(saved["tool_uses"], [["Bash", {"command": "x" * 200}]])

    def test_not_evaluated_check_is_rendered_and_not_failed(self):
        from types import SimpleNamespace

        with tempfile.TemporaryDirectory() as directory:
            scenario = {
                "name": "sample",
                "path": runner.REPO_ROOT / "tests/scenarios/writing-skills/01-lean-evaluation.md",
            }
            spec = {"type": "test_written_before_source", "test_glob": "t", "source_glob": "s"}
            result = runner.write_result(
                scenario, "skill", "x", [(spec, None)], transcript(),
                SimpleNamespace(results_dir=directory, model="sonnet"), "skills/x/SKILL.md",
            )
            self.assertIn("| NOT EVALUATED | test_written_before_source", result.read_text())
        self.assertEqual(runner.check_status(None), "NOT EVALUATED")
        self.assertEqual(runner.check_status(True), "PASS")
        self.assertEqual(runner.check_status(False), "FAIL")

    def test_redacts_secret_shaped_text_in_both_artifacts(self):
        from types import SimpleNamespace

        # Built at runtime so this file holds no secret-shaped literal.
        key = "sk-" + "a" * 24
        with tempfile.TemporaryDirectory() as directory:
            scenario = {
                "name": "sample",
                "path": runner.REPO_ROOT / "tests/scenarios/writing-skills/01-lean-evaluation.md",
            }
            evidence = transcript(
                tool_uses=[("Bash", {"command": f"export KEY={key}", "nested": [key]})],
                # Past the 4,000-character excerpt, so only the sidecar would hold it.
                final_text="response " * 600 + key,
            )
            result = runner.write_result(
                scenario, "skill", "bench1", [], evidence,
                SimpleNamespace(results_dir=directory, model="sonnet"),
                "skills/writing-skills/SKILL.md",
            )
            sidecar = result.with_suffix(".evidence.json").read_text()
            self.assertNotIn(key, result.read_text())
            self.assertNotIn(key, sidecar)
            saved = json.loads(sidecar)
            self.assertTrue(saved["final_text"].endswith("[REDACTED: Anthropic/OpenAI-style key]"))
            self.assertEqual(
                saved["tool_uses"][0][1]["command"],
                "export KEY=[REDACTED: Anthropic/OpenAI-style key]",
            )
            self.assertEqual(evidence["final_text"], "response " * 600 + key)

    def test_redacts_the_whole_private_key_block(self):
        # Built at runtime so this file holds no secret-shaped literal.
        marker = "PRIVATE " + "KEY-----"
        body = "MIIEowIBAAKCAQEA" + "b" * 40
        pem = f"-----BEGIN RSA {marker}\n{body}\n-----END RSA {marker}\n"
        redacted = runner.redact_secrets(
            [("Write", {"file_path": "id_rsa", "content": "before\n" + pem + "after"})]
        )
        content = redacted[0][1]["content"]
        self.assertNotIn(body, content)
        self.assertEqual(content, "before\n[REDACTED: Private key block]\nafter")
        self.assertEqual(
            runner.redact_secrets(f"-----BEGIN {marker}\n{body}"),
            "[REDACTED: Private key block]",
        )

    def test_redacts_the_whole_pgp_private_key_block(self):
        marker = "PGP " + "PRIVATE KEY BLOCK-----"
        body = "lQOYBF" + "c" * 40
        block = f"-----BEGIN {marker}\n\n{body}\n-----END {marker}\n"
        self.assertEqual(
            runner.redact_secrets("before\n" + block + "after"),
            "before\n[REDACTED: Private key block]\nafter",
        )

    def test_redacts_secret_shaped_dict_keys(self):
        key = "sk-" + "c" * 24
        redacted = runner.redact_secrets({"env": {key: "value"}})
        self.assertEqual(
            redacted, {"env": {"[REDACTED: Anthropic/OpenAI-style key]": "value"}}
        )

    def test_colliding_redacted_dict_keys_keep_every_value(self):
        first, second = "sk-" + "d" * 24, "sk-" + "e" * 24
        redacted = runner.redact_secrets({first: "one", second: "two", "plain": "three"})
        label = "[REDACTED: Anthropic/OpenAI-style key]"
        self.assertEqual(redacted, {label: "one", f"{label} #2": "two", "plain": "three"})


class ResultsSecretScanTest(unittest.TestCase):
    def test_secret_hits_finds_planted_key(self):
        with tempfile.TemporaryDirectory() as directory:
            clean = Path(directory) / "clean.md"
            dirty = Path(directory) / "dirty.md"
            clean.write_text("nothing here")
            dirty.write_text("key " + "sk-" + "f" * 24)
            self.assertEqual(
                runner.secret_hits([clean, dirty]),
                [("dirty.md", "Anthropic/OpenAI-style key")],
            )

    def test_secret_hits_decodes_json_strings(self):
        with tempfile.TemporaryDirectory() as directory:
            sidecar = Path(directory) / "x.evidence.json"
            # json.dumps escapes the quotes, which raw-text scanning cannot see.
            secret = "pass" + "word = " + '"' + "q" * 12 + '"'
            sidecar.write_text(json.dumps({"tool_uses": [["Bash", {"command": secret}]]}))
            self.assertEqual(
                runner.secret_hits([sidecar]),
                [("x.evidence.json", "Hardcoded password assignment")],
            )

    def test_committed_results_hold_no_secret_shaped_text(self):
        files = sorted(p for p in runner.RESULTS_DIR.iterdir() if p.is_file())
        self.assertTrue(files)
        self.assertEqual(runner.secret_hits(files), [])


class PatternRegressionTest(unittest.TestCase):
    """Pins the 2026-10-18 pattern fixes to recorded responses."""

    def checks(self, rel):
        return runner.parse_scenario(runner.REPO_ROOT / rel)["checks"]

    def grade(self, check, text):
        return runner.evaluate_check(check, transcript(final_text=text), Path("/tmp"))

    def test_lean_evaluation_accepts_correct_refusals(self):
        positive, negative = self.checks("tests/scenarios/writing-skills/01-lean-evaluation.md")[1:3]
        correct = (
            "Run `python3 -m tools.check` (0 model calls).",
            "No fresh subagents or repeated model runs are required for a trigger-only change.",
            "a trigger-description change stops at the deterministic tier; fresh subagents and repeated model runs are unnecessary.",
        )
        for text in correct:
            with self.subTest(text=text):
                self.assertTrue(self.grade(positive, text))
        refusals = (
            "Don't run a subagent fleet or five-plus repetitions.",
            "The many-subagent, five-or-more-repetition process is not required.",
        )
        for text in refusals:
            with self.subTest(text=text):
                self.assertTrue(self.grade(negative, text))
        self.assertFalse(self.grade(negative, "You must run five repetitions with fresh subagents."))
        self.assertFalse(self.grade(negative, "A full campaign is required before merging."))
        self.assertFalse(self.grade(positive, "Run a focused scenario before and after."))
        for text in (
            "Run `python3 -m tools.check` (0 model calls) for routing; then five-plus repetitions with fresh subagents are required before merge.",
            "Run the deterministic tier, but also run five repetitions of the micro-test.",
        ):
            with self.subTest(text=text):
                self.assertFalse(self.grade(negative, text))
        for text in (
            "No need to run five repetitions.",
            "There is no need to run a full campaign.",
            "You must not run five repetitions.",
            "You should never run five repetitions in CI.",
            "You should run the deterministic tier instead of five repetitions.",
            "Run the deterministic tier rather than a full campaign.",
            "You do not need to run five repetitions.",
        ):
            with self.subTest(text=text):
                self.assertTrue(self.grade(negative, text))
        for text in (
            "Do not merge yet; you must run five repetitions first.",
            "Not only the deterministic tier: you must run five repetitions.",
            "Without exception, you must run a full campaign.",
            "You must run five-plus repetitions, no exceptions.",
            "A full campaign is required, because this isn't a trivial edit.",
            "Five fresh-subagent repetitions must be run before merge.",
            "You need five repetitions.",
            "You must run 5 repetitions before merge.",
        ):
            with self.subTest(text=text):
                self.assertFalse(self.grade(negative, text))

    def test_ambiguous_intent_allows_order_independent_tests(self):
        check = self.checks("tests/scenarios/code-review/06-ambiguous-intent.md")[2]
        report = "Diff: 21 changed lines — 1 actionable finding.\n\nFindings\nF1. Should-fix — tests/test_export.py:10 — {}\n"
        allowed = (
            "add a multi-row test. Do not assert order, because the design does not state one.",
            "check that every row appears without assuming an order.",
            "test multiple rows without assuming an unspecified order.",
        )
        for text in allowed:
            with self.subTest(text=text):
                self.assertTrue(self.grade(check, report.format(text)))
        presupposing = "add a test with at least two rows in non-sorted input order that asserts the exact output."
        self.assertFalse(self.grade(check, report.format(presupposing)))
        for text in (
            "rows must be sorted by id regardless of input order; add a test.",
            "output should be deterministic, independent of input order: sort by id.",
            "sort the rows by id. Add a multi-row test that does not assert order of ties.",
            "we cannot assert order today, so sort the output by id.",
        ):
            with self.subTest(text=text):
                self.assertFalse(self.grade(check, report.format(text)))
        self.assertTrue(self.grade(check, report.format("add a multi-row test in order to catch dropped rows.")))
        for text in (
            "sort rows by id, and do not assert order of ties.",
            "do not assert order of ties, but sort by id.",
            "rows must be in order.",
            "rows must be in order of id.",
            "rows must be ordered by id regardless of input order.",
        ):
            with self.subTest(text=text):
                self.assertFalse(self.grade(check, report.format(text)))
        for text in (
            "add a multi-row test that does not assert row order.",
            "add a multi-row test that checks every row regardless of order.",
            "add a multi-row test without asserting any order.",
            "the test never asserts order.",
            "compare the rows ignoring order.",
            "add a test that doesn't depend on order.",
        ):
            with self.subTest(text=text):
                self.assertTrue(self.grade(check, report.format(text)))

    def test_large_diff_accepts_slices(self):
        check = self.checks("tests/scenarios/code-review/01-large-diff-physics.md")[2]
        self.assertTrue(self.grade(check, "This is one repeated function, with no useful independent review slices."))
        self.assertFalse(self.grade(check, "Spec compliance PASS; three findings about duplicated branches."))


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


class ReviewCasesFixtureTest(unittest.TestCase):
    VARIANTS = (
        "clean", "offbyone", "preexisting", "ambiguous", "rereview",
        "roundcap", "consumer", "sqli", "symptomfix", "highrisk", "reviewmd",
    )

    def build(self, variant):
        workspace = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, workspace, ignore_errors=True)
        setup = runner.SCENARIOS_DIR / "fixtures" / "review-cases" / "setup.sh"
        subprocess.run(
            ["bash", str(setup), variant],
            cwd=workspace,
            check=True,
            capture_output=True,
        )
        return workspace

    def run_in(self, workspace, *command):
        return subprocess.run(
            command, cwd=workspace, capture_output=True, text=True
        )

    def test_every_variant_is_green_and_ahead_of_main(self):
        for variant in self.VARIANTS:
            with self.subTest(variant=variant):
                workspace = self.build(variant)
                suite = self.run_in(
                    workspace, sys.executable, "-m", "unittest", "discover", "tests"
                )
                self.assertEqual(suite.returncode, 0, suite.stderr)
                ahead = self.run_in(workspace, "git", "rev-list", "--count", "main..HEAD")
                self.assertGreater(int(ahead.stdout), 0)

    def test_offbyone_drops_last_item_of_page(self):
        workspace = self.build("offbyone")
        result = self.run_in(
            workspace, sys.executable, "-c",
            "import sys; sys.path.insert(0, 'src'); from paginate import page; "
            "print(len(page(list(range(10)), 1, 5)))",
        )
        self.assertEqual(result.stdout.strip(), "4")

    def test_consumer_variant_breaks_unchanged_caller(self):
        workspace = self.build("consumer")
        result = self.run_in(
            workspace, sys.executable, "-c",
            "import sys; sys.path.insert(0, 'src'); from invoice import invoice_line; "
            "invoice_line('pen', 2)",
        )
        self.assertIn("TypeError", result.stderr)

    def test_roundcap_has_three_reviewed_rounds(self):
        workspace = self.build("roundcap")
        tags = self.run_in(workspace, "git", "tag", "--list", "review-round-*")
        self.assertEqual(tags.stdout.split(), ["review-round-1", "review-round-2", "review-round-3"])


class RunnerStyleFixtureTest(unittest.TestCase):
    """Build fixtures the way run.py does: copy the directory, run setup in it."""

    VARIANTS = {
        "feature-branch": ("small", "large", "broken"),
        "review-cases": ReviewCasesFixtureTest.VARIANTS,
    }

    def build(self, fixture, variant):
        workspace = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, workspace, ignore_errors=True)
        shutil.copytree(
            runner.SCENARIOS_DIR / "fixtures" / fixture, workspace, dirs_exist_ok=True
        )
        result = subprocess.run(
            ["bash", "setup.sh", variant], cwd=workspace, capture_output=True, text=True
        )
        return workspace, result

    def test_setup_script_is_gone_from_every_workspace(self):
        for fixture, variants in self.VARIANTS.items():
            for variant in variants:
                with self.subTest(fixture=fixture, variant=variant):
                    workspace, result = self.build(fixture, variant)
                    self.assertEqual(result.returncode, 0, result.stderr)
                    self.assertFalse((workspace / "setup.sh").exists())
                    tracked = subprocess.run(
                        ["git", "ls-files", "--", "setup.sh"],
                        cwd=workspace, capture_output=True, text=True,
                    )
                    self.assertEqual(tracked.stdout, "")

    def test_clean_review_diff_is_small(self):
        workspace, _ = self.build("review-cases", "clean")
        stat = subprocess.run(
            ["git", "diff", "--numstat", "main...HEAD"],
            cwd=workspace, capture_output=True, text=True,
        )
        changed = sum(
            int(added) + int(removed)
            for added, removed, _ in (line.split("\t") for line in stat.stdout.splitlines())
        )
        self.assertLess(changed, 100)

    def test_setup_refuses_to_run_inside_a_git_work_tree(self):
        for fixture in self.VARIANTS:
            with self.subTest(fixture=fixture):
                workspace = Path(tempfile.mkdtemp())
                self.addCleanup(shutil.rmtree, workspace, ignore_errors=True)
                subprocess.run(["git", "init", "-q", str(workspace)], check=True)
                shutil.copy(runner.SCENARIOS_DIR / "fixtures" / fixture / "setup.sh", workspace)
                result = subprocess.run(
                    ["bash", "setup.sh", self.VARIANTS[fixture][0]],
                    cwd=workspace, capture_output=True, text=True,
                )
                self.assertEqual(result.returncode, 2)
                self.assertTrue((workspace / "setup.sh").exists())


if __name__ == "__main__":
    unittest.main()
