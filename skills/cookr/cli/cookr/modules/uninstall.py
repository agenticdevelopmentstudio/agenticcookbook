"""`cookr uninstall` — remove what `cookr install` put in place, by its receipt."""

from __future__ import annotations

import argparse

from rich.markup import escape

from ..core import install as inst
from .install import ERRORS, add_target_args, installer, show

NAME = "uninstall"
HELP = ("Remove what `cookr install` installed, as its receipt lists: unregister the routed "
        "set, delete it, and remove the always-on skill (restoring any skill it replaced).")


def register(parser: argparse.ArgumentParser) -> None:
    add_target_args(parser)
    parser.add_argument("--force", action="store_true",
                        help="Also remove an always-on skill edited since it was installed.")
    parser.add_argument("--every-library", action="store_true",
                        help="Every library the receipt lists, not just --library's.")


def run(args, ctx) -> int:
    if args.every_library and args.library:
        ctx.ui.error("--every-library and --library name different things; give one")
        return 2
    try:
        if args.target:
            i = installer(args, [])
        else:  # everything the receipt lists, on every host
            i = inst.Installer(folders=[], library=args.library, routed=True,
                               targets=[inst.HostTarget(h, (h.name,)) for h in inst.hosts_mod.manifest().values()],
                               router=inst.Router.find())
        statuses = i.uninstall(force=args.force, every_library=args.every_library, dry_run=args.dry_run)
    except ERRORS as e:
        ctx.ui.error(escape(str(e)))
        return 2
    return show(ctx, args, f"cookr uninstall{' --dry-run' if args.dry_run else ''}", statuses)
