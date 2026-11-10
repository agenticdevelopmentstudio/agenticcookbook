import json

import pytest

from cookr.cli import main


# Every tmp_path here is a git repo, as a real cookbook checkout is.
pytestmark = pytest.mark.usefixtures("git_tmp_path")


def test_create_v2_cookbook(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    assert main(["create", "--rdid", "adkitchen"]) == 0
    root = tmp_path / "cookbook"
    manifest = json.loads((root / "cookbook.json").read_text())
    assert manifest["format"] == 2 and manifest["rdid"] == "adkitchen"
    assert len(manifest["id"]) == 36
    index = json.loads((root / "index.json").read_text())
    assert index["format"] == 2 and index["entries"] == {}
    assert index["cookbook"] == {"id": manifest["id"], "rdid": "adkitchen"}
    assert sorted(p.name for p in root.iterdir()) == ["cookbook.json", "index.json"]


def test_create_is_idempotent_for_the_same_rdid(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    assert main(["create", "--rdid", "adkitchen"]) == 0
    before = (tmp_path / "cookbook" / "cookbook.json").read_text()
    assert main(["create", "--rdid", "adkitchen"]) == 0
    assert (tmp_path / "cookbook" / "cookbook.json").read_text() == before


def test_create_refuses_a_different_rdid(tmp_path, monkeypatch, capsys):
    monkeypatch.chdir(tmp_path)
    assert main(["create", "--rdid", "adkitchen"]) == 0
    before = (tmp_path / "cookbook" / "cookbook.json").read_text()
    assert main(["create", "--rdid", "other"]) == 1
    assert "adkitchen" in capsys.readouterr().out
    assert (tmp_path / "cookbook" / "cookbook.json").read_text() == before


def test_create_refuses_a_format_1_cookbook_and_points_at_upgrade(tmp_path, monkeypatch, capsys):
    monkeypatch.chdir(tmp_path)
    (tmp_path / "cookbook").mkdir()
    (tmp_path / "cookbook" / "cookbook.json").write_text('{"type": "cookbook", "name": "x"}')
    assert main(["create", "--rdid", "adkitchen"]) == 1
    assert "cookr upgrade" in capsys.readouterr().out


def test_create_refuses_a_bad_rdid(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    assert main(["create", "--rdid", "Bad_Name"]) == 1
    assert not (tmp_path / "cookbook").exists()


def test_create_in_a_parent_directory(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    assert main(["create", "--rdid", "adkitchen", "--in", str(tmp_path / "sub")]) == 0
    assert (tmp_path / "sub" / "cookbook" / "cookbook.json").is_file()


def test_create_with_p_makes_the_cookbook_in_that_repo_not_cwd(tmp_path, monkeypatch):
    repo, elsewhere = tmp_path / "repo", tmp_path / "elsewhere"
    repo.mkdir()
    elsewhere.mkdir()
    monkeypatch.chdir(elsewhere)
    assert main(["-p", str(repo), "create", "--rdid", "adkitchen"]) == 0
    assert (repo / "cookbook" / "cookbook.json").is_file()
    assert not (elsewhere / "cookbook").exists()
