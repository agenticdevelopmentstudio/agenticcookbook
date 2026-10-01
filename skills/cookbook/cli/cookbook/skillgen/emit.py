"""Render the plugin's files: router SKILL.md, index.md, leaves, manifest.

Every renderer is a pure function of its inputs, with sorted iteration, so
two builds of the same source are byte-identical.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field

from .rules import Rule, TestVector

DESCRIPTION_BUDGET = 250
MANIFEST_SCHEMA = 1
GENERATOR = "cookbook skills build"

VERB_PHRASES = {
    "review": "Review code for",
    "verify": "Verify a review's findings on",
    "implement": "Implement",
    "plan": "Plan",
    "test": "Test",
    "research": "Research",
    "brainstorm": "Brainstorm",
    "ship": "Ship",
    "story": "Tell the story of",
    "cookbook": "Maintain the cookbook's",
    "recipes": "Build to the recipes for",
    "principles": "Apply the design principles",
    "ingredients": "Build to the ingredients",
    "compliance": "Check compliance",
}

PROCEDURES = {
    "review": """\
Review the change against the rules in the leaves that apply to it.

1. Read `index.md` and pick the leaves whose summary, platforms and triggers
   match the files under review. Read only those.
2. Each leaf opens with its rule checklist. For **every** rule in every leaf
   you read, report exactly one status:
   - `violated` — with `file:line` evidence and what the rule requires;
   - `clean` — the change complies;
   - `n/a` — with the reason it does not apply.
3. Cite a rule as `<leaf-id>#<slug>`, e.g. `{example}`.
""",
    "verify": """\
Verify a worker's review against the same rules it used.

1. The rules are the leaves of `{review}`: read `../{review}/index.md` and the
   leaves the worker cited or should have.
2. For each `violated` finding: is the violation real in the code, and does it
   cite the rule that it breaks? Reject what fails either test.
3. For each `clean` claim on a MUST rule: is it plausible from the code? Flag
   the ones that are not.
4. A rule the worker gave no status is a coverage gap; report it.
""",
    "implement": """\
Build to the rules in the leaves that apply to what you are writing.

1. Read `index.md` and pick the leaves that match the files and component at
   hand. Read only those.
2. Satisfy every MUST. Follow every SHOULD, or record why not. MAY is your call.
3. Cite a rule as `<leaf-id>#<slug>` when you explain a choice.
""",
}
DEFAULT_PROCEDURE = """\
Apply the rules in the leaves that fit the task.

1. Read `index.md` and pick the leaves that match. Read only those.
2. Each leaf opens with its rule checklist: MUST is required, SHOULD is the
   default unless you record why not, MAY is optional.
3. Cite a rule as `<leaf-id>#<slug>`.
"""


@dataclass
class Leaf:
    id: str
    router: str
    path: str
    source: str
    source_hash: str
    title: str
    heading: str
    summary: str
    doc_type: str
    domain: str
    section: str
    body: str
    platforms: list[str]
    triggers: list[str]
    tags: list[str]
    globs: list[str]
    files: list[str]
    rules: list[Rule] = field(default_factory=list)
    vectors: list[TestVector] = field(default_factory=list)
    routers: list[str] = field(default_factory=list)
    # Other source docs whose body was identical and were folded into this
    # leaf (a reviewing copy of an implementing guideline). A consumer that
    # names a doc by path finds its leaf through these as well as `source`.
    aliases: list[str] = field(default_factory=list)


@dataclass
class Router:
    name: str
    verb: str
    domain: str
    leaves: list[str] = field(default_factory=list)  # leaf ids, including aliased ones
    index_of: str = ""  # verify routers read another router's index

    @property
    def index_path(self) -> str:
        return f"skills/{self.index_of or self.name}/index.md"


def _truncate(text: str, budget: int) -> str:
    if len(text) <= budget:
        return text
    cut = text[: budget - 2].rsplit(" ", 1)[0].rstrip(",;: ")
    return cut + " …"


def description(router: Router, leaves: dict[str, Leaf]) -> str:
    domain = router.domain.replace("-", " ")
    phrase = VERB_PHRASES.get(router.verb, router.verb.capitalize())
    head = f"{phrase} {domain}" if router.verb not in ("principles", "ingredients", "compliance") else phrase
    if router.verb == "verify":
        return _truncate(
            f"{phrase} {domain}: check each finding against the rules in {router.index_of}.",
            DESCRIPTION_BUDGET,
        )
    titles = []
    for leaf_id in router.leaves:
        title = leaves[leaf_id].title
        if title not in titles:
            titles.append(title)
    return _truncate(f"{head}. Covers: {', '.join(titles)}.", DESCRIPTION_BUDGET)


def _yaml_str(text: str) -> str:
    return json.dumps(text, ensure_ascii=False)


def render_router(router: Router, leaves: dict[str, Leaf]) -> str:
    example = f"{router.leaves[0]}#<slug>" if router.leaves else "<leaf-id>#<slug>"
    procedure = PROCEDURES.get(router.verb, DEFAULT_PROCEDURE).format(
        example=example, review=router.index_of
    )
    index_ref = f"../{router.index_of}/index.md" if router.index_of else "index.md"
    return (
        "---\n"
        f"name: {router.name}\n"
        f"description: {_yaml_str(description(router, leaves))}\n"
        "---\n\n"
        f"# {router.name}\n\n"
        f"{procedure}\n"
        f"Leaves: [{index_ref}]({index_ref}) — one line per leaf. Leaves are "
        "plain files, not skills; read them with the Read tool.\n"
    )


# A router's index is read whole by the worker before it picks a leaf.
INDEX_BUDGET = 12_000

def _rel(router: Router, leaf: Leaf) -> str:
    if leaf.router == router.name:
        return leaf.path.removeprefix(f"skills/{router.name}/")
    return "../" + leaf.path.removeprefix("skills/")


def index_line(router: Router, parts: list[Leaf]) -> str:
    """One line per source doc: its main leaf, then its split-out parts inline."""
    main = next((p for p in parts if not p.section), parts[0])
    levels = {"MUST": 0, "SHOULD": 0, "MAY": 0}
    for part in parts:
        for rule in part.rules:
            levels[rule.level] += 1
    counts = " ".join(f"{n} {lvl}" for lvl, n in levels.items() if n)
    vectors = sum(len(p.vectors) for p in parts)
    head = f"- [`{main.id}`]({_rel(router, main)}) — {main.title}"
    if main.heading:
        head += f" — {main.heading}"
    bits = [head]
    if main.summary:
        bits.append(main.summary)
    if main.platforms:
        bits.append("platforms: " + ", ".join(main.platforms))
    if main.triggers:
        bits.append("triggers: " + ", ".join(main.triggers))
    if counts:
        bits.append("rules: " + counts)
    if vectors:
        bits.append(f"test vectors: {vectors}")
    others = [p for p in parts if p is not main]
    if others:
        bits.append("parts: " + ", ".join(f"[{p.section or 'main'}]({_rel(router, p)})" for p in others))
    return " · ".join(bits)


def render_index(router: Router, leaves: dict[str, Leaf]) -> str:
    by_source: dict[str, list[Leaf]] = {}
    for leaf_id in router.leaves:
        leaf = leaves[leaf_id]
        by_source.setdefault(leaf.source, []).append(leaf)
    lines = [f"# {router.name} — leaves", ""]
    lines += [index_line(router, parts) for parts in by_source.values()]
    return "\n".join(lines) + "\n"


def render_leaf(leaf: Leaf) -> str:
    out = [f"<!-- leaf: {leaf.id} · source: {leaf.source} -->", ""]
    if leaf.heading:
        # A split-out section already opens with its own H2; don't repeat it in the H1.
        own_h2 = leaf.body.startswith(f"## {leaf.heading}\n")
        out += [f"# {leaf.title}" if own_h2 else f"# {leaf.title} — {leaf.heading}", ""]
    if leaf.rules:
        out.append("**Rules** (cite as `" + leaf.id + "#<slug>`):")
        out.append("")
        for rule in leaf.rules:
            line = f"- `{rule.slug}` {rule.level}"
            if rule.qualifier:
                line += f" ({rule.qualifier})"
            if not rule.explicit:
                line += f" — {rule.excerpt}"
            out.append(line)
        out.append("")
    # `out` ends with an empty entry, so this leaves one blank line before the body.
    return "\n".join(out) + "\n" + leaf.body


def manifest(plugin: str, layout: str, code_roots, routers: dict[str, Router], leaves: dict[str, Leaf]) -> str:
    data = {
        "generator": GENERATOR,
        "schema": MANIFEST_SCHEMA,
        "plugin": plugin,
        "layout": layout,
        "code_roots": list(code_roots),
        "routers": {
            name: {
                "verb": r.verb,
                "domain": r.domain,
                "skill": f"skills/{name}/SKILL.md",
                "index": r.index_path,
                "leaves": r.leaves,
            }
            for name, r in sorted(routers.items())
        },
        "leaves": {
            leaf_id: {
                "path": leaf.path,
                "router": leaf.router,
                "routers": sorted(leaf.routers),
                "source": leaf.source,
                "aliases": sorted(leaf.aliases),
                "source_hash": leaf.source_hash,
                "domain": leaf.domain,
                "type": leaf.doc_type,
                "title": leaf.title,
                "section": leaf.section,
                "summary": leaf.summary,
                "platforms": leaf.platforms,
                "triggers": leaf.triggers,
                "tags": leaf.tags,
                "globs": leaf.globs,
                "files": leaf.files,
                "rules": [
                    {"slug": r.slug, "level": r.level, "explicit": r.explicit, "qualifier": r.qualifier}
                    for r in leaf.rules
                ],
                "test_vectors": [{"id": v.id, "requirements": list(v.requirements)} for v in leaf.vectors],
            }
            for leaf_id, leaf in sorted(leaves.items())
        },
    }
    return json.dumps(data, indent=2, sort_keys=False, ensure_ascii=False) + "\n"


def plugin_json(plugin: str, layout: str) -> str:
    # "the cookbook", not "the cookbook cookbook"; "the agentictoolkit recipes".
    source = plugin if plugin == layout else f"{plugin} {layout}"
    data = {
        "name": plugin,
        "version": "1.0.0",
        "description": f"Routed rule skills generated from the {source} by `{GENERATOR}`.",
    }
    return json.dumps(data, indent=2) + "\n"
