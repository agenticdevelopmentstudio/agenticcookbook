import json

import pytest

from cookr.core.identity import CookbookIdentity
from cookr.core.index import Entry, Index, save_index
from cookr.core.links import (Dependency, Link, Resolver, format_link, in_text_links, parse_link,
                              read_locations, relabel, remember_location, stale_labels)

OWN = CookbookIdentity("5b1e0000-0000-4000-8000-000000000000", "adc")
FOR = CookbookIdentity("9d020000-0000-4000-8000-000000000000", "adhsdk")
A1, A2 = "11111111-1111-4111-8111-111111111111", "22222222-2222-4222-8222-222222222222"
MISSING = "33333333-3333-4333-8333-333333333333"


@pytest.fixture(autouse=True)
def home(tmp_path, monkeypatch):
    monkeypatch.setenv("COOKR_HOME", str(tmp_path / "home"))


def own_index():
    return Index(OWN, {A1: Entry(A1, "recipe", "adc.recipe.a", "recipes/a")})


def foreign_cookbook(path, rdid="adhsdk.recipe.z"):
    path.mkdir(parents=True)
    save_index(Index(FOR, {A2: Entry(A2, "recipe", rdid, "recipes/z")}), path)


def test_parse_and_format_round_trip():
    assert parse_link(A1) == Link(None, A1)
    assert format_link(Link(None, A1)) == A1
    link = parse_link(f"{FOR.id.upper()}/{A2}")
    assert link == Link(FOR.id, A2)
    assert format_link(link) == f"{FOR.id}/{A2}"
    with pytest.raises(ValueError):
        parse_link("not-a-link")


def test_in_text_links_and_relabel():
    text = f"See [old](cookbook:{FOR.id}/{A2}) and [x](cookbook:{A1}) and [no](http://x)."
    found = in_text_links(text)
    assert found == [("old", Link(FOR.id, A2)), ("x", Link(None, A1))]
    out = relabel(text, {Link(FOR.id, A2): "adhsdk.recipe.z"})
    assert f"[adhsdk.recipe.z](cookbook:{FOR.id}/{A2})" in out
    assert f"[x](cookbook:{A1})" in out


def test_resolve_local_ok_and_missing(tmp_path):
    r = Resolver(tmp_path, own_index(), {})
    ok = r.resolve(Link(None, A1))
    assert (ok.state, ok.rdid) == ("ok", "adc.recipe.a") and ok.entry.id == A1
    assert r.resolve(Link(OWN.id, A1)).state == "ok"
    assert r.resolve(Link(None, MISSING)).state == "missing"


def test_resolve_dependency_by_relative_location(tmp_path):
    foreign_cookbook(tmp_path / "external" / "cb")
    deps = {FOR.id: Dependency(FOR.id, "adhsdk", "external/cb")}
    r = Resolver(tmp_path, own_index(), deps)
    assert r.resolve(Link(FOR.id, A2)).state == "ok"
    assert r.resolve(Link(FOR.id, MISSING)).state == "missing"
    assert r.index_for(FOR.id) is r.index_for(FOR.id)


def test_resolve_falls_back_to_locations_json(tmp_path):
    other = tmp_path / "elsewhere"
    foreign_cookbook(other)
    remember_location(FOR, other, None)
    remember_location(OWN, tmp_path, "adc")
    locs = read_locations()
    assert locs[FOR.id] == {"rdid": "adhsdk", "path": str(other)}
    assert locs[OWN.id]["legacy_scheme"] == "adc"
    deps = {FOR.id: Dependency(FOR.id, "adhsdk", "does/not/exist")}
    assert Resolver(tmp_path, own_index(), deps).resolve(Link(FOR.id, A2)).state == "ok"
    assert Resolver(tmp_path, own_index(), {}).resolve(Link(FOR.id, A2)).state == "ok"


def test_unreachable_cookbook_is_not_an_error(tmp_path):
    r = Resolver(tmp_path, own_index(), {})
    res = r.resolve(Link(FOR.id, A2))
    assert res.state == "unreachable" and res.entry is None
    assert r.index_for(FOR.id) is None
    # location that doesn't exist
    remember_location(FOR, tmp_path / "gone", None)
    assert Resolver(tmp_path, own_index(), {}).resolve(Link(FOR.id, A2)).state == "unreachable"
    # corrupt index.json, and a format 1 index
    bad = tmp_path / "bad"
    bad.mkdir()
    (bad / "index.json").write_text("{not json")
    deps = {FOR.id: Dependency(FOR.id, "adhsdk", "bad")}
    assert Resolver(tmp_path, own_index(), deps).resolve(Link(FOR.id, A2)).state == "unreachable"
    (bad / "index.json").write_text(json.dumps({"format": 1}))
    assert Resolver(tmp_path, own_index(), deps).resolve(Link(FOR.id, A2)).state == "unreachable"


def test_remember_location_keeps_others_and_is_atomic(tmp_path):
    remember_location(FOR, tmp_path, None)
    remember_location(OWN, tmp_path, None)
    assert set(read_locations()) == {FOR.id, OWN.id}
    assert not list((tmp_path / "home").glob("*.tmp"))


def test_stale_label_detected(tmp_path):
    foreign_cookbook(tmp_path / "cb", rdid="adhsdk.recipe.renamed")
    own = own_index()
    own.foreign = {f"{FOR.id}/{A2}": "adhsdk.recipe.z", f"{FOR.id}/{MISSING}": "adhsdk.recipe.q"}
    deps = {FOR.id: Dependency(FOR.id, "adhsdk", "cb")}
    stale = stale_labels(own, Resolver(tmp_path, own, deps))
    assert stale == {f"{FOR.id}/{A2}": ("adhsdk.recipe.z", "adhsdk.recipe.renamed")}


def test_in_text_links_and_relabel_skip_unparseable():
    junk = "[x](cookbook:" + "-" * 36 + ")"
    text = f"{junk} and [ok](cookbook:{A1})"
    assert in_text_links(text) == [("ok", Link(None, A1))]
    assert relabel(text, {Link(None, A1): "adc.recipe.a"}) == f"{junk} and [adc.recipe.a](cookbook:{A1})"


def test_url_dependency_location_is_skipped(tmp_path):
    # A cookbook sits where the URL would land if it were read as a path, so an
    # attempt would resolve: unreachable proves the URL was skipped, not tried.
    url = "https://example.com/cookbook"
    foreign_cookbook(tmp_path / url)
    as_path = {FOR.id: Dependency(FOR.id, "adhsdk", "https:/example.com/cookbook")}
    assert Resolver(tmp_path, own_index(), as_path).resolve(Link(FOR.id, A2)).state == "ok"
    deps = {FOR.id: Dependency(FOR.id, "adhsdk", url)}
    r = Resolver(tmp_path, own_index(), deps)
    assert r.resolve(Link(FOR.id, A2)).state == "unreachable"


def test_in_text_links_accept_upper_case_uuids():
    text = f"[a](cookbook:{A1.upper()}) and [z](cookbook:{FOR.id.upper()}/{A2.upper()})"
    assert in_text_links(text) == [("a", Link(None, A1)), ("z", Link(FOR.id, A2))]
    assert relabel(text, {Link(None, A1): "adc.recipe.a"}).startswith(
        f"[adc.recipe.a](cookbook:{A1.upper()})")


def test_an_absolute_dependency_location_is_not_read(tmp_path):
    # A committed location is relative to the repo; an absolute one (a path on
    # one machine) belongs in locations.json, and is never read from the config.
    foreign_cookbook(tmp_path / "elsewhere")
    (tmp_path / "repo").mkdir()
    deps ={FOR.id: Dependency(FOR.id, "adhsdk", str(tmp_path / "elsewhere"))}
    assert Resolver(tmp_path / "repo", own_index(), deps).resolve(Link(FOR.id, A2)).state == \
        "unreachable"
    sibling = {FOR.id: Dependency(FOR.id, "adhsdk", "../elsewhere")}  # a sibling checkout
    assert Resolver(tmp_path / "repo", own_index(), sibling).resolve(Link(FOR.id, A2)).state == "ok"


def test_an_unreachable_dependency_is_found_once_it_arrives(tmp_path):
    deps = {FOR.id: Dependency(FOR.id, "adhsdk", "cb")}
    r = Resolver(tmp_path, own_index(), deps)
    assert r.resolve(Link(FOR.id, A2)).state == "unreachable"
    foreign_cookbook(tmp_path / "cb")                      # e.g. a submodule checked out
    assert r.resolve(Link(FOR.id, A2)).state == "ok"
    assert r.dir_for(FOR.id) == tmp_path / "cb"
