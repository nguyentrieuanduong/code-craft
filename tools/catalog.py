"""Validate the skill catalog and deterministic routing fixtures."""

import argparse
import math
import re
import sys
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from itertools import combinations
from pathlib import Path
from typing import Any, Optional

from tools.frontmatter import FrontmatterError, load_mapping, parse_frontmatter


TOKEN_PATTERN = re.compile(r"[a-z0-9]+")
STOP_WORDS = frozenset({
    "and", "any", "are", "before", "for", "from", "into", "not",
    "the", "that", "this", "use", "when", "with", "without",
})
SKILL_SCHEMA = {"name": str, "description": str}
SKILL_REQUIRED = frozenset(SKILL_SCHEMA)
TOP_K = 3
COLLISION_WARN = 0.50
COLLISION_SEVERE = 0.75
NAME_PATTERN = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
REPOSITORY_ROOT = Path(__file__).resolve().parent.parent


@dataclass(frozen=True)
class Skill:
    name: str
    description: str
    path: Path
    frontmatter_chars: int


@dataclass(frozen=True)
class CatalogReport:
    errors: tuple[str, ...]
    warnings: tuple[str, ...]
    positive_passed: int
    positive_total: int
    negative_passed: int
    negative_total: int
    rank_first_passed: int
    rank_first_total: int


def tokenize(text: str) -> frozenset[str]:
    return frozenset(
        token
        for token in TOKEN_PATTERN.findall(text.lower())
        if len(token) > 2 and token not in STOP_WORDS
    )


def binary_cosine(
    left: frozenset[str],
    right: frozenset[str],
) -> float:
    if not left or not right:
        return 0.0
    return len(left & right) / math.sqrt(len(left) * len(right))


def routing_description(skill: Skill, skill_names: frozenset[str]) -> str:
    text = skill.description
    for name in skill_names - {skill.name}:
        text = re.sub(rf"\b{re.escape(name)}\b", " ", text, flags=re.I)
        spaced = name.replace("-", " ")
        text = re.sub(rf"\b{re.escape(spaced)}\b", " ", text, flags=re.I)
    return text


def rank_skills(
    prompt: str,
    skills: Sequence[Skill],
) -> list[tuple[str, float]]:
    skills = tuple(skills)
    skill_names = frozenset(skill.name for skill in skills)
    prompt_tokens = tokenize(prompt)
    scores = (
        (
            skill.name,
            binary_cosine(
                prompt_tokens,
                tokenize(skill.name.replace("-", " "))
                | tokenize(routing_description(skill, skill_names)),
            ),
        )
        for skill in skills
    )
    return sorted(scores, key=lambda item: (-item[1], item[0]))


def load_skill(path: Path) -> Skill:
    parsed = parse_frontmatter(
        path.read_text(),
        schema=SKILL_SCHEMA,
        required=SKILL_REQUIRED,
        context=str(path),
    )
    return Skill(
        name=parsed.metadata["name"],
        description=parsed.metadata["description"],
        path=path,
        frontmatter_chars=parsed.frontmatter_chars,
    )


def _load_skills(root: Path, errors: list[str]) -> tuple[Skill, ...]:
    skills_dir = root / "skills"
    if not skills_dir.is_dir():
        errors.append(f"missing skills directory: {skills_dir}")
        return ()
    skills = []
    for path in sorted(skills_dir.glob("*/SKILL.md")):
        try:
            skill = load_skill(path)
        except (FrontmatterError, OSError) as error:
            errors.append(str(error))
            continue
        if skill.frontmatter_chars > 1024:
            errors.append(f"{skill.name}: frontmatter exceeds 1024 characters")
        if skill.name != path.parent.name:
            errors.append(
                f"{skill.name}: name does not match directory {path.parent.name!r}"
            )
        if not NAME_PATTERN.fullmatch(skill.name):
            errors.append(f"{skill.name}: invalid skill name")
        if len(skill.description) > 500:
            errors.append(f"{skill.name}: description exceeds 500 characters")
        if not skill.description.startswith("Use "):
            errors.append(f"{skill.name}: description must begin with 'Use '")
        skills.append(skill)
    if not skills:
        errors.append(f"no skill files found under {skills_dir}")
    names = [skill.name for skill in skills]
    for name in sorted(set(names)):
        if names.count(name) > 1:
            errors.append(f"duplicate skill name: {name}")
    return tuple(skills)


def _load_cases(path: Path, errors: list[str]) -> Mapping[str, Any]:
    try:
        document = load_mapping(path.read_text(), context=str(path))
    except (FrontmatterError, OSError) as error:
        errors.append(str(error))
        return {}
    expected = {"version", "top_k", "skills"}
    unknown = sorted(set(document) - expected)
    if unknown:
        errors.append(f"routing cases: unknown field(s): {', '.join(unknown)}")
    if type(document.get("version")) is not int or document.get("version") != 1:
        errors.append("routing cases: version must be 1")
    if type(document.get("top_k")) is not int or document.get("top_k") != TOP_K:
        errors.append(f"routing cases: top_k must be {TOP_K}")
    cases = document.get("skills")
    if not isinstance(cases, dict):
        errors.append("routing cases: skills must be a mapping")
        return {}
    if any(type(name) is not str for name in cases):
        errors.append("routing cases: skill names must be text")
        return {}
    return cases


def _validate_case_shape(
    skills: Sequence[Skill],
    cases: Mapping[str, Any],
    errors: list[str],
) -> None:
    skill_names = frozenset(skill.name for skill in skills)
    for name in sorted(skill_names - set(cases)):
        errors.append(f"{name}: missing routing cases")
    for name in sorted(set(cases) - skill_names):
        errors.append(f"{name}: routing cases reference unknown skill")
    for name in sorted(skill_names & set(cases)):
        entry = cases[name]
        if not isinstance(entry, dict):
            errors.append(f"{name}: routing entry must be a mapping")
            continue
        unknown = sorted(set(entry) - {"positive", "negative"})
        if unknown:
            errors.append(f"{name}: unknown routing field(s): {', '.join(unknown)}")
        positives = entry.get("positive")
        negatives = entry.get("negative")
        if not isinstance(positives, list) or len(positives) != 3:
            errors.append(f"{name}: expected exactly 3 positive prompts")
        elif any(type(prompt) is not str or not prompt.strip() for prompt in positives):
            errors.append(f"{name}: positive prompts must be non-empty text")
        if not isinstance(negatives, list) or len(negatives) != 2:
            errors.append(f"{name}: expected exactly 2 negative prompts")
            continue
        for index, negative in enumerate(negatives, start=1):
            if not isinstance(negative, dict) or set(negative) != {"prompt", "owner"}:
                errors.append(f"{name}: negative {index} needs prompt and owner")
                continue
            prompt = negative["prompt"]
            owner = negative["owner"]
            if type(prompt) is not str or not prompt.strip():
                errors.append(f"{name}: negative {index} prompt must be non-empty text")
            if type(owner) is not str or owner not in skill_names:
                errors.append(f"{name}: negative {index} has unknown owner {owner!r}")


def _evaluate_routing(
    skills: Sequence[Skill],
    cases: Mapping[str, Any],
    errors: list[str],
) -> tuple[int, int, int, int, int, int]:
    positive_passed = 0
    positive_total = 0
    negative_passed = 0
    negative_total = 0
    rank_first_passed = 0
    rank_first_total = 0
    skill_names = frozenset(skill.name for skill in skills)
    for name in sorted(skill_names & set(cases)):
        entry = cases[name]
        if not isinstance(entry, dict):
            continue
        positives = entry.get("positive")
        if isinstance(positives, list):
            for prompt in positives:
                if type(prompt) is not str or not prompt.strip():
                    continue
                positive_total += 1
                ranking = rank_skills(prompt, skills)
                scores = dict(ranking)
                rank_first_total += 1
                rank_first_passed += int(ranking[0][0] == name)
                if scores[name] == 0:
                    errors.append(f"{name}: positive prompt scored 0: {prompt!r}")
                elif name not in [skill for skill, _ in ranking[:TOP_K]]:
                    errors.append(
                        f"{name}: positive owner outside top {TOP_K}: {prompt!r}"
                    )
                else:
                    positive_passed += 1
        negatives = entry.get("negative")
        if not isinstance(negatives, list):
            continue
        for negative in negatives:
            if not isinstance(negative, dict) or set(negative) != {"prompt", "owner"}:
                continue
            prompt = negative["prompt"]
            owner = negative["owner"]
            if (
                type(prompt) is not str
                or not prompt.strip()
                or type(owner) is not str
                or owner not in skill_names
            ):
                continue
            negative_total += 1
            ranking = rank_skills(prompt, skills)
            positions = {
                skill_name: index
                for index, (skill_name, _) in enumerate(ranking)
            }
            if positions[owner] >= positions[name]:
                errors.append(
                    f"{owner}: named owner does not outrank {name}: {prompt!r}"
                )
            else:
                negative_passed += 1
    return (
        positive_passed,
        positive_total,
        negative_passed,
        negative_total,
        rank_first_passed,
        rank_first_total,
    )


def _collision_warnings(skills: Sequence[Skill]) -> tuple[str, ...]:
    names = frozenset(skill.name for skill in skills)
    warnings = []
    for left, right in combinations(skills, 2):
        similarity = binary_cosine(
            tokenize(routing_description(left, names)),
            tokenize(routing_description(right, names)),
        )
        if similarity < COLLISION_WARN:
            continue
        label = "severe collision" if similarity >= COLLISION_SEVERE else "collision"
        warnings.append(
            f"{label}: {left.name} / {right.name} ({similarity:.2f})"
        )
    return tuple(warnings)


def validate_repository(root: Path) -> CatalogReport:
    errors: list[str] = []
    skills = _load_skills(root, errors)
    cases = _load_cases(root / "tests" / "routing_cases.yaml", errors)
    _validate_case_shape(skills, cases, errors)
    counts = _evaluate_routing(skills, cases, errors)
    return CatalogReport(
        errors=tuple(errors),
        warnings=_collision_warnings(skills),
        positive_passed=counts[0],
        positive_total=counts[1],
        negative_passed=counts[2],
        negative_total=counts[3],
        rank_first_passed=counts[4],
        rank_first_total=counts[5],
    )


def render_report(report: CatalogReport) -> str:
    lines = [
        (
            "routing: "
            f"positive {report.positive_passed}/{report.positive_total}, "
            f"negative {report.negative_passed}/{report.negative_total}"
        ),
        f"rank-first (informational): {report.rank_first_passed}/{report.rank_first_total}",
    ]
    lines.extend(f"WARNING: {warning}" for warning in report.warnings)
    lines.extend(f"ERROR: {error}" for error in report.errors)
    return "\n".join(lines) + "\n"


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", nargs="?", type=Path, default=REPOSITORY_ROOT)
    args = parser.parse_args(argv)
    report = validate_repository(args.root)
    sys.stdout.write(render_report(report))
    return int(bool(report.errors))


if __name__ == "__main__":
    raise SystemExit(main())
