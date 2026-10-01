"""The compliance check catalog a recipe's Compliance table cites against.

A check is a `### <name>` heading in a catalog document. The document's path
under the catalog, minus `.md`, names it exactly as its `domain` does, so a
recipe cites a check as `agenticdevelopercookbook://compliance/<document>#<name>`:
`compliance/security#secure-storage` for `security.md`, and
`compliance/artifact-formatting/recipe-formatting#has-frontmatter` for
`artifact-formatting/recipe-formatting.md`. Which files count is
`cookbook.core.markdown.iter_markdown`'s rule, the one every cookbook walk uses,
so index, references and template files never define checks.

install.sh materialises the catalog into the extract prompt module's references
(its reference-manifest.json). When it has not been materialised — a source
checkout that never ran install.sh — `load_checks` returns None and callers skip
the check rather than report every citation unknown.
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import Optional

from cookbook.core.markdown import iter_markdown

CITATION = re.compile(r"agenticdevelopercookbook://compliance/([a-z0-9-]+(?:/[a-z0-9-]+)*)#([a-z0-9-]+)")
_CHECK = re.compile(r"^###\s+([a-z0-9-]+)\s*$", re.MULTILINE)


def load_checks(catalog: Path) -> Optional[frozenset[str]]:
    """Every `<document>#<check>` the catalog defines, or None if it is absent."""
    if not catalog.is_dir():
        return None
    found = set()
    for f in iter_markdown(catalog):
        document = f.relative_to(catalog).with_suffix("").as_posix()
        found.update(f"{document}#{name}" for name in _CHECK.findall(f.read_text(encoding="utf-8")))
    return frozenset(found)


def unknown_citations(body: str, checks: frozenset[str]) -> list[str]:
    """Cited `<document>#<check>` pairs the catalog does not define, sorted, de-duplicated."""
    return sorted({f"{d}#{n}" for d, n in CITATION.findall(body)} - checks)


def summary(checks: frozenset[str]) -> str:
    """One line per document, `document: check, check, …` — the brief's citation list."""
    by_doc: dict[str, list[str]] = {}
    for item in checks:
        document, name = item.split("#", 1)
        by_doc.setdefault(document, []).append(name)
    return "\n".join(f"- `{doc}`: {', '.join(sorted(names))}" for doc, names in sorted(by_doc.items()))
