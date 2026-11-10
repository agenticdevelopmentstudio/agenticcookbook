"""`cookr relink`: follow code that moved, using git's own rename detection.

`git_renames()` reads `git diff -M --diff-filter=R` into an old-path -> new-path
map. `relink_rows()` rewrites one index entry's implementation locations against
that map: a file row follows its file; a directory row follows only when every
*moved* file below it moved to one new directory with the same path below that;
anything gone with no rename to follow is reported as lost, never guessed.
`relink()` runs that over the whole index and writes `index.json`; no artifact's
content changes, so nothing is bumped.
"""

from __future__ import annotations

import subprocess

import pytest

from cookr.core.index import load_index
from cookr.core.relink import Change, git_renames, relink, relink_rows, _dir_target

from .cookbook_helpers import config as _cfg

STAT = "mini-repo.ingredient.blocks.stat-card"
BUTTON = "mini-repo.ingredient.components.button"


def _entry(repo, rdid):
    return load_index(repo / "cookbook").get(rdid)


def _locations(repo, rdid):
    return [(i.platform, i.location) for i in _entry(repo, rdid).implementations]


def _git(repo, *args, check=True):
    return subprocess.run(["git", "-C", str(repo), *args], capture_output=True, text=True, check=check)


def _init_git(repo):
    _git(repo, "init", "-q")
    _git(repo, "config", "user.email", "test@example.com")
    _git(repo, "config", "user.name", "Test Author")
    _git(repo, "add", "-A")
    _git(repo, "commit", "-q", "-m", "initial")


# --- git_renames ---------------------------------------------------------------------------


def test_git_renames_maps_a_staged_single_file_move(mini_repo):
    _init_git(mini_repo)
    (mini_repo / "web" / "blocks" / "Stat").mkdir()
    _git(mini_repo, "mv", "web/blocks/StatCard.tsx", "web/blocks/Stat/StatCard.tsx")
    assert git_renames(mini_repo) == {"web/blocks/StatCard.tsx": "web/blocks/Stat/StatCard.tsx"}


def test_git_renames_is_empty_for_a_plain_delete_with_nothing_to_follow(mini_repo):
    _init_git(mini_repo)
    _git(mini_repo, "rm", "-q", "web/blocks/StatCard.tsx")
    assert git_renames(mini_repo) == {}


def test_git_renames_raises_configerror_on_a_git_failure(mini_repo, tmp_path):
    from cookr.core.repoconfig import ConfigError
    with pytest.raises(ConfigError, match="git diff HEAD failed"):
        git_renames(tmp_path / "not-a-repo")


# --- _dir_target -----------------------------------------------------------------------------


def test_dir_target_follows_a_directory_whose_files_all_moved_alike(mini_repo):
    _init_git(mini_repo)
    (mini_repo / "apple" / "Widgets").mkdir()
    _git(mini_repo, "mv", "apple/UI/Button.swift", "apple/Widgets/Button.swift")
    _git(mini_repo, "mv", "apple/UI/ToolbarButton.swift", "apple/Widgets/ToolbarButton.swift")
    renames = git_renames(mini_repo)
    assert _dir_target("apple/UI/", renames) == "apple/Widgets/"


def test_dir_target_is_none_when_moved_files_scatter_to_different_directories(mini_repo):
    _init_git(mini_repo)
    (mini_repo / "apple" / "Widgets").mkdir()
    (mini_repo / "apple" / "Other").mkdir()
    _git(mini_repo, "mv", "apple/UI/Button.swift", "apple/Widgets/Button.swift")
    _git(mini_repo, "mv", "apple/UI/ToolbarButton.swift", "apple/Other/ToolbarButton.swift")
    renames = git_renames(mini_repo)
    assert _dir_target("apple/UI/", renames) is None


def test_dir_target_follows_the_directory_even_when_only_some_of_its_files_moved(mini_repo):
    # `_dir_target` judges only the files git reports as moved -- a file that
    # never moved leaves no trace in `renames` at all, so it cannot disagree.
    _init_git(mini_repo)
    (mini_repo / "apple" / "Widgets2").mkdir()
    _git(mini_repo, "mv", "apple/UI/ToolbarButton.swift", "apple/Widgets2/ToolbarButton.swift")
    renames = git_renames(mini_repo)
    assert _dir_target("apple/UI/", renames) == "apple/Widgets2/"


# --- relink_rows -----------------------------------------------------------------------------


def _rows(repo, rdid, renames):
    rows, change = relink_rows(repo, _entry(repo, rdid), renames)
    return [(r.platform, r.location) for r in rows], change


def test_relink_rows_follows_a_moved_file(mini_repo):
    _init_git(mini_repo)
    (mini_repo / "web" / "blocks" / "Stat").mkdir()
    _git(mini_repo, "mv", "web/blocks/StatCard.tsx", "web/blocks/Stat/StatCard.tsx")
    rows, change = _rows(mini_repo, STAT, git_renames(mini_repo))
    assert rows == [("web", "web/blocks/Stat/StatCard.tsx")]
    assert change == Change(spec=STAT,
                            rows=[("web/blocks/StatCard.tsx", "web/blocks/Stat/StatCard.tsx")], lost=[])


def test_relink_rows_follows_a_moved_directory(mini_repo):
    _init_git(mini_repo)
    (mini_repo / "apple" / "Widgets").mkdir()
    _git(mini_repo, "mv", "apple/UI/Button.swift", "apple/Widgets/Button.swift")
    _git(mini_repo, "mv", "apple/UI/ToolbarButton.swift", "apple/Widgets/ToolbarButton.swift")
    rows, change = _rows(mini_repo, BUTTON, git_renames(mini_repo))
    assert rows == [("web", "web/components/Button.tsx"), ("apple", "apple/Widgets/")]
    assert change.rows == [("apple/UI/", "apple/Widgets/")]
    assert change.lost == []


def test_relink_rows_reports_a_row_gone_with_no_rename_to_follow(mini_repo):
    _init_git(mini_repo)
    _git(mini_repo, "rm", "-q", "web/blocks/StatCard.tsx")
    rows, change = _rows(mini_repo, STAT, git_renames(mini_repo))
    assert change.lost == ["web/blocks/StatCard.tsx"]
    assert change.rows == []
    assert rows == [("web", "web/blocks/StatCard.tsx")]  # unchanged


def test_relink_rows_is_a_no_op_when_nothing_moved(mini_repo):
    _init_git(mini_repo)
    rows, change = _rows(mini_repo, "mini-repo.ingredient.components.chat-composer", {})
    assert change.rows == [] and change.lost == []
    assert rows == [("web", "web/components/chat-composer.tsx")]


# --- relink: the whole index, written without a bump ------------------------------------------


def _move_stat_card(repo):
    _init_git(repo)
    (repo / "web" / "blocks" / "Stat").mkdir()
    _git(repo, "mv", "web/blocks/StatCard.tsx", "web/blocks/Stat/StatCard.tsx")


def test_relink_dry_run_reports_changes_but_writes_nothing(mini_repo):
    _move_stat_card(mini_repo)
    index = mini_repo / "cookbook" / "index.json"
    before = index.read_text(encoding="utf-8")
    changes = relink(_cfg(mini_repo), git_renames(mini_repo), dry_run=True)
    assert len(changes) == 1
    assert changes[0].spec == STAT
    assert changes[0].rows == [("web/blocks/StatCard.tsx", "web/blocks/Stat/StatCard.tsx")]
    assert index.read_text(encoding="utf-8") == before


def test_relink_only_reports_specs_that_actually_changed(mini_repo):
    _move_stat_card(mini_repo)
    changes = relink(_cfg(mini_repo), git_renames(mini_repo), dry_run=True)
    assert [c.spec for c in changes] == [STAT]  # button, chat-composer, site-menu untouched


def test_relink_rewrites_index_locations_without_bump(mini_repo):
    _init_git(mini_repo)
    (mini_repo / "apple" / "Widgets").mkdir()
    _git(mini_repo, "mv", "apple/UI/Button.swift", "apple/Widgets/Button.swift")
    _git(mini_repo, "mv", "apple/UI/ToolbarButton.swift", "apple/Widgets/ToolbarButton.swift")
    folder = mini_repo / "cookbook" / "components" / "button"
    before = {f.name: f.read_text(encoding="utf-8") for f in folder.iterdir()}
    changes = relink(_cfg(mini_repo), git_renames(mini_repo))
    assert [c.spec for c in changes] == [BUTTON]
    assert _locations(mini_repo, BUTTON) == [
        ("web", "web/components/Button.tsx"), ("apple", "apple/Widgets/")]
    after = {f.name: f.read_text(encoding="utf-8") for f in folder.iterdir()}
    assert after == before  # no version bump, no history entry


def test_relink_brings_a_moved_folders_path_up_to_date(mini_repo):
    _init_git(mini_repo)
    cb = mini_repo / "cookbook"
    (cb / "blocks" / "stat-card").rename(cb / "blocks" / "stats")
    changes = relink(_cfg(mini_repo), {})
    assert [(c.spec, c.folder) for c in changes] == [(STAT, ("blocks/stat-card", "blocks/stats"))]
    assert _entry(mini_repo, STAT).path == "blocks/stats"


def test_relink_accepts_a_preloaded_index(mini_repo):
    _move_stat_card(mini_repo)
    index = load_index(mini_repo / "cookbook")
    changes = relink(_cfg(mini_repo), git_renames(mini_repo), dry_run=True, index=index)
    assert [c.spec for c in changes] == [STAT]
