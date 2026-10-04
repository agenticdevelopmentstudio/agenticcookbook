"""`cookr lint` — Phase A deterministic checks + Phase B claude -p quality pass."""

from __future__ import annotations

import subprocess
from pathlib import Path

from ..core import refs
from ..core.checks import fix_for, phase_a
from ..core.errors import NoCookbookRootError
from ..core.markdown import iter_markdown
from ..core.shell import claude_available, claude_p, git_changed_markdown

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


def _phase_a(root: Path, ui) -> int:
    ui.section("Phase A: deterministic checks")
    report = phase_a(root)
    if report.ok:
        ui.ok(f"All {report.files_checked} artifacts passed deterministic checks.")
        return 0
    rows = [[i.file, i.rule, i.detail, fix_for(i.rule)] for i in report.issues]
    ui.table(["file", "rule", "issue", "fix"], rows)
    ui.error(f"{len(report.issues)} issue(s) across {report.files_checked} files.")
    return 1


def _resolve_phase_b_targets(
    root: Path, files: list[Path], since: str | None, ui
) -> list[Path] | None:
    """Return the file list for Phase B, or None on a fatal error."""
    if files and since:
        ui.error("Pass either explicit files or --since, not both.")
        return None
    if files:
        return files
    if since:
        try:
            changed = git_changed_markdown(root, since)
        except subprocess.CalledProcessError as e:
            ui.error(f"git diff failed: {e.stderr.strip() or e}")
            return None
        except FileNotFoundError:
            ui.error("`git` not found on PATH; cannot resolve --since.")
            return None
        ui.info(f"--since {since}: {len(changed)} changed markdown file(s).")
        return changed
    return iter_markdown(root)


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
        rel = f.relative_to(root) if f.is_absolute() else f
        content = (root / f if not f.is_absolute() else f).read_text(encoding="utf-8")
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
    root = ctx.cookbook_root
    ctx.ui.title(f"cookr lint · {root}")

    exit_a = _phase_a(root, ctx.ui)
    exit_b = 0
    if not args.no_llm:
        targets = _resolve_phase_b_targets(root, list(args.files or []), args.since, ctx.ui)
        if targets is None:
            return 2
        exit_b = _phase_b(root, targets, ctx.ui)
    return exit_a or exit_b
