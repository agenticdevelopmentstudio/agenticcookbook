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
