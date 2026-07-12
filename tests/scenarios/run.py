#!/usr/bin/env python3
"""Headless eval runner for skill pressure-test scenarios.

Runs each scenario's prompt through `claude -p` in a disposable workspace —
with the skill under test injected (arm "skill") or without it (arm
"baseline") — then evaluates the declared checks against the transcript and
the resulting file state, and writes a result file to results/.

Baseline runs never fail the process: their check violations are the RED
evidence writing-skills requires. Skill runs must pass every check.

See README.md in this directory for the scenario format and eval workflow.
"""
import argparse
import datetime
import fnmatch
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

SCENARIOS_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCENARIOS_DIR.parent.parent
RESULTS_DIR = SCENARIOS_DIR / "results"
NON_SCENARIO_DIRS = {"fixtures", "results", "__pycache__"}
ALLOWED_TOOLS = "Bash,Read,Write,Edit,Glob,Grep"
# CLI built-ins that fire even without --allowedTools membership. Blocking
# ExitPlanMode is what stops the harness from ending in plan mode with an
# empty `result` event and writing the plan draft to ~/.claude/plans/.
DISALLOWED_TOOLS = "ExitPlanMode,Agent,Task,WebFetch,WebSearch,NotebookEdit"
SKILL_PREAMBLE = (
    "You must follow this skill exactly; it overrides your defaults:\n\n"
)
CHECK_TYPES = {
    "output_matches",
    "output_not_matches",
    "file_exists",
    "file_not_exists",
    "file_matches",
    "file_not_matches",
    "anywhere_matches",
    "ran_command",
    "not_ran_command",
    "test_written_before_source",
    "files_untouched",
}


# ---------------------------------------------------------------- scenarios

def find_scenarios(paths=None):
    if paths:
        return [Path(p).resolve() for p in paths]
    found = []
    for entry in sorted(SCENARIOS_DIR.iterdir()):
        if entry.is_dir() and entry.name not in NON_SCENARIO_DIRS:
            found.extend(sorted(entry.glob("*.md")))
    return found


def extract_section(body, name):
    match = re.search(
        rf"^## {name}\n(.*?)(?=^## |\Z)", body, re.DOTALL | re.MULTILINE
    )
    if not match:
        raise ValueError(f"missing section '## {name}'")
    return match.group(1).strip()


def parse_scenario(path):
    text = path.read_text()
    if not text.startswith("---"):
        raise ValueError(f"{path}: missing frontmatter")
    _, frontmatter, body = text.split("---", 2)
    meta = {}
    for line in frontmatter.strip().splitlines():
        key, _, value = line.partition(":")
        if key.strip():
            meta[key.strip()] = value.strip()
    for required in ("name", "skill"):
        if not meta.get(required):
            raise ValueError(f"{path}: frontmatter needs '{required}'")
    checks_block = extract_section(body, "Checks")
    match = re.search(r"```json\n(.*?)```", checks_block, re.DOTALL)
    if not match:
        raise ValueError(f"{path}: Checks section needs a ```json block")
    checks = json.loads(match.group(1))
    for check in checks:
        if check.get("type") not in CHECK_TYPES:
            raise ValueError(f"{path}: unknown check type {check.get('type')}")
    return {
        "path": path,
        "name": meta["name"],
        "skill": meta["skill"],
        "fixture": meta.get("fixture"),
        "setup": meta.get("setup"),
        "max_turns": int(meta.get("max_turns", 30)),
        "prompt": extract_section(body, "Prompt"),
        "checks": checks,
    }


# --------------------------------------------------------------- transcript

def parse_transcript(stdout):
    tool_uses = []
    final_text = ""
    last_assistant_text = ""
    for line in stdout.splitlines():
        line = line.strip()
        if not line.startswith("{"):
            continue
        try:
            event = json.loads(line)
        except json.JSONDecodeError:
            continue
        if event.get("type") == "assistant":
            for block in event.get("message", {}).get("content", []):
                if block.get("type") == "tool_use":
                    tool_uses.append(
                        (block.get("name", ""), block.get("input", {}))
                    )
                elif block.get("type") == "text" and block.get("text"):
                    last_assistant_text = block["text"]
        elif event.get("type") == "result":
            final_text = event.get("result") or ""
    # Fall back to the last assistant text when the run ends without a
    # `result` event (e.g. hit --max-turns, or the CLI errored after
    # producing content). Checks then still see something to grade.
    if not final_text:
        final_text = last_assistant_text
    return {"tool_uses": tool_uses, "final_text": final_text}


RATE_LIMIT_MARKER = re.compile(
    r"you'?ve hit your limit|rate.?limit|429", re.IGNORECASE
)


def looks_rate_limited(final_text, stderr):
    return bool(
        RATE_LIMIT_MARKER.search(final_text or "")
        or RATE_LIMIT_MARKER.search(stderr or "")
    )


# ------------------------------------------------------------------- checks

def _tool_path_matches(tool_input, pattern, workspace):
    file_path = tool_input.get("file_path", "")
    if not file_path:
        return False
    try:
        rel = Path(file_path).resolve().relative_to(
            Path(workspace).resolve()
        ).as_posix()
    except ValueError:
        rel = file_path
    return fnmatch.fnmatch(rel, pattern) or fnmatch.fnmatch(
        Path(file_path).name, pattern
    )


def _glob_files(workspace, pattern):
    return [
        p
        for p in Path(workspace).glob(pattern)
        if p.is_file() and ".git" not in p.parts
    ]


def _commands(transcript):
    return [
        tool_input.get("command", "")
        for name, tool_input in transcript["tool_uses"]
        if name == "Bash"
    ]


def _write_index(transcript, pattern, workspace):
    for index, (name, tool_input) in enumerate(transcript["tool_uses"]):
        if name in ("Write", "Edit") and _tool_path_matches(
            tool_input, pattern, workspace
        ):
            return index
    return None


def evaluate_check(check, transcript, workspace):
    kind = check["type"]
    pattern = check.get("pattern", "")
    glob = check.get("glob", "")
    text = transcript["final_text"]
    if kind == "output_matches":
        return re.search(pattern, text) is not None
    if kind == "output_not_matches":
        return re.search(pattern, text) is None
    if kind == "file_exists":
        return bool(_glob_files(workspace, glob))
    if kind == "file_not_exists":
        return not _glob_files(workspace, glob)
    if kind == "file_matches":
        return any(
            re.search(pattern, p.read_text(errors="replace"))
            for p in _glob_files(workspace, glob)
        )
    if kind == "file_not_matches":
        return not any(
            re.search(pattern, p.read_text(errors="replace"))
            for p in _glob_files(workspace, glob)
        )
    if kind == "anywhere_matches":
        if re.search(pattern, text):
            return True
        return any(
            re.search(pattern, p.read_text(errors="replace"))
            for p in _glob_files(workspace, glob)
        )
    if kind == "ran_command":
        return any(re.search(pattern, c) for c in _commands(transcript))
    if kind == "not_ran_command":
        return not any(re.search(pattern, c) for c in _commands(transcript))
    if kind == "test_written_before_source":
        test_index = _write_index(transcript, check["test_glob"], workspace)
        source_index = _write_index(
            transcript, check["source_glob"], workspace
        )
        if test_index is None:
            return False
        return source_index is None or test_index < source_index
    if kind == "files_untouched":
        return all(
            not _tool_path_matches(tool_input, glob, workspace)
            for name, tool_input in transcript["tool_uses"]
            if name in ("Write", "Edit")
        )
    raise ValueError(f"unknown check type: {kind}")


def describe_check(check):
    parts = [check["type"]]
    for key in ("pattern", "glob", "test_glob", "source_glob"):
        if key in check:
            parts.append(f"{key}={check[key]!r}")
    return " ".join(parts)


# -------------------------------------------------------------------- claude

def run_claude(scenario, workspace, skill_text, args):
    cmd = [
        args.claude_bin,
        "-p",
        scenario["prompt"],
        "--output-format",
        "stream-json",
        "--verbose",
        "--max-turns",
        str(args.max_turns or scenario["max_turns"]),
        "--allowedTools",
        ALLOWED_TOOLS,
        "--disallowedTools",
        DISALLOWED_TOOLS,
        "--permission-mode",
        "acceptEdits",
    ]
    if skill_text:
        cmd += ["--append-system-prompt", SKILL_PREAMBLE + skill_text]
    if args.model:
        cmd += ["--model", args.model]
    env = os.environ.copy()
    if args.isolate:
        config_dir = Path(workspace) / ".claude-isolated-config"
        config_dir.mkdir(exist_ok=True)
        env["CLAUDE_CONFIG_DIR"] = str(config_dir)
    return subprocess.run(
        cmd,
        cwd=workspace,
        capture_output=True,
        text=True,
        timeout=args.timeout,
        env=env,
    )


# ------------------------------------------------------------------- results

def write_result(scenario, arm, label, results, transcript, args, skill_file):
    results_dir = Path(args.results_dir) if args.results_dir else RESULTS_DIR
    results_dir.mkdir(parents=True, exist_ok=True)
    date = datetime.date.today().isoformat()
    suffix = f"-{label}" if label else ""
    out = results_dir / f"{date}-{scenario['name']}-{arm}{suffix}.md"
    lines = [
        f"# {scenario['name']} — {arm}{suffix}",
        "",
        f"- Date: {date}",
        f"- Model: {args.model or 'CLI default'}",
        f"- Skill file: {skill_file if arm == 'skill' else 'none (baseline)'}",
        f"- Scenario: {scenario['path'].relative_to(REPO_ROOT)}",
        "",
        "## Checks",
        "",
        "| Result | Check |",
        "|---|---|",
    ]
    for check, passed in results:
        lines.append(
            f"| {'PASS' if passed else 'FAIL'} | {describe_check(check)} |"
        )
    lines += ["", "## Tool calls", ""]
    for name, tool_input in transcript["tool_uses"]:
        detail = tool_input.get("command") or tool_input.get("file_path") or ""
        lines.append(f"- {name}: `{str(detail)[:160]}`")
    lines += [
        "",
        "## Final response (truncated)",
        "",
        "```",
        transcript["final_text"][:4000],
        "```",
        "",
        "## Rationalizations observed (manual notes)",
        "",
        "_Read the transcript and record rationalizations verbatim here._",
        "",
    ]
    out.write_text("\n".join(lines))
    return out


# ---------------------------------------------------------------------- main

def rep_label(base, rep):
    if rep is None:
        return base
    return f"{base}-r{rep}" if base else f"r{rep}"


def run_arm(scenario, arm, args, rep=None):
    workspace = Path(tempfile.mkdtemp(prefix=f"eval-{scenario['name']}-"))
    try:
        if scenario["fixture"]:
            shutil.copytree(
                SCENARIOS_DIR / "fixtures" / scenario["fixture"],
                workspace,
                dirs_exist_ok=True,
            )
        if scenario["setup"]:
            subprocess.run(
                scenario["setup"],
                shell=True,
                cwd=workspace,
                check=True,
                capture_output=True,
                text=True,
            )
        skill_file = args.skill_override or scenario["skill"]
        skill_text = None
        if arm == "skill":
            skill_text = (REPO_ROOT / skill_file).read_text()
        try:
            proc = run_claude(scenario, workspace, skill_text, args)
        except subprocess.TimeoutExpired:
            print(f"  [{arm}] TIMEOUT after {args.timeout}s — counted as failed")
            proc = None
        transcript = parse_transcript(proc.stdout if proc else "")
        if proc and looks_rate_limited(
            transcript["final_text"], proc.stderr
        ):
            print(
                f"  [{arm}] RATE-LIMITED — aborting the rest of this batch. "
                f"Re-run after the quota resets."
            )
            return "rate_limited"
        if proc and proc.returncode != 0 and not transcript["tool_uses"]:
            print(f"  claude exited {proc.returncode}: {proc.stderr[:500]}")
        results = [
            (check, evaluate_check(check, transcript, workspace))
            for check in scenario["checks"]
        ]
        out = write_result(
            scenario,
            arm,
            rep_label(args.label, rep),
            results,
            transcript,
            args,
            skill_file,
        )
        failed = [c for c, passed in results if not passed]
        status = "PASS" if not failed else f"{len(failed)} check(s) failed"
        try:
            shown = out.relative_to(REPO_ROOT)
        except ValueError:
            shown = out
        print(f"  [{arm}] {status} -> {shown}")
        if arm == "baseline" and failed:
            print(
                f"  [baseline] RED evidence: violated {len(failed)}/"
                f"{len(results)} target checks"
            )
        return not failed
    finally:
        if args.keep_workspace:
            print(f"  workspace kept: {workspace}")
        else:
            shutil.rmtree(workspace, ignore_errors=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("paths", nargs="*", help="scenario files (default: all)")
    parser.add_argument(
        "--arm",
        choices=("skill", "baseline", "both"),
        default="skill",
        help="run with skill injected, without, or both (default: skill)",
    )
    parser.add_argument(
        "--skill-override",
        help="repo-relative path to an edited skill file (A/B wording evals)",
    )
    parser.add_argument(
        "--label", help="suffix for result filenames, e.g. 'r3-edit'"
    )
    parser.add_argument("--model", help="model for the agent under test")
    parser.add_argument(
        "--reps",
        type=int,
        default=1,
        help="repetitions per arm; result files get -rN suffixes",
    )
    parser.add_argument(
        "--results-dir",
        help="write result files here instead of results/ (raw campaign runs)",
    )
    parser.add_argument("--claude-bin", default="claude")
    parser.add_argument("--max-turns", type=int, default=None)
    parser.add_argument("--timeout", type=int, default=600)
    parser.add_argument(
        "--isolate",
        action="store_true",
        help="point CLAUDE_CONFIG_DIR at a scratch dir (needs ANTHROPIC_API_KEY)",
    )
    parser.add_argument("--keep-workspace", action="store_true")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="parse and validate scenarios without calling claude",
    )
    args = parser.parse_args()

    scenarios = []
    for path in find_scenarios(args.paths):
        try:
            scenarios.append(parse_scenario(path))
        except (ValueError, json.JSONDecodeError) as error:
            print(f"INVALID {path}: {error}")
            return 1
    if not scenarios:
        print("no scenarios found")
        return 1
    if args.dry_run:
        for scenario in scenarios:
            print(
                f"OK {scenario['path'].relative_to(REPO_ROOT)} "
                f"({len(scenario['checks'])} checks, "
                f"fixture={scenario['fixture'] or 'none'})"
            )
        return 0

    arms = ("baseline", "skill") if args.arm == "both" else (args.arm,)
    any_failed = False
    rate_limited = False
    tally = []
    for scenario in scenarios:
        if rate_limited:
            break
        print(f"{scenario['name']}:")
        for arm in arms:
            if rate_limited:
                break
            passes = 0
            reps_run = 0
            for rep in range(1, args.reps + 1):
                outcome = run_arm(
                    scenario, arm, args, rep if args.reps > 1 else None
                )
                if outcome == "rate_limited":
                    rate_limited = True
                    break
                reps_run += 1
                passes += int(outcome)
                any_failed |= arm == "skill" and not outcome
            tally.append((scenario["name"], arm, passes, reps_run))
    if args.reps > 1:
        print(f"\nSUMMARY (passing reps out of {args.reps}):")
        for name, arm, passes, reps_run in tally:
            note = f" ({reps_run} ran)" if reps_run < args.reps else ""
            print(f"  {name} [{arm}] {passes}/{args.reps}{note}")
    if rate_limited:
        print("\nStopped early: rate limit reached.")
    return 1 if any_failed else 0


if __name__ == "__main__":
    sys.exit(main())
