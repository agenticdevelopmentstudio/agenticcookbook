from datetime import date

import pytest

from cookr.indexing import engine, flat, use_case, triggers


# Every tmp_path here is a git repo, as a real cookbook checkout is.
pytestmark = pytest.mark.usefixtures("git_tmp_path")


def _make_recipe(root, name, title="Recipe"):
    (root / "recipes").mkdir(parents=True, exist_ok=True)
    (root / "recipes" / name).write_text(
        f"---\ntitle: {title}\n---\n# {title}\n", encoding="utf-8",
    )


def test_flat_strategy(tmp_path):
    root = tmp_path
    _make_recipe(root, "alpha.md", "Alpha")
    _make_recipe(root, "beta.md", "Beta")
    config = {
        "name": "recipes-flat",
        "strategy": "flat",
        "applies_when": {"path_exists": "recipes"},
        "target_dir": "recipes",
        "output": "recipes/INDEX.md",
        "title": "Recipes",
        "summary": "All recipes",
        "description": "Test",
    }
    text, counts = flat.generate(config, root, today=date(2026, 5, 15))
    assert "# Recipes" in text
    assert "[Alpha](alpha.md)" in text
    assert "[Beta](beta.md)" in text
    assert counts["total"] == 2


def test_engine_skips_missing_dir(tmp_path):
    root = tmp_path
    (root / "index.md").write_text("", encoding="utf-8")
    config = {
        "name": "guidelines",
        "strategy": "use_case",
        "applies_when": {"path_exists": "guidelines"},
        "target_dir": "guidelines",
        "output": "guidelines/INDEX.md",
        "use_cases": [],
    }
    r = engine.run_one(config, root)
    assert r.status == "skipped"
    assert "missing dir" in r.reason


def test_engine_writes_then_unchanged(tmp_path):
    root = tmp_path
    _make_recipe(root, "alpha.md", "Alpha")
    config = {
        "name": "recipes-flat",
        "strategy": "flat",
        "applies_when": {"path_exists": "recipes"},
        "target_dir": "recipes",
        "output": "recipes/INDEX.md",
        "title": "Recipes",
        "summary": "All recipes",
    }
    r1 = engine.run_one(config, root, today=date(2026, 5, 15))
    assert r1.status == "written"
    r2 = engine.run_one(config, root, today=date(2026, 5, 15))
    assert r2.status == "unchanged"


def test_a_new_day_alone_is_no_change(tmp_path):
    # Otherwise validate reports drift, and update rewrites every index,
    # each time the date rolls over.
    root = tmp_path
    _make_recipe(root, "alpha.md", "Alpha")
    config = {
        "name": "recipes-flat",
        "strategy": "flat",
        "target_dir": "recipes",
        "output": "recipes/INDEX.md",
        "title": "Recipes",
        "summary": "All recipes",
    }
    engine.run_one(config, root, today=date(2026, 5, 15))
    assert engine.run_one(config, root, today=date(2026, 5, 16)).status == "unchanged"
    assert "2026-05-15" in (root / "recipes" / "INDEX.md").read_text()
    _make_recipe(root, "beta.md", "Beta")
    assert engine.run_one(config, root, today=date(2026, 5, 16)).status == "written"
    assert "2026-05-16" in (root / "recipes" / "INDEX.md").read_text()


def test_triggers_strategy(tmp_path):
    root = tmp_path
    g = root / "guidelines" / "testing"
    g.mkdir(parents=True)
    (g / "test-pyramid.md").write_text(
        "---\ntitle: Test Pyramid\ntriggers:\n  - writing-tests\n---\n# x\n",
        encoding="utf-8",
    )
    (g / "stale.md").write_text(
        "---\ntitle: Stale\ntriggers:\n  - unknown-trigger\n---\n# y\n",
        encoding="utf-8",
    )
    config = {
        "name": "triggers",
        "strategy": "triggers",
        "applies_when": {"path_exists": "guidelines"},
        "target_dir": "guidelines",
        "output": "index/triggers.yaml",
        "canonical_triggers": ["writing-tests"],
    }
    text, counts = triggers.generate(config, root, today=date(2026, 5, 15))
    assert "writing-tests" in text
    assert counts["unique_triggers"] == 2
    assert any("unknown-trigger" in w for w in counts["warnings"])


def test_triggers_index_is_unchanged_on_a_second_run(tmp_path):
    # A wall-clock stamp in the output made every validate after an update drift.
    g = tmp_path / "guidelines"
    g.mkdir()
    (g / "a.md").write_text("---\ntitle: A\ntriggers:\n  - writing-tests\n---\n# a\n", encoding="utf-8")
    config = {
        "name": "triggers",
        "strategy": "triggers",
        "applies_when": {"path_exists": "guidelines"},
        "target_dir": "guidelines",
        "output": "index/triggers.yaml",
    }
    assert engine.run_one(config, tmp_path).status == "written"
    assert engine.run_one(config, tmp_path).status == "unchanged"
