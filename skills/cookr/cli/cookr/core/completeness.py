"""The rules that separate a `partial` recipe from a `complete` one.

A recipe is complete when:
1. its status is `review` or `accepted`;
2. its body carries no `NEEDS REVIEW` marker outside the Change History
   section (a changelog row that says "removed the NEEDS REVIEW marker" is a
   record of the fix, not a gap);
3. its `type` is one of `templates.TYPES`;
4. every `## ` section of its type's template (`templates.required_sections`)
   is present with at least one non-blank body line before the next `##`
   heading, so a section added to a template is required at once;
5. its Platform Notes section has a WinUI 3 bullet with translation guidance:
   the bold label names `WinUI 3` (decoration such as `**WinUI 3** (Windows):`
   or `**WinUI 3 / C#**:` is tolerated), text follows it on the same line or
   an indented continuation line, and that text is not `Not applicable` —
   Platform Notes is translation guidance, never a gap;
6. every `NEEDS REVIEW` marker outside Change History is a named bullet with
   the whole phrase on one line, `- **name**: NEEDS REVIEW: Not implemented in
   source.`, and none sits in Compliance (the rationale there describes the gap
   in prose; the bullet it qualifies carries the marker);
7. no requirement name is prefixed with its RFC 2119 word (`**must-…**`);
8. it cites no source line numbers (`(line 42)`, `source lines 10-20`,
   `Store.swift:88`) — they go stale with the next edit;
9. every compliance check it cites exists in the catalog, when one is given;
10. its Compliance section cites every check each component meets
    (REQUIRED_CHECKS);
11. its Conformance Test Vectors table has at least MIN_VECTORS rows;
12. each Design Decision is the three bold lines `**Decision**:`,
    `**Rationale**:`, `**Approved**:`;
13. its frontmatter `platforms` are exactly the source platforms' identifiers,
    when the caller says which platforms its sources are on;
14. its Change History table is one block of rows with a version, date and
    author each, in one version order, the newest row's version is the
    frontmatter `version`, and frontmatter `modified` is not older than the
    newest row's date;
15. its frontmatter `domain` is exactly the one its path derives
    (`Config.domain`), when the caller says what that is — `cookbook validate`
    checks only the path suffix, so a wrong scheme or directory passes there.

Rules 6-15 are what writers got wrong repeatedly; a script can see each one,
so the grade says so instead of a reviewer re-deriving it, and a new writer
rule re-grades the corpus already written, not just the next recipe.

Sections are found fence-aware (cookbook.core.history), so a `#` comment or a
`## ` line inside a code sample never ends a section or starts one, and prose
checks (the WinUI bullet, line citations) skip fenced code.
"""

from __future__ import annotations

import datetime as _dt
import re
from collections.abc import Iterable, Iterator, Mapping
from typing import Optional

from cookbook.core import history

from . import templates
from .compliance import CITATION, unknown_citations
from .recipes import RecipeInfo

COMPLETE_STATUSES = ("review", "accepted")
NEEDS_REVIEW = "NEEDS REVIEW"
CHANGE_HISTORY = history.HEADING
# Every component meets these (extract/module.md, Compliance); `<document>#<check>`.
REQUIRED_CHECKS = ("best-practices#separation-of-concerns", "best-practices#unit-test-coverage")
MIN_VECTORS = 5
VECTORS_SECTION = "Conformance Test Vectors"
# The frontmatter `platforms` each source platform (a `.cookr.json` root's
# `platform`) writes, per extract/module.md. `apple` needs `swift` plus at least
# one of `macos`/`ios`. A source platform missing here leaves rule 13 ungraded.
PLATFORM_IDS: dict[str, tuple[frozenset[str], frozenset[str]]] = {
    # platform: (identifiers all required, identifiers of which at least one is required)
    "web": (frozenset({"typescript", "web"}), frozenset()),
    "apple": (frozenset({"swift"}), frozenset({"macos", "ios"})),
    "python": (frozenset({"python"}), frozenset()),
}


class _RequiredSections(Mapping):
    """`{type: sections}` read from the templates on first use of each type.

    Kept for callers that ask `rtype in REQUIRED_SECTIONS`; membership is
    templates.TYPES and never reads a file. New code calls templates directly.
    """

    def __getitem__(self, rtype: str) -> tuple[str, ...]:
        if rtype not in templates.TYPES:
            raise KeyError(rtype)
        return templates.required_sections(rtype)

    def __contains__(self, rtype: object) -> bool:
        return rtype in templates.TYPES

    def __iter__(self) -> Iterator[str]:
        return iter(templates.TYPES)

    def __len__(self) -> int:
        return len(templates.TYPES)


REQUIRED_SECTIONS: Mapping[str, tuple[str, ...]] = _RequiredSections()

_MARKER = re.compile(r"NEEDS\s+REVIEW")
_WINUI = re.compile(
    r"^-[ \t]+\*\*[^*\n]*WinUI 3[^*\n]*\*\*[ \t]*(?:\([^)\n]*\))?[ \t]*:?[ \t]*(.*)$"
)
_CONTINUATION = re.compile(r"^[ \t]+(?![-*+][ \t]|\d+[.)][ \t])(\S.*)$")
_NOT_APPLICABLE = re.compile(r"^not applicable\b", re.IGNORECASE)
_MARKER_BULLET = re.compile(r"^\s*- \*\*[^*\n]+\*\*: NEEDS REVIEW: Not implemented in source\.")
_RFC_NAME = re.compile(r"^\s*- \*\*(must|should|may)-", re.MULTILINE | re.IGNORECASE)

# Source line citations. A bare `line N` is how behavior is described too
# ("caret at line 1 of the new block"), so a citation needs a sign it points at
# source: a file name next to it, the word `source`, or, with no file name, a
# citing preposition, a line number past single digits and no `of` after it.
_SOURCE_EXT = (r"(?:swift|mm?|h|hpp|c|cc|cpp|kts?|java|cs|xaml|[cm]?jsx?|tsx?|vue|svelte"
               r"|py|go|rs|rb)")
_FILE_COLON_LINE = re.compile(rf"\.{_SOURCE_EXT}:\d+")  # literal-led: cheap to scan
_FILE_NAME = re.compile(rf"\w\.{_SOURCE_EXT}\b")
_LINE_WORD = re.compile(r"[Ll]ine(s?)[ \t]+(\d+)")
_NEAR = 40
_CITING_BEFORE = re.compile(r"(?:\b(?:at|on|see|in)[ \t]+|\()$", re.IGNORECASE)
_SOURCE_BEFORE = re.compile(r"\bsource[ \t]+$", re.IGNORECASE)
_OF_AFTER = re.compile(r"^[ \t]*[,;]?[ \t]*of\b", re.IGNORECASE)
_RANGE_AFTER = re.compile(r"^[ \t]*[-–][ \t]*\d+")
_TABLE_ROW = re.compile(r"^ {0,3}\|")
_DELIMITER_ROW = re.compile(r"^ {0,3}\|?[ \t]*:?-+:?[ \t]*(?:\|[ \t]*:?-+:?[ \t]*)*\|?[ \t]*$")
# The label may lead a list item (`1. **Decision**:`) or its indented continuation.
_DECISION_LINE = re.compile(
    r"^[ \t]*(?:(?:[-*+]|\d+[.)])[ \t]+)?\*\*(Decision|Rationale|Approved)(?::\*\*|\*\*:)")


def _split(body: str) -> tuple[dict[str, str], str]:
    """`(sections, graded body)` from one fence-aware pass over `body`.

    `sections` maps each `## Heading` outside a fence to its text up to the next
    `#`/`##` heading (a repeated heading keeps its first section); the graded
    body is `body` without its Change History section.
    """
    lines = history.split_lines(body)
    found: dict[str, str] = {}
    graded = body
    for span in history.h2_spans(lines):
        found.setdefault(span.heading, "".join(lines[span.start + 1:span.end]))
        if span.heading == CHANGE_HISTORY and graded is body:
            graded = "".join(lines[:span.start] + lines[span.end:])
    return found, graded


def sections(body: str) -> dict[str, str]:
    """Map each `## Heading` outside a fence to its text up to the next `#`/`##` heading."""
    return _split(body)[0]


def _prose_lines(text: str) -> list[str]:
    """`text`'s lines, endings stripped, with fenced code blocks (fences included) blanked."""
    lines = history.split_lines(text)
    # history's fence walker is the one CommonMark fence rule in the codebase;
    # this is the only place cookr reaches for it.
    return [bare or "" for _, bare in history._unfenced(lines, 0, len(lines))]


def _has_text(chunk: str) -> bool:
    return any(line.strip() for line in chunk.splitlines())


def _marker_problems(graded: str, compliance: str) -> list[str]:
    out = []
    found = list(_MARKER.finditer(graded))
    if found:
        out.append(f"body carries a `{NEEDS_REVIEW}` marker")
        # A marker broken across a line break (or spaced oddly) is never the
        # one-line bullet, and a line holding the phrase must be that bullet.
        if any(m.group(0) != NEEDS_REVIEW for m in found) or any(
                NEEDS_REVIEW in line and not _MARKER_BULLET.match(line)
                for line in graded.splitlines()):
            out.append(f"a `{NEEDS_REVIEW}` marker is not a one-line "
                       f"`- **name**: {NEEDS_REVIEW}: Not implemented in source.` bullet")
    if _MARKER.search(compliance):
        out.append(f"Compliance carries a `{NEEDS_REVIEW}` marker; put it on the bullet it qualifies")
    return out


def _is_citation(line: str, m: re.Match) -> bool:
    start, end = m.span()
    if start and (line[start - 1].isalnum() or line[start - 1] == "_"):
        return False  # "pipeline 3", "outline 2"
    before, after = line[max(0, start - _NEAR):start], line[end:end + _NEAR]
    if _FILE_NAME.search(before) or _FILE_NAME.search(after):
        return True
    if _SOURCE_BEFORE.search(before):
        return True
    if _OF_AFTER.match(after):
        return False  # "line 2 of the bubble": a position in what renders
    if m.group(1) and _RANGE_AFTER.match(after):
        return True  # "lines 10-20"
    return (not _TABLE_ROW.match(line) and bool(_CITING_BEFORE.search(before))
            and int(m.group(2)) >= 10)


def cites_source_lines(prose: Iterable[str]) -> bool:
    """True when a line of `prose` (fences already removed) cites a source line number."""
    for line in prose:
        for m in _FILE_COLON_LINE.finditer(line):
            if m.start() and (line[m.start() - 1].isalnum() or line[m.start() - 1] == "_"):
                return True
        if "ine" in line and any(_is_citation(line, m) for m in _LINE_WORD.finditer(line)):
            return True
    return False


def _winui_problems(notes: str) -> list[str]:
    lines = _prose_lines(notes)
    texts = []
    for i, line in enumerate(lines):
        m = _WINUI.match(line)
        if m is None:
            continue
        text = m.group(1).strip()
        if not text and i + 1 < len(lines):
            cont = _CONTINUATION.match(lines[i + 1])
            text = cont.group(1).strip() if cont else ""
        if text:
            texts.append(text)
    if not texts:
        return ["Platform Notes has no filled `WinUI 3` bullet"]
    if all(_NOT_APPLICABLE.match(text) for text in texts):
        return ["Platform Notes `WinUI 3` bullet says not applicable; it must give translation guidance"]
    return []


def _compliance_problems(compliance: str) -> list[str]:
    cited = {f"{d}#{n}" for d, n in CITATION.findall(compliance)}
    missing = [check for check in REQUIRED_CHECKS if check not in cited]
    if missing:
        return [f"Compliance does not cite {', '.join(f'`{c}`' for c in missing)}; "
                f"every component meets them"]
    return []


def _table_data_rows(text: str) -> int:
    """Data rows across the pipe tables in `text` (header and delimiter rows excluded)."""
    rows = 0
    lines = _prose_lines(text)
    for i, line in enumerate(lines):
        if not _TABLE_ROW.match(line) or _DELIMITER_ROW.match(line):
            continue
        is_header = i + 1 < len(lines) and _TABLE_ROW.match(lines[i + 1]) \
            and _DELIMITER_ROW.match(lines[i + 1])
        if not is_header:
            rows += 1
    return rows


def _decision_problems(decisions: str) -> list[str]:
    counts = {"Decision": 0, "Rationale": 0, "Approved": 0}
    for line in _prose_lines(decisions):
        m = _DECISION_LINE.match(line)
        if m:
            counts[m.group(1)] += 1
    if counts["Decision"] == 0 or len(set(counts.values())) != 1:
        return ["Design Decisions are not `**Decision**:` / `**Rationale**:` / `**Approved**:` "
                "line triples"]
    return []


def platform_problems(declared: Iterable[str], source_platforms: Iterable[str]) -> list[str]:
    """Rule 13: frontmatter `platforms` against the platforms the sources are on."""
    sources = sorted(set(source_platforms))
    if not sources or any(p not in PLATFORM_IDS for p in sources):
        return []
    have = {str(p) for p in declared}
    required: set[str] = set()
    allowed: set[str] = set()
    missing: list[str] = []
    for platform in sources:
        must, one_of = PLATFORM_IDS[platform]
        required |= must
        allowed |= must | one_of
        if one_of and not have & one_of:
            missing.append(" or ".join(f"`{p}`" for p in sorted(one_of)))
    missing = [f"`{p}`" for p in sorted(required - have)] + missing
    extra = sorted(have - allowed)
    if not missing and not extra:
        return []
    parts = []
    if missing:
        parts.append(f"lacks {', '.join(missing)}")
    if extra:
        parts.append(f"lists {', '.join(f'`{p}`' for p in extra)}, not a source platform")
    return [f"frontmatter `platforms` {'; '.join(parts)} (sources: {', '.join(sources)})"]


def _date(value: object) -> Optional[_dt.date]:
    if isinstance(value, _dt.datetime):
        return value.date()
    if isinstance(value, _dt.date):
        return value
    try:
        return _dt.date.fromisoformat(str(value).strip())
    except ValueError:
        return None


def history_problems(body: str, frontmatter: Mapping) -> list[str]:
    """Rule 14: the Change History table against itself and the frontmatter."""
    try:
        table = history.read(body)
    except history.HistoryError as e:
        if f"no `## {CHANGE_HISTORY}` section" in str(e):
            return []  # reported as a missing required section
        return [f"Change History: {e}"]
    if table.header is None:
        return ["Change History holds no `| Version | Date | Author | Summary |` table"]
    out = []
    blank = [row for row in table.rows
             if not all(row.cell(c) for c in ("Version", "Date", "Author"))]
    if blank:
        lines = ", ".join(str(row.line + 1) for row in blank)
        out.append(f"Change History has rows with a blank version, date or author (body lines {lines})")
    unreadable = [row.cell("Version") for row in table.rows
                  if row.cell("Version") and row.version is None]
    if unreadable:
        out.append(f"Change History versions are not X.Y.Z: {', '.join(unreadable)}")
    bad_dates = [row.cell("Date") for row in table.rows
                 if row.cell("Date") and _date(row.cell("Date")) is None]
    if bad_dates:
        out.append(f"Change History dates are not YYYY-MM-DD: {', '.join(bad_dates)}")
    if not unreadable and not blank and table.order == history.UNORDERED:
        listed = ", ".join(row.cell("Version") for row in table.rows)
        out.append(f"Change History rows are not in one version order ({listed}); "
                   f"sort them newest-first or oldest-first")
    newest = table.newest
    if newest is not None:
        version = str(frontmatter.get("version", "") or "").strip()
        if version != newest.cell("Version"):
            out.append(f"frontmatter `version` is `{version or '(none)'}` but the newest "
                       f"Change History row is {newest.cell('Version')}")
        row_date = _date(newest.cell("Date"))
        modified = _date(frontmatter.get("modified", "") or "")
        if row_date is not None and (modified is None or modified < row_date):
            shown = str(frontmatter.get("modified", "") or "").strip() or "(none)"
            out.append(f"frontmatter `modified` ({shown}) is older than the newest "
                       f"Change History row's date ({row_date.isoformat()})")
    return out


def _frontmatter(info: RecipeInfo) -> Mapping:
    return info.data


def problems(info: RecipeInfo, checks: Optional[frozenset[str]] = None,
             source_platforms: Optional[Iterable[str]] = None,
             domain: Optional[str] = None) -> list[str]:
    """Everything that keeps `info` from `complete`.

    `checks` is the compliance catalog (None skips rule 9); `source_platforms`
    are the `.cookr.json` platforms of every component this recipe covers
    (None skips rule 13); `domain` is the recipe's path-derived domain (None
    skips rule 15).
    """
    out = []
    if info.status not in COMPLETE_STATUSES:
        out.append(f"status is `{info.status or '(none)'}`, not review/accepted")
    found, graded = _split(info.body)
    compliance = found.get("Compliance", "")
    out += _marker_problems(graded, compliance)
    if _RFC_NAME.search(info.body):
        out.append("a requirement name starts with its RFC 2119 word (`must-`/`should-`/`may-`)")
    if cites_source_lines(_prose_lines(graded)):
        out.append("cites source line numbers; cite the type, function or quoted comment")
    if checks is not None:
        bad = unknown_citations(info.body, checks)
        if bad:
            out.append(f"cites compliance checks not in the catalog: {', '.join(bad)}")
    rtype = info.type
    if rtype not in templates.TYPES:
        # Graded against the ingredient template anyway, but never silently: a
        # typo'd type must not be able to report `complete`.
        out.append(f"unknown type `{rtype or '(none)'}`")
        rtype = "ingredient"
    required = templates.required_sections(rtype)
    for name in required:
        if name not in found:
            out.append(f"section `{name}` is missing")
        elif not _has_text(found[name]):
            out.append(f"section `{name}` is empty")
    out += _winui_problems(found.get("Platform Notes", ""))
    if "Compliance" in found:
        out += _compliance_problems(compliance)
    if VECTORS_SECTION in found and VECTORS_SECTION in required:
        rows = _table_data_rows(found[VECTORS_SECTION])
        if rows < MIN_VECTORS:
            out.append(f"{VECTORS_SECTION} has {rows} rows; at least {MIN_VECTORS} are required")
    if "Design Decisions" in found and _has_text(found["Design Decisions"]):
        out += _decision_problems(found["Design Decisions"])
    frontmatter = _frontmatter(info)
    if source_platforms is not None:
        declared = frontmatter.get("platforms") or []
        out += platform_problems(declared if isinstance(declared, list) else [declared],
                                 source_platforms)
    if domain is not None:
        actual = str(frontmatter.get("domain", "") or "").strip()
        if actual != domain:
            out.append(f"frontmatter `domain` is `{actual or '(none)'}`, not `{domain}`")
    out += history_problems(info.body, frontmatter)
    return out
