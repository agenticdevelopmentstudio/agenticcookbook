"""The rules that separate a `partial` recipe from a `complete` one.

A recipe is complete when:
1. its status is `review` or `accepted`;
2. its body carries no `NEEDS REVIEW` marker;
3. every section in REQUIRED_SECTIONS[type] is present with at least one
   non-blank body line before the next `##` heading;
4. its Platform Notes section has a `- **WinUI 3**:` bullet with text after the colon.
"""

from __future__ import annotations

import re

from .recipes import RecipeInfo

COMPLETE_STATUSES = ("review", "accepted")
NEEDS_REVIEW = "NEEDS REVIEW"

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
_WINUI = re.compile(r"^-\s+\*\*WinUI 3\*\*:\s*(\S.*)?$", re.MULTILINE)


def sections(body: str) -> dict:
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


def problems(info: RecipeInfo) -> list:
    out = []
    if info.status not in COMPLETE_STATUSES:
        out.append(f"status is `{info.status or '(none)'}`, not review/accepted")
    if NEEDS_REVIEW in info.body:
        out.append(f"body carries a `{NEEDS_REVIEW}` marker")
    required = REQUIRED_SECTIONS.get(info.type, REQUIRED_SECTIONS["ingredient"])
    found = sections(info.body)
    for name in required:
        if name not in found:
            out.append(f"section `{name}` is missing")
        elif not _has_text(found[name]):
            out.append(f"section `{name}` is empty")
    notes = found.get("Platform Notes", "")
    m = _WINUI.search(notes)
    if not m or not (m.group(1) or "").strip():
        out.append("Platform Notes has no filled `WinUI 3` bullet")
    return out
