"""A spec's `## Reference Implementations` section: the code that implements it.

In format 2 the rows live in the cookbook index (`index.json`, each entry's
`implementations`), never in the artifact. `render` draws them as the section
a compiled doc or skill shows. `parse`/`implementations` read the format-1
`| Platform | Path |` table, which only the upgrader still meets: `Path` is a
backticked path relative to the repository root; a path ending in `/` is a
directory and claims every source file below it.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Optional

from . import history
from .artifact import Part

SECTION = "Reference Implementations"

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


def render(rows) -> str:
    """The section's table for index implementations `rows` (without the `## ` heading)."""
    lines = ["| Platform | Location | Conformance |", "|----------|----------|-------------|"]
    for r in rows:
        where = f"`{r.location}`" if r.location else "(planned)"
        state = r.conformance.state
        if r.conformance.version:
            state += f" ({r.conformance.version})"
        lines.append(f"| {r.platform} | {where} | {state} |")
    return "\n".join(lines)


def part(rows):
    """The derived `## Reference Implementations` part for a compiled doc or skill;
    None when there are no rows."""
    if not rows:
        return None
    return Part(name="reference-implementations", text=f"\n{render(rows)}\n\n", heading=SECTION)
