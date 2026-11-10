"""`cookr bump` — bump an artifact's version and record it in Change History.

For each file: raise frontmatter `version`, set `modified`, and add one Change
History row (version, date, author, summary) at the table's newest end: the top of
a newest-first table, the bottom of an oldest-first one. A table with fewer than
two rows grows newest-first (core/history.DEFAULT_ORDER).

One bump per change. The new version is computed from the version the branch
started from (its merge base with main), and the level is proposed from what
changed since: an added named requirement is `minor`, a changed or removed one
`major`, other edits `patch`; `--level` overrides. Bumping again on the same
branch changes nothing at the same or a lower level and re-levels the row at a
higher one. The base version is frozen byte for byte into the folder's
`versions/<X.Y.Z>/`, so `cookr diff` can compare it later. An artifact the base
lacks bumps from its current version and freezes nothing.

Only the `version` and `modified` lines and the new row change; the frontmatter
is edited in place (never re-dumped), so key order and quoting survive. A file
compiled from a source folder (or the folder itself) is bumped in the folder,
and its doc recompiled only if one is there (core/artifact.save_document): a
folder-only checkout stays folder-only.

All or nothing: if any file cannot be bumped — rows not in one version order, a
row for the new version already there, no `version`/`modified` line, a
`versions/` directory already holding other bytes — every problem is reported
with its file, nothing is written, and the exit is non-zero.
"""

from __future__ import annotations

from datetime import date
from pathlib import Path

from rich.markup import escape

from ..core.artifact import doc_path, is_folder, save_document
from ..core.bumping import LEVELS, BumpError, Freeze, Plan, git_user, plan_against_base
from ..core.errors import CookbookError
from ..core.versions import conflict, freeze

NAME = "bump"
HELP = "Bump version, set modified and add a Change History row (deterministic; no LLM)."


def register(parser) -> None:
    parser.add_argument("files", nargs="+", type=Path, metavar="FILE",
                        help="Recipe, ingredient or other artifact markdown files.")
    parser.add_argument("--summary", required=True,
                        help="The Change History row's summary of what changed.")
    parser.add_argument("--level", choices=LEVELS, default=None,
                        help="Which semver part to raise (default: proposed from the "
                             "requirements changed since the branch's base; patch for "
                             "an artifact the base lacks).")
    parser.add_argument("--author", default=None,
                        help="The row's author (default: `git config user.name`).")
    parser.add_argument("--date", default=None, metavar="YYYY-MM-DD",
                        help="The row's date and the new `modified` (default: today).")
    parser.add_argument("--dry-run", action="store_true",
                        help="Print the planned change; write nothing.")


def run(args, ctx) -> int:
    summary = args.summary.strip()
    if not summary:
        raise CookbookError("--summary must not be empty")
    try:
        day = date.fromisoformat(args.date).isoformat() if args.date else date.today().isoformat()
    except ValueError as e:
        raise CookbookError(f"--date {args.date!r} is not YYYY-MM-DD") from e
    author = (args.author or "").strip() or git_user(ctx.cwd)
    if not author:
        raise CookbookError("no author: pass --author, or set `git config user.name`")

    plans: list[Plan] = []
    freezes: list[Freeze] = []
    failures: list[list[str]] = []
    for f in args.files:
        path = f if f.is_absolute() else ctx.cwd / f
        if is_folder(path):
            path = doc_path(path)
        try:
            planned, frozen = plan_against_base(path, level=args.level, summary=summary,
                                                author=author, day=day)
        except BumpError as e:
            failures.append([str(f), str(e)])
            continue
        plans.append(planned)
        if frozen is not None:
            freezes.append(frozen)

    if failures:
        ctx.ui.table(["file", "cannot bump"], failures)
        ctx.ui.error(f"{len(failures)} of {len(args.files)} file(s) cannot be bumped; "
                     "nothing was written.")
        return 1
    refused = [[str(z.folder), why] for z in freezes if (why := conflict(z.folder, z.version, z.files))]
    if refused:
        ctx.ui.table(["folder", "cannot freeze"], refused)
        ctx.ui.error(f"{len(refused)} version(s) cannot be frozen; nothing was written.")
        return 1

    rows = [[str(p.path), p.note or f"{p.old} → {p.new}", day, p.where] for p in plans]
    for p in plans:
        if p.warning:
            ctx.ui.warn(escape(p.warning))
    ctx.ui.table(["file", "version", "modified", "row"], rows)
    if args.dry_run:
        ctx.ui.info("Dry run: nothing was written.")
        return 0
    # Freezes go first: they are idempotent (identical bytes are a no-op), so a
    # failure before the documents are saved is fixed by running bump again.
    for z in freezes:
        freeze(z.folder, z.version, z.files)
    live = [p for p in plans if not p.noop]
    for p in live:
        save_document(p.path, p.text)
    ctx.ui.ok(f"Bumped {len(live)} file(s)." if live else "Nothing to bump.")
    return 0
