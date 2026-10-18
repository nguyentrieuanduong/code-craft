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
import shlex
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any

SCENARIOS_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCENARIOS_DIR.parent.parent
sys.path.insert(0, str(REPO_ROOT))

from tools.frontmatter import parse_frontmatter  # noqa: E402


def _load_secret_patterns():
    # Reuse the write-time secret hook's patterns so committed results meet
    # the same bar as every file the agent writes (security-baseline SEC-02).
    import importlib.util

    hooks_dir = REPO_ROOT / "hooks"
    sys.path.insert(0, str(hooks_dir))
    try:
        spec = importlib.util.spec_from_file_location(
            "scan_secrets", hooks_dir / "scan-secrets.py"
        )
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
    finally:
        sys.path.remove(str(hooks_dir))
    return module.SECRET_PATTERNS


# The hook's private-key pattern matches only the header, which is enough to
# block a write but not to redact one: this span also removes the key body
# (through the END line, or to the end of an unterminated block).
REDACTION_PATTERNS = (
    ("Private key block", re.compile(
        r"(?s)-----BEGIN [A-Z ]*PRIVATE KEY(?: BLOCK)?-----"
        r".*?(?:-----END [A-Z ]*PRIVATE KEY(?: BLOCK)?-----|\Z)"
    )),
) + _load_secret_patterns()

RESULTS_DIR = SCENARIOS_DIR / "results"
NON_SCENARIO_DIRS = {"fixtures", "results", "__pycache__"}
ALLOWED_TOOLS = "Bash,Read,Write,Edit,Glob,Grep"
# CLI built-ins that fire even without --allowedTools membership. Blocking
# ExitPlanMode is what stops the harness from ending in plan mode with an
# empty `result` event; blocking EnterPlanMode stops plan mode from starting
# at all — 2026-07-14 baseline runs entered it unprompted and wrote plan
# drafts to ~/.claude/plans/ despite the ExitPlanMode block.
DISALLOWED_TOOLS = (
    "EnterPlanMode,ExitPlanMode,Agent,Task,WebFetch,WebSearch,NotebookEdit"
)
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
    "report_matches",
    "report_not_matches",
    "report_actionable_count",
}
REPORT_CHECK_TYPES = frozenset({"report_matches", "report_not_matches"})
REPORT_FIELDS = frozenset({
    "diff",
    "review independence",
    "risk tier",
    "verification evidence",
    "merge readiness",
    "spec compliance",
    "code quality",
    "security",
    "security pass",
})
REPORT_SECTIONS = frozenset({
    "verdicts", "findings", "pre-existing", "nits", "declined to judge",
})
SCENARIO_SCHEMA = {
    "name": str,
    "skill": str,
    "fixture": str,
    "setup": str,
    "max_turns": int,
}
SCENARIO_REQUIRED = frozenset({"name", "skill"})
DEFAULT_CALL_CEILING = 2


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


def parse_scenario(path: Path) -> dict[str, Any]:
    parsed = parse_frontmatter(
        path.read_text(),
        schema=SCENARIO_SCHEMA,
        required=SCENARIO_REQUIRED,
        context=str(path),
    )
    meta = parsed.metadata
    body = parsed.body
    checks_block = extract_section(body, "Checks")
    match = re.search(r"```json\n(.*?)```", checks_block, re.DOTALL)
    if not match:
        raise ValueError(f"{path}: Checks section needs a ```json block")
    checks = json.loads(match.group(1))
    for check in checks:
        if check.get("type") not in CHECK_TYPES:
            raise ValueError(f"{path}: unknown check type {check.get('type')}")
        if check["type"] in REPORT_CHECK_TYPES:
            _validate_report_check(check, path)
    return {
        "path": path,
        "name": meta["name"],
        "skill": meta["skill"],
        "fixture": meta.get("fixture"),
        "setup": meta.get("setup"),
        "max_turns": meta.get("max_turns", 30),
        "prompt": extract_section(body, "Prompt"),
        "checks": checks,
    }


def _validate_report_check(check, path):
    if ("field" in check) == ("section" in check):
        raise ValueError(f"{path}: report check needs exactly one of field/section")
    if not isinstance(check.get("pattern"), str):
        raise ValueError(f"{path}: report check needs a pattern")
    if "severity" in check and "section" not in check:
        raise ValueError(f"{path}: severity applies only to section checks")


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


_DECORATION = re.compile(r"\*\*|__|`")
_LEAD_MARKERS = re.compile(r"^\s*(?:(?:#+|>+|[-*+])\s+)*")
_ITEM_START = re.compile(r"^(?:[-*+]\s+|\d+[.)]\s+|[a-z]{1,3}\d+(?:-\d+)?[.):]\s+)")
_LABEL = re.compile(r"^([a-z][a-z -]*?)\s*:\s*(.*)$")
_SEVERITY = re.compile(r"(?<![\w-])(blocking|should[- ]fix|nit)\b")
_NUMBER_WORDS = {
    word: number for number, word in enumerate(
        ("one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten"), start=1
    )
}
_NONE_ITEM = re.compile(r"^none\b")


def _report_item(text):
    severity = _SEVERITY.search(text)
    return {
        "text": text,
        "severity": severity.group(1).replace(" ", "-") if severity else None,
    }


def _add_item(items, text, new):
    if new or not items:
        items.append(text)
    else:
        items[-1] += " " + text


def parse_report(text):
    """Read the code-review report template out of free-form final text.

    Returns {"fields": {label: value}, "sections": {name: [item, ...]}}, all
    lowercased, with derived fields "changed lines" and "actionable".
    """
    fields = {}
    raw_sections = {}
    current = None
    previous_blank = True
    for raw in text.splitlines():
        line = _DECORATION.sub("", raw).strip().lower()
        if not line:
            previous_blank = True
            continue
        body = _LEAD_MARKERS.sub("", line)
        label = _LABEL.match(body)
        header = body.rstrip(":").strip()
        if header in REPORT_SECTIONS or (label and label.group(1) in REPORT_SECTIONS):
            current = header if header in REPORT_SECTIONS else label.group(1)
            raw_sections.setdefault(current, [])
            inline = label.group(2).strip() if label and current == label.group(1) else ""
            if inline:
                raw_sections[current].append(inline)
            previous_blank = True
            continue
        if label and label.group(1) in REPORT_FIELDS:
            fields.setdefault(label.group(1), label.group(2).strip())
            if current != "verdicts":
                current = None
            previous_blank = False
            continue
        heading = line.startswith("#")
        if heading and not (current and _ITEM_START.match(body)):
            current = None
        elif current:
            starts_item = heading or bool(_ITEM_START.match(line))
            # Strip a bullet, then an ID such as "F1." that may follow it.
            item = _ITEM_START.sub("", _ITEM_START.sub("", body if heading else line))
            _add_item(raw_sections[current], item, starts_item or previous_blank)
        previous_blank = False
    diff = fields.get("diff", "")
    changed = re.search(r"([\d,]+)\s+changed lines", diff)
    if changed:
        fields["changed lines"] = changed.group(1).replace(",", "")
    actionable = re.search(r"\b(\d+|no|zero|none|" + "|".join(_NUMBER_WORDS) + r")\s+actionable", diff)
    if actionable:
        count = actionable.group(1)
        fields["actionable"] = count if count.isdigit() else str(_NUMBER_WORDS.get(count, 0))
    sections = {
        name: [_report_item(item) for item in items if not _NONE_ITEM.match(item)]
        for name, items in raw_sections.items()
    }
    return {"fields": fields, "sections": sections}


def _report_check(check, text):
    report = parse_report(text)
    if "diff" not in report["fields"] and "findings" not in report["sections"]:
        return False
    negate = check["type"] == "report_not_matches"
    if "field" in check:
        value = report["fields"].get(check["field"])
        if value is None:
            return False
        return bool(re.search(check["pattern"], value, re.IGNORECASE)) != negate
    items = report["sections"].get(check["section"], [])
    severities = check.get("severity")
    if severities:
        items = [item for item in items if item["severity"] in severities]
    found = any(re.search(check["pattern"], item["text"], re.IGNORECASE) for item in items)
    return found != negate


def _commands(transcript):
    return [
        tool_input.get("command", "")
        for name, tool_input in transcript["tool_uses"]
        if name == "Bash"
    ]


_HEREDOC = re.compile(
    r"<<-?\s*(['\"]?)(\w+)\1([^\n]*)\n(.*?)^\s*\2\s*$", re.DOTALL | re.MULTILINE
)
_SEPARATORS = frozenset({";", "&&", "||", "|", "|&", "&", "(", ")"})
_REDIRECTS = frozenset({">", ">>", "&>", "&>>", ">|"})
_SKIP_NEXT = frozenset({">&", "<", "<<", "<<<", "<&", "<>"})
_WRAPPERS = frozenset({"sudo", "env", "command", "exec", "time", "nohup"})
_PYTHON = re.compile(r"^python[\d.]*$")
_ASSIGN = re.compile(r"\b(\w+)\s*=\s*(?:Path\(\s*)?['\"]([^'\"\n]+)['\"]")
_KWARG = re.compile(r"^(\w+)\s*=\s*(.*)$", re.DOTALL)
_WRITE_TEXT = re.compile(r"(?:Path\(\s*([^()\n]+?)\s*\)|\b(\w+))\.write_(?:text|bytes)\(")
_PATH_TOKEN = re.compile(r"[\w./-]+")


def _literal(expr, assigns):
    expr = expr.strip()
    quoted = re.fullmatch(r"['\"]([^'\"]+)['\"]", expr)
    if quoted:
        return quoted.group(1)
    return assigns.get(expr)


def _call_args(code, start):
    """Top-level arguments of the call whose '(' ends at code[start - 1]."""
    args, current, depth, quote = [], [], 1, None
    for char in code[start:]:
        if quote:
            current.append(char)
            quote = None if char == quote else quote
            continue
        if char in "'\"":
            quote = char
        elif char in "([{":
            depth += 1
        elif char in ")]}":
            depth -= 1
            if depth == 0:
                args.append("".join(current).strip())
                return [arg for arg in args if arg]
        elif char == "," and depth == 1:
            args.append("".join(current).strip())
            current = []
            continue
        current.append(char)
    return None


def _python_writes(code):
    """Paths Python code writes, and whether it writes a path it does not name."""
    assigns = dict(_ASSIGN.findall(code))
    paths, opaque = set(), False
    for match in re.finditer(r"\bopen\(", code):
        args = _call_args(code, match.end())
        if not args:
            continue
        keywords = dict(m.groups() for m in map(_KWARG.match, args) if m)
        positional = [arg for arg in args if not _KWARG.match(arg)]
        mode = keywords.get("mode") or (positional[1] if len(positional) > 1 else "'r'")
        mode_value = _literal(mode, {})
        if mode_value is None or set(mode_value) & set("wax+"):
            target = keywords.get("file") or (positional[0] if positional else "")
            value = _literal(target, assigns)
            if value is None:
                opaque = True
            else:
                paths.add(value)
    for named, variable in _WRITE_TEXT.findall(code):
        value = _literal(named or variable, assigns)
        if value is None:
            opaque = True
        else:
            paths.add(value)
    return paths, opaque


def _options_and_files(args, valued=("-e", "-f", "--expression", "--file")):
    """Split command arguments into option tokens and positional words."""
    options, positional, skip = [], [], False
    for arg in args:
        if skip:
            skip = False
        elif arg in valued:
            options.append(arg)
            skip = True
        elif arg.startswith("-") and arg != "-":
            options.append(arg)
        else:
            positional.append(arg)
    return options, positional


def _in_place(options):
    return any(
        option.startswith("--in-place") or (not option.startswith("--") and "i" in option[1:])
        for option in options
    )


def _segment_writes(tokens):
    """(write targets, Python code run) for one shell segment's tokens."""
    targets, words, index = [], [], 0
    while index < len(tokens):
        token = tokens[index]
        if token in _REDIRECTS and index + 1 < len(tokens):
            targets.append(tokens[index + 1])
            index += 2
        elif token in _SKIP_NEXT:
            index += 2
        else:
            words.append(token)
            index += 1
    while words and (re.match(r"^\w+=", words[0]) or words[0] in _WRAPPERS):
        words.pop(0)
    if not words:
        return targets, []
    name, args = Path(words[0]).name, words[1:]
    options, files = _options_and_files(args)
    code = []
    if name == "tee":
        targets += files
    elif name in ("cp", "mv", "install", "ln") and files:
        targets.append(files[-1])
    elif name in ("touch", "truncate"):
        targets += files
    elif name == "dd":
        targets += [arg[3:] for arg in args if arg.startswith("of=")]
    elif name == "sed" and _in_place(options):
        has_script = any(option in ("-e", "-f", "--expression", "--file") for option in options)
        targets += files if has_script else files[1:]
    elif name == "perl" and _in_place(options):
        targets += files
    elif _PYTHON.match(name) and "-c" in args:
        position = args.index("-c")
        if position + 1 < len(args):
            code.append(args[position + 1])
    return targets, code


def _bash_writes(command):
    """Paths a Bash command writes, and the texts holding a write it does not name.

    Only the shell part is parsed (heredoc bodies are file content, except a
    body fed to python, which is code). Unrecognised writers — patch,
    git apply, rsync, shutil — are not seen.
    """
    codes = []

    def strip_body(match):
        line_start = command.rfind("\n", 0, match.start()) + 1
        header = command[line_start:match.start()]
        if re.search(r"(?:^|[\s;&|(])python[\d.]*(?:\s|$)", header):
            codes.append(match.group(4))
        return match.group(3)

    shell = _HEREDOC.sub(strip_body, command)
    try:
        lexer = shlex.shlex(shell.replace("\n", " ; "), posix=True, punctuation_chars=True)
        lexer.whitespace_split = True
        tokens = list(lexer)
    except ValueError:
        return set(), [command]
    paths, opaque_texts, segment = set(), [], []
    for token in tokens + [";"]:
        if token not in _SEPARATORS:
            segment.append(token)
            continue
        targets, code = _segment_writes(segment)
        codes += code
        segment = []
        for target in targets:
            if target == "/dev/null" or target.startswith("&"):
                continue
            if "$" in target or "`" in target:
                opaque_texts.append(shell)
            else:
                paths.add(target)
    for code in codes:
        written, opaque = _python_writes(code)
        paths |= written
        if opaque:
            opaque_texts.append(code)
    return paths, opaque_texts


def _mentions(text, pattern, workspace):
    return any(
        _tool_path_matches({"file_path": token}, pattern, workspace)
        for token in _PATH_TOKEN.findall(text)
    )


def _first_write(transcript, pattern, workspace):
    """(index of the first write to a matching file, whether that write is unattributable)."""
    for index, (name, tool_input) in enumerate(transcript["tool_uses"]):
        if name in ("Write", "Edit") and _tool_path_matches(tool_input, pattern, workspace):
            return index, False
        if name != "Bash":
            continue
        paths, opaque_texts = _bash_writes(tool_input.get("command", ""))
        if any(_tool_path_matches({"file_path": p}, pattern, workspace) for p in paths):
            return index, False
        if any(_mentions(text, pattern, workspace) for text in opaque_texts):
            return index, True
    return None, False


_LEAD_SEVERITY = re.compile(r"^\W*(?:[\w-]+\W+){0,2}?(blocking|should[- ]fix)\b")
_DONE = re.compile(r"\b(addressed|resolved|fixed)\b")


def _open_actionable(text):
    """Whether a Findings item opens with Blocking or Should-fix and is not marked done."""
    lead = re.split(r"\s+[—–]\s+", text, maxsplit=1)[0]
    if _DONE.search(lead) and "still open" not in lead:
        return False
    match = _LEAD_SEVERITY.match(lead)
    return bool(match) and not re.search(r"\bnot\s+$", lead[:match.start(1)])


def check_status(passed):
    if passed is None:
        return "NOT EVALUATED"
    return "PASS" if passed else "FAIL"


def evaluate_check(check, transcript, workspace):
    kind = check["type"]
    pattern = check.get("pattern", "")
    glob = check.get("glob", "")
    text = transcript["final_text"]
    if kind == "output_matches":
        return re.search(pattern, text) is not None
    if kind in REPORT_CHECK_TYPES:
        return _report_check(check, text)
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
        # None = NOT EVALUATED: a Bash write names a matching file but its
        # target cannot be read from the command, or one command writes both.
        test_index, test_opaque = _first_write(transcript, check["test_glob"], workspace)
        source_index, source_opaque = _first_write(transcript, check["source_glob"], workspace)
        written = [i for i in (test_index, source_index) if i is not None]
        if not written:
            return False
        first = min(written)
        if test_index == source_index or (first == test_index and test_opaque) or (
            first == source_index and source_opaque
        ):
            return None
        if test_index is None:
            return False
        return source_index is None or test_index < source_index
    if kind == "files_untouched":
        return all(
            not _tool_path_matches(tool_input, glob, workspace)
            for name, tool_input in transcript["tool_uses"]
            if name in ("Write", "Edit")
        )
    if kind == "report_actionable_count":
        report = parse_report(text)
        count = report["fields"].get("actionable")
        if count is None:
            return False
        listed = [
            item for item in report["sections"].get("findings", [])
            if _open_actionable(item["text"])
        ]
        return int(count) == len(listed)
    raise ValueError(f"unknown check type: {kind}")


def describe_check(check):
    parts = [check["type"]]
    for key in ("field", "section", "severity", "pattern", "glob", "test_glob", "source_glob"):
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

def redact_secrets(value):
    """Return a copy of a transcript value with secret-shaped strings masked."""
    if isinstance(value, str):
        for label, pattern in REDACTION_PATTERNS:
            value = pattern.sub(f"[REDACTED: {label}]", value)
        return value
    if isinstance(value, dict):
        # Two secret keys can redact to the same label; number the repeats so
        # no value is dropped.
        redacted = {}
        for key, item in value.items():
            base = new_key = redact_secrets(key)
            count = 2
            while new_key in redacted:
                new_key = f"{base} #{count}"
                count += 1
            redacted[new_key] = redact_secrets(item)
        return redacted
    if isinstance(value, (list, tuple)):
        return [redact_secrets(item) for item in value]
    return value


def _strings(value):
    if isinstance(value, str):
        yield value
    elif isinstance(value, dict):
        for key, item in value.items():
            yield from _strings(key)
            yield from _strings(item)
    elif isinstance(value, (list, tuple)):
        for item in value:
            yield from _strings(item)


def secret_hits(paths):
    """(file name, pattern label) for every secret-shaped match in the files.

    JSON files are decoded first: json.dumps escapes quotes, which would hide
    a quoted password from the raw text.
    """
    hits = []
    for path in paths:
        text = path.read_text(errors="replace")
        texts = [text]
        if path.suffix == ".json":
            try:
                texts += list(_strings(json.loads(text)))
            except json.JSONDecodeError:
                pass
        hits += [
            (path.name, label)
            for label, pattern in REDACTION_PATTERNS
            if any(pattern.search(chunk) for chunk in texts)
        ]
    return hits


def write_result(scenario, arm, label, results, transcript, args, skill_file):
    # Results are committed: mask secrets before either artifact is written.
    transcript = redact_secrets(transcript)
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
            f"| {check_status(passed)} | {describe_check(check)} |"
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
    out.with_suffix(".evidence.json").write_text(
        json.dumps(transcript, indent=2) + "\n"
    )
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
        failed = [c for c, passed in results if passed is False]
        unscored = [c for c, passed in results if passed is None]
        status = "PASS" if not failed else f"{len(failed)} check(s) failed"
        if unscored:
            status += f" ({len(unscored)} not evaluated)"
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
    parser.add_argument("paths", nargs="*", help="scenario files")
    parser.add_argument("--all", action="store_true")
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
        "--allow-many",
        type=int,
        metavar="N",
        default=None,
        help="explicit model-call budget for runs requiring more than 2 calls",
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

    if args.paths and args.all:
        parser.error("choose scenario paths or --all, not both")
    if not args.dry_run and not args.paths and not args.all:
        parser.error("model runs require scenario paths or explicit --all")
    if args.reps < 1:
        parser.error("--reps must be >= 1")

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
    arm_count = 2 if args.arm == "both" else 1
    planned_calls = len(scenarios) * arm_count * args.reps
    if args.allow_many is not None and args.allow_many < 1:
        parser.error("--allow-many N requires N >= 1")
    call_budget = (
        args.allow_many
        if args.allow_many is not None
        else DEFAULT_CALL_CEILING
    )
    if not args.dry_run and planned_calls > call_budget:
        parser.error(
            f"planned model calls: {planned_calls}; budget: {call_budget}; "
            f"pass --allow-many {planned_calls} to authorize exactly this batch"
        )
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
