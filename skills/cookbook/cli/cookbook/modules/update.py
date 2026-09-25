"""`cookbook update` — fill missing frontmatter and regenerate indexes.

Fully deterministic. No LLM. Run repeatedly without side effects beyond what
the filesystem requires.
"""

from __future__ import annotations

import functools
import getpass
from datetime import date
from pathlib import Path

from ..core import refs
from ..core.errors import NoCookbookRootError
from ..core.frontmatter import dump, fill_defaults, parse_file
from ..core.markdown import iter_markdown
from ..core.scheme import cookbook_scheme
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
    cookbook_name = root.name
    scheme = functools.cache(lambda: cookbook_scheme(root))  # only if a domain is missing

    for md in iter_markdown(root):
        fm = parse_file(md)
        rel = md.relative_to(root)
        new_fm, added = fill_defaults(
            fm, rel_path=rel, cookbook_name=cookbook_name, scheme=scheme, author=author, today=today,
        )
        if added:
            md.write_text(dump(new_fm), encoding="utf-8")
            files_touched += 1
            fields_added_total += len(added)
            ui.skip(f"{rel}  +{','.join(added)}")
    return files_touched, fields_added_total


def run(args, ctx) -> int:
    if ctx.cookbook_root is None:
        raise NoCookbookRootError(
            "Could not find a cookbook root. Run from inside a cookbook dir, or pass -p."
        )
    root = ctx.cookbook_root
    ctx.ui.title(f"cookbook update · {root}")

    if not args.no_frontmatter:
        ctx.ui.section("Frontmatter")
        author = args.author or getpass.getuser()
        files_touched, fields_added = _fill_frontmatter(root, author, ctx.ui)
        if files_touched:
            ctx.ui.ok(f"{files_touched} files updated · {fields_added} fields added")
        else:
            ctx.ui.info("All artifacts already have complete frontmatter.")

    if not args.no_indexes:
        ctx.ui.section("Indexes")
        configs_dir = ctx.references_dir / "index-configs"
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
    return 0
