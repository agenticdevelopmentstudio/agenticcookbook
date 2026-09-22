"""`cookr prompt extract <name>` — the brief for writing one component's recipe.

Assembled, in order: role header + module preamble, the bundled guidelines,
the selected template, the rendered action, then every source file for the
component and the existing recipe if there is one. No LLM is called here.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Optional

from cookbook.modules.prompt.render import assemble_prompt

from ...core.completeness import REQUIRED_SECTIONS
from ...core.inventory import scan
from ...core.recipes import load_corpus
from ..inventory import require_config

NAME = "prompt"
HELP = "Assemble the extraction prompt for one component and print it."

PROMPTS_DIR = Path(__file__).parent / "prompts"
ACTIONS = ("extract",)


def references_dir() -> Path:
    """Materialised by install.sh from prompts/extract/reference-manifest.json."""
    return PROMPTS_DIR / "extract" / "references"


def register(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("paction", nargs="?", help="Action: extract. Omit to list.")
    parser.add_argument("name", nargs="?", help="Component name (kebab-case).")
    parser.add_argument("--type", choices=("ingredient", "recipe"), default=None,
                        help="Template to write against "
                             "(default: the existing recipe's type, else ingredient).")
    parser.add_argument("--json", action="store_true",
                        help="Wrap the prompt with the resolved paths as JSON.")


def build(name: str, ctx, rtype: Optional[str]):
    """Return (prompt_text, info) for `name`, or raise LookupError or FileNotFoundError.

    `rtype` of None means "whatever the existing recipe is", falling back to
    `ingredient` when there is no recipe yet.
    """
    cfg = ctx.config
    slug = cfg.aliases.get(name, name)
    components = [c for c in scan(cfg) if cfg.aliases.get(c.name, c.name) == slug]
    if not components:
        raise LookupError(f"no source file in the inventory is named `{name}`")

    recipe_rel = f"{cfg.recipes}/{slug}.md"
    domain = cfg.domain(slug)
    corpus = load_corpus(cfg.recipes_dir)
    existing = corpus.get(slug)
    # Without an explicit --type, keep the existing recipe's type: re-running
    # extract on a composite must not hand back the ingredient template and
    # silently convert it.
    rtype = rtype or (
        existing.type if existing is not None and existing.type in REQUIRED_SECTIONS
        else "ingredient"
    )
    platforms = ", ".join(sorted({c.platform for c in components}))

    prompt = assemble_prompt(
        module_md_path=PROMPTS_DIR / "extract" / "module.md",
        references_dir=references_dir() / "guidelines",
        action_md_path=PROMPTS_DIR / "extract" / "actions" / "extract.md",
        params={"name": name, "recipe_path": recipe_rel, "domain": domain, "type": rtype,
                "platforms": platforms},
        task=f"Produce `{recipe_rel}` for `{name}`.",
    )

    # Append the selected template
    template_path = references_dir() / "templates" / f"{rtype}.md"
    if not template_path.exists():
        raise FileNotFoundError(f"template for `{rtype}` not installed at {template_path}; run install.sh")
    template_text = template_path.read_text(encoding="utf-8")

    parts = [prompt.rstrip(), f"## reference: templates/{rtype}.md\n\n{template_text.rstrip()}"]
    for c in components:
        body = (cfg.repo_root / c.path).read_text(encoding="utf-8", errors="replace")
        parts.append(f"## source: {c.path} ({c.platform})\n\n```\n{body.rstrip()}\n```")
    if existing is not None:
        parts.append(
            f"## existing recipe: {recipe_rel}\n\n```markdown\n"
            f"{existing.path.read_text(encoding='utf-8', errors='replace').rstrip()}\n```"
        )
    text = "\n\n".join(parts) + "\n"
    info = {
        "name": name, "slug": slug, "type": rtype, "recipe_path": recipe_rel, "domain": domain,
        "sources": [c.path for c in components], "platforms": platforms.split(", "),
        "existing": existing is not None, "template": str(template_path),
    }
    return text, info


def run(args, ctx) -> int:
    if not args.paction:
        ctx.ui.title("cookr prompt — available actions")
        for a in ACTIONS:
            ctx.ui.info(f"  {a}")
        return 0
    if args.paction not in ACTIONS:
        ctx.ui.error(f"cookr prompt: unknown action '{args.paction}'.")
        return 2
    if not require_config(ctx):
        return 2
    if not args.name:
        ctx.ui.error("cookr prompt extract: a component name is required.")
        return 2
    try:
        text, info = build(args.name, ctx, args.type)
    except LookupError as e:
        ctx.ui.error(f"cookr prompt extract: {e}")
        return 2
    except FileNotFoundError as e:
        ctx.ui.error(f"cookr prompt extract: {e}")
        return 2
    if args.json:
        info["prompt"] = text
        sys.stdout.write(json.dumps(info, indent=2) + "\n")
    else:
        sys.stdout.write(text)
    return 0
