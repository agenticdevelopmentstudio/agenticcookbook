"""`cookr roles` — convert a topic to roles: `set`, `check`, `lossless` (judged
verdicts required unless `--draft`; `--pin-for` prints the pin a judge writes;
`--retarget` retargets a judged-fail entry once),
the `worklist` of every topic to convert, and `gaps`: the sentences of reference
text a topic does not hold (core/gaps.py).

Each prints JSON. The work is in core/rolework.py; further actions join this
group as subparsers.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from ..core import gaps, rolework, worklist
from ..core.errors import CookbookError
from ..core.roles import census

NAME = "roles"
HELP = ("Convert a topic to roles: `set` gives parts roles, `check` runs its census and "
        "compiles its four skills, `lossless` lists every sentence at a base revision that "
        "no part holds now and the folder's lossless.json does not account for, `worklist` lists "
        "every guideline topic to convert, by batch, `gaps` lists each sentence of reference text "
        "the topic does not hold.")


def register(parser: argparse.ArgumentParser) -> None:
    sub = parser.add_subparsers(dest="action", metavar="ACTION", required=True)

    s = sub.add_parser("set", help="Give named parts roles (`<part>=none` clears one).")
    s.add_argument("folder", type=Path, help="The artifact source folder.")
    s.add_argument("--part", action="append", required=True, metavar="NAME=ROLE",
                   help="A part and its role; repeat for each part.")
    s.add_argument("--twin-differs", default=None,
                   help="Set the folder's twin_differs reason (empty clears it).")

    c = sub.add_parser("check", help="The topic's role census and its four compiled skills; "
                                     "exit 1 on any finding.")
    c.add_argument("folder", type=Path, help="The roled artifact source folder.")

    l = sub.add_parser("lossless", help="Every sentence at --base in no part now and not accounted for in "
                                          "<folder>/lossless.json; exit 1 when any. Every reworded or "
                                          "obsolete entry needs a judged pass whose pin matches, unless --draft.",
                       allow_abbrev=False)   # `--pin` is gone: never read as `--pin-for`
    l.add_argument("folder", type=Path, nargs="?", default=None, help="The artifact source folder.")
    l.add_argument("--base", default=None,
                   help="The git revision the text is checked against (required, except with --pin-for).")
    l.add_argument("--copy", action="append", type=Path, default=[], metavar="FOLDER",
                   help="A copy folded into it since --base (its path at --base); repeatable.")
    l.add_argument("--draft", action="store_true",
                   help="A draft: reworded and obsolete entries pass without a judged verdict (said aloud).")
    l.add_argument("--require-judged", action="store_true",
                   help="The default; accepted and ignored.")
    l.add_argument("--pin-for", type=Path, default=None, metavar="FOLDER",
                   help="Print the pin of --entry N of FOLDER's lossless.json, for its judge to write "
                        "beside the verdict; writes nothing.")
    l.add_argument("--retarget", type=Path, default=None, metavar="FOLDER",
                   help="Retarget --entry N of FOLDER's lossless.json once, to the --to targets, after "
                        "its judged fail named content they carry; a second retarget is refused.")
    l.add_argument("--entry", type=int, default=None, metavar="N",
                   help="With --pin-for or --retarget: the entry, from 1 (moved in order, then obsolete).")
    l.add_argument("--to", action="append", default=[], metavar="NAME",
                   help="With --retarget: a rule or part the entry moves to; repeatable (at most 3).")

    w = sub.add_parser("worklist", help="Every guideline topic: its survivor, copies to fold, the devteam "
                                        "specialities whose text moves in (or authored), roled; by batch.")
    w.add_argument("--cookbook", type=Path, default=None,
                   help="The cookbook/ directory (default: the resolved cookbook root).")
    w.add_argument("--map", type=Path, required=True,
                   help="JSON: every speciality, the topic each stands on, and what each building one covers.")
    w.add_argument("--batches", type=Path, required=True,
                   help="JSON: batch labels, area -> batch, per-topic overrides, copies to fold_check.")
    w.add_argument("--new-rows", type=Path, required=True, help="JSON: the topics still to be written.")
    w.add_argument("--json", action="store_true", help="Print the whole worklist as JSON.")
    w.add_argument("--out", type=Path, default=None, help="Also write the worklist JSON here.")

    g = sub.add_parser("gaps", help="Each sentence (6+ words) of each --against file that the topic's "
                                    "own text does not hold: neither a substring of it nor 80%% of its "
                                    "words in it. Exit 0; 2 on a bad path.")
    g.add_argument("folder", type=Path, help="The artifact source folder (its research/ is not read).")
    g.add_argument("--against", action="append", type=Path, required=True, metavar="FILE",
                   help="A plain-text reference file, extracted by the caller; repeatable.")
    g.add_argument("--json", action="store_true", help="Print the whole measure as one JSON object.")


def _emit(data: dict) -> None:
    sys.stdout.write(json.dumps(data, indent=2) + "\n")


def run(args, ctx) -> int:
    for name in ("folder", "pin_for", "retarget"):
        if hasattr(args, name):
            setattr(args, name, ctx.artifact(getattr(args, name)))
    if hasattr(args, "copy"):
        args.copy = [ctx.artifact(c) for c in args.copy]
    if args.action == "set":
        specs = [rolework.parse_spec(p) for p in args.part]
        art = rolework.set_roles(args.folder, specs, args.twin_differs)
        _emit({"folder": str(args.folder),
               "parts": {p.name: p.role for p in art.parts},
               "findings": [{"kind": f.kind, "detail": f.detail} for f in census([args.folder])]})
        return 0
    if args.action == "worklist":
        return _worklist(args, ctx)
    if args.action == "gaps":
        return _gaps(args)
    if args.action == "check":
        report = rolework.check(args.folder)
        _emit(report.as_json())
        return 0 if report.ok else 1
    return _lossless(args)


def _lossless(args) -> int:
    if args.pin_for is not None:
        if args.folder is not None or args.entry is None:
            raise CookbookError("roles lossless --pin-for <folder> takes --entry <n> and no other folder")
        _emit({"folder": str(args.pin_for), **rolework.pin_for(args.pin_for, args.entry, args.copy)})
        return 0
    if args.retarget is not None:
        if args.folder is not None or args.entry is None or not args.to or args.pin_for is not None:
            raise CookbookError("roles lossless --retarget <folder> takes --entry <n>, --to <name> "
                                "(repeatable) and no other folder")
        to = args.to if len(args.to) > 1 else args.to[0]
        _emit({"folder": str(args.retarget), **rolework.retarget(args.retarget, args.entry, to)})
        return 0
    if args.to:
        raise CookbookError("roles lossless: --to goes with --retarget")
    if args.entry is not None:
        raise CookbookError("roles lossless: --entry goes with --pin-for or --retarget")
    if args.folder is None or args.base is None:
        raise CookbookError("roles lossless: give <folder> and --base (or --pin-for <folder> --entry <n>)")
    report = rolework.lossless(args.folder, args.base, args.copy, require_judged=not args.draft)
    _emit({"folder": str(args.folder), "base": args.base, "draft": report.draft, "copies": report.copies,
           "checked": report.checked, "missing": report.missing, "failures": report.failures,
           "obsolete": report.obsolete, "moved": report.moved, "unused": report.unused,
           "counts": report.counts})
    if report.draft:
        print("DRAFT: reworded and obsolete entries pass without a judged verdict; "
              "the topic is not done until it passes without --draft", file=sys.stderr)
    print("moved: " + ", ".join(f"{k.replace('_', '-')} {v}" for k, v in report.counts.items()),
          file=sys.stderr)
    for o in report.obsolete:   # dropped on purpose: said aloud, never silent
        print(f"obsolete: {o['sentence']!r} ({o['reason']})", file=sys.stderr)
    for e in [*report.moved, *report.obsolete, *report.failures]:
        if e.get("stale"):      # a verdict on text that has changed: re-judge
            print(f"stale: {e['sentence']!r}: its judged verdict's pin is missing or does not match; "
                  f"re-judge", file=sys.stderr)
    for u in report.unused:     # a stale account fails, by name
        print(f"unused: {u['sentence']!r} accounts for no sentence absent since --base", file=sys.stderr)
    return 0 if report.ok else 1


def _gaps(args) -> int:
    measured = gaps.measure(args.folder, args.against)
    if args.json:
        _emit({"folder": str(args.folder), "references": [g.as_json() for g in measured]})
        return 0
    for g in measured:
        print(f"{g.file}: {g.sentences} sentence(s), {g.held} held, {g.lacking} lacking")
        for s in g.lacking_sentences:
            print(f"  lacking: {s}")
    return 0


def _worklist(args, ctx) -> int:
    cookbook = args.cookbook or ctx.cookbook_root or Path("cookbook")
    data = worklist.worklist(cookbook, args.map, args.batches, args.new_rows)
    if args.out is not None:
        if not args.out.parent.is_dir():
            raise CookbookError(f"--out {args.out}: no directory {args.out.parent}")
        args.out.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    if args.json:
        _emit(data)
    else:
        _emit({"inputs": data["inputs"], "counts": data["counts"]})
    return 0
