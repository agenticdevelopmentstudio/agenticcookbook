"""`cookr fold <copy> --into <topic>` — fold a copy of a topic into the topic.

The copy's text the topic lacks becomes new unroled parts, the fold is recorded
in the topic's Change History, the copy is deleted and every link to it across
the cookbook is redirected to the topic. Prints JSON:
`{"redirected": [paths], "parts_added": [names], "identical": bool}`.
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import date
from pathlib import Path

from ..core import rolework
from ..core.bumping import git_user
from ..core.errors import CookbookError

NAME = "fold"
HELP = "Fold a copy of a topic into the topic: its extra text, its history and every link to it."


def register(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("copy", type=Path, help="The copy's source folder (unroled); deleted.")
    parser.add_argument("--into", required=True, type=Path, help="The topic's source folder.")
    parser.add_argument("--author", default=None,
                        help="The Change History row's author (default: `git config user.name`).")
    parser.add_argument("--date", default=None, metavar="YYYY-MM-DD",
                        help="The row's date (default: today).")


def run(args, ctx) -> int:
    try:
        day = date.fromisoformat(args.date).isoformat() if args.date else date.today().isoformat()
    except ValueError as e:
        raise CookbookError(f"--date {args.date!r} is not YYYY-MM-DD") from e
    author = (args.author or "").strip() or git_user(ctx.cwd)
    if not author:
        raise CookbookError("no author: pass --author, or set `git config user.name`")
    report = rolework.fold(ctx.artifact(args.copy), ctx.artifact(args.into), author=author, day=day)
    sys.stdout.write(json.dumps(report.as_json(), indent=2) + "\n")
    return 0
