"""`cookr skills sync` — keep this repo's skill sets (its cookbook and its dependencies') compiled and registered."""

from __future__ import annotations

import argparse
import json
import sys

from rich.markup import escape

from ..core import install as inst
from ..core import skillsync
from .inventory import require_config

NAME = "skills"
HELP = ("Skill sets per cookbook. `sync` compiles this repo's cookbook and each reachable "
        "dependency cookbook into $COOKR_HOME/sets/<rdid> when stale or missing and registers "
        "it with skill-router, scoped to the repos that use it. Never touches the always-on skill.")


def register(parser: argparse.ArgumentParser) -> None:
    sub = parser.add_subparsers(dest="action", metavar="ACTION", required=True)
    sync = sub.add_parser("sync", help="Compile and register what is stale or missing.")
    sync.add_argument("--json", action="store_true", help="Emit JSON instead of lines.")


def run(args, ctx) -> int:
    if not require_config(ctx):
        return 2
    try:
        lines = skillsync.sync(ctx.config, lambda m: ctx.ui.warn(escape(m)))
    except inst.RouterError as e:
        ctx.ui.error(escape(str(e)))
        return 1
    failed = any(l.action == skillsync.BROKEN for l in lines)
    if args.json:
        sys.stdout.write(json.dumps({"libraries": [l.as_json() for l in lines], "ok": not failed},
                                    indent=2) + "\n")
    else:
        for l in lines:
            (ctx.ui.error if l.action == skillsync.BROKEN else ctx.ui.info)(escape(l.text()))
    return 1 if failed else 0
