"""Join the source inventory against the recipe corpus."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from .completeness import problems
from .config import Config
from .inventory import Component, scan
from .recipes import load_corpus

STATES = ("missing", "partial", "complete")
_RANK = {s: i for i, s in enumerate(STATES)}


@dataclass(frozen=True)
class CoverageRow:
    name: str
    slug: str  # the recipe stem this name resolves to (through `aliases`), matched or not
    tiers: tuple
    platforms: tuple
    paths: tuple
    state: str  # `missing` means no recipes/<slug>.md; otherwise that file is the recipe
    problems: tuple


@dataclass
class CoverageReport:
    rows: list
    unmatched_recipes: list
    tier: Optional[str] = None  # the `--tier` scope this report was computed for

    def tally(self) -> dict[str, dict[str, int]]:
        """Count each row once under each of its tiers, or only under `tier` when scoped."""
        out = {}
        for r in self.rows:
            for tier in ((self.tier,) if self.tier else r.tiers):
                t = out.setdefault(tier, {s: 0 for s in STATES})
                t[r.state] += 1
        return out

    def below(self, level: str) -> list[CoverageRow]:
        return [r for r in self.rows if _RANK[r.state] < _RANK[level]]


def collision(items: list[Component], config: Config) -> Optional[str]:
    """A name shared by same-platform sources in more than one tier, or None.

    Those are almost always two unrelated components that happen to share a
    file stem, and one recipe cannot specify both. Sources on different
    platforms (the Swift and TypeScript button) are the intended cross-platform
    merge, and sources in one tier (iOS and macOS twins) are one component. A
    path a `renames` key covers is named on purpose, so renaming both sides to
    this name records a deliberate merge.
    """
    tiers_by_platform = {}
    for c in items:
        if config.renamed(c.path) is None:
            tiers_by_platform.setdefault(c.platform, set()).add(c.tier)
    spans = [f"{p} in {', '.join(sorted(t))}" for p, t in sorted(tiers_by_platform.items())
             if len(t) > 1]
    if not spans:
        return None
    return (f"name collision across tiers ({'; '.join(spans)}): give one side its own name "
            f"in `.cookr.json` `renames`, or list every path there under this name to merge "
            f"them on purpose")


def compute(config: Config, tier: Optional[str] = None,
            checks: Optional[frozenset[str]] = None) -> CoverageReport:
    """One row per component `name`, across every tier the name appears in.

    Each row carries `slug`, the recipe stem the name resolves to through
    `aliases`, even when no recipe exists yet: two aliased names that share a
    slug want one recipe, and a caller writing one brief per recipe needs to
    see that before the file exists.

    `tier` filters the rows that are returned (and graded); it never narrows
    the corpus the rows are matched against, so `unmatched_recipes` is the same
    list either way.

    A name collision (see `collision`) is a problem on its row: a matched row
    grades `partial` until the config resolves it.

    `checks` is the compliance catalog (`compliance.load_checks`); None skips
    the unknown-citation check.
    """
    corpus = load_corpus(config.recipes_dir)

    grouped = {}
    for c in scan(config):
        grouped.setdefault(c.name, []).append(c)

    # a recipe's platforms are judged against every component it covers, aliases included
    platforms_by_slug = {}
    for name, items in grouped.items():
        platforms_by_slug.setdefault(config.aliases.get(name, name), set()).update(i.platform for i in items)

    graded = {}  # slug -> problems(); aliased names share one grade
    matched_slugs = set()
    rows = []
    for name, items in sorted(grouped.items()):
        slug = config.aliases.get(name, name)
        info = corpus.get(slug)
        if info is not None:
            matched_slugs.add(slug)
        tiers = tuple(sorted({i.tier for i in items}))
        if tier is not None and tier not in tiers:
            continue
        clash = collision(items, config)
        probs = (clash,) if clash else ()
        if info is None:
            state = "missing"
        else:
            if slug not in graded:
                stem = info.path.relative_to(config.recipes_dir).with_suffix("").as_posix()
                graded[slug] = tuple(problems(info, checks, platforms_by_slug[slug],
                                              config.domain(stem)))
            probs = graded[slug] + probs
            state = "partial" if probs else "complete"
        rows.append(CoverageRow(
            name=name,
            slug=slug,
            tiers=tiers,
            platforms=tuple(sorted({i.platform for i in items})),
            paths=tuple(sorted(i.path for i in items)),
            state=state, problems=probs,
        ))

    unmatched = sorted(s for s in corpus if s not in matched_slugs)
    return CoverageReport(rows=rows, unmatched_recipes=unmatched, tier=tier)
