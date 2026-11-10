"""`cookr scope` — the recipes and ingredients a change touches, and their siblings.

Each argument is a path (an existing file, anything with a `/`, or a planned new
file) or an id (a UUID or rdid in this cookbook's index, scoped as if its
implementation were touched). With neither, the branch diff plus the
working tree.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from dataclasses import asdict
from pathlib import Path

from rich.markup import escape

from ..core import changes as git_changes
from ..core.errors import CookbookError
from ..core.identity import is_uuid
from ..core.index import current_index
from ..core.links import resolver_for
from ..core.scope import Scope, compute
from ..core.versions import GitError, base_ref
from .inventory import require_config

NAME = "scope"
HELP = "List the recipes and ingredients a change touches: the minimum, further up, siblings."


def register(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("targets", nargs="*", metavar="PATH|ID",
                        help="Planned or changed files, or artifact UUIDs/rdids "
                             "(default: the branch diff plus the working tree).")
    parser.add_argument("--since", default=None, metavar="REF",
                        help="Diff from this ref instead of the branch's merge base.")
    parser.add_argument("--json", action="store_true", help="Emit the scope as JSON.")


def _rel(cfg, cwd: Path, raw: str) -> str:
    """`raw` as a repo-relative POSIX path: relative to cwd when that lands inside
    the repo, else relative to the repo root (as with `-p`)."""
    path = Path(raw)
    for base in ((cwd, cfg.repo_root) if not path.is_absolute() else (cwd,)):
        abs_path = Path(os.path.normpath(path if path.is_absolute() else base / path))
        try:
            return abs_path.relative_to(cfg.repo_root).as_posix()
        except ValueError:
            continue
    raise CookbookError(f"{raw}: not inside the repo {cfg.repo_root}")


def _split_targets(ctx, index, targets: list[str]) -> tuple[list[str], list]:
    """(repo-relative paths, index entries) for the positional arguments. An
    existing path, or anything with a `/`, is a path; else a UUID or rdid in the
    index is an id; else a UUID-shaped argument is an error; else a planned path."""
    cfg = ctx.config
    paths, entries = [], []
    for t in targets:
        if "/" not in t and not (ctx.cwd / t).exists() and not (cfg.repo_root / t).exists():
            entry = index.get(t.lower() if is_uuid(t) else t)
            if entry is not None:
                if entry.kind in ("recipe", "ingredient"):
                    entries.append(entry)
                else:
                    ctx.ui.warn(escape(f"{entry.rdid} is a {entry.kind}; scope walks only "
                                       "recipes and ingredients"))
                continue
            if is_uuid(t):
                raise CookbookError(f"{t!r} matches no artifact in {cfg.identity.rdid}")
        rel = _rel(cfg, ctx.cwd, t)
        if cfg.root_for(rel) is None and not index.owners(rel):
            ctx.ui.warn(escape(f"{t}: not under any code root (or an unknown id)"))
        paths.append(rel)
    return paths, entries


def _changes(args, ctx, paths: list[str]) -> list:
    cfg = ctx.config
    if paths:
        return git_changes.planned(paths, cfg.repo_root)
    ref = args.since or base_ref(cfg.repo_root)
    if ref:
        return git_changes.branch(cfg.repo_root, ref)
    ctx.ui.warn("no base branch found (origin/main, main); scoping the uncommitted changes "
                "(against HEAD, else staged) and untracked files only")
    return git_changes.uncommitted(cfg.repo_root)


def _print(ctx, scope: Scope) -> None:
    for title, items in (("minimum", scope.minimum), ("further", scope.further),
                         ("siblings", scope.siblings)):
        ctx.ui.section(title)
        if not items:
            ctx.ui.info("  (none)")
        for i in items:
            via = f" via {i.via}" if i.via else ""
            ctx.ui.info(escape(f"  {i.rdid}  {i.state}{via}"))
    ctx.ui.section("uncovered")
    if not scope.uncovered:
        ctx.ui.info("  (none)")
    for p in scope.uncovered:
        ctx.ui.info(escape(f"  {p}"))


def run(args, ctx) -> int:
    if not require_config(ctx):
        return 2
    cfg = ctx.config
    index = current_index(cfg.cookbook_dir)
    paths, entries = _split_targets(ctx, index, args.targets)
    try:
        found = [] if args.targets and not paths else _changes(args, ctx, paths)
    except GitError as e:
        ctx.ui.error(escape(f"git failed, so the change set is unknown: {e}"))
        return 1
    scope = compute(cfg, index, resolver_for(cfg, index), found, entries)
    if args.json:
        sys.stdout.write(json.dumps(asdict(scope), indent=2) + "\n")
    else:
        _print(ctx, scope)
    return 0
