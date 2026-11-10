"""`cookr status` — uncovered files and implementation conformance, per root."""

from __future__ import annotations

import argparse
import json
import sys

from rich.markup import escape

from ..core.conformance import (current_hash, effective_state, entry_version, is_missing,
                                recipe_state)
from ..core.index import current_index
from ..core.inventory import scan
from ..core.recipes import load_corpus
from .inventory import require_config

NAME = "status"
HELP = "Report uncovered files and each implementation's conformance state."


def register(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--json", action="store_true", help="Emit JSON instead of text.")


def gather(cfg) -> dict:
    index = current_index(cfg.cookbook_dir)
    corpus = load_corpus(cfg.cookbook_dir, index)
    uncovered: dict[str, list[str]] = {r.path: [] for r in cfg.roots}
    for c in scan(cfg, corpus):
        if not c.claimed:
            root = cfg.root_for(c.path)
            uncovered.setdefault(root.path if root else "", []).append(c.path)
    impls, recipes = [], []
    for e in sorted(index.entries.values(), key=lambda e: e.rdid):
        if not e.implementations:
            continue
        version = entry_version(cfg.cookbook_dir, e)
        hashes = {id(i): current_hash(cfg, i) for i in e.implementations}
        gone = {id(i): is_missing(cfg, i) for i in e.implementations}
        for i in e.implementations:
            impls.append({"rdid": e.rdid, "platform": i.platform, "location": i.location,
                          "missing": gone[id(i)],
                          "state": effective_state(i, version, hashes[id(i)], gone[id(i)])})
        recipes.append({"rdid": e.rdid, "state": recipe_state(
            e, version, lambda i: hashes[id(i)], lambda i: gone[id(i)])})
    counts = {s: sum(1 for i in impls if i["state"] == s)
              for s in ("unverified", "needs-validation", "planned")}
    counts["uncovered"] = sum(len(v) for v in uncovered.values())
    counts["missing"] = sum(1 for i in impls if i["missing"])
    return {"uncovered": uncovered, "implementations": impls, "recipes": recipes, "counts": counts}


def summary(counts: dict) -> str:
    if not any(counts.values()):
        return "fully conformant"
    line = (f"{counts['uncovered']} uncovered · {counts['unverified']} unverified · "
            f"{counts['needs-validation']} needs-validation · {counts['planned']} planned")
    return line + (f" · {counts['missing']} missing" if counts["missing"] else "")


def run(args, ctx) -> int:
    if not require_config(ctx):
        return 2
    data = gather(ctx.config)
    if args.json:
        sys.stdout.write(json.dumps({**data, "summary": summary(data["counts"])}, indent=2) + "\n")
        return 0
    ctx.ui.title(f"cookr status · {ctx.config.repo_root}")
    for root, files in data["uncovered"].items():
        if files:
            ctx.ui.section(escape(f"{root}: {len(files)} uncovered"))
            for f in files:
                ctx.ui.info(escape(f"  {f}"))
    if data["implementations"]:
        ctx.ui.table(["artifact", "platform", "location", "state"],
                     [[escape(str(i[k] or "")) for k in ("rdid", "platform", "location")]
                      + [i["state"] + (" (missing)" if i["missing"] else "")]
                      for i in data["implementations"]])
    ctx.ui.info(escape(summary(data["counts"])))
    return 0
