"""`cookr relink` at the CLI level."""

from __future__ import annotations

import json
import subprocess

from cookr.cli import main


def _git(repo, *args, check=True):
    return subprocess.run(["git", "-C", str(repo), *args], capture_output=True, text=True, check=check)


def _init_git(repo):
    _git(repo, "init", "-q")
    _git(repo, "config", "user.email", "test@example.com")
    _git(repo, "config", "user.name", "Test Author")
    _git(repo, "add", "-A")
    _git(repo, "commit", "-q", "-m", "initial")


def _move_stat_card(repo):
    (repo / "web" / "blocks" / "Stat").mkdir()
    _git(repo, "mv", "web/blocks/StatCard.tsx", "web/blocks/Stat/StatCard.tsx")


def test_relink_reports_nothing_when_no_code_moved(mini_repo, capsys):
    _init_git(mini_repo)
    assert main(["-p", str(mini_repo), "relink", "--dry-run"]) == 0
    assert "0 spec(s) would be relinked" in capsys.readouterr().out


STAT_CARD = "mini-repo.ingredient.blocks.stat-card"


def _stat_card_locations(repo):
    from cookr.core.index import load_index
    entry = next(e for e in load_index(repo / "cookbook").entries.values() if e.rdid == STAT_CARD)
    return [i.location for i in entry.implementations]


def test_relink_dry_run_names_the_row_and_leaves_the_index_untouched(mini_repo, capsys):
    _init_git(mini_repo)
    before = (mini_repo / "cookbook" / "index.json").read_text(encoding="utf-8")
    _move_stat_card(mini_repo)
    assert main(["-p", str(mini_repo), "relink", "--dry-run"]) == 0
    out = capsys.readouterr().out
    assert STAT_CARD in out
    assert "web/blocks/StatCard.tsx → web/blocks/Stat/StatCard.tsx" in out
    assert "1 spec(s) would be relinked" in out
    assert (mini_repo / "cookbook" / "index.json").read_text(encoding="utf-8") == before


def test_relink_dry_run_json_reports_the_move(mini_repo, capsys):
    _init_git(mini_repo)
    _move_stat_card(mini_repo)
    assert main(["-p", str(mini_repo), "relink", "--dry-run", "--json"]) == 0
    data = json.loads(capsys.readouterr().out)
    assert data == [{
        "spec": STAT_CARD,
        "rows": [{"from": "web/blocks/StatCard.tsx", "to": "web/blocks/Stat/StatCard.tsx"}],
        "lost": [],
        "folder": [],
    }]


def test_relink_writes_the_index_and_leaves_the_artifact_alone(mini_repo, capsys):
    # A moved file is an index fact, not an edit to the spec: no version bump.
    _init_git(mini_repo)
    folder = mini_repo / "cookbook" / "blocks" / "stat-card"
    before = {f.name: f.read_text(encoding="utf-8") for f in folder.iterdir()}
    _move_stat_card(mini_repo)
    assert main(["-p", str(mini_repo), "relink"]) == 0
    assert "1 spec(s) relinked" in capsys.readouterr().out
    assert _stat_card_locations(mini_repo) == ["web/blocks/Stat/StatCard.tsx"]
    assert {f.name: f.read_text(encoding="utf-8") for f in folder.iterdir()} == before


def test_relink_exits_1_when_a_claimed_file_is_gone(mini_repo, capsys):
    _init_git(mini_repo)
    (mini_repo / "web" / "blocks" / "Other.tsx").write_text("export {}\n", encoding="utf-8")
    _git(mini_repo, "rm", "-q", "web/blocks/StatCard.tsx")
    assert main(["-p", str(mini_repo), "relink"]) == 1
    assert "gone, no rename to follow: web/blocks/StatCard.tsx" in capsys.readouterr().out


def test_relink_leaves_a_planned_row_alone(mini_repo, capsys):
    # A planned row names code that does not exist yet: not lost, not moved.
    from .cookbook_helpers import set_implementations
    set_implementations(mini_repo, "blocks/stat-card",
                        [("web", "web/blocks/StatCard.tsx"),
                         ("ios", "Sources/Blocks/StatCard.swift", "planned")])
    _init_git(mini_repo)
    before = (mini_repo / "cookbook" / "index.json").read_text(encoding="utf-8")
    assert main(["-p", str(mini_repo), "relink"]) == 0
    out = capsys.readouterr().out
    assert "gone" not in out and "0 spec(s) relinked" in out
    assert (mini_repo / "cookbook" / "index.json").read_text(encoding="utf-8") == before


def test_relink_without_config_exits_2(tmp_path, capsys):
    assert main(["-p", str(tmp_path), "relink"]) == 2
