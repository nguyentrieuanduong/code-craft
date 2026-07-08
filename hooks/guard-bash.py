#!/usr/bin/env python3
"""PreToolUse gate on Bash: block hook-bypassing and history-destroying git.

If a pre-commit hook fails, the fix is the code, not --no-verify.
Commands are tokenized rather than regex-matched so that flag order cannot
dodge the rules (`git push origin main -f`, `git push origin +main`) and
quoted strings cannot trigger false positives.
Exit 2 denies the command and feeds stderr back to the model.
"""
import json
import shlex
import sys

PROTECTED_BRANCHES = ("main", "master")

NO_VERIFY_MSG = (
    "git --no-verify bypasses quality hooks. Fix whatever the hook is "
    "failing on instead (systematic-debugging), or ask the user."
)
FORCE_PUSH_MSG = (
    "Force-pushing to main/master can destroy shared history. Ask the user "
    "explicitly before any force push."
)


def split_commands(command):
    """Yield the token list of each simple command in a compound line."""
    lex = shlex.shlex(command, posix=True, punctuation_chars=True)
    lex.whitespace_split = True
    segment = []
    for token in lex:
        if token and all(ch in ";&|" for ch in token):
            if segment:
                yield segment
            segment = []
        else:
            segment.append(token)
    if segment:
        yield segment


def targets_protected_branch(token):
    destination = token.lstrip("+").split(":")[-1]
    return destination in PROTECTED_BRANCHES or destination.endswith(
        tuple(f"/{branch}" for branch in PROTECTED_BRANCHES)
    )


def violation(tokens):
    if "git" not in tokens:
        return None
    rest = tokens[tokens.index("git") + 1:]
    if "--no-verify" in rest and ("commit" in rest or "push" in rest):
        return NO_VERIFY_MSG
    if "push" in rest:
        args = rest[rest.index("push") + 1:]
        forced = any(arg == "-f" or arg.startswith("--force") for arg in args)
        for arg in args:
            if arg.startswith("-"):
                continue
            if targets_protected_branch(arg) and (forced or arg.startswith("+")):
                return FORCE_PUSH_MSG
    return None


def main() -> None:
    payload = json.load(sys.stdin)
    command = payload.get("tool_input", {}).get("command", "")
    try:
        segments = list(split_commands(command))
    except ValueError:
        # Unbalanced quotes: fall back to a naive split — may false-positive
        # on quoted text, never false-negative on a real git command.
        segments = [command.split()]
    for tokens in segments:
        reason = violation(tokens)
        if reason:
            print(f"BLOCKED: {reason}", file=sys.stderr)
            sys.exit(2)


if __name__ == "__main__":
    main()
