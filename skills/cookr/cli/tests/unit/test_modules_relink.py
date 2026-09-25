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


def test_relink_dry_run_names_the_row_and_leaves_the_file_untouched(mini_repo, capsys):
    _init_git(mini_repo)
    before = (mini_repo / "cookbook" / "blocks" / "stat-card.md").read_text(encoding="utf-8")
    _move_stat_card(mini_repo)
    assert main(["-p", str(mini_repo), "relink", "--dry-run"]) == 0
    out = capsys.readouterr().out
    assert "blocks/stat-card" in out
    assert "web/blocks/StatCard.tsx → web/blocks/Stat/StatCard.tsx" in out
    assert "would be relinked" in out
    after = (mini_repo / "cookbook" / "blocks" / "stat-card.md").read_text(encoding="utf-8")
    assert after == before


def test_relink_dry_run_json_reports_the_move(mini_repo, capsys):
    _init_git(mini_repo)
    _move_stat_card(mini_repo)
    assert main(["-p", str(mini_repo), "relink", "--dry-run", "--json"]) == 0
    data = json.loads(capsys.readouterr().out)
    assert data == [{
        "spec": "blocks/stat-card",
        "rows": [{"from": "web/blocks/StatCard.tsx", "to": "web/blocks/Stat/StatCard.tsx"}],
        "lost": [],
        "bump_error": "",
    }]


def test_relink_writes_the_row_and_exits_1_on_a_bump_failure(mini_repo, capsys):
    # stat-card.md has no `version:` line in the fixture, so the patch bump
    # fails even though the row itself is written -- a non-clean exit that
    # still reflects real, applied work.
    _init_git(mini_repo)
    _move_stat_card(mini_repo)
    rc = main(["-p", str(mini_repo), "relink", "--author", "Test Author <test@example.com>"])
    out = capsys.readouterr().out
    assert "not bumped: the frontmatter has no plain `version:` line" in out
    assert rc == 1
    text = (mini_repo / "cookbook" / "blocks" / "stat-card.md").read_text(encoding="utf-8")
    assert "web/blocks/Stat/StatCard.tsx" in text


def test_relink_without_config_exits_2(tmp_path, capsys):
    assert main(["-p", str(tmp_path), "relink"]) == 2
