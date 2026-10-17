#!/usr/bin/env python3
"""PreToolUse gate on Bash: block hook-bypassing and history-destroying git.

If a pre-commit hook fails, the fix is the code, not --no-verify.
Commands are tokenized rather than regex-matched so that flag order cannot
dodge the rules (`git push origin main -f`, `git push origin +main`) and
quoted strings cannot trigger false positives. Git's own option grammar is
followed where a bypass hides in it: global options before the subcommand,
`-c core.hooksPath=...` overrides, combined short flags (`-anm`), option
values (`-m '--no-verify'`, `-mn`), and unambiguous long-option prefixes
(`--no-veri`).
Exit 2 denies the command and feeds stderr back to the model.
"""
import json
import shlex
import sys

from hook_payload import command as payload_command

PROTECTED_BRANCHES = ("main", "master")
HOOKED_SUBCOMMANDS = frozenset({"commit", "push", "merge", "cherry-pick", "rebase", "am"})
GLOBAL_VALUE_OPTIONS = frozenset({"-c", "-C", "--git-dir", "--work-tree", "--namespace", "--config-env"})
NO_VERIFY_FLAG = "--no-verify"
# Shortest prefix git resolves to --no-verify: `--no-ver` is ambiguous
# with the auto-negated `--no-verbose`, so git rejects it.
NO_VERIFY_MIN_PREFIX = "--no-veri"
# Short options whose value follows (stuck or as the next token), and the
# long options that take a separate value, per subcommand. Their values are
# data: `git commit -mn` sets the message to "n".
SHORT_VALUE_OPTIONS = {
    "commit": frozenset("mFCct"),
    "push": frozenset("o"),
    "merge": frozenset("mFsX"),
    "cherry-pick": frozenset("msX"),
    "rebase": frozenset("sXx"),
    "am": frozenset(),
}
# Optional values that can only be stuck to the flag (`-uno`, `-Skeyid`).
SHORT_STUCK_OPTIONS = {"commit": frozenset("uS")}
LONG_VALUE_OPTIONS = {
    "commit": frozenset({
        "--message", "--file", "--reuse-message", "--reedit-message", "--fixup",
        "--squash", "--author", "--date", "--template", "--cleanup", "--trailer",
    }),
    "push": frozenset({"--repo", "--receive-pack", "--exec", "--push-option"}),
    "merge": frozenset({"--message", "--file", "--strategy", "--strategy-option", "--into-name"}),
    "cherry-pick": frozenset({"--mainline", "--strategy", "--strategy-option"}),
    "rebase": frozenset({"--onto", "--strategy", "--strategy-option", "--exec"}),
    "am": frozenset({"--directory", "--exclude", "--include", "--patch-format", "--resolvemsg"}),
}

NO_VERIFY_MSG = (
    "git --no-verify bypasses quality hooks. Fix whatever the hook is "
    "failing on instead (systematic-debugging), or ask the user."
)
HOOKS_PATH_MSG = (
    "Overriding core.hooksPath bypasses quality hooks. Fix whatever the hook "
    "is failing on instead (systematic-debugging), or ask the user."
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


def overrides_hooks_path(setting):
    return setting.split("=", 1)[0].strip().lower() == "core.hookspath"


def parse_invocation(args):
    """Split git's arguments into (config settings, subcommand, its args)."""
    settings = []
    index = 0
    while index < len(args) and args[index].startswith("-"):
        option = args[index]
        if option in GLOBAL_VALUE_OPTIONS and index + 1 < len(args):
            if option in ("-c", "--config-env"):
                settings.append(args[index + 1])
            index += 2
            continue
        if option.startswith("-c") and len(option) > 2:
            settings.append(option[2:])
        elif option.startswith("--config-env="):
            settings.append(option.split("=", 1)[1])
        index += 1
    if index == len(args):
        return settings, None, []
    return settings, args[index], args[index + 1:]


def short_cluster_has_no_verify(subcommand, cluster):
    """Scan `-anm`-style clusters; `-n` means --no-verify on commit only."""
    value_options = SHORT_VALUE_OPTIONS.get(subcommand, frozenset())
    stuck_options = SHORT_STUCK_OPTIONS.get(subcommand, frozenset())
    for position, flag in enumerate(cluster):
        if flag in value_options or flag in stuck_options:
            return False, flag in value_options and position == len(cluster) - 1
        if flag == "n" and subcommand == "commit":
            return True, False
    return False, False


def has_no_verify(subcommand, args):
    long_values = LONG_VALUE_OPTIONS.get(subcommand, frozenset())
    skip_next = False
    for arg in args:
        if skip_next:
            skip_next = False
            continue
        if arg == "--":
            return False
        if arg.startswith("--"):
            name = arg.split("=", 1)[0]
            if len(name) >= len(NO_VERIFY_MIN_PREFIX) and NO_VERIFY_FLAG.startswith(name):
                return True
            skip_next = name in long_values and "=" not in arg
        elif arg.startswith("-") and len(arg) > 1:
            found, skip_next = short_cluster_has_no_verify(subcommand, arg[1:])
            if found:
                return True
    return False


def force_pushes_protected_branch(args):
    forced = any(arg == "-f" or arg.startswith("--force") for arg in args)
    for arg in args:
        if arg.startswith("-"):
            continue
        if targets_protected_branch(arg) and (forced or arg.startswith("+")):
            return True
    return False


def violation(tokens):
    if "git" not in tokens:
        return None
    settings, subcommand, args = parse_invocation(tokens[tokens.index("git") + 1:])
    if subcommand not in HOOKED_SUBCOMMANDS:
        return None
    if any(overrides_hooks_path(setting) for setting in settings):
        return HOOKS_PATH_MSG
    if has_no_verify(subcommand, args):
        return NO_VERIFY_MSG
    if subcommand == "push" and force_pushes_protected_branch(args):
        return FORCE_PUSH_MSG
    return None


def main() -> None:
    payload = json.load(sys.stdin)
    command = payload_command(payload)
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
