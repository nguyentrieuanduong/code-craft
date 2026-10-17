#!/usr/bin/env python3
"""PreToolUse gate: block edits to linter/formatter configs and ignore files.

Prevents the classic weak-model shortcut of weakening lint rules — or adding
the failing file to an ignore list — instead of fixing the code. Creation of
a missing config is allowed; modification is not. Names match
case-insensitively: on macOS and Windows `.ESLINTRC.JSON` is the same file.
Exit 2 denies the tool call and feeds stderr back to the model.
"""
import fnmatch
import json
import sys

from hook_payload import target_paths

PROTECTED = (
    ".eslintrc*", "eslint.config.*", ".eslintignore",
    ".prettierrc*", "prettier.config.*", ".prettierignore",
    "biome.json*", ".biome.json*",
    ".stylelintrc*", "stylelint.config.*", ".stylelintignore",
    ".markdownlint*",
    "ruff.toml", ".ruff.toml",
    ".flake8", "mypy.ini", ".pylintrc",
    ".shellcheckrc", ".editorconfig",
    ".golangci.yml", ".golangci.yaml",
    ".rubocop.yml",
)


def is_protected(name: str) -> bool:
    return any(fnmatch.fnmatchcase(name.lower(), pattern) for pattern in PROTECTED)


def main() -> None:
    for path in target_paths(json.load(sys.stdin)):
        if is_protected(path.name) and path.exists():
            print(
                f"BLOCKED: {path.name} is a protected linter/formatter config. "
                "Do not weaken quality gates to make checks pass — fix the code the "
                "linter is complaining about instead. If the config genuinely needs "
                "changing, ask the user to approve it explicitly.",
                file=sys.stderr,
            )
            sys.exit(2)


if __name__ == "__main__":
    main()
