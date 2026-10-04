"""`cookr create` — scaffold a client cookbook in cwd.

Creates:
    cookbook/
        index.md          (empty)
        description.md    (placeholder)
        recipes/.gitkeep
        reference/.gitkeep

Idempotent: anything that already exists is skipped silently.
"""

from __future__ import annotations

from pathlib import Path

NAME = "create"
HELP = "Scaffold a new client cookbook (cookbook/, index.md, description.md, recipes/, reference/)."

DESCRIPTION_PLACEHOLDER = """# Cookbook Description

One-paragraph description of what this cookbook is for, who it's aimed at, and
how to use it. Replace this placeholder.
"""

SUBDIRS = ("recipes", "reference")


def register(parser) -> None:
    parser.add_argument(
        "--in",
        dest="target",
        type=Path,
        default=None,
        help="Parent dir to create the cookbook in (defaults to cwd).",
    )


def _create(path: Path, factory) -> bool:
    """Run `factory(path)` only if `path` is missing. Returns True iff created."""
    if path.exists():
        return False
    factory(path)
    return True


def run(args, ctx) -> int:
    parent = (args.target or ctx.cwd).resolve()
    parent.mkdir(parents=True, exist_ok=True)
    root = parent / "cookbook"

    ctx.ui.title("cookr create")

    actions: list[tuple[str, bool]] = []  # (label, created?)

    def mkdir(p: Path) -> None:
        p.mkdir(parents=True, exist_ok=True)

    actions.append(("cookbook/", _create(root, mkdir)))
    actions.append(("cookbook/index.md", _create(root / "index.md", lambda p: p.write_text("", encoding="utf-8"))))
    actions.append((
        "cookbook/description.md",
        _create(root / "description.md", lambda p: p.write_text(DESCRIPTION_PLACEHOLDER, encoding="utf-8")),
    ))
    for sub in SUBDIRS:
        sub_path = root / sub
        actions.append((f"cookbook/{sub}/", _create(sub_path, mkdir)))
        gk = sub_path / ".gitkeep"
        actions.append((f"cookbook/{sub}/.gitkeep", _create(gk, lambda p: p.write_text("", encoding="utf-8"))))

    ctx.ui.section("Result")
    rows = [[label, "created" if created else "skipped"] for label, created in actions]
    ctx.ui.table(["path", "status"], rows)
    ctx.ui.blank()
    created_count = sum(1 for _, c in actions if c)
    ctx.ui.ok(f"{created_count} created · {len(actions) - created_count} skipped")
    ctx.ui.info(f"Cookbook root: {root}")
    return 0
