"""Top-level CLI entry point.

Usage:
    cookr [--help] [-p PATH] [--version] <module> [module-args]

`-p` names the target repo root (the directory holding `.cookr.json`).
Without it, cookr walks up from cwd to the first directory holding one.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Optional

from cookbook.core.errors import CookbookError
from cookbook.core.ui import UI

from . import __version__
from .context import CookrContext
from .core.config import CONFIG_NAME, ConfigError, load_config
from .registry import discover


def find_repo_root(start: Path, explicit: Optional[Path] = None) -> Optional[Path]:
    if explicit is not None:
        p = explicit.expanduser().resolve()
        return p if (p / CONFIG_NAME).is_file() else None
    start = start.resolve()
    for d in (start, *start.parents):
        if (d / CONFIG_NAME).is_file():
            return d
    return None


def _build_parser(modules):
    common = argparse.ArgumentParser(add_help=False)
    common.add_argument(
        "-p", "--path", type=Path, default=None,
        help=f"Repo root holding {CONFIG_NAME} (defaults to discovery from cwd).",
    )
    parser = argparse.ArgumentParser(
        prog="cookr",
        description="Inventory, coverage and extraction prompts for component recipes.",
        parents=[common],
    )
    parser.add_argument("--version", action="version", version=f"cookr {__version__}")
    sub = parser.add_subparsers(dest="module", metavar="<module>", required=False)
    for mod in modules:
        sp = sub.add_parser(mod.NAME, help=mod.HELP, description=mod.HELP, parents=[common])
        mod.register(sp)
        sp.set_defaults(_module=mod)
    return parser


def _print_module_table(ui: UI, modules) -> None:
    ui.title(f"cookr {__version__}")
    ui.info("Usage: cookr [-p PATH] <module> [args]")
    ui.blank()
    ui.table(["module", "description"], [[m.NAME, m.HELP] for m in modules], title="Modules")
    ui.blank()
    ui.info("Run `cookr <module> --help` for module-specific options.")


def main(argv: Optional[list] = None) -> int:
    argv = list(sys.argv[1:] if argv is None else argv)
    ui = UI()
    try:
        modules = discover()
        parser = _build_parser(modules)
        args = parser.parse_args(argv)
        if not getattr(args, "module", None):
            _print_module_table(ui, modules)
            return 0
        cwd = Path.cwd()
        root = find_repo_root(cwd, args.path)
        config = load_config(root / CONFIG_NAME) if root else None
        ctx = CookrContext(cwd=cwd, repo_root=root, config=config, ui=ui)
        return int(args._module.run(args, ctx) or 0)
    except (CookbookError, ConfigError) as e:
        ui.error(str(e))
        return 2
    except KeyboardInterrupt:
        ui.warn("Interrupted.")
        return 130


if __name__ == "__main__":
    raise SystemExit(main())
