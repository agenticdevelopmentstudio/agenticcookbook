"""`cookr scope`: the minimum, further, siblings and uncovered files."""

from __future__ import annotations

import json
import subprocess

from cookr.cli import main
from cookr.core.changes import Change
from cookr.core.identity import read_manifest
from cookr.core.index import Entry, Index, current_index, save_index
from cookr.core.links import resolver_for
from cookr.core.repoconfig import load_repo_config
from cookr.core.scope import compute

from .cookbook_helpers import add_spec, edit_repo_config, new_repo

ROOT = {"path": "web", "platform": "web", "kind": "ui", "group": "ui"}
FOREIGN = "f0000000-0000-4000-8000-000000000000"
ABSTRACT = "a0000000-0000-4000-8000-000000000001"
PANEL_S = "a0000000-0000-4000-8000-000000000002"
PANEL_C = "a0000000-0000-4000-8000-000000000003"
GUIDE = "a0000000-0000-4000-8000-000000000004"
DEEP = "a0000000-0000-4000-8000-000000000005"


def _files(repo, *names):
    for n in names:
        (repo / "web" / n).write_text("export {}\n", encoding="utf-8")


def _repo(tmp_path):
    repo = new_repo(tmp_path / "r", [ROOT])
    _files(repo, "safari.ts", "chrome.ts", "abstract.ts", "stray.ts")
    add_spec(repo, "ui/deep", type="ingredient", artifact_id=DEEP)
    add_spec(repo, "ui/abstract", type="ingredient", artifact_id=ABSTRACT,
             meta={"depends-on": [DEEP]}, impls=[("web", "web/abstract.ts")])
    add_spec(repo, "ui/guide", type="guideline", artifact_id=GUIDE)
    add_spec(repo, "ui/safari", type="recipe", artifact_id=PANEL_S,
             meta={"depends-on": [ABSTRACT, GUIDE]}, impls=[("web", "web/safari.ts")])
    add_spec(repo, "ui/chrome", type="recipe", artifact_id=PANEL_C,
             meta={"depends-on": [ABSTRACT, GUIDE]}, impls=[("web", "web/chrome.ts")])
    return repo


def _scope(repo, *changes):
    cfg = load_repo_config(repo)
    index = current_index(cfg.cookbook_dir)
    return compute(cfg, index, resolver_for(cfg, index), list(changes))


def _rdids(items):
    return [i.rdid for i in items]


def test_minimum_is_owner_plus_direct_deps(tmp_path):
    s = _scope(_repo(tmp_path), Change("M", "web/safari.ts"))
    assert _rdids(s.minimum) == ["test-repo.recipe.ui.safari", "test-repo.ingredient.ui.abstract"]
    assert s.minimum[0].via is None
    assert s.minimum[1].via == "test-repo.recipe.ui.safari"
    assert s.minimum[0].state == "unverified"
    assert _rdids(s.further) == ["test-repo.ingredient.ui.deep"]
    assert s.further[0].via == "test-repo.ingredient.ui.abstract"


def test_guidelines_never_walked(tmp_path):
    s = _scope(_repo(tmp_path), Change("M", "web/safari.ts"))
    everything = s.minimum + s.further + s.siblings
    assert all("guideline" not in i.rdid for i in everything)


def test_siblings_share_a_direct_dep(tmp_path):
    s = _scope(_repo(tmp_path), Change("M", "web/safari.ts"))
    assert _rdids(s.siblings) == ["test-repo.recipe.ui.chrome"]
    assert s.siblings[0].via == "test-repo.ingredient.ui.abstract"


def test_uncovered_touched_file_listed(tmp_path):
    repo = _repo(tmp_path)
    (repo / "outside.txt").write_text("x", encoding="utf-8")
    (repo / "web" / "new.ts").write_text("export {}\n", encoding="utf-8")
    s = _scope(repo, Change("A", "web/new.ts"), Change("M", "outside.txt"),
               Change("D", "web/safari.ts"))
    assert s.uncovered == ["web/new.ts"]
    assert "test-repo.recipe.ui.safari" in _rdids(s.minimum)   # a deletion still maps to its owner


def test_frozen_version_files_are_not_implementation(tmp_path):
    repo = _repo(tmp_path)
    s = _scope(repo, Change("M", "cookbook/ui/safari/versions/1.0.0/overview.md"))
    assert s.minimum == [] and s.uncovered == []


def test_rename_within_root_uses_old_owner(tmp_path):
    repo = _repo(tmp_path)
    (repo / "web" / "safari2.ts").write_text("export {}\n", encoding="utf-8")
    s = _scope(repo, Change("R", "web/safari2.ts", "web/safari.ts"))
    assert "test-repo.recipe.ui.safari" in _rdids(s.minimum)
    assert s.uncovered == []


def test_foreign_dependency_in_minimum(tmp_path):
    repo = _repo(tmp_path)
    fid = "f1111111-0000-4000-8000-000000000001"
    fcb = repo / "ext" / "cookbook"
    fcb.mkdir(parents=True)
    (fcb / "cookbook.json").write_text(
        json.dumps({"format": 2, "id": FOREIGN, "rdid": "ext"}), encoding="utf-8")
    fidx = Index(cookbook=read_manifest(fcb))
    fidx.entries[fid] = Entry(id=fid, kind="ingredient", rdid="ext.ingredient.net", path="net")
    save_index(fidx, fcb)
    edit_repo_config(repo, lambda d: d.setdefault("dependencies", {}).__setitem__(
        FOREIGN, {"rdid": "ext", "location": "ext/cookbook"}))
    gone = "99999999-0000-4000-8000-000000000009"
    add_spec(repo, "ui/net-user", type="recipe", impls=[("web", "web/stray.ts")],
             meta={"depends-on": [f"{FOREIGN}/{fid}", f"{gone}/{fid}"]})
    s = _scope(repo, Change("M", "web/stray.ts"))
    by = {i.rdid: i for i in s.minimum}
    assert by["ext.ingredient.net"].via == "test-repo.recipe.ui.net-user"
    assert by["ext.ingredient.net"].state == "unplaced"
    unreachable = by[f"{gone}/{fid}"]
    assert unreachable.state == "unreachable" and unreachable.via == "test-repo.recipe.ui.net-user"


def _git(repo, *args):
    subprocess.run(["git", "-C", str(repo), *args], check=True, capture_output=True)


def test_module_paths_json_and_text(tmp_path, capsys):
    repo = _repo(tmp_path)
    assert main(["-p", str(repo), "scope", "web/safari.ts", "--json"]) == 0
    data = json.loads(capsys.readouterr().out)
    assert [i["rdid"] for i in data["minimum"]][0] == "test-repo.recipe.ui.safari"
    assert main(["-p", str(repo), "scope", "web/safari.ts"]) == 0
    out = capsys.readouterr().out
    assert out.index("minimum") < out.index("further") < out.index("siblings") < out.index("uncovered")
    assert "via test-repo.recipe.ui.safari" in out


def test_module_no_base_warns_and_git_failure_exits_1(tmp_path, capsys):
    repo = _repo(tmp_path)
    assert main(["-p", str(repo), "scope"]) == 1          # not a repo: an error, not "no changes"
    _git(repo, "init", "-q", "-b", "trunk")
    _git(repo, "config", "user.email", "t@example.com")
    _git(repo, "config", "user.name", "T")
    _git(repo, "add", "-A")
    _git(repo, "commit", "-q", "-m", "base")
    (repo / "web" / "safari.ts").write_text("export const a = 1\n", encoding="utf-8")
    _git(repo, "add", "web/safari.ts")
    capsys.readouterr()
    assert main(["-p", str(repo), "scope"]) == 0
    out = " ".join(capsys.readouterr().out.split())
    assert "no base branch" in out and "test-repo.recipe.ui.safari" in out
