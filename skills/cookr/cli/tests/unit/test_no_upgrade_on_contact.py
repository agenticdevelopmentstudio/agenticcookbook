"""No cookr command upgrades a format-1 repo on contact. Converting a cookbook
rewrites many files, so it happens only when the agent runs `cookr upgrade`
itself; every other command leaves the repo exactly as it found it and, outside
the hook's check, says on stderr that the upgrade is available."""

from __future__ import annotations

import json
import shutil

import pytest

from cookr.cli import main
from tests.unit.test_upgrade import FIXTURES, _git, _repo

NOTICE = "`cookr upgrade` converts it to format 2 when you choose to"


@pytest.fixture(autouse=True)
def home(tmp_path, monkeypatch):
    monkeypatch.setenv("COOKR_HOME", str(tmp_path / "cookr-home"))


def _untouched(repo, manifest_before: str) -> None:
    assert (repo / "cookbook" / "cookbook.json").read_text() == manifest_before
    status = [line for line in _git(repo, "status", "--porcelain").stdout.splitlines()
              if "cookr-home" not in line]
    assert status == []


@pytest.mark.parametrize("argv", [["validate"], ["inventory"],
                                  ["check"], ["check", "--staged"]])
def test_a_command_leaves_a_v1_repo_alone_and_says_upgrade_is_available(
        git_tmp_path, argv, capsys):
    repo = _repo(git_tmp_path, "v1-repo")
    before = (repo / "cookbook" / "cookbook.json").read_text()
    main(["-p", str(repo), *argv])
    assert NOTICE in " ".join(capsys.readouterr().err.split())
    _untouched(repo, before)


@pytest.mark.parametrize("scope", ["--staged", "--branch"])
def test_the_hook_check_leaves_a_v1_repo_alone_without_the_notice(git_tmp_path, scope, capsys):
    repo = _repo(git_tmp_path, "v1-repo")
    before = (repo / "cookbook" / "cookbook.json").read_text()
    main(["-p", str(repo), "check", scope, "--hook"])
    assert NOTICE not in " ".join(capsys.readouterr().err.split())
    _untouched(repo, before)


def test_a_dirty_v1_repo_keeps_its_uncommitted_work(git_tmp_path, capsys):
    repo = _repo(git_tmp_path, "v1-repo")
    (repo / "scratch.txt").write_text("x")
    before = (repo / "cookbook" / "cookbook.json").read_text()
    main(["-p", str(repo), "validate"])
    assert (repo / "cookbook" / "cookbook.json").read_text() == before
    assert _git(repo, "status", "--porcelain").stdout.split() == ["??", "scratch.txt"]


def test_upgrade_runs_only_when_asked_for(git_tmp_path, capsys):
    repo = _repo(git_tmp_path, "v1-repo")
    assert main(["-p", str(repo), "upgrade"]) == 0
    assert json.loads((repo / "cookbook" / "cookbook.json").read_text())["format"] == 2


def test_v2_repo_runs_command_normally_without_the_notice(git_tmp_path, capsys):
    repo = _repo(git_tmp_path, "v1-repo")
    assert main(["-p", str(repo), "upgrade"]) == 0
    _git(repo, "add", "-A")
    _git(repo, "commit", "-q", "-m", "upgrade")
    capsys.readouterr()
    assert main(["-p", str(repo), "inventory"]) == 0
    out, err = capsys.readouterr()
    assert "source file(s)" in out
    assert NOTICE not in " ".join(err.split())


def test_outside_any_cookbook_nothing_is_attempted(tmp_path, monkeypatch):
    import cookr.cli as cli

    found: list = []
    real = cli.needs_upgrade
    monkeypatch.setattr(cli, "needs_upgrade", lambda repo: found.extend(real(repo)) or found)
    monkeypatch.chdir(tmp_path)
    assert main(["inventory"]) == 2  # exactly as before: no repo, no config
    assert found == []
    assert list(tmp_path.iterdir()) == []  # nothing was written, not even cookr's home


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
