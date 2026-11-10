"""`cookr id` — look an artifact up by UUID or rdid, in either direction."""

from __future__ import annotations

import argparse
import json
import sys

from ..core.errors import CookbookError
from ..core.links import format_link, lookup, resolver_for
from .inventory import require_config

NAME = "id"
HELP = "Print an artifact's uuid, rdid, path and kind from its uuid or rdid."


def register(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("value", metavar="UUID|RDID",
                        help="An artifact UUID or rdid (`<cookbook>/<artifact>` for a dependency).")
    parser.add_argument("--json", action="store_true", help="Emit JSON instead of a line.")


def run(args, ctx) -> int:
    if not require_config(ctx):
        return 2
    try:
        link, entry = lookup(args.value, resolver_for(ctx.config))
    except CookbookError as e:
        ctx.ui.error(str(e))
        return 1
    uuid = format_link(link)
    if args.json:
        sys.stdout.write(json.dumps({"uuid": uuid, "rdid": entry.rdid, "path": entry.path,
                                     "kind": entry.kind}, indent=2) + "\n")
    else:
        sys.stdout.write(f"{uuid} {entry.rdid} {entry.path} {entry.kind}\n")
    return 0
