"""`cookr prompt extract` — the brief for writing one component's recipe.

A brief is assembled, in order: role header + module preamble, the bundled
guidelines (each under `## reference: guidelines/<path>`, frontmatter reduced to
its citable `domain`, Change History dropped), the non-UI guidance for a
component from a `logic` root, the selected template, the compliance check list,
the rendered action and `## Your task`, then every source file for the component
and the existing recipe if there is one. Embedded files are fenced with a
backtick run longer than any inside them, so their own fences stay inside.
No LLM is called here.

`extract <name>` builds one brief. `extract --tier <tier> --out-dir <dir>` is
the extraction worklist for a tier: one brief per recipe that still needs a
writer, de-duplicated by slug, written to `<dir>/<slug>.md`. A recipe whose only
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

from cookbook.core.deps import require
from cookbook.core.errors import CookbookError
from cookbook.core.frontmatter import parse_file
from cookbook.core.history import h2_sections
from cookbook.core.markdown import iter_markdown
from cookbook.modules.prompt.render import render_template

from ...core.completeness import CHANGE_HISTORY, NEEDS_REVIEW
from ...core.compliance import load_checks, summary
from ...core.config import Config
from ...core.coverage import compute
from ...core.inventory import Component, scan
from ...core.recipes import load_corpus
from ...core.templates import TYPES, template_path
from ..inventory import require_config, require_known_tier

NAME = "prompt"
HELP = "Assemble the extraction prompt for one component, or every brief a tier still needs."

PROMPTS_DIR = Path(__file__).parent / "prompts"
EXTRACT_DIR = PROMPTS_DIR / "extract"
ACTIONS = ("extract",)
TO_WRITE = ("missing", "partial")
# The one problem that leaves a recipe finished but waiting on a reviewer.
AWAITING_REVIEW = (f"body carries a `{NEEDS_REVIEW}` marker",)

yaml = require("yaml")

_BACKTICKS = re.compile(r"`+")


def references_dir() -> Path:
    """Materialised by install.sh from prompts/extract/reference-manifest.json."""
    return EXTRACT_DIR / "references"


def compliance_dir() -> Path:
    """The compliance check catalog, materialised with the other references."""
    return references_dir() / "compliance"


def register(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("paction", nargs="?", choices=ACTIONS, help="Omit to list the actions.")
    parser.add_argument("name", nargs="?", help="Component name (kebab-case).")
    parser.add_argument("--tier", default=None,
                        help="Every component in this tier that still needs a writer "
                             "(requires --out-dir).")
    parser.add_argument("--out-dir", type=Path, default=None,
                        help="Write each brief to <dir>/<slug>.md and print where, "
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
    """Every guideline under `root`: citable domain kept, other metadata dropped."""
    base = references_dir() / "guidelines"
    chunks = []
    for path in iter_markdown(root):
        fm = parse_file(path)
        domain = fm.data.get("domain")
        cite = f"Cite as `{domain}`.\n\n" if domain else ""
        body = _without_change_history(fm.body).strip()
        chunks.append(f"## reference: guidelines/{path.relative_to(base).as_posix()}\n\n{cite}{body}")
    return "\n\n".join(chunks)


@functools.cache
def _checks(catalog: Path) -> str:
    checks = load_checks(catalog)
    if not checks:
        return ""
    return ("## reference: compliance checks\n\n"
            "The Compliance table cites only these checks, each as a markdown link whose target\n"
            "is `agenticdevelopercookbook://compliance/<document>#<check>`:\n\n" + summary(checks))


# ---- one brief ----------------------------------------------------------------------------

def _existing_recipe(cfg: Config, slug: str) -> Optional[Path]:
    found = sorted(cfg.recipes_dir.rglob(f"{slug}.md"))
    if len(found) > 1:
        raise CookbookError(f"duplicate recipe slug `{slug}`: {found[0]} and {found[1]}")
    return found[0] if found else None


def _brief(name: str, cfg: Config, components: list[Component], existing: Optional[Path],
           existing_type: str, rtype: Optional[str]) -> tuple[str, dict]:
    slug = cfg.aliases.get(name, name)
    if existing is not None:
        # A recipe already filed in a subdirectory is rewritten where it is.
        recipe_path = existing.relative_to(cfg.repo_root).as_posix()
        domain = cfg.domain(existing.relative_to(cfg.recipes_dir).with_suffix("").as_posix())
    else:
        recipe_path = f"{cfg.recipes}/{slug}.md"
        domain = cfg.domain(slug)
    # Without an explicit --type, keep the existing recipe's type: re-running
    # extract on a composite must not hand back the ingredient template and
    # silently convert it.
    rtype = rtype or (existing_type if existing_type in TYPES else "ingredient")
    template = template_path(rtype)
    platforms = sorted({c.platform for c in components})
    kind = "logic" if all(c.kind == "logic" for c in components) else "ui"
    recipe_file = cfg.repo_root / recipe_path

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
              _checks(compliance_dir()),
              render_template(action.body, {
                  "name": name, "recipe_path": recipe_path, "recipe_file": str(recipe_file),
                  "domain": domain, "type": rtype, "platforms": ", ".join(platforms),
              }).strip(),
              f"## Your task\n\nProduce `{recipe_file}` for `{name}`."]
    for c in components:
        body = (cfg.repo_root / c.path).read_text(encoding="utf-8", errors="replace").rstrip()
        parts.append(f"## source: {c.path} ({c.platform})\n\n{fenced(body)}")
    if existing is not None:
        body = existing.read_text(encoding="utf-8", errors="replace").rstrip()
        parts.append(f"## existing recipe: {recipe_path}\n\n{fenced(body, 'markdown')}")
    text = "\n\n".join(p for p in parts if p) + "\n"
    info = {
        "name": name, "slug": slug, "type": rtype, "recipe_path": recipe_path,
        "recipe_file": str(recipe_file), "domain": domain,
        "sources": [c.path for c in components], "platforms": platforms,
        "kind": kind, "existing": existing is not None, "template": str(template),
    }
    return text, info


def build(name: str, config: Config, rtype: Optional[str] = None) -> tuple[str, dict]:
    """Return (prompt_text, info) for `name`; raise LookupError or FileNotFoundError.

    `rtype` of None means "whatever the existing recipe is", falling back to
    `ingredient` when there is no recipe yet.
    """
    slug = config.aliases.get(name, name)
    components = [c for c in scan(config) if config.aliases.get(c.name, c.name) == slug]
    if not components:
        raise LookupError(f"no source file in the inventory is named `{name}`")
    existing = _existing_recipe(config, slug)
    existing_type = ""
    if existing is not None:
        try:
            existing_type = str(parse_file(existing).data.get("type", "") or "")
        except (yaml.YAMLError, UnicodeDecodeError) as e:
            raise CookbookError(f"{existing}: cannot read recipe (bad YAML frontmatter "
                                f"or not UTF-8) — {e}") from e
    return _brief(name, config, components, existing, existing_type, rtype)


def build_tier(config: Config, tier: str, rtype: Optional[str] = None
               ) -> tuple[list[tuple[str, dict]], list[dict]]:
    """Every brief `tier` still needs, one per slug, and the rows awaiting review."""
    report = compute(config, tier=tier, checks=load_checks(compliance_dir()))
    by_slug: dict[str, list[Component]] = {}
    for c in scan(config):
        by_slug.setdefault(config.aliases.get(c.name, c.name), []).append(c)
    corpus = load_corpus(config.recipes_dir)

    briefs, awaiting, seen = [], [], set()
    for row in report.rows:
        if row.state not in TO_WRITE or row.slug in seen:
            continue
        seen.add(row.slug)
        info = corpus.get(row.slug)
        if tuple(row.problems) == AWAITING_REVIEW:
            awaiting.append({"name": row.name, "slug": row.slug,
                             "recipe_path": info.path.relative_to(config.repo_root).as_posix()})
            continue
        briefs.append(_brief(row.name, config, by_slug[row.slug],
                             info.path if info else None, info.type if info else "", rtype))
    return briefs, awaiting


# ---- CLI ----------------------------------------------------------------------------------

def _write(out_dir: Path, text: str, info: dict) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    brief = (out_dir / f"{info['slug']}.md").resolve()
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
            "repo_root": str(cfg.repo_root), "recipes_dir": str(cfg.recipes_dir),
            "tier": args.tier, "write": write, "awaiting_review": awaiting,
        }, indent=2) + "\n")
        return 0
    ctx.ui.title(f"cookr prompt extract · {args.tier} · {cfg.repo_root}")
    ctx.ui.info(f"recipes: {cfg.recipes_dir}")
    ctx.ui.section(f"to write ({len(write)})")
    for info in write:
        ctx.ui.info(f"  {info['slug']}  {info['recipe_file']}  brief: {info['brief']}")
    ctx.ui.section(f"awaiting review ({len(awaiting)})")
    for row in awaiting:
        ctx.ui.skip(f"{row['slug']}  {row['recipe_path']}")
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
                         else f"{info['slug']}  {info['recipe_file']}  brief: {info['brief']}\n")
    elif args.json:
        info["prompt"] = text
        sys.stdout.write(json.dumps(info, indent=2) + "\n")
    else:
        sys.stdout.write(text)
    return 0
