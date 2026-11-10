"""Top-level CLI entry point.

Usage:
    cookr [--help] [-p PATH] [--version] <module> [module-args]

`-p` names the target repo root (the directory holding `.cookr.json` or
`cookbook/cookbook.json`), or the cookbook directory itself. Without it, cookr
walks up from cwd to the first directory that holds one (core/repoconfig.py).
A repo on an older format leaves the config unread with a `cookr upgrade` hint.
The maintenance modules (update, validate, lint) also accept a cookbook with no
`cookbook.json`, such as agenticcookbook's own (core/roots.py).

The scaffold (module discovery, `-p`, the module table, error mapping) lives
in core/cliapp.py.
"""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Optional

from rich.markup import escape

from cookr.core import cliapp, roots
from cookr.core.repo import repo_top
from cookr.core.upgrade import DirtyTree, UpgradeError, needs_upgrade, upgrade
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


def _upgrade_paths(repo: Path, reports) -> list[str]:
    """The pathspec that stages every change the upgrade made, and nothing that
    does not exist in the tree or the index: each cookbook dir, the legacy recipes
    dir it emptied, and any other file it wrote or removed (`.cookr.json`)."""
    out: list[str] = []
    for r in reports:
        dirs = [d for d in (r.cookbook_dir, r.legacy_dir) if d is not None]
        for f in r.files:
            owner = next((d for d in dirs if f == d or d in f.parents), f)
            rel = owner.relative_to(repo).as_posix()
            if rel not in out:
                out.append(rel)
    return out


_DIRTY_STEPS = ("commit all your work now (stage every change; a WIP commit is fine), then "
                "run `cookr upgrade`, commit its changes on their own, and continue")


def _upgrade_on_contact(explicit: Optional[Path], ui: UI, hook: Optional[str] = None) -> None:
    """Upgrade a format-1 repo found from `-p` or cwd, then end the run with 3 so
    the upgrade is committed on its own. Same discovery as `cookr upgrade`. A repo
    that cannot be upgraded ends the run with 1, never runs the command against
    format 1. Outside any cookbook this does nothing.

    `hook` is "commit" for `check --staged --hook`, "stop" for the branch check;
    every message then goes to stderr. An upgrade that ran blocks (2) with "cookr:
    commit the cookr upgrade first". A dirty tree, which the upgrade refuses, does
    not block the commit (1, a warning): that commit is how the agent sets its work
    aside, and the message says the steps. On stop it blocks (2) with the same
    steps. Any other refusal blocks (2) with why. Nothing here ever stashes or
    commits the agent's work."""
    start = (explicit or Path.cwd()).expanduser().resolve()
    repo = repo_top(start) or start
    if not needs_upgrade(repo):
        return
    try:
        reports = upgrade(repo)
    except DirtyTree as e:
        if hook:
            paths = "\n  ".join(e.paths)
            let_through = ("This commit is not checked: " if hook == "commit"
                           else "The WIP commit is let through: ")
            sys.stderr.write(f"cookr: the cookbook needs the format 2 upgrade, which needs a "
                             f"clean work tree. {let_through}{_DIRTY_STEPS}. Uncommitted:\n"
                             f"  {paths}\n")
            raise cliapp.ExitWith(1 if hook == "commit" else 2)
        raise cliapp.ExitWith(1, f"cookr: this cookbook needs the format 2 upgrade, which "
                                 f"cannot run yet: {e}")
    except UpgradeError as e:
        if hook:
            sys.stderr.write(f"cookr: the cookbook needs the format 2 upgrade, which "
                             f"cannot run yet: {e}\n")
            raise cliapp.ExitWith(2)
        raise cliapp.ExitWith(1, f"cookr: this cookbook needs the format 2 upgrade, which "
                                 f"cannot run yet: {e}")
    if hook:
        sys.stderr.write("cookr: commit the cookr upgrade first\n")
        raise cliapp.ExitWith(2)
    for r in reports:
        ui.table(["", ""], [
            ["cookbook", escape(f"{r.cookbook_dir.relative_to(repo).as_posix()} ({r.identity.rdid})")],
            ["artifacts", str(r.artifacts)],
            ["links rewritten", str(r.links_rewritten)],
            ["files changed", str(len(r.files))],
        ])
        for item in r.needs_review:
            ui.warn(escape(item))
    cookbook = ", ".join(r.cookbook_dir.relative_to(repo).as_posix() for r in reports)
    paths = " ".join(_upgrade_paths(repo, reports))
    raise cliapp.ExitWith(3, f"cookr upgraded {cookbook}: commit the upgrade on its own "
                             f"(`git add -A {paths} && git commit -m "
                             f"'chore: cookr format 2 upgrade'`), then rerun")


def _hook_run(args) -> bool:
    """Whether this is the hook's `check --hook`, whose every message goes to stderr."""
    module = getattr(args, "_module", None)
    return getattr(module, "NAME", None) == "check" and bool(getattr(args, "hook", False))


def _hook_mode(args) -> Optional[str]:
    """"commit" for the hook's staged check, "stop" for its branch check, else None."""
    if not _hook_run(args):
        return None
    return "commit" if getattr(args, "staged", False) else "stop"


def _context(explicit: Optional[Path], ui: UI, module: str = "", args=None) -> CookrContext:
    """A config cookr cannot read (bad JSON, an older format) leaves `config`
    None and says why in `config_error`: only the modules that need the config
    refuse, never validate, lint, compile or install."""
    if module != "upgrade":
        _upgrade_on_contact(explicit, ui, hook=_hook_mode(args))
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
