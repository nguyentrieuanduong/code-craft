"""Strict YAML loading for project-owned authoring metadata."""

from collections.abc import Collection, Mapping
from dataclasses import dataclass
from typing import Any

import yaml
from yaml.nodes import MappingNode


class FrontmatterError(ValueError):
    """Project metadata is missing, malformed, or outside its schema."""


class StrictSafeLoader(yaml.SafeLoader):
    """SafeLoader variant that rejects duplicate mapping keys."""


def _construct_mapping(
    loader: StrictSafeLoader,
    node: MappingNode,
    deep: bool = False,
) -> dict[str, Any]:
    loader.flatten_mapping(node)
    result = {}
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node, deep=deep)
        if type(key) is not str:
            raise FrontmatterError(f"mapping key must be text: {key!r}")
        if key in result:
            raise FrontmatterError(f"duplicate key: {key!r}")
        result[key] = loader.construct_object(value_node, deep=deep)
    return result


StrictSafeLoader.add_constructor(
    yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG,
    _construct_mapping,
)


@dataclass(frozen=True)
class ParsedDocument:
    metadata: dict[str, Any]
    body: str
    frontmatter_chars: int


def load_mapping(source: str, *, context: str) -> dict[str, Any]:
    try:
        value = yaml.load(source, Loader=StrictSafeLoader)
    except FrontmatterError:
        raise
    except yaml.YAMLError as error:
        raise FrontmatterError(f"{context}: malformed YAML: {error}") from error
    if not isinstance(value, dict):
        raise FrontmatterError(f"{context}: YAML root must be a mapping")
    return value


def parse_frontmatter(
    text: str,
    *,
    schema: Mapping[str, type],
    required: Collection[str],
    context: str,
) -> ParsedDocument:
    lines = text.splitlines(keepends=True)
    if not lines or lines[0].rstrip("\r\n") != "---":
        raise FrontmatterError(f"{context}: missing opening delimiter")
    closing = next(
        (
            index
            for index, line in enumerate(lines[1:], start=1)
            if line.rstrip("\r\n") == "---"
        ),
        None,
    )
    if closing is None:
        raise FrontmatterError(f"{context}: missing closing delimiter")
    source = "".join(lines[1:closing])
    metadata = load_mapping(source, context=context)
    unknown = sorted(set(metadata) - set(schema))
    if unknown:
        raise FrontmatterError(
            f"{context}: unknown field(s): {', '.join(unknown)}"
        )
    for field in required:
        if field not in metadata:
            raise FrontmatterError(f"{context}: missing required field {field!r}")
        if isinstance(metadata[field], str) and not metadata[field].strip():
            raise FrontmatterError(f"{context}: empty required field {field!r}")
    for field, value in metadata.items():
        expected = schema[field]
        if type(value) is not expected:
            raise FrontmatterError(
                f"{context}: {field!r} must be {expected.__name__}"
            )
    return ParsedDocument(
        metadata=metadata,
        body="".join(lines[closing + 1 :]),
        frontmatter_chars=len(source),
    )
