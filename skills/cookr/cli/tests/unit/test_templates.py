from __future__ import annotations

import pytest

from cookr.core import templates


def test_types():
    assert templates.TYPES == ("ingredient", "recipe")


def test_required_sections_are_the_template_headings_in_order():
    sections = templates.required_sections("recipe")
    assert sections[0] == "Overview"
    assert sections[-2:] == ("Compliance", "Change History")
    assert "Logging" in templates.required_sections("ingredient")


def test_headings_inside_a_fence_are_not_sections(tmp_path, monkeypatch):
    (tmp_path / "recipe.md").write_text(
        "---\ntype: recipe\n---\n\n# Name\n\n## Overview\n\n```md\n## Not A Section\n```\n\n"
        "~~~~\n## Nor This\n~~~~\n\n## Layout\n\nx\n",
        encoding="utf-8",
    )
    monkeypatch.setattr(templates, "templates_dir", lambda: tmp_path)
    assert templates.required_sections("recipe") == ("Overview", "Layout")


def test_missing_template_names_the_install_fix(tmp_path, monkeypatch):
    monkeypatch.setattr(templates, "templates_dir", lambda: tmp_path)
    with pytest.raises(FileNotFoundError, match="install.sh"):
        templates.template_path("ingredient")


def test_unknown_type_is_refused():
    with pytest.raises(ValueError, match="unknown template type"):
        templates.template_path("guideline")


def test_default_dir_is_the_cookbook_references(monkeypatch):
    from cookbook.core import refs

    monkeypatch.undo()  # drop the suite's hermetic override for this one check
    assert templates.templates_dir() == refs.references_dir() / "templates"
