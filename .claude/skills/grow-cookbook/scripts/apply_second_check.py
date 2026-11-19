#!/usr/bin/env python3
"""Apply stage 2's second check to research.json, mechanically.

    python3 apply_second_check.py <artifact-folder> <second-check.md> [--date YYYY-MM-DD]
    python3 apply_second_check.py <artifact-folder> --list

`--list` prints the claims the second check covers, one id per line: every
claim a `contradicted` or `new` verdict names, in verdict order, except the
`prior cookbook text` claims, which are the rules themselves.

`second-check.md` holds one block per checked claim:

    ## <claim-id>
    - quote-found: yes|no|partly
    - supports-claim: yes|no|partly
    - citation <n>: holds-quote|lacks-quote|unreachable   (one per citation, 1-based)
    - result: confirmed|refuted
    - note: ...

The rule, whatever the block's own `result` says: a claim is refuted unless
`quote-found` and `supports-claim` are both `yes`. A refuted claim's trust
score drops by 20 when the only shortfall is `partly`, else by 40 (never below
0), and its basis gets "Second check <date>: refuted (quote-found X,
supports-claim Y): <note>; lowered a->b." When at least one citation holds the
quote, every citation marked `lacks-quote` is dropped and independence is
recomputed from the publishers left (two or more distinct: multi-independent;
else single), never raised. Each applied block gets a `- correction:` line in
second-check.md; a block that already has one is not applied again, so a
re-run changes nothing.

Prints JSON: {"refuted", "dropped", "corrections", "result_disagrees",
"unknown"}. `corrections` lists every block with a correction line, for the
write brief (write_brief.py reads them). `result_disagrees` names the blocks
whose `result` line the rule overrode. Exit 2 when a block names a claim
research.json lacks; exit 0 otherwise.
"""

from __future__ import annotations

import argparse
import datetime as _dt
import json
import re
import sys
from pathlib import Path

RANK = {"uncorroborated": 0, "single": 1, "multi-independent": 2}
_BLOCK = re.compile(r"(?m)^## (\S+)[ \t]*\n((?:(?!^## ).*\n?)*)")
_FIELD = re.compile(r"(?m)^- ([a-z-]+(?: \d+)?):[ \t]*(.*)$")


def parse(text: str) -> list[dict]:
    """Every `## <id>` block of a second-check file, its fields as a dict."""
    blocks = []
    for m in _BLOCK.finditer(text):
        fields: dict = {"id": m.group(1), "citations": {}, "span": m.span()}
        for key, value in _FIELD.findall(m.group(2)):
            if key.startswith("citation "):
                fields["citations"][int(key.split()[1])] = value.strip().lower()
            else:
                fields[key] = value.strip()
        blocks.append(fields)
    return blocks


def _word(value: str | None) -> str:
    return (value or "").split()[0].strip(".,;").lower() if value else ""


def is_refuted(block: dict) -> bool:
    return not (_word(block.get("quote-found")) == "yes" and _word(block.get("supports-claim")) == "yes")


def penalty(block: dict) -> int:
    words = {_word(block.get("quote-found")), _word(block.get("supports-claim"))}
    return 20 if words <= {"yes", "partly"} else 40


def _independence(citations: list[dict], old: str) -> str:
    publishers = {(c.get("publisher") or c.get("url") or "").lower() for c in citations}
    new = "multi-independent" if len(publishers) >= 2 else "single"
    return new if RANK[new] < RANK.get(old, 2) else old


def apply(folder: Path, check: Path, date: str) -> dict:
    path = folder / "research" / "research.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    claims = {c["id"]: c for c in data.get("claims", [])}
    text = check.read_text(encoding="utf-8")
    report: dict = {"refuted": [], "dropped": [], "corrections": [], "result_disagrees": [], "unknown": []}
    inserts: list[tuple[int, str]] = []
    for block in parse(text):
        cid = block["id"]
        if cid not in claims:
            report["unknown"].append(cid)
            continue
        if "correction" in block:
            report["corrections"].append({"claim": cid, "correction": block["correction"]})
            continue
        claim, notes = claims[cid], []
        refuted = is_refuted(block)
        if refuted != (_word(block.get("result")) == "refuted"):
            report["result_disagrees"].append(cid)
        if refuted:
            old = int(claim["trust"]["score"])
            new = max(0, old - penalty(block))
            claim["trust"]["score"] = new
            why = (f"refuted (quote-found {_word(block.get('quote-found')) or '?'}, "
                   f"supports-claim {_word(block.get('supports-claim')) or '?'})")
            note = block.get("note", "").rstrip(".")
            claim["trust"]["basis"] = (claim["trust"]["basis"].rstrip() +
                                       f" Second check {date}: {why}: {note}; lowered {old}->{new}.")
            report["refuted"].append(cid)
            notes.append(f"{why}; trust {old} -> {new}; a rule citing it cannot carry MUST")
        marks = block["citations"]
        if any(v.startswith("holds") for v in marks.values()):
            keep, gone = [], []
            for n, citation in enumerate(claim.get("citations", []), start=1):
                (gone if marks.get(n, "").startswith("lacks") else keep).append(citation)
            if gone:
                claim["citations"] = keep
                before = claim.get("independence")
                claim["independence"] = _independence(keep, before)
                for c in gone:
                    report["dropped"].append({"claim": cid, "citation": c.get("url", c.get("title"))})
                notes.append(f"dropped {len(gone)} citation(s) lacking the quote; independence "
                             f"{before} -> {claim['independence']}")
        if notes:
            correction = "; ".join(notes)
            report["corrections"].append({"claim": cid, "correction": correction})
            end = block["span"][1]
            sep = "" if text[:end].endswith("\n") else "\n"
            inserts.append((end, f"{sep}- correction: {correction}\n"))
    for end, line in sorted(inserts, reverse=True):
        body_end = end
        while body_end > 0 and text[body_end - 2:body_end] == "\n\n":
            body_end -= 1
        text = text[:body_end] + line + text[body_end:]
    if inserts:
        check.write_text(text, encoding="utf-8")
        path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return report


def to_check(folder: Path) -> list[str]:
    """The claim ids the second check covers."""
    data = json.loads((folder / "research" / "research.json").read_text(encoding="utf-8"))
    prior = {c["id"] for c in data.get("claims", []) if c.get("source_type") == "prior cookbook text"}
    out: list[str] = []
    for v in data.get("verdicts", []):
        if v.get("verdict") in ("contradicted", "new"):
            out += [c for c in v.get("claims", []) if c not in prior and c not in out]
    return out


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("folder", type=Path)
    ap.add_argument("check", type=Path, nargs="?")
    ap.add_argument("--date", default=_dt.date.today().isoformat())
    ap.add_argument("--list", action="store_true", help="print the claim ids to check, and stop")
    args = ap.parse_args(argv)
    if args.list:
        print("\n".join(to_check(args.folder)))
        return 0
    if args.check is None:
        ap.error("give second-check.md, or --list")
    report = apply(args.folder, args.check, args.date)
    print(json.dumps(report, indent=2))
    return 2 if report["unknown"] else 0


if __name__ == "__main__":
    sys.path.insert(0, str(Path(__file__).resolve().parent))      # run with -I too
    from repo_path import run_main      # gapfix13 (G263, G271)
    run_main(main)
