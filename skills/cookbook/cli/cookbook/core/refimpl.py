"""A spec's `## Reference Implementations` section: the code that implements it.

The section is a `| Platform | Path |` table. `Path` is a backticked path
relative to the repository root; a path ending in `/` is a directory and claims
every source file below it. A cookbook with no code writes one `Not applicable`
line instead of the table, which reads as no rows.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Optional

from . import history

SECTION = "Reference Implementations"
PLATFORMS = ("web", "apple", "android", "windows", "python")

_CODE = re.compile(r"`([^`]+)`")


@dataclass(frozen=True)
class Implementation:
    platform: str
    path: str  # repo-relative POSIX path, no leading `/`; a directory keeps its trailing `/`

    @property
    def is_dir(self) -> bool:
        return self.path.endswith("/")


def section(body: str) -> Optional[str]:
    """The section's text, or None when the spec has no such section."""
    return dict(history.h2_sections(body)).get(SECTION)


def parse(text: str) -> list[Implementation]:
    """Every table row of a section's text, in order. Header and delimiter rows are skipped."""
    out = []
    for line in text.splitlines():
        if not line.lstrip().startswith("|"):
            continue
        cells = history.split_row(line)
        if len(cells) < 2:
            continue
        platform = cells[0].strip().lower()
        m = _CODE.search(cells[1])
        if platform == "platform" or set(cells[0].strip()) <= set("-: ") or m is None:
            continue
        out.append(Implementation(platform=platform, path=m.group(1).strip().lstrip("/")))
    return out


def implementations(body: str) -> list[Implementation]:
    """The implementations a spec body lists; empty when it lists none."""
    text = section(body)
    return parse(text) if text is not None else []


def render(rows: list[Implementation]) -> str:
    """The section's table for `rows` (without the `## ` heading)."""
    lines = ["| Platform | Path |", "|----------|------|"]
    lines += [f"| {r.platform} | `{r.path}` |" for r in rows]
    return "\n".join(lines)


# The template puts the section right before these, in this order of preference.
_BEFORE = ("Design Decisions", "Compliance", "Change History")


def _body_start(lines: list[str]) -> int:
    """Index of the first line after the YAML frontmatter; 0 when there is none."""
    if lines and lines[0].rstrip("\r\n") == "---":
        for i in range(1, len(lines)):
            if lines[i].rstrip("\r\n") in ("---", "..."):
                return i + 1
    return 0


def with_section(text: str, rows: list[Implementation]) -> str:
    """`text` (a whole spec file) with its Reference Implementations section set to `rows`.

    An existing section's body is replaced and every other line keeps its
    bytes. Without one, the section goes before Design Decisions (else
    Compliance, else Change History), or at the end.
    """
    lines = history.split_lines(text)
    spans = history.h2_spans(lines, _body_start(lines))
    block = f"{render(rows)}\n\n"
    found = next((s for s in spans if s.heading == SECTION), None)
    if found is not None:
        return "".join(lines[:found.start + 1] + ["\n", block] + lines[found.end:])
    for heading in _BEFORE:
        at = next((s.start for s in spans if s.heading == heading), None)
        if at is not None:
            return "".join(lines[:at] + [f"## {SECTION}\n\n", block] + lines[at:])
    tail = "" if text.endswith("\n") else "\n"
    return f"{text}{tail}\n## {SECTION}\n\n{render(rows)}\n"
