"""`cookr confirm` — record that code was checked against its recipe.

An index-only change: no artifact is bumped.
"""

from __future__ import annotations

import argparse

from rich.markup import escape

from ..core.conformance import check_location, current_hash, entry_version, is_url
from ..core.errors import CookbookError
from ..core.history import parse_version
from ..core.identity import is_uuid
from ..core.index import INDEX_FILE, Conformance, Index, load_index, save_index, sync_from_folders
from ..core.repoconfig import PLATFORMS
from .inventory import require_config

NAME = "confirm"
HELP = "Record an artifact's implementations as confirmed against its current version."


def register(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("value", metavar="UUID|RDID", help="The artifact checked.")
    parser.add_argument("--platform", default=None, help=f"Only this platform ({', '.join(PLATFORMS)}).")
    parser.add_argument("--location", default=None, help="Only the row at this location.")


def run(args, ctx) -> int:
    if not require_config(ctx):
        return 2
    cfg = ctx.config
    if args.platform is not None and args.platform not in PLATFORMS:
        raise CookbookError(f"--platform {args.platform!r} is not one of {', '.join(PLATFORMS)}")
    cookbook = cfg.cookbook_dir
    index = (load_index(cookbook) if (cookbook / INDEX_FILE).is_file()
             else Index(cookbook=cfg.identity))
    sync_from_folders(index, cookbook)
    entry = index.get(args.value.lower() if is_uuid(args.value) else args.value)
    if entry is None:
        ctx.ui.error(escape(f"{args.value!r} matches no artifact in {cfg.identity.rdid}"))
        return 1
    rows = [i for i in entry.implementations
            if (args.platform is None or i.platform == args.platform)
            and (args.location is None or i.location == args.location)]
    if not rows:
        ctx.ui.error(escape(f"{entry.rdid} has no matching implementation"))
        return 1
    for i in rows:
        if not i.location:
            ctx.ui.error(escape(f"{entry.rdid}: the {i.platform} row is planned with no location"))
            return 1
        check_location(i.location)  # a hand-edited row may point outside the repo
        if not is_url(i.location) and not (cfg.repo_root / i.location).exists():
            ctx.ui.error(escape(f"{entry.rdid}: {i.location!r} does not exist in the repo"))
            return 1
    version = entry_version(cookbook, entry)
    if parse_version(version) is None:
        ctx.ui.error(escape(f"{entry.rdid}: its version {version!r} is missing or not X.Y.Z "
                            "(or the artifact cannot be read); nothing to confirm against"))
        return 1
    for i in rows:
        i.conformance = Conformance("confirmed", version, current_hash(cfg, i))
    save_index(index, cookbook)
    for i in rows:
        ctx.ui.ok(escape(f"{entry.rdid}: confirmed {i.platform} {i.location} at {version}"))
    return 0
