"""The rules that separate a `partial` recipe from a `complete` one.

A recipe is complete when:
1. its status is `review` or `accepted`;
2. its body carries no `NEEDS REVIEW` marker outside the Change History
   section (a changelog row that says "removed the NEEDS REVIEW marker" is a
   record of the fix, not a gap);
3. its `type` is one REQUIRED_SECTIONS knows;
4. every section in REQUIRED_SECTIONS[type] is present with at least one
   non-blank body line before the next `##` heading;
5. its Platform Notes section has a WinUI 3 bullet with translation guidance:
   the bold label names `WinUI 3` (decoration such as `**WinUI 3** (Windows):`
   or `**WinUI 3 / C#**:` is tolerated), text follows it, and that text is
   not `Not applicable` — Platform Notes is translation guidance, never a gap;
6. every `NEEDS REVIEW` marker outside Change History is a named bullet with
   the whole phrase on one line, `- **name**: NEEDS REVIEW: Not implemented in
   source.`, and none sits in Compliance (the rationale there describes the gap
   in prose; the bullet it qualifies carries the marker);
7. no requirement name is prefixed with its RFC 2119 word (`**must-…**`);
8. it cites no source line numbers (`(line 42)`, `source lines 10-20`,
   `Store.swift:88`) — they go stale with the next edit;
9. every compliance check it cites exists in the catalog, when one is given.

Rules 6-8 are what writers got wrong repeatedly; a script can see each one,
so the grade says so instead of a reviewer re-deriving it.
"""

from __future__ import annotations

import re
from typing import Optional

from .compliance import unknown_citations
from .recipes import RecipeInfo

COMPLETE_STATUSES = ("review", "accepted")
NEEDS_REVIEW = "NEEDS REVIEW"
CHANGE_HISTORY = "Change History"

REQUIRED_SECTIONS = {
    "ingredient": (
        "Overview", "Behavioral Requirements", "Appearance", "States", "Accessibility",
        "Conformance Test Vectors", "Edge Cases", "Configuration", "Platform Notes",
        "Design Decisions",
    ),
    "recipe": (
        "Overview", "Ingredients", "Integration Requirements", "Layout", "Shared State",
        "Integration Test Vectors", "Edge Cases", "Platform Notes", "Design Decisions",
    ),
}

_H2 = re.compile(r"^##\s+(.+?)\s*$", re.MULTILINE)
_WINUI = re.compile(
    r"^-\s+\*\*[^*\n]*WinUI 3[^*\n]*\*\*\s*(?:\([^)\n]*\))?\s*:?\s*(\S.*)?$",
    re.MULTILINE,
)
_NOT_APPLICABLE = re.compile(r"^not applicable\b", re.IGNORECASE)
_MARKER_BULLET = re.compile(r"^\s*- \*\*[^*\n]+\*\*: NEEDS REVIEW: Not implemented in source\.")
_RFC_NAME = re.compile(r"^\s*- \*\*(must|should|may)-", re.MULTILINE | re.IGNORECASE)
_CODE_SPAN = re.compile(r"`[^`\n]*`")
# Citation shapes only: "line 1" inside a test vector's data is not a citation.
_LINE_CITE = re.compile(
    r"\b(?:source|at|on|see)\s+lines?\s+\d+|\(lines?\s+\d+|\blines\s+\d+\s*[-\u2013]\s*\d+"
    r"|\.(?:swift|tsx?|jsx?|py|m|h|kt|cs):\d+"
)


def sections(body: str) -> dict[str, str]:
    """Map each `## Heading` to the text up to the next `##` (or `#`) heading."""
    out = {}
    matches = list(_H2.finditer(body))
    for i, m in enumerate(matches):
        start = m.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(body)
        chunk = body[start:end]
        # Stop at a top-level heading if one appears before the next ##.
        h1 = re.search(r"^#\s", chunk, re.MULTILINE)
        if h1:
            chunk = chunk[: h1.start()]
        out[m.group(1)] = chunk
    return out


def _has_text(chunk: str) -> bool:
    return any(line.strip() for line in chunk.splitlines())


def problems(info: RecipeInfo, checks: Optional[frozenset[str]] = None) -> list[str]:
    """Everything that keeps `info` from `complete`; `checks` is the compliance catalog."""
    out = []
    if info.status not in COMPLETE_STATUSES:
        out.append(f"status is `{info.status or '(none)'}`, not review/accepted")
    found = sections(info.body)
    history = found.get(CHANGE_HISTORY, "")
    graded_body = info.body.replace(history, "", 1) if history else info.body
    if NEEDS_REVIEW in graded_body:
        out.append(f"body carries a `{NEEDS_REVIEW}` marker")
    if any(NEEDS_REVIEW in line and not _MARKER_BULLET.match(line)
           for line in graded_body.splitlines()):
        out.append(f"a `{NEEDS_REVIEW}` marker is not a one-line "
                   f"`- **name**: {NEEDS_REVIEW}: Not implemented in source.` bullet")
    if NEEDS_REVIEW in found.get("Compliance", ""):
        out.append(f"Compliance carries a `{NEEDS_REVIEW}` marker; put it on the bullet it qualifies")
    if _RFC_NAME.search(info.body):
        out.append("a requirement name starts with its RFC 2119 word (`must-`/`should-`/`may-`)")
    if _LINE_CITE.search(_CODE_SPAN.sub("", info.body)):
        out.append("cites source line numbers; cite the type, function or quoted comment")
    if checks is not None:
        bad = unknown_citations(info.body, checks)
        if bad:
            out.append(f"cites compliance checks not in the catalog: {', '.join(bad)}")
    if info.type not in REQUIRED_SECTIONS:
        # Graded against the ingredient list anyway, but never silently: a typo'd
        # type must not be able to report `complete`.
        out.append(f"unknown type `{info.type or '(none)'}`")
    required = REQUIRED_SECTIONS.get(info.type, REQUIRED_SECTIONS["ingredient"])
    for name in required:
        if name not in found:
            out.append(f"section `{name}` is missing")
        elif not _has_text(found[name]):
            out.append(f"section `{name}` is empty")
    notes = found.get("Platform Notes", "")
    m = _WINUI.search(notes)
    text = (m.group(1) or "").strip() if m else ""
    if not text:
        out.append("Platform Notes has no filled `WinUI 3` bullet")
    elif _NOT_APPLICABLE.match(text):
        out.append("Platform Notes `WinUI 3` bullet says not applicable; it must give translation guidance")
    return out
