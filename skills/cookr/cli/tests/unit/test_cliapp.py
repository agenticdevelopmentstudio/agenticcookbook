"""The CLI scaffold shared by cookbook and cookr (cookr.core.cliapp)."""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

from cookr.core import cliapp
from cookr.core.errors import CookbookError




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
                         path_help="p", make_context=lambda explicit, ui, module: {"seen": seen}, **kw)


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
    from cookr.cli import APP
    modules = cliapp.discover(APP.modules_package)
    args = cliapp.build_parser(APP, modules).parse_args(["-p", "/tmp/X", "validate"])
    assert args.path == Path("/tmp/X")


def test_listed_errors_exit_2_with_markup_escaped(fake_pkg, capsys):
    def boom(explicit, ui, module):
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


@pytest.mark.parametrize("code, message, mark", [
    (3, "commit the upgrade [first]", "✗"),   # nonzero: an error, markup escaped
    (0, "nothing to do [yet]", "!"),          # zero: a warning
    (1, "", None),                            # no message: only the code
])
def test_exit_with_ends_the_run_with_its_code_and_message(fake_pkg, capsys, code, message, mark):
    def stop(explicit, ui, module):
        raise cliapp.ExitWith(code, message)
    app = cliapp.CliApp(prog="fake", version="0", description="d", modules_package=fake_pkg,
                        path_help="p", make_context=stop)
    assert cliapp.main(app, ["alpha"]) == code
    out = capsys.readouterr().out
    if mark:
        assert out.strip() == f"{mark} {message}"
    else:
        assert out.strip() == ""


def test_exit_with_goes_to_stderr_in_hook_mode(fake_pkg, capsys):
    def stop(explicit, ui, module):
        raise cliapp.ExitWith(2, "blocked")
    app = cliapp.CliApp(prog="fake", version="0", description="d", modules_package=fake_pkg,
                        path_help="p", make_context=stop, ui_on_stderr=lambda args: True)
    assert cliapp.main(app, ["alpha"]) == 2
    captured = capsys.readouterr()
    assert "blocked" in captured.err and "blocked" not in captured.out
