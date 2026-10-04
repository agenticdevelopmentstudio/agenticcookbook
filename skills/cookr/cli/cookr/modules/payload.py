"""`cookr payload` — what a model reads to tune the cookbook for itself."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from rich.markup import escape

from ..core import hosts, payload, tuning
from ..core.artifact import ArtifactError, find_folders
from ..core.skill import templates_root

NAME = "payload"
HELP = ("Survey tuning for one target: each template and artifact, the additions it has along "
        "the target's chain, and which went stale. --out-dir writes per-artifact worklists.")


def register(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("paths", nargs="*", type=Path,
                        help="Artifact folders or directories to search (default: the cookbook).")
    parser.add_argument("--target", required=True,
                        help="Who is tuning: `claude.opus-5-5`, `codex.gpt-5-codex`, or a family "
                             "or host (`claude.opus`, `codex`).")
    parser.add_argument("--library", help="The library skill names are prefixed with.")
    parser.add_argument("--json", action="store_true", help="Emit the survey as JSON.")
    parser.add_argument("--out-dir", type=Path,
                        help="Write the artifacts as worklists of --batch-size, each entry holding "
                             "the skill as the target receives it today.")
    parser.add_argument("--batch-size", type=int, default=25, help="Artifacts per worklist (default 25).")


def _target_chain(spec: str) -> tuple[str, ...]:
    """Like hosts.parse_target, but a bare host means the host alone: a tuning
    pass writes at the level it names."""
    if "." not in spec:
        return (hosts.host(spec).name,)
    return hosts.parse_target(spec)


def run(args, ctx) -> int:
    paths = args.paths or ([ctx.cookbook_root] if ctx.cookbook_root else [Path("cookbook")])
    missing = [p for p in paths if not p.exists()]
    if missing:
        ctx.ui.error(escape(f"no such path: {', '.join(map(str, missing))}"))
        return 2
    if args.batch_size < 1:
        ctx.ui.error("--batch-size must be at least 1")
        return 2
    try:
        chain = _target_chain(args.target)
        folders = find_folders(paths)
        root = templates_root(ctx.cookbook_root)
        data = payload.survey(chain, folders,
                              templates=payload.template_levels(root / "skill", root / "always"))
        batches = []
        if args.out_dir:
            items = payload.worklist(chain, folders, args.library, templates=root / "skill")
            args.out_dir.mkdir(parents=True, exist_ok=True)
            for n, i in enumerate(range(0, len(items), args.batch_size), 1):
                p = args.out_dir / f"worklist-{n:02d}.json"
                p.write_text(json.dumps({"chain": list(chain), "items": items[i:i + args.batch_size]},
                                        indent=2) + "\n", encoding="utf-8")
                batches.append(str(p))
    except (hosts.HostError, tuning.TuningError, ArtifactError) as e:
        ctx.ui.error(escape(str(e)))
        return 2
    data["worklists"] = batches
    if args.json:
        sys.stdout.write(json.dumps(data, indent=2) + "\n")
        return 0
    ctx.ui.title(f"cookr payload · {' → '.join(chain)}")
    rows = []
    for lv in data["templates"] + data["artifacts"]:
        for a in lv["additions"]:
            state = "stale" if a["stale"] else ("current" if a["stamped"] else "hand-written")
            rows.append([lv["level"], Path(a["path"]).name, state])
    if rows:
        ctx.ui.table(["level", "addition", "state"], rows)
    stale = sum(r[2] == "stale" for r in rows)
    ctx.ui.info(f"{len(data['templates'])} template(s), {len(data['artifacts'])} artifact(s), "
                f"{len(rows)} addition(s) along the chain, {stale} stale")
    for b in batches:
        ctx.ui.info(escape(f"worklist: {b}"))
    return 0
