"""`cookbook skills build` — compile a cookbook-schema tree into a plugin of routed skills."""

from __future__ import annotations

from collections import Counter
from pathlib import Path

from ..skillgen import build as skill_build
from ..skillgen import source as skill_source
from ..skillgen.leaves import DEFAULT_CAP

NAME = "skills"
HELP = "Generate a plugin of routed review/implement/verify skills from a cookbook or recipes repo."

SHOWN_WARNINGS = 15


def register(parser) -> None:
    sub = parser.add_subparsers(dest="skills_action", metavar="<action>", required=True)
    b = sub.add_parser("build", help="Build the plugin (or check it for drift with --check).")
    b.add_argument("--source", type=Path, default=None,
                   help="Cookbook dir, or a repo with .cookr.json (default: the resolved cookbook root).")
    b.add_argument("--out", type=Path, required=True, help="Plugin output directory.")
    b.add_argument("--name", default=None, help="Plugin name (default: `cookbook`, or the .cookr.json scheme).")
    b.add_argument("--cap", type=int, default=DEFAULT_CAP, help=f"Leaf size cap in characters (default {DEFAULT_CAP}).")
    b.add_argument("--check", action="store_true", help="Write nothing; exit 1 if --out differs from a fresh build.")
    b.add_argument("--verbose", action="store_true", help="List every warning, not just the first few.")


def _report_warnings(ui, warnings, verbose: bool) -> None:
    if not warnings:
        return
    counts = Counter(w.kind for w in warnings)
    ui.warn("warnings: " + ", ".join(f"{n} {k}" for k, n in sorted(counts.items())))
    shown = warnings if verbose else warnings[:SHOWN_WARNINGS]
    ui.table(["kind", "where", "detail"], [[w.kind, w.where, w.detail] for w in shown])
    if len(shown) < len(warnings):
        ui.info(f"… {len(warnings) - len(shown)} more (--verbose lists them all).")


def run(args, ctx) -> int:
    start = args.source or ctx.cookbook_root
    if start is None:
        ctx.ui.error("No source: pass --source, or run from inside a cookbook.")
        return 2
    src = skill_source.resolve(start, args.name)
    if src is None:
        ctx.ui.error(f"{start} is neither a cookbook nor a repo with .cookr.json.")
        return 2

    ctx.ui.title(f"cookbook skills build · {src.name} ({src.layout}) · {src.root}")
    result = skill_build.build(src, args.cap)
    ctx.ui.info(
        f"{result.docs} docs → {result.routers} routers, {result.leaves} leaves, {result.rules} rules"
    )
    _report_warnings(ctx.ui, result.warnings, args.verbose)
    if result.errors:
        for err in result.errors:
            ctx.ui.error(err)
        ctx.ui.error(f"{len(result.errors)} error(s); nothing written.")
        return 1

    out = args.out.resolve()
    if args.check:
        drift = skill_build.drift(result.files, skill_build.read_tree(out))
        if drift:
            ctx.ui.table(["drift", "path"], [list(d) for d in drift[:50]])
            ctx.ui.error(f"{out} is stale: {len(drift)} file(s) differ. Re-run without --check.")
            return 1
        ctx.ui.ok(f"{out} is current ({len(result.files)} files).")
        return 0

    try:
        skill_build.write(out, result.files)
    except skill_build.RefusedOutput as e:
        ctx.ui.error(str(e))
        return 2
    ctx.ui.ok(f"Wrote {len(result.files)} files to {out}.")
    return 0
