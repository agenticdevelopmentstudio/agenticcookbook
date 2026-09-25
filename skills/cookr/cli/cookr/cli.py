"""Top-level CLI entry point.

Usage:
    cookr [--help] [-p PATH] [--version] <module> [module-args]

`-p` names the target repo root (the directory holding `.cookr.json`).
Without it, cookr walks up from cwd to the first directory holding one.

The scaffold (module discovery, `-p`, the module table, error mapping) is
cookbook's, shared through cookbook.core.cliapp.
"""

from __future__ import annotations

from pathlib import Path
from typing import Optional

from cookbook.core import cliapp
from cookbook.core.errors import CookbookError
from cookbook.core.ui import UI

from . import __version__
from .context import CookrContext
from .core.config import CONFIG_NAME, ConfigError, load_config


def find_repo_root(start: Path, explicit: Optional[Path] = None) -> Optional[Path]:
    if explicit is not None:
        p = explicit.expanduser().resolve()
        if not (p / CONFIG_NAME).is_file():
            raise ConfigError(f"no {CONFIG_NAME} at {p}")
        return p
    start = start.resolve()
    for d in (start, *start.parents):
        if (d / CONFIG_NAME).is_file():
            return d
    return None


def _check_path(explicit: Optional[Path]) -> None:
    # A bad explicit -p is an error even with no module named.
    find_repo_root(Path.cwd(), explicit)


def _context(explicit: Optional[Path], ui: UI) -> CookrContext:
    root = find_repo_root(Path.cwd(), explicit)
    return CookrContext(config=load_config(root / CONFIG_NAME) if root else None, ui=ui)


APP = cliapp.CliApp(
    prog="cookr",
    version=__version__,
    description="Inventory, coverage and extraction prompts for component recipes.",
    modules_package="cookr.modules",
    path_help=f"Repo root holding {CONFIG_NAME} (defaults to discovery from cwd).",
    make_context=_context,
    check_path=_check_path,
    errors=(CookbookError, ConfigError),
)


def main(argv: Optional[list] = None) -> int:
    return cliapp.main(APP, argv)


if __name__ == "__main__":
    raise SystemExit(main())
