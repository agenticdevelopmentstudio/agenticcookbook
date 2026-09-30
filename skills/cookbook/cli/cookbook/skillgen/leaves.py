"""Clean a doc body and split it into leaves no larger than the cap.

Cleaning drops what an agent applying the rules never needs: the Change
History and Compliance sections, placeholder sections ("_None yet_", "Not
applicable"), and relative links — a leaf linking to another leaf would be a
third hop, so the link text stays and the link goes.

Recipes and ingredients are split by section (states, test vectors, edge
cases, logging each become a leaf). Any leaf still over the cap is packed
into parts by H2, then H3, then paragraph, then list item (a table by rows,
header repeated). Only a single list item or line over the cap is an error.
"""

from __future__ import annotations

import re
from dataclasses import dataclass

DEFAULT_CAP = 12_000

STRIP_SECTIONS = {"change history", "compliance"}
PLACEHOLDER_RE = re.compile(r"^\s*(?:_?none yet|not applicable|n/a)\b", re.IGNORECASE)
SPLIT_SECTIONS = {
    "states": "states",
    "conformance test vectors": "test-vectors",
    "edge cases": "edge-cases",
    "logging": "logging",
}
SPLIT_TYPES = {"recipe", "ingredient"}

LIST_ITEM_RE = re.compile(r"^ ?(?:[-*+]|\d+[.)]) +")
H2_RE = re.compile(r"^## +(.+?)\s*#*\s*$")
REL_LINK_RE = re.compile(r"(?<!!)\[([^\]]+)\]\((?!https?://|mailto:|#)[^)\s]+\)")


class LeafTooLarge(Exception):
    pass


@dataclass(frozen=True)
class Part:
    suffix: str   # "" for the main leaf, else e.g. "states" or "part-2"
    heading: str  # section label for the leaf's own H1 ("" for main)
    text: str


def _sections(body: str) -> list[tuple[str, str]]:
    """Split at H2, outside code fences: [(heading or "", text)]."""
    out: list[tuple[str, list[str]]] = [("", [])]
    fenced = False
    for line in body.splitlines():
        if line.lstrip().startswith("```"):
            fenced = not fenced
        m = None if fenced else H2_RE.match(line)
        if m:
            out.append((m.group(1).strip(), [line]))
        else:
            out[-1][1].append(line)
    return [(h, "\n".join(lines)) for h, lines in out]


def clean(body: str) -> str:
    kept = []
    for heading, text in _sections(body):
        key = heading.lower()
        if key in STRIP_SECTIONS:
            continue
        content = text.split("\n", 1)[1] if heading and "\n" in text else ("" if heading else text)
        if heading and (not content.strip() or PLACEHOLDER_RE.match(content.strip())):
            continue
        kept.append(text)
    text = "\n".join(kept)
    text = REL_LINK_RE.sub(r"\1", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip() + "\n"


def _split_units(text: str, strategy: int) -> list[str]:
    lines = text.split("\n")
    if strategy in (0, 1):
        marker = "## " if strategy == 0 else "### "
        units: list[list[str]] = [[]]
        fenced = False
        for line in lines:
            if line.lstrip().startswith("```"):
                fenced = not fenced
            if not fenced and line.startswith(marker) and units[-1]:
                units.append([])
            units[-1].append(line)
        return ["\n".join(u) for u in units if "\n".join(u).strip()]
    if strategy == 3:
        # top-level list items, each with its continuation and nested lines
        units, fenced = [[]], False
        for line in lines:
            if line.lstrip().startswith("```"):
                fenced = not fenced
            if not fenced and LIST_ITEM_RE.match(line) and units[-1]:
                units.append([])
            units[-1].append(line)
        return ["\n".join(u) for u in units if "\n".join(u).strip()]
    # paragraphs (blank-line separated, code fences kept whole)
    units, cur, fenced = [], [], False
    for line in lines:
        if line.lstrip().startswith("```"):
            fenced = not fenced
        if not fenced and not line.strip():
            if cur:
                units.append("\n".join(cur))
                cur = []
            continue
        cur.append(line)
    if cur:
        units.append("\n".join(cur))
    return units


def _split_table(text: str, cap: int) -> list[str] | None:
    lines = text.split("\n")
    if len(lines) < 3 or not all(l.lstrip().startswith("|") for l in lines):
        return None
    header, rows = lines[:2], lines[2:]
    chunks, cur = [], list(header)
    for row in rows:
        if len("\n".join(cur + [row])) > cap and len(cur) > 2:
            chunks.append("\n".join(cur))
            cur = list(header)
        cur.append(row)
    chunks.append("\n".join(cur))
    return chunks


def fit(text: str, cap: int, where: str, strategy: int = 0) -> list[str]:
    """Pack `text` into chunks of at most `cap` characters."""
    if len(text) <= cap:
        return [text]
    if strategy == 3:
        table = _split_table(text, cap)
        if table and all(len(c) <= cap for c in table):
            return table
    if strategy > 3:
        raise LeafTooLarge(f"{where}: a single block of {len(text)} chars exceeds the {cap}-char leaf cap")
    units = _split_units(text, strategy)
    if len(units) <= 1:
        return fit(text, cap, where, strategy + 1)
    sep = "\n\n" if strategy == 2 else "\n"
    chunks: list[str] = []
    cur = ""
    for unit in units:
        pieces = fit(unit, cap, where, strategy + 1) if len(unit) > cap else [unit]
        for piece in pieces:
            joined = f"{cur}{sep}{piece}" if cur else piece
            if len(joined) > cap and cur:
                chunks.append(cur)
                cur = piece
            else:
                cur = joined
    if cur:
        chunks.append(cur)
    return chunks


HEADER_ROOM = 400  # a leaf's comment line and optional H1


def split(body: str, doc_type: str, cap: int, where: str, budget: int | None = None) -> list[Part]:
    """Split into parts whose text is at most `budget` chars (default: cap minus header room).

    The caller renders each part with its rule checklist prepended and, when
    that overflows the cap, calls again with a smaller budget.
    """
    text = clean(body)
    sections = [(text, "", "")]
    if doc_type in SPLIT_TYPES:
        main, split_out = [], []
        for heading, section in _sections(text):
            suffix = SPLIT_SECTIONS.get(heading.lower())
            if suffix:
                split_out.append((section.strip() + "\n", suffix, heading))
            else:
                main.append(section)
        sections = [("\n".join(main).strip() + "\n", "", "")] + split_out
    parts: list[Part] = []
    if budget is None:
        budget = cap - HEADER_ROOM
    for section, suffix, heading in sections:
        chunks = fit(section.strip(), budget, where)
        for i, chunk in enumerate(chunks, start=1):
            part_suffix = suffix if i == 1 else f"{suffix}-part-{i}".lstrip("-")
            parts.append(Part(part_suffix, heading if i == 1 else f"{heading or 'continued'} (part {i})".strip(), chunk + "\n"))
    return parts
