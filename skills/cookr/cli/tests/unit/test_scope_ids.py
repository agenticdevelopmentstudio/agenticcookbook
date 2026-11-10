"""`cookr scope`: ids, unresolvable links, base fallback and `--since`."""

from __future__ import annotations

import json

from cookr.cli import main
from cookr.core.changes import Change

from .cookbook_helpers import add_spec, edit_repo_config
from .test_scope import FOREIGN, PANEL_S, _git, _rdids, _repo, _scope


def test_ids_seed_the_scope_and_mix_with_paths(tmp_path, capsys):
    repo = _repo(tmp_path)
    assert main(["-p", str(repo), "scope", "test-repo.recipe.ui.safari", "--json"]) == 0
    data = json.loads(capsys.readouterr().out)
    assert [i["rdid"] for i in data["minimum"]] == [
        "test-repo.recipe.ui.safari", "test-repo.ingredient.ui.abstract"]
    assert [i["rdid"] for i in data["further"]] == ["test-repo.ingredient.ui.deep"]
    assert main(["-p", str(repo), "scope", PANEL_S.upper(), "web/stray.ts", "--json"]) == 0
    data = json.loads(capsys.readouterr().out)
    assert "test-repo.recipe.ui.safari" in [i["rdid"] for i in data["minimum"]]
    assert data["uncovered"] == ["web/stray.ts"]


def test_planned_new_files_named_like_rdids_are_paths(tmp_path, capsys):
    repo = _repo(tmp_path)
    for name in ("setup.py", "foo.ts"):
        assert main(["-p", str(repo), "scope", name]) == 0     # a planned add, outside the roots
        assert f"{name}: not under any code root" in " ".join(capsys.readouterr().out.split())


def test_explicit_path_outside_every_root_warns(tmp_path, capsys):
    repo = _repo(tmp_path)
    assert main(["-p", str(repo), "scope", "test-repo.recipe.ui.nope", "--json"]) == 0
    out = " ".join(capsys.readouterr().out.split())
    assert "test-repo.recipe.ui.nope: not under any code root (or an unknown id)" in out
    assert main(["-p", str(repo), "scope", "web/new.ts", "--json"]) == 0
    assert "not under any code root" not in capsys.readouterr().out


def test_uuid_shaped_unknown_is_an_error(tmp_path):
    repo = _repo(tmp_path)
    assert main(["-p", str(repo), "scope", "11111111-2222-4333-8444-555555555555"]) == 2


def test_id_of_a_guideline_warns_and_seeds_nothing(tmp_path, capsys):
    repo = _repo(tmp_path)
    assert main(["-p", str(repo), "scope", "test-repo.guideline.ui.guide", "--json"]) == 0
    out = " ".join(capsys.readouterr().out.split())
    assert "is a guideline; scope walks only recipes and ingredients" in out
    assert '"minimum": []' in out


def test_malformed_dependency_link_is_unresolvable(tmp_path):
    repo = _repo(tmp_path)
    add_spec(repo, "ui/bad", type="recipe", impls=[("web", "web/stray.ts")],
             meta={"depends-on": ["not a link"]})
    s = _scope(repo, Change("M", "web/stray.ts"))
    item = next(i for i in s.minimum if i.state == "unresolvable")
    assert item.rdid == "not a link" and item.via == "test-repo.recipe.ui.bad"


def test_dangling_dependency_is_missing_or_unreachable(tmp_path):
    repo = _repo(tmp_path)
    ghost = "88888888-0000-4000-8000-000000000008"
    add_spec(repo, "ui/dangling", type="recipe", impls=[("web", "web/stray.ts")],
             meta={"depends-on": [ghost, f"{FOREIGN}/{ghost}"]})
    s = _scope(repo, Change("M", "web/stray.ts"))
    states = {i.rdid: i.state for i in s.minimum}
    assert states[ghost] == "missing"
    assert states[f"{FOREIGN}/{ghost}"] == "unreachable"


def test_cross_root_rename_with_both_sides_in_roots(tmp_path):
    repo = _repo(tmp_path)
    (repo / "lib").mkdir()
    (repo / "lib" / "safari.ts").write_text("export {}\n", encoding="utf-8")
    edit_repo_config(repo, lambda d: d["roots"].append(
        {"path": "lib", "platform": "web", "kind": "logic", "group": "logic"}))
    s = _scope(repo, Change("R", "lib/safari.ts", "web/safari.ts"))
    assert "test-repo.recipe.ui.safari" in _rdids(s.minimum)
    assert s.uncovered == []


def _commit_repo(repo):
    _git(repo, "init", "-q", "-b", "trunk")
    _git(repo, "config", "user.email", "t@example.com")
    _git(repo, "config", "user.name", "T")
    _git(repo, "add", "-A")
    _git(repo, "commit", "-q", "-m", "base")


def test_no_base_counts_unstaged_edits_to_tracked_files(tmp_path, capsys):
    repo = _repo(tmp_path)
    _commit_repo(repo)
    (repo / "web" / "safari.ts").write_text("export const a = 2\n", encoding="utf-8")   # unstaged
    assert main(["-p", str(repo), "scope", "--json"]) == 0
    out = capsys.readouterr().out
    assert "no base branch" in out
    assert "test-repo.recipe.ui.safari" in out


def test_unborn_head_falls_back_to_staged_and_untracked(tmp_path, capsys):
    repo = _repo(tmp_path)
    _git(repo, "init", "-q", "-b", "trunk")
    _git(repo, "add", "web/safari.ts")
    assert main(["-p", str(repo), "scope", "--json"]) == 0
    assert "test-repo.recipe.ui.safari" in capsys.readouterr().out


def test_since_ref(tmp_path, capsys):
    repo = _repo(tmp_path)
    _commit_repo(repo)
    (repo / "web" / "chrome.ts").write_text("export const c = 1\n", encoding="utf-8")
    _git(repo, "commit", "-q", "-am", "chrome")
    assert main(["-p", str(repo), "scope", "--since", "HEAD~1", "--json"]) == 0
    data = json.loads(capsys.readouterr().out)
    assert [i["rdid"] for i in data["minimum"]][0] == "test-repo.recipe.ui.chrome"
    assert main(["-p", str(repo), "scope", "--since", "nonexistent-ref"]) == 1
