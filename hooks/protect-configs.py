#!/usr/bin/env python3
"""PreToolUse gate: block edits to linter/formatter configs.

Prevents the classic weak-model shortcut of weakening lint rules instead of
fixing the code. Creation of a missing config is allowed; modification is not.
Exit 2 denies the tool call and feeds stderr back to the model.
"""
import fnmatch
import json
import sys

from hook_payload import target_paths

PROTECTED = (
    ".eslintrc*", "eslint.config.*",
    ".prettierrc*", "prettier.config.*",
    "biome.json*",
    "ruff.toml", ".ruff.toml",
    ".flake8", "mypy.ini", ".pylintrc",
    ".shellcheckrc", ".editorconfig",
    ".golangci.yml", ".golangci.yaml",
    ".rubocop.yml",
)


def main() -> None:
    for path in target_paths(json.load(sys.stdin)):
        name = path.name
        if any(fnmatch.fnmatch(name, pattern) for pattern in PROTECTED) and path.exists():
            print(
                f"BLOCKED: {name} is a protected linter/formatter config. "
                "Do not weaken quality gates to make checks pass — fix the code the "
                "linter is complaining about instead. If the config genuinely needs "
                "changing, ask the user to approve it explicitly.",
                file=sys.stderr,
            )
            sys.exit(2)


if __name__ == "__main__":
    main()
