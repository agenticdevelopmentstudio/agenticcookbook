"""A command on one artifact folder costs what that folder needs: it never
walks the rest of the cookbook. Every directory listing a run makes is
recorded; none may fall inside the cookbook's other areas."""

from __future__ import annotations

import json
import os
from pathlib import Path

import pytest

from cookr.cli import main
from cookr.core import roles, rolework, roots
from cookr.core.artifact import Artifact, Part, find_folders, write_folder

from .cookbook_helpers import add_doc
from .test_research import TOPIC, roled, write_research
from .test_roles import make, parts

pytestmark = pytest.mark.usefixtures("git_tmp_path", "patch_refs")

#: Areas a walk of the whole cookbook lists and a one-folder command never needs.
ELSEWHERE = ("guidelines/testing", "principles")


def _cookbook(tmp_path, monkeypatch):
    cb, folder = roled(tmp_path, monkeypatch, cite=" (claim: fk-index)")
    write_research(folder)
    for i in range(3):
        f = add_doc(tmp_path, f"guidelines/testing/unit/decoy-{i}", f"# Decoy {i}\n\nText.\n",
                    type="guideline")
        (f.parent / f"{f.name}.md").unlink()
    f = add_doc(tmp_path, "principles/decoy", "# Decoy\n\nText.\n", type="principle")
    (f.parent / f"{f.name}.md").unlink()
    return cb, folder


def _listed(monkeypatch) -> list[Path]:
    """Every directory listed from now on (os.scandir and os.listdir: what
    rglob, os.walk and iterdir use)."""
    seen: list[Path] = []
    for name in ("scandir", "listdir"):
        real = getattr(os, name)

        def spy(path=".", _real=real):
            seen.append(Path(os.fspath(path)).absolute())
            return _real(path)
        monkeypatch.setattr(os, name, spy)
    return seen


@pytest.mark.parametrize("argv", [["roles", "check"], ["validate", "--research"]])
def test_a_one_folder_command_never_walks_the_rest_of_the_cookbook(argv, tmp_path, monkeypatch, capsys):
    cb, folder = _cookbook(tmp_path, monkeypatch)
    seen = _listed(monkeypatch)
    code = main(["-p", str(tmp_path), *argv, str(folder)])
    capsys.readouterr()
    assert code == 0
    away = [(cb / a).resolve() for a in ELSEWHERE]
    # Listing a type dir itself is one listing, not a walk; nothing below it may be listed.
    walked = sorted({str(d) for d in seen for a in away
                     if d.resolve().is_relative_to(a) and d.resolve() != a})
    assert walked == []


# ── one folder's census is the whole census, for that folder ─────────────────

def _unroled(root, rel, uid="u"):
    folder = root / rel
    write_folder(Artifact(meta={"id": uid, "type": rel.split("/")[0].rstrip("s")},
                          parts=[Part("intro", "# U\n")]), folder)
    return folder


def _layout(root, case):
    """(the roled folder checked, every folder in the cookbook) for `case`."""
    if case == "alone":
        mine = make(root)
    elif case == "twin-under-another-use-case":
        mine = make(root, "guidelines/implementing/data/t")
        make(root, "guidelines/planning/data/t")
    elif case == "long-names-twin":
        tail = "data/" + "a-very-long-topic-name-" * 3 + "t"
        mine = make(root, f"guidelines/implementing/{tail}")
        make(root, f"guidelines/planning/{tail}")
    elif case == "unroled-at-a-verifier-path":
        mine = make(root, "guidelines/planning/data/t")
        _unroled(root, "guidelines/verifying-build/data/t")
    elif case == "dashes-split-another-way":
        mine = make(root, "guidelines/implementing/data/x-t")
        _unroled(root, "guidelines/implementing/data-x/t")
        _unroled(root, "guidelines/reviewing-data/x/t", uid="v")
    elif case == "principle-and-guideline":
        mine = root / "principles" / "t"
        write_folder(Artifact(meta={"id": "t", "type": "principle"},
                              parts=parts()), mine)
        _unroled(root, "guidelines/reviewing/principle/t")
    elif case == "a-frozen-copy-is-no-folder":
        mine = make(root, "guidelines/implementing/data/t")
        frozen = root / "guidelines/planning/data/t"
        make(root, "guidelines/planning/data/t")
        (frozen / "versions").mkdir()
        _unroled(root, "guidelines/planning/data/t/versions/1")
    else:
        raise AssertionError(case)
    return mine


@pytest.mark.parametrize("case", ["alone", "twin-under-another-use-case", "long-names-twin",
                                  "unroled-at-a-verifier-path", "dashes-split-another-way",
                                  "principle-and-guideline", "a-frozen-copy-is-no-folder"])
def test_one_folders_census_matches_the_whole_census(case, tmp_path):
    root = tmp_path / "cookbook"
    mine = _layout(root, case)
    whole = [(f.kind, f.detail) for f in roles.census(find_folders([root])) if f.folder == mine]
    assert [(f.kind, f.detail) for f in roles.census_of(mine, root)] == whole


def test_a_collider_the_index_lists_off_the_usual_places_is_found(tmp_path, monkeypatch):
    cb, mine = roled(tmp_path, monkeypatch)
    other = add_doc(tmp_path, f"guidelines/misc/guidelines/verifying-build/{TOPIC.split('/', 2)[2]}",
                    "# Other\n\nText.\n", type="guideline")
    (other.parent / f"{other.name}.md").unlink()
    whole = [(f.kind, f.detail) for f in roles.census(find_folders([cb])) if f.folder == mine]
    assert [k for k, _ in whole] == ["name-collision"]
    assert [(f.kind, f.detail) for f in roles.census_of(mine, cb)] == whole


# ── one way to find the cookbook holding an artifact ─────────────────────────

def test_the_cookbook_of_an_artifact_is_found_one_way(tmp_path):
    package = Path(rolework.__file__).parent.parent
    defined = [f for f in package.rglob("*.py") if "def cookbook_of(" in f.read_text(encoding="utf-8")]
    assert defined == [Path(roots.__file__)]
    with_manifest = tmp_path / "a" / "cookbook"
    (with_manifest / "guidelines" / "x" / "t").mkdir(parents=True)
    (with_manifest / "cookbook.json").write_text("{}", encoding="utf-8")
    assert roots.cookbook_of(with_manifest / "guidelines" / "x" / "t") == with_manifest.resolve()
    by_type_dir = tmp_path / "b"
    (by_type_dir / "principles" / "t").mkdir(parents=True)
    assert roots.cookbook_of(by_type_dir / "principles" / "t") == by_type_dir.resolve()
    assert roots.cookbook_of(tmp_path / "c") is None


# ── one folder's index answers as the synced index does ──────────────────────

@pytest.mark.parametrize("since", ["nothing", "the-link-target-moved", "the-link-target-removed",
                                   "the-link-target-is-new"])
def test_one_folders_index_renders_as_the_synced_index(since, tmp_path, monkeypatch):
    from cookr.core.artifact import load_folder
    from cookr.core.index import IndexCache
    from cookr.core.skill import compose_all
    from .cookbook_helpers import new_repo

    monkeypatch.chdir(tmp_path)
    new_repo(tmp_path)
    other = add_doc(tmp_path, "guidelines/testing/unit/other", "# Other\n\nText.\n", type="guideline")
    uid = load_folder(other).meta["id"]
    mine = add_doc(tmp_path, "guidelines/testing/unit/mine",
                   f"# Mine\n\nSee [the other](cookbook:{uid}).\n", type="guideline",
                   **{"depends-on": [uid]})
    for f in (other, mine):
        (f.parent / f"{f.name}.md").unlink()
    cb = tmp_path / "cookbook"
    if since == "the-link-target-moved":
        other.rename(other.parent / "moved")
    elif since == "the-link-target-removed":
        import shutil
        shutil.rmtree(other)
    elif since == "the-link-target-is-new":
        index = json.loads((cb / "index.json").read_text(encoding="utf-8"))
        index["entries"].pop(uid)
        (cb / "index.json").write_text(json.dumps(index), encoding="utf-8")
    full = [s.text for s in compose_all(mine, indexes=IndexCache())]
    assert [s.text for s in compose_all(mine, indexes=IndexCache(one_folder=True))] == full
