"""Top-level CLI shape: --version, module table, unknown module, -p."""

from __future__ import annotations

import pytest

from cookr import __version__
from cookr.cli import main


def test_version_flag(capsys):
    with pytest.raises(SystemExit) as exc:
        main(["--version"])
    assert exc.value.code == 0
    assert __version__ in capsys.readouterr().out


def test_no_args_shows_module_table(capsys):
    assert main([]) == 0
    out = capsys.readouterr().out
    assert "cookr" in out


def test_unknown_module_exits_nonzero():
    with pytest.raises(SystemExit) as exc:
        main(["nope"])
    assert exc.value.code != 0


def test_explicit_path_without_config_exits_2(tmp_path, capsys):
    rc = main(["-p", str(tmp_path)])
    assert rc == 2
    assert ".cookr.json" in capsys.readouterr().out


@pytest.mark.parametrize("before", [True, False])
def test_path_flag_before_or_after_the_module(mini_repo, tmp_path, monkeypatch, capsys, before):
    monkeypatch.chdir(tmp_path)  # no .cookr.json reachable from cwd
    argv = ["-p", str(mini_repo), "inventory", "--json"] if before else ["inventory", "--json", "-p", str(mini_repo)]
    assert main(argv) == 0
    assert "toolbar-button" in capsys.readouterr().out


def test_context_carries_only_config_and_ui(mini_repo, monkeypatch):
    # The repo root lives on config.repo_root alone (one derivation, not two).
    import dataclasses
    from cookr.cli import _context
    from cookr.context import CookrContext
    assert [f.name for f in dataclasses.fields(CookrContext)] == ["config", "ui"]
    ctx = _context(mini_repo, ui=None)
    assert ctx.config.repo_root == mini_repo.resolve()
