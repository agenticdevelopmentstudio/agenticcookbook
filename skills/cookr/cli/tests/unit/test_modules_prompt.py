"""`cookr prompt extract` assembles module + references + action + sources + existing recipe."""

from __future__ import annotations

import json
import shutil
from pathlib import Path

import pytest

from cookr.cli import main
from cookr.modules.prompt import prompt_cli


@pytest.fixture
def extract_refs(monkeypatch, tmp_path):
    """Stand-in for install.sh's materialisation: copy the manifest's files."""
    repo_root = Path(__file__).resolve().parents[5]
    manifest = json.loads((prompt_cli.PROMPTS_DIR / "extract" / "reference-manifest.json").read_text())
    dest = tmp_path / "references"
    for entry in manifest["files"]:
        src = repo_root / entry["src"]
        dst = dest / entry["dst"]
        if entry["type"] == "file":
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, dst)
        else:
            for f in src.rglob(entry.get("include", "*")):
                if f.is_file():
                    t = dst / f.relative_to(src)
                    t.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(f, t)
    monkeypatch.setattr(prompt_cli, "references_dir", lambda: dest)
    return dest


def test_prompt_lists_actions(capsys):
    assert main(["prompt"]) == 0
    assert "extract" in capsys.readouterr().out


def test_extract_includes_sources_and_existing_recipe(mini_repo, extract_refs, capsys):
    assert main(["-p", str(mini_repo), "prompt", "extract", "button"]) == 0
    out = capsys.readouterr().out
    assert "You are a UI component specification writer." in out
    assert "## reference: templates/ingredient.md" in out
    assert "## reference: templates/recipe.md" not in out  # recipe template must not be present
    assert "## reference: recipe-quality/source-fidelity.md" in out
    assert "## source: web/components/Button.tsx (web)" in out
    assert "## source: apple/UI/Button.swift (apple)" in out
    assert "## existing recipe: recipes/button.md" in out
    assert "Source platforms\npresent: apple, web" in out or "present: apple, web" in out


def test_extract_alias_pulls_alias_sources_too(mini_repo, extract_refs, capsys):
    assert main(["-p", str(mini_repo), "prompt", "extract", "toolbar-button"]) == 0
    out = capsys.readouterr().out
    assert "## source: apple/UI/ToolbarButton.swift (apple)" in out
    assert "recipes/button.md" in out          # alias resolves to the button recipe


def test_extract_gathers_every_source_for_the_slug(mini_repo, extract_refs, capsys):
    """One slug, one prompt, all of its sources — however they are reached."""
    expected = [
        "apple/UI/Button.swift",
        "apple/UI/ToolbarButton.swift",
        "web/components/Button.tsx",
    ]
    assert main(["-p", str(mini_repo), "prompt", "extract", "button", "--json"]) == 0
    by_name = json.loads(capsys.readouterr().out)
    assert sorted(by_name["sources"]) == expected

    assert main(["-p", str(mini_repo), "prompt", "extract", "toolbar-button", "--json"]) == 0
    by_alias = json.loads(capsys.readouterr().out)
    assert sorted(by_alias["sources"]) == expected

    assert by_name["recipe_path"] == by_alias["recipe_path"] == "recipes/button.md"
    assert by_name["name"] == "button"          # the requested name is preserved
    assert by_alias["name"] == "toolbar-button"


def test_extract_missing_component_exits_2(mini_repo, extract_refs, capsys):
    assert main(["-p", str(mini_repo), "prompt", "extract", "nope"]) == 2


def test_extract_json_reports_paths(mini_repo, extract_refs, capsys):
    assert main(["-p", str(mini_repo), "prompt", "extract", "chat-composer", "--json"]) == 0
    data = json.loads(capsys.readouterr().out)
    assert data["recipe_path"] == "recipes/chat-composer.md"
    assert data["sources"] == ["web/components/chat-composer.tsx"]
    assert "prompt" in data


def test_extract_type_recipe_uses_recipe_template(mini_repo, extract_refs, capsys):
    assert main(["-p", str(mini_repo), "prompt", "extract", "stat-card", "--type", "recipe"]) == 0
    out = capsys.readouterr().out
    assert "Write the **recipe** recipe" in out
    assert "## reference: templates/recipe.md" in out
    assert "## reference: templates/ingredient.md" not in out  # ingredient template must not be present
