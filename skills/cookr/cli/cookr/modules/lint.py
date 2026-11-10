"""`cookr lint` — Phase A deterministic checks + Phase B claude -p quality pass."""

from __future__ import annotations

import subprocess
from pathlib import Path

from ..core import refs
from ..core.checks import phase_a, show
from ..core.errors import NoCookbookRootError
from ..core.artifact import ArtifactError, doc_path, find_folders, folder_for, is_folder
from ..core.artifact_build import compiled_text
from ..core.markdown import (ARTIFACT_FILE, SKIP_NAMES, in_source_folder, in_versions,
                             iter_markdown)
from ..core.shell import claude_available, claude_p, git_changed_files

NAME = "lint"
HELP = "Lint a cookbook: deterministic checks + LLM-driven recipe-quality pass."


def register(parser) -> None:
    parser.add_argument(
        "--no-llm",
        action="store_true",
        help="Skip the `claude -p` quality pass; run deterministic checks only.",
    )
    parser.add_argument(
        "--since",
        metavar="REF",
        default=None,
        help="Limit Phase B to markdown files changed since the given git ref (e.g. `--since main`).",
    )
    parser.add_argument(
        "files",
        nargs="*",
        type=Path,
        help="Limit the LLM pass to specific files (deterministic checks always cover the whole cookbook).",
    )


def _phase_a(root: Path, ui, config=None) -> int:
    ui.section("Phase A: deterministic checks")
    return show(phase_a(root, config), ui)


def _owner(p: Path, root: Path) -> Path | None:
    """The source folder holding `p`, the nearest artifact folder at or above it under root."""
    return next((d for d in (p, *p.parents) if (d == root or root in d.parents) and is_folder(d)),
                None)


def _unit_for(root: Path, p: Path) -> Path | None:
    """The unit Phase B reviews for a changed or named path: a source folder for
    its manifest, a part (even a deleted one), a host addition or its compiled
    doc; the file itself for a plain markdown doc; None for anything else."""
    if p.name == ARTIFACT_FILE:
        return p.parent if is_folder(p.parent) else None
    if is_folder(p):
        return p
    frozen = in_versions(p, root) if root in p.parents else in_versions(p)
    if p.suffix != ".md" or p.name in SKIP_NAMES or frozen:
        return None
    if is_folder(folder_for(p)):
        return folder_for(p)                      # a compiled doc: review its folder
    if not p.exists() or in_source_folder(p, root):
        return _owner(p.parent, root)             # a part or host addition, or a deleted one
    return p if p.is_file() else None


def _units(root: Path, paths: list[Path]) -> list[Path]:
    """Each path's review unit, once however many of its files are listed."""
    out: list[Path] = []
    for p in paths:
        unit = _unit_for(root, p)
        if unit is not None and unit not in out:
            out.append(unit)
    return out


def _resolve_phase_b_targets(
    root: Path, files: list[Path], since: str | None, ui
) -> list[Path] | None:
    """Return the review units for Phase B (source folders, composed in memory,
    and plain markdown files), or None on a fatal error."""
    if files and since:
        ui.error("Pass either explicit files or --since, not both.")
        return None
    if files:
        return [_unit_for(root, f.resolve()) or f for f in files]
    if since:
        try:
            changed = _units(root, git_changed_files(root, since, (".md", ".json"), deleted=True))
        except subprocess.CalledProcessError as e:
            ui.error(f"git diff failed: {e.stderr.strip() or e}")
            return None
        except FileNotFoundError:
            ui.error("`git` not found on PATH; cannot resolve --since.")
            return None
        ui.info(f"--since {since}: {len(changed)} changed artifact(s) or markdown file(s).")
        return changed
    return _units(root, [*find_folders([root]), *iter_markdown(root)])


def _review_text(root: Path, unit: Path) -> tuple[Path, str]:
    """(the label, the text) Phase B reviews for a unit. A source folder is
    composed in memory, as `cookr compile` would write it; nothing is written,
    so a fresh checkout with no compiled docs is reviewed in full."""
    if is_folder(unit):
        label = doc_path(unit)
        text = compiled_text(unit)[0]
    else:
        label, text = unit, unit.read_text(encoding="utf-8")
    return (label.relative_to(root) if root in label.parents else label), text


def _phase_b(root: Path, targets: list[Path], ui) -> int:
    if not claude_available():
        ui.warn("`claude` not found on PATH — skipping LLM pass.")
        return 0
    if not targets:
        ui.info("No files to review.")
        return 0

    ui.section("Phase B: LLM quality pass")
    template = refs.prompt_template("lint")

    principles_dir = refs.references_dir() / "principles"
    conventions_path = refs.references_dir() / "conventions.md"
    glossary_path = refs.references_dir() / "glossary.md"

    def safe_read(p: Path) -> str:
        return p.read_text(encoding="utf-8") if p.exists() else "(not bundled)"

    def list_principles() -> str:
        if not principles_dir.is_dir():
            return "(not bundled)"
        return "\n".join(f"- {p.name}" for p in sorted(principles_dir.glob("*.md")))

    failed = 0
    for f in targets:
        try:
            rel, content = _review_text(root, f if f.is_absolute() else root / f)
        except (OSError, ArtifactError) as e:
            failed += 1
            ui.error(f"cannot read {f}: {e}")
            continue
        prompt = (
            template
            .replace("{{principles}}", list_principles())
            .replace("{{conventions}}", safe_read(conventions_path))
            .replace("{{glossary}}", safe_read(glossary_path))
            .replace("{{file_path}}", str(rel))
            .replace("{{file_contents}}", content)
        )
        ui.info(f"Reviewing {rel}…")
        result = claude_p(prompt)
        if not result.ok:
            failed += 1
            ui.error(f"claude failed on {rel}: {result.stderr.strip()[:200]}")
            continue
        ui.blank()
        ui.console.print(f"[bold]{rel}[/bold]")
        ui.console.print(result.stdout.rstrip())
        ui.blank()
    return 1 if failed else 0


def run(args, ctx) -> int:
    if ctx.cookbook_root is None:
        raise NoCookbookRootError(
            "Could not find a cookbook root. Run from inside a cookbook dir, or pass -p."
        )
    root = ctx.cookbook_root.resolve()
    ctx.ui.title(f"cookr lint · {root}")

    exit_a = _phase_a(root, ctx.ui, ctx.config)
    exit_b = 0
    if not args.no_llm:
        targets = _resolve_phase_b_targets(root, list(args.files or []), args.since, ctx.ui)
        if targets is None:
            return 2
        exit_b = _phase_b(root, targets, ctx.ui)
    return exit_a or exit_b
