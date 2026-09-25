"""`cookr arrangement` — which specs sit where their code's arrangement puts them."""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter

from rich.markup import escape

from ..core.arrangement import STATES, report
from .inventory import require_config, require_known_tier

NAME = "arrangement"
HELP = "Report each spec as aligned with its code's arrangement, or drifted from it."


def register(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--tier", default=None,
                        help="Only this group of the cookbook (a directory, e.g. `ai-plugin-kit/chat`).")
    parser.add_argument("--all", action="store_true", help="List aligned specs too.")
    parser.add_argument("--json", action="store_true", help="Emit JSON instead of a table.")
    parser.add_argument("--strict", action="store_true", help="Exit 1 if any spec has drifted.")


def run(args, ctx) -> int:
    if not require_config(ctx):
        return 2
    if not require_known_tier(args, ctx):
        return 2
    rows = report(ctx.config, tier=args.tier)
    tally = Counter(r.state for r in rows)
    failing = args.strict and tally["drifted"] > 0
    if args.json:
        sys.stdout.write(json.dumps({
            "rows": [{"name": r.name, "state": r.state, "expected": r.expected} for r in rows],
            "tally": {s: tally[s] for s in STATES},
        }, indent=2) + "\n")
        return 1 if failing else 0
    ctx.ui.title(f"cookr arrangement · {ctx.config.repo_root}")
    shown = [r for r in rows if args.all or r.state != "aligned"]
    ctx.ui.table(["spec", "state", "expected"],
                 [[escape(v) for v in (r.name, r.state, r.expected)] for r in shown])
    ctx.ui.info("  ".join(f"{s}={tally[s]}" for s in STATES))
    if failing:
        ctx.ui.error(f"{tally['drifted']} spec(s) drifted from the code's arrangement")
        return 1
    return 0
