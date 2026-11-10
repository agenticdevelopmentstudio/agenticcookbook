"""Bump an artifact's version and add its Change History row, in memory.

`plan` returns the bumped text of one file (raising BumpError when it cannot be
bumped); `cookr bump` (modules/bump.py) writes the plans. The frontmatter is
edited in place (never re-dumped), so key order and quoting survive.

`plan_against_base` is what `cookr bump` calls: it computes the new version from
the version the branch started from, proposes the level from what changed, and
returns the freeze of the base version into the folder's `versions/`.
"""

from __future__ import annotations

import re
import subprocess
from dataclasses import dataclass, replace
from pathlib import Path

from . import history, versions
from .artifact import ArtifactError, authored_text, edit_text, folder_for, is_folder
from .errors import CookbookError

LEVELS = ("patch", "minor", "major")


class BumpError(CookbookError):
    """One file cannot be bumped."""


def bumped(version: history.Version, level: str) -> history.Version:
    major, minor, patch = version
    if level == "major":
        return (major + 1, 0, 0)
    if level == "minor":
        return (major, minor + 1, 0)
    return (major, minor, patch + 1)


def level_of(old: history.Version, new: history.Version) -> str:
    """How far `new` is past `old`: `patch`, `minor` or `major`."""
    if new[0] != old[0]:
        return "major"
    return "minor" if new[1] != old[1] else "patch"


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
    where: str   # "top" | "bottom" | "replaced" | "no-op"
    text: str    # the whole new file
    noop: bool = False
    note: str = ""
    warning: str = ""


@dataclass(frozen=True)
class Freeze:
    """The base version's files, to keep in `folder/versions/<version>/`."""
    folder: Path
    version: str
    files: dict


def _read(path: Path) -> str:
    try:
        return edit_text(path)
    except OSError as e:
        raise BumpError(f"cannot read: {e.strerror or e}") from e
    except ArtifactError as e:
        raise BumpError(str(e)) from e


def plan(path: Path, *, level: str, summary: str, author: str, day: str,
         base_version: history.Version | None = None, text: str | None = None) -> Plan:
    """The bumped text of `path`, or BumpError saying why it cannot be bumped.

    With `base_version` (the version the branch started from) the new version is
    that plus `level`. When the branch already bumped past it, a same-or-lower
    level changes nothing and a higher one re-levels: the newest row is replaced
    and `version` re-set."""
    if text is None:
        text = _read(path)
    lines = history.split_lines(text)
    end = _frontmatter_end(lines)
    version_at = _find_key(lines, end, "version")
    modified_at = _find_key(lines, end, "modified")
    old = version_at[1]["value"].strip()
    current = history.parse_version(old)
    if current is None:
        raise BumpError(f"`version: {old}` is not X.Y.Z")
    start = base_version or current
    if current < start:
        raise BumpError(f"`version: {old}` is below the base version "
                        f"{history.format_version(start)}; fix `version` first")
    new = bumped(start, level)

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
    cells = (history.format_version(new), day, author, summary)
    if current > start:   # the branch already bumped
        if LEVELS.index(level) <= LEVELS.index(level_of(start, current)):
            return Plan(path, old, old, "no-op", text, noop=True, note=f"already bumped to {old}")
        if newest is None or newest.version != current:
            raise BumpError(f"the newest Change History row is not {old}; fix it before re-levelling")
        try:
            lines = history.split_lines(history.replace_newest_row(table, new, cells))
        except history.HistoryError as e:
            raise BumpError(str(e)) from e
        where = "replaced"
    else:
        try:
            added, where = history.add_row(table, new, cells)
        except history.HistoryError as e:
            raise BumpError(str(e)) from e
        lines = history.split_lines(added)
    _set(lines, version_at, history.format_version(new))
    _set(lines, modified_at, day)
    return Plan(path, old, history.format_version(new), where, "".join(lines))


def plan_against_base(path: Path, *, level: str | None, summary: str, author: str,
                      day: str) -> tuple[Plan, Freeze | None]:
    """`plan`, with the version computed from the branch's base and the level
    proposed from what changed since it when `level` is None. Also the freeze of
    the base version, when the artifact existed at base and its folder differs.
    An artifact the base never had bumps from its current version (patch by
    default) and freezes nothing."""
    text = _read(path)
    folder = folder_for(path)
    try:
        root = versions.repo_root(path.parent)
        ref = versions.base_ref(root)
        base = versions.base_text(root, folder, ref) if ref else None
    except versions.GitError as e:
        raise BumpError(f"git failed, so the base version is unknown: {e}") from e
    except ArtifactError as e:
        raise BumpError(f"cannot read the base version: {e}") from e
    if not ref:   # no base branch: say so, never fall back silently
        fallback = plan(path, level=level or "patch", summary=summary, author=author, day=day,
                        text=text)
        warning = (f"no base branch found (origin/main, main); bumping from current version "
                   f"{fallback.old}, level {level or 'patch'}, nothing frozen")
        return replace(fallback, warning=warning), None
    if base is None:   # the base never had this artifact: a new one
        return plan(path, level=level or "patch", summary=summary, author=author, day=day,
                    text=text), None
    base_v = history.parse_version(versions.version_of(base))
    if base_v is None:
        raise BumpError(f"the base version {versions.version_of(base)!r} is not X.Y.Z")
    try:
        changed = versions.content_changed(base, text)
        proposed = versions.propose_level(
            versions.diff(authored_text(base), authored_text(text)), changed)
    except ArtifactError as e:
        raise BumpError(str(e)) from e
    chosen = level or proposed
    if chosen == "none":
        current = versions.version_of(text)
        return Plan(path, current, current, "no-op", text, noop=True,
                    note="nothing changed since the base; nothing to bump"), None
    result = plan(path, level=chosen, summary=summary, author=author, day=day,
                  base_version=base_v, text=text)
    freeze = None
    if not result.noop and is_folder(folder):
        before = versions.base_files(root, folder, ref)
        if before is not None and before != versions.folder_files(folder):
            freeze = Freeze(folder, history.format_version(base_v), before)
    return result, freeze


def git_user(cwd: Path) -> str:
    try:
        proc = subprocess.run(["git", "-C", str(cwd), "config", "user.name"],
                              capture_output=True, text=True, check=False)
    except FileNotFoundError:
        return ""
    return proc.stdout.strip() if proc.returncode == 0 else ""
