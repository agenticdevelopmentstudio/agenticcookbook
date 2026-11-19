"""paraphrase_hints.py: for each lacking sentence of A/gaps/*.json, the topic
sentences with the highest word overlap, as an advisory pre-check (G31)."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

SCRIPT = Path(__file__).resolve().parent / "paraphrase_hints.py"
sys.path.insert(0, str(SCRIPT.parent))

import paraphrase_hints as ph  # noqa: E402

LACKING = ["Absolute session timeouts are enforced server-side.",
           "Quantum widgets frobnicate."]


def topic(repo: Path) -> Path:
    folder = repo / "cookbook" / "guidelines" / "implementing" / "security" / "authentication"
    folder.mkdir(parents=True)
    (folder / "artifact.json").write_text(json.dumps({"meta": {}, "parts": [
        {"part": "intro"}, {"part": "rules", "role": "rules"}, {"part": "history"}]}), encoding="utf-8")
    (folder / "intro.md").write_text("Authentication proves who a user is.\n", encoding="utf-8")
    (folder / "rules.md").write_text(
        "- The server MUST enforce an absolute timeout on every session.\n"
        "- Session cookies stay server-side.\n- Timeouts end idle work. Passwords are hashed.\n"
        "- Every session is enforced.\n", encoding="utf-8")
    (folder / "history.md").write_text("Session timeouts enforced server-side since 1.0.\n", encoding="utf-8")
    return folder


def gaps(dir_: Path, folder: Path) -> Path:
    dir_.mkdir(parents=True)
    f = dir_ / "authentication.json"
    f.write_text(json.dumps({"folder": str(folder), "references": [
        {"file": "/A/reference/security--authentication.txt", "sentences": 4, "held": 2, "lacking": 2,
         "lacking_sentences": LACKING}]}), encoding="utf-8")
    return dir_


def test_each_lacking_sentence_lists_the_closest_topic_sentences(tmp_path):
    folder = topic(tmp_path)
    out = ph.hints(gaps(tmp_path / "A" / "gaps", folder), tmp_path)
    assert out["advisory"]
    [g] = out["gaps"]
    assert g["gaps_file"] == "authentication.json" and g["folder"] == str(folder)
    [ref] = g["references"]
    first, second = ref["lacking"]
    assert first["text"] == LACKING[0]
    assert len(first["hints"]) == 3   # the default top 3 of four overlapping sentences
    top = first["hints"][0]
    # the topic's own parts only (artifact.json), never its history part (a change log)
    assert top["text"] == "- The server MUST enforce an absolute timeout on every session."
    assert top["part"] == "rules" and 0 < top["score"] <= 1
    assert [h["score"] for h in first["hints"]] == sorted((h["score"] for h in first["hints"]), reverse=True)
    assert all("since 1.0" not in h["text"] for h in first["hints"])
    assert second["text"] == LACKING[1] and second["hints"] == []   # no overlap, no hint
    # 1.4.17, M3: --top caps the hints (four topic sentences overlap the first)
    capped = ph.hints(tmp_path / "A" / "gaps", tmp_path, top=1)["gaps"][0]["references"][0]["lacking"][0]
    assert capped["hints"] == first["hints"][:1]


def test_cli_prints_json_and_a_missing_folder_exits_2(tmp_path):
    folder = topic(tmp_path)
    d = gaps(tmp_path / "A" / "gaps", folder)
    r = subprocess.run([sys.executable, str(SCRIPT), str(d), "--repo", str(tmp_path)], capture_output=True, text=True)
    assert r.returncode == 0 and json.loads(r.stdout)["gaps"][0]["references"][0]["lacking"][0]["hints"]
    (d / "authentication.json").write_text(json.dumps({"folder": "cookbook/guidelines/nowhere", "references": []}),
                                           encoding="utf-8")
    r = subprocess.run([sys.executable, str(SCRIPT), str(d), "--repo", str(tmp_path)], capture_output=True, text=True)
    assert r.returncode == 2 and "nowhere" in r.stderr


def test_a_missing_gaps_folder_exits_2(tmp_path):
    # 1.4.17, M4: a mistyped A/gaps printed "gaps": [] and exited 0.
    (tmp_path / "cookbook" / "guidelines").mkdir(parents=True)     # a real repo: only the folder is wrong
    r = subprocess.run([sys.executable, str(SCRIPT), str(tmp_path / "A" / "gpas"), "--repo", str(tmp_path)],
                       capture_output=True, text=True)
    assert r.returncode == 2 and "gpas" in r.stderr and "Traceback" not in r.stderr and not r.stdout


def test_a_flat_list_holds_one_row_per_lacking_sentence(tmp_path):
    # 1.4.24, G59: readable without a summariser: one row per sentence.
    folder = topic(tmp_path)
    out = ph.hints(gaps(tmp_path / "A" / "gaps", folder), tmp_path)
    nested = out["gaps"][0]["references"][0]["lacking"]
    assert out["sentences"] == [{"gaps_file": "authentication.json", "folder": str(folder),
                                 "file": "/A/reference/security--authentication.txt",
                                 "text": s["text"], "hints": s["hints"]} for s in nested]
    assert len(out["sentences"]) == 2


def test_a_given_repo_with_no_cookbook_exits_2(tmp_path):
    # 1.4.26 (M8): a wrong --repo is refused like every other script's,
    # never read as a cookbook with no topics.
    folder = topic(tmp_path)
    d = gaps(tmp_path / "A" / "gaps", folder)
    r = subprocess.run([sys.executable, str(SCRIPT), str(d), "--repo", str(tmp_path / "elsewhere")],
                       capture_output=True, text=True)
    assert r.returncode == 2 and "holds no cookbook/guidelines/" in r.stderr and not r.stdout
