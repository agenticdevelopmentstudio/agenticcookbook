"""`cookr update` — fill missing frontmatter, sync `index.json`, and regenerate indexes.

Frontmatter is filled in every artifact source folder's manifest, and in any
single-file doc with no folder. The cookbook index (`index.json`) is brought in
line with the folders (`index.sync_from_folders`) when the root holds a
format-2 `cookbook.json`.

Fully deterministic. No LLM. Run repeatedly without side effects beyond what
the filesystem requires.
"""

from __future__ import annotations

import getpass
from datetime import date
from pathlib import Path

from ..core.artifact import (
    ARTIFACT_FILE, doc_path, dump_manifest, edit_text, find_folders, folder_for, is_folder,
    load_folder, save_document,
)
from ..core import refs
from ..core.errors import CookbookError, NoCookbookRootError
from ..core.frontmatter import Frontmatter, dump, fill_defaults, parse
from ..core.identity import MANIFEST, IdentityError, read_manifest
from ..core.index import (
    INDEX_FILE, Index, current_index, load_index, save_index, sync_from_folders,
)
from ..core.linkedit import edit_links
from ..core.links import Resolver, is_authored_link, to_stored, to_stored_text
from ..core.markdown import iter_markdown
from ..core.repoconfig import config_for_cookbook
from ..indexing import engine

NAME = "update"
HELP = "Fill missing frontmatter and regenerate indexes (deterministic; no LLM)."


def register(parser) -> None:
    parser.add_argument(
        "--author",
        default="",
        help="Author name to use when filling missing frontmatter.",
    )
    parser.add_argument(
        "--no-frontmatter",
        action="store_true",
        help="Skip frontmatter fill step; only regenerate indexes.",
    )
    parser.add_argument(
        "--no-indexes",
        action="store_true",
        help="Skip index regeneration; only fill frontmatter.",
    )


def _fill_frontmatter(root: Path, author: str, ui) -> tuple[int, int]:
    """Returns (files_touched, fields_added_total)."""
    files_touched = 0
    fields_added_total = 0
    today = date.today()

    for folder in find_folders([root]):
        rel = folder.relative_to(root)
        doc = doc_path(folder)
        if doc.is_file():
            # A doc compiled beside its folder: edit through it so both stay in step.
            new_fm, added = fill_defaults(parse(edit_text(doc)), rel_path=rel.with_suffix(".md"),
                                          author=author, today=today)
            if added:
                save_document(doc, dump(new_fm))
        else:
            art = load_folder(folder)
            fm = Frontmatter(data=art.meta, body=art.body(), had_frontmatter=True)
            _, added = fill_defaults(fm, rel_path=rel.with_suffix(".md"), author=author, today=today)
            if added:
                (folder / ARTIFACT_FILE).write_text(dump_manifest(art), encoding="utf-8")
        if added:
            files_touched += 1
            fields_added_total += len(added)
            ui.skip(f"{rel}/  +{','.join(added)}")

    for md in iter_markdown(root):
        if is_folder(folder_for(md)):
            continue  # its folder is the source, filled above
        fm = parse(edit_text(md))
        rel = md.relative_to(root)
        new_fm, added = fill_defaults(fm, rel_path=rel, author=author, today=today)
        if added:
            save_document(md, dump(new_fm))
            files_touched += 1
            fields_added_total += len(added)
            ui.skip(f"{rel}  +{','.join(added)}")
    return files_touched, fields_added_total


def _store_links(root: Path, ctx) -> int:
    """Rewrite every link authored as an rdid to its UUID form, resolving against
    the index as the folders stand. A link that cannot be resolved is left as
    written and reported; returns 1 for any such link or failure."""
    if not (root / MANIFEST).is_file():
        return 0
    try:
        index = current_index(root)
        config = ctx.config
        if config is None or config.cookbook_dir.resolve() != root.resolve():
            config = config_for_cookbook(root)
        resolver = Resolver(config.repo_root, index, config.dependencies)
        problems: list[str] = []

        def value(v: str) -> str:
            if not is_authored_link(v):
                return v
            try:
                return to_stored(v, resolver)
            except CookbookError as e:
                problems.append(str(e))
                return v

        changed = edit_links(root, value, lambda t: to_stored_text(t, resolver, problems))
    except (CookbookError, ValueError) as e:
        ctx.ui.error(f"links not stored: {e}")
        return 1
    for folder in changed:
        ctx.ui.skip(f"{folder.relative_to(root)}/  links stored as UUIDs")
    for problem in sorted(set(problems)):
        ctx.ui.error(f"link not stored: {problem}")
    return 1 if problems else 0


def _sync_index(root: Path, ui) -> None:
    """Bring `index.json` in line with the folders; a root without a format-2
    manifest has no index to keep."""
    if not (root / MANIFEST).is_file():
        return
    try:
        index = (load_index(root) if (root / INDEX_FILE).is_file()
                 else Index(cookbook=read_manifest(root)))
    except IdentityError as e:
        ui.warn(f"index.json not synced: {e}")
        return
    changes = sync_from_folders(index, root)
    if changes or not (root / INDEX_FILE).is_file():
        save_index(index, root)
    for line in changes:
        ui.skip(line)
    ui.ok(f"index.json: {len(changes)} change(s)")


def run(args, ctx) -> int:
    if ctx.cookbook_root is None:
        raise NoCookbookRootError(
            "Could not find a cookbook root. Run from inside a cookbook dir, or pass -p."
        )
    root = ctx.cookbook_root
    ctx.ui.title(f"cookr update · {root}")
    status = 0

    if not args.no_frontmatter:
        ctx.ui.section("Frontmatter")
        author = args.author or getpass.getuser()
        files_touched, fields_added = _fill_frontmatter(root, author, ctx.ui)
        if files_touched:
            ctx.ui.ok(f"{files_touched} files updated · {fields_added} fields added")
        else:
            ctx.ui.info("All artifacts already have complete frontmatter.")
        _sync_index(root, ctx.ui)

    status = _store_links(root, ctx)

    if not args.no_indexes:
        ctx.ui.section("Indexes")
        configs_dir = refs.embedded(ctx.references_dir, "index-configs")
        results = engine.run_all(configs_dir, root)
        if not results:
            ctx.ui.warn(f"No index configs found in {configs_dir}.")
        else:
            rows = []
            for r in results:
                detail = r.output if r.output else r.reason
                rows.append([r.name, r.strategy, r.status, detail])
            ctx.ui.table(["config", "strategy", "status", "detail"], rows)

    ctx.ui.blank()
    ctx.ui.ok("Done.")
    return status
