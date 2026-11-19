"""copy_check.py: every difference between a merged copy and its survivor,
and every file linking the copy's UUID (G58, 1.4.24)."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import copy_check  # noqa: E402

AREA = "planning/networking"
SURV = "cookbook/guidelines/implementing/networking/api-design"
COPY = f"cookbook/guidelines/{AREA}/api-design"
CID, SID = "6079c539-f547-46de-9284-d404a76f6d9d", "49399746-a81f-4163-8b07-0cfa11d87c2e"


def topic(repo: Path, folder: str, uid: str, version: str, refs: list, parts: dict) -> None:
    d = repo / folder
    d.mkdir(parents=True)
    meta = {"id": uid, "title": "API Design", "version": version, "references": refs, "related": []}
    (d / "artifact.json").write_text(json.dumps({"meta": meta, "parts": [{"part": p} for p in parts]}),
                                     encoding="utf-8")
    for p, text in parts.items():
        (d / f"{p}.md").write_text(text, encoding="utf-8")


def setup(tmp: Path, same: bool = False) -> tuple[Path, Path]:
    repo = tmp / "repo"
    intro = "Use REST. See [paging](https://example.com/paging) and cookbook:aaaaaaaa-0000-0000-0000-000000000001.\n"
    topic(repo, SURV, SID, "1.0.3", [], {"intro": intro, "history": "- 1.0.3 done\n"})
    if same:
        topic(repo, COPY, CID, "1.0.3", [], {"intro": intro, "history": "- 1.0.3 done\n"})
    else:
        topic(repo, COPY, CID, "1.0.4", ["https://www.rfc-editor.org/rfc/rfc8594.html"],
              {"intro": intro.replace("example.com/paging", "example.com/pages"), "history": "- 1.0.4 done\n",
               "extra": "More.\n"})
    other = repo / "cookbook/guidelines/planning/networking/api-style/artifact.json"
    other.parent.mkdir(parents=True)
    other.write_text(json.dumps({"meta": {"id": "x", "related": [CID]}, "parts": []}), encoding="utf-8")
    md = repo / "cookbook/guidelines/reviewing/networking/contract/intro.md"
    md.parent.mkdir(parents=True)
    md.write_text(f"Read cookbook:{CID} first.\n", encoding="utf-8")
    ws = tmp / "ws"
    plan = ws / "areas" / AREA / "area-plan.md"
    plan.parent.mkdir(parents=True)
    plan.write_text("# Plan\n\n## Proposed topics\n\n| Topic | Action | Artifact | Why |\n|---|---|---|---|\n"
                    f"| api-design | merged | `{SURV}` | copy |\n| own | kept | `cookbook/guidelines/{AREA}/own` | x |\n",
                    encoding="utf-8")
    (ws / "worklist.json").write_text(json.dumps({"batches": [{"topics": [{
        "topic": "api-design", "survivor": SURV.removeprefix("cookbook/"),
        "copies": [{"folder": COPY.removeprefix("cookbook/"), "identical": True, "exact": True}]}]}]}),
        encoding="utf-8")
    return repo, ws


def test_every_difference_and_every_linking_file_is_listed(tmp_path):
    repo, ws = setup(tmp_path)
    out = copy_check.check(AREA, ws, repo)
    assert out["area"] == AREA and len(out["copies"]) == 1
    c = out["copies"][0]
    assert (c["topic"], c["copy"], c["survivor"], c["from"]) == ("api-design", COPY, SURV, ["plan", "worklist"])
    assert c["worklist_says"] == {"identical": True, "exact": True}
    assert c["identical"] is False
    assert c["parts"]["only_copy"] == ["extra"] and c["parts"]["only_survivor"] == []
    assert c["parts"]["differ"] == []     # G107: history/intro listed apart
    assert [d["part"] for d in c["parts"]["differ_uncarried"]] == ["history", "intro"]
    assert any("1.0.4" in line for line in c["parts"]["differ_uncarried"][0]["diff"])
    meta = {m["key"]: (m["copy"], m["survivor"]) for m in c["meta"]}
    assert meta["version"] == ("1.0.4", "1.0.3")
    assert meta["references"] == (["https://www.rfc-editor.org/rfc/rfc8594.html"], [])
    assert "id" not in meta
    assert c["links"] == {"only_copy": ["https://example.com/pages"], "only_survivor": ["https://example.com/paging"]}
    assert c["linked_by"] == ["cookbook/guidelines/planning/networking/api-style/artifact.json",
                              "cookbook/guidelines/reviewing/networking/contract/intro.md"]


def test_an_identical_copy_says_so_and_still_names_its_linkers(tmp_path):
    repo, ws = setup(tmp_path, same=True)
    c = copy_check.check(AREA, ws, repo)["copies"][0]
    assert c["identical"] is True and c["meta"] == [] and c["parts"]["differ"] == []
    assert len(c["linked_by"]) == 2


def test_a_copy_folder_that_does_not_exist_is_a_move_listed_apart(tmp_path):
    repo, ws = setup(tmp_path)
    import shutil
    shutil.rmtree(repo / COPY)
    out = copy_check.check(AREA, ws, repo)
    assert out["copies"] == [] and out["moved"] == [{"topic": "api-design", "copy": COPY, "survivor": SURV}]


def test_cli_prints_json_from_any_directory(tmp_path):
    repo, ws = setup(tmp_path)
    r = subprocess.run([sys.executable, "-I", str(HERE / "copy_check.py"), AREA, "--workspace", str(ws),
                        "--repo", str(repo)], capture_output=True, text=True, cwd=tmp_path)
    assert r.returncode == 0, r.stderr
    assert json.loads(r.stdout)["copies"][0]["identical"] is False
    r = subprocess.run([sys.executable, "-I", str(HERE / "copy_check.py"), AREA, "--workspace", str(tmp_path / "no"),
                        "--repo", str(repo)], capture_output=True, text=True, cwd=tmp_path)
    assert r.returncode == 2 and "worklist.json" in r.stderr


def test_a_copy_differing_only_in_its_meta_is_not_identical(tmp_path):
    # G58 (1.4.24): a meta difference (version, references) alone is a
    # difference the fold must carry.
    repo, ws = setup(tmp_path, same=True)
    art = repo / COPY / "artifact.json"
    data = json.loads(art.read_text())
    data["meta"]["references"] = ["https://www.rfc-editor.org/rfc/rfc8594.html"]
    art.write_text(json.dumps(data))
    c = copy_check.check(AREA, ws, repo)["copies"][0]
    assert c["parts"]["differ"] == [] and c["meta"] != []
    assert c["identical"] is False


# 1.4.25 G74: incoming copies, twin_differs first, linkers that are copies.

def _worklist(ws: Path, topics: list) -> None:
    (ws / "worklist.json").write_text(json.dumps({"batches": [{"topics": topics}]}), encoding="utf-8")


def test_every_row_has_a_direction_and_incoming_copies_are_listed(tmp_path):
    # A worklist copy in another area whose survivor is in this area is
    # incoming, planned or not; this area's own copies are outgoing.
    repo, ws = setup(tmp_path)
    inc = "cookbook/guidelines/reviewing/networking/own"
    topic(repo, f"cookbook/guidelines/{AREA}/own", "11111111-0000-4000-8000-000000000001", "1.0.0", [],
          {"intro": "Own.\n"})
    topic(repo, inc, "11111111-0000-4000-8000-000000000002", "1.0.1", [], {"intro": "Own, reviewed.\n"})
    _worklist(ws, [{"topic": "api-design", "survivor": SURV.removeprefix("cookbook/"),
                    "copies": [{"folder": COPY.removeprefix("cookbook/"), "identical": True, "exact": True}]},
                   {"topic": "own", "survivor": f"guidelines/{AREA}/own",
                    "copies": [{"folder": inc.removeprefix("cookbook/"), "identical": True, "exact": True}]}])
    rows = {c["copy"]: c for c in copy_check.check(AREA, ws, repo)["copies"]}
    assert rows[COPY]["direction"] == "out"
    assert rows[inc]["direction"] == "in" and rows[inc]["survivor"] == f"cookbook/guidelines/{AREA}/own"
    assert rows[inc]["from"] == ["worklist"] and rows[inc]["identical"] is False


def test_an_owner_recorded_twin_differs_is_reported_first(tmp_path):
    # twin_differs sits at the top of artifact.json, beside meta: it is
    # compared, makes the copy not identical, and leads the row and the result.
    repo, ws = setup(tmp_path, same=True)
    art = repo / COPY / "artifact.json"
    data = json.loads(art.read_text())
    data["twin_differs"] = "The planning copy keeps the original text."
    data["meta"]["triggers"] = ["api"]
    data["meta"]["platforms"] = ["web"]
    art.write_text(json.dumps(data))
    out = copy_check.check(AREA, ws, repo)
    assert list(out)[1] == "twin_differs"
    assert out["twin_differs"] == [{"copy": COPY, "survivor": SURV,
                                    "copy_says": "The planning copy keeps the original text.",
                                    "survivor_says": None}]
    c = out["copies"][0]
    assert list(c)[0] == "twin_differs" and c["twin_differs"]["copy_says"].startswith("The planning copy")
    assert c["identical"] is False
    assert {m["key"] for m in c["meta"]} == {"triggers", "platforms"}
    assert c["top"] == [{"key": "twin_differs", "copy": "The planning copy keeps the original text.",
                         "survivor": None}]


def test_a_linking_file_that_is_itself_a_folded_copy_is_flagged(tmp_path):
    repo, ws = setup(tmp_path, same=True)
    other = "cookbook/guidelines/reviewing/networking/contract"
    _worklist(ws, [{"topic": "api-design", "survivor": SURV.removeprefix("cookbook/"),
                    "copies": [{"folder": COPY.removeprefix("cookbook/"), "identical": True, "exact": True}]},
                   {"topic": "contract", "survivor": "guidelines/implementing/networking/contract",
                    "copies": [{"folder": other.removeprefix("cookbook/")}]}])
    c = copy_check.check(AREA, ws, repo)["copies"][0]
    assert c["linked_by_folded"] == [{"file": f"{other}/intro.md", "copy": other}]
    assert len(c["linked_by"]) == 2


def test_a_linking_file_folded_by_another_areas_plan_is_flagged(tmp_path):
    # 1.4.26 (M6): the linking file's folder is no worklist copy, but another
    # area's plan merges it away: it is flagged too, so its link moves.
    repo, ws = setup(tmp_path, same=True)
    other = "cookbook/guidelines/reviewing/networking/contract"
    plan = ws / "areas" / "reviewing/networking" / "area-plan.md"
    plan.parent.mkdir(parents=True)
    plan.write_text("# Plan\n\n## Proposed topics\n\n| Topic | Action | Artifact | Why |\n|---|---|---|---|\n"
                    "| contract | merged | `cookbook/guidelines/implementing/networking/contract` | copy |\n",
                    encoding="utf-8")
    c = copy_check.check(AREA, ws, repo)["copies"][0]
    assert c["linked_by_folded"] == [{"file": f"{other}/intro.md", "copy": other}]


# 1.4.33: G106 stamps, G107 --summary, kept rows, history/intro apart.

def test_a_sync_or_approval_stamp_is_listed_under_stamps_never_against_identical(tmp_path):
    # G106: `synced` (top) and the approval/modified stamps (meta) are never
    # carried by a fold: listed under `stamps`, out of `top`/`meta`, and a
    # copy differing only in them is identical.
    repo, ws = setup(tmp_path, same=True)
    for folder, stamp in ((COPY, "2026-01-01"), (SURV, "2026-02-02")):
        art = repo / folder / "artifact.json"
        data = json.loads(art.read_text())
        data["synced"] = stamp
        data["meta"].update({"approved-by": folder, "approved-date": stamp, "modified": stamp})
        art.write_text(json.dumps(data))
    c = copy_check.check(AREA, ws, repo)["copies"][0]
    assert c["identical"] is True and c["top"] == [] and c["meta"] == []
    assert c["stamps"] == [
        {"key": "synced", "copy": "2026-01-01", "survivor": "2026-02-02"},
        {"key": "meta.approved-by", "copy": COPY, "survivor": SURV},
        {"key": "meta.approved-date", "copy": "2026-01-01", "survivor": "2026-02-02"},
        {"key": "meta.modified", "copy": "2026-01-01", "survivor": "2026-02-02"}]


def test_history_and_intro_differences_are_listed_apart_from_carried_parts(tmp_path):
    # G107: a fold never carries `history`/`intro` as content; their diffs
    # sit in `parts.differ_uncarried`, the carried parts' in `parts.differ`.
    repo, ws = setup(tmp_path)
    (repo / SURV / "artifact.json").write_text(json.dumps({**json.loads((repo / SURV / "artifact.json").read_text()),
                                                           "parts": [{"part": "intro"}, {"part": "history"},
                                                                     {"part": "extra"}]}))
    (repo / SURV / "extra.md").write_text("Less.\n")
    c = copy_check.check(AREA, ws, repo)["copies"][0]
    assert [d["part"] for d in c["parts"]["differ"]] == ["extra"]
    assert [d["part"] for d in c["parts"]["differ_uncarried"]] == ["history", "intro"]
    assert c["identical"] is False


def test_a_twin_the_copys_plan_keeps_is_marked_kept(tmp_path):
    # G107: a worklist copy its own area's plan keeps (the row's Artifact is
    # the copy itself) is `kept: true`, a merged copy `kept: false`.
    repo, ws = setup(tmp_path)
    plan = ws / "areas" / AREA / "area-plan.md"
    plan.write_text(plan.read_text().replace(f"| api-design | merged | `{SURV}` | copy |",
                                             f"| api-design | kept | `{COPY}` | twin |"))
    assert copy_check.check(AREA, ws, repo)["copies"][0]["kept"] is True
    repo2, ws2 = setup(tmp_path / "two")
    assert copy_check.check(AREA, ws2, repo2)["copies"][0]["kept"] is False


def test_summary_prints_names_only_never_a_diff(tmp_path):
    # G107: --summary prints each row with the names of what differs (parts,
    # meta, top, stamps, links) and no diff lines.
    repo, ws = setup(tmp_path)
    for folder, text in ((SURV, "Page by cursor.\n"), (COPY, "Page by offset.\n")):     # a carried part differs
        art = repo / folder / "artifact.json"
        data = json.loads(art.read_text(encoding="utf-8"))
        data["parts"].append({"part": "rules"})
        art.write_text(json.dumps(data), encoding="utf-8")
        (repo / folder / "rules.md").write_text(text, encoding="utf-8")
    r = subprocess.run([sys.executable, "-I", str(HERE / "copy_check.py"), AREA, "--workspace", str(ws),
                        "--repo", str(repo), "--summary"], capture_output=True, text=True, cwd=tmp_path)
    assert r.returncode == 0, r.stderr
    c = json.loads(r.stdout)["copies"][0]
    assert c["parts"] == {"only_copy": ["extra"], "differ": ["rules"],     # G175: empty only_survivor left out
                          "differ_uncarried": [{"part": "history", "first_line": "-- 1.0.3 done"},
                                               {"part": "intro", "first_line": c["parts"]["differ_uncarried"][1]
                                                ["first_line"]}]}
    assert c["parts"]["differ_uncarried"][1]["first_line"].startswith("-Use REST.")
    # G143 (1.4.36): each meta key with its values, cut to 80 characters
    assert c["meta"] == [{"key": "references", "copy": '["https://www.rfc-editor.org/rfc/rfc8594.html"]',
                          "survivor": "[]"}, {"key": "version", "copy": "1.0.4", "survivor": "1.0.3"}]
    assert "top" not in c and "stamps" not in c        # G175 (1.4.37): empty fields left out
    assert c["links"] == {"only_copy": ["https://example.com/pages"], "only_survivor": ["https://example.com/paging"]}
    assert c["identical"] is False and "kept" not in c and '"diff"' not in r.stdout


def test_a_long_meta_value_is_cut_to_80_characters():
    assert copy_check._cut("x" * 200) == "x" * 79 + "…" and copy_check._cut(None) is None
    assert copy_check._cut(["a"]) == '["a"]'


def test_the_digest_is_one_line_and_changes_when_a_survivor_file_changes(tmp_path):
    # G133 (1.4.36): `--digest` prints the line the plan records under Overlaps.
    repo, ws = setup(tmp_path)
    args = [sys.executable, "-I", str(HERE / "copy_check.py"), "--area", AREA, "--workspace", str(ws),
            "--repo", str(repo), "--digest"]
    r = subprocess.run(args, capture_output=True, text=True, cwd=tmp_path)
    assert r.returncode == 0, r.stderr
    line = r.stdout.strip()
    assert line.startswith(f"copy_check.py {AREA}: copies 1; identical 0; moved 0; unreadable 0; twin_differs 0; "
                           "differ_uncarried api-design:history,api-design:intro; result "), line
    assert line == copy_check.digest(copy_check.check(AREA, ws, repo))
    (repo / SURV / "history.md").write_text("- 1.0.3 done, again\n", encoding="utf-8")
    assert subprocess.run(args, capture_output=True, text=True).stdout.strip() != line


def test_summary_drops_the_fields_with_no_difference():
    # G175 (N26): a --summary row keeps who it is (topic, copy, survivor,
    # direction, from) and `identical`, and drops each field
    # with nothing in it; an identical copy is that row alone.
    same = {"twin_differs": None, "topic": "t", "copy": "cookbook/guidelines/a/t", "survivor": "cookbook/guidelines/b/t",
            "direction": "out", "from": ["worklist"], "worklist_says": None, "identical": True, "top": [],
            "parts": {"only_copy": [], "only_survivor": [], "differ": [], "differ_uncarried": []}, "meta": [],
            "stamps": [], "kept": False, "links": {"only_copy": [], "only_survivor": []}, "linked_by": [],
            "linked_by_folded": []}
    linked = {**same, "copy": "cookbook/guidelines/a/u", "linked_by": ["cookbook/guidelines/c/x/rules.md"],
              "stamps": [{"key": "synced", "copy": 1, "survivor": 2}], "kept": True}
    out = copy_check.summary({"area": "a", "copies": [same, linked], "moved": [], "unreadable": [],
                              "twin_differs": []})
    assert out["copies"][0] == {"topic": "t", "copy": "cookbook/guidelines/a/t", "survivor": "cookbook/guidelines/b/t",
                                "direction": "out", "from": ["worklist"], "identical": True}
    assert out["copies"][1]["linked_by"] == ["cookbook/guidelines/c/x/rules.md"]
    assert out["copies"][1]["stamps"] == ["synced"] and out["copies"][1]["kept"] is True
    assert "parts" not in out["copies"][1] and "meta" not in out["copies"][1]
