"""Top-level CLI entry point.

Usage:
    cookr [--help] [-p PATH] [--version] <module> [module-args]

`-p` names the target repo root (the directory holding `cookbook/cookbook.json`),
or the cookbook directory itself. Without it, cookr walks up from cwd to the
first directory that holds one. A repo still on `.cookr.json` is found the same
way, for `cookr organize` to convert. The maintenance modules (update, validate,
lint) also accept a cookbook with no `cookbook.json`, such as agenticcookbook's
own (core/roots.py).

The scaffold (module discovery, `-p`, the module table, error mapping) lives
in core/cliapp.py.
"""

from __future__ import annotations

from pathlib import Path
from typing import Optional

from cookr.core import cliapp, roots
from cookr.core.errors import CookbookError
from cookr.core.ui import UI

from . import __version__
from .context import CookrContext
from .core.config import COOKBOOK_DIR, MANIFEST, ConfigError, find_cookbook, load_config
from .core.legacy import CONFIG_NAME as LEGACY_NAME


def _find(start: Path, explicit: Optional[Path]) -> tuple[Optional[Path], Optional[Path]]:
    """(the cookbook directory, the legacy `.cookr.json`), each None when absent."""
    if explicit is not None:
        p = explicit.expanduser().resolve()
        cookbook = next((c for c in (p / COOKBOOK_DIR, p) if (c / MANIFEST).is_file()), None)
        legacy = p / LEGACY_NAME if (p / LEGACY_NAME).is_file() else None
        if cookbook is None and legacy is None and roots.resolve(p, p) is None:
            raise ConfigError(f"no {COOKBOOK_DIR}/{MANIFEST}, {LEGACY_NAME} or cookbook directory at {p}")
        return cookbook, legacy
    cookbook = find_cookbook(start)
    legacy = None
    for d in (start.resolve(), *start.resolve().parents):
        if (d / LEGACY_NAME).is_file():
            legacy = d / LEGACY_NAME
            break
    return cookbook, legacy


def _check_path(explicit: Optional[Path]) -> None:
    # A bad explicit -p is an error even with no module named.
    _find(Path.cwd(), explicit)


def _context(explicit: Optional[Path], ui: UI) -> CookrContext:
    """A `cookbook.json` cookr cannot read (no `code` block, bad JSON) leaves
    `config` None and says why in `config_error`: only the modules that need
    the config refuse, never validate, lint, compile or install."""
    cookbook, legacy = _find(Path.cwd(), explicit)
    config, error = None, None
    if cookbook:
        try:
            config = load_config(cookbook)
        except ConfigError as e:
            error = str(e)
    return CookrContext(config=config, ui=ui, legacy=legacy, config_error=error,
                        cookbook_root=roots.resolve(Path.cwd(), explicit))


APP = cliapp.CliApp(
    prog="cookr",
    version=__version__,
    description="Inventory, coverage, extraction prompts, arrangement and maintenance for a cookbook.",
    modules_package="cookr.modules",
    path_help=f"Repo root holding {COOKBOOK_DIR}/{MANIFEST} (defaults to discovery from cwd).",
    make_context=_context,
    check_path=_check_path,
    errors=(CookbookError, ConfigError),
)


def main(argv: Optional[list] = None) -> int:
    return cliapp.main(APP, argv)


if __name__ == "__main__":
    raise SystemExit(main())
