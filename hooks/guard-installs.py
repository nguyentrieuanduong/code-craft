#!/usr/bin/env python3
"""PreToolUse gate on Bash: pause before commands that add a new dependency.

~20% of LLM package suggestions name packages that do not exist, and the
fake names recur often enough for attackers to pre-register them
("slopsquatting" — Spracklen et al., USENIX Security 2025). Restoring from
a lockfile or pinned requirements file is routine and passes silently;
adding a NEW package returns permission decision "ask" with the SEC-09
vetting checklist so a human confirms the package is real, healthy, and
pinned before it lands.
"""
import json
import shlex
import sys

# manager token -> subcommands that add new packages
ADD_SUBCOMMANDS = {
    "npm": {"install", "i", "add"},
    "pnpm": {"install", "i", "add"},
    "yarn": {"add"},
    "pip": {"install"},
    "pip3": {"install"},
    "uv": {"add"},
    "cargo": {"add"},
    "go": {"get"},
}

# flags whose following token is a value, never a package name
VALUE_FLAGS = {
    "-c", "--constraint", "-i", "--index-url", "--extra-index-url",
    "-f", "--find-links", "-t", "--target", "--registry", "-w", "--workspace",
}

LOCAL_SUFFIXES = (".whl", ".tar.gz", ".tgz", ".zip")


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


def is_local(arg):
    return (
        arg in (".", "..")
        or arg.startswith(("./", "../", "/", "~"))
        or arg.endswith(LOCAL_SUFFIXES)
    )


def added_packages(tokens):
    """Names of registry packages this command would newly install."""
    names = []
    for index, raw in enumerate(tokens):
        manager = raw.rsplit("/", 1)[-1]
        subcommands = ADD_SUBCOMMANDS.get(manager)
        if not subcommands:
            continue
        rest = tokens[index + 1:]
        sub_index = next(
            (j for j, tok in enumerate(rest) if not tok.startswith("-")), None
        )
        if sub_index is None or rest[sub_index] not in subcommands:
            continue
        args = rest[sub_index + 1:]
        if manager in ("pip", "pip3") and (
            "-r" in args or "--requirement" in args
        ):
            continue  # restoring pinned requirements, not adding
        skip_next = False
        for arg in args:
            if skip_next:
                skip_next = False
                continue
            if arg in VALUE_FLAGS:
                skip_next = True
                continue
            if arg.startswith("-") or is_local(arg):
                continue
            names.append(arg)
    return names


def main() -> None:
    payload = json.load(sys.stdin)
    command = payload.get("tool_input", {}).get("command", "")
    try:
        segments = list(split_commands(command))
    except ValueError:
        # Unbalanced quotes: naive split may false-positive on quoted text,
        # never false-negative on a real install command.
        segments = [command.split()]
    packages = []
    for tokens in segments:
        packages.extend(added_packages(tokens))
    if not packages:
        return
    listed = ", ".join(dict.fromkeys(packages))
    reason = (
        f"SEC-09 supply-chain gate: this command adds {listed}. Verify "
        "before approving: (1) the name is exactly the intended package — "
        "~20% of LLM package suggestions are hallucinated and recurring "
        "fakes get pre-registered by attackers; (2) the registry page shows "
        "plausible age, maintainers, and adoption; (3) the version is "
        "pinned and the lockfile lands in the same change; (4) the reason "
        "for the dependency is stated."
    )
    print(json.dumps({
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "ask",
            "permissionDecisionReason": reason,
        }
    }))


if __name__ == "__main__":
    main()
