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
