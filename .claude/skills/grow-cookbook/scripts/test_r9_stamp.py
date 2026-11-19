"""r9_stamp.py and reference_format.r9_stale: an R9 `new-<name>.json` records
the hash of each reference it was measured against (1.4.33, G94).

    python3 -m pytest .claude/skills/grow-cookbook/scripts -q
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import r9_stamp  # noqa: E402
from reference_format import R9_FOLDER_HASH, R9_HASHES, blob_hash, folder_hash, r9_reference, r9_stale  # noqa: E402


def survivor(root: Path) -> Path:
    """A candidate survivor folder: the files cookr reads (artifact.json, *.md)."""
    d = root / "survivor"
    if not d.is_dir():
        (d / "parts").mkdir(parents=True)
        (d / "artifact.json").write_text('{"name": "survivor"}')
        (d / "parts" / "rules.md").write_text("Page by cursor.\n")
    return d


def r9(gaps: Path, name: str, refs: list, folder=None) -> Path:
    gaps.mkdir(parents=True, exist_ok=True)
    f = gaps / f"new-{name}.json"
    folder = str(survivor(gaps.parent)) if folder is None else folder
    f.write_text(json.dumps({"folder": folder, "references": [
        {"file": str(r), "sentences": 1, "held": 0, "lacking": 1, "lacking_sentences": ["x"]} for r in refs]}))
    return f


def test_blob_hash_is_what_git_hash_object_prints(tmp_path):
    f = tmp_path / "ref.txt"
    f.write_text("Never log a secret.\n")
    want = subprocess.run(["git", "hash-object", str(f)], capture_output=True, text=True, check=True).stdout.strip()
    assert blob_hash(f) == want


def test_a_stamped_r9_file_records_each_reference_and_is_current(tmp_path, capsys):
    ref = tmp_path / "reference" / "security--x.txt"
    ref.parent.mkdir()
    ref.write_text("Never log a secret.\n")
    f = r9(tmp_path / "gaps", "audit", [ref])
    assert r9_stamp.main([str(f)]) == 0
    data = json.loads(f.read_text())
    assert data[R9_HASHES] == {str(ref): blob_hash(ref)}
    assert data[R9_FOLDER_HASH] == folder_hash(tmp_path / "survivor")
    assert data["references"][0]["lacking_sentences"] == ["x"]          # the measure itself is kept
    assert r9_stale(tmp_path / "gaps") == []
    printed = json.loads(capsys.readouterr().out)
    assert printed == {"file": str(f), R9_HASHES: {str(ref): blob_hash(ref)},
                       R9_FOLDER_HASH: folder_hash(tmp_path / "survivor")}


def test_every_unstamped_changed_missing_or_unreadable_r9_file_is_stale(tmp_path):
    gaps = tmp_path / "gaps"
    ref = tmp_path / "a.txt"
    ref.write_text("one\n")
    other = tmp_path / "b.txt"
    other.write_text("two\n")
    unstamped = r9(gaps, "unstamped", [ref])
    changed = r9(gaps, "changed", [ref, other])
    gone = r9(gaps, "gone", [tmp_path / "missing.txt"])
    assert r9_stamp.main([str(changed)]) == 0
    other.write_text("two, changed\n")
    (gaps / "new-broken.json").write_text("{not json")
    (gaps / "authn.json").write_text("{}")                    # a topic's gaps file is never an R9 file
    (gaps / "home--authn.json").write_text("{}")
    rows = r9_stale(gaps)
    assert [(r["file"], r["reason"]) for r in rows] == [
        ("new-broken.json", "unreadable"), ("new-changed.json", "changed"),
        ("new-gone.json", "missing_reference"), ("new-gone.json", "folder_no_hash"),
        ("new-unstamped.json", "no_hash"), ("new-unstamped.json", "folder_no_hash")], rows
    by = {r["file"]: r for r in rows if r["input"] != "folder"}
    assert by["new-changed.json"]["reference"] == str(other)
    assert by["new-changed.json"]["recorded"] != by["new-changed.json"]["current"] == blob_hash(other)
    assert by["new-unstamped.json"]["recorded"] is None and by["new-unstamped.json"]["current"] == blob_hash(ref)
    assert all("r9_stamp.py" in r["why"] for r in rows)
    assert unstamped.is_file() and gone.is_file()
    assert r9_stale(tmp_path / "no-such-folder") == []


def test_a_stamp_on_a_reference_since_removed_from_the_file_is_still_current_only_for_listed_ones(tmp_path):
    # Only the references the file lists are compared; an extra recorded hash is harmless.
    gaps = tmp_path / "gaps"
    ref = tmp_path / "a.txt"
    ref.write_text("one\n")
    f = r9(gaps, "x", [ref])
    data = json.loads(f.read_text())
    data[R9_HASHES] = {str(ref): blob_hash(ref), "/elsewhere.txt": "0" * 40}
    data[R9_FOLDER_HASH] = folder_hash(tmp_path / "survivor")
    f.write_text(json.dumps(data))
    assert r9_stale(gaps) == []


def test_stamping_an_unreadable_or_unlisted_file_fails_and_writes_nothing(tmp_path, capsys):
    bad = tmp_path / "new-x.json"
    bad.write_text("{not json")
    assert r9_stamp.main([str(bad)]) == 2
    assert bad.read_text() == "{not json"
    empty = tmp_path / "new-y.json"
    empty.write_text(json.dumps({"references": []}))
    assert r9_stamp.main([str(empty)]) == 2
    assert json.loads(empty.read_text()) == {"references": []}
    ref_gone = r9(tmp_path, "z", [tmp_path / "missing.txt"])
    before = ref_gone.read_text()
    assert r9_stamp.main([str(ref_gone)]) == 2
    assert ref_gone.read_text() == before
    assert r9_stamp.main([str(tmp_path / "authn.json")]) == 2       # not an R9 file name


# ---- fix round 1 (1.4.34): review I2 and M6 ----

def test_the_folder_hash_covers_the_files_cookr_reads(tmp_path):
    d = survivor(tmp_path)
    h = folder_hash(d)
    (d / "notes.txt").write_text("not read by cookr\n")
    assert folder_hash(d) == h
    (d / "parts" / "rules.md").write_text("Page by offset.\n")
    assert folder_hash(d) != h
    (d / "parts" / "rules.md").write_text("Page by cursor.\n")
    assert folder_hash(d) == h
    (d / "parts" / "rules.md").rename(d / "parts" / "other.md")      # a rename is a change
    assert folder_hash(d) != h


def test_a_survivor_edited_after_the_stamp_is_folder_changed(tmp_path):
    # review I2: the R9 measure's other input is the survivor folder
    ref = tmp_path / "a.txt"
    ref.write_text("one\n")
    f = r9(tmp_path / "gaps", "x", [ref])
    assert r9_stamp.main([str(f)]) == 0
    assert r9_stale(tmp_path / "gaps") == []
    (tmp_path / "survivor" / "parts" / "rules.md").write_text("Page by offset.\n")
    rows = r9_stale(tmp_path / "gaps")
    assert [(r["file"], r["input"], r["reason"]) for r in rows] == [("new-x.json", "folder", "folder_changed")], rows
    assert rows[0]["reference"] == str(tmp_path / "survivor") and rows[0]["current"] == folder_hash(
        tmp_path / "survivor") != rows[0]["recorded"]
    assert "r9_stamp.py" in rows[0]["why"]


def test_a_stamp_with_no_folder_hash_or_a_gone_folder_is_stale(tmp_path):
    ref = tmp_path / "a.txt"
    ref.write_text("one\n")
    f = r9(tmp_path / "gaps", "x", [ref])
    assert r9_stamp.main([str(f)]) == 0
    data = json.loads(f.read_text())
    del data[R9_FOLDER_HASH]                                         # a 1.4.33 stamp
    f.write_text(json.dumps(data))
    assert [(r["input"], r["reason"]) for r in r9_stale(tmp_path / "gaps")] == [("folder", "folder_no_hash")]
    gone = r9(tmp_path / "gaps2", "y", [ref], folder=str(tmp_path / "no-such-survivor"))
    assert [(r["input"], r["reason"]) for r in r9_stale(tmp_path / "gaps2")] == [
        ("reference", "no_hash"), ("folder", "missing_folder")]
    assert r9_stamp.main([str(gone)]) == 2                           # nothing to hash: refused


def test_an_empty_references_list_or_no_folder_is_unreadable(tmp_path):
    # review M6.1: r9_stamp refuses it, so r9_stale lists it
    gaps = tmp_path / "gaps"
    gaps.mkdir()
    (gaps / "new-empty.json").write_text(json.dumps({"folder": str(survivor(tmp_path)), "references": []}))
    (gaps / "new-nofolder.json").write_text(json.dumps({"references": [{"file": "/a.txt"}]}))
    assert [(r["file"], r["reason"]) for r in r9_stale(gaps)] == [
        ("new-empty.json", "unreadable"), ("new-nofolder.json", "unreadable")]


def test_a_relative_reference_resolves_against_the_area_never_the_cwd(tmp_path, monkeypatch):
    # review M6.2: a same-named file under the cwd is never read
    ws = tmp_path / "ws"
    a = ws / "areas" / "data" / "rows-area"
    ref = a / "reference" / "x.txt"
    ref.parent.mkdir(parents=True)
    ref.write_text("Index every key.\n")
    written = "areas/data/rows-area/reference/x.txt"                  # relative to the workspace
    f = r9(a / "gaps", "x", [written])
    elsewhere = tmp_path / "elsewhere"
    (elsewhere / "areas" / "data" / "rows-area" / "reference").mkdir(parents=True)
    (elsewhere / written).write_text("A decoy.\n")
    (elsewhere / "reference").mkdir()
    (elsewhere / "reference" / "x.txt").write_text("Another decoy.\n")
    monkeypatch.chdir(elsewhere)
    assert r9_stamp.main([str(f)]) == 0
    assert json.loads(f.read_text())[R9_HASHES] == {written: blob_hash(ref)}
    assert r9_stale(a / "gaps") == []
    ref.write_text("Index every foreign key.\n")
    assert [r["reason"] for r in r9_stale(a / "gaps")] == ["changed"]
    g = r9(a / "gaps", "y", ["reference/x.txt"])                       # relative to the area
    assert r9_stamp.main([str(g)]) == 0
    assert json.loads(g.read_text())[R9_HASHES] == {"reference/x.txt": blob_hash(ref)}
    lost = r9(a / "gaps", "z", ["reference/only-in-cwd.txt"])
    (elsewhere / "reference" / "only-in-cwd.txt").write_text("cwd only\n")
    assert r9_stamp.main([str(lost)]) == 2
    assert ("new-z.json", "missing_reference") in [(r["file"], r["reason"]) for r in r9_stale(a / "gaps")]


def test_a_relative_path_found_nowhere_above_the_area_resolves_against_the_repo(tmp_path):
    # review M6.2 (fix round 1): the lookup climbs from the area only up to the
    # folder that holds the workspace, then tries the repo; a same-named file
    # higher up is never read.
    outer = tmp_path / "outer"
    gaps = outer / "ws" / "areas" / "data" / "rows-area" / "gaps"
    gaps.mkdir(parents=True)
    rel = "cookbook/guidelines/data/rows/rules.md"
    repo = tmp_path / "repo"
    for root, text in ((repo, "Index every key.\n"), (tmp_path, "A decoy above the workspace.\n")):
        (root / rel).parent.mkdir(parents=True, exist_ok=True)
        (root / rel).write_text(text)
    assert r9_reference(rel, gaps, repo) == repo / rel
    (outer / rel).parent.mkdir(parents=True)
    (outer / rel).write_text("Beside the workspace.\n")
    assert r9_reference(rel, gaps, repo) == outer / rel                # the workspace's folder comes first
    f = r9(gaps, "rows", [rel], folder="cookbook/guidelines/data/rows")
    assert r9_stamp.main([str(f), "--repo", str(repo)]) == 0
    assert json.loads(f.read_text())[R9_HASHES] == {rel: blob_hash(outer / rel)}
    assert json.loads(f.read_text())[R9_FOLDER_HASH] == folder_hash(outer / "cookbook/guidelines/data/rows")
