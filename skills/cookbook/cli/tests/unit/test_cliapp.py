"""The CLI scaffold shared by cookbook and cookr (cookbook.core.cliapp)."""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

from cookbook.core import cliapp
from cookbook.core.errors import CookbookError




@pytest.fixture
def fake_pkg(tmp_path, monkeypatch):
    """A throwaway modules package on sys.path: fakepkg.modules.{alpha,beta,_helper}."""
    root = tmp_path / "fakepkg" / "modules"
    root.mkdir(parents=True)
    (tmp_path / "fakepkg" / "__init__.py").write_text("")
    (root / "__init__.py").write_text("")
    body = "NAME = {n!r}\nHELP = 'h'\ndef register(p): pass\ndef run(args, ctx): return ctx['seen'].append(getattr(args, 'path', None))\n"
    (root / "beta.py").write_text(body.format(n="beta"))
    (root / "alpha.py").write_text(body.format(n="alpha"))
    (root / "_helper.py").write_text("X = 1\n")
    monkeypatch.syspath_prepend(str(tmp_path))
    yield "fakepkg.modules"
    for m in [m for m in sys.modules if m.startswith("fakepkg")]:
        del sys.modules[m]


def _app(package, seen, **kw):
    return cliapp.CliApp(prog="fake", version="0.0.1", description="d", modules_package=package,
                         path_help="p", make_context=lambda explicit, ui: {"seen": seen}, **kw)


def test_discover_sorts_and_skips_underscore_helpers(fake_pkg):
    assert [m.NAME for m in cliapp.discover(fake_pkg)] == ["alpha", "beta"]


def test_discover_fails_fast_on_a_module_missing_an_attribute(fake_pkg, tmp_path):
    (tmp_path / "fakepkg" / "modules" / "gamma.py").write_text("NAME = 'gamma'\nHELP = 'h'\n")
    with pytest.raises(CookbookError, match=r"fakepkg\.modules\.gamma.*register, run"):
        cliapp.discover(fake_pkg)


@pytest.mark.parametrize("argv", [
    ["-p", "/tmp/X", "alpha"],   # leading form: default=None used to drop this
    ["alpha", "-p", "/tmp/X"],
    ["--path", "/tmp/X", "alpha"],
])
def test_path_flag_before_or_after_the_subcommand(fake_pkg, argv):
    seen = []
    assert cliapp.main(_app(fake_pkg, seen), argv) == 0
    assert seen == [Path("/tmp/X")]


def test_no_path_flag_is_none(fake_pkg):
    seen = []
    assert cliapp.main(_app(fake_pkg, seen), ["alpha"]) == 0
    assert seen == [None]


def test_cookbook_parser_keeps_a_leading_path():
    from cookbook.cli import APP
    modules = cliapp.discover(APP.modules_package)
    args = cliapp.build_parser(APP, modules).parse_args(["-p", "/tmp/X", "validate"])
    assert args.path == Path("/tmp/X")


def test_listed_errors_exit_2_with_markup_escaped(fake_pkg, capsys):
    def boom(explicit, ui):
        raise CookbookError("bad path apps/[slug]/x.tsx and weird[/x]")
    app = cliapp.CliApp(prog="fake", version="0", description="d", modules_package=fake_pkg,
                        path_help="p", make_context=boom)
    assert cliapp.main(app, ["alpha"]) == 2
    assert "apps/[slug]/x.tsx and weird[/x]" in capsys.readouterr().out


def test_check_path_runs_even_without_a_module(fake_pkg, capsys):
    def check(explicit):
        raise CookbookError(f"no config at {explicit}")
    assert cliapp.main(_app(fake_pkg, [], check_path=check), ["-p", "/nowhere"]) == 2
    assert "no config at /nowhere" in capsys.readouterr().out


def test_no_module_prints_the_table(fake_pkg, capsys):
    assert cliapp.main(_app(fake_pkg, []), []) == 0
    out = capsys.readouterr().out
    assert "alpha" in out and "beta" in out and "Usage: fake [-p PATH]" in out
