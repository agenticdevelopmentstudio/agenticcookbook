import pytest

from cookr.cli import main
from cookr.core.frontmatter import parse


# Every tmp_path here is a git repo, as a real cookbook checkout is.
pytestmark = pytest.mark.usefixtures("git_tmp_path")


def test_update_fills_a_converted_artifact_in_its_folder(tmp_path, monkeypatch, patch_refs):
    monkeypatch.chdir(tmp_path)
    assert main(["create"]) == 0
    cb = tmp_path / "cookbook"
    (cb / "recipes" / "alpha.md").write_text(
        "---\ntitle: Alpha\ntype: recipe\n---\n# Alpha\n\n## Change History\n\nx\n", encoding="utf-8")
    assert main(["convert", str(cb / "recipes" / "alpha.md")]) == 0
    assert main(["update", "-p", str(cb), "--author", "Tester"]) == 0
    folder = cb / "recipes" / "alpha"
    assert '"author": "Tester"' in (folder / "artifact.json").read_text()
    assert parse((cb / "recipes" / "alpha.md").read_text()).data["author"] == "Tester"
    assert main(["compile", "--check", str(folder)]) == 0
    index = (cb / "recipes" / "INDEX.md").read_text()
    assert "Alpha" in index and "intro" not in index.lower()  # parts are not indexed


def test_update_fills_frontmatter_and_regenerates_index(tmp_path, monkeypatch, patch_refs):
    monkeypatch.chdir(tmp_path)
    assert main(["create"]) == 0
    cb = tmp_path / "cookbook"
    (cb / "recipes" / "alpha.md").write_text("# Alpha Recipe\n", encoding="utf-8")
    (cb / "recipes" / "beta.md").write_text(
        "---\ntitle: Already Set\nid: 11111111-2222-3333-4444-555555555555\n---\n# Beta\n",
        encoding="utf-8",
    )

    assert main(["update", "-p", str(cb), "--author", "Tester"]) == 0

    alpha_fm = parse((cb / "recipes" / "alpha.md").read_text())
    assert alpha_fm.had_frontmatter
    assert alpha_fm.data["title"] == "Alpha Recipe"
    assert alpha_fm.data["type"] == "recipe"
    assert alpha_fm.data["author"] == "Tester"

    beta_fm = parse((cb / "recipes" / "beta.md").read_text())
    assert beta_fm.data["title"] == "Already Set"  # preserved
    assert beta_fm.data["id"] == "11111111-2222-3333-4444-555555555555"  # preserved

    index = (cb / "recipes" / "INDEX.md").read_text()
    assert "Alpha Recipe" in index
    assert "Already Set" in index
