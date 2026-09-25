"""`cookr organize` — convert a flat `.cookr.json` corpus into a library cookbook.

    cookr organize plan --out plan.json    propose where each recipe goes (edit it)
    cookr organize apply --plan plan.json  carry the plan out in the git work tree
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from pathlib import Path

from rich.markup import escape

from ..core.legacy import CONFIG_NAME, load_legacy
from ..core.organize import OrganizeError, apply, plan

NAME = "organize"
HELP = "Convert a flat .cookr.json recipe corpus into a cookbook/ tree that mirrors the code."
ACTIONS = ("plan", "apply")


def register(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("oaction", nargs="?", choices=ACTIONS, help="Omit to list the actions.")
    parser.add_argument("--out", type=Path, default=None,
                        help="plan: write the plan here instead of printing it.")
    parser.add_argument("--plan", type=Path, default=None, help="apply: the plan to carry out.")
    parser.add_argument("--author", default="",
                        help="apply: Change History author (default: git config user.name).")
    parser.add_argument("--json", action="store_true", help="apply: report as JSON.")


def _plan(args, ctx) -> int:
    if ctx.legacy is None:
        ctx.ui.error(f"cookr organize plan: no {CONFIG_NAME} found; nothing to convert.")
        return 2
    data = plan(load_legacy(ctx.legacy))
    text = json.dumps(data, indent=2) + "\n"
    if args.out is None:
        sys.stdout.write(text)
        return 0
    args.out.write_text(text, encoding="utf-8")
    ctx.ui.title(f"cookr organize plan · {ctx.legacy.parent}")
    groups = Counter(m["to"].split("/", 1)[0] if "/" in m["to"] else "(top level)"
                     for m in data["moves"])
    ctx.ui.table(["group", "specs"], [[escape(g), str(n)] for g, n in sorted(groups.items())])
    if data["unmatched"]:
        ctx.ui.section(f"no source files ({len(data['unmatched'])})")
        for slug in data["unmatched"]:
            ctx.ui.skip(escape(slug))
    ctx.ui.ok(f"{len(data['moves'])} move(s) written to {args.out}")
    return 0


def _apply(args, ctx) -> int:
    if args.plan is None:
        ctx.ui.error("cookr organize apply: --plan is required.")
        return 2
    if ctx.legacy is None:
        ctx.ui.error(f"cookr organize apply: no {CONFIG_NAME} found; nothing to convert.")
        return 2
    data = json.loads(args.plan.read_text(encoding="utf-8"))
    repo = ctx.legacy.parent
    try:
        done = apply(data, repo, author=args.author)
    except OrganizeError as e:
        ctx.ui.error(f"cookr organize apply: {e}")
        return 2
    if args.json:
        sys.stdout.write(json.dumps({
            "moved": done.moved, "rewritten": done.rewritten, "manifest": done.manifest,
            "bump_failures": [{"file": f, "reason": r} for f, r in done.bump_failures],
            "leftovers": done.leftovers,
        }, indent=2) + "\n")
    else:
        ctx.ui.title(f"cookr organize apply · {repo}")
        ctx.ui.ok(f"moved {done.moved} spec(s); wrote {done.manifest}")
        ctx.ui.info(f"rewrote references in {len(done.rewritten)} file(s)")
        for f, reason in done.bump_failures:
            ctx.ui.error(escape(f"not bumped: {f}: {reason}"))
        for f in done.leftovers:
            ctx.ui.skip(escape(f"left in place: {f}"))
    return 1 if done.bump_failures else 0


def run(args, ctx) -> int:
    if not args.oaction:
        ctx.ui.title("cookr organize — available actions")
        for a in ACTIONS:
            ctx.ui.info(f"  {a}")
        return 0
    return _plan(args, ctx) if args.oaction == "plan" else _apply(args, ctx)
