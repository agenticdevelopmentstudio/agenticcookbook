"""Join the source inventory against the spec corpus."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from cookbook.core import refimpl

from .completeness import problems
from .config import Config
from .inventory import Component, in_group, scan
from .recipes import RecipeInfo, load_corpus

STATES = ("missing", "partial", "complete")
_RANK = {s: i for i, s in enumerate(STATES)}


@dataclass(frozen=True)
class CoverageRow:
    name: str  # the spec's path in the cookbook, without `.md`, whether or not it exists yet
    tiers: tuple
    platforms: tuple
    paths: tuple
    state: str  # `missing` means no cookbook/<name>.md; otherwise that file is the spec
    problems: tuple


@dataclass
class CoverageReport:
    rows: list
    unmatched_recipes: list
    tier: Optional[str] = None  # the `--tier` scope this report was computed for

    def tally(self) -> dict[str, dict[str, int]]:
        """Count each row under its top-level group, or only under `tier` when scoped."""
        out = {}
        for r in self.rows:
            for tier in ((self.tier,) if self.tier else r.tiers):
                t = out.setdefault(tier, {s: 0 for s in STATES})
                t[r.state] += 1
        return out

    def below(self, level: str) -> list[CoverageRow]:
        return [r for r in self.rows if _RANK[r.state] < _RANK[level]]


def collision(items: list[Component], config: Config) -> Optional[str]:
    """Why the sources of one row cannot share one spec, or None.

    Unclaimed sources on one platform from different roots that land on one
    name are almost always two unrelated components that happen to share a
    directory and stem. A source two specs claim at once belongs to neither.
    """
    out = []
    roots_by_platform = {}
    for c in items:
        if not c.claimed:
            root = config.root_for(c.path)
            roots_by_platform.setdefault(c.platform, set()).add(root.path if root else "")
    spans = [f"{p} in {', '.join(sorted(r))}" for p, r in sorted(roots_by_platform.items())
             if len(r) > 1]
    if spans:
        out.append(f"name collision across roots ({'; '.join(spans)}): write a spec for one "
                   f"side under another name and claim its file in `## Reference Implementations`")
    return "; ".join(out) or None


def claim_problems(info: RecipeInfo, items: list[Component], config: Config,
                   claimed_by: dict[str, list[str]]) -> list[str]:
    """What the spec's Reference Implementations gets wrong about its sources."""
    out = []
    for impl in info.implementations:
        if impl.platform not in refimpl.PLATFORMS:
            out.append(f"Reference Implementations platform `{impl.platform}` is not one of "
                       f"{', '.join(refimpl.PLATFORMS)}")
        target = config.repo_root / impl.path
        if not (target.is_dir() if impl.is_dir else target.is_file()):
            out.append(f"Reference Implementations path `{impl.path}` does not exist"
                       + (" as a directory" if impl.is_dir and target.exists() else ""))
    for c in items:
        if not c.claimed:
            out.append(f"Reference Implementations does not list `{c.path}` ({c.platform})")
        elif len(claimed_by.get(c.path, ())) > 1:
            others = [s for s in claimed_by[c.path] if s != info.slug]
            out.append(f"`{c.path}` is also claimed by {', '.join(others)}")
    return out


def compute(config: Config, tier: Optional[str] = None,
            checks: Optional[frozenset[str]] = None,
            corpus: Optional[dict[str, RecipeInfo]] = None) -> CoverageReport:
    """One row per spec name that has sources.

    `tier` filters the rows that are returned (and graded) to one group of the
    cookbook; it never narrows the corpus the rows are matched against, so
    `unmatched_recipes` is the same list either way.

    A matched row grades `partial` while its spec has completeness problems, a
    Reference Implementations row that names nothing, a source it does not
    list, or a source another spec claims too.

    `checks` is the compliance catalog (`compliance.load_checks`); None skips
    the unknown-citation check.
    """
    corpus = load_corpus(config.cookbook_dir) if corpus is None else corpus
    components = scan(config, corpus)

    grouped: dict[str, list[Component]] = {}
    claimed_by: dict[str, list[str]] = {}
    for c in components:
        grouped.setdefault(c.name, []).append(c)
        if c.claimed:
            claimed_by.setdefault(c.path, []).append(c.name)

    rows = []
    for name, items in sorted(grouped.items()):
        if not in_group(name, tier):
            continue
        info = corpus.get(name)
        clash = collision(items, config)
        probs = (clash,) if clash else ()
        platforms = {i.platform for i in items}
        if info is None:
            state = "missing"
        else:
            probs = tuple(problems(info, checks, platforms, config.domain(name))) + tuple(
                claim_problems(info, items, config, claimed_by)) + probs
            state = "partial" if probs else "complete"
        rows.append(CoverageRow(
            name=name,
            tiers=(name.split("/", 1)[0],),
            platforms=tuple(sorted(platforms)),
            paths=tuple(sorted(i.path for i in items)),
            state=state, problems=probs,
        ))

    unmatched = sorted(s for s in corpus if s not in grouped)
    return CoverageReport(rows=rows, unmatched_recipes=unmatched, tier=tier)
