"""The type registry agrees with the formatting rules, and validate() enforces them."""

from __future__ import annotations

import json
import re

import pytest

from cookr.core.artifact import load_folder
from cookr.core.artifact_types import COMMON_FIELDS, TYPES, validate

from ..conftest import FIXTURES, REPO_ROOT

FORMATTING = REPO_ROOT / "tbd" / "compliance" / "artifact-formatting"
FOLDERS = sorted((FIXTURES / "artifacts" / "folders").iterdir())


def _section_order(kind: str) -> list[tuple[str, bool]]:
    text = (FORMATTING / f"{kind}-formatting.md").read_text()
    block = text.split("## Section Order", 1)[1].split("\n## ", 1)[0]
    found = re.findall(r"^\d+\. `## ([^`]+)`(.*)$", block, re.M)
    return [(h, "MAY" not in rest) for h, rest in found if h != "Change History"]


@pytest.mark.parametrize("kind", ["ingredient", "recipe"])
def test_closed_sections_match_the_formatting_rules(kind):
    assert list(TYPES[kind].sections) == _section_order(kind)


def test_common_fields_match_the_conventions_table():
    text = (REPO_ROOT / "guide" / "introduction" / "conventions.md").read_text()
    required = re.findall(r"^\| `([a-z-]+)` \| Yes \|", text, re.M)
    assert list(COMMON_FIELDS) == required


def _schema() -> dict:
    return json.loads((REPO_ROOT / "references" / "artifact.schema.json").read_text())


@pytest.mark.parametrize("folder", FOLDERS, ids=lambda p: p.name)
def test_samples_conform(folder):
    assert validate(load_folder(folder)) == []


def test_samples_cover_every_type():
    assert sorted(load_folder(f).type for f in FOLDERS) == sorted(TYPES)


@pytest.mark.parametrize("folder", FOLDERS, ids=lambda p: p.name)
def test_samples_match_the_json_schema(folder):
    jsonschema = pytest.importorskip("jsonschema")
    jsonschema.validate(json.loads((folder / "artifact.json").read_text()), _schema())


def _sample(name: str):
    return load_folder(FIXTURES / "artifacts" / "folders" / name)


def test_schema_requires_exactly_the_common_fields():
    assert _schema()["properties"]["meta"]["required"] == list(COMMON_FIELDS)


@pytest.mark.parametrize("folder", FOLDERS, ids=lambda p: p.name)
def test_an_artifact_without_approval_fields_conforms(folder):
    a = load_folder(folder)
    for f in ("approved-by", "approved-date"):
        a.meta.pop(f, None)
    assert validate(a) == []
    jsonschema = pytest.importorskip("jsonschema")
    doc = json.loads((folder / "artifact.json").read_text())
    for f in ("approved-by", "approved-date"):
        doc["meta"].pop(f, None)
    jsonschema.validate(doc, _schema())


def test_missing_and_misordered_sections_are_reported():
    a = _sample("mcp-tool")
    a.parts = [p for p in a.parts if p.name != "states"]
    i = next(n for n, p in enumerate(a.parts) if p.name == "logging")
    a.parts.insert(1, a.parts.pop(i))
    problems = validate(a)
    assert "missing section: ## States" in problems
    assert any(p.startswith("out of order:") for p in problems)


def test_unknown_section_in_a_closed_type_is_reported():
    a = _sample("mcp-server")
    a.parts[2].heading = "Architecture"
    assert "unknown section: ## Architecture" in validate(a)


def test_free_form_types_allow_any_section():
    a = _sample("transactions-and-concurrency")
    a.parts[1].heading = "Anything At All"
    assert validate(a) == []


def test_history_must_come_last():
    a = _sample("yagni")
    a.parts.reverse()
    assert any("Change History" in p for p in validate(a))


def test_title_must_open_the_intro():
    a = _sample("yagni")
    a.meta["title"] = "Something Else"
    assert any(p.startswith("intro must open with") for p in validate(a))


def test_meta_problems_are_reported():
    a = _sample("mcp-server")
    del a.meta["ingredients"]
    a.meta.update(id="nope", version="1.0", status="done", created="June", tags="x")
    problems = validate(a)
    for expected in ("missing field: ingredients", "id: not a UUID", "version: not semver",
                     "status: not one of", "created: not an ISO date", "tags: must be a list"):
        assert any(p.startswith(expected) for p in problems), expected


def test_unknown_type_is_reported():
    a = _sample("yagni")
    a.meta["type"] = "reference"
    assert validate(a) == ["type: not an artifact type: 'reference'"]


@pytest.mark.parametrize("value", ["June 9", "2026-6-9"])
def test_a_malformed_approved_date_is_reported(value):
    a = _sample("mcp-tool")
    a.meta["approved-date"] = value
    assert f"approved-date: not an ISO date or \"\": {value!r}" in validate(a)
    jsonschema = pytest.importorskip("jsonschema")
    doc = json.loads((FIXTURES / "artifacts" / "folders" / "mcp-tool" / "artifact.json").read_text())
    doc["meta"]["approved-date"] = value
    with pytest.raises(jsonschema.ValidationError):
        jsonschema.validate(doc, _schema())


@pytest.mark.parametrize("value", ["", "2026-06-09"])
def test_an_empty_or_iso_approved_date_conforms(value):
    a = _sample("mcp-tool")
    a.meta["approved-date"] = value
    assert validate(a) == []
