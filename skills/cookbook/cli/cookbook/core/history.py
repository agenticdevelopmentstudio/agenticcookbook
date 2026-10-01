"""The `## Change History` table: find it, read its rows, add one.

conventions.md ("Change History") ends every cookbook artifact with:

    ## Change History

    | Version | Date | Author | Summary |
    |---------|------|--------|---------|
    | 1.0.0 | YYYY-MM-DD | Name | Initial creation |

This module is the one parser for that table. `cookbook bump` adds rows with it,
and cookr's completeness checks read rows with it. It works on the text's own
lines and never re-renders the table, so adding a row changes no other byte.
Headings and tables inside fenced code blocks are skipped, so a document that
shows an example Change History in a fence (conventions.md does) reads correctly.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Sequence

HEADING = "Change History"
COLUMNS = ("Version", "Date", "Author", "Summary")

NEWEST_FIRST = "newest-first"
OLDEST_FIRST = "oldest-first"
UNORDERED = "unordered"
# A table with fewer than two rows shows no order of its own, and conventions.md
# names none, so it grows the way most tables in the cookbook and in the repos
# that use it already run: newest first.
DEFAULT_ORDER = NEWEST_FIRST

Version = tuple[int, int, int]
_VERSION = re.compile(r"^(\d+)\.(\d+)\.(\d+)$")

# CommonMark fences: three or more backticks or tildes, indented at most three
# spaces. A backtick fence's info string cannot hold a backtick; a fence closes on
# a line of the same character, at least as long, with nothing after it.
_FENCE = re.compile(r"^ {0,3}(`{3,}|~{3,})(.*)$")
# A level-1 or level-2 ATX heading, minus any closing `#` run.
_HEADING = re.compile(r"^ {0,3}(#{1,2})(?:[ \t]+(.*?))?(?:[ \t]+#+)?[ \t]*$")
_TABLE_LINE = re.compile(r"^ {0,3}\|")
_DELIMITER_CELL = re.compile(r"^:?-+:?$")
_LINES = re.compile(r"[^\n]*\n|[^\n]+\Z")


class HistoryError(ValueError):
    """The Change History section cannot be read, or cannot take the row asked for."""


def parse_version(text: str) -> Version | None:
    """`"1.2.3"` as `(1, 2, 3)`; None for anything that is not exactly X.Y.Z."""
    m = _VERSION.match(text.strip())
    return (int(m[1]), int(m[2]), int(m[3])) if m else None


def format_version(version: Version) -> str:
    return ".".join(str(part) for part in version)


def split_lines(text: str) -> list[str]:
    """`text` cut after each newline, endings kept: `"".join(split_lines(t)) == t`."""
    return _LINES.findall(text)


def _fence_open(line: str) -> str | None:
    m = _FENCE.match(line)
    if not m or (m.group(1)[0] == "`" and "`" in m.group(2)):
        return None
    return m.group(1)


def _fence_closes(line: str, run: str) -> bool:
    m = _FENCE.match(line)
    return bool(m) and m.group(1)[0] == run[0] and len(m.group(1)) >= len(run) \
        and not m.group(2).strip()


def unfenced(lines: Sequence[str], start: int = 0, end: int | None = None):
    """`(index, line)` for each line in `lines[start:end]`: the line without its
    ending when it is outside a fenced code block, None when it is inside one.

    Fence lines themselves yield None too, so a fenced block reads as a gap.
    """
    end = len(lines) if end is None else end
    fence: str | None = None
    for i in range(start, end):
        bare = lines[i].rstrip("\r\n")
        if fence is not None:
            if _fence_closes(bare, fence):
                fence = None
            yield i, None
            continue
        run = _fence_open(bare)
        if run is not None:
            fence = run
            yield i, None
            continue
        yield i, bare


_unfenced = unfenced  # the name before it was public


@dataclass(frozen=True)
class Section:
    """A `## ` heading outside any fence, and the lines it owns."""

    heading: str  # the heading's text
    start: int    # index of the heading line
    end: int      # one past its last line: the next `#`/`##` heading outside a fence, or the end


def h2_spans(lines: Sequence[str], start: int = 0) -> list[Section]:
    """Every `## ` section in `lines[start:]`, in order, indexed into `lines`.

    A section runs to the next `#` or `##` heading outside a fence; deeper
    headings stay inside it, and so does anything fenced, headings included.
    """
    out: list[Section] = []
    heading: str | None = None
    opened = 0
    for i, bare in unfenced(lines, start, len(lines)):
        m = _HEADING.match(bare) if bare is not None else None
        if m is None:
            continue
        if heading is not None:
            out.append(Section(heading, opened, i))
            heading = None
        if m.group(1) == "##":
            heading, opened = (m.group(2) or "").strip(), i
    if heading is not None:
        out.append(Section(heading, opened, len(lines)))
    return out


def h2_sections(text: str) -> list[tuple[str, str]]:
    """`(heading, body)` for each `## ` heading outside a fenced code block, in order."""
    lines = split_lines(text)
    return [(s.heading, "".join(lines[s.start + 1:s.end])) for s in h2_spans(lines)]


def split_row(line: str) -> list[str]:
    """The cells of a pipe-table row, stripped. An escaped pipe (`\\|`) stays in its cell."""
    s = line.rstrip("\r\n").strip()
    if s.startswith("|"):
        s = s[1:]
    cells: list[str] = []
    cell: list[str] = []
    ended_on_pipe = False
    i = 0
    while i < len(s):
        ch = s[i]
        if ch == "\\" and i + 1 < len(s):
            cell.append(s[i:i + 2])
            ended_on_pipe = False
            i += 2
            continue
        if ch == "|":
            cells.append("".join(cell).strip())
            cell = []
            ended_on_pipe = True
        else:
            cell.append(ch)
            ended_on_pipe = False
        i += 1
    if not ended_on_pipe:
        cells.append("".join(cell).strip())
    return cells


def format_row(cells: Sequence[str]) -> str:
    """A table row holding `cells`, each pipe escaped so it stays in its cell."""
    out = []
    for cell in cells:
        if "\n" in cell or "\r" in cell:
            raise HistoryError(f"a table cell cannot span lines: {cell!r}")
        out.append(re.sub(r"(?<!\\)\|", r"\\|", cell.strip()))
    return "| " + " | ".join(out) + " |"


@dataclass(frozen=True)
class Row:
    """One data row of the table."""

    line: int                # index of the row's line
    cells: tuple[str, ...]   # its cells, stripped, escapes as written

    def cell(self, column: str) -> str:
        """The row's cell under `column` (one of COLUMNS); `""` when the row is short."""
        i = COLUMNS.index(column)
        return self.cells[i] if i < len(self.cells) else ""

    @property
    def version(self) -> Version | None:
        return parse_version(self.cell("Version"))


@dataclass(frozen=True)
class History:
    """A text's Change History section and the one table it holds."""

    lines: tuple[str, ...]   # every line of the text, endings kept
    section: Section
    header: int | None       # index of the table's header row; None when the section holds no table
    rows: tuple[Row, ...]    # the table's data rows, top to bottom

    @property
    def order(self) -> str | None:
        """NEWEST_FIRST or OLDEST_FIRST when versions strictly fall or rise down the
        table, UNORDERED otherwise (a repeated or unreadable version included), and
        None with fewer than two rows."""
        if len(self.rows) < 2:
            return None
        versions = [row.version for row in self.rows]
        if None in versions:
            return UNORDERED
        pairs = list(zip(versions, versions[1:]))
        if all(a > b for a, b in pairs):
            return NEWEST_FIRST
        if all(a < b for a, b in pairs):
            return OLDEST_FIRST
        return UNORDERED

    @property
    def newest(self) -> Row | None:
        """The row with the highest version, or None when no row has a readable one."""
        readable = [row for row in self.rows if row.version is not None]
        return max(readable, key=lambda row: row.version, default=None)


def read(text: str, *, start: int = 0) -> History:
    """The Change History of `text`, looking only from line index `start` on.

    Pass the index of the first line after the frontmatter so YAML never reads as
    Markdown. Raises HistoryError when there is no `## Change History` heading,
    more than one, or the section's table has a wrong header, no delimiter row, or
    is split (a blank line, text, or a fence between its rows).
    """
    lines = split_lines(text)
    found = [s for s in h2_spans(lines, start) if s.heading == HEADING]
    if not found:
        raise HistoryError(f"no `## {HEADING}` section")
    if len(found) > 1:
        where = ", ".join(str(s.start + 1) for s in found)
        raise HistoryError(f"{len(found)} `## {HEADING}` sections (lines {where}); expected one")
    section = found[0]

    runs: list[list[int]] = []
    previous = -2
    for i, bare in unfenced(lines, section.start + 1, section.end):
        if bare is None or not _TABLE_LINE.match(bare):
            continue
        if i == previous + 1:
            runs[-1].append(i)
        else:
            runs.append([i])
        previous = i
    if not runs:
        return History(tuple(lines), section, None, ())
    if len(runs) > 1:
        raise HistoryError(
            f"the table is split: line {runs[1][0] + 1} continues it after a gap "
            f"at line {runs[0][-1] + 2}; keep every row in one block"
        )

    table = runs[0]
    header = split_row(lines[table[0]])
    if tuple(header) != COLUMNS:
        raise HistoryError(
            f"line {table[0] + 1}: the table header is `| {' | '.join(header)} |`; "
            f"expected `| {' | '.join(COLUMNS)} |`"
        )
    if len(table) < 2 or not _is_delimiter(lines[table[1]], len(header)):
        raise HistoryError(
            f"line {table[0] + 2}: expected the delimiter row "
            f"(`|---|---|---|---|`) under the table header"
        )
    rows = tuple(Row(i, tuple(split_row(lines[i]))) for i in table[2:])
    return History(tuple(lines), section, table[0], rows)


def _is_delimiter(line: str, width: int) -> bool:
    cells = split_row(line)
    return len(cells) == width and all(_DELIMITER_CELL.match(cell) for cell in cells)


def add_row(history: History, version: Version, cells: Sequence[str]) -> tuple[str, str]:
    """The text with a row for `version` added at the table's newest end.

    Returns `(text, "top" | "bottom")`. A newest-first table takes the row under
    its delimiter, an oldest-first table after its last row, and a table with
    fewer than two rows follows DEFAULT_ORDER. Every other line keeps its bytes;
    the row takes the line ending of the line it follows. Raises HistoryError when
    the section holds no table, a row's version is not X.Y.Z, the rows are not in
    one version order, a row for `version` already exists, or `version` is not
    newer than every row.
    """
    if history.header is None:
        raise HistoryError(
            f"`## {HEADING}` holds no table; add its header and delimiter rows first: "
            f"`| {' | '.join(COLUMNS)} |` then `|---|---|---|---|`"
        )
    bad = [row for row in history.rows if row.version is None]
    if bad:
        raise HistoryError(
            f"line {bad[0].line + 1}: version `{bad[0].cell('Version')}` is not X.Y.Z"
        )
    if any(row.version == version for row in history.rows):
        raise HistoryError(f"the table already has a row for {format_version(version)}")
    order = history.order or DEFAULT_ORDER
    if order == UNORDERED:
        listed = ", ".join(row.cell("Version") for row in history.rows)
        raise HistoryError(
            f"the rows are not in one version order ({listed}); sort them "
            f"newest-first or oldest-first before adding a row"
        )
    newest = history.newest
    if newest is not None and newest.version > version:
        raise HistoryError(
            f"{format_version(version)} is older than the newest row, {newest.cell('Version')}"
        )

    if order == NEWEST_FIRST or not history.rows:
        at = history.header + 2
    else:
        at = history.rows[-1].line + 1
    lines = list(history.lines)
    before = lines[at - 1]
    ending = before[len(before.rstrip("\r\n")):] or _ending(lines)
    row = format_row(cells)
    if before.endswith("\n"):
        lines.insert(at, row + ending)
    else:
        # The row goes after the file's last line, which has no newline: give that
        # line one and leave the new last line without, as the file was.
        lines[at - 1] = before + ending
        lines.insert(at, row)
    return "".join(lines), ("top" if order == NEWEST_FIRST else "bottom")


def _ending(lines: Sequence[str]) -> str:
    for line in lines:
        if line.endswith("\n"):
            return "\r\n" if line.endswith("\r\n") else "\n"
    return "\n"
