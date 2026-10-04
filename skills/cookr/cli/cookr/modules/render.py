"""`cookr render` — a skill's text as one host (and model) receives it.

Applies the skill's `hosts/` additions along the target chain (core/tuning.py),
then checks the result against the host's load rules. A skill that would not
load is BROKEN and exits 1, so a tuning that breaks a host never ships.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from rich.markup import escape

from ..core import hosts, tuning

NAME = "render"
HELP = "Render a skill for a host (and model) and check that it would load there."

SKILL_FILE = "SKILL.md"


def register(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("skill", type=Path, help=f"The skill directory (holding {SKILL_FILE}).")
    parser.add_argument("--host", required=True, help="The host to render for.")
    parser.add_argument("--model", help="The model to render for (default: the host alone).")
    parser.add_argument("--out", type=Path, help="Write the rendered text here (default: stdout).")
    parser.add_argument("--check", action="store_true",
                        help="Write nothing; only report whether the render would load.")
    parser.add_argument("--json", action="store_true", help="Emit the result as JSON.")


def render_skill(skill: Path, host: hosts.Host, model: str | None = None) -> tuple[str, list, list[str]]:
    """(rendered text, additions applied, problems). Problems cover the
    additions and the host's load rules; empty means it loads."""
    source = (skill / SKILL_FILE).read_text(encoding="utf-8")
    chain = host.chain(model)
    adds = tuning.layers([skill / tuning.HOSTS_DIR], chain)
    every = list(tuning.additions(skill / tuning.HOSTS_DIR).values())
    problems = tuning.addition_problems(every, hosts.manifest())
    text = tuning.render(source, adds)
    return text, adds, problems + tuning.load_problems(text, host)


def run(args, ctx) -> int:
    if not (args.skill / SKILL_FILE).is_file():
        ctx.ui.error(escape(f"{args.skill} has no {SKILL_FILE}"))
        return 2
    try:
        host = hosts.host(args.host)
        text, adds, problems = render_skill(args.skill, host, args.model)
    except (hosts.HostError, tuning.TuningError) as e:
        ctx.ui.error(escape(str(e)))
        return 2

    status = "BROKEN" if problems else "OK"
    if args.json:
        sys.stdout.write(json.dumps({
            "skill": str(args.skill), "host": host.name, "model": args.model,
            "chain": list(host.chain(args.model)), "status": status,
            "applied": [str(a.path) for a in adds], "problems": problems,
            **({} if args.check or args.out else {"text": text}),
        }, indent=2) + "\n")
    elif problems or args.check or args.out:
        label = " → ".join(host.chain(args.model))
        for p in problems:
            ctx.ui.error(escape(f"{args.skill}: {p}"))
        (ctx.ui.error if problems else ctx.ui.ok)(
            escape(f"{status}: {args.skill} for {label} ({len(adds)} addition(s))"))
    else:
        sys.stdout.write(text)
    if args.out and not args.check and not problems:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(text, encoding="utf-8")
    return 1 if problems else 0
