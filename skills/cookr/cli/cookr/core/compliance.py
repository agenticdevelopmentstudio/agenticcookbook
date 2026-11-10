"""Compliance checks, and the citations a recipe's Compliance section makes.

A check is a `### <name>` heading in a catalog document; the catalog is the
directory a cookbook's index names as its `catalog`. The cookbook index gives
each check an entry of kind `check`, with a UUID derived from the cookbook and
`<document>#<name>` (`identity.check_uuid`) and that pair as its `path`.
A recipe cites a check as an in-text link to that entry,
`[adc.check.best-practices.unit-test-coverage](cookbook:<cookbook-uuid>/<check-uuid>)`,
so a citation is checked by resolving its link (`links.Resolver`), never by
matching text. Which catalog files count is `cookr.core.markdown.iter_markdown`'s
rule, so index, references and template files never define checks.
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import Optional

from cookr.core.markdown import iter_markdown

from .index import Index
from .links import Link, Resolver, format_link, in_text_links

_CHECK = re.compile(r"^###\s+([a-z0-9-]+)\s*$", re.MULTILINE)
# A check rdid: `<cookbook>.check.<document, dotted>.<name>`.
_CHECK_RDID = re.compile(r"^[a-z][a-z0-9-]*\.check\.([a-z0-9.-]+)\.([a-z0-9-]+)$")


def load_checks(catalog: Path) -> Optional[frozenset[str]]:
    """Every `<document>#<check>` the catalog defines, or None if it is absent."""
    if not catalog.is_dir():
        return None
    found = set()
    for f in iter_markdown(catalog):
        document = f.relative_to(catalog).with_suffix("").as_posix()
        found.update(f"{document}#{name}" for name in _CHECK.findall(f.read_text(encoding="utf-8")))
    return frozenset(found)


def is_check_label(label: str) -> bool:
    return _CHECK_RDID.match(label.strip()) is not None


def citations(text: str) -> list[tuple[str, Link]]:
    """The in-text links in `text` whose label is a check rdid, in order."""
    return [(label, link) for label, link in in_text_links(text) if is_check_label(label)]


def _label_check(label: str) -> str:
    """`<document dotted>.<name>` from a check rdid label, as `<document>#<name>` with
    the document's dots read as directory separators (a best guess for a link that
    does not resolve)."""
    m = _CHECK_RDID.match(label.strip())
    return f"{m.group(1).replace('.', '/')}#{m.group(2)}" if m else ""


def cited_checks(text: str, resolver: Optional[Resolver] = None) -> set[str]:
    """Every `<document>#<name>` a check citation in `text` names: the resolved entry's
    path, else (unresolvable, or no `resolver`) the label's."""
    out = set()
    for label, link in citations(text):
        res = resolver.resolve(link) if resolver is not None else None
        if res is not None and res.state == "ok" and res.entry.kind == "check":
            out.add(res.entry.path)
        else:
            out.add(_label_check(label))
    return out


def unknown_citations(text: str, resolver: Resolver) -> list[str]:
    """Check citations in `text` that name no check: the link resolves to nothing,
    or to an artifact that is not a check. A citation into a cookbook that cannot
    be reached is not judged here (validate warns about it). Sorted labels."""
    bad = set()
    for label, link in citations(text):
        res = resolver.resolve(link)
        if res.state == "missing" or (res.state == "ok" and res.entry.kind != "check"):
            bad.add(f"{label} ({format_link(link)})")
    return sorted(bad)


def check_links(index: Index) -> list[str]:
    """`[rdid](cookbook:<cookbook>/<uuid>)` for every check `index` defines, by rdid."""
    cid = index.cookbook.id
    return [f"[{e.rdid}](cookbook:{cid}/{e.id})"
            for e in sorted(index.entries.values(), key=lambda e: e.rdid) if e.kind == "check"]
