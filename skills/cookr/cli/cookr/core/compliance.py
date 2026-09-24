"""The compliance check catalog a recipe's Compliance table cites against.

A check is a `### <name>` heading in `cookbook/compliance/<category>.md`; files
one directory down (`artifact-formatting/recipe-formatting.md`) take the
directory name as their category. A recipe cites a check as
`agenticdevelopercookbook://compliance/<category>#<name>`.

install.sh materialises the catalog next to the extract templates (the prompt
module's reference-manifest.json). When it has not been materialised — a
source checkout that never ran install.sh — `load_checks` returns None and
callers skip the check rather than report every citation unknown.
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import Optional

CITATION = re.compile(r"agenticdevelopercookbook://compliance/([a-z0-9-]+)#([a-z0-9-]+)")
_CHECK = re.compile(r"^###\s+([a-z0-9-]+)\s*$", re.MULTILINE)


def load_checks(catalog: Path) -> Optional[frozenset[str]]:
    """Every `<category>#<check>` the catalog defines, or None if it is absent."""
    if not catalog.is_dir():
        return None
    found = set()
    for f in catalog.glob("**/*.md"):
        if f.name == "INDEX.md":
            continue
        category = f.stem if f.parent == catalog else f.parent.name
        found.update(f"{category}#{name}" for name in _CHECK.findall(f.read_text(encoding="utf-8")))
    return frozenset(found)


def unknown_citations(body: str, checks: frozenset[str]) -> list[str]:
    """Cited `<category>#<check>` pairs the catalog does not define, sorted, de-duplicated."""
    return sorted({f"{c}#{n}" for c, n in CITATION.findall(body)} - checks)


def summary(checks: frozenset[str]) -> str:
    """One line per category, `category: check, check, …` — the brief's citation list."""
    by_cat: dict[str, list[str]] = {}
    for item in checks:
        cat, name = item.split("#", 1)
        by_cat.setdefault(cat, []).append(name)
    return "\n".join(f"- `{cat}`: {', '.join(sorted(names))}" for cat, names in sorted(by_cat.items()))
