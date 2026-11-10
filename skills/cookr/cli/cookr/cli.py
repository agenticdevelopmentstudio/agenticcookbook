"""Top-level CLI entry point.

Usage:
    cookr [--help] [-p PATH] [--version] <module> [module-args]

`-p` names the target repo root (the directory holding `.cookr.json` or
`cookbook/cookbook.json`), or the cookbook directory itself. Without it, cookr
walks up from cwd to the first directory that holds one (core/repoconfig.py).
A repo on an older format leaves the config unread with a `cookr upgrade` hint;
cookr never upgrades it unasked.
The maintenance modules (update, validate, lint) also accept a cookbook with no
`cookbook.json`, such as agenticcookbook's own (core/roots.py).

The scaffold (module discovery, `-p`, the module table, error mapping) lives
in core/cliapp.py.
"""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Optional


from cookr.core import cliapp, roots
from cookr.core.repo import repo_top
from cookr.core.upgrade import needs_upgrade
from cookr.core.errors import CookbookError
from cookr.core.ui import UI

from . import __version__
from .context import CookrContext
from .core.identity import MANIFEST
from .core.repoconfig import (
    CONFIG_NAME,
    COOKBOOK_DIR,
    Config,
    ConfigError,
    config_for_cookbook,
    find_repo,
    load_repo_config,
)


def _find(start: Path, explicit: Optional[Path]) -> tuple[Optional[Path], Optional[Path]]:
    """(the repo root, the cookbook directory when `-p` named one), each None when absent.
    A repo root holds `.cookr.json` or `cookbook/cookbook.json`."""
    if explicit is None:
        return find_repo(start), None
    p = explicit.expanduser().resolve()
    if (p / CONFIG_NAME).is_file() or (p / COOKBOOK_DIR / MANIFEST).is_file():
        return p, None
    if (p / MANIFEST).is_file():
        return p.parent, p
    if roots.resolve(p, p) is None:
        raise ConfigError(f"no {CONFIG_NAME}, {COOKBOOK_DIR}/{MANIFEST} or cookbook directory at {p}")
    return None, None


def _load(repo: Path, cookbook: Optional[Path]) -> Config:
    """The repo config: `.cookr.json` when the repo has one, else the cookbook alone (no roots)."""
    if (repo / CONFIG_NAME).is_file():
        config = load_repo_config(repo)
        if cookbook is None or config.cookbook_dir.resolve() == cookbook.resolve():
            return config
    return config_for_cookbook(cookbook or repo / COOKBOOK_DIR)


def _check_path(explicit: Optional[Path]) -> None:
    # A bad explicit -p is an error even with no module named.
    _find(Path.cwd(), explicit)


def _format1_notice(explicit: Optional[Path], hook: bool) -> None:
    """Say, on stderr, that a format-1 repo found from `-p` or cwd can be upgraded.
    Never writes anything: converting a cookbook rewrites many files, so it runs
    only when the agent chooses to run `cookr upgrade` and then commits it itself.
    The command carries on against the repo as it is. Silent in the hook's check,
    whose output is the hook's own message, and outside any cookbook."""
    if hook:
        return
    start = (explicit or Path.cwd()).expanduser().resolve()
    repo = repo_top(start) or start
    if needs_upgrade(repo):
        sys.stderr.write("cookr: this cookbook is format 1. `cookr upgrade` converts it to "
                         "format 2 when you choose to; review and commit that on its own.\n")


def _hook_run(args) -> bool:
    """Whether this is the hook's `check --hook`, whose every message goes to stderr."""
    module = getattr(args, "_module", None)
    return getattr(module, "NAME", None) == "check" and bool(getattr(args, "hook", False))


def _context(explicit: Optional[Path], ui: UI, module: str = "", args=None) -> CookrContext:
    """A config cookr cannot read (bad JSON, an older format) leaves `config`
    None and says why in `config_error`: only the modules that need the config
    refuse, never validate, lint, compile or install."""
    if module != "upgrade":
        _format1_notice(explicit, hook=_hook_run(args))
    if getattr(getattr(args, "_module", None), "CREATES_REPO", False):
        # `adopt` makes the repo -p names, so -p need only be a directory.
        target = (explicit or Path.cwd()).expanduser().resolve()
        if not target.is_dir():
            raise ConfigError(f"no directory at {target}")
        return CookrContext(config=None, ui=ui, cwd=target)
    repo, cookbook = _find(Path.cwd(), explicit)
    config, error = None, None
    if repo is not None:
        try:
            config = _load(repo, cookbook)
        except ConfigError as e:
            error = str(e)
    # A `.cookr.json` says where its cookbook is (`cookbook`, possibly not `cookbook/`).
    if config is not None and config.config_file is not None and cookbook is None:
        cookbook_root = config.cookbook_dir
    else:
        cookbook_root = roots.resolve(Path.cwd(), explicit)
    return CookrContext(config=config, ui=ui, config_error=error, cookbook_root=cookbook_root)


APP = cliapp.CliApp(
    prog="cookr",
    version=__version__,
    description="Inventory, coverage, extraction prompts, arrangement and maintenance for a cookbook.",
    modules_package="cookr.modules",
    path_help=f"Repo root holding {CONFIG_NAME} or {COOKBOOK_DIR}/{MANIFEST} (defaults to discovery from cwd).",
    make_context=_context,
    pass_args=True,
    check_path=_check_path,
    errors=(CookbookError, ConfigError),
    # The hook forwards only stderr, so a `check --hook` error must land there.
    ui_on_stderr=_hook_run,
)


def main(argv: Optional[list] = None) -> int:
    return cliapp.main(APP, argv)


if __name__ == "__main__":
    raise SystemExit(main())
