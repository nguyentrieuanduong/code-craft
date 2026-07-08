#!/usr/bin/env python3
"""Inject the using-code-craft dispatch skill at session start.

Fires on startup, clear, and compact so dispatch survives context loss —
enforcement is mechanical, not dependent on the model remembering.
"""
import json
import os
from pathlib import Path


def main() -> None:
    root = Path(os.environ.get("CLAUDE_PLUGIN_ROOT") or Path(__file__).resolve().parent.parent)
    skill = (root / "skills" / "using-code-craft" / "SKILL.md").read_text(encoding="utf-8")
    context = (
        "<code-craft-bootstrap>\n"
        f"{skill}\n"
        f"The full skills live in {root / 'skills'}/<name>/SKILL.md — "
        "read the matching SKILL.md before acting on any dispatch-table row.\n"
        "</code-craft-bootstrap>"
    )
    print(json.dumps({
        "hookSpecificOutput": {
            "hookEventName": "SessionStart",
            "additionalContext": context,
        }
    }))


if __name__ == "__main__":
    main()
