"""`cookr id`, `rename` and `implements`, and `update` storing rdid links as UUIDs."""

from __future__ import annotations

import json

import pytest

from cookr.cli import main
from cookr.core.artifact import load_folder
from cookr.core.errors import CookbookError
from cookr.core.index import load_index
from cookr.core.links import Resolver, to_stored

from .cookbook_helpers import ADC_ID, add_dependency

BUTTON = "mini-repo.ingredient.components.button"
BUTTON_ID = "6f1c2a4e-0b3d-4c5e-9f10-a1b2c3d4e501"
CHAT = "mini-repo.ingredient.components.chat-composer"
CHAT_ID = "6f1c2a4e-0b3d-4c5e-9f10-a1b2c3d4e502"
STAT = "mini-repo.ingredient.blocks.stat-card"


def _entry(repo, rdid):
    return next(e for e in load_index(repo / "cookbook").entries.values() if e.rdid == rdid)


def test_id_both_directions(mini_repo, capsys):
    assert main(["-p", str(mini_repo), "id", BUTTON]) == 0
    assert capsys.readouterr().out.split() == [BUTTON_ID, BUTTON, "components/button", "ingredient"]
    assert main(["-p", str(mini_repo), "id", BUTTON_ID.upper(), "--json"]) == 0
    assert json.loads(capsys.readouterr().out) == {
        "uuid": BUTTON_ID, "rdid": BUTTON, "path": "components/button", "kind": "ingredient"}


def test_id_finds_a_foreign_artifact_and_rejects_the_unknown(mini_repo, capsys):
    add_dependency(mini_repo, "external/adc", checks=[("doc.md", "one")])
    foreign = next(iter(load_index(mini_repo / "external" / "adc").entries.values()))
    assert main(["-p", str(mini_repo), "id", foreign.rdid]) == 0
    assert capsys.readouterr().out.split()[:2] == [f"{ADC_ID}/{foreign.id}", foreign.rdid]
    assert main(["-p", str(mini_repo), "id", "mini-repo.ingredient.nope"]) == 1
    assert "nope" in capsys.readouterr().out


def test_rename_refuses_collision(mini_repo, capsys):
    before = (mini_repo / "cookbook" / "index.json").read_text(encoding="utf-8")
    assert main(["-p", str(mini_repo), "rename", BUTTON, CHAT]) == 1
    assert "components/chat-composer" in capsys.readouterr().out
    assert main(["-p", str(mini_repo), "rename", BUTTON, "Not An Rdid"]) == 2
    assert (mini_repo / "cookbook" / "index.json").read_text(encoding="utf-8") == before


def test_rename_is_idempotent_and_repairs_stale_labels(mini_repo):
    overview = mini_repo / "cookbook" / "blocks" / "stat-card" / "overview.md"
    overview.write_text(f"See [stale.label](cookbook:{BUTTON_ID}).\n", encoding="utf-8")
    assert main(["-p", str(mini_repo), "rename", BUTTON, BUTTON]) == 0
    assert overview.read_text(encoding="utf-8") == f"See [{BUTTON}](cookbook:{BUTTON_ID}).\n"


def test_rename_relabels_in_text_links(mini_repo, capsys):
    folder = mini_repo / "cookbook" / "blocks" / "stat-card"
    overview = folder / "overview.md"
    overview.write_text(
        f"See [{BUTTON}](cookbook:{BUTTON_ID}) and [{CHAT}](cookbook:{CHAT_ID}).\n", encoding="utf-8")
    meta_before = (folder / "artifact.json").read_text(encoding="utf-8")
    assert main(["-p", str(mini_repo), "rename", BUTTON_ID, "mini-repo.ingredient.ui.push-button"]) == 0
    assert overview.read_text(encoding="utf-8") == (
        f"See [mini-repo.ingredient.ui.push-button](cookbook:{BUTTON_ID}) and "
        f"[{CHAT}](cookbook:{CHAT_ID}).\n")
    assert _entry(mini_repo, "mini-repo.ingredient.ui.push-button").id == BUTTON_ID
    assert (folder / "artifact.json").read_text(encoding="utf-8") == meta_before  # no bump
    assert "stat-card" in capsys.readouterr().out


def test_implements_add_remove_and_refuse_owned(mini_repo, capsys):
    stat_rows = lambda: [(i.platform, i.location, i.conformance.state)  # noqa: E731
                         for i in _entry(mini_repo, STAT).implementations]
    base = ["-p", str(mini_repo), "implements", STAT]
    assert main([*base, "web/components/Button.tsx", "--platform", "web"]) == 1  # exactly owned
    assert main([*base, "web/blocks/Missing.tsx", "--platform", "web"]) == 1  # not on disk
    assert main([*base, "web/blocks/Missing.tsx", "--platform", "cobol", "--planned"]) == 2
    assert main([*base, "web/blocks/Missing.tsx", "--platform", "web", "--planned"]) == 0
    assert ("web", "web/blocks/Missing.tsx", "planned") in stat_rows()
    assert main([*base, "--remove", "web/blocks/Missing.tsx"]) == 0
    assert all(loc != "web/blocks/Missing.tsx" for _, loc, _ in stat_rows())
    assert main([*base, "--remove", "web/blocks/Missing.tsx"]) == 1
    assert main([*base, "web/components/index.ts", "--platform", "web"]) == 0
    assert ("web", "web/components/index.ts", "unverified") in stat_rows()


def test_implements_names_the_owner(mini_repo, capsys):
    capsys.readouterr()
    assert main(["-p", str(mini_repo), "implements", STAT, "web/components/Button.tsx",
                 "--platform", "web"]) == 1
    assert BUTTON in capsys.readouterr().out


def test_update_rewrites_rdid_links_to_uuids(mini_repo, capsys):
    folder = mini_repo / "cookbook" / "blocks" / "stat-card"
    manifest = json.loads((folder / "artifact.json").read_text(encoding="utf-8"))
    manifest["meta"]["depends-on"] = [BUTTON, CHAT_ID]
    manifest["meta"]["related"] = [BUTTON]
    (folder / "artifact.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    (folder / "overview.md").write_text(f"Uses [button](cookbook:{BUTTON}).\n", encoding="utf-8")
    assert main(["update", "-p", str(mini_repo / "cookbook"), "--no-indexes", "--author", "T"]) == 0
    art = load_folder(folder)
    assert art.meta["depends-on"] == [BUTTON_ID, CHAT_ID]
    assert art.meta["related"] == [BUTTON_ID]
    assert (folder / "overview.md").read_text(encoding="utf-8") == (
        f"Uses [{BUTTON}](cookbook:{BUTTON_ID}).\n")


def test_update_leaves_an_unresolved_rdid_and_fails(mini_repo, capsys):
    folder = mini_repo / "cookbook" / "blocks" / "stat-card"
    manifest = json.loads((folder / "artifact.json").read_text(encoding="utf-8"))
    manifest["meta"]["depends-on"] = ["mini-repo.ingredient.nope"]
    (folder / "artifact.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    assert main(["update", "-p", str(mini_repo / "cookbook"), "--no-indexes", "--author", "T"]) == 1
    assert load_folder(folder).meta["depends-on"] == ["mini-repo.ingredient.nope"]
    assert "nope" in capsys.readouterr().out


def test_to_stored_forms_and_failures(mini_repo):
    add_dependency(mini_repo, "external/adc", checks=[("doc.md", "one")])
    from cookr.core.repoconfig import load_repo_config
    from cookr.core.links import resolver_for
    cfg = load_repo_config(mini_repo)
    r = resolver_for(cfg)
    foreign = next(iter(load_index(mini_repo / "external" / "adc").entries.values()))
    assert to_stored(BUTTON, r) == BUTTON_ID
    assert to_stored(BUTTON_ID, r) == BUTTON_ID
    assert to_stored(f"mini-repo/{BUTTON}", r) == BUTTON_ID
    assert to_stored(foreign.rdid, r) == f"{ADC_ID}/{foreign.id}"
    assert to_stored(f"adc/{foreign.rdid}", r) == f"{ADC_ID}/{foreign.id}"
    with pytest.raises(CookbookError, match="ingredient.nope"):
        to_stored("mini-repo.ingredient.nope", r)
    with pytest.raises(CookbookError, match="adc.check.gone"):
        to_stored("adc.check.gone", r)
    unreachable = Resolver(cfg.repo_root, r.own, cfg.dependencies | {})
    unreachable._cache[ADC_ID] = None
    with pytest.raises(CookbookError, match="unreachable"):
        to_stored(foreign.rdid, unreachable)


def test_update_stores_resolvable_links_even_when_another_is_unresolved(mini_repo, capsys):
    folder = mini_repo / "cookbook" / "blocks" / "stat-card"
    manifest = json.loads((folder / "artifact.json").read_text(encoding="utf-8"))
    manifest["meta"]["depends-on"] = [BUTTON, "mini-repo.ingredient.nope"]
    (folder / "artifact.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    assert main(["update", "-p", str(mini_repo / "cookbook"), "--no-frontmatter",
                 "--no-indexes"]) == 1
    assert load_folder(folder).meta["depends-on"] == [BUTTON_ID, "mini-repo.ingredient.nope"]
    assert "nope" in capsys.readouterr().out


def test_to_stored_prefers_the_longest_dependency_rdid(mini_repo):
    # Real cookbook rdids cannot contain a dot, so overlapping prefixes are built
    # directly on the resolver, with their indexes pre-loaded.
    from cookr.core.index import Entry, Index
    from cookr.core.identity import CookbookIdentity
    from cookr.core.links import resolver_for
    from cookr.core.repoconfig import Dependency, load_repo_config
    cfg = load_repo_config(mini_repo)
    short_id, long_id = "a" * 8 + "-0000-4000-8000-000000000001", "b" * 8 + "-0000-4000-8000-000000000002"
    art = "c" * 8 + "-0000-4000-8000-000000000003"
    rdid = "adc.x.ingredient.thing"
    r = resolver_for(cfg)
    r.dependencies = {short_id: Dependency(short_id, "adc"), long_id: Dependency(long_id, "adc.x")}
    r._cache[short_id] = Index(cookbook=CookbookIdentity(short_id, "adc"))
    r._cache[long_id] = Index(cookbook=CookbookIdentity(long_id, "adc.x"),
                              entries={art: Entry(art, "ingredient", rdid, "thing")})
    assert to_stored(rdid, r) == f"{long_id}/{art}"
