"""Join the source inventory against the recipe corpus."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from .completeness import problems
from .config import Config
from .inventory import scan
from .recipes import load_corpus

STATES = ("missing", "partial", "complete")
_RANK = {s: i for i, s in enumerate(STATES)}


@dataclass(frozen=True)
class CoverageRow:
    name: str
    tier: str
    platforms: tuple
    paths: tuple
    state: str
    recipe: Optional[str]
    problems: tuple


@dataclass
class CoverageReport:
    rows: list
    unmatched_recipes: list

    def tally(self) -> dict:
        out = {}
        for r in self.rows:
            t = out.setdefault(r.tier, {s: 0 for s in STATES})
            t[r.state] += 1
        return out

    def below(self, level: str) -> list:
        return [r for r in self.rows if _RANK[r.state] < _RANK[level]]


def compute(config: Config, tier: Optional[str] = None) -> CoverageReport:
    corpus = load_corpus(config.recipes_dir)
    components = [c for c in scan(config) if tier is None or c.tier == tier]

    grouped = {}
    for c in components:
        grouped.setdefault((c.tier, c.name), []).append(c)

    matched_slugs = set()
    rows = []
    for (t, name), items in sorted(grouped.items()):
        slug = config.aliases.get(name, name)
        info = corpus.get(slug)
        if info is None:
            state, recipe, probs = "missing", None, ()
        else:
            matched_slugs.add(slug)
            probs = tuple(problems(info))
            state, recipe = ("partial" if probs else "complete"), slug
        rows.append(CoverageRow(
            name=name, tier=t,
            platforms=tuple(sorted({i.platform for i in items})),
            paths=tuple(i.path for i in items),
            state=state, recipe=recipe, problems=probs,
        ))

    if tier is None:
        unmatched = sorted(s for s in corpus if s not in matched_slugs)
    else:
        unmatched = []
    return CoverageReport(rows=rows, unmatched_recipes=unmatched)
