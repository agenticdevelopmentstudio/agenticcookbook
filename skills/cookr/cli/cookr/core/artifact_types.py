"""The artifact type registry: what each type's folder must hold, and in what order.

Derived from `cookbook/compliance/artifact-formatting/<type>-formatting.md` and
the field table in `cookbook/introduction/conventions.md`; those files stay the
authority, and tests/unit/test_artifact_types.py fails when this drifts from them.

A section is `(heading, required)`. Ingredients and recipes have a closed,
ordered section list, so their part names are fixed. Principles and guidelines
are free-form between the intro and the history, so any section is allowed.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Optional

from .artifact import HISTORY, HISTORY_HEADING, INTRO, Artifact

COMMON_FIELDS = (
    "id", "title", "domain", "type", "version", "status", "language", "created",
    "modified", "author", "copyright", "license", "summary", "platforms", "tags",
    "depends-on", "related", "references", "approved-by", "approved-date",
)
LIST_FIELDS = frozenset({"platforms", "tags", "depends-on", "related", "references",
                         "ingredients", "triggers"})
STATUSES = ("wip", "draft", "review", "accepted", "deprecated")

_SEMVER = re.compile(r"\d+\.\d+\.\d+")
_DATE = re.compile(r"\d{4}-\d{2}-\d{2}")
_UUID = re.compile(r"[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}", re.I)


@dataclass(frozen=True)
class ArtifactType:
    name: str
    fields: tuple[str, ...]           # required frontmatter fields
    sections: Optional[tuple[tuple[str, bool], ...]]  # None: free-form body

    @property
    def closed(self) -> bool:
        return self.sections is not None


_INGREDIENT = (
    ("Overview", True), ("Behavioral Requirements", True), ("Appearance", True),
    ("States", True), ("Accessibility", True), ("Conformance Test Vectors", True),
    ("Edge Cases", True), ("Configuration", True), ("Deep Linking", False),
    ("Localization", False), ("Accessibility Options", False), ("Feature Flags", False),
    ("Analytics", False), ("Privacy", False), ("Logging", True), ("Platform Notes", True),
    ("Reference Implementations", False), ("Design Decisions", True), ("Compliance", True),
)
_RECIPE = (
    ("Overview", True), ("Ingredients", True), ("Integration Requirements", True),
    ("Layout", True), ("Shared State", True), ("Integration Test Vectors", True),
    ("Edge Cases", True), ("Platform Notes", True), ("Reference Implementations", False),
    ("Design Decisions", True), ("Compliance", True),
)

TYPES: dict[str, ArtifactType] = {
    "principle": ArtifactType("principle", COMMON_FIELDS, None),
    "guideline": ArtifactType("guideline", COMMON_FIELDS, None),
    "ingredient": ArtifactType("ingredient", COMMON_FIELDS, _INGREDIENT),
    "recipe": ArtifactType("recipe", COMMON_FIELDS + ("ingredients",), _RECIPE),
}


def _check_meta(meta: dict, t: ArtifactType) -> list[str]:
    problems = [f"missing field: {f}" for f in t.fields if f not in meta]
    for f in LIST_FIELDS & meta.keys():
        if not isinstance(meta[f], list):
            problems.append(f"{f}: must be a list")
    if "id" in meta and not _UUID.fullmatch(str(meta["id"])):
        problems.append(f"id: not a UUID: {meta['id']!r}")
    if "version" in meta and not _SEMVER.fullmatch(str(meta["version"])):
        problems.append(f"version: not semver: {meta['version']!r}")
    if "status" in meta and meta["status"] not in STATUSES:
        problems.append(f"status: not one of {', '.join(STATUSES)}: {meta['status']!r}")
    for f in ("created", "modified"):
        if f in meta and not _DATE.fullmatch(str(meta[f])):
            problems.append(f"{f}: not an ISO date: {meta[f]!r}")
    return problems


def _check_sections(headings: list[str], t: ArtifactType) -> list[str]:
    order = {h: i for i, (h, _) in enumerate(t.sections or ())}
    problems = [f"missing section: ## {h}" for h, req in t.sections or () if req and h not in headings]
    problems += [f"unknown section: ## {h}" for h in headings if h not in order]
    known = [h for h in headings if h in order]
    for a, b in zip(known, known[1:]):
        if order[b] <= order[a]:
            problems.append(f"out of order: ## {b} after ## {a}")
    return problems


def validate(artifact: Artifact) -> list[str]:
    """Every way `artifact` breaks its type's shape; empty when it conforms."""
    t = TYPES.get(artifact.type)
    if t is None:
        return [f"type: not an artifact type: {artifact.type!r}"]
    problems = _check_meta(artifact.meta, t)
    parts = artifact.parts
    intro = parts[0] if parts and parts[0].name == INTRO else None
    title = artifact.meta.get("title")
    if intro is None:
        problems.append("missing intro (the `# Title` and its statement)")
    else:
        h1 = next((l for l in intro.text.splitlines() if l.strip()), "")
        if h1 != f"# {title}":
            problems.append(f"intro must open with `# {title}`, found {h1!r}")
        elif not t.closed and len(intro.text.strip().splitlines()) < 2:
            # A free-form type states its idea under the title; a closed type
            # states it in ## Overview.
            problems.append("intro has no statement after the title")
    if not parts or parts[-1].name != HISTORY:
        problems.append(f"must end with ## {HISTORY_HEADING}")
    elif "| Version | Date | Author | Summary |" not in parts[-1].text:
        problems.append(f"## {HISTORY_HEADING} has no Version | Date | Author | Summary table")
    if t.closed:
        problems += _check_sections([p.heading.strip() for p in parts
                                     if p.heading is not None and p.name != HISTORY], t)
    return problems
