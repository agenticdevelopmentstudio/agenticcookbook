"""`cookr targets` — the tuning targets cookr's host manifest declares."""

from __future__ import annotations

import argparse
import json
import sys

from rich.markup import escape

from ..core import hosts

NAME = "targets"
HELP = "List the hosts, families and models cookr tunes for, or resolve one model's chain."


def register(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--host", help="Only this host (default: every declared host).")
    parser.add_argument("--model", help="Resolve this model's chain on --host, least specific first.")
    parser.add_argument("--json", action="store_true", help="Emit JSON instead of a table.")


def run(args, ctx) -> int:
    if args.model and not args.host:
        ctx.ui.error("--model needs --host: a model ID is resolved against one host's manifest entry.")
        return 2
    try:
        declared = hosts.manifest()
        chosen = [hosts.host(args.host)] if args.host else list(declared.values())
        if args.model:
            chain = chosen[0].chain(args.model)
            if args.json:
                sys.stdout.write(json.dumps({"host": args.host, "model": args.model,
                                             "chain": list(chain)}) + "\n")
            else:
                ctx.ui.info(escape(" → ".join(chain)))
            return 0
    except hosts.HostError as e:
        ctx.ui.error(escape(str(e)))
        return 2

    if args.json:
        sys.stdout.write(json.dumps({h.name: {"default_model": h.default_model,
                                              "targets": list(h.targets())} for h in chosen},
                                    indent=2) + "\n")
        return 0
    ctx.ui.title("cookr targets")
    ctx.ui.table(["host", "default model", "targets"],
                 [[h.name, h.default_model, ", ".join(h.targets())] for h in chosen])
    return 0
