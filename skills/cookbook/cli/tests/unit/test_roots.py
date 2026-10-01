from pathlib import Path

from cookbook.core import roots


def _make(root: Path, subdirs: list[str], with_index: bool = True) -> Path:
    root.mkdir(parents=True, exist_ok=True)
    if with_index:
        (root / "index.md").write_text("", encoding="utf-8")
    for s in subdirs:
        (root / s).mkdir(parents=True, exist_ok=True)
    return root


def test_child_match(tmp_path):
    cookbook = tmp_path / "cookbook"
    _make(cookbook, ["recipes", "reference"])
    assert roots.resolve(tmp_path) == cookbook


def test_walk_up_match(tmp_path):
    cookbook = tmp_path / "myproject" / "cookbook"
    _make(cookbook, ["recipes"])
    deep = cookbook / "recipes"
    assert roots.resolve(deep) == cookbook


def test_no_match_returns_none(tmp_path):
    (tmp_path / "scratch").mkdir()
    assert roots.resolve(tmp_path) is None


def test_explicit_path_wins(tmp_path):
    a = tmp_path / "a"; _make(a, ["recipes"])
    b = tmp_path / "b"; _make(b, ["recipes"])
    assert roots.resolve(a, b) == b.resolve()


def test_requires_canonical_subdir(tmp_path):
    """An index.md alone isn't enough — needs a canonical subdir."""
    (tmp_path / "index.md").write_text("", encoding="utf-8")
    assert roots.resolve(tmp_path) is None


def test_manifest_marks_a_library_cookbook(tmp_path):
    """A library cookbook has cookbook.json and group directories, no canonical subdirs."""
    cookbook = tmp_path / "cookbook"
    (cookbook / "ai-plugin-kit").mkdir(parents=True)
    (cookbook / "cookbook.json").write_text("{}", encoding="utf-8")
    assert roots.resolve(tmp_path) == cookbook
    assert roots.resolve(cookbook / "ai-plugin-kit") == cookbook
