import json

import pytest

from cookr.cli import main
from cookr.core.repoconfig import load_repo_config

pytestmark = pytest.mark.usefixtures("git_tmp_path")

DEP_ID = "9d02a1b4-1111-4222-8333-444455556666"
LOC = "external/adhsdk/cookbook"


def _dep(root, rdid="adhsdk", fmt=2):
    cb = root / LOC
    cb.mkdir(parents=True)
    if fmt == 2:
        (cb / "cookbook.json").write_text(json.dumps({"format": 2, "id": DEP_ID, "rdid": rdid}))
        (cb / "index.json").write_text(json.dumps(
            {"format": 2, "cookbook": {"id": DEP_ID, "rdid": rdid}, "entries": {}, "foreign": {}}))
    else:
        (cb / "cookbook.json").write_text(json.dumps({"type": "cookbook"}))
    return LOC


def _repo(tmp_path):
    (tmp_path / "App" / "Sources").mkdir(parents=True)
    return tmp_path


def test_adopt_writes_repo_config_with_dependency(tmp_path, monkeypatch, capsys):
    _repo(tmp_path)
    loc = _dep(tmp_path)
    monkeypatch.chdir(tmp_path)
    assert main(["adopt", "--rdid", "adkitchen", "--root", "App/Sources:macos:ui:app",
                 "--dependency", loc]) == 0
    cfg = load_repo_config(tmp_path)
    assert cfg.identity.rdid == "adkitchen"
    assert [(r.path, r.platform, r.kind, r.group) for r in cfg.roots] == [
        ("App/Sources", "macos", "ui", "app")]
    assert cfg.dependencies[DEP_ID].rdid == "adhsdk"
    assert cfg.dependencies[DEP_ID].location == loc
    assert "cookr status" in capsys.readouterr().out


def test_adopt_refuses_unknown_platform(tmp_path, monkeypatch, capsys):
    _repo(tmp_path)
    monkeypatch.chdir(tmp_path)
    assert main(["adopt", "--rdid", "adkitchen", "--root", "App/Sources:beos"]) == 2
    assert "beos" in capsys.readouterr().out
    assert not (tmp_path / ".cookr.json").exists()


def test_adopt_is_idempotent(tmp_path, monkeypatch):
    _repo(tmp_path)
    monkeypatch.chdir(tmp_path)
    args = ["adopt", "--rdid", "adkitchen", "--root", "App/Sources:macos"]
    assert main(args) == 0
    names = (".cookr.json", "cookbook/cookbook.json", "cookbook/index.json")
    before = [(tmp_path / n).read_text() for n in names]
    assert main(args) == 0
    assert [(tmp_path / n).read_text() for n in names] == before


def test_adopt_merges_additions_and_refuses_conflicts(tmp_path, monkeypatch, capsys):
    _repo(tmp_path)
    (tmp_path / "Web").mkdir()
    monkeypatch.chdir(tmp_path)
    assert main(["adopt", "--rdid", "adkitchen", "--root", "App/Sources:macos"]) == 0
    assert main(["adopt", "--rdid", "adkitchen", "--root", "App/Sources:macos",
                 "--root", "Web:web"]) == 0
    assert [r.path for r in load_repo_config(tmp_path).roots] == ["App/Sources", "Web"]
    before = (tmp_path / ".cookr.json").read_text()
    capsys.readouterr()
    assert main(["adopt", "--rdid", "adkitchen", "--root", "App/Sources:ios"]) == 1
    assert "App/Sources" in capsys.readouterr().out
    assert (tmp_path / ".cookr.json").read_text() == before


def test_adopt_unreadable_dependency_exits_2_naming_it(tmp_path, monkeypatch, capsys):
    _repo(tmp_path)
    monkeypatch.chdir(tmp_path)
    assert main(["adopt", "--rdid", "adkitchen", "--dependency", "nowhere/cookbook"]) == 2
    assert "nowhere/cookbook" in capsys.readouterr().out
    assert not (tmp_path / "cookbook").exists()


def test_adopt_a_format_1_dependency_without_an_id_exits_2(tmp_path, monkeypatch):
    _repo(tmp_path)
    loc = _dep(tmp_path, fmt=1)
    monkeypatch.chdir(tmp_path)
    assert main(["adopt", "--rdid", "adkitchen", "--dependency", loc]) == 2


def test_adopt_reads_a_format_1_dependency_through_derive_index(tmp_path, monkeypatch):
    _repo(tmp_path)
    cb = tmp_path / LOC
    cb.mkdir(parents=True)
    (cb / "cookbook.json").write_text(json.dumps({"id": DEP_ID, "rdid": "adhsdk"}))
    monkeypatch.chdir(tmp_path)
    assert main(["adopt", "--rdid", "adkitchen", "--dependency", LOC]) == 0
    data = json.loads((tmp_path / ".cookr.json").read_text())
    assert data["dependencies"] == {DEP_ID: {"rdid": "adhsdk", "location": LOC}}


def test_a_refused_adopt_leaves_nothing_behind(tmp_path, monkeypatch, capsys):
    _repo(tmp_path)
    monkeypatch.chdir(tmp_path)
    (tmp_path / ".cookr.json").write_text(json.dumps({"format": 2, "cookbook": "cookbook"}))
    # a config whose cookbook does not exist yet cannot be judged: nothing may be
    # created, and the refusal (bad input, exit 2) says what is wrong
    assert main(["adopt", "--rdid", "adkitchen", "--root", "App/Sources:macos"]) == 2
    assert "holds no cookbook" in " ".join(capsys.readouterr().out.split())
    assert not (tmp_path / "cookbook").exists()


def _adopted(tmp_path, monkeypatch, *extra):
    _repo(tmp_path)
    loc = _dep(tmp_path)
    monkeypatch.chdir(tmp_path)
    assert main(["adopt", "--rdid", "adkitchen", "--root", "App/Sources:macos",
                 "--dependency", loc, *extra]) == 0
    return loc


def test_adopt_refuses_a_conflicting_dependency(tmp_path, monkeypatch, capsys):
    loc = _adopted(tmp_path, monkeypatch)
    before = (tmp_path / ".cookr.json").read_text()
    other = tmp_path / "vendor" / "cookbook"
    other.mkdir(parents=True)
    (other / "cookbook.json").write_text(json.dumps({"format": 2, "id": DEP_ID, "rdid": "renamed"}))
    (other / "index.json").write_text(json.dumps(
        {"format": 2, "cookbook": {"id": DEP_ID, "rdid": "renamed"}, "entries": {}, "foreign": {}}))
    capsys.readouterr()
    assert main(["adopt", "--rdid", "adkitchen", "--dependency", "vendor/cookbook"]) == 1
    assert DEP_ID in capsys.readouterr().out
    assert (tmp_path / ".cookr.json").read_text() == before
    assert loc in before


def test_adopt_refuses_a_different_rdid_and_changes_nothing(tmp_path, monkeypatch, capsys):
    _adopted(tmp_path, monkeypatch)
    names = (".cookr.json", "cookbook/cookbook.json", "cookbook/index.json")
    before = [(tmp_path / n).read_text() for n in names]
    capsys.readouterr()
    assert main(["adopt", "--rdid", "other", "--root", "App/Sources:macos"]) == 1
    assert "adkitchen" in capsys.readouterr().out
    assert [(tmp_path / n).read_text() for n in names] == before


@pytest.mark.parametrize("text", ["[1]", "[]", "42", '"x"', "null"])
def test_adopt_a_cookbook_json_that_is_not_an_object_exits_2(tmp_path, monkeypatch, capsys, text):
    _repo(tmp_path)
    loc = _dep(tmp_path)
    (tmp_path / loc / "cookbook.json").write_text(text)
    monkeypatch.chdir(tmp_path)
    assert main(["adopt", "--rdid", "adkitchen", "--dependency", loc]) == 2
    assert loc in capsys.readouterr().out
    assert not (tmp_path / "cookbook").exists()


@pytest.mark.parametrize("text", ["[1]", "[]", "42", '"x"', "null"])
def test_adopt_a_format_1_dependency_ignores_a_non_object_index(
        tmp_path, monkeypatch, text):
    _repo(tmp_path)
    cb = tmp_path / LOC
    cb.mkdir(parents=True)
    (cb / "cookbook.json").write_text(json.dumps({"id": DEP_ID, "rdid": "adhsdk"}))
    (cb / "index.json").write_text(text)
    monkeypatch.chdir(tmp_path)
    # a format-1 manifest is derived from its folder; a stray non-object index.json is ignored
    assert main(["adopt", "--rdid", "adkitchen", "--dependency", LOC]) == 0


def test_adopt_with_p_targets_a_fresh_repo_from_elsewhere(tmp_path, monkeypatch, capsys):
    repo = tmp_path / "repo"
    _repo(repo)
    loc = _dep(repo)
    elsewhere = tmp_path / "elsewhere"
    elsewhere.mkdir()
    monkeypatch.chdir(elsewhere)
    assert main(["-p", str(repo), "adopt", "--rdid", "adkitchen", "--root", "App/Sources:macos",
                 "--dependency", loc]) == 0
    assert load_repo_config(repo).identity.rdid == "adkitchen"
    assert (repo / "cookbook" / "cookbook.json").is_file()
    assert not (elsewhere / ".cookr.json").exists()
    assert not (elsewhere / "cookbook").exists()


def test_adopt_with_p_naming_a_missing_directory_exits_2(tmp_path, monkeypatch, capsys):
    monkeypatch.chdir(tmp_path)
    assert main(["-p", str(tmp_path / "nowhere"), "adopt", "--rdid", "x"]) == 2
    assert "nowhere" in capsys.readouterr().out
