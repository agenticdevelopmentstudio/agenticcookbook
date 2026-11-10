"""`cookr prompt extract` — the brief for writing one component's recipe.

A brief is assembled, in order: role header + module preamble, the bundled
guidelines (each under `## reference: guidelines/<path>`, frontmatter dropped,
Change History dropped), the non-UI guidance for a component from a `logic`
root, the selected template, the compliance check list (every check the
cookbook and its reachable dependencies define, as the link a citation uses),
the rendered action and `## Your task`, then every source file for the
component and the existing recipe if there is one. The component's code is
recorded in the cookbook index with `cookr implements`, never in the recipe. Embedded files are fenced with a
backtick run longer than any inside them, so their own fences stay inside.
No LLM is called here.

`extract <name>` builds one brief. `extract --tier <tier> --out-dir <dir>` is
the extraction worklist for a group of the cookbook: one brief per spec that
still needs a writer, written to `<dir>/<spec name>.md`. A recipe whose only
problem is its `NEEDS REVIEW` marker is finished work waiting on a reviewer, so
it is listed as awaiting review rather than handed back to a writer. The scan
and the corpus are read once for the whole tier.
"""

from __future__ import annotations

import argparse
import functools
import json
import re
import sys
from pathlib import Path
from typing import Optional

from cookr.core.frontmatter import parse_file
from cookr.core.history import h2_sections
from cookr.core.markdown import iter_markdown
from cookr.modules.prompt.render import render_template

from ...core.completeness import CHANGE_HISTORY, NEEDS_REVIEW
from ...core.compliance import check_links
from ...core.links import resolver_for
from ...core.repoconfig import Config
from ...core.coverage import compute
from ...core.inventory import Component, scan
from ...core.recipes import RecipeInfo, load_corpus
from ...core.templates import TYPES, template_path
from ..inventory import require_config, require_known_tier

NAME = "prompt"
HELP = "Assemble the extraction prompt for one component, or every brief a group still needs."

PROMPTS_DIR = Path(__file__).parent / "prompts"
EXTRACT_DIR = PROMPTS_DIR / "extract"
ACTIONS = ("extract",)
TO_WRITE = ("missing", "partial")
# The one problem that leaves a recipe finished but waiting on a reviewer.
AWAITING_REVIEW = (f"body carries a `{NEEDS_REVIEW}` marker",)


_BACKTICKS = re.compile(r"`+")


def references_dir() -> Path:
    """Materialised by ./install from prompts/extract/reference-manifest.json."""
    return EXTRACT_DIR / "references"


def register(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("paction", nargs="?", choices=ACTIONS, help="Omit to list the actions.")
    parser.add_argument("name", nargs="?",
                        help="Spec name: its path in the cookbook, or its last segment when unique.")
    parser.add_argument("--tier", default=None,
                        help="Every component in this group of the cookbook that still needs a writer "
                             "(requires --out-dir).")
    parser.add_argument("--out-dir", type=Path, default=None,
                        help="Write each brief to <dir>/<spec name>.md and print where, "
                             "instead of printing the brief.")
    parser.add_argument("--type", choices=TYPES, default=None,
                        help="Template to write against "
                             "(default: the existing recipe's type, else ingredient).")
    parser.add_argument("--json", action="store_true",
                        help="Report as JSON (the brief itself too, without --out-dir).")


# ---- embedded files ---------------------------------------------------------------------

def fenced(text: str, info: str = "") -> str:
    """`text` in a backtick fence longer than any backtick run inside it."""
    longest = max((len(run) for run in _BACKTICKS.findall(text)), default=0)
    fence = "`" * max(3, longest + 1)
    return f"{fence}{info}\n{text}\n{fence}"


def _without_change_history(body: str) -> str:
    history = dict(h2_sections(body)).get(CHANGE_HISTORY)
    if history is None:
        return body
    heading = rf"^ {{0,3}}## {re.escape(CHANGE_HISTORY)}[ \t#]*\r?\n"
    m = re.search(heading + re.escape(history), body, re.M)
    return body[:m.start()] + body[m.end():] if m else body


@functools.cache
def _guidelines(root: Path) -> str:
    """Every guideline under `root`, metadata and Change History dropped."""
    base = references_dir() / "guidelines"
    chunks = []
    for path in iter_markdown(root):
        fm = parse_file(path)
        body = _without_change_history(fm.body).strip()
        chunks.append(f"## reference: guidelines/{path.relative_to(base).as_posix()}\n\n{body}")
    return "\n\n".join(chunks)


def _checks(cfg: Config) -> str:
    """The checks a Compliance table may cite: the cookbook's own and every
    reachable dependency's, each as the in-text link a citation is written as."""
    resolver = resolver_for(cfg)
    links = check_links(resolver.own)
    for dep in sorted(cfg.dependencies):
        index = resolver.index_for(dep)
        if index is not None:
            links += check_links(index)
    if not links:
        return ""
    return ("## reference: compliance checks\n\n"
            "The Compliance table cites only these checks, each written exactly as listed:\n\n"
            + "\n".join(f"- {link}" for link in links))


# ---- one brief ----------------------------------------------------------------------------

def _implementations(existing: Optional[RecipeInfo], components: list[Component]
                     ) -> list[dict]:
    """The existing spec's index rows, then a row for each source they do not list yet."""
    rows = [{"platform": r.platform, "location": r.location, "state": r.conformance.state}
            for r in (existing.implementations if existing is not None else ())]
    for c in components:
        if not c.claimed and all(r["location"] != c.path for r in rows):
            rows.append({"platform": c.platform, "location": c.path, "state": "unverified"})
    return rows


def _render_rows(rows: list[dict]) -> str:
    """The rows as `cookr implements` lines the writer runs once the recipe exists."""
    if not rows:
        return "(none)"
    return "\n".join(f"- {r['platform']}: `{r['location'] or '(planned)'}` ({r['state']})"
                      for r in rows)


def _brief(name: str, cfg: Config, components: list[Component], existing: Optional[RecipeInfo],
           rtype: Optional[str]) -> tuple[str, dict]:
    recipe_path = f"{cfg.cookbook}/{name}.md"
    rdid = existing.rdid if existing is not None and existing.rdid else ""
    # Without an explicit --type, keep the existing recipe's type: re-running
    # extract on a composite must not hand back the ingredient template and
    # silently convert it.
    existing_type = existing.type if existing is not None else ""
    rtype = rtype or (existing_type if existing_type in TYPES else "ingredient")
    template = template_path(rtype)
    platforms = sorted({c.platform for c in components})
    kind = "logic" if all(c.kind == "logic" for c in components) else "ui"
    recipe_file = cfg.repo_root / recipe_path
    impls = _implementations(existing, components)

    module = parse_file(EXTRACT_DIR / "module.md")
    action = parse_file(EXTRACT_DIR / "actions" / "extract.md")
    # A non-UI brief carries only the recipe-quality guidelines; the platform
    # design-language guidance has nothing to act on without a visual surface.
    guidelines = references_dir() / "guidelines"
    parts = [f"You are a {module.data.get('role', 'specialist')}.", module.body.strip(),
             _guidelines(guidelines / "recipe-quality" if kind == "logic" else guidelines)]
    if kind == "logic":
        parts.append((EXTRACT_DIR / "logic.md").read_text(encoding="utf-8").strip())
    parts += [f"## reference: templates/{rtype}.md\n\n"
              f"{template.read_text(encoding='utf-8').rstrip()}",
              _checks(cfg),
              render_template(action.body, {
                  "name": name, "recipe_path": recipe_path, "recipe_file": str(recipe_file),
                  "rdid": rdid or "(assigned when the recipe is first indexed)",
                  "type": rtype, "platforms": ", ".join(platforms),
                  "reference_implementations": _render_rows(impls),
              }).strip(),
              f"## Your task\n\nProduce `{recipe_file}` for `{name}`."]
    for c in components:
        body = (cfg.repo_root / c.path).read_text(encoding="utf-8", errors="replace").rstrip()
        parts.append(f"## source: {c.path} ({c.platform})\n\n{fenced(body)}")
    if existing is not None:
        doc = existing.path.parent / f"{existing.path.name}.md"
        body = (doc.read_text(encoding="utf-8", errors="replace") if doc.is_file()
                else existing.body).rstrip()
        parts.append(f"## existing recipe: {recipe_path}\n\n{fenced(body, 'markdown')}")
    text = "\n\n".join(p for p in parts if p) + "\n"
    info = {
        "name": name, "type": rtype, "recipe_path": recipe_path,
        "recipe_file": str(recipe_file), "rdid": rdid,
        "sources": [c.path for c in components], "platforms": platforms,
        "reference_implementations": impls,
        "kind": kind, "existing": existing is not None, "template": str(template),
    }
    return text, info


def resolve_name(name: str, names: set[str]) -> str:
    """`name` itself when it is a spec name, else the one spec name ending in `/<name>`."""
    name = name.strip("/")
    if name in names:
        return name
    found = sorted(n for n in names if n.endswith("/" + name))
    if len(found) == 1:
        return found[0]
    if found:
        raise LookupError(f"`{name}` names several components: {', '.join(found)}")
    raise LookupError(f"no source file in the inventory is named `{name}`")


def build(name: str, config: Config, rtype: Optional[str] = None) -> tuple[str, dict]:
    """Return (prompt_text, info) for `name`; raise LookupError or FileNotFoundError.

    `name` is a spec's path in the cookbook, or its last segment when only one
    spec ends with it. `rtype` of None means "whatever the existing recipe is",
    falling back to `ingredient` when there is no recipe yet.
    """
    corpus = load_corpus(config.cookbook_dir)
    components = scan(config, corpus)
    name = resolve_name(name, {c.name for c in components})
    return _brief(name, config, [c for c in components if c.name == name], corpus.get(name), rtype)


def build_tier(config: Config, tier: str, rtype: Optional[str] = None
               ) -> tuple[list[tuple[str, dict]], list[dict]]:
    """Every brief group `tier` still needs, one per spec, and the rows awaiting review."""
    corpus = load_corpus(config.cookbook_dir)
    report = compute(config, tier=tier, corpus=corpus)
    by_name: dict[str, list[Component]] = {}
    for c in scan(config, corpus, tier=tier):
        by_name.setdefault(c.name, []).append(c)

    briefs, awaiting = [], []
    for row in report.rows:
        if row.state not in TO_WRITE:
            continue
        info = corpus.get(row.name)
        if tuple(row.problems) == AWAITING_REVIEW:
            awaiting.append({"name": row.name,
                             "recipe_path": f"{info.path.relative_to(config.repo_root).as_posix()}.md"})
            continue
        briefs.append(_brief(row.name, config, by_name[row.name], info, rtype))
    return briefs, awaiting


# ---- CLI ----------------------------------------------------------------------------------

def _write(out_dir: Path, text: str, info: dict) -> None:
    brief = (out_dir / f"{info['name']}.md").resolve()
    brief.parent.mkdir(parents=True, exist_ok=True)
    brief.write_text(text, encoding="utf-8")
    info["brief"] = str(brief)


def _run_tier(args, ctx) -> int:
    cfg = ctx.config
    briefs, awaiting = build_tier(cfg, args.tier, args.type)
    for text, info in briefs:
        _write(args.out_dir, text, info)
    write = [info for _, info in briefs]
    if args.json:
        sys.stdout.write(json.dumps({
            "repo_root": str(cfg.repo_root), "cookbook_dir": str(cfg.cookbook_dir),
            "tier": args.tier, "write": write, "awaiting_review": awaiting,
        }, indent=2) + "\n")
        return 0
    ctx.ui.title(f"cookr prompt extract · {args.tier} · {cfg.repo_root}")
    ctx.ui.info(f"cookbook: {cfg.cookbook_dir}")
    ctx.ui.section(f"to write ({len(write)})")
    for info in write:
        ctx.ui.info(f"  {info['name']}  {info['recipe_file']}  brief: {info['brief']}")
    ctx.ui.section(f"awaiting review ({len(awaiting)})")
    for row in awaiting:
        ctx.ui.skip(f"{row['name']}  {row['recipe_path']}")
    return 0


def run(args, ctx) -> int:
    if not args.paction:
        ctx.ui.title("cookr prompt — available actions")
        for a in ACTIONS:
            ctx.ui.info(f"  {a}")
        return 0
    if not require_config(ctx):
        return 2
    if bool(args.name) == bool(args.tier):
        ctx.ui.error("cookr prompt extract: give either a component name or --tier.")
        return 2
    if args.tier and not args.out_dir:
        ctx.ui.error("cookr prompt extract: --tier writes one brief per recipe and needs --out-dir.")
        return 2
    if not require_known_tier(args, ctx):
        return 2
    try:
        if args.tier:
            return _run_tier(args, ctx)
        text, info = build(args.name, ctx.config, args.type)
    except (LookupError, FileNotFoundError) as e:
        ctx.ui.error(f"cookr prompt extract: {e}")
        return 2
    if args.out_dir:
        _write(args.out_dir, text, info)
        sys.stdout.write(json.dumps(info, indent=2) + "\n" if args.json
                         else f"{info['name']}  {info['recipe_file']}  brief: {info['brief']}\n")
    elif args.json:
        info["prompt"] = text
        sys.stdout.write(json.dumps(info, indent=2) + "\n")
    else:
        sys.stdout.write(text)
    return 0
