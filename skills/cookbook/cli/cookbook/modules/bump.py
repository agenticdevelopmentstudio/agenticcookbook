"""`cookbook bump` — bump an artifact's version and record it in Change History.

For each file: raise frontmatter `version` (patch by default), set `modified`,
and add one Change History row (version, date, author, summary) at the table's
newest end: the top of a newest-first table, the bottom of an oldest-first one.
A table with fewer than two rows grows newest-first (core/history.DEFAULT_ORDER).

Only the `version` and `modified` lines and the new row change; the frontmatter
is edited in place (never re-dumped), so key order and quoting survive.

All or nothing: if any file cannot be bumped — rows not in one version order, a
row for the new version already there, no `version`/`modified` line — every
problem is reported with its file, nothing is written, and the exit is non-zero.
"""

from __future__ import annotations

import re
import subprocess
from dataclasses import dataclass
from datetime import date
from pathlib import Path

from ..core import history
from ..core.errors import CookbookError

NAME = "bump"
HELP = "Bump version, set modified and add a Change History row (deterministic; no LLM)."

LEVELS = ("patch", "minor", "major")


def register(parser) -> None:
    parser.add_argument("files", nargs="+", type=Path, metavar="FILE",
                        help="Recipe, ingredient or other artifact markdown files.")
    parser.add_argument("--summary", required=True,
                        help="The Change History row's summary of what changed.")
    parser.add_argument("--level", choices=LEVELS, default="patch",
                        help="Which semver part to raise (default: patch).")
    parser.add_argument("--author", default=None,
                        help="The row's author (default: `git config user.name`).")
    parser.add_argument("--date", default=None, metavar="YYYY-MM-DD",
                        help="The row's date and the new `modified` (default: today).")
    parser.add_argument("--dry-run", action="store_true",
                        help="Print the planned change; write nothing.")


class BumpError(CookbookError):
    """One file cannot be bumped."""


def bumped(version: history.Version, level: str) -> history.Version:
    major, minor, patch = version
    if level == "major":
        return (major + 1, 0, 0)
    if level == "minor":
        return (major, minor + 1, 0)
    return (major, minor, patch + 1)


# A top-level frontmatter key line: `key: value`, `key: "value"` or `key: 'value'`,
# with an optional trailing comment.
def _key_line(key: str) -> re.Pattern:
    return re.compile(
        rf"^(?P<head>{re.escape(key)}:[ \t]*)"
        r"(?P<q>['\"]?)(?P<value>[^'\"#\r\n]*?)(?P=q)"
        r"(?P<tail>[ \t]*(?:#[^\r\n]*)?)(?P<end>\r?\n?)$"
    )


def _frontmatter_end(lines: list[str]) -> int:
    """Index of the frontmatter's closing `---` line."""
    if not lines or lines[0].rstrip("\r\n") != "---":
        raise BumpError("no YAML frontmatter (the file must start with `---`)")
    for i in range(1, len(lines)):
        if lines[i].rstrip("\r\n") == "---":
            return i
    raise BumpError("the frontmatter has no closing `---` line")


def _find_key(lines: list[str], end: int, key: str) -> tuple[int, re.Match]:
    pattern = _key_line(key)
    found = [(i, m) for i in range(1, end) if (m := pattern.match(lines[i]))]
    if not found:
        raise BumpError(f"the frontmatter has no plain `{key}:` line")
    if len(found) > 1:
        raise BumpError(f"the frontmatter has {len(found)} `{key}:` lines")
    return found[0]


def _set(lines: list[str], at: tuple[int, re.Match], value: str) -> None:
    i, m = at
    lines[i] = f"{m['head']}{m['q']}{value}{m['q']}{m['tail']}{m['end']}"


@dataclass(frozen=True)
class Plan:
    path: Path
    old: str
    new: str
    where: str   # "top" | "bottom"
    text: str    # the whole new file


def plan(path: Path, *, level: str, summary: str, author: str, day: str) -> Plan:
    """The bumped text of `path`, or BumpError saying why it cannot be bumped."""
    try:
        text = path.read_text(encoding="utf-8")
    except OSError as e:
        raise BumpError(f"cannot read: {e.strerror or e}") from e
    lines = history.split_lines(text)
    end = _frontmatter_end(lines)
    version_at = _find_key(lines, end, "version")
    modified_at = _find_key(lines, end, "modified")
    old = version_at[1]["value"].strip()
    current = history.parse_version(old)
    if current is None:
        raise BumpError(f"`version: {old}` is not X.Y.Z")
    new = bumped(current, level)

    try:
        table = history.read(text, start=end + 1)
    except history.HistoryError as e:
        raise BumpError(str(e)) from e
    newest = table.newest
    if newest is not None and newest.version is not None and newest.version > current:
        raise BumpError(
            f"the newest Change History row is {newest.cell('Version')}, "
            f"above `version: {old}`; fix `version` first"
        )
    try:
        added, where = history.add_row(
            table, new, (history.format_version(new), day, author, summary))
    except history.HistoryError as e:
        raise BumpError(str(e)) from e

    lines = history.split_lines(added)
    _set(lines, version_at, history.format_version(new))
    _set(lines, modified_at, day)
    return Plan(path, old, history.format_version(new), where, "".join(lines))


def _git_user(cwd: Path) -> str:
    try:
        proc = subprocess.run(["git", "-C", str(cwd), "config", "user.name"],
                              capture_output=True, text=True, check=False)
    except FileNotFoundError:
        return ""
    return proc.stdout.strip() if proc.returncode == 0 else ""


def run(args, ctx) -> int:
    summary = args.summary.strip()
    if not summary:
        raise CookbookError("--summary must not be empty")
    try:
        day = date.fromisoformat(args.date).isoformat() if args.date else date.today().isoformat()
    except ValueError as e:
        raise CookbookError(f"--date {args.date!r} is not YYYY-MM-DD") from e
    author = (args.author or "").strip() or _git_user(ctx.cwd)
    if not author:
        raise CookbookError("no author: pass --author, or set `git config user.name`")

    plans: list[Plan] = []
    failures: list[list[str]] = []
    for f in args.files:
        path = f if f.is_absolute() else ctx.cwd / f
        try:
            plans.append(plan(path, level=args.level, summary=summary, author=author, day=day))
        except BumpError as e:
            failures.append([str(f), str(e)])

    if failures:
        ctx.ui.table(["file", "cannot bump"], failures)
        ctx.ui.error(f"{len(failures)} of {len(args.files)} file(s) cannot be bumped; "
                     "nothing was written.")
        return 1

    rows = [[str(p.path), f"{p.old} → {p.new}", day, p.where] for p in plans]
    ctx.ui.table(["file", "version", "modified", "row"], rows)
    if args.dry_run:
        ctx.ui.info("Dry run: nothing was written.")
        return 0
    for p in plans:
        p.path.write_text(p.text, encoding="utf-8", newline="")
    ctx.ui.ok(f"Bumped {len(plans)} file(s).")
    return 0
