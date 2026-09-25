"""The CLI scaffold shared by every module-based tool (`cookbook`, `cookr`).

A tool is a package of modules plus one `CliApp` describing it. A module is a
file (or a package with an `__init__`) under the tool's modules package that
exposes:

    NAME: str                       # subcommand name shown in CLI
    HELP: str                       # short help line
    def register(parser): ...       # configure the subcommand's arguments
    def run(args, ctx): ...         # execute; return exit code

Files whose name starts with `_` are helpers, never subcommands. Any other file
missing one of those attributes is a startup error, not a silently dropped
subcommand.

`-p / --path` lives on a shared parent parser, so it works before OR after the
subcommand. Its default is SUPPRESS: with `default=None` the subcommand
parser's own default would overwrite a `-p` given before the subcommand.
"""

from __future__ import annotations

import argparse
import importlib
import pkgutil
import sys
from dataclasses import dataclass
from pathlib import Path
from types import ModuleType
from typing import Any, Callable, Optional

from .errors import CookbookError
from .ui import UI

from rich.markup import escape  # rich is present: importing .ui required it

MODULE_ATTRS = ("NAME", "HELP", "register", "run")


@dataclass(frozen=True)
class CliApp:
    prog: str
    version: str
    description: str
    modules_package: str  # dotted name, e.g. "cookbook.modules"
    path_help: str
    # Build the ctx handed to run() from the explicit `-p` (None when absent).
    make_context: Callable[[Optional[Path], UI], Any]
    # Validate an explicit `-p` even when no module is named (None: no check).
    check_path: Optional[Callable[[Optional[Path]], None]] = None
    # Exceptions surfaced as a clean message and exit 2.
    errors: tuple = (CookbookError,)


def discover(package: str) -> list[ModuleType]:
    pkg = importlib.import_module(package)
    found = []
    for info in pkgutil.iter_modules(pkg.__path__):
        if info.name.startswith("_"):
            continue
        mod = importlib.import_module(f"{package}.{info.name}")
        missing = [a for a in MODULE_ATTRS if not hasattr(mod, a)]
        if missing:
            raise CookbookError(
                f"module `{package}.{info.name}` is missing {', '.join(missing)}; "
                f"prefix its name with `_` if it is not a subcommand"
            )
        found.append(mod)
    return sorted(found, key=lambda m: m.NAME)


def build_parser(app: CliApp, modules: list[ModuleType]) -> argparse.ArgumentParser:
    common = argparse.ArgumentParser(add_help=False)
    common.add_argument("-p", "--path", type=Path, default=argparse.SUPPRESS, help=app.path_help)
    parser = argparse.ArgumentParser(prog=app.prog, description=app.description, parents=[common])
    parser.add_argument("--version", action="version", version=f"{app.prog} {app.version}")
    sub = parser.add_subparsers(dest="module", metavar="<module>", required=False)
    for mod in modules:
        sp = sub.add_parser(mod.NAME, help=mod.HELP, description=mod.HELP, parents=[common])
        mod.register(sp)
        sp.set_defaults(_module=mod)
    return parser


def print_module_table(ui: UI, app: CliApp, modules: list[ModuleType]) -> None:
    ui.title(f"{app.prog} {app.version}")
    ui.info(escape(f"Usage: {app.prog} [-p PATH] <module> [args]"))
    ui.blank()
    ui.table(["module", "description"], [[escape(m.NAME), escape(m.HELP)] for m in modules],
             title="Modules")
    ui.blank()
    ui.info(f"Run `{app.prog} <module> --help` for module-specific options.")


def main(app: CliApp, argv: Optional[list] = None) -> int:
    argv = list(sys.argv[1:] if argv is None else argv)
    ui = UI()
    try:
        modules = discover(app.modules_package)
        args = build_parser(app, modules).parse_args(argv)
        explicit = getattr(args, "path", None)
        if app.check_path is not None:
            app.check_path(explicit)
        if not getattr(args, "module", None):
            print_module_table(ui, app, modules)
            return 0
        ctx = app.make_context(explicit, ui)
        return int(args._module.run(args, ctx) or 0)
    except app.errors as e:
        ui.error(escape(str(e)))
        return 2
    except KeyboardInterrupt:
        ui.warn("Interrupted.")
        return 130
