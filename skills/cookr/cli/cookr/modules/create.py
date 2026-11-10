"""`cookr create` — scaffold a format-2 cookbook.

Creates `cookbook/cookbook.json` (a new UUID and the given `--rdid`) and an empty
`cookbook/index.json`. Nothing else: artifacts and their folders come with `add`.

Idempotent: the same `--rdid` on a format-2 cookbook changes nothing (exit 0); a
different rdid is refused (exit 1), and so is a format-1 cookbook, which
`cookr upgrade` converts.
"""

from __future__ import annotations

import json
import uuid
from pathlib import Path

from rich.markup import escape

from ..core.errors import CookbookError
from ..core.identity import (MANIFEST, CookbookIdentity, IdentityError, is_cookbook_rdid,
                             read_manifest, write_manifest)
from ..core.index import INDEX_FILE, Index, save_index

NAME = "create"
HELP = "Scaffold a new format-2 cookbook (cookbook/cookbook.json and an empty index.json)."
CREATES_REPO = True  # -p names the repo to create a cookbook in; it need hold none yet


class CreateRefused(CookbookError):
    """The cookbook already exists in a way create will not touch."""


def register(parser) -> None:
    parser.add_argument("--rdid", required=True,
                        help="The cookbook's rdid, e.g. `adkitchen` (lowercase, digits, hyphens).")
    parser.add_argument(
        "--in",
        dest="target",
        type=Path,
        default=None,
        help="Parent dir to create the cookbook in (defaults to -p, else cwd).",
    )


def create_cookbook(parent: Path, rdid: str) -> tuple[CookbookIdentity, bool]:
    """Make `<parent>/cookbook` a format-2 cookbook. Returns (identity, created)."""
    if not is_cookbook_rdid(rdid):
        raise CreateRefused(f"{rdid!r} is not a valid cookbook rdid "
                            "(lowercase letters, digits and hyphens, starting with a letter)")
    root = Path(parent) / "cookbook"
    manifest = root / MANIFEST
    if manifest.is_file():
        try:
            fmt = json.loads(manifest.read_text(encoding="utf-8")).get("format")
        except (OSError, json.JSONDecodeError, AttributeError):
            fmt = None
        if fmt != 2:
            raise CreateRefused(f"{manifest} is not a format 2 cookbook; "
                                "convert it with `cookr upgrade`")
        try:
            existing = read_manifest(root)
        except IdentityError as e:
            raise CreateRefused(str(e)) from e
        if existing.rdid != rdid:
            raise CreateRefused(f"{root} is already the cookbook `{existing.rdid}`; "
                                f"refusing to re-create it as `{rdid}`")
        if not (root / INDEX_FILE).is_file():
            save_index(Index(cookbook=existing), root)
        return existing, False
    if root.exists() and any(root.iterdir()):
        raise CreateRefused(f"{root} exists without a cookbook.json (a format-1 cookbook?); "
                            "convert it with `cookr upgrade`")
    root.mkdir(parents=True, exist_ok=True)
    identity = CookbookIdentity(id=str(uuid.uuid4()), rdid=rdid)
    write_manifest(root, identity)
    save_index(Index(cookbook=identity), root)
    return identity, True


def run(args, ctx) -> int:
    parent = (args.target or ctx.cwd).resolve()
    parent.mkdir(parents=True, exist_ok=True)
    ctx.ui.title("cookr create")
    try:
        identity, created = create_cookbook(parent, args.rdid)
    except CookbookError as e:
        ctx.ui.error(escape(str(e)))
        return 1
    root = parent / "cookbook"
    if created:
        ctx.ui.ok(escape(f"created {root} ({identity.rdid}, {identity.id})"))
    else:
        ctx.ui.skip(escape(f"{root} already is the cookbook `{identity.rdid}`"))
    return 0
