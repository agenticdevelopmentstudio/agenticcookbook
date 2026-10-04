"""`cookr convert` — turn single-file artifacts into source folders."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from rich.markup import escape

from ..core.artifact import find_documents
from ..core.artifact_build import convert

NAME = "convert"
HELP = "Convert single-file artifacts (<name>.md) into source folders (<name>/artifact.json + parts)."


def register(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("paths", nargs="*", type=Path,
                        help="Artifact files or directories to search (default: ./cookbook).")
    parser.add_argument("--out", type=Path,
                        help="Write folders under this directory, mirroring their path below "
                             "the current directory (default: beside each source).")
    parser.add_argument("--remove-source", action="store_true",
                        help="Delete each .md once its folder is written and verified.")
    parser.add_argument("--update", action="store_true",
                        help="For an artifact that already has a folder, fold edits made to its .md "
                             "back into the folder (other files there are kept) and recompile the .md.")
    parser.add_argument("--force", action="store_true",
                        help="With --update, fold the .md in even over edits made to the folder since.")
    parser.add_argument("--dry-run", action="store_true",
                        help="Verify that every artifact converts losslessly; write nothing.")
    parser.add_argument("--json", action="store_true", help="Emit JSON instead of a report.")


def report(ctx, results, verb: str) -> None:
    for r in results:
        if r.status == "error":
            ctx.ui.error(escape(f"{r.source}: {r.detail}"))
        elif r.problems:
            ctx.ui.warn(escape(f"{r.dest}: {'; '.join(r.problems)}"))
    bad = sum(r.failed for r in results)
    skipped = sum(r.status == "skipped" for r in results)
    shaped = sum(bool(r.problems) for r in results)
    summary = f"{len(results) - bad - skipped} of {len(results)} {verb}"
    if skipped:
        summary += f"; {skipped} already source folders (skipped)"
    if shaped:
        summary += f"; {shaped} with type-shape problems (reported, not fatal)"
    (ctx.ui.error if bad else ctx.ui.ok)(summary)


def run(args, ctx) -> int:
    if args.remove_source and args.dry_run:
        ctx.ui.error("--remove-source and --dry-run contradict each other")
        return 2
    if args.force and not args.update:
        ctx.ui.error("--force applies to --update alone")
        return 2
    if args.update and (args.out or args.remove_source):
        ctx.ui.error("--update works in place; it takes neither --out nor --remove-source")
        return 2
    paths = args.paths or [Path("cookbook")]
    missing = [p for p in paths if not p.exists()]
    if missing:
        ctx.ui.error(escape(f"no such path: {', '.join(map(str, missing))}"))
        return 2
    docs = find_documents(paths)
    not_artifacts = [p for p in paths if p.is_file() and p not in docs]
    if not_artifacts:
        ctx.ui.error(escape(f"not an artifact (no frontmatter `type`): {', '.join(map(str, not_artifacts))}"))
        return 2
    results = convert(docs, base=Path.cwd(), out=args.out,
                      write=not args.dry_run, remove_source=args.remove_source, update=args.update,
                      force=args.force)
    failed = any(r.failed for r in results)
    if args.json:
        sys.stdout.write(json.dumps([r.as_json() for r in results], indent=2) + "\n")
        return 1 if failed else 0
    ctx.ui.title(f"cookr convert{' (dry run)' if args.dry_run else ''}")
    report(ctx, results, "would convert losslessly" if args.dry_run else "converted")
    return 1 if failed else 0
