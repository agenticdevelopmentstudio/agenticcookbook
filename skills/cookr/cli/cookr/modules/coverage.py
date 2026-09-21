"""`cookr coverage` — which components have a finished recipe."""

from __future__ import annotations

import argparse
import json
import sys

from ..core.coverage import STATES, compute
from .inventory import require_config

NAME = "coverage"
HELP = "Report each component as missing, partial or complete against the recipe corpus."


def register(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--tier", default=None, help="Only this tier.")
    parser.add_argument("--json", action="store_true", help="Emit JSON instead of a table.")
    parser.add_argument(
        "--require", choices=("partial", "complete"), default=None,
        help="Exit 1 if any component in scope is below this state.",
    )


def _row_dict(r) -> dict:
    return {
        "name": r.name, "tier": r.tier, "platforms": list(r.platforms),
        "paths": list(r.paths), "state": r.state, "recipe": r.recipe,
        "problems": list(r.problems),
    }


def run(args, ctx) -> int:
    if not require_config(ctx):
        return 2
    report = compute(ctx.config, tier=args.tier)
    failing = report.below(args.require) if args.require else []

    if args.json:
        sys.stdout.write(json.dumps({
            "rows": [_row_dict(r) for r in report.rows],
            "tally": report.tally(),
            "unmatched_recipes": report.unmatched_recipes,
        }, indent=2) + "\n")
        return 1 if failing else 0

    ctx.ui.title(f"cookr coverage · {ctx.repo_root}")
    ctx.ui.table(
        ["tier", "name", "state", "recipe", "problems"],
        [[r.tier, r.name, r.state, r.recipe or "—", "; ".join(r.problems)] for r in report.rows],
    )
    for tier, counts in report.tally().items():
        ctx.ui.info("  ".join([f"{tier}:"] + [f"{s}={counts[s]}" for s in STATES]))
    if report.unmatched_recipes:
        ctx.ui.section("recipes with no inventory match")
        for slug in report.unmatched_recipes:
            ctx.ui.skip(slug)
    if args.require:
        if failing:
            ctx.ui.error(f"{len(failing)} component(s) below `{args.require}`")
            return 1
        ctx.ui.ok(f"every component in scope is at least `{args.require}`")
    return 0
