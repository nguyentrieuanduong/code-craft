#!/usr/bin/env python3
"""PreToolUse gate: block writes containing secret-shaped strings.

Committed secrets live in git history forever (security-baseline SEC-02), so
they are stopped at write time, not review time. Exit 2 denies the tool call.
"""
import json
import re
import sys

SECRET_PATTERNS = (
    ("Anthropic/OpenAI-style key", re.compile(r"\bsk-[A-Za-z0-9_-]{20,}")),
    ("GitHub token", re.compile(r"\bgh[pousr]_[A-Za-z0-9]{36,}")),
    ("AWS access key", re.compile(r"\bAKIA[0-9A-Z]{16}\b")),
    ("Google API key", re.compile(r"\bAIza[0-9A-Za-z_-]{35}\b")),
    ("Slack token", re.compile(r"\bxox[baprs]-[A-Za-z0-9-]{10,}")),
    ("Private key block", re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----")),
    ("Hardcoded password assignment", re.compile(r"(?i)\b(password|passwd|secret)\s*[:=]\s*[\"'][^\"']{8,}[\"']")),
)


def main() -> None:
    payload = json.load(sys.stdin)
    tool_input = payload.get("tool_input", {})
    content = "\n".join(
        str(tool_input.get(field, "")) for field in ("content", "new_string")
    )
    findings = [label for label, pattern in SECRET_PATTERNS if pattern.search(content)]
    if findings:
        print(
            f"BLOCKED: write contains secret-shaped content ({', '.join(findings)}). "
            "Secrets never go in source (security-baseline SEC-02). Use an "
            "environment variable or secret manager, and a placeholder like "
            "os.environ['API_KEY'] in code.",
            file=sys.stderr,
        )
        sys.exit(2)


if __name__ == "__main__":
    main()
