"""Conformance hashing, effective state, and `confirm`."""

from __future__ import annotations

import json

import pytest

from cookr.cli import main
from cookr.core.conformance import effective_state, level_between, location_hash
from cookr.core.index import Conformance, Implementation, load_index
from cookr.core.inventory import ignore_set

from .cookbook_helpers import add_spec, new_repo

NONE = ignore_set(())
ROOT = {"path": "web", "platform": "web", "kind": "ui", "group": "ui"}


def _impl(state="confirmed", version="1.0.0", hash="sha256:a"):
    return Implementation("web", "web/x.ts", Conformance(state, version, hash))


def _repo(tmp_path, version="1.0.0"):
    repo = new_repo(tmp_path / "r", [ROOT])
    (repo / "web" / "x.ts").write_text("export const a = 1\n", encoding="utf-8")
    add_spec(repo, "ui/x", meta={"version": version}, impls=[("web", "web/x.ts")])
    return repo


def _bump(repo, version):
    p = repo / "cookbook" / "ui" / "x" / "artifact.json"
    data = json.loads(p.read_text(encoding="utf-8"))
    data["meta"]["version"] = version
    p.write_text(json.dumps(data, indent=2), encoding="utf-8")


def test_hash_changes_when_file_changes(tmp_path):
    (tmp_path / "d").mkdir()
    f = tmp_path / "d" / "a.ts"
    f.write_text("one", encoding="utf-8")
    before = location_hash(tmp_path, "d/", NONE)
    assert before.startswith("sha256:")
    f.write_text("two", encoding="utf-8")
    assert location_hash(tmp_path, "d/", NONE) != before
    assert location_hash(tmp_path, "d/a.ts", NONE) == location_hash(tmp_path, "d/a.ts", NONE)


def test_hash_ignores_ignored_files(tmp_path):
    (tmp_path / "d").mkdir()
    (tmp_path / "d" / "a.ts").write_text("one", encoding="utf-8")
    ignore = ignore_set(("**/*.stories.ts",))
    before = location_hash(tmp_path, "d/", ignore)
    (tmp_path / "d" / "a.stories.ts").write_text("noise", encoding="utf-8")
    assert location_hash(tmp_path, "d/", ignore) == before


def test_confirmed_flips_on_code_change():
    assert effective_state(_impl(), "1.0.0", "sha256:a") == "confirmed"
    assert effective_state(_impl(), "1.0.0", "sha256:b") == "needs-validation"
    assert effective_state(_impl(), "1.0.0", None) == "confirmed"
    assert effective_state(_impl("unverified"), "2.0.0", "sha256:b") == "unverified"
    assert effective_state(_impl("planned", None, None), "2.0.0", None) == "planned"


def test_patch_bump_keeps_confirmed():
    assert level_between("1.0.0", "1.0.3") == "patch"
    assert effective_state(_impl(), "1.0.3", "sha256:a") == "confirmed"


def test_minor_bump_needs_validation():
    assert level_between("1.0.0", "1.1.0") == "minor"
    assert level_between("1.0.0", "2.0.0") == "major"
    assert effective_state(_impl(), "1.1.0", "sha256:a") == "needs-validation"
    assert effective_state(_impl(), "2.0.0", "sha256:a") == "needs-validation"


def test_confirm_records_version_and_hash(tmp_path, capsys):
    repo = _repo(tmp_path, "1.2.0")
    assert main(["-p", str(repo), "confirm", "test-repo.ingredient.ui.x"]) == 0
    row = next(iter(load_index(repo / "cookbook").entries.values())).implementations[0]
    assert (row.conformance.state, row.conformance.version) == ("confirmed", "1.2.0")
    assert row.conformance.hash.startswith("sha256:")


def test_confirm_refuses(tmp_path, capsys):
    repo = _repo(tmp_path)
    assert main(["-p", str(repo), "confirm", "nope.nope"]) == 1
    assert main(["-p", str(repo), "confirm", "test-repo.ingredient.ui.x", "--platform", "ios"]) == 1
    assert main(["-p", str(repo), "confirm", "test-repo.ingredient.ui.x", "--platform", "bad"]) == 2
    (repo / "web" / "x.ts").unlink()
    assert main(["-p", str(repo), "confirm", "test-repo.ingredient.ui.x"]) == 1


def test_confirm_url_stores_no_hash(tmp_path):
    repo = _repo(tmp_path)
    assert main(["-p", str(repo), "implements", "test-repo.ingredient.ui.x",
                 "https://example.com/x", "--platform", "python"]) == 0
    assert main(["-p", str(repo), "confirm", "test-repo.ingredient.ui.x",
                 "--location", "https://example.com/x"]) == 0
    rows = next(iter(load_index(repo / "cookbook").entries.values())).implementations
    url = next(r for r in rows if r.platform == "python")
    assert url.conformance.state == "confirmed" and url.conformance.hash is None


def test_unparseable_versions_never_read_as_conformant():
    for bad in ("", "1.2", "1.2.0-rc1"):
        assert level_between("1.0.0", bad) == "none"
        assert level_between(bad, "1.0.0") == "none"
        assert effective_state(_impl(), bad, "sha256:a") == "needs-validation"


def test_confirmed_with_no_stored_hash_on_a_file_needs_validation():
    assert effective_state(_impl(hash=None), "1.0.0", "sha256:a") == "needs-validation"
    url = Implementation("python", "https://example.com/x", Conformance("confirmed", "1.0.0"))
    assert effective_state(url, "1.0.0", None) == "confirmed"


@pytest.mark.parametrize("location", ["https://example.com/x", "src/a.py"])
def test_confirmed_with_no_stored_version_needs_validation(location):
    # `confirm` always records the version; a row without one was hand-edited
    # and says nothing about which version the code matches.
    row = Implementation("python", location, Conformance("confirmed", None, "sha256:a"))
    assert effective_state(row, "1.0.0", None) == "needs-validation"


def test_missing_location_needs_validation():
    assert effective_state(_impl(), "1.0.0", None, missing=True) == "needs-validation"


def test_directory_hash_covers_nested_files_and_dot(tmp_path):
    (tmp_path / "d" / "sub" / "deep").mkdir(parents=True)
    nested = tmp_path / "d" / "sub" / "deep" / "n.ts"
    nested.write_text("one", encoding="utf-8")
    for loc in ("d/", "."):
        before = location_hash(tmp_path, loc, NONE)
        nested.write_text("two", encoding="utf-8")
        assert location_hash(tmp_path, loc, NONE) != before
        nested.write_text("one", encoding="utf-8")
    ignore = ignore_set(("d/sub/**",))
    before = location_hash(tmp_path, ".", ignore)
    nested.write_text("three", encoding="utf-8")
    assert location_hash(tmp_path, ".", ignore) == before


def test_confirm_a_planned_row(tmp_path):
    repo = _repo(tmp_path)
    assert main(["-p", str(repo), "implements", "test-repo.ingredient.ui.x", "web/p.ts",
                 "--platform", "ios", "--planned"]) == 0
    assert main(["-p", str(repo), "confirm", "test-repo.ingredient.ui.x", "--platform", "ios"]) == 1
    (repo / "web" / "p.ts").write_text("x", encoding="utf-8")
    assert main(["-p", str(repo), "confirm", "test-repo.ingredient.ui.x", "--platform", "ios"]) == 0
    rows = next(iter(load_index(repo / "cookbook").entries.values())).implementations
    assert next(r for r in rows if r.platform == "ios").conformance.state == "confirmed"


@pytest.mark.parametrize("where", ["../outside.ts", "OUTSIDE_ABS", "~/outside.ts"])
def test_implements_refuses_a_location_outside_the_repo(tmp_path, capsys, where):
    repo = _repo(tmp_path)
    (tmp_path / "outside.ts").write_text("x\n", encoding="utf-8")
    loc = str(tmp_path / "outside.ts") if where == "OUTSIDE_ABS" else where
    before = (repo / "cookbook" / "index.json").read_text(encoding="utf-8")
    capsys.readouterr()
    assert main(["-p", str(repo), "implements", "test-repo.ingredient.ui.x", loc,
                 "--platform", "web"]) == 2
    assert "inside the repo" in " ".join(capsys.readouterr().out.split())
    assert (repo / "cookbook" / "index.json").read_text(encoding="utf-8") == before


def test_confirm_refuses_a_hand_edited_row_outside_the_repo(tmp_path, capsys):
    repo = _repo(tmp_path)
    (tmp_path / "outside.ts").write_text("x\n", encoding="utf-8")
    index = repo / "cookbook" / "index.json"
    index.write_text(index.read_text(encoding="utf-8").replace('"web/x.ts"', '"../outside.ts"'),
                     encoding="utf-8")
    before = index.read_text(encoding="utf-8")
    capsys.readouterr()
    assert main(["-p", str(repo), "confirm", "test-repo.ingredient.ui.x"]) == 2
    assert "../outside.ts" in capsys.readouterr().out
    assert index.read_text(encoding="utf-8") == before


def test_location_hash_refuses_a_location_outside_the_repo(tmp_path):
    from cookr.core.errors import CookbookError

    (tmp_path / "r").mkdir()
    (tmp_path / "x.ts").write_text("x", encoding="utf-8")
    for loc in ("../x.ts", str(tmp_path / "x.ts")):
        with pytest.raises(CookbookError):
            location_hash(tmp_path / "r", loc, NONE)


def test_unreadable_artifact_confirm_refuses_and_status_flags(tmp_path, capsys):
    repo = _repo(tmp_path)
    assert main(["-p", str(repo), "confirm", "test-repo.ingredient.ui.x"]) == 0
    _bump(repo, "not-a-version")
    assert main(["-p", str(repo), "confirm", "test-repo.ingredient.ui.x"]) == 1
    capsys.readouterr()
    assert main(["-p", str(repo), "status", "--json"]) == 0
    assert json.loads(capsys.readouterr().out)["implementations"][0]["state"] == "needs-validation"
    (repo / "cookbook" / "ui" / "x" / "artifact.json").write_text("{", encoding="utf-8")
    assert main(["-p", str(repo), "confirm", "test-repo.ingredient.ui.x"]) == 1
