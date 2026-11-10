"""`cookr implements` — add or remove an implementation row in `index.json`.

An index-only change: no artifact is bumped. A new row starts `unverified`
(`planned` with `--planned`, which names code that need not exist yet).
"""

from __future__ import annotations

import argparse

from rich.markup import escape

from ..core.conformance import check_location
from ..core.errors import CookbookError
from ..core.identity import is_uuid
from ..core.index import (INDEX_FILE, Conformance, Implementation, Index, load_index,
                          save_index, sync_from_folders)
from ..core.repoconfig import PLATFORMS
from .inventory import require_config

NAME = "implements"
HELP = "Record (or --remove) the code that implements an artifact, in index.json."


def register(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("value", metavar="UUID|RDID", help="The artifact implemented.")
    parser.add_argument("location", nargs="?", default=None,
                        help="Repo-relative file or directory (or a URL) implementing it.")
    parser.add_argument("--platform", default=None, help=f"One of {', '.join(PLATFORMS)}.")
    parser.add_argument("--planned", action="store_true",
                        help="Record planned code: the location need not exist yet.")
    parser.add_argument("--remove", metavar="LOCATION", default=None,
                        help="Remove the row at this location instead of adding one.")


def _refuse(ctx, message: str) -> int:
    """The index state does not allow the change: logged, exit 1."""
    ctx.ui.error(escape(message))
    return 1


def run(args, ctx) -> int:
    if not require_config(ctx):
        return 2
    cfg = ctx.config
    cookbook = cfg.cookbook_dir
    index = (load_index(cookbook) if (cookbook / INDEX_FILE).is_file()
             else Index(cookbook=cfg.identity))
    sync_from_folders(index, cookbook)
    entry = index.get(args.value.lower() if is_uuid(args.value) else args.value)
    if entry is None:
        return _refuse(ctx, f"{args.value!r} matches no artifact in {cfg.identity.rdid}")

    if args.remove is not None:
        keep = [i for i in entry.implementations if i.location != args.remove]
        if len(keep) == len(entry.implementations):
            return _refuse(ctx, f"{entry.rdid} has no implementation at {args.remove!r}")
        entry.implementations = keep
        save_index(index, cookbook)
        ctx.ui.ok(escape(f"{entry.rdid}: removed {args.remove}"))
        return 0

    loc = args.location
    if args.platform is None:
        raise CookbookError("--platform is required")
    if args.platform not in PLATFORMS:
        raise CookbookError(f"--platform {args.platform!r} is not one of {', '.join(PLATFORMS)}")
    if loc is None and not args.planned:
        raise CookbookError("a location is required (only --planned may omit it)")
    if loc is not None:
        check_location(loc)
        if not args.planned and "://" not in loc and not (cfg.repo_root / loc).exists():
            return _refuse(ctx, f"{loc!r} does not exist in the repo (use --planned for code "
                                "not written yet)")
        for other in index.entries.values():
            if other.id != entry.id and any(i.location == loc for i in other.implementations):
                return _refuse(ctx, f"{loc!r} is already owned by {other.rdid}")
        if any(i.location == loc and i.platform == args.platform for i in entry.implementations):
            return _refuse(ctx, f"{entry.rdid} already lists {loc!r} for {args.platform}")
    state = "planned" if args.planned else "unverified"
    entry.implementations.append(Implementation(args.platform, loc, Conformance(state)))
    save_index(index, cookbook)
    ctx.ui.ok(escape(f"{entry.rdid}: {state} {args.platform} {loc or ''}".rstrip()))
    return 0
