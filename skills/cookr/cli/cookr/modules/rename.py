"""`cookr rename` — give an artifact a new rdid.

The rdid is a name held in `index.json`; links store the UUID, so only the
index entry and the cached in-text labels change. No artifact is bumped.
"""

from __future__ import annotations

import argparse

from rich.markup import escape

from ..core.errors import CookbookError
from ..core.identity import is_rdid, is_uuid
from ..core.index import INDEX_FILE, Index, load_index, save_index, sync_from_folders
from ..core.linkedit import edit_links
from ..core.links import Link, relabel
from .inventory import require_config

NAME = "rename"
HELP = "Rename an artifact's rdid: one index entry, plus the in-text labels that show it."


def register(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("value", metavar="UUID|RDID", help="The artifact to rename.")
    parser.add_argument("new_rdid", metavar="NEW-RDID", help="Its new rdid.")


def run(args, ctx) -> int:
    if not require_config(ctx):
        return 2
    cfg = ctx.config
    cookbook = cfg.cookbook_dir
    if not is_rdid(args.new_rdid):
        raise CookbookError(f"{args.new_rdid!r} is not a valid rdid")
    index = (load_index(cookbook) if (cookbook / INDEX_FILE).is_file()
             else Index(cookbook=cfg.identity))
    sync_from_folders(index, cookbook)
    entry = index.get(args.value.lower() if is_uuid(args.value) else args.value)
    if entry is None:
        ctx.ui.error(escape(f"{args.value!r} matches no artifact in {cfg.identity.rdid}"))
        return 1
    other = next((e for e in index.entries.values()
                  if e.rdid == args.new_rdid and e.id != entry.id), None)
    if other is not None:
        ctx.ui.error(escape(f"rdid {args.new_rdid!r} already names {other.path}"))
        return 1
    old = entry.rdid
    entry.rdid = args.new_rdid
    labels = {Link(None, entry.id): args.new_rdid,
              Link(index.cookbook.id, entry.id): args.new_rdid}
    # Labels first: if this fails midway the index still has the old rdid, and a
    # rerun (idempotent when the rdid is already new) finishes the job.
    changed = edit_links(cookbook, lambda v: v, lambda t: relabel(t, labels))
    save_index(index, cookbook)
    ctx.ui.title(f"cookr rename · {escape(old)} → {escape(args.new_rdid)}")
    for folder in changed:
        ctx.ui.info(escape(f"  relabelled {folder.relative_to(cfg.repo_root).as_posix()}/"))
    ctx.ui.ok(f"{len(changed)} artifact(s) relabelled")
    return 0
