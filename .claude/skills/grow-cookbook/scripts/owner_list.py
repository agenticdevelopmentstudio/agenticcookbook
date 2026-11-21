#!/usr/bin/env python3
"""Write a topic's owner-list.md from its research, and check a draft against it.

    python3 owner_list.py <artifact-folder> [--draft <draft.md>] [--out <owner-list.md>]

The owner list holds:

(a) every prior rule whose verdict is `unsupported` or `contradicted`: the
    rule, its verdict, the claims its verdict names, and the prior text (the
    quote of the verdict's prior-cookbook-text claim, `<rule>-prior`), which
    stage 3 keeps word for word. This is the predicate cookr's
    `owner-decides` warning keys on: a claim whose source_type is "prior
    cookbook text", named by a verdict of one of those two kinds;
(b) every entry of research.json's `open_questions`, the questions and policy
    choices research hands to the owner.

Being on the list exempts only the rule's wording from review, nothing else.

With `--draft` (stage 3 onward), each (a) rule in the draft's `## Rules` is
compared with its prior text, citation stripped and whitespace collapsed:
`verbatim`; `lead-in` (the prior text, whole, after a lead-in, accepted only
when the prior text has no RFC keyword and the lead-in carries one: it is
listed and is the one change the reviewer accepts); `reworded` (any other
change, a lead-in on a prior rule that already has a keyword or a lead-in
with none included); or `dropped` (no such rule). A reworded or
dropped rule is a problem: exit 1. Without a draft every rule is `not-written`.
A prior text with no RFC keyword is named as such (`keyword` false): stage 3
may put a lead-in carrying the keyword in front of it.

Prints JSON {"prior": [...], "open_questions": [...], "problems": [...]};
writes the markdown to --out when given.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

OWNER_VERDICTS = ("unsupported", "contradicted")
PRIOR_SOURCE = "prior cookbook text"
_RULE = re.compile(r"^- \*\*([a-z0-9-]+)\*\*:\s*(.*)$")
_KEYWORD = re.compile(r"\b(MUST|SHOULD|MAY|SHALL|REQUIRED|RECOMMENDED|OPTIONAL)\b")
_CITATION = re.compile(r"\s*\((?:claim|claims):[^)]*\)\s*$")


def is_prior(claim: dict | None) -> bool:
    """A claim quoting the cookbook's own text before research."""
    return bool(claim) and claim.get("source_type") == PRIOR_SOURCE


def _norm(text: str) -> str:
    return " ".join(text.split())


def draft_rules(text: str) -> dict[str, str]:
    """Each named rule of a draft's `## Rules` section: name -> text without its citation."""
    rules: dict[str, str] = {}
    inside, current = False, None
    for line in text.splitlines():
        if line.startswith("## "):
            inside, current = line.strip() == "## Rules", None
            continue
        if not inside:
            continue
        m = _RULE.match(line)
        if m:
            current = m.group(1)
            rules[current] = m.group(2)
        elif not line.strip():
            continue  # a blank line inside a bullet: its next paragraph is indented
        elif current and line.startswith((" ", "\t")):
            rules[current] += " " + line.strip()
        else:
            current = None
    return {name: _norm(_CITATION.sub("", body)) for name, body in rules.items()}


def compare(prior: str, written: str | None) -> tuple[str, str]:
    if written is None:
        return "dropped", ""
    prior, written = _norm(prior), _norm(written)
    if written == prior:
        return "verbatim", ""
    lead = written[: -len(prior)].strip() if written.endswith(prior) else ""
    if lead and not _KEYWORD.search(prior) and _KEYWORD.search(lead):
        return "lead-in", lead
    return "reworded", ""


def build(folder: Path, draft: Path | None = None) -> dict:
    data = json.loads((folder / "research" / "research.json").read_text(encoding="utf-8"))
    claims = {c["id"]: c for c in data.get("claims", [])}
    rules = draft_rules(draft.read_text(encoding="utf-8")) if draft else None
    prior, problems = [], []
    for verdict in data.get("verdicts", []):
        if verdict.get("verdict") not in OWNER_VERDICTS:
            continue
        named = [claims[c] for c in verdict.get("claims", []) if is_prior(claims.get(c))]
        if not named:
            continue
        claim = next((c for c in named if c["id"] == f"{verdict['rule']}-prior"), named[0])
        entry = {"rule": verdict["rule"], "verdict": verdict["verdict"],
                 "claims": verdict.get("claims", []), "prior": claim["quote"],
                 "against": [claims[c]["claim"] for c in verdict.get("claims", [])
                             if c in claims and c != claim["id"]],
                 "status": "not-written", "lead_in": "",
                 "keyword": bool(_KEYWORD.search(claim["quote"]))}
        if rules is not None:
            entry["status"], entry["lead_in"] = compare(claim["quote"], rules.get(verdict["rule"]))
            if entry["status"] in ("reworded", "dropped"):
                problems.append({"rule": entry["rule"], "status": entry["status"],
                                 "prior": claim["quote"], "written": rules.get(verdict["rule"])})
        prior.append(entry)
    return {"prior": prior, "open_questions": list(data.get("open_questions", [])), "problems": problems}


def render(topic: str, result: dict) -> str:
    out = [f"# Owner list: {topic}", "",
           "For each rule below, only the rule's wording is exempt from review; everything "
           "else about it is reviewed as usual.", "",
           "## Prior rules the research could not support", ""]
    if not result["prior"]:
        out.append("none")
    for r in result["prior"]:
        line = (f"- **{r['rule']}** — verdict `{r['verdict']}` (claims: {', '.join(r['claims'])}). "
                f"Prior text, kept word for word: \"{r['prior']}\"")
        if not r["keyword"]:
            line += (" It has no RFC keyword: stage 3 keeps it word for word and may put one "
                     "lead-in in front of it carrying the keyword the old text implied.")
        if r["lead_in"]:
            line += f" lead-in: \"{r['lead_in']}\" (the one change the reviewer accepts)"
        if r["status"] not in ("not-written", "verbatim", "lead-in"):
            line += f" PROBLEM: {r['status']}"
        out.append(line)
        for against in r["against"]:
            out.append(f"  - against: {against}")
    out += ["", "## Open questions", ""]
    out += [f"- {q}" for q in result["open_questions"]] or ["none"]
    return "\n".join(out) + "\n"


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("folder", type=Path)
    ap.add_argument("--draft", type=Path)
    ap.add_argument("--out", type=Path)
    args = ap.parse_args(argv)
    result = build(args.folder, args.draft)
    if args.out:
        args.out.write_text(render(args.folder.name, result), encoding="utf-8")
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 1 if result["problems"] else 0


if __name__ == "__main__":
    sys.path.insert(0, str(Path(__file__).resolve().parent))      # run with -I too
    from repo_path import run_main      # gapfix13 (G263, G271)
    run_main(main)
