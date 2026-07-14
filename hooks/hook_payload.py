"""Payload normalizer for Claude Edit/Write and Codex apply_patch/Bash.

Never log the payload — hooks may see secrets or PII.
"""
from __future__ import annotations

import re
from pathlib import Path
from typing import Any, Iterator, Mapping

PATCH_HEADER = re.compile(
    r"^\*\*\* (?:Add|Update|Delete) File: (.+)$",
    re.MULTILINE,
)


def _iter_strings(value: Any) -> Iterator[str]:
    if isinstance(value, str):
        yield value
    elif isinstance(value, Mapping):
        for item in value.values():
            yield from _iter_strings(item)
    elif isinstance(value, (list, tuple)):
        for item in value:
            yield from _iter_strings(item)


def tool_input(payload: Any) -> Any:
    return payload.get("tool_input", {}) if isinstance(payload, Mapping) else {}


def proposed_text(payload: Any) -> str:
    return "\n".join(_iter_strings(tool_input(payload)))


def command(payload: Any) -> str:
    normalized = tool_input(payload)
    if not isinstance(normalized, Mapping):
        return ""
    return str(
        normalized.get("command")
        or normalized.get("cmd")
        or normalized.get("input")
        or ""
    )


def target_paths(payload: Any) -> tuple[Path, ...]:
    normalized = tool_input(payload)
    paths: list[str] = []
    if isinstance(normalized, Mapping) and normalized.get("file_path"):
        paths.append(str(normalized["file_path"]))
    for text in _iter_strings(normalized):
        paths.extend(PATCH_HEADER.findall(text))
    return tuple(dict.fromkeys(Path(path) for path in paths))
