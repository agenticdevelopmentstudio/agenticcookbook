"""`cookr relink`: follow code that moved, using git's own rename detection.

`git_renames()` reads `git diff -M --diff-filter=R` into an old-path -> new-path
map. `relink_rows()` rewrites one spec's Reference Implementations rows against
that map: a file row follows its file; a directory row follows only when every
*moved* file below it moved to one new directory with the same path below that;
anything gone with no rename to follow is reported as lost, never guessed.
`relink()` runs that over a whole corpus, writing and patch-bumping the specs
that actually changed.
"""

from __future__ import annotations

import subprocess

import pytest

from cookr.core.config import load_config
from cookr.core.recipes import load_corpus
from cookr.core.relink import Change, git_renames, relink, relink_rows, _dir_target


def _cfg(mini_repo):
    return load_config(mini_repo / "cookbook")


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
    from cookr.core.config import ConfigError
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


def test_relink_rows_follows_a_moved_file(mini_repo):
    _init_git(mini_repo)
    (mini_repo / "web" / "blocks" / "Stat").mkdir()
    _git(mini_repo, "mv", "web/blocks/StatCard.tsx", "web/blocks/Stat/StatCard.tsx")
    cfg = _cfg(mini_repo)
    corpus = load_corpus(cfg.cookbook_dir)
    rows, change = relink_rows(mini_repo, corpus["blocks/stat-card"], git_renames(mini_repo))
    assert [(r.platform, r.path) for r in rows] == [("web", "web/blocks/Stat/StatCard.tsx")]
    assert change == Change(spec="blocks/stat-card",
                             rows=[("web/blocks/StatCard.tsx", "web/blocks/Stat/StatCard.tsx")], lost=[])


def test_relink_rows_follows_a_moved_directory(mini_repo):
    _init_git(mini_repo)
    (mini_repo / "apple" / "Widgets").mkdir()
    _git(mini_repo, "mv", "apple/UI/Button.swift", "apple/Widgets/Button.swift")
    _git(mini_repo, "mv", "apple/UI/ToolbarButton.swift", "apple/Widgets/ToolbarButton.swift")
    cfg = _cfg(mini_repo)
    corpus = load_corpus(cfg.cookbook_dir)
    rows, change = relink_rows(mini_repo, corpus["components/button"], git_renames(mini_repo))
    assert [(r.platform, r.path) for r in rows] == [
        ("web", "web/components/Button.tsx"), ("apple", "apple/Widgets/")]
    assert change.rows == [("apple/UI/", "apple/Widgets/")]
    assert change.lost == []


def test_relink_rows_reports_a_row_gone_with_no_rename_to_follow(mini_repo):
    _init_git(mini_repo)
    cfg = _cfg(mini_repo)
    corpus = load_corpus(cfg.cookbook_dir)
    _git(mini_repo, "rm", "-q", "web/blocks/StatCard.tsx")
    rows, change = relink_rows(mini_repo, corpus["blocks/stat-card"], git_renames(mini_repo))
    assert change.lost == ["web/blocks/StatCard.tsx"]
    assert change.rows == []
    assert [(r.platform, r.path) for r in rows] == [("web", "web/blocks/StatCard.tsx")]  # unchanged


def test_relink_rows_is_a_no_op_when_nothing_moved(mini_repo):
    _init_git(mini_repo)
    cfg = _cfg(mini_repo)
    corpus = load_corpus(cfg.cookbook_dir)
    rows, change = relink_rows(mini_repo, corpus["components/chat-composer"], {})
    assert change.rows == [] and change.lost == []
    assert [(r.platform, r.path) for r in rows] == [("web", "web/components/chat-composer.tsx")]


# --- relink: whole-corpus, write, patch-bump --------------------------------------------------


def test_relink_dry_run_reports_changes_but_writes_nothing(mini_repo):
    _init_git(mini_repo)
    (mini_repo / "web" / "blocks" / "Stat").mkdir()
    _git(mini_repo, "mv", "web/blocks/StatCard.tsx", "web/blocks/Stat/StatCard.tsx")
    cfg = _cfg(mini_repo)
    before = (mini_repo / "cookbook" / "blocks" / "stat-card.md").read_text(encoding="utf-8")
    changes = relink(cfg, git_renames(mini_repo), dry_run=True)
    assert len(changes) == 1
    assert changes[0].spec == "blocks/stat-card"
    assert changes[0].rows == [("web/blocks/StatCard.tsx", "web/blocks/Stat/StatCard.tsx")]
    after = (mini_repo / "cookbook" / "blocks" / "stat-card.md").read_text(encoding="utf-8")
    assert after == before


def test_relink_only_reports_specs_that_actually_changed(mini_repo):
    _init_git(mini_repo)
    (mini_repo / "web" / "blocks" / "Stat").mkdir()
    _git(mini_repo, "mv", "web/blocks/StatCard.tsx", "web/blocks/Stat/StatCard.tsx")
    cfg = _cfg(mini_repo)
    changes = relink(cfg, git_renames(mini_repo), dry_run=True)
    assert [c.spec for c in changes] == ["blocks/stat-card"]  # button, chat-composer, site-menu untouched


def test_relink_writes_the_new_row_and_patch_bumps_the_spec(mini_repo):
    _init_git(mini_repo)
    (mini_repo / "apple" / "Widgets").mkdir()
    _git(mini_repo, "mv", "apple/UI/Button.swift", "apple/Widgets/Button.swift")
    _git(mini_repo, "mv", "apple/UI/ToolbarButton.swift", "apple/Widgets/ToolbarButton.swift")
    cfg = _cfg(mini_repo)
    changes = relink(cfg, git_renames(mini_repo), author="Test Author <test@example.com>", day="2026-09-25")
    assert len(changes) == 1 and changes[0].spec == "components/button"
    assert changes[0].bump_error == ""  # button.md already has a `version:` line
    text = (mini_repo / "cookbook" / "components" / "button.md").read_text(encoding="utf-8")
    assert "| apple | `apple/Widgets/` |" in text
    assert "version: 1.1.2" in text
    assert "Relinked Reference Implementations after the code moved." in text


def test_relink_reports_a_bump_failure_without_crashing(mini_repo):
    # stat-card.md has no `version:` line in the fixture; the write still
    # happens, the patch bump fails, and relink() reports it rather than raising.
    _init_git(mini_repo)
    (mini_repo / "web" / "blocks" / "Stat").mkdir()
    _git(mini_repo, "mv", "web/blocks/StatCard.tsx", "web/blocks/Stat/StatCard.tsx")
    cfg = _cfg(mini_repo)
    changes = relink(cfg, git_renames(mini_repo), author="Test Author <test@example.com>", day="2026-09-25")
    assert changes[0].bump_error == "the frontmatter has no plain `version:` line"
    text = (mini_repo / "cookbook" / "blocks" / "stat-card.md").read_text(encoding="utf-8")
    assert "| web | `web/blocks/Stat/StatCard.tsx` |" in text  # the row still got written


def test_relink_accepts_a_precomputed_corpus_instead_of_reloading(mini_repo):
    _init_git(mini_repo)
    (mini_repo / "web" / "blocks" / "Stat").mkdir()
    _git(mini_repo, "mv", "web/blocks/StatCard.tsx", "web/blocks/Stat/StatCard.tsx")
    cfg = _cfg(mini_repo)
    corpus = load_corpus(cfg.cookbook_dir)
    changes = relink(cfg, git_renames(mini_repo), dry_run=True, corpus=corpus)
    assert [c.spec for c in changes] == ["blocks/stat-card"]
