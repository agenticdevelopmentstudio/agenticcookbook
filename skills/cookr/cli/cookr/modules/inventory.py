"""`cookr inventory` — list the component source files and the spec each belongs to."""

from __future__ import annotations

import argparse
import json
import sys

from rich.markup import escape

from ..core.inventory import scan
from ..core.recipes import load_corpus

NAME = "inventory"
HELP = "List component source files and the spec that names each."


def register(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--tier", default=None,
                        help="Only this group of the cookbook (a directory, e.g. `ai-plugin-kit/chat`).")
    parser.add_argument("--json", action="store_true", help="Emit JSON rows instead of a table.")


def require_config(ctx) -> bool:
    if ctx.config is None:
        ctx.ui.error("No cookbook/cookbook.json found. Run from inside a repo with a library "
                     "cookbook, or pass -p <repo-root>. A repo still on .cookr.json converts "
                     "with `cookr organize`.")
        return False
    return True


def require_known_tier(args, ctx) -> bool:
    """A typo'd `--tier` must be an error, never an empty (green) result."""
    if args.tier is not None and not ctx.config.is_group(args.tier):
        ctx.ui.error(
            escape(f"unknown group `{args.tier}`; top-level groups: {', '.join(ctx.config.tiers)}")
        )
        return False
    return True


def run(args, ctx) -> int:
    if not require_config(ctx):
        return 2
    if not require_known_tier(args, ctx):
        return 2
    rows = scan(ctx.config, load_corpus(ctx.config.cookbook_dir), tier=args.tier)
    if args.json:
        sys.stdout.write(json.dumps([{"name": c.name, "path": c.path, "tier": c.tier,
                                      "platform": c.platform, "claimed": c.claimed}
                                     for c in rows], indent=2) + "\n")
        return 0
    ctx.ui.title(f"cookr inventory · {ctx.config.repo_root}")
    # Cells are escaped: rich reads `[...]` as markup, and paths carry `[slug]` segments.
    ctx.ui.table(["spec", "claimed", "platform", "path"],
                 [[escape(v) for v in (c.name, "yes" if c.claimed else "no", c.platform, c.path)]
                  for c in rows])
    ctx.ui.info(f"{len(rows)} source file(s)")
    return 0
