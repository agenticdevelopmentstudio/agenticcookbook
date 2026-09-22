"""Cover every rule emitted by `core.checks.phase_a`.

Each test builds the minimal markdown that triggers one rule; we then assert
the report contains an issue for that rule (and that no unrelated rule fired
for a clean baseline)."""

from __future__ import annotations

from pathlib import Path

import pytest

from cookbook.core.checks import phase_a


GOOD_FRONTMATTER = """\
---
id: 11111111-2222-3333-4444-555555555555
title: T
domain: agenticdevelopercookbook://cookbook/recipes/r
type: recipe
version: 1.0.0
status: draft
language: en
created: 2026-05-15
modified: 2026-05-15
author: T
copyright: 2026 T
license: MIT
summary: x
---
# T

Body.
"""


def _cookbook_with(tmp_path: Path, name: str, body: str) -> Path:
    root = tmp_path / "cookbook"
    (root / "recipes").mkdir(parents=True)
    (root / "recipes" / name).write_text(body, encoding="utf-8")
    return root


def test_clean_baseline_passes(tmp_path):
    root = _cookbook_with(tmp_path, "r.md", GOOD_FRONTMATTER)
    report = phase_a(root)
    assert report.ok, report.issues


def test_missing_frontmatter(tmp_path):
    root = _cookbook_with(tmp_path, "r.md", "# Just a header\n")
    report = phase_a(root)
    rules = {i.rule for i in report.issues}
    assert "frontmatter-present" in rules


def test_missing_required_field(tmp_path):
    body = GOOD_FRONTMATTER.replace("license: MIT\n", "")
    root = _cookbook_with(tmp_path, "r.md", body)
    report = phase_a(root)
    rules = {i.rule for i in report.issues}
    assert "required-field:license" in rules


def test_bad_uuid(tmp_path):
    body = GOOD_FRONTMATTER.replace(
        "id: 11111111-2222-3333-4444-555555555555",
        "id: not-a-uuid",
    )
    root = _cookbook_with(tmp_path, "r.md", body)
    report = phase_a(root)
    rules = {i.rule for i in report.issues}
    assert "id-uuid" in rules


def test_bad_semver(tmp_path):
    body = GOOD_FRONTMATTER.replace("version: 1.0.0", "version: v1.x")
    root = _cookbook_with(tmp_path, "r.md", body)
    report = phase_a(root)
    rules = {i.rule for i in report.issues}
    assert "version-semver" in rules


def test_bad_type(tmp_path):
    body = GOOD_FRONTMATTER.replace("type: recipe", "type: bogus")
    root = _cookbook_with(tmp_path, "r.md", body)
    report = phase_a(root)
    rules = {i.rule for i in report.issues}
    assert "type-valid" in rules


def test_bad_status(tmp_path):
    body = GOOD_FRONTMATTER.replace("status: draft", "status: rejected")
    root = _cookbook_with(tmp_path, "r.md", body)
    report = phase_a(root)
    rules = {i.rule for i in report.issues}
    assert "status-valid" in rules


def test_domain_mismatch(tmp_path):
    body = GOOD_FRONTMATTER.replace(
        "domain: agenticdevelopercookbook://cookbook/recipes/r",
        "domain: agenticdevelopercookbook://cookbook/recipes/wrong",
    )
    root = _cookbook_with(tmp_path, "r.md", body)
    report = phase_a(root)
    rules = {i.rule for i in report.issues}
    assert "domain-matches-path" in rules


def test_broken_link(tmp_path):
    root = _cookbook_with(
        tmp_path,
        "r.md",
        GOOD_FRONTMATTER.replace("Body.", "See [missing](./does-not-exist.md)."),
    )
    report = phase_a(root)
    rules = {i.rule for i in report.issues}
    assert "link-resolves" in rules


def test_external_links_ignored(tmp_path):
    body = GOOD_FRONTMATTER.replace(
        "Body.",
        "Links: [a](https://example.com) [b](mailto:x@y) [c](agenticdevelopercookbook://x/y)"
        " [d](agenticdevelopertoolkit://recipes/button#pressed).",
    )
    root = _cookbook_with(tmp_path, "r.md", body)
    report = phase_a(root)
    assert report.ok, report.issues


def test_duplicate_id(tmp_path):
    root = tmp_path / "cookbook"
    (root / "recipes").mkdir(parents=True)
    (root / "recipes" / "a.md").write_text(
        GOOD_FRONTMATTER.replace(
            "domain: agenticdevelopercookbook://cookbook/recipes/r",
            "domain: agenticdevelopercookbook://cookbook/recipes/a",
        ),
        encoding="utf-8",
    )
    (root / "recipes" / "b.md").write_text(
        GOOD_FRONTMATTER.replace(
            "domain: agenticdevelopercookbook://cookbook/recipes/r",
            "domain: agenticdevelopercookbook://cookbook/recipes/b",
        ),
        encoding="utf-8",
    )
    report = phase_a(root)
    rules = {i.rule for i in report.issues}
    assert "id-unique" in rules


def test_fix_for_known_rule_returns_hint():
    from cookbook.core.checks import fix_for

    assert "UUID" in fix_for("id-uuid")
    assert "semver" in fix_for("version-semver").lower()


def test_fix_for_required_field_includes_field_name():
    from cookbook.core.checks import fix_for

    hint = fix_for("required-field:title")
    assert "title" in hint
    assert "cookbook update" in hint


def test_fix_for_unknown_rule_returns_empty():
    from cookbook.core.checks import fix_for

    assert fix_for("not-a-real-rule") == ""
