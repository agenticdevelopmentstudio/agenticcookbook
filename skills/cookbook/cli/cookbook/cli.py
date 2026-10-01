"""Top-level CLI entry point.

Usage:
    cookbook [--help] [-p PATH] [--version] <module> [module-args]

The scaffold (module discovery, `-p`, the module table, error mapping) is
shared with cookr; see core/cliapp.py.
"""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Optional

from . import __version__
from .core import cliapp, refs, roots
from .core.ui import UI
from .modules._base import CookbookContext


def _context(explicit: Optional[Path], ui: UI) -> CookbookContext:
    cwd = Path.cwd()
    return CookbookContext(
        cwd=cwd,
        cookbook_root=roots.resolve(cwd, explicit),
        references_dir=refs.references_dir(),
        ui=ui,
    )


APP = cliapp.CliApp(
    prog="cookbook",
    version=__version__,
    description="Create and maintain cookbook directories (recipes, reference, indexes).",
    modules_package="cookbook.modules",
    path_help="Path to the cookbook dir (defaults to discovery from cwd).",
    make_context=_context,
)


def main(argv: list[str] | None = None) -> int:
    return cliapp.main(APP, argv)


if __name__ == "__main__":
    raise SystemExit(main())
