"""`cookr install` / `uninstall`: targets, states, adopt, receipt, the CLI."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from cookr.cli import main
from cookr.core import hosts, install as inst
from cookr.core.artifact import find_folders

from .test_skill import make


class FakeRouter(inst.Router):
    """skill-router's registry in memory, answering as its CLI does."""

    def __init__(self):
        super().__init__(["fake"])
        self.skills: dict[str, dict] = {}
        self.calls: list[str] = []

    def listed(self, source):
        return [e for e in self.skills.values() if e["source"] == source]

    def register(self, set_dir, source):
        self.calls.append("register")
        old = {n for n, e in self.skills.items() if e["source"] == source}
        new = {p.parent.name: {"name": p.parent.name, "path": str(p.parent), "source": source}
               for p in Path(set_dir).glob("*/SKILL.md")}
        for n in old - set(new):
            del self.skills[n]
        self.skills.update(new)
        return {"registered": sorted(new), "failed": [], "removed": sorted(old - set(new))}

    def unregister(self, source):
        self.calls.append("unregister")
        if not self.listed(source):
            raise inst.RouterError(f"no skills registered from source {source!r}")
        self.skills = {n: e for n, e in self.skills.items() if e["source"] != source}


@pytest.fixture
def env(tmp_path, monkeypatch):
    root = tmp_path / "cookbook"
    root.mkdir()
    (root / "index.md").write_text("# Cookbook\n")   # what makes it a cookbook cookr finds
    make(root, "principles/simplicity", "principle")
    make(root, "guidelines/implementing/data/use-wal", "guideline")
    home = tmp_path / "home"
    (home / ".claude").mkdir(parents=True)
    monkeypatch.setenv("HOME", str(home))
    monkeypatch.setenv("COOKR_HOME", str(tmp_path / "cookr"))
    router = FakeRouter()
    monkeypatch.setattr(inst.Router, "find", classmethod(lambda cls: router))
    return type("Env", (), {"book": root, "home": home, "router": router, "cookr": tmp_path / "cookr"})


def installer(env, specs=None, **kw):
    routed, targets = inst.select(specs)
    return inst.Installer(folders=find_folders([env.book]), routed=routed, targets=targets,
                          router=env.router, **kw)


def states(statuses):
    return {s.item: s.state for s in statuses}


SKILL = ".claude/skills/general-principles/SKILL.md"


def test_targets_default_to_routed_and_hosts_whose_home_exists(env):
    routed, targets = inst.select(None)
    assert routed and [t.host.name for t in targets] == ["claude"]
    assert targets[0].chain == ("claude",)          # every model on the host reads the file
    receipt = {"always-on:claude:general-principles": {"kind": "always-on", "host": "claude",
                                                      "target": "claude.opus"}}
    assert inst.select(None, receipt=receipt)[1][0].chain == ("claude", "claude.opus")


def test_target_specs_name_a_host_family_or_model(env):
    h = hosts.manifest()
    assert inst.host_target("claude.opus", h).chain == ("claude", "claude.opus")
    assert inst.host_target("claude.opus-5-5", h).target == "claude.opus-5-5"
    routed, targets = inst.select(["codex"])
    assert not routed and targets[0].host.name == "codex"
    with pytest.raises(inst.InstallError, match="one target per host"):
        inst.select(["claude.opus", "claude.sonnet"])
    with pytest.raises(hosts.HostError):
        inst.select(["nope"])


def test_install_check_uninstall_round_trip(env):
    i = installer(env)
    assert set(states(i.check()).values()) == {inst.MISSING}
    assert set(states(i.install(dry_run=True)).values()) == {inst.MISSING}
    assert not env.cookr.exists() and env.router.calls == []
    out = i.install()
    assert set(states(out).values()) == {inst.OK}
    assert [s.action for s in out] == ["compiled", "registered", "wrote"]
    assert set(env.router.skills) == {"principle-simplicity", "implementing-data-use-wal"}
    assert "principle-simplicity" in (env.home / SKILL).read_text()
    assert set(states(i.check()).values()) == {inst.OK}
    assert [s.action for s in i.install()] == ["", "", ""]          # idempotent
    assert env.router.calls == ["register"]
    assert set(states(i.uninstall()).values()) == {inst.OK}
    assert env.router.skills == {} and not env.cookr.exists()
    assert not (env.home / ".claude/skills").exists()


def test_a_sets_near_duplicate_keywords_are_accepted_and_reported(env, monkeypatch):
    seen = []
    monkeypatch.setattr(inst.Router, "_run", lambda self, *a: seen.append(a) or {})
    inst.Router(["x"]).register(Path("set"), "lib")
    assert "--new-keyword" in seen[0]
    warn = "accepted new keyword 'service' looks like existing 'services'"
    real = FakeRouter.register
    monkeypatch.setattr(FakeRouter, "register",
                        lambda self, d, s: {**real(self, d, s), "warnings": [warn, warn]})
    out = installer(env, ["routed"]).install()
    assert states(out)[out[1].item] == inst.OK
    assert out[1].detail.endswith("; accepted near-duplicate keywords: "
                                  "new keyword 'service' looks like existing 'services'")


def test_a_skills_dir_that_was_there_stays(env):
    (env.home / ".claude/skills/other").mkdir(parents=True)
    i = installer(env, ["claude"])
    i.install()
    i.uninstall()
    assert (env.home / ".claude/skills/other").is_dir()
    assert not (env.home / ".claude/skills/general-principles").exists()


def test_a_foreign_skill_is_broken_until_adopted_and_comes_back(env):
    mine = env.home / SKILL
    mine.parent.mkdir(parents=True)
    mine.write_text("hand-kept\n")
    i = installer(env, ["claude"])
    assert states(i.install()) == {"always-on:claude:general-principles": inst.BROKEN}
    assert mine.read_text() == "hand-kept\n"
    assert [s.action for s in i.install(adopt=True)] == ["adopted"]
    assert mine.read_text() != "hand-kept\n"
    assert [s.action for s in i.uninstall()] == ["removed, original restored"]
    assert mine.read_text() == "hand-kept\n" and not env.cookr.exists()


def test_an_edited_skill_drifts_and_survives_uninstall_without_force(env):
    i = installer(env, ["claude"])
    i.install()
    (env.home / SKILL).write_text("mine now\n")
    assert states(i.check())["always-on:claude:general-principles"] == inst.DRIFT
    assert states(i.uninstall())["always-on:claude:general-principles"] == inst.DRIFT
    assert (env.home / SKILL).read_text() == "mine now\n"
    assert states(i.uninstall(force=True))["always-on:claude:general-principles"] == inst.OK
    assert not (env.home / SKILL).exists()


def test_a_changed_cookbook_drifts_and_reinstall_catches_up(env):
    i = installer(env)
    i.install()
    make(env.book, "principles/yagni", "principle", summary="Build for today.")
    i = installer(env)
    got = states(i.check())
    assert got["set:cookbook"] == inst.DRIFT and got["routed:cookbook"] == inst.DRIFT
    assert got["always-on:claude:general-principles"] == inst.DRIFT
    assert set(states(i.install()).values()) == {inst.OK}
    assert "principle-yagni" in env.router.skills and "yagni" in (env.home / SKILL).read_text()


def test_no_router_is_broken_but_the_rest_installs(env):
    routed, targets = inst.select(None)
    i = inst.Installer(folders=find_folders([env.book]), routed=routed, targets=targets, router=None)
    got = states(i.install())
    assert got == {"set:cookbook": inst.OK, "routed:cookbook": inst.BROKEN,
                   "always-on:claude:general-principles": inst.OK}


def test_uninstall_narrows_by_library_and_target(env):
    installer(env).install()
    other = inst.Installer(folders=find_folders([env.book]), library="adtoolkit", routed=True,
                           targets=[], router=env.router)
    other.install()
    assert {e["source"] for e in env.router.skills.values()} == {"cookbook", "adtoolkit"}
    inst.Installer(folders=[], library="adtoolkit", routed=True, router=env.router).uninstall()
    assert {e["source"] for e in env.router.skills.values()} == {"cookbook"}
    assert (env.home / SKILL).exists()


def test_the_cli_reports_json_and_exits_by_state(env, monkeypatch, capsys):
    monkeypatch.chdir(env.book.parent)
    assert main(["install", "--check", "--json"]) == 1
    assert {i["state"] for i in json.loads(capsys.readouterr().out)["items"]} == {"missing"}
    assert main(["install", "--json"]) == 0
    capsys.readouterr()
    assert main(["install", "--check"]) == 0
    assert main(["install", "--check", "--adopt"]) == 2
    assert main(["install", "--target", "nope"]) == 2
    capsys.readouterr()
    assert main(["uninstall", "--json"]) == 0
    assert json.loads(capsys.readouterr().out)["ok"] is True
    assert env.router.skills == {} and not env.cookr.exists()


# ── safety: what install and uninstall refuse to do ─────────────────────────

def test_installing_no_folders_refuses_and_keeps_the_installed_set(env, monkeypatch, capsys):
    monkeypatch.chdir(env.book.parent)
    assert main(["install", "--target", "routed"]) == 0
    (env.book.parent / "empty").mkdir()
    assert main(["install", "--target", "routed", "empty"]) == 2
    assert "no artifact folders" in capsys.readouterr().out
    assert set(env.router.skills) == {"principle-simplicity", "implementing-data-use-wal"}


def test_no_cookbook_found_is_an_error_not_an_empty_install(env, tmp_path, monkeypatch, capsys):
    (tmp_path / "elsewhere").mkdir()
    monkeypatch.chdir(tmp_path / "elsewhere")
    assert main(["install"]) == 2
    assert "no cookbook found" in capsys.readouterr().out


def test_concerns_default_to_the_cookbook_holding_the_path(env):
    from cookr.modules.install import _concerns
    assert _concerns(env.book / "principles") == env.book / "workflows/pipeline-concerns.json"


def test_a_library_installed_from_other_paths_needs_replace(env, monkeypatch, capsys):
    monkeypatch.chdir(env.book.parent)
    assert main(["install", "--target", "routed"]) == 0
    capsys.readouterr()
    assert main(["install", "--target", "routed", "cookbook/principles", "--json"]) == 1
    got = json.loads(capsys.readouterr().out)["items"]
    assert [i["item"] for i in got] == ["library:cookbook"] and "--replace" in got[0]["detail"]
    assert "implementing-data-use-wal" in env.router.skills       # nothing pruned
    assert main(["install", "--check", "--target", "routed", "cookbook/principles"]) == 1
    assert main(["install", "--target", "routed", "cookbook/principles", "--replace"]) == 0
    assert set(env.router.skills) == {"principle-simplicity"}
    receipt = inst.read_receipt(env.cookr)
    assert receipt["set:cookbook"]["from"] == [str((env.book / "principles").resolve())]


def test_library_names_are_checked_and_the_default_is_unprefixed(env, monkeypatch):
    from cookr.core.skill import SkillError, library_name
    assert library_name("cookbook") is None and library_name("adtoolkit") == "adtoolkit"
    for bad in ("MyLib", "my_lib", "-x", "a--b", "x" * 33):
        with pytest.raises(SkillError):
            library_name(bad)
    i = installer(env, ["routed"], library="cookbook")
    assert i.library is None and i.set_dir.name == "cookbook"
    i.install()
    assert "principle-simplicity" in env.router.skills            # not cookbook-principle-…
    monkeypatch.chdir(env.book.parent)
    with pytest.raises(SystemExit):
        main(["install", "--library", "MyLib"])


def test_uninstall_takes_the_default_library_unless_told_every_library(env, monkeypatch):
    installer(env, ["routed"]).install()
    installer(env, ["routed"], library="adtoolkit").install()
    monkeypatch.chdir(env.book.parent)
    assert main(["uninstall", "--target", "routed"]) == 0
    assert {e["source"] for e in env.router.skills.values()} == {"adtoolkit"}
    installer(env, ["routed"]).install()
    assert main(["uninstall", "--target", "routed", "--every-library"]) == 0
    assert env.router.skills == {} and not env.cookr.exists()


def test_an_edited_skill_is_not_overwritten_without_force(env):
    i = installer(env, ["claude"])
    i.install()
    (env.home / SKILL).write_text("mine now\n")
    s = i.install()[0]
    assert s.state == inst.DRIFT and "--force" in s.detail
    assert (env.home / SKILL).read_text() == "mine now\n"
    assert [s.action for s in i.install(force=True)] == ["wrote"]
    assert "principle-simplicity" in (env.home / SKILL).read_text()


def test_adopt_never_writes_a_rendering_that_would_not_load(env, monkeypatch):
    mine = env.home / SKILL
    mine.parent.mkdir(parents=True)
    mine.write_text("hand-kept\n")
    monkeypatch.setattr(inst.tuning, "load_problems", lambda text, host: ["too long"])
    s = installer(env, ["claude"]).install(adopt=True)[0]
    assert s.state == inst.BROKEN and "would not load" in s.detail
    assert mine.read_text() == "hand-kept\n" and not (env.cookr / "backup").exists()


def test_a_failed_install_still_writes_the_receipt(env, monkeypatch):
    def boom(self, set_dir, source):
        raise RuntimeError("router crashed")
    monkeypatch.setattr(FakeRouter, "register", boom)
    with pytest.raises(RuntimeError):
        installer(env, ["routed"]).install()
    assert "set:cookbook" in inst.read_receipt(env.cookr)           # the compiled set is known
    assert not list(env.cookr.glob(".install.json.*"))              # written whole, no temp left


def test_the_receipt_lock_goes_with_the_last_item(env):
    i = installer(env, ["routed"])
    i.install()
    assert (env.cookr / inst.LOCK).exists()
    i.uninstall()
    assert not env.cookr.exists()


def test_uninstall_restores_nothing_over_files_it_did_not_write(env):
    mine = env.home / SKILL
    mine.parent.mkdir(parents=True)
    mine.write_text("hand-kept\n")
    i = installer(env, ["claude"])
    i.install(adopt=True)
    (mine.parent / "notes.md").write_text("added later\n")
    s = i.uninstall()[0]
    assert s.state == inst.BROKEN and "notes.md" in s.detail
    assert mine.is_file() and "principle-simplicity" in mine.read_text()    # nothing deleted
    assert "always-on:claude:general-principles" in inst.read_receipt(env.cookr)


def test_a_set_still_registered_is_kept(env, monkeypatch):
    installer(env, ["routed"]).install()

    def fail(self, source):
        raise inst.RouterError("registry locked")
    monkeypatch.setattr(FakeRouter, "unregister", fail)
    got = states(installer(env, ["routed"]).uninstall())
    assert got == {"routed:cookbook": inst.BROKEN, "set:cookbook": inst.BROKEN}
    assert (env.cookr / "sets/cookbook/principle-simplicity/SKILL.md").is_file()


def test_a_set_compiled_again_since_registering_drifts(env):
    i = installer(env, ["routed"])
    i.install()
    f = env.cookr / "sets/cookbook/principle-simplicity/SKILL.md"
    f.write_text(f.read_text() + "\nchanged\n")
    i.install()                                                     # recompiles, re-registers
    assert env.router.calls == ["register", "register"]
    receipt = inst.read_receipt(env.cookr)
    receipt["routed:cookbook"]["digest"] = "stale"
    inst.write_receipt(env.cookr, receipt)
    assert states(i.check())["routed:cookbook"] == inst.DRIFT


def test_the_always_on_skill_links_only_skills_that_compile(env):
    bad = make(env.book, "principles/broken", "principle")
    manifest = bad / "artifact.json"
    manifest.write_text(manifest.read_text().replace('"type": "principle"', '"type": "recipe"', 1))
    installer(env, ["claude"]).install()
    text = (env.home / SKILL).read_text()
    assert "(`principle-simplicity`)" in text and "principle-broken" not in text


def test_a_router_too_old_for_cookr_is_refused():
    import sys

    def router(out, code=0):
        return inst.Router([sys.executable, "-c", f"import sys; print({out!r}); sys.exit({code})"])
    with pytest.raises(inst.RouterError, match="is 0.1.9; cookr needs skill-router 0.2.0"):
        router("skill-router-registry 0.1.9").require_version()
    with pytest.raises(inst.RouterError, match="has no --version"):
        router("usage: ...", 2).require_version()
    router("skill-router-registry 0.2.0").require_version()


def test_a_doc_with_no_source_folder_stops_install(env, monkeypatch, capsys):
    # Installing without it would drop its skill unnoticed.
    (env.book / "principles" / "loose.md").write_text("---\ntype: principle\n---\n# Loose\n")
    monkeypatch.chdir(env.book.parent)
    assert main(["install"]) == 2
    assert "loose.md" in capsys.readouterr().out and env.router.skills == {}
