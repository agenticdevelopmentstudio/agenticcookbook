"""Any cookr command upgrades a format-1 repo on contact, then exits 3."""

from __future__ import annotations

import json
import shutil

import pytest

from cookr.cli import main
from tests.unit.test_upgrade import FIXTURES, _git, _repo


@pytest.fixture(autouse=True)
def home(tmp_path, monkeypatch):
    monkeypatch.setenv("COOKR_HOME", str(tmp_path / "cookr-home"))


def test_any_command_upgrades_a_v1_repo_and_exits_3(git_tmp_path, capsys):
    repo = _repo(git_tmp_path, "v1-repo")
    assert main(["-p", str(repo), "validate"]) == 3
    out = capsys.readouterr().out
    assert "commit the upgrade on its own" in out
    assert "chore: cookr format 2 upgrade" in out
    assert json.loads((repo / "cookbook" / "cookbook.json").read_text())["format"] == 2
    capsys.readouterr()
    assert main(["-p", str(repo), "inventory"]) == 0
    assert "source file(s)" in capsys.readouterr().out


def test_dirty_v1_repo_refuses_and_lists_paths(git_tmp_path, capsys):
    repo = _repo(git_tmp_path, "v1-repo")
    (repo / "scratch.txt").write_text("x")
    before = (repo / "cookbook" / "cookbook.json").read_text()
    assert main(["-p", str(repo), "validate"]) == 1
    assert "scratch.txt" in capsys.readouterr().out
    assert (repo / "cookbook" / "cookbook.json").read_text() == before
    assert _git(repo, "status", "--porcelain").stdout.split() == ["??", "scratch.txt"]


def test_v2_repo_runs_command_normally(git_tmp_path, capsys):
    repo = _repo(git_tmp_path, "v1-repo")
    assert main(["-p", str(repo), "upgrade"]) == 0
    _git(repo, "add", "-A")
    _git(repo, "commit", "-q", "-m", "upgrade")
    assert main(["-p", str(repo), "inventory"]) == 0
    assert "source file(s)" in capsys.readouterr().out


def test_upgrade_module_does_not_recurse(git_tmp_path):
    repo = _repo(git_tmp_path, "v1-repo")
    assert main(["-p", str(repo), "upgrade"]) == 0


def test_outside_any_cookbook_nothing_is_attempted(tmp_path, monkeypatch):
    import cookr.cli as cli

    found: list = []
    real = cli.needs_upgrade
    monkeypatch.setattr(cli, "needs_upgrade", lambda repo: found.extend(real(repo)) or found)
    monkeypatch.setattr(cli, "upgrade", lambda repo: pytest.fail("upgrade ran outside a cookbook"))
    monkeypatch.chdir(tmp_path)
    assert main(["inventory"]) == 2  # exactly as before: no repo, no config
    assert found == []               # no cookbook found, so no upgrade was attempted
    assert list(tmp_path.iterdir()) == []  # and nothing was written, not even cookr's home


@pytest.mark.parametrize("flag", ["--version", "--help"])
def test_help_and_version_leave_a_v1_repo_alone(git_tmp_path, flag, capsys):
    repo = _repo(git_tmp_path, "v1-repo")
    manifest = repo / "cookbook" / "cookbook.json"
    before = manifest.read_text()
    with pytest.raises(SystemExit) as e:
        main(["-p", str(repo), flag])
    assert e.value.code == 0
    assert not (repo / "cookbook" / "index.json").exists()
    assert not (repo / ".cookr.json").exists()
    assert manifest.read_text() == before


def test_a_v1_cookbook_outside_git_refuses_with_what_to_do(tmp_path, capsys):
    shutil.copytree(FIXTURES / "v1-repo", tmp_path / "repo")
    repo = tmp_path / "repo"
    before = (repo / "cookbook" / "cookbook.json").read_text()
    assert main(["-p", str(repo), "validate"]) == 1
    out = " ".join(capsys.readouterr().out.split())
    assert "not a git work tree" in out
    assert "clean work tree, then rerun" in out
    assert (repo / "cookbook" / "cookbook.json").read_text() == before


def test_check_hook_blocks_with_exit_2_after_upgrading(git_tmp_path, capsys):
    repo = _repo(git_tmp_path, "v1-repo")
    assert main(["-p", str(repo), "check", "--hook"]) == 2
    assert capsys.readouterr().err.strip() == "cookr: commit the cookr upgrade first"
    assert json.loads((repo / "cookbook" / "cookbook.json").read_text())["format"] == 2


def test_check_hook_blocks_with_exit_2_on_a_dirty_tree(git_tmp_path, capsys):
    repo = _repo(git_tmp_path, "v1-repo")
    (repo / "scratch.txt").write_text("x")
    assert main(["-p", str(repo), "check", "--hook"]) == 2
    assert "scratch.txt" in capsys.readouterr().err


def test_check_without_hook_still_exits_3_on_upgrade(git_tmp_path):
    repo = _repo(git_tmp_path, "v1-repo")
    assert main(["-p", str(repo), "check"]) == 3


def _hinted_add(out: str) -> list[str]:
    """The pathspec of the `git add -A …` the on-contact upgrade tells the agent to run."""
    text = " ".join(out.split())
    return text.split("`git add -A ", 1)[1].split(" && git commit", 1)[0].split()


def test_the_commit_hint_stages_every_upgrade_change(git_tmp_path, capsys):
    repo = _repo(git_tmp_path, "legacy-repo")  # legacy recipes/ moves into cookbook/
    assert main(["-p", str(repo), "validate"]) == 3
    paths = _hinted_add(capsys.readouterr().out)
    assert "recipes" in paths and "cookbook" in paths
    _git(repo, "add", "-A", *paths)
    unstaged = [line for line in _git(repo, "status", "--porcelain").stdout.splitlines()
                if line[1] != " " and "cookr-home" not in line]  # the test's COOKR_HOME
    assert unstaged == []


def test_check_hook_on_a_dirty_tree_lets_the_wip_commit_through(git_tmp_path, capsys):
    """The commit that sets the work aside must not be blocked: it names the steps."""
    repo = _repo(git_tmp_path, "v1-repo")
    (repo / "scratch.txt").write_text("x")
    assert main(["-p", str(repo), "check", "--staged", "--hook"]) == 1  # a warning, no block
    err = " ".join(capsys.readouterr().err.split())
    assert "scratch.txt" in err
    assert "WIP commit" in err and "cookr upgrade" in err
    assert "stash" not in err


def test_stop_hook_on_a_dirty_tree_blocks_and_names_the_steps(git_tmp_path, capsys):
    repo = _repo(git_tmp_path, "v1-repo")
    (repo / "scratch.txt").write_text("x")
    assert main(["-p", str(repo), "check", "--branch", "--hook"]) == 2
    err = " ".join(capsys.readouterr().err.split())
    assert "WIP commit" in err and "cookr upgrade" in err and "stash" not in err


@pytest.mark.parametrize("bad", [{"format": 2, "roots": 5},
                                 {"format": 2, "ignore": "x"}])
def test_check_hook_puts_a_config_error_on_stderr(git_tmp_path, bad, capsys):
    """The hook forwards only stderr: an error on stdout would block with no reason."""
    shutil.copytree(FIXTURES / "mini-repo", git_tmp_path, dirs_exist_ok=True)
    (git_tmp_path / ".cookr.json").write_text(json.dumps(bad))
    assert main(["-p", str(git_tmp_path), "check", "--staged", "--hook"]) == 2
    out, err = capsys.readouterr()
    assert out == ""
    assert ".cookr.json" in err


def test_check_hook_puts_a_cookbook_error_on_stderr(git_tmp_path, capsys):
    shutil.copytree(FIXTURES / "mini-repo", git_tmp_path, dirs_exist_ok=True)
    index = git_tmp_path / "cookbook" / "index.json"
    index.write_text(json.dumps({**json.loads(index.read_text()), "entries": 5}))
    assert main(["-p", str(git_tmp_path), "check", "--staged", "--hook"]) == 2
    out, err = capsys.readouterr()
    assert out == ""
    assert "index.json" in err


@pytest.mark.parametrize("fmt", ["2", 2.0, True])
def test_a_malformed_config_format_is_refused_never_upgraded(git_tmp_path, fmt, capsys):
    """A format-2 config whose `format` is mistyped is an error, not a format-1 file
    the upgrade would rewrite."""
    shutil.copytree(FIXTURES / "mini-repo", git_tmp_path, dirs_exist_ok=True)
    config = git_tmp_path / ".cookr.json"
    config.write_text(json.dumps({**json.loads(config.read_text()), "format": fmt}))
    before = config.read_text()
    assert main(["-p", str(git_tmp_path), "validate"]) == 2
    assert "`format` must be the integer 2" in " ".join(capsys.readouterr().out.split())
    assert config.read_text() == before


def test_check_without_hook_keeps_errors_on_stdout(git_tmp_path, capsys):
    shutil.copytree(FIXTURES / "mini-repo", git_tmp_path, dirs_exist_ok=True)
    (git_tmp_path / ".cookr.json").write_text(json.dumps({"format": 2, "roots": 5}))
    assert main(["-p", str(git_tmp_path), "check", "--staged"]) == 2
    assert ".cookr.json" in capsys.readouterr().out
