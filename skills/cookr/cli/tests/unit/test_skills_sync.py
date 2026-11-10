"""`cookr skills sync`: per-cookbook sets compiled on contact and registered with skill-router, scoped."""

from __future__ import annotations

import json
import shlex
import sys
from pathlib import Path

import pytest

from cookr.cli import main
from cookr.core import install as inst

from .cookbook_helpers import add_spec, edit_repo_config, new_repo

DEP_ID = "d0000000-0000-4000-8000-000000000000"

ROUTER = '''
import json, sys
from pathlib import Path
state, log = Path(sys.argv[1]), Path(sys.argv[2])
reg = json.loads(state.read_text()) if state.is_file() else {}
args = [a for a in sys.argv[3:] if a != "--json"]
with log.open("a") as f:
    f.write(json.dumps(args) + "\\n")
cmd = args[0]
if cmd == "--version":
    print("skill-router 0.5.0"); sys.exit(0)
if cmd == "list":
    out = {"claude": {"skills": [{"name": n, "path": "/copy/" + n, "origin": o} for n, o in reg.items()]}}
elif cmd == "register":
    reg[Path(args[1]).name] = args[1]
    out = {"claude": {"registered": {"name": Path(args[1]).name}, "warnings": []}}
else:
    reg.pop(args[1], None)
    out = {"claude": {"unregistered": args[1]}}
state.write_text(json.dumps(reg))
print(json.dumps({"hosts": out}))
'''


@pytest.fixture
def env(tmp_path, monkeypatch):
    script = tmp_path / "router.py"
    script.write_text(ROUTER)
    log = tmp_path / "router.log"
    monkeypatch.setenv("COOKR_HOME", str(tmp_path / "cookr"))
    monkeypatch.setenv(inst.ROUTER_ENV, shlex.join([sys.executable, str(script),
                                                    str(tmp_path / "registry.json"), str(log)]))

    def registers():
        calls = [json.loads(l) for l in log.read_text().splitlines()] if log.is_file() else []
        return [c for c in calls if c[0] == "register"]
    return type("Env", (), {"tmp": tmp_path, "registers": staticmethod(registers),
                            "cookr": tmp_path / "cookr"})


def scopes_of(call):
    return [call[i + 1] for i, a in enumerate(call) if a == "--scope"]


def library(tmp_path, name="app", rdid="test-repo", cookbook_id="c0000000-0000-4000-8000-000000000000"):
    repo = new_repo(tmp_path / name, rdid=rdid, cookbook_id=cookbook_id)
    add_spec(repo, "ui/badge", type="recipe", meta={"title": "Badge", "summary": "A badge.",
                                                     "version": "1.0.0"})
    return repo


def sync(repo, capsys, *extra):
    code = main(["-p", str(repo), "skills", "sync", *extra])
    return code, capsys.readouterr().out


def receipt(env):
    return inst.read_receipt(env.cookr)


def test_sync_compiles_and_registers_with_scope(env, capsys):
    repo = library(env.tmp)
    code, out = sync(repo, capsys)
    assert code == 0 and "registered test-repo (1 skills)" in out
    assert (env.cookr / "sets" / "test-repo").is_dir()
    [call] = env.registers()
    assert scopes_of(call) == [str(repo.resolve())]
    assert receipt(env)["routed:test-repo"]["scopes"] == [str(repo.resolve())]


def test_sync_adds_dependent_repo_to_dependency_scopes(env, capsys):
    dep = library(env.tmp, "dep", rdid="dep-lib", cookbook_id=DEP_ID)
    assert sync(dep, capsys)[0] == 0
    app = library(env.tmp, "app")
    edit_repo_config(app, lambda d: d.setdefault("dependencies", {}).__setitem__(
        DEP_ID, {"rdid": "dep-lib", "location": "../dep/cookbook"}))
    code, out = sync(app, capsys)
    assert code == 0 and "registered dep-lib" in out and "registered test-repo" in out
    by_lib = {Path(c[1]).parent.name: scopes_of(c) for c in env.registers()}
    assert by_lib["dep-lib"] == sorted([str(dep.resolve()), str(app.resolve())])
    assert by_lib["test-repo"] == [str(app.resolve())]
    assert receipt(env)["routed:dep-lib"]["scopes"] == sorted([str(dep.resolve()), str(app.resolve())])


def test_sync_noop_when_current(env, capsys):
    repo = library(env.tmp)
    sync(repo, capsys)
    before = len(env.registers())
    code, out = sync(repo, capsys, "--json")
    assert code == 0 and len(env.registers()) == before
    assert json.loads(out)["libraries"][0]["action"] == "ok"
    assert "ok test-repo (1 skills)" in sync(repo, capsys)[1]


def test_unscoped_cookbook_has_no_scope_args(env, capsys):
    repo = library(env.tmp)
    (repo / ".cookr.json").unlink()                # no .cookr.json: the adc cookbook
    code, out = sync(repo, capsys)
    assert code == 0 and "registered test-repo" in out
    assert scopes_of(env.registers()[0]) == [] and "scopes" not in receipt(env)["routed:test-repo"]


def test_an_unreachable_dependency_is_warned_and_skipped(env, capsys):
    app = library(env.tmp)
    edit_repo_config(app, lambda d: d.setdefault("dependencies", {}).__setitem__(
        DEP_ID, {"rdid": "dep-lib", "location": "../nowhere/cookbook"}))
    code, out = sync(app, capsys)
    assert code == 0 and "registered test-repo" in out and "dep-lib" in out and "not reachable" in out


def test_a_router_below_the_minimum_is_refused(env, capsys, monkeypatch):
    monkeypatch.setenv(inst.ROUTER_ENV, f"{sys.executable} -c \"print('skill-router 0.4.0')\"")
    code, out = sync(library(env.tmp), capsys)
    assert code == 1 and "0.5.0" in out and "broken" not in out and not (env.cookr / "sets").exists()


def test_install_scope_flags_replace_and_add(env, capsys, monkeypatch):
    repo = library(env.tmp)
    monkeypatch.chdir(repo)
    a, b = env.tmp / "a", env.tmp / "b"
    assert main(["install", "--target", "routed", "--scope", str(a)]) == 0
    assert main(["install", "--target", "routed", "--scope-add", str(b)]) == 0
    assert scopes_of(env.registers()[-1]) == sorted([str(a.resolve()), str(b.resolve())])
    assert main(["install", "--target", "routed", "--scope", str(b)]) == 0
    assert scopes_of(env.registers()[-1]) == [str(b.resolve())]


def test_a_dependency_synced_from_its_dependent_first_is_scoped_to_both_repos(env, capsys):
    dep = library(env.tmp, "dep", rdid="dep-lib", cookbook_id=DEP_ID)
    app = library(env.tmp, "app")
    edit_repo_config(app, lambda d: d.setdefault("dependencies", {}).__setitem__(
        DEP_ID, {"rdid": "dep-lib", "location": "../dep/cookbook"}))
    assert sync(app, capsys)[0] == 0                      # the dependency's own repo never synced
    by_lib = {Path(c[1]).parent.name: scopes_of(c) for c in env.registers()}
    assert by_lib["dep-lib"] == sorted([str(dep.resolve()), str(app.resolve())])


def test_a_dependency_in_an_unscoped_repo_is_scoped_to_the_repo_that_syncs_it(env, capsys):
    """A dependency whose own repo has no .cookr.json (like adc) must not be routed
    everywhere: it gets the scope of the repo that synced it."""
    dep = library(env.tmp, "dep", rdid="dep-lib", cookbook_id=DEP_ID)
    (dep / ".cookr.json").unlink()
    app = library(env.tmp, "app")
    edit_repo_config(app, lambda d: d.setdefault("dependencies", {}).__setitem__(
        DEP_ID, {"rdid": "dep-lib", "location": "../dep/cookbook"}))
    assert sync(app, capsys)[0] == 0
    by_lib = {Path(c[1]).parent.name: scopes_of(c) for c in env.registers()}
    assert by_lib["dep-lib"] == [str(app.resolve())]
    assert receipt(env)["routed:dep-lib"]["scopes"] == [str(app.resolve())]


def test_scope_replaces_and_scope_add_extends_in_one_call(env, monkeypatch):
    repo = library(env.tmp)
    monkeypatch.chdir(repo)
    a, b = env.tmp / "a", env.tmp / "b"
    assert main(["install", "--target", "routed", "--scope", str(a), "--scope-add", str(b)]) == 0
    assert scopes_of(env.registers()[-1]) == sorted([str(a.resolve()), str(b.resolve())])
    assert main(["install", "--target", "routed", "--scope", str(a), "--scope-add", str(b)]) == 0
    assert len(env.registers()) == 1                      # unchanged: no re-register
