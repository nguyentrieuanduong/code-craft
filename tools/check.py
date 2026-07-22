"""Run the deterministic project checks used locally and in CI."""

import subprocess
import sys
from collections.abc import Sequence


COMMANDS = (
    (sys.executable, "-m", "unittest", "discover", "tests"),
    (sys.executable, "-m", "tools.catalog"),
)
FORBIDDEN_COMMAND_FRAGMENTS = (
    "tests/scenarios/run.py",
    "claude",
)


def assert_deterministic_commands(
    commands: Sequence[Sequence[str]] = COMMANDS,
) -> None:
    for command in commands:
        rendered = " ".join(command)
        forbidden = next(
            (
                fragment
                for fragment in FORBIDDEN_COMMAND_FRAGMENTS
                if fragment in rendered
            ),
            None,
        )
        if forbidden:
            raise RuntimeError(
                f"deterministic check contains forbidden command: {forbidden}"
            )


def main() -> int:
    assert_deterministic_commands()
    for command in COMMANDS:
        completed = subprocess.run(command, check=False)
        if completed.returncode:
            return completed.returncode
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
