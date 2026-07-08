#!/usr/bin/env python3
"""PostToolUse audit: flag debug prints left in edited source files.

Advisory feedback (exit 2 on PostToolUse informs the model without undoing
the edit). Structured logging is required at boundaries; print/console.log
in production code violates coding-standards.
"""
import json
import re
import sys
from pathlib import Path

CHECKS = {
    ".py": re.compile(r"\bprint\("),
    ".js": re.compile(r"\bconsole\.(log|debug)\("),
    ".jsx": re.compile(r"\bconsole\.(log|debug)\("),
    ".ts": re.compile(r"\bconsole\.(log|debug)\("),
    ".tsx": re.compile(r"\bconsole\.(log|debug)\("),
}


def main() -> None:
    payload = json.load(sys.stdin)
    file_path = payload.get("tool_input", {}).get("file_path", "")
    path = Path(file_path)
    pattern = CHECKS.get(path.suffix)
    if not pattern or not path.exists():
        return
    lines = [
        str(number)
        for number, line in enumerate(path.read_text(encoding="utf-8", errors="ignore").splitlines(), 1)
        if pattern.search(line)
    ]
    if lines:
        print(
            f"WARNING: {path.name} contains print/console.log on line(s) "
            f"{', '.join(lines)}. Production code uses structured logging "
            "(coding-standards). If this file is a CLI entry point where stdout "
            "IS the interface, state that explicitly; otherwise replace with a "
            "logger call before completing.",
            file=sys.stderr,
        )
        sys.exit(2)


if __name__ == "__main__":
    main()
