"""`cookr inventory` — list the component source files the config names."""

from __future__ import annotations

import argparse
import json
import sys

from ..core.inventory import scan

NAME = "inventory"
HELP = "List component source files under the configured roots."


def register(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--tier", default=None, help="Only this tier.")
    parser.add_argument("--json", action="store_true", help="Emit JSON rows instead of a table.")


def require_config(ctx) -> bool:
    if ctx.config is None:
        ctx.ui.error("No .cookr.json found. Run from inside a configured repo, or pass -p <repo-root>.")
        return False
    return True


def require_known_tier(args, ctx) -> bool:
    """A typo'd `--tier` must be an error, never an empty (green) result."""
    if args.tier is not None and args.tier not in ctx.config.tiers:
        ctx.ui.error(
            f"unknown tier `{args.tier}`; configured tiers: {', '.join(ctx.config.tiers)}"
        )
        return False
    return True


def run(args, ctx) -> int:
    if not require_config(ctx):
        return 2
    if not require_known_tier(args, ctx):
        return 2
    rows = [c for c in scan(ctx.config) if args.tier is None or c.tier == args.tier]
    if args.json:
        sys.stdout.write(json.dumps([{"name": c.name, "path": c.path, "tier": c.tier, "platform": c.platform} for c in rows], indent=2) + "\n")
        return 0
    ctx.ui.title(f"cookr inventory · {ctx.repo_root}")
    ctx.ui.table(["tier", "name", "platform", "path"],
                 [[c.tier, c.name, c.platform, c.path] for c in rows])
    ctx.ui.info(f"{len(rows)} source file(s)")
    return 0
