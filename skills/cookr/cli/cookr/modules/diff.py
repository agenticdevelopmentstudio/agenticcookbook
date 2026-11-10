"""`cookr diff` — the requirement-level difference between two versions.

`cookr diff <uuid|rdid> <from> [<to>]` prints the named requirements added,
changed and removed from `<from>` to `<to>` (default: the current version).
Versions are read from the artifact's `versions/` directory or its working copy.
"""

from __future__ import annotations

import argparse

from rich.markup import escape

from ..core.artifact import ArtifactError, is_folder
from ..core.errors import CookbookError
from ..core.identity import is_uuid
from ..core.index import INDEX_FILE, Index, load_index, sync_from_folders
from ..core.versions import (
    diff, folder_files, compose_files, frozen_versions, propose_level, requirements, version_of,
    version_text,
)
from .inventory import require_config

NAME = "diff"
HELP = "Print the requirements added, changed and removed between two versions of an artifact."


def register(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("value", metavar="UUID|RDID", help="The artifact to compare.")
    parser.add_argument("from_version", metavar="FROM", help="The older version (X.Y.Z).")
    parser.add_argument("to_version", metavar="TO", nargs="?", default=None,
                        help="The newer version (default: the current one).")


def run(args, ctx) -> int:
    if not require_config(ctx):
        return 2
    cfg = ctx.config
    cookbook = cfg.cookbook_dir
    index = (load_index(cookbook) if (cookbook / INDEX_FILE).is_file()
             else Index(cookbook=cfg.identity))
    sync_from_folders(index, cookbook)
    entry = index.get(args.value.lower() if is_uuid(args.value) else args.value)
    if entry is None:
        ctx.ui.error(escape(f"{args.value!r} matches no artifact in {cfg.identity.rdid}"))
        return 1
    folder = cookbook / entry.path
    files = folder_files(folder) if is_folder(folder) else None
    if files is None:
        raise CookbookError(f"{entry.rdid}: its source folder cannot be read")
    try:
        current = version_of(compose_files(files))
        known = sorted({*frozen_versions(folder), *([current] if current else [])},
                       key=lambda v: tuple(int(n) for n in v.split(".")))
        wanted = [args.from_version, args.to_version or current]
        texts = []
        for v in wanted:
            text = version_text(folder, v)
            if text is None:
                ctx.ui.error(escape(f"{entry.rdid} has no version {v!r}; it has "
                                    f"{', '.join(known) or 'none'}"))
                return 1
            texts.append(text)
    except ArtifactError as e:
        raise CookbookError(str(e)) from e

    old, new = texts
    d = diff(old, new)
    a, b = requirements(old), requirements(new)
    rows = ([["added", n, b[n]] for n in d.added]
            + [["changed", n, f"{a[n]}  ->  {b[n]}"] for n in d.changed]
            + [["removed", n, a[n]] for n in d.removed])
    ctx.ui.info(escape(f"{entry.rdid}: {wanted[0]} -> {wanted[1]}"))
    if not rows:
        ctx.ui.info("No requirement differs.")
        return 0
    ctx.ui.table(["change", "requirement", "text"], [[c, escape(n), escape(t)] for c, n, t in rows])
    ctx.ui.info(f"A change this size is a {propose_level(d, True)} bump.")
    return 0
