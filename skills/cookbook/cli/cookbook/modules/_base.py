"""Module protocol.

A `cookbook` subcommand is a module file under `cookbook.modules` that exposes:

    NAME: str                       # subcommand name shown in CLI
    HELP: str                       # short help line
    def register(subparsers): ...   # add a subparser; configure its args
    def run(args, ctx): ...         # execute; return exit code

`ctx` is a CookbookContext built by cli._context; discovery and dispatch live
in core/cliapp.py.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from ..core.ui import UI


@dataclass
class CookbookContext:
    cwd: Path
    cookbook_root: Path | None
    references_dir: Path
    ui: UI
