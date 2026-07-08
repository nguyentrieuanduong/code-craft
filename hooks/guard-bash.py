#!/usr/bin/env python3
"""PreToolUse gate on Bash: block hook-bypassing and history-destroying git.

If a pre-commit hook fails, the fix is the code, not --no-verify.
Exit 2 denies the command and feeds stderr back to the model.
"""
import json
import re
import sys

RULES = (
    (
        re.compile(r"\bgit\b[^|;&]*\b(commit|push)\b[^|;&]*--no-verify\b"),
        "git --no-verify bypasses quality hooks. Fix whatever the hook is "
        "failing on instead (systematic-debugging), or ask the user.",
    ),
    (
        re.compile(r"\bgit\b[^|;&]*\bpush\b[^|;&]*(--force\b|-f\b)[^|;&]*\b(main|master)\b"),
        "Force-pushing to main/master can destroy shared history. Ask the user "
        "explicitly before any force push.",
    ),
)


def main() -> None:
    payload = json.load(sys.stdin)
    command = payload.get("tool_input", {}).get("command", "")
    for pattern, reason in RULES:
        if pattern.search(command):
            print(f"BLOCKED: {reason}", file=sys.stderr)
            sys.exit(2)


if __name__ == "__main__":
    main()
