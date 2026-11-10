import json
import shutil

import pytest

from cookr.core.identity import CookbookIdentity
from cookr.core.index import (Conformance, Entry, Implementation, Index, IndexFileError,
                              load_index, save_index, sync_from_folders)

CB = CookbookIdentity("5b1e0000-0000-4000-8000-000000000000", "adc")
U1, U2 = "11111111-1111-4111-8111-111111111111", "22222222-2222-4222-8222-222222222222"


def impl(loc, state="unverified"):
    return Implementation("macos", loc, Conformance(state))


def make_folder(root, rel, uid, type_="guideline"):
    d = root / rel
    d.mkdir(parents=True)
    (d / "artifact.json").write_text(json.dumps({"format": 1, "meta": {"id": uid, "type": type_}, "parts": []}))


def test_index_round_trip(tmp_path):
    idx = Index(CB, {
        U1: Entry(U1, "recipe", "adc.recipe.a", "recipes/a",
                  [Implementation("macos", "src/a/", Conformance("confirmed", "1.4.0", "sha256:ab")),
                   Implementation("ios", None, Conformance("planned"))]),
        "c": Entry("c", "check", "adc.check.x.y", "x#y"),
    }, {"9d02/17d2": "other.recipe.z"}, catalog="tbd/compliance")
    save_index(idx, tmp_path)
    assert load_index(tmp_path) == idx
    assert (tmp_path / "index.json").read_text().endswith("}\n")


def test_owners_file_beats_dir_deepest_dir_wins():
    idx = Index(CB, {
        U1: Entry(U1, "recipe", "adc.recipe.a", "a", [impl("src/"), impl("src/deep/"), impl("src/deep/f.swift")]),
        U2: Entry(U2, "recipe", "adc.recipe.b", "b", [impl("https://x.dev/y")]),
    })
    assert [i.location for _, i in idx.owners("src/deep/f.swift")] == ["src/deep/f.swift"]
    assert [i.location for _, i in idx.owners("src/deep/g.swift")] == ["src/deep/"]
    assert [i.location for _, i in idx.owners("src/h.swift")] == ["src/"]
    assert idx.owners("other/h.swift") == []


def test_sync_adds_moves_drops(tmp_path):
    make_folder(tmp_path, "guidelines/testing/pyramid", U1)
    idx = Index(CB)
    assert sync_from_folders(idx, tmp_path) == ["added adc.guideline.testing.pyramid (guidelines/testing/pyramid)"]
    idx.entries[U1].rdid = "adc.guideline.custom"
    (tmp_path / "guidelines/testing/pyramid").rename(tmp_path / "guidelines/other")
    (tmp_path / "guidelines/testing").rmdir()
    out = sync_from_folders(idx, tmp_path)
    assert out and out[0].startswith("moved")
    assert idx.entries[U1].path == "guidelines/other" and idx.entries[U1].rdid == "adc.guideline.custom"
    idx.entries["chk"] = Entry("chk", "check", "adc.check.a.b", "a#b")
    shutil.rmtree(tmp_path / "guidelines")
    assert sync_from_folders(idx, tmp_path)[0].startswith("dropped")
    assert list(idx.entries) == ["chk"]


def test_sync_refuses_rdid_collision(tmp_path):
    make_folder(tmp_path, "guidelines/t/a", U1)
    make_folder(tmp_path, "guidelines/old/a", U2)
    idx = Index(CB, {U2: Entry(U2, "guideline", "adc.guideline.t.a", "guidelines/old/a")})
    with pytest.raises(IndexFileError) as e:
        sync_from_folders(idx, tmp_path)
    assert "guidelines/t/a" in str(e.value) and "guidelines/old/a" in str(e.value)


def test_get_by_uuid_or_rdid():
    e = Entry(U1, "recipe", "adc.recipe.a", "a")
    idx = Index(CB, {U1: e})
    assert idx.get(U1) is e and idx.get("adc.recipe.a") is e and idx.get("nope") is None
    assert idx.by_path("a") is e


def test_sync_refuses_duplicate_folder_id(tmp_path):
    make_folder(tmp_path, "guidelines/a", U1)
    make_folder(tmp_path, "guidelines/b", U1.upper())
    with pytest.raises(IndexFileError) as e:
        sync_from_folders(Index(CB), tmp_path)
    assert "guidelines/a" in str(e.value) and "guidelines/b" in str(e.value)


def test_load_index_lowercases_uuids(tmp_path):
    save_index(Index(CB, {U1: Entry(U1, "recipe", "adc.recipe.a", "a")}), tmp_path)
    p = tmp_path / "index.json"
    p.write_text(p.read_text().replace(U1, U1.upper()).replace(CB.id, CB.id.upper()))
    idx = load_index(tmp_path)
    assert list(idx.entries) == [U1] and idx.entries[U1].id == U1 and idx.cookbook.id == CB.id


def _saved(tmp_path, edit):
    """An index.json saved for one recipe with two rows, then hand-edited by `edit(data)`."""
    save_index(Index(CB, {U1: Entry(U1, "recipe", "adc.recipe.a", "a",
                                    [impl("src/a.swift"),
                                     Implementation("ios", None, Conformance("planned"))])}),
               tmp_path)
    p = tmp_path / "index.json"
    data = json.loads(p.read_text())
    edit(data)
    p.write_text(json.dumps(data))


def _row(d, n):
    return d["entries"][U1]["implementations"][n]


@pytest.mark.parametrize("what, edit", [
    ("kind", lambda d: d["entries"][U1].__setitem__("kind", "widget")),
    ("state", lambda d: _row(d, 0)["conformance"].__setitem__("state", "conforms")),
    ("no location", lambda d: _row(d, 1)["conformance"].__setitem__("state", "unverified")),
])
def test_load_refuses_a_broken_invariant(tmp_path, what, edit):
    _saved(tmp_path, edit)
    with pytest.raises(IndexFileError, match=what):
        load_index(tmp_path)


def test_a_planned_row_may_name_its_intended_location(tmp_path):
    _saved(tmp_path, lambda d: _row(d, 0)["conformance"].__setitem__("state", "planned"))
    assert load_index(tmp_path).entries[U1].implementations[0].location == "src/a.swift"


def test_load_refuses_keys_that_differ_only_in_case(tmp_path):
    lettered = "abcdef00-0000-4000-8000-000000000000"

    def dup(d):
        d["entries"][lettered] = dict(d["entries"][U1], rdid="adc.recipe.b", path="b")
        d["entries"][lettered.upper()] = dict(d["entries"][U1], rdid="adc.recipe.c", path="c")
    _saved(tmp_path, dup)
    with pytest.raises(IndexFileError, match="differ only in case"):
        load_index(tmp_path)


def test_a_failed_save_leaves_no_tmp_file(tmp_path, monkeypatch):
    import cookr.core.index as index_mod

    def boom(src, dst):
        raise OSError("disk full")
    monkeypatch.setattr(index_mod.os, "replace", boom)
    with pytest.raises(OSError):
        save_index(Index(CB, {U1: Entry(U1, "recipe", "adc.recipe.a", "a")}), tmp_path)
    assert list(tmp_path.iterdir()) == []


def test_an_underivable_rdid_is_an_index_error(tmp_path):
    make_folder(tmp_path, "guidelines/Bad Name", U1)
    with pytest.raises(IndexFileError, match="Bad Name"):
        sync_from_folders(Index(CB), tmp_path)
