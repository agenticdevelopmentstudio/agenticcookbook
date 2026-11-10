"""`cookr upgrade` — bring a repo's cookbook to format 2 (core/upgrade.py).

    cookr upgrade                  upgrade in place (needs a clean git work tree)
    cookr upgrade --dry-run        report what would change; write nothing
    cookr upgrade --rdid adc       name the cookbook instead of deriving it
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from rich.markup import escape

from ..core.repo import repo_top
from ..core.upgrade import UpgradeReport, upgrade

NAME = "upgrade"
HELP = "Upgrade the repo's cookbook to format 2: UUID identity, index.json and UUID links."


def register(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--rdid", default=None,
                        help="The cookbook's rdid (default: from its domain scheme).")
    parser.add_argument("--dry-run", action="store_true", help="Report only; write nothing.")
    parser.add_argument("--json", action="store_true", help="Print the reports as JSON.")


def _rel(path: Path, repo: Path) -> str:
    try:
        return path.relative_to(repo).as_posix()
    except ValueError:
        return str(path)


def _as_json(r: UpgradeReport, repo: Path) -> dict:
    return {"cookbook_dir": _rel(r.cookbook_dir, repo),
            "identity": {"id": r.identity.id, "rdid": r.identity.rdid},
            "artifacts": r.artifacts, "links_rewritten": r.links_rewritten,
            "needs_review": r.needs_review, "dropped_roots": r.dropped_roots,
            "root_conflicts": r.root_conflicts, "left_as_text": r.left_as_text,
            "self_links_dropped": r.self_links_dropped,
            "missing_paths": r.missing_paths, "moved_legacy": r.moved_legacy,
            "files": [_rel(f, repo) for f in r.files]}


def run(args, ctx) -> int:
    start = Path(getattr(args, "path", None) or Path.cwd()).expanduser().resolve()
    repo = repo_top(start) or start
    reports = upgrade(repo, rdid=args.rdid, dry_run=args.dry_run)
    if args.json:
        sys.stdout.write(json.dumps([_as_json(r, repo) for r in reports], indent=2) + "\n")
        return 0
    mode = " (dry run)" if args.dry_run else ""
    ctx.ui.title(f"cookr upgrade{mode} · {repo}")
    if not reports:
        ctx.ui.ok("up to date: everything is format 2")
        return 0
    for r in reports:
        ctx.ui.table(["", ""], [
            ["cookbook", escape(f"{_rel(r.cookbook_dir, repo)} ({r.identity.rdid}, {r.identity.id})")],
            ["artifacts", str(r.artifacts)],
            ["links rewritten", str(r.links_rewritten)],
            ["legacy recipes moved", str(r.moved_legacy)],
            ["files changed", str(len(r.files)) if not args.dry_run else "none (dry run)"],
        ])
        for title, items in (("needs review", r.needs_review), ("dropped roots", r.dropped_roots),
                             ("root conflicts (the first source kept)", r.root_conflicts),
                             ("missing implementation paths", r.missing_paths),
                             ("left as text (names no artifact)", r.left_as_text),
                             ("self-links dropped", r.self_links_dropped)):
            if items:
                ctx.ui.section(f"{title} ({len(items)})")
                for item in items:
                    ctx.ui.warn(escape(item))
    ctx.ui.ok("dry run: nothing written" if args.dry_run else "upgraded to format 2")
    return 0
