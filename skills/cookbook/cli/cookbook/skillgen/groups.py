"""Assign each doc to a router skill, and fold identical duplicates.

A router's NAME is its whole routing signal: a `claude -p` worker sees skill
names only, never descriptions. So names are `<verb>-<domain>`, never ids.
"""

from __future__ import annotations

import hashlib
import re
from collections import Counter, defaultdict
from dataclasses import dataclass, field, replace
from typing import Callable

from .source import Doc

# guidelines/<use-case>/… → the verb its router is named with.
USE_CASE_VERBS = {
    "reviewing": "review",
    "implementing": "implement",
    "planning": "plan",
    "testing": "test",
    "researching": "research",
    "brainstorming": "brainstorm",
    "shipping": "ship",
    "storytelling": "story",
    "cookbook": "cookbook",
}

# Top-level cookbook dirs that hold rules, each one router (plus recipes,
# which get one router per category).
SINGLE_ROUTER_DIRS = {
    "principles": "principles",
    "ingredients": "ingredients",
    "compliance": "compliance",
}

# Top-level cookbook dirs that describe the cookbook rather than rule on code.
NOT_RULE_CONTENT = ("appendix", "introduction", "reference", "workflows")

# recipes layout: a name prefix becomes a router once this many docs share it.
MIN_PREFIX_GROUP = 4

NAME_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")


def slugify(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")


@dataclass(frozen=True)
class Placement:
    router: str
    verb: str
    domain: str
    stem: str
    dedup_key: str = ""


@dataclass
class Grouping:
    placements: dict[str, Placement] = field(default_factory=dict)  # doc rel → placement
    aliases: dict[str, str] = field(default_factory=dict)  # duplicate doc rel → canonical doc rel
    skipped: list[tuple[str, str]] = field(default_factory=list)
    drift: list[tuple[str, list[str]]] = field(default_factory=list)  # tail → rels whose bodies differ


def _cookbook_placement(doc: Doc) -> Placement | str:
    parts = doc.rel.with_suffix("").parts
    head = parts[0]
    if head == "guidelines" and len(parts) >= 3:
        use_case = parts[1]
        verb = USE_CASE_VERBS.get(use_case)
        if verb is None:
            return f"unknown use case {use_case!r}"
        if len(parts) == 3:
            return Placement(f"{verb}-general", verb, "general", slugify(parts[2]))
        domain = parts[2]
        return Placement(
            f"{verb}-{slugify(domain)}", verb, domain,
            slugify("-".join(parts[3:])), dedup_key="/".join(parts[2:]),
        )
    if head == "recipes":
        category = parts[1] if len(parts) >= 3 else "general"
        rest = parts[2:] if len(parts) >= 3 else parts[1:]
        return Placement(f"recipes-{slugify(category)}", "recipes", category, slugify("-".join(rest)))
    if head in SINGLE_ROUTER_DIRS:
        name = SINGLE_ROUTER_DIRS[head]
        return Placement(name, name, name, slugify("-".join(parts[1:])))
    if head in NOT_RULE_CONTENT:
        return f"{head}/ is not rule content"
    return f"no router for top-level dir {head!r}"


def _prefix_routers(docs: list[Doc]) -> dict[str, str]:
    """recipes layout: map each doc to the longest name prefix it shares widely.

    Two-token prefixes first (`status-server`), then one token (`extension`),
    else `general`. Deterministic: a pure function of the set of names.
    """
    stems = [d.rel.stem for d in docs]
    two = Counter("-".join(s.split("-")[:2]) for s in stems if s.count("-") >= 2)
    one = Counter(s.split("-")[0] for s in stems if "-" in s)
    out = {}
    for stem in stems:
        tokens = stem.split("-")
        if len(tokens) >= 3 and two["-".join(tokens[:2])] >= MIN_PREFIX_GROUP:
            out[stem] = "-".join(tokens[:2])
        elif len(tokens) >= 2 and one[tokens[0]] >= MIN_PREFIX_GROUP:
            out[stem] = tokens[0]
        else:
            out[stem] = "general"
    return out


def _split_router(name: str, rels: list[str], placements: dict[str, Placement],
                  cost: Callable[[str], int], budget: int, taken: set[str]) -> dict[str, Placement]:
    """New placements for an over-budget router's docs, or {} if it cannot split.

    First by a shared leading stem token (`status-web` → `status-web-server`,
    the token dropped from the stem), then by a shared trailing token
    (`general` → `general-view`, the stem kept whole), then into alphabetical
    runs (`general-1`, `general-2`, …) that each fit the budget.
    """
    base = placements[rels[0]]
    stems = {r: placements[r].stem for r in rels}

    def child(token: str) -> tuple[str, str]:
        return f"{name}-{token}", f"{base.domain}-{token}"

    for position in (0, -1):
        tokens = Counter(s.split("-")[position] for s in stems.values() if "-" in s)
        # A token every doc shares moves them all into one child: a rename, not a split.
        picks = sorted(t for t, n in tokens.items()
                       if MIN_PREFIX_GROUP <= n < len(rels) and child(t)[0] not in taken)
        if not picks:
            continue
        out = {}
        for rel, stem in stems.items():
            token = stem.split("-")[position] if "-" in stem else ""
            if token in picks:
                router, domain = child(token)
                new_stem = stem.split("-", 1)[1] if position == 0 else stem
                out[rel] = replace(placements[rel], router=router, domain=domain, stem=new_stem)
        return out

    runs: list[list[str]] = [[]]
    for rel in sorted(rels, key=lambda r: stems[r]):
        if runs[-1] and sum(cost(r) for r in runs[-1]) + cost(rel) > budget:
            runs.append([])
        runs[-1].append(rel)
    if len(runs) < 2:
        return {}
    out = {}
    for i, run in enumerate(runs, start=1):
        router, domain = child(str(i))
        for rel in run:
            out[rel] = replace(placements[rel], router=router, domain=domain)
    return out


def refine(placements: dict[str, Placement], cost: Callable[[str], int], budget: int) -> dict[str, Placement]:
    """Split every router whose index would cost more than `budget` characters
    (the sum of `cost(rel)` over its docs) until each fits or cannot split.
    Deterministic: routers are visited in name order, docs in path order."""
    out = dict(placements)
    pending = sorted({p.router for p in out.values()})
    while pending:
        name = pending.pop(0)
        rels = sorted(r for r, p in out.items() if p.router == name)
        if not rels or sum(cost(r) for r in rels) <= budget:
            continue
        taken = {p.router for p in out.values()}
        moved = _split_router(name, rels, out, cost, budget, taken)
        if not moved:
            continue
        out.update(moved)
        pending = sorted(set(pending) | {name} | {p.router for p in moved.values()})
    return out


def _normalized_hash(body: str) -> str:
    body = re.split(r"\n## Change History\b", body, maxsplit=1)[0]
    return hashlib.sha256(" ".join(body.split()).encode("utf-8")).hexdigest()


def group(docs: list[Doc], layout: str) -> Grouping:
    result = Grouping()
    if layout == "recipes":
        prefixes = _prefix_routers(docs)
        for doc in docs:
            prefix = prefixes[doc.rel.stem]
            stem = doc.rel.stem
            if prefix != "general" and stem.startswith(prefix + "-"):
                stem = stem[len(prefix) + 1:]
            result.placements[doc.rel.as_posix()] = Placement(
                f"implement-{prefix}", "implement", prefix, slugify(stem)
            )
        return result

    by_key: dict[str, list[Doc]] = defaultdict(list)
    for doc in docs:
        placed = _cookbook_placement(doc)
        if isinstance(placed, str):
            result.skipped.append((doc.rel.as_posix(), placed))
            continue
        result.placements[doc.rel.as_posix()] = placed
        if placed.dedup_key:
            by_key[placed.dedup_key].append(doc)

    # The same guideline often appears under several use cases. Identical
    # bodies are emitted once (the first by path) and aliased from the other
    # routers; differing bodies are drift, emitted separately and reported.
    for key in sorted(by_key):
        group_docs = sorted(by_key[key], key=lambda d: d.rel.as_posix())
        if len(group_docs) < 2:
            continue
        hashes = defaultdict(list)
        for d in group_docs:
            hashes[_normalized_hash(d.body)].append(d.rel.as_posix())
        if len(hashes) > 1:
            result.drift.append((key, [d.rel.as_posix() for d in group_docs]))
        for rels in hashes.values():
            for dup in rels[1:]:
                result.aliases[dup] = rels[0]
    return result
