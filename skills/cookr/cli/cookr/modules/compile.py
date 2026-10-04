"""`cookr compile` — build a target from artifact source folders."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from rich.markup import escape

from ..core.artifact import find_folders
from ..core import skill as skill_mod
from ..core.artifact_build import TARGETS, compile_doc, unconverted_results
from .convert import report

NAME = "compile"
HELP = ("Compile artifact source folders into a target (doc: the single-file markdown form; "
        "skill: routed skills, one rendering per host and model).")


def register(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("paths", nargs="*", type=Path,
                        help="Artifact folders or directories to search (default: ./cookbook).")
    parser.add_argument("--target", choices=TARGETS, default="doc", help="What to build (default: doc).")
    parser.add_argument("--out", type=Path,
                        help="Write output under this directory. doc: mirroring its path below the "
                             "current directory (default: beside each folder). skill: the skill set's "
                             "directory (required).")
    parser.add_argument("--library",
                        help="skill: the library a library cookbook's skills are named and routed "
                             f"under (default: none, routed as `{skill_mod.DEFAULT_LIBRARY}`).")
    parser.add_argument("--check", action="store_true",
                        help="Write nothing; exit 1 when any output is missing or stale.")
    parser.add_argument("--force", action="store_true",
                        help="doc: overwrite a .md edited since cookr wrote it, discarding the edit.")
    parser.add_argument("--json", action="store_true", help="Emit JSON instead of a report.")


def run(args, ctx) -> int:
    paths = args.paths or ([ctx.cookbook_root] if ctx.cookbook_root else [Path("cookbook")])
    missing = [p for p in paths if not p.exists()]
    if missing:
        ctx.ui.error(escape(f"no such path: {', '.join(map(str, missing))}"))
        return 2
    if args.force and (args.check or args.target != "doc"):
        ctx.ui.error("--force applies to writing the doc target alone")
        return 2
    if args.target == "skill":
        return _skill(args, ctx, paths)
    results = unconverted_results(paths) + compile_doc(find_folders(paths), base=Path.cwd(), out=args.out,
                                                        write=not args.check, force=args.force)
    failed = any(r.failed for r in results)
    if args.json:
        sys.stdout.write(json.dumps([r.as_json() for r in results], indent=2) + "\n")
        return 1 if failed else 0
    ctx.ui.title(f"cookr compile --target {args.target}{' --check' if args.check else ''}")
    for r in results:
        if r.status in ("stale", "missing"):
            ctx.ui.error(escape(f"{r.dest}: {r.status}{': ' + r.detail if r.detail else ''}"))
        elif r.status == "unconverted":
            ctx.ui.error(escape(f"{r.source}: {r.detail}"))
    report(ctx, results, "current" if args.check else "compiled")
    return 1 if failed else 0


def _skill(args, ctx, paths) -> int:
    if args.out is None:
        ctx.ui.error("--target skill needs --out: the skill set's directory")
        return 2
    stray = unconverted_results(paths)
    try:
        rep = skill_mod.compile_set(find_folders(paths), args.out, library=args.library,
                                    templates=skill_mod.templates_root(ctx.cookbook_root) / "skill",
                                    write=not args.check)
    except skill_mod.SkillError as e:
        ctx.ui.error(escape(str(e)))
        return 2
    if args.json:
        sys.stdout.write(json.dumps({"results": [r.as_json() for r in rep.results],
                                     "over_cap": rep.over_cap, "removed": rep.removed,
                                     "unconverted": [str(r.source) for r in stray]},
                                    indent=2) + "\n")
        return 1 if rep.failed or stray else 0
    ctx.ui.title(f"cookr compile --target skill{' --check' if args.check else ''}")
    for r in stray:
        ctx.ui.error(escape(f"{r.source}: {r.detail}"))
    for r in rep.results:
        if r.failed and r.status != "error":  # report() prints errors
            ctx.ui.error(escape(f"{r.dest}: {r.status}{': ' + r.detail if r.detail else ''}"))
    for node, n in sorted(rep.over_cap.items()):
        ctx.ui.error(escape(f"route {node or '(top)'}: {n} entries, over the cap of {skill_mod.FANOUT_CAP}"))
    for rel in rep.removed:
        ctx.ui.info(escape(f"removed {rel}"))
    report(ctx, rep.results, "current" if args.check else "compiled")
    return 1 if rep.failed or stray else 0
