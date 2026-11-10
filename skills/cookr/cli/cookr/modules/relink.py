"""`cookr relink` — rewrite the index's implementation locations after code moves."""

from __future__ import annotations

import argparse
import json
import sys

from rich.markup import escape

from ..core.relink import git_renames, relink
from .inventory import require_config

NAME = "relink"
HELP = "Follow moved code: rewrite index implementation locations from git's renames."


def register(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--since", default="HEAD",
                        help="Renames since this commit, plus what is staged (default: HEAD, "
                             "i.e. staged `git mv`s only).")
    parser.add_argument("--dry-run", action="store_true", help="Report without writing.")
    parser.add_argument("--json", action="store_true", help="Emit JSON instead of a report.")


def run(args, ctx) -> int:
    if not require_config(ctx):
        return 2
    cfg = ctx.config
    changes = relink(cfg, git_renames(cfg.repo_root, args.since), dry_run=args.dry_run)
    trouble = any(c.lost for c in changes)
    if args.json:
        sys.stdout.write(json.dumps([{
            "spec": c.spec, "rows": [{"from": a, "to": b} for a, b in c.rows],
            "lost": c.lost, "folder": list(c.folder),
        } for c in changes], indent=2) + "\n")
        return 1 if trouble else 0
    ctx.ui.title(f"cookr relink{' (dry run)' if args.dry_run else ''} · {cfg.repo_root}")
    for c in changes:
        ctx.ui.section(escape(c.spec))
        for a, b in c.rows:
            ctx.ui.info(escape(f"  {a} → {b}"))
        if c.folder:
            ctx.ui.info(escape(f"  folder {c.folder[0]} → {c.folder[1]}"))
        for p in c.lost:
            ctx.ui.error(escape(f"  gone, no rename to follow: {p}"))
    moved = sum(1 for c in changes if c.rows or c.folder)
    ctx.ui.ok(f"{moved} spec(s) {'would be ' if args.dry_run else ''}relinked")
    return 1 if trouble else 0
