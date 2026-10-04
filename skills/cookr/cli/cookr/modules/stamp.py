"""`cookr stamp` — record the source a tuning addition was written against."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from rich.markup import escape

from ..core import hosts, payload, tuning
from ..core.artifact import ArtifactError
from ..core.skill import templates_root

NAME = "stamp"
HELP = ("Stamp tuning additions with the hash of the source they were written against, so "
        "`cookr validate` reports them stale once that source changes.")


def register(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("additions", nargs="+", type=Path,
                        help="Addition files (<level>/hosts/<target>.add.md or .add.yaml).")
    parser.add_argument("--json", action="store_true", help="Emit the result as JSON.")


def run(args, ctx) -> int:
    root = templates_root(ctx.cookbook_root)
    templates = payload.template_levels(root / "skill", root / "always")
    results, failed = [], False
    for path in args.additions:
        try:
            if not path.is_file():
                raise payload.PayloadError(f"{path} does not exist")
            key = tuning.parse_name(path.name)
            if key is None:
                raise payload.PayloadError(
                    f"{path.name} is not an addition (<target>{tuning.MARK}.md or .yaml)")
            problems = tuning.addition_problems(
                [tuning.additions(path.parent)[key]], hosts.manifest())
            if problems:
                raise payload.PayloadError("; ".join(problems))
            level, changed = payload.stamp_addition(path, templates)
            results.append({"path": str(path), "level": level.name, "stamped": changed, "error": None})
        except (payload.PayloadError, tuning.TuningError, ArtifactError, KeyError) as e:
            failed = True
            results.append({"path": str(path), "level": None, "stamped": False, "error": str(e)})
    if args.json:
        sys.stdout.write(json.dumps({"results": results}, indent=2) + "\n")
    else:
        for r in results:
            if r["error"]:
                ctx.ui.error(escape(f"{r['path']}: {r['error']}"))
            else:
                ctx.ui.ok(escape(f"{r['path']} ({r['level']}): "
                                 + ("stamped" if r["stamped"] else "already current")))
    return 1 if failed else 0
