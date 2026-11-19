#!/usr/bin/env python3
"""Stage 4's review rounds, read and counted by script.

    python3 review_findings.py parse <review.md>
    python3 review_findings.py status <topic-dir>
    python3 review_findings.py owner <topic-dir>

A review.md has `## Findings` (findings only, each a top-level `- ` bullet,
continuation lines indented), `## Checked` (positive notes), from round 2 a
`## Rulings` section, `## Lint`, and the last line `verdict: pass|fail`. Each
finding gets an id `R<round>.<n>`, in order; a lone `- none` bullet is no
finding. A ruling line is `- <id>: fixed|disputed-accepted|routed|open —
<reason>`, the id optionally in bold. `routed`: the finding belongs to a
named sibling topic and was recorded in that sibling's write-brief.md if it
has not passed stage 4, or in its integrate.md if it has; like `fixed` and
`disputed-accepted`, it closes the finding. `status` reads only the topic
folder's top level, never an earlier run kept in `run-<k>/`. `## Lint` holds the /lint-artifact report and
ends with a fixed line, exactly `lint: clean` or `lint: fail <n>` (n >= 1);
only that line is read. `lint: fail <n>`, a missing or malformed line, or no
`## Lint` section at all is a lint error (`lint_errors`): lint fails closed,
and a round with a lint error is no pass, whatever its verdict line says.

A lossless hard failure in stage 5 is recorded by `write_brief.py lossless`
as `lossless-<N>.md` (N the review rounds so far): its `## Findings` get ids
`L<N>.<n>` and are open, for the next scoped review to rule on, like any
finding. Each lossless failure opens one round past the cap.

Older reviews (the 1.3.7 trial's) put positive notes inside `## Findings`
after a plain line such as "Checked with no finding:" or "Not reported:";
`parse` ends the findings at the first such line and files the rest under
checked.

`status` reads every `review-<N>.md` of a topic folder (the orchestrator
saves each round's review.md as review-N.md). A finding is open until a later round rules it
`fixed`, `disputed-accepted` or `routed`; the latest round's own findings are open.
Prints JSON {"rounds", "max_rounds", "allowed_rounds", "verdict",
"lint_errors", "lossless": [N...], "open": [{"id", "text", "history"}],
"next", "why"}. `next` is:
- `review` before any round;
- `write` after a lossless failure that has had no round yet (the author
  fixes it, then a scoped re-review), or after a failed round below the cap
  (round N+1: the author fixes or disputes, then a scoped re-review);
- `integrate` when the last verdict is pass (after a lossless round, stage 5
  runs its check again);
- `stop` (with `why`) when the round a lossless failure opened fails, when a
  second lossless failure comes, or when round `max_rounds` failed with a lint
  error standing: none of these goes to the owner;
- `owner` when round `max_rounds` failed with no lint error: its open
  findings go to the owner and the topic proceeds to stage 5.

`owner` appends the open findings, with their round history, to the topic's
integrate.md under `## For the owner` (creating either if missing); a finding
whose bold id is already in that section is not added twice. Only that
section is looked at: a sibling's routed `## From <topic>'s review` section
may hold the same id for another finding. `routed` reads those sections as
owner items for stage_status.py.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

MAX_ROUNDS = 3
RULINGS = ("fixed", "disputed-accepted", "routed", "open")
_ROUND = re.compile(r"^review-(\d+)\.md$")
_LOSSLESS = re.compile(r"^lossless-(\d+)\.md$")
_RULING = re.compile(r"^- (?:\*\*)?([RL]\d+\.\d+)(?:\*\*)?:?(?:\*\*)?:?\s*\**(fixed|disputed-accepted|routed|open)\b\**"
                     r"\s*[—:-]*\s*(.*)$")
_NONE = re.compile(r"^[`*_]*none[`*_.]*$", re.I)
_LINT_LINE = re.compile(r"^lint: (?:clean|fail [1-9]\d*)$")
_VERDICT = re.compile(r"(?m)^verdict:\s*(pass|fail)\s*$")


def _sections(text: str) -> dict[str, list[str]]:
    sections: dict[str, list[str]] = {}
    name = ""
    for line in text.splitlines():
        if line.startswith("## "):
            name = line[3:].strip().lower()
            sections.setdefault(name, [])
        elif name:
            sections[name].append(line)
    return sections


def _bullets(lines: list[str]) -> tuple[list[str], list[str]]:
    """Top-level bullets until the first plain paragraph line; the rest."""
    items: list[str] = []
    for i, line in enumerate(lines):
        if line.startswith("- "):
            if _NONE.match(line[2:].strip()):
                continue
            items.append(line[2:].strip())
        elif line.startswith((" ", "\t")) and line.strip() and items:
            items[-1] += "\n" + line.rstrip()
        elif line.strip():
            return items, lines[i:]
    return items, []


def parse(text: str, round_no: int = 1, prefix: str = "R") -> dict:
    sections = _sections(text)
    findings, rest = _bullets(sections.get("findings", []))
    checked = [l[2:].strip() for l in rest + sections.get("checked", []) if l.startswith("- ")]
    rulings = {}
    for line in sections.get("rulings", []):
        m = _RULING.match(line.strip())
        if m:
            rulings[m.group(1)] = {"ruling": m.group(2), "reason": m.group(3)}
    verdicts = _VERDICT.findall(text)
    lint = lint_of(sections)
    return {"round": round_no, "verdict": verdicts[-1] if verdicts else None,
            "findings": [{"id": f"{prefix}{round_no}.{n}", "text": t} for n, t in enumerate(findings, 1)],
            "checked": checked, "rulings": rulings, "lint": lint,
            "lint_errors": [] if lint["state"] == "clean" else [lint["reason"]]}


def lint_of(sections: dict[str, list[str]]) -> dict:
    """`## Lint` read by its last line (before the verdict) alone:
    {"state": clean|fail|missing|malformed|no-section, "reason", "report"}.
    `report` is the section's lines bar the verdict. Only `clean` is no lint
    error; `fail` is the draft's, the other three are the reviewer's."""
    if "lint" not in sections:
        return {"state": "no-section", "reason": "no `## Lint` section", "report": []}
    report = [l.rstrip() for l in sections["lint"] if not _VERDICT.match(l.strip())]
    while report and not report[-1].strip():
        report.pop()
    while report and not report[0].strip():
        report.pop(0)
    lines = [l.strip() for l in report if l.strip()]
    if not lines:
        return {"state": "missing", "reason": "no `lint: clean` or `lint: fail <n>` line in `## Lint`",
                "report": report}
    last = lines[-1]
    if not _LINT_LINE.match(last):
        state = "malformed" if "lint:" in last.lower() else "missing"
        return {"state": state, "reason": f"`## Lint` does not end with `lint: clean` or `lint: fail <n>`: {last}",
                "report": report}
    if last == "lint: clean":
        return {"state": "clean", "reason": "", "report": report}
    return {"state": "fail", "reason": last, "report": report}



def rounds(topic: Path) -> list[dict]:
    found = sorted((int(m.group(1)), p) for p in topic.glob("review-*.md") if (m := _ROUND.match(p.name)))
    return [parse(p.read_text(encoding="utf-8"), n) for n, p in found]


def lossless(topic: Path) -> list[dict]:
    """The recorded lossless failures, each `{"round": N, "findings": [...]}`
    (N the review rounds before it)."""
    found = sorted((int(m.group(1)), p) for p in topic.glob("lossless-*.md") if (m := _LOSSLESS.match(p.name)))
    return [parse(p.read_text(encoding="utf-8"), n, prefix="L") for n, p in found]


def allowed_rounds(topic: Path, max_rounds: int = MAX_ROUNDS) -> int:
    """The cap, plus one round per recorded lossless failure."""
    return max_rounds + len(lossless(topic))


def status(topic: Path, max_rounds: int = MAX_ROUNDS) -> dict:
    reviews = rounds(topic)
    losses = lossless(topic)
    open_: dict[str, dict] = {}
    for loss in (l for l in losses if l["round"] == 0):
        for f in loss["findings"]:
            open_[f["id"]] = {**f, "history": ["lossless failure before round 1"]}
    for review in reviews:
        for fid, ruling in review["rulings"].items():
            if fid in open_:
                open_[fid]["history"].append(f"round {review['round']}: {ruling['ruling']}"
                                             + (f" — {ruling['reason']}" if ruling["reason"] else ""))
                if ruling["ruling"] != "open":
                    del open_[fid]
        for f in review["findings"]:
            open_[f["id"]] = {**f, "history": [f"round {review['round']}: raised"]}
        for loss in (l for l in losses if l["round"] == review["round"]):
            for f in loss["findings"]:
                open_[f["id"]] = {**f, "history": [f"lossless failure after round {review['round']}"]}
    last = reviews[-1] if reviews else None
    verdict = last["verdict"] if last else None
    lint = last["lint_errors"] if last else []
    passed = verdict == "pass" and not lint
    n = len(reviews)
    after = [l["round"] for l in losses]
    why = ""
    if after and after[-1] == n:              # a lossless failure awaits its round
        if len(after) > 1:
            nxt, why = "stop", "a second lossless failure"
        else:
            nxt = "write"
    elif after and n == after[-1] + 1:        # the round a lossless failure opened
        nxt = "integrate" if passed else "stop"
        why = "" if passed else "the round the lossless failure opened failed"
    elif not last:
        nxt = "review"
    elif passed:
        nxt = "integrate"
    elif n >= max_rounds:
        nxt, why = ("stop", "a lint error stands at the round cap") if lint else ("owner", "")
    else:
        nxt = "write"
    return {"rounds": n, "max_rounds": max_rounds, "allowed_rounds": max_rounds + len(losses),
            "verdict": verdict, "lint_errors": lint, "lossless": after,
            "open": list(open_.values()), "next": nxt, "why": why}


_FENCE = re.compile(r"^ {0,3}(`{3,}|~{3,})(.*)$")
_FROM = re.compile(r"^## From .+'s review\s*$")


def from_sections(brief: str) -> list[str]:
    """Each `## From <topic>'s review` section of `brief`, verbatim: its
    heading up to the next `## ` heading or the end. A `## ` line inside a
    fenced code block (``` or ~~~, closed by a run of the same character at
    least as long) is text, not a heading."""
    sections: list[list[str]] = []
    keep = False
    fence = ""
    for line in brief.splitlines(keepends=True):
        m = _FENCE.match(line)
        if fence:
            if m and m.group(1)[0] == fence[0] and len(m.group(1)) >= len(fence) and not m.group(2).strip():
                fence = ""
        elif m:
            fence = m.group(1)
        elif line.startswith("## "):
            keep = bool(_FROM.match(line.rstrip("\n")))
            if keep:
                sections.append([])
        if keep:
            sections[-1].append(line)
    return ["".join(s).rstrip("\n") + "\n" for s in sections]


def _fenced(text: str):
    """Each line of `text` with whether it is fence text (a fence line, or a
    line inside a fenced code block of ``` or ~~~)."""
    fence = ""
    for line in text.splitlines():
        m = _FENCE.match(line)
        if fence:
            if m and m.group(1)[0] == fence[0] and len(m.group(1)) >= len(fence) and not m.group(2).strip():
                fence = ""
            yield line, True
        elif m:
            fence = m.group(1)
            yield line, True
        else:
            yield line, False


_FROM_NAME = re.compile(r"^## From (.+)'s review\s*$")


def routed(text: str) -> list[str]:
    """Each finding a sibling routed to this topic's integrate.md, as one
    owner item: `from <sibling>'s review: <entry>`, from every `## From
    <sibling>'s review` section. A finding starts only at a top-level `- `
    bullet and runs to the next one: its continuation lines, indented or
    not and after a blank line too, stay in it (prose joined by a space, a
    new paragraph after a blank line), and its fenced text, its evidence, is
    kept verbatim, line by line. Text before a section's first bullet, fenced
    or not, is an item of its own."""
    items: list[str] = []
    for section in from_sections(text):
        head, _, body = section.partition("\n")
        who = f"from {_FROM_NAME.match(head).group(1)}'s review: "
        cur = None
        gap = after_fence = False
        for line, fenced in _fenced(body):
            if not fenced and not line.strip():
                gap = cur is not None
                continue
            m = None if fenced else re.match(r"^- +(.*)$", line)
            if m or cur is None:
                items.append(who + (m.group(1) if m else line).strip())
                cur = len(items) - 1
            elif fenced:
                items[cur] += ("\n\n" if gap else "\n") + line
            else:
                items[cur] += ("\n\n" if gap else "\n" if after_fence else " ") + line.strip()
            gap, after_fence = False, fenced
    return items


def _owner_section(text: str) -> str:
    """The `## For the owner` section of integrate.md, the only place
    `to_owner` writes: from its heading to the next `## ` heading."""
    _, sep, tail = text.partition("## For the owner\n")
    if not sep:
        return ""
    nxt = tail.find("\n## ")
    return tail if nxt < 0 else tail[:nxt + 1]


def to_owner(topic: Path, max_rounds: int = MAX_ROUNDS) -> dict:
    result = status(topic, max_rounds)
    if result["next"] != "owner":
        return {**result, "added": 0}
    path = topic / "integrate.md"
    text = path.read_text(encoding="utf-8") if path.exists() else f"# Integrate: {topic.name}\n"
    if "## For the owner" not in text:
        text = text.rstrip("\n") + "\n\n## For the owner\n"
    added = []
    recorded = _owner_section(text)   # never a sibling's routed section with the same id
    for f in result["open"]:
        tag = f"**{f['id']}**"
        if tag in recorded:
            continue
        body = f["text"].replace("\n", "\n  ")
        added.append(f"- {tag} (open after round {max_rounds}; " + "; ".join(f["history"]) + f"): {body}")
    if added:
        head, sep, tail = text.partition("## For the owner\n")
        nxt = tail.find("\n## ")
        section, after = (tail, "") if nxt < 0 else (tail[:nxt + 1], tail[nxt + 1:])
        section = re.sub(r"(?m)^none\b.*\n?", "", section).rstrip("\n")
        section = (section + "\n" if section.strip() else "\n") + "\n".join(added) + "\n"
        text = head + sep + section + ("\n" + after if after else "")
        path.write_text(text, encoding="utf-8")
    return {**result, "added": len(added)}


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("parse")
    p.add_argument("review", type=Path)
    p.add_argument("--round", type=int, default=1)
    for name in ("status", "owner"):
        s = sub.add_parser(name)
        s.add_argument("topic", type=Path)
        s.add_argument("--max-rounds", type=int, default=MAX_ROUNDS)
    args = ap.parse_args(argv)
    if args.cmd == "parse":
        out = parse(args.review.read_text(encoding="utf-8"), args.round)
    elif args.cmd == "status":
        out = status(args.topic, args.max_rounds)
    else:
        out = to_owner(args.topic, args.max_rounds)
    print(json.dumps(out, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.path.insert(0, str(Path(__file__).resolve().parent))      # run with -I too
    from repo_path import run_main      # gapfix13 (G263, G271)
    run_main(main)
