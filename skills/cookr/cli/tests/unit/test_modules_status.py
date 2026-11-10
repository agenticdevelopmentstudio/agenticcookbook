"""`cookr status`."""

from __future__ import annotations

import json

from cookr.cli import main

from .test_conformance import _bump, _repo


def test_status_fully_conformant(tmp_path, capsys):
    repo = _repo(tmp_path)
    assert main(["-p", str(repo), "confirm", "test-repo.ingredient.ui.x"]) == 0
    capsys.readouterr()
    assert main(["-p", str(repo), "status"]) == 0
    assert "fully conformant" in capsys.readouterr().out


def test_status_lists_uncovered_and_states(tmp_path, capsys):
    repo = _repo(tmp_path)
    (repo / "web" / "stray.ts").write_text("export {}\n", encoding="utf-8")
    assert main(["-p", str(repo), "status"]) == 0
    out = capsys.readouterr().out
    assert "web/stray.ts" in out and "1 uncovered · 1 unverified · 0 needs-validation · 0 planned" in out
    main(["-p", str(repo), "confirm", "test-repo.ingredient.ui.x"])
    _bump(repo, "1.1.0")
    capsys.readouterr()
    assert main(["-p", str(repo), "status", "--json"]) == 0
    data = json.loads(capsys.readouterr().out)
    assert data["implementations"][0]["state"] == "needs-validation"
    assert data["recipes"][0]["state"] == "needs-validation"
    assert data["uncovered"]["web"] == ["web/stray.ts"]


def test_status_marks_a_deleted_location_missing(tmp_path, capsys):
    repo = _repo(tmp_path)
    main(["-p", str(repo), "confirm", "test-repo.ingredient.ui.x"])
    (repo / "web" / "x.ts").unlink()
    capsys.readouterr()
    assert main(["-p", str(repo), "status", "--json"]) == 0
    data = json.loads(capsys.readouterr().out)
    assert data["implementations"][0]["state"] == "needs-validation"
    assert data["implementations"][0]["missing"] is True
    assert data["summary"].endswith("· 1 missing")
    assert main(["-p", str(repo), "status"]) == 0
    assert "(missing)" in capsys.readouterr().out


def test_status_stored_hash_none_on_a_file_row(tmp_path, capsys):
    repo = _repo(tmp_path)
    main(["-p", str(repo), "confirm", "test-repo.ingredient.ui.x"])
    p = repo / "cookbook" / "index.json"
    data = json.loads(p.read_text(encoding="utf-8"))
    for e in data["entries"].values():
        for i in e["implementations"]:
            i["conformance"].pop("hash")
    p.write_text(json.dumps(data), encoding="utf-8")
    capsys.readouterr()
    assert main(["-p", str(repo), "status", "--json"]) == 0
    assert json.loads(capsys.readouterr().out)["implementations"][0]["state"] == "needs-validation"
