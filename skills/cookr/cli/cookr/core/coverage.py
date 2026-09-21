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
    tiers: tuple
    platforms: tuple
    paths: tuple
    state: str
    recipe: Optional[str]
    problems: tuple


@dataclass
class CoverageReport:
    rows: list
    unmatched_recipes: list

    def tally(self) -> dict[str, dict[str, int]]:
        out = {}
        for r in self.rows:
            for tier in r.tiers:
                t = out.setdefault(tier, {s: 0 for s in STATES})
                t[r.state] += 1
        return out

    def below(self, level: str) -> list[CoverageRow]:
        return [r for r in self.rows if _RANK[r.state] < _RANK[level]]


def compute(config: Config, tier: Optional[str] = None) -> CoverageReport:
    """One row per component `name`, across every tier the name appears in.

    `tier` filters the rows that are returned; it never narrows the corpus the
    rows are matched against, so `unmatched_recipes` is the same list either way.
    """
    corpus = load_corpus(config.recipes_dir)

    grouped = {}
    for c in scan(config):
        grouped.setdefault(c.name, []).append(c)

    matched_slugs = set()
    rows = []
    for name, items in sorted(grouped.items()):
        slug = config.aliases.get(name, name)
        info = corpus.get(slug)
        if info is None:
            state, recipe, probs = "missing", None, ()
        else:
            matched_slugs.add(slug)
            probs = tuple(problems(info))
            state, recipe = ("partial" if probs else "complete"), slug
        rows.append(CoverageRow(
            name=name,
            tiers=tuple(sorted({i.tier for i in items})),
            platforms=tuple(sorted({i.platform for i in items})),
            paths=tuple(sorted(i.path for i in items)),
            state=state, recipe=recipe, problems=probs,
        ))

    unmatched = sorted(s for s in corpus if s not in matched_slugs)
    if tier is not None:
        rows = [r for r in rows if tier in r.tiers]
    return CoverageReport(rows=rows, unmatched_recipes=unmatched)
