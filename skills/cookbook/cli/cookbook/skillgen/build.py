"""Build a plugin in memory, gate it, then write it or check it for drift."""

from __future__ import annotations

import json
import shutil
from collections import Counter
from dataclasses import dataclass, field
from pathlib import Path

from . import emit, gates, groups, leaves, rules, source

MANAGED_MARKER = "manifest.json"


@dataclass
class Warning_:
    kind: str
    where: str
    detail: str


@dataclass
class Build:
    files: dict[str, str] = field(default_factory=dict)
    errors: list[str] = field(default_factory=list)
    warnings: list[Warning_] = field(default_factory=list)
    docs: int = 0
    routers: int = 0
    leaves: int = 0
    rules: int = 0


def _leaf_id(router: str, stem: str, suffix: str) -> str:
    return f"{router}/{stem}--{suffix}" if suffix else f"{router}/{stem}"


MIN_BUDGET = 2_000


def _doc_leaves(doc: source.Doc, place: groups.Placement, cap: int) -> list[emit.Leaf]:
    """One doc's leaves, re-split with a smaller text budget until every
    rendered leaf (text plus its rule checklist) fits the cap."""
    rel = doc.rel.as_posix()
    budget = cap - leaves.HEADER_ROOM
    while True:
        seen: Counter = Counter()
        made = []
        for part in leaves.split(doc.body, doc.type, cap, rel, budget):
            leaf_id = _leaf_id(place.router, place.stem, part.suffix)
            made.append(emit.Leaf(
                id=leaf_id,
                router=place.router,
                path=f"skills/{leaf_id.replace('/', '/leaves/', 1)}.md",
                source=rel,
                source_hash=doc.source_hash,
                title=doc.title,
                heading=part.heading,
                summary=doc.summary,
                doc_type=doc.type,
                domain=doc.domain,
                section=part.suffix,
                body=part.text,
                platforms=doc.platforms,
                triggers=doc.triggers,
                tags=doc.tags,
                globs=doc.globs,
                files=doc.files,
                rules=rules.extract(part.text, seen),
                vectors=rules.test_vectors(part.text),
            ))
        over = max(len(emit.render_leaf(leaf)) for leaf in made) - cap
        if over <= 0:
            return made
        budget -= over + 200
        if budget < MIN_BUDGET:
            raise leaves.LeafTooLarge(f"{rel}: its rule checklist alone overflows the {cap}-char leaf cap")


def _made_leaves(docs: dict[str, source.Doc], grouping: groups.Grouping,
                 cap: int) -> dict[str, list[emit.Leaf] | str]:
    """Each canonical doc's leaves under its current placement, or the error
    that stopped them."""
    made: dict[str, list[emit.Leaf] | str] = {}
    for rel in sorted(grouping.placements):
        if rel in grouping.aliases:
            continue
        try:
            made[rel] = _doc_leaves(docs[rel], grouping.placements[rel], cap)
        except leaves.LeafTooLarge as e:
            made[rel] = str(e)
    return made


def compile_source(src: source.Source, cap: int = leaves.DEFAULT_CAP) -> Build:
    build = Build()
    loaded = source.load(src)
    for rel, reason in loaded.skipped:
        build.warnings.append(Warning_("skipped", rel, reason))
    grouping = groups.group(loaded.docs, src.layout)
    for rel, reason in grouping.skipped:
        build.warnings.append(Warning_("skipped", rel, reason))
    for tail, rels in grouping.drift:
        build.warnings.append(Warning_("drift", tail, "bodies differ: " + ", ".join(rels)))

    docs = {d.rel.as_posix(): d for d in loaded.docs}
    routers: dict[str, emit.Router] = {}
    all_leaves: dict[str, emit.Leaf] = {}
    doc_leaves: dict[str, list[str]] = {}

    made = _made_leaves(docs, grouping, cap)
    # Split any router whose one-line-per-doc index would outgrow the budget,
    # measured on the lines the first placement renders; the margin covers the
    # small change in a line's length when its doc moves router.
    def cost(rel: str) -> int:
        leaves_of = made.get(grouping.aliases.get(rel, rel))
        if not isinstance(leaves_of, list) or not leaves_of:
            return 0
        place = grouping.placements[rel]
        return len(emit.index_line(emit.Router(place.router, place.verb, place.domain), leaves_of)) + 1

    refined = groups.refine(grouping.placements, cost, int(emit.INDEX_BUDGET * 0.9))
    if refined != grouping.placements:
        grouping.placements = refined
        made = _made_leaves(docs, grouping, cap)

    for rel in sorted(made):
        doc, result = docs[rel], made[rel]
        if isinstance(result, str):
            build.errors.append(result)
            continue
        ids = []
        for leaf in result:
            if leaf.id in all_leaves:
                build.errors.append(f"{rel}: leaf id {leaf.id} collides with {all_leaves[leaf.id].source}")
                continue
            all_leaves[leaf.id] = leaf
            ids.append(leaf.id)
        # Principles are heuristics written as prose; only rule-bearing types should carry keywords.
        if doc.type != "principle" and not any(all_leaves[i].rules for i in ids):
            build.warnings.append(Warning_("no-rules", rel, "no MUST/SHOULD/MAY statement found"))
        doc_leaves[rel] = ids

    for rel in sorted(grouping.placements):
        place = grouping.placements[rel]
        ids = doc_leaves.get(grouping.aliases.get(rel, rel), [])
        router = routers.setdefault(place.router, emit.Router(place.router, place.verb, place.domain))
        for leaf_id in ids:
            if leaf_id not in router.leaves:
                router.leaves.append(leaf_id)
            if place.router not in all_leaves[leaf_id].routers:
                all_leaves[leaf_id].routers.append(place.router)

    for name in sorted(routers):
        if routers[name].verb == "review":
            domain = routers[name].domain
            verify = f"verify-{name.removeprefix('review-')}"
            routers[verify] = emit.Router(verify, "verify", domain, list(routers[name].leaves), index_of=name)
            for leaf_id in routers[name].leaves:
                all_leaves[leaf_id].routers.append(verify)

    for name in sorted(routers):
        router = routers[name]
        router.leaves.sort()
        build.files[f"skills/{name}/SKILL.md"] = emit.render_router(router, all_leaves)
        if not router.index_of:
            build.files[router.index_path] = emit.render_index(router, all_leaves)
    for leaf in all_leaves.values():
        build.files[leaf.path] = emit.render_leaf(leaf)
    build.files["manifest.json"] = emit.manifest(src.name, src.layout, src.code_roots, routers, all_leaves)
    build.files[".claude-plugin/plugin.json"] = emit.plugin_json(src.name, src.layout)

    build.errors += gates.run_all(build.files, cap)
    build.docs = len(doc_leaves)
    build.routers = len(routers)
    build.leaves = len(all_leaves)
    build.rules = sum(len(l.rules) for l in all_leaves.values())
    return build


def build(src: source.Source, cap: int = leaves.DEFAULT_CAP) -> Build:
    """Compile twice and fail unless both runs produce the same bytes."""
    first = compile_source(src, cap)
    second = compile_source(src, cap)
    if first.files != second.files:
        changed = sorted(p for p in set(first.files) | set(second.files) if first.files.get(p) != second.files.get(p))
        first.errors.append("output is not byte-stable across two builds: " + ", ".join(changed[:10]))
    return first


def read_tree(out: Path) -> dict[str, str]:
    if not out.is_dir():
        return {}
    return {
        p.relative_to(out).as_posix(): p.read_text(encoding="utf-8")
        for p in sorted(out.rglob("*"))
        if p.is_file() and ".git" not in p.relative_to(out).parts
    }


def drift(expected: dict[str, str], actual: dict[str, str]) -> list[tuple[str, str]]:
    out = []
    for path in sorted(set(expected) | set(actual)):
        if path not in actual:
            out.append(("missing", path))
        elif path not in expected:
            out.append(("extra", path))
        elif expected[path] != actual[path]:
            out.append(("changed", path))
    return out


class RefusedOutput(Exception):
    pass


def _owned(out: Path) -> bool:
    marker = out / MANAGED_MARKER
    if not marker.is_file():
        return False
    try:
        return json.loads(marker.read_text(encoding="utf-8")).get("generator") == emit.GENERATOR
    except (json.JSONDecodeError, AttributeError):
        return False


def write(out: Path, files: dict[str, str]) -> None:
    """Replace `out` with `files`. Refuses a non-empty dir this generator does not own."""
    if out.exists() and any(out.iterdir()) and not _owned(out):
        raise RefusedOutput(f"{out} is not empty and has no {MANAGED_MARKER} from `{emit.GENERATOR}`; refusing to overwrite it")
    if out.exists():
        for child in out.iterdir():
            if child.name == ".git":
                continue
            shutil.rmtree(child) if child.is_dir() else child.unlink()
    for rel, text in sorted(files.items()):
        path = out / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
