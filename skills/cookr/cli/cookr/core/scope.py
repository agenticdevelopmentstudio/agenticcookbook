"""`cookr scope`: which recipes and ingredients a change touches (spec section 6).

minimum   the owner of each touched file plus the owners' direct recipe and
          ingredient dependencies, across cookbooks.
further   dependencies beyond the first level (informational).
siblings  recipes and ingredients outside the minimum that share a direct
          dependency with a minimum item.
uncovered touched files inside a root that no entry owns.

Only recipes and ingredients are walked; guidelines, principles and checks in
`depends-on` are rules, not code, and never enter the result. A dependency that
cannot be resolved is listed with state `missing` or `unreachable`, never dropped.
A dependency in another cookbook is a leaf: its own dependencies live in its repo,
so it adds nothing to further or siblings.

`ScopeItem.via` means two things. In `minimum` and `further` it names the item that
depends on this one. In `siblings` it names the shared dependency that makes the
item a sibling.

States: a conformance state, `unplaced` (no implementations), `missing` (a link to an
artifact absent from its index), `unresolvable` (a malformed link, shown by its raw
text) or `unreachable` (a dependency in a cookbook that cannot be reached).
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional

from .changes import Change, split_rename
from .conformance import current_hash, entry_version, is_missing, recipe_state, stored_state
from .index import Entry, Index
from .inventory import ignored_for
from .links import Link, Resolved, Resolver, format_link, parse_link
from .markdown import VERSIONS_DIR
from .recipes import load_corpus
from .repoconfig import Config

WALKED = ("recipe", "ingredient")


@dataclass
class ScopeItem:
    id: str
    rdid: str
    state: str
    via: Optional[str] = None


@dataclass
class Scope:
    minimum: list[ScopeItem] = field(default_factory=list)
    further: list[ScopeItem] = field(default_factory=list)
    siblings: list[ScopeItem] = field(default_factory=list)
    uncovered: list[str] = field(default_factory=list)


def resolve_dependency(resolver: Resolver, own_id: str, link: Link) -> tuple[bool, Resolved]:
    """(is it in this cookbook, what the link reaches). The one place a depends-on
    link is classified: ok, missing or unreachable."""
    local = link.cookbook is None or link.cookbook == own_id
    return local, resolver.resolve(Link(None, link.artifact) if local else link)


def link_state(resolver: Resolver, own_id: str, raw: str) -> str:
    """A raw depends-on value as ok, missing, unreachable, or unresolvable (malformed)."""
    try:
        link = parse_link(raw)
    except ValueError:
        return "unresolvable"
    return resolve_dependency(resolver, own_id, link)[1].state


@dataclass
class _Node:
    key: str            # link string: "<uuid>" or "<cookbook>/<uuid>"
    rdid: str
    state: str
    entry: Optional[Entry]
    own: bool


def in_frozen_version(config: Config, rel: str) -> bool:
    parts = rel.split("/")
    for i, name in enumerate(parts[:-1]):
        if name == VERSIONS_DIR and (config.repo_root / "/".join(parts[:i]) / "artifact.json").is_file():
            return True
    return False


def compute(config: Config, index: Index, resolver: Resolver, changes: list[Change],
            seeds: Optional[list[Entry]] = None) -> Scope:
    corpus = load_corpus(config.cookbook_dir, index)
    depends = {info.id: [str(v) for v in info.data.get("depends-on") or []]
               for info in corpus.values()}
    own_id = index.cookbook.id

    def own_state(entry: Entry) -> str:
        version = entry_version(config.cookbook_dir, entry)
        return recipe_state(entry, version, lambda i: current_hash(config, i),
                            lambda i: is_missing(config, i))

    def node_for(link: Link) -> Optional[_Node]:
        """The node a link reaches. An unresolved link becomes a node with state
        missing/unreachable; a kind that is not walked gives None."""
        local, res = resolve_dependency(resolver, own_id, link)
        key = link.artifact if local else format_link(link)
        if res.state != "ok":
            return _Node(key, key, res.state, None, local)
        entry = res.entry
        if entry.kind not in WALKED:
            return None
        return _Node(key, entry.rdid, own_state(entry) if local else stored_state(entry),
                     entry, local)

    def direct(node: _Node) -> list[_Node]:
        if not node.own or node.entry is None:
            return []
        out = []
        for raw in depends.get(node.entry.id, []):
            try:
                n = node_for(parse_link(raw))
            except ValueError:
                n = _Node(raw, raw, "unresolvable", None, True)
            if n is not None:
                out.append(n)
        return out

    # --- touched files -> owners ---------------------------------------------
    paths: dict[str, Optional[str]] = {}    # touched path -> where it was renamed from
    sources: set[str] = set()               # old sides of in-root renames
    for change in changes:
        for c in split_rename(change, lambda p: config.root_for(p) is not None):
            paths.setdefault(c.path, c.old_path if c.status == "R" else None)
            if c.status == "R" and c.old_path:
                paths.setdefault(c.old_path, None)
                sources.add(c.old_path)
    owners: dict[str, Entry] = {e.id: e for e in seeds or []}
    uncovered: set[str] = set()
    for path, old in paths.items():
        if in_frozen_version(config, path):
            continue
        found = index.owners(path) or (index.owners(old) if old else [])
        for entry, _impl in found:
            owners[entry.id] = entry
        if found or path in sources:
            continue                         # the old side of a rename: its new path decides
        root = config.root_for(path)
        if root is not None and not ignored_for(config, root).ignores(path):
            uncovered.add(path)
    scope = Scope(uncovered=sorted(uncovered))

    # --- minimum -------------------------------------------------------------
    minimum: dict[str, ScopeItem] = {}
    min_nodes: list[_Node] = []
    for entry in sorted((e for e in owners.values() if e.kind in WALKED), key=lambda e: e.rdid):
        n = _Node(entry.id, entry.rdid, own_state(entry), entry, True)
        minimum[n.key] = ScopeItem(n.key, n.rdid, n.state)
        min_nodes.append(n)
    first_level: list[_Node] = []
    for owner in list(min_nodes):
        for dep in direct(owner):
            if dep.key not in minimum:
                minimum[dep.key] = ScopeItem(dep.key, dep.rdid, dep.state, owner.rdid)
                min_nodes.append(dep)
                first_level.append(dep)
    scope.minimum = list(minimum.values())

    # --- further: levels beyond the first ------------------------------------
    further: dict[str, ScopeItem] = {}
    visited = set(minimum)
    frontier = first_level
    while frontier:
        nxt: list[_Node] = []
        for node in frontier:
            for dep in direct(node):
                if dep.key not in visited:
                    visited.add(dep.key)
                    further[dep.key] = ScopeItem(dep.key, dep.rdid, dep.state, node.rdid)
                    nxt.append(dep)
        frontier = nxt
    scope.further = list(further.values())

    # --- siblings ------------------------------------------------------------
    shared = {d.key for n in min_nodes for d in direct(n)}
    for entry in sorted(index.entries.values(), key=lambda e: e.rdid):
        if entry.kind not in WALKED or entry.id in minimum:
            continue
        common = sorted(d.rdid for d in direct(_Node(entry.id, entry.rdid, "", entry, True))
                        if d.key in shared)
        if common:
            scope.siblings.append(ScopeItem(entry.id, entry.rdid, own_state(entry), common[0]))
    return scope
