"""`cookr install` — compile a cookbook's skills and put them where agents reach them."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Optional

from rich.markup import escape

from ..core import install as inst
from ..core import roots
from ..core.artifact import find_folders, unconverted
from ..core.always_on import CONCERNS
from ..core.skill import DEFAULT_LIBRARY, SkillError, library_name, templates_root

NAME = "install"
HELP = ("Compile skills and install them: the routed set registered with skill-router, and "
        "the always-on principles skill in each host's skills dir. --check reports each item "
        "OK, MISSING, DRIFT or BROKEN.")

_STYLE = {inst.OK: "ok", inst.MISSING: "warn", inst.DRIFT: "warn", inst.BROKEN: "error"}
# Anything install or uninstall can raise for bad input or a failed write:
# reported, exit 2. The receipt is written either way (core/install.py).
ERRORS = (ValueError, inst.RouterError, OSError)


def _library(value: str) -> Optional[str]:
    try:
        return library_name(value)
    except SkillError as e:
        raise argparse.ArgumentTypeError(str(e)) from e


def add_target_args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--target", action="append", metavar="T",
                        help=f"`{inst.ROUTED}` (the routed set), or a host target for the always-on "
                             "skill: `claude` (every model on it), `claude.opus`, `claude.opus-5-5`. "
                             "Repeatable. Default: the routed set and every host whose home exists, "
                             "at the target it was installed for.")
    parser.add_argument("--library", type=_library,
                        help=f"The library the set is named, routed and registered as "
                             f"(default: {DEFAULT_LIBRARY}, whose skill names carry no prefix).")
    parser.add_argument("--dry-run", action="store_true", help="Report what would change; change nothing.")
    parser.add_argument("--json", action="store_true", help="Emit JSON instead of a report.")


def register(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("paths", nargs="*", type=Path,
                        help="Artifact folders or directories to search (default: the cookbook, "
                             "found as -p or from cwd).")
    add_target_args(parser)
    parser.add_argument("--check", action="store_true",
                        help="Change nothing; exit 1 unless every item is OK.")
    parser.add_argument("--adopt", action="store_true",
                        help="Replace a skill dir cookr did not install (it is moved to "
                             "$COOKR_HOME/backup/, and uninstall puts it back).")
    parser.add_argument("--force", action="store_true",
                        help="Overwrite an always-on skill edited since it was installed.")
    parser.add_argument("--replace", action="store_true",
                        help="Install a library already installed from other paths, replacing "
                             "every skill it installed from them.")
    parser.add_argument("--concerns", type=Path,
                        help=f"The pipeline concerns list (default: <cookbook>/{CONCERNS}, the "
                             "cookbook holding the first path).")


def installer(args, folders, concerns=None, origin=(), cookbook=None) -> inst.Installer:
    routed, targets = inst.select(args.target, receipt=inst.read_receipt(inst.home()))
    return inst.Installer(folders=folders, library=args.library, routed=routed, targets=targets,
                          concerns=concerns, router=inst.Router.find(), origin=origin,
                          templates=templates_root(cookbook))


def show(ctx, args, title: str, statuses: list[inst.Status]) -> int:
    failed = any(s.failed for s in statuses)
    if args.json:
        sys.stdout.write(json.dumps({"items": [s.as_json() for s in statuses], "ok": not failed},
                                    indent=2) + "\n")
        return 1 if failed else 0
    ctx.ui.title(title)
    for s in statuses:
        line = f"{s.state.upper():8} {s.item}" + (f"  [{s.action}]" if s.action else "")
        line += f"  {s.detail}" if s.detail else ""
        getattr(ctx.ui, _STYLE[s.state])(escape(line))
    if not statuses:
        ctx.ui.info("nothing to do")
    return 1 if failed else 0


def _cookbook(path: Path) -> Optional[Path]:
    """The cookbook holding `path`."""
    return roots.resolve(path if path.is_dir() else path.parent)


def _concerns(path: Path) -> Optional[Path]:
    """The concerns list of the cookbook holding `path`, if it has one."""
    root = _cookbook(path)
    return root / CONCERNS if root is not None else None


def run(args, ctx) -> int:
    paths = args.paths or ([ctx.cookbook_root] if ctx.cookbook_root else [])
    if not paths:
        ctx.ui.error("no cookbook found: run inside one, pass -p <repo-root>, or name the paths to install")
        return 2
    missing = [p for p in paths if not p.exists()]
    if missing:
        ctx.ui.error(escape(f"no such path: {', '.join(map(str, missing))}"))
        return 2
    if args.check and (args.adopt or args.dry_run or args.force or args.replace):
        ctx.ui.error("--check changes nothing; it takes no --adopt, --dry-run, --force or --replace")
        return 2
    try:
        stray = unconverted(paths)
        if stray:
            # Installing without them would drop (or uninstall) their skills unnoticed.
            ctx.ui.error(escape(f"{len(stray)} artifact doc(s) have no source folder: "
                                f"{', '.join(map(str, stray[:5]))}{' …' if len(stray) > 5 else ''}; "
                                "run `cookr convert` on them first"))
            return 2
        folders = find_folders(paths)
        if not folders:
            # Installing nothing would remove every skill installed before.
            ctx.ui.error(escape(f"no artifact folders under {', '.join(map(str, paths))}; nothing to "
                                "install (`cookr uninstall` removes an installed set)"))
            return 2
        i = installer(args, folders, args.concerns or _concerns(paths[0]),
                      origin=tuple(str(p.resolve()) for p in paths), cookbook=_cookbook(paths[0]))
        if args.check:
            return show(ctx, args, "cookr install --check", i.check())
        statuses = i.install(adopt=args.adopt, force=args.force, replace=args.replace,
                             dry_run=args.dry_run)
    except ERRORS as e:
        ctx.ui.error(escape(str(e)))
        return 2
    return show(ctx, args, f"cookr install{' --dry-run' if args.dry_run else ''}", statuses)
