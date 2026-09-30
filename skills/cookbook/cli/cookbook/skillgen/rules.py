"""Extract rules (MUST/SHOULD/MAY statements) and test-vector ids from a leaf.

A rule is one bullet item (with its continuation lines and nested bullets) or
one paragraph that carries an RFC 2119 keyword. Its slug is, in order:

1. an explicit kebab-case bold label — `- **save-restore-urls**: …` (recipes);
2. a slugified bold label — `- **Native apps (iOS):** …` → `native-apps`;
3. a slug built from the content words around the first keyword —
   `Refresh token rotation MUST be used` → `refresh-token-rotation-used`.

Only (1) appears in the source text, so a leaf prints its checklist of slugs
for the others — a reviewer cannot cite a slug it cannot see.
"""

from __future__ import annotations

import re
from collections import Counter
from dataclasses import dataclass

KEYWORD_RE = re.compile(
    r"\b(MUST NOT|MUST|SHALL NOT|SHALL|REQUIRED|SHOULD NOT|SHOULD|RECOMMENDED|MAY)\b"
)
LEVEL_OF = {
    "MUST": "MUST", "MUST NOT": "MUST", "SHALL": "MUST", "SHALL NOT": "MUST", "REQUIRED": "MUST",
    "SHOULD": "SHOULD", "SHOULD NOT": "SHOULD", "RECOMMENDED": "SHOULD",
    "MAY": "MAY",
}
LEVEL_RANK = {"MUST": 0, "SHOULD": 1, "MAY": 2}

BULLET_RE = re.compile(r"^( *)(?:[-*+]|\d+[.)]) +(.*)$")
LABEL_RE = re.compile(r"^\*\*(.+?)\*\*\s*(\(([^)]*)\))?\s*[:—–-]?\s*")
KEBAB_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)+$")
HEADING_RE = re.compile(r"^#{1,6} ")
STOPWORDS = frozenset(
    "a an the be is are was to of for and or in on at with by as it its this that "
    "these those which when if then all any each every must should may shall not no "
    "required recommended".split()
)
SLUG_WORDS_BEFORE = 3
SLUG_WORDS_AFTER = 4
EXCERPT_CHARS = 120


@dataclass(frozen=True)
class Rule:
    slug: str
    level: str
    explicit: bool
    qualifier: str
    excerpt: str


@dataclass(frozen=True)
class TestVector:
    id: str
    requirements: tuple[str, ...]


def _plain(text: str) -> str:
    text = re.sub(r"\[([^\]]+)\]\([^)]*\)", r"\1", text)
    text = text.replace("**", "").replace("`", "")
    return " ".join(text.split())


def _slugify(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")


def _units(text: str) -> list[str]:
    """Top-level bullet items and paragraphs, outside code fences and tables."""
    units: list[list[str]] = []
    cur: list[str] | None = None
    fenced = False
    for line in text.split("\n"):
        if line.lstrip().startswith("```"):
            fenced = not fenced
            cur = None
            continue
        if fenced or line.lstrip().startswith("|") or HEADING_RE.match(line):
            cur = None
            continue
        if not line.strip():
            cur = None
            continue
        bullet = BULLET_RE.match(line)
        if bullet and len(bullet.group(1)) < 2:
            cur = [bullet.group(2)]
            units.append(cur)
        elif cur is not None:
            cur.append(line.strip())
        else:
            cur = [line.strip()]
            units.append(cur)
    return [" ".join(u) for u in units]


def _words(text: str) -> list[str]:
    return [w for w in _slugify(text).split("-") if len(w) > 1 and w not in STOPWORDS]


def _derived_slug(text: str, match: re.Match) -> str:
    before = _words(text[: match.start()])[-SLUG_WORDS_BEFORE:]
    after = _words(text[match.end():])[:SLUG_WORDS_AFTER]
    negated = ["not"] if match.group(1).endswith("NOT") else []
    return "-".join(before + negated + after)


def _rule(unit: str) -> Rule | None:
    matches = list(KEYWORD_RE.finditer(unit))
    if not matches:
        return None
    level = min((LEVEL_OF[m.group(1)] for m in matches), key=LEVEL_RANK.__getitem__)
    label = LABEL_RE.match(unit)
    qualifier = ""
    if label:
        raw = label.group(1).strip().rstrip(":").strip()
        qualifier = (label.group(3) or "").strip()
        if KEBAB_RE.match(raw) or re.fullmatch(r"[a-z0-9]+", raw):
            return Rule(raw, level, True, qualifier, _excerpt(unit[label.end():]))
        inner = re.sub(r"\([^)]*\)", "", raw)
        slug = _slugify(inner)
        if slug:
            return Rule(slug, level, False, qualifier, _excerpt(unit[label.end():]))
    plain = _plain(unit)
    m = KEYWORD_RE.search(plain)
    slug = _derived_slug(plain, m) or "rule"
    return Rule(slug, level, False, qualifier, _excerpt(unit))


def _excerpt(text: str) -> str:
    plain = _plain(text)
    if len(plain) <= EXCERPT_CHARS:
        return plain
    cut = plain[:EXCERPT_CHARS].rsplit(" ", 1)[0]
    return cut + " …"


def extract(text: str, seen: Counter) -> list[Rule]:
    """Rules in `text`. `seen` is shared across a doc's leaves so slugs stay unique per doc."""
    out = []
    for unit in _units(text):
        rule = _rule(unit)
        if rule is None:
            continue
        seen[rule.slug] += 1
        if seen[rule.slug] > 1:
            rule = Rule(f"{rule.slug}-{seen[rule.slug]}", rule.level, rule.explicit, rule.qualifier, rule.excerpt)
        out.append(rule)
    return out


def test_vectors(text: str) -> list[TestVector]:
    """Rows of any table whose header starts `| ID | Requirements |`."""
    out = []
    in_table = False
    for line in text.split("\n"):
        cells = [c.strip() for c in line.strip().strip("|").split("|")] if line.lstrip().startswith("|") else None
        if cells is None:
            in_table = False
            continue
        if len(cells) >= 2 and cells[0].lower() == "id" and cells[1].lower().startswith("requirement"):
            in_table = True
            continue
        if not in_table or set(cells[0]) <= set("-: "):
            continue
        reqs = tuple(r.strip().strip("`") for r in cells[1].split(",") if r.strip())
        out.append(TestVector(cells[0].strip("`"), reqs))
    return out
