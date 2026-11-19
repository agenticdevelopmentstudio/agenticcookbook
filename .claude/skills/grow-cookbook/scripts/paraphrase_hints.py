#!/usr/bin/env python3
"""Advisory hints for stage 1's "held in other words" judgement.

    python3 paraphrase_hints.py A/gaps [--repo R] [--top 3]

`cookr roles gaps` matches wording, not subject, so step 1.3 judges each
lacking sentence against the topic's text by hand. This lists, for each
lacking sentence of every `A/gaps/*.json`, the topic sentences with the
highest word overlap, to read first. It is advisory: its output never decides
held, partly held or not held; the plan still judges each sentence.

The topic is the gaps file's `folder` (relative to --repo when not absolute);
its text is every part `artifact.json` lists (`<part>.md`) but `history`
(a change log, not guidance), split into
sentences as quote_building.py splits them. A sentence's score is the share
of the lacking sentence's words (lowercased, common words left out) that the
topic sentence holds, 0 to 1; only a score above 0 is listed.

Prints JSON: {"advisory", "gaps": [{"gaps_file", "folder", "references":
[{"file", "lacking": [{"text", "hints": [{"part", "text", "score"}]}]}]}],
"sentences": [{"gaps_file", "folder", "file", "text", "hints"}]}: `sentences`
is the same, flat, one row per lacking sentence (G59, 1.4.24).
A gaps folder that does not exist, or a gaps file, topic folder or
artifact.json that cannot be read, exits 2,
naming it. Stdlib only.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from json_keys import keys as output_keys  # noqa: E402
from quote_building import sentences  # noqa: E402
from repo_path import cookbook_repo  # noqa: E402

ADVISORY = ("word-overlap hints only: they never decide held, partly held or not held; "
            "judge each lacking sentence against the topic text")
_WORD = re.compile(r"[a-z0-9]+(?:['-][a-z0-9]+)*")
_COMMON = frozenset(
    "a an and are as at be been but by can do does each every for from has have how if in into is it its "
    "may must no not of on or should shall so than that the their them then there these this those to "
    "was were what when where which while who will with without".split())


def words(text: str) -> set[str]:
    return {w for w in _WORD.findall(text.lower()) if w not in _COMMON}


def topic_sentences(folder: Path) -> list[tuple[str, str]]:
    """[(part, sentence)] of every part artifact.json lists, but `history`."""
    try:
        parts = json.loads((folder / "artifact.json").read_text(encoding="utf-8"))["parts"]
    except (OSError, ValueError, KeyError, TypeError) as e:
        raise SystemExit(f"paraphrase_hints.py: cannot read {folder / 'artifact.json'} ({e.__class__.__name__})")
    out = []
    for p in parts:
        name = p.get("part") if isinstance(p, dict) else None
        f = folder / f"{name}.md"
        if name and name != "history" and f.is_file():
            out += [(name, s) for s in sentences(f.read_text(encoding="utf-8"))]
    return out


def rank(text: str, candidates: list[tuple[str, str]], top: int) -> list[dict]:
    want = words(text)
    if not want:
        return []
    scored = [(len(want & words(s)) / len(want), i, part, s) for i, (part, s) in enumerate(candidates)]
    scored = sorted((x for x in scored if x[0] > 0), key=lambda x: (-x[0], x[1]))[:top]
    return [{"part": part, "text": s, "score": round(score, 2)} for score, _, part, s in scored]


def hints(gaps_dir: Path, repo: Path, top: int = 3) -> dict:
    if not gaps_dir.is_dir():
        raise SystemExit(f"paraphrase_hints.py: {gaps_dir} is no folder (the area's gaps folder, A/gaps)")
    out = []
    for f in sorted(gaps_dir.glob("*.json")):
        try:
            data = json.loads(f.read_text(encoding="utf-8"))
            folder = Path(data["folder"])
        except (OSError, ValueError, KeyError, TypeError) as e:
            raise SystemExit(f"paraphrase_hints.py: cannot read {f} ({e.__class__.__name__})")
        folder = folder if folder.is_absolute() else repo / folder
        if not folder.is_dir():
            raise SystemExit(f"paraphrase_hints.py: {f.name} names {data['folder']}, no folder")
        candidates = topic_sentences(folder)
        out.append({"gaps_file": f.name, "folder": data["folder"], "references": [
            {"file": r.get("file"), "lacking": [{"text": s, "hints": rank(s, candidates, top)}
                                                for s in r.get("lacking_sentences", [])]}
            for r in data.get("references", [])]})
    flat = [{"gaps_file": g["gaps_file"], "folder": g["folder"], "file": r["file"], "text": s["text"],
             "hints": s["hints"]} for g in out for r in g["references"] for s in r["lacking"]]
    return {"advisory": ADVISORY, "gaps": out, "sentences": flat}


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("gaps", type=Path, help="A/gaps")
    ap.add_argument("--repo", type=Path, help="default: the nearest cookbook at or above this directory (repo_path.py)")
    ap.add_argument("--top", type=int, default=3)
    ap.add_argument("--keys", "--summary", action="store_true", help="print each output key only, never dropping one: a list as {\"rows\": N} or [], a dict as its keys, a scalar as it is (json_keys.py)")
    a = ap.parse_args(argv)
    try:
        result = hints(a.gaps, cookbook_repo(a.repo, "paraphrase_hints.py"), a.top)   # M8: --repo checked too
    except SystemExit as e:
        print(e, file=sys.stderr)
        return 2
    print(json.dumps(output_keys(result) if a.keys else result, indent=2))
    return 0


if __name__ == "__main__":
    sys.path.insert(0, str(Path(__file__).resolve().parent))      # run with -I too
    from repo_path import run_main      # gapfix13 (G263, G271)
    run_main(main)
