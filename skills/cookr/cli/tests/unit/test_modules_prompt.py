"""`cookr prompt extract` assembles module + references + action + sources + existing recipe."""

from __future__ import annotations

import json
import re
from pathlib import Path

import pytest

from cookbook.core.manifest import materialize

from cookr.cli import main
from cookr.core import templates
from cookr.modules.prompt import prompt_cli


REPO_ROOT = Path(__file__).resolve().parents[5]
MANIFEST = prompt_cli.EXTRACT_DIR / "reference-manifest.json"


@pytest.fixture
def extract_refs(monkeypatch, tmp_path):
    """The extract manifest materialised from this checkout, as install.sh would."""
    dest = tmp_path / "references"
    materialize(MANIFEST, REPO_ROOT, dest)
    monkeypatch.setattr(prompt_cli, "references_dir", lambda: dest)
    return dest


def test_prompt_lists_actions(capsys):
    assert main(["prompt"]) == 0
    assert "extract" in capsys.readouterr().out


def test_extract_includes_sources_and_existing_recipe(mini_repo, extract_refs, capsys):
    # "button" is a shorthand: it is the unique spec name ending in `/button`.
    assert main(["-p", str(mini_repo), "prompt", "extract", "button"]) == 0
    out = capsys.readouterr().out
    assert "You are a component specification writer." in out
    assert "## reference: templates/ingredient.md" in out
    assert "## reference: templates/recipe.md" not in out  # recipe template must not be present
    assert "## reference: guidelines/recipe-quality/source-fidelity.md" in out
    assert "## source: web/components/Button.tsx (web)" in out
    assert "## source: apple/UI/Button.swift (apple)" in out
    assert "## existing recipe: cookbook/components/button.md" in out
    assert "Source platforms present: apple, web." in out


def test_extract_gathers_every_source_for_a_whole_directory_claim(mini_repo, extract_refs, capsys):
    """One name, one prompt, all of its sources - however the claim reaches them.

    `components/button.md` claims the whole `apple/UI/` directory, so
    `ToolbarButton.swift` is one more source under `components/button`, not a
    separate name (the old model's aliases don't exist here).
    """
    expected = [
        "apple/UI/Button.swift",
        "apple/UI/ToolbarButton.swift",
        "web/components/Button.tsx",
    ]
    assert main(["-p", str(mini_repo), "prompt", "extract", "button", "--json"]) == 0
    data = json.loads(capsys.readouterr().out)
    assert sorted(data["sources"]) == expected
    assert data["recipe_path"] == "cookbook/components/button.md"
    assert data["name"] == "components/button"  # the resolved name, not the shorthand asked for


def test_extract_ambiguous_shorthand_lists_every_candidate(mini_repo, extract_refs, capsys):
    lib = mini_repo / "python" / "widgets"
    lib.mkdir(parents=True)
    (lib / "button.py").write_text("class Button:\n    pass\n", encoding="utf-8")
    p = mini_repo / "cookbook" / "cookbook.json"
    data = json.loads(p.read_text(encoding="utf-8"))
    data["code"]["roots"].append({"path": "python/widgets", "platform": "python", "recipes": "engine"})
    p.write_text(json.dumps(data), encoding="utf-8")
    assert main(["-p", str(mini_repo), "prompt", "extract", "button"]) == 2
    out = capsys.readouterr().out
    assert "names several components" in out
    assert "components/button" in out
    assert "engine/button" in out


def test_extract_missing_component_exits_2(mini_repo, extract_refs, capsys):
    assert main(["-p", str(mini_repo), "prompt", "extract", "nope"]) == 2


def test_extract_json_reports_paths(mini_repo, extract_refs, capsys):
    assert main(["-p", str(mini_repo), "prompt", "extract", "chat-composer", "--json"]) == 0
    data = json.loads(capsys.readouterr().out)
    assert data["recipe_path"] == "cookbook/components/chat-composer.md"
    assert data["domain"] == "mini-repo://cookbook/components/chat-composer"
    assert "`domain` is exactly `mini-repo://cookbook/components/chat-composer`" in data["prompt"]
    assert data["sources"] == ["web/components/chat-composer.tsx"]
    assert "prompt" in data


def _retype_stat_card(mini_repo, rtype):
    p = mini_repo / "cookbook" / "blocks" / "stat-card.md"
    p.write_text(
        p.read_text(encoding="utf-8").replace("type: ingredient", f"type: {rtype}", 1),
        encoding="utf-8",
    )


def test_type_defaults_to_the_existing_recipes_type(mini_repo, extract_refs, capsys):
    _retype_stat_card(mini_repo, "recipe")
    assert main(["-p", str(mini_repo), "prompt", "extract", "stat-card"]) == 0
    out = capsys.readouterr().out
    assert "## reference: templates/recipe.md" in out
    assert "## reference: templates/ingredient.md" not in out
    assert "Write the **recipe** recipe" in out


def test_explicit_type_overrides_the_existing_recipes_type(mini_repo, extract_refs, capsys):
    _retype_stat_card(mini_repo, "recipe")
    assert main(["-p", str(mini_repo), "prompt", "extract", "stat-card",
                 "--type", "ingredient"]) == 0
    out = capsys.readouterr().out
    assert "## reference: templates/ingredient.md" in out
    assert "## reference: templates/recipe.md" not in out


def test_type_defaults_to_ingredient_without_an_existing_recipe(mini_repo, extract_refs, capsys):
    (mini_repo / "cookbook" / "components" / "chat-composer.md").unlink()
    assert main(["-p", str(mini_repo), "prompt", "extract", "chat-composer", "--json"]) == 0
    assert json.loads(capsys.readouterr().out)["type"] == "ingredient"


def test_extract_type_recipe_uses_recipe_template(mini_repo, extract_refs, capsys):
    assert main(["-p", str(mini_repo), "prompt", "extract", "stat-card", "--type", "recipe"]) == 0
    out = capsys.readouterr().out
    assert "Write the **recipe** recipe" in out
    assert "## reference: templates/recipe.md" in out
    assert "## reference: templates/ingredient.md" not in out  # ingredient template must not be present


def _add_logic_root(repo):
    lib = repo / "python" / "lib"
    lib.mkdir(parents=True)
    (lib / "session_store.py").write_text("class SessionStore:\n    pass\n", encoding="utf-8")
    p = repo / "cookbook" / "cookbook.json"
    data = json.loads(p.read_text(encoding="utf-8"))
    data["code"]["roots"].append({"path": "python/lib", "platform": "python", "kind": "logic",
                                  "recipes": "engine"})
    p.write_text(json.dumps(data), encoding="utf-8")


def test_extract_logic_component_carries_non_ui_guidance(mini_repo, extract_refs, capsys):
    _add_logic_root(mini_repo)
    # No spec claims `python/lib/`, so the source falls back to its arrangement
    # name `engine/session-store`; "session-store" resolves to it uniquely.
    assert main(["-p", str(mini_repo), "prompt", "extract", "session-store", "--json"]) == 0
    data = json.loads(capsys.readouterr().out)
    assert data["name"] == "engine/session-store"
    assert data["kind"] == "logic"
    assert data["platforms"] == ["python"]
    assert "## non-UI component" in data["prompt"]
    assert "## source: python/lib/session_store.py (python)" in data["prompt"]
    # UI design-language guidance is noise for a non-UI brief
    assert "platform-design-languages.md" not in data["prompt"]
    assert "behavioral-requirements.md" in data["prompt"]


def test_extract_ui_component_omits_non_ui_guidance(mini_repo, extract_refs, capsys):
    _add_logic_root(mini_repo)
    assert main(["-p", str(mini_repo), "prompt", "extract", "button", "--json"]) == 0
    data = json.loads(capsys.readouterr().out)
    assert data["kind"] == "ui"
    assert "## non-UI component" not in data["prompt"]
    assert "## reference: guidelines/platform-design-languages.md" in data["prompt"]


def test_module_example_requirement_name_is_subject_only():
    body = (prompt_cli.PROMPTS_DIR / "extract" / "module.md").read_text(encoding="utf-8")
    assert "**must-" not in body
    assert 'role: "component specification writer"' in body


def test_extract_lists_the_compliance_catalog(mini_repo, extract_refs, capsys):
    assert main(["-p", str(mini_repo), "prompt", "extract", "button"]) == 0
    out = capsys.readouterr().out
    assert "## reference: compliance checks" in out
    assert "`best-practices`:" in out and "unit-test-coverage" in out


# ---- review fixes -------------------------------------------------------------------------

_FENCE_LINE = re.compile(r"^(`{3,})(.*)$")


def _top_level_h2(text: str) -> list[str]:
    """`## ` headings outside CommonMark backtick fences, in order."""
    out, fence = [], None
    for line in text.splitlines():
        m = _FENCE_LINE.match(line)
        if fence is not None:
            if m and len(m.group(1)) >= len(fence) and not m.group(2).strip():
                fence = None
        elif m:
            fence = m.group(1)
        elif line.startswith("## "):
            out.append(line)
    assert fence is None, "a fence is still open at the end of the brief"
    return out


def test_fenced_outruns_every_backtick_run_inside():
    assert prompt_cli.fenced("plain") == "```\nplain\n```"
    assert prompt_cli.fenced("a\n```\nb\n```", "markdown").startswith("````markdown\n")
    assert prompt_cli.fenced("x ````` y").endswith("\n``````")


def test_embedded_recipe_and_source_fences_stay_inside(mini_repo, extract_refs, capsys):
    recipe = mini_repo / "cookbook" / "components" / "button.md"
    recipe.write_text(recipe.read_text(encoding="utf-8")
                      + "\n```\n## Not A Brief Section\n```\n", encoding="utf-8")
    src = mini_repo / "web" / "components" / "Button.tsx"
    src.write_text(src.read_text(encoding="utf-8") + "\n/*\n```\n## Also Not\n*/\n", encoding="utf-8")
    assert main(["-p", str(mini_repo), "prompt", "extract", "button"]) == 0
    headings = _top_level_h2(capsys.readouterr().out)
    assert "## Not A Brief Section" not in headings
    assert "## Also Not" not in headings
    assert headings[-1] == "## existing recipe: cookbook/components/button.md"


def test_template_and_guidelines_sit_above_the_action_that_points_at_them(
        mini_repo, extract_refs, capsys):
    assert main(["-p", str(mini_repo), "prompt", "extract", "button"]) == 0
    out = capsys.readouterr().out
    pointer = out.index("template under `## reference: templates/ingredient.md` above")
    assert out.index("## reference: templates/ingredient.md\n") < pointer
    assert out.index("## reference: guidelines/") < pointer
    assert pointer < out.index("## Your task") < out.index("## source: ")
    assert not re.search(r"^## reference: (?!guidelines/|templates/|compliance checks)", out, re.M)


def test_guidelines_keep_their_domain_and_drop_other_metadata(mini_repo, extract_refs, capsys):
    assert main(["-p", str(mini_repo), "prompt", "extract", "button"]) == 0
    out = capsys.readouterr().out
    head = "## reference: guidelines/recipe-quality/source-fidelity.md\n\n"
    chunk = out[out.index(head) + len(head):]
    chunk = chunk[:chunk.index("\n## reference: ")]
    assert chunk.startswith("Cite as `agenticdevelopercookbook://guidelines/")
    assert "approved-by:" not in chunk and "copyright:" not in chunk
    assert "## Change History" not in chunk
    assert "## " in chunk  # the guideline's own sections are still there


def test_nested_recipe_is_rewritten_where_it_lives(mini_repo, extract_refs, capsys):
    # Moving a spec file changes its name too: name is its cookbook-relative
    # path without `.md`. The claim on `apple/UI/` (and the file's own
    # `web/components/Button.tsx` row) travels with it unchanged.
    (mini_repo / "cookbook" / "components" / "ui").mkdir()
    (mini_repo / "cookbook" / "components" / "button.md").rename(
        mini_repo / "cookbook" / "components" / "ui" / "button.md")
    assert main(["-p", str(mini_repo), "prompt", "extract", "button", "--json"]) == 0
    data = json.loads(capsys.readouterr().out)
    assert data["name"] == "components/ui/button"
    assert data["recipe_path"] == "cookbook/components/ui/button.md"
    assert data["domain"] == "mini-repo://cookbook/components/ui/button"
    assert Path(data["recipe_file"]) == mini_repo.resolve() / "cookbook" / "components" / "ui" / "button.md"
    assert "## existing recipe: cookbook/components/ui/button.md" in data["prompt"]


def test_brief_names_the_absolute_file_to_write(mini_repo, extract_refs, capsys):
    assert main(["-p", str(mini_repo), "prompt", "extract", "chat-composer", "--json"]) == 0
    data = json.loads(capsys.readouterr().out)
    assert Path(data["recipe_file"]).is_absolute()
    assert f"Save the result to `{data['recipe_file']}`" in data["prompt"]


def test_extract_reads_the_resolved_components_own_recipe(mini_repo, extract_refs, capsys):
    # A single-name `extract` still needs the whole corpus once: resolving a
    # shorthand name and each spec's claims requires seeing every spec's
    # Reference Implementations, not just the requested one. (The old model's
    # "single-brief extract must not parse the whole corpus" optimization no
    # longer applies now that ownership is claim-based across the corpus.) The
    # invariant that still holds is that the *embedded existing recipe* is the
    # resolved component's own file, not some other spec's.
    assert main(["-p", str(mini_repo), "prompt", "extract", "stat-card"]) == 0
    assert "## existing recipe: cookbook/blocks/stat-card.md" in capsys.readouterr().out


def test_template_is_the_cookbook_packages_copy(mini_repo, extract_refs, capsys):
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    assert not [e for e in manifest["files"] if e["dst"].startswith("templates/")]
    assert main(["-p", str(mini_repo), "prompt", "extract", "button", "--json"]) == 0
    assert json.loads(capsys.readouterr().out)["template"] == str(templates.template_path("ingredient"))


def test_unknown_action_is_rejected_by_the_parser(capsys):
    with pytest.raises(SystemExit) as e:
        main(["prompt", "bogus"])
    assert e.value.code == 2


def test_name_and_tier_are_exclusive_and_tier_needs_out_dir(mini_repo, extract_refs, tmp_path):
    root = str(mini_repo)
    assert main(["-p", root, "prompt", "extract"]) == 2
    assert main(["-p", root, "prompt", "extract", "button", "--tier", "ui",
                 "--out-dir", str(tmp_path)]) == 2
    assert main(["-p", root, "prompt", "extract", "--tier", "ui"]) == 2
    assert main(["-p", root, "prompt", "extract", "--tier", "nope", "--out-dir", str(tmp_path)]) == 2


def _mark_button_for_review(mini_repo):
    p = mini_repo / "cookbook" / "components" / "button.md"
    p.write_text(p.read_text(encoding="utf-8").replace(
        "Button must respond to click events.\n",
        "Button must respond to click events.\n\n"
        "- **focus-ring**: NEEDS REVIEW: Not implemented in source. No focus style.\n", 1),
        encoding="utf-8")


def _tier(mini_repo, tier, out_dir, capsys):
    assert main(["-p", str(mini_repo), "prompt", "extract", "--tier", tier,
                 "--out-dir", str(out_dir), "--json"]) == 0
    return json.loads(capsys.readouterr().out)


def test_tier_worklist_writes_one_brief_per_recipe_still_to_write(
        mini_repo, extract_refs, capsys, tmp_path):
    data = _tier(mini_repo, "components", tmp_path / "briefs", capsys)
    assert Path(data["repo_root"]) == mini_repo.resolve()
    assert Path(data["cookbook_dir"]) == mini_repo.resolve() / "cookbook"
    assert [w["name"] for w in data["write"]] == ["components/chat-composer"]  # button is complete
    brief = Path(data["write"][0]["brief"])
    assert brief == (tmp_path / "briefs" / "components" / "chat-composer.md").resolve()
    assert "Produce `" in brief.read_text(encoding="utf-8")
    assert data["awaiting_review"] == []


def test_tier_worklist_leaves_marker_only_recipes_to_the_reviewer(
        mini_repo, extract_refs, capsys, tmp_path):
    _mark_button_for_review(mini_repo)
    data = _tier(mini_repo, "components", tmp_path, capsys)
    assert data["awaiting_review"] == [
        {"name": "components/button", "recipe_path": "cookbook/components/button.md"}]
    # chat-composer has plenty of its own problems (none of them the marker
    # alone), so it still goes out to a writer.
    assert [w["name"] for w in data["write"]] == ["components/chat-composer"]
    assert not (tmp_path / "components" / "button.md").exists()


def test_tier_worklist_splits_into_arrangement_names_once_the_spec_is_gone(
        mini_repo, extract_refs, capsys, tmp_path):
    # No aliases in the new model: deleting the spec that claimed the whole
    # `apple/UI/` directory just drops the claim, so each source falls back to
    # its own arrangement-derived name under the `ui` root's group, rather than
    # being deduped into one name the way a rename-based alias used to be.
    (mini_repo / "cookbook" / "components" / "button.md").unlink()
    data = _tier(mini_repo, "ui", tmp_path, capsys)
    assert sorted(w["name"] for w in data["write"]) == ["ui/button", "ui/toolbar-button"]
    names_and_paths = {w["name"]: w["sources"] for w in data["write"]}
    assert names_and_paths["ui/button"] == ["apple/UI/Button.swift"]
    assert names_and_paths["ui/toolbar-button"] == ["apple/UI/ToolbarButton.swift"]


def test_templates_name_requirements_by_subject_only():
    for rtype in templates.TYPES:
        text = templates.template_path(rtype).read_text(encoding="utf-8")
        assert not re.search(r"\*\*(must|should|may)-", text, re.I), rtype
        assert not re.search(r"\| (must|should|may)-", text, re.I), rtype
