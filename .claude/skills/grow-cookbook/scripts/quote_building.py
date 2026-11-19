#!/usr/bin/env python3
"""Quote a building speciality's text once, each sentence marked by area.

    python3 quote_building.py <area> --speciality S --file F [--repo R] [--keep K | --marks M [--quiet]]

A building speciality's text spans many areas (devops-observability covers
logging, tracing, SLOs, config and containers), so stage 1 quotes it whole,
once, and marks each sentence this area's or another named area's. Only this
area's sentences go into the area's gaps and its topics' research briefs; the
rest stay quoted, marked, never dropped.

Without --marks: prints {"speciality", "sentences": [{"n", "text"}], "marks":
{"<n>": null}}, the template to fill: each n maps to an area path below
cookbook/guidelines/ (this area's own path for this area's sentences).

With --keep K (the marks file this run's output replaces, A/building-<name>.json):
a re-run never wipes marks. When K holds any non-null mark and its sentences
are the new quote's, the re-run is idempotent: it prints K's own bytes
unchanged, says "marks kept (sentences unchanged)" on stderr and exits 0, so
write_on_success.py leaves K untouched (1.4.18). A K that cannot be read as a
marks file exits 2, naming it, and is kept. When K's sentences differ, the template keeps
each mark whose sentence text is unchanged and adds `dropped`: [{"n", "text",
"mark"}], every marked old sentence the new text no longer has (also named on
stderr). A missing K, or one with only null marks, changes nothing. Marks travel
by text, never by number (G54, 1.4.24): a new sentence that joins old
sentences the old splitter cut apart carries every area their marks name
(`joined`: [{"n", "from", "mark"}], named on stderr). `--check` with --keep
writes nothing and prints {"file", "renumbered", "changed", "old_count",
"new_count", "marks", "joined", "lost", "kept"} (`renumbered`: an old sentence moves
to another number or the count changes, an append included; `changed`: each new
sentence number whose text is new; `lost`: every mark it cannot carry; `kept`:
true when nothing is lost, G111); exit 0 unchanged, 1 any change, 2 unreadable.
An --file not yet written exits 2 naming the speciality_reference.py command
that writes it (G117).

G158 (1.4.37): when the workspace (--workspace, else the one --marks or
--keep sits in) has a readable speciality-map.json, a --speciality it does
not name exits 2 naming the map (a short form such as `ui` once dropped
`topics` silently). G168 (1.4.37): the kept path says "marks kept (sentences
unchanged)" and that nothing is to run; a --marks run says one line on
stderr (the sentence counts it prints, which write_on_success.py writes to
A/building-<name>-quoted.json); --quiet leaves `markdown` out of its output.

A sentence ends at `.`, `!` or `?` before a capital, quote, bracket or
backtick, but never after e.g., i.e., vs. or cf., nor inside a parenthesis
that closes later in its unit (G54); one never closed there closes at the
unit's end. After etc. it ends wherever such a cut is made (fix round 1).

A mark is an area path or a list of them, for a sentence spanning areas
(G55, mark.py sets one): the sentence is each named area's.

With --marks (that JSON object, or just its "marks"): prints {"markdown",
"this_area": [{"n", "text"}], "problems": [{"n", "why"}], "topics"}. The
markdown quotes every sentence, in order, each followed by `[this area's]` or
`[<area>'s]`. `topics` are this area's topics the worklist's building entries
reach for the speciality, as unmeasured.json's `building` row names them
(null without a readable W/worklist.json; G77, 1.4.25). The workspace W is
--workspace, else the one the marks file sits in (W/areas/<area>/building-*.json).
A sentence unmarked, or marked with an area that is neither a folder of
cookbook/guidelines/ nor a planned new area (W/areas/<area>/area-plan.md,
G65), is a problem: exit 2. Blank lines are not sentences;
every word of the text is in exactly one sentence.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

_END = re.compile(r"(?<=[.!?])\s+(?=[A-Z`*\[(\"'])")
_ITEM = re.compile(r"^\s*(?:[-*+]|\d+[.)])\s")
_ABBREV = re.compile(r"(?:^|[\s(\[\"'])(?:e\.g|i\.e|vs|cf)\.$", re.I)


def areas_of(mark) -> list[str]:
    """The areas a mark names: [] for none, one for a path, each of a list (G55)."""
    if not mark:
        return []
    return [mark] if isinstance(mark, str) else [m for m in mark if isinstance(m, str) and m]


def _mark(areas: list[str]):
    """One area as a path, several as a sorted list, none as null."""
    areas = sorted(set(areas))
    return None if not areas else areas[0] if len(areas) == 1 else areas


def known_area(area: str, repo: Path, workspace: Path | None = None) -> bool:
    """An area a mark may name: a folder of `repo`/cookbook/guidelines/, or a
    planned new area, one with `workspace`/areas/<area>/area-plan.md (G65,
    1.4.25). A path that is empty, absolute or climbs (`..`) never is."""
    if not area or area.startswith("/") or ".." in area.split("/"):
        return False
    return ((repo / "cookbook" / "guidelines" / area).is_dir()
            or (workspace is not None and (workspace / "areas" / area / "area-plan.md").is_file()))


def _units(para: str) -> list[str]:
    """The paragraph's lines, each list item (`- `, `* `, `+ `, `1. `, `1) `)
    starting a unit of its own, its continuation lines joined to it."""
    units: list[list[str]] = []
    for line in para.splitlines():
        if not units or _ITEM.match(line):
            units.append([])
        units[-1].append(line)
    return [" ".join(" ".join(u).split()) for u in units]


def sentences(text: str) -> list[str]:
    """The text's sentences: each paragraph cut into list items, each part
    split at sentence ends; blank lines dropped, nothing else."""
    out = []
    for para in re.split(r"\n\s*\n", text):
        for unit in _units(para):
            if unit:
                out += _rejoin([s for s in _END.split(unit) if s])
    return out


def _closes(depth: int, rest: list[str]) -> bool:
    """Whether `depth` open parentheses close within `rest`, the unit's
    remaining parts: one never closed there closes at the unit's end."""
    for ch in " ".join(rest):
        depth += (ch == "(") - (ch == ")")
        if depth <= 0:
            return True
    return False


def _rejoin(parts: list[str]) -> list[str]:
    """No cut after e.g., i.e., vs. or cf., nor inside a parenthesis that
    closes later in the unit (G54, 1.4.24): such a cut's two parts are one
    sentence. `etc.` may end a sentence: a cut after it always stands, and
    `_END` never cuts before lowercase or a closing mark (fix round 1, I2;
    fix round 2, N-C)."""
    out: list[str] = []
    for i, part in enumerate(parts):
        depth = out[-1].count("(") - out[-1].count(")") if out else 0
        if out and (_ABBREV.search(out[-1]) or (depth > 0 and _closes(depth, parts[i:]))):
            out[-1] += " " + part
        else:
            out.append(part)
    return out


def render(area: str, speciality: str, file: Path, marks: dict, repo: Path,
           workspace: Path | None = None) -> dict:
    found = sentences(file.read_text(encoding="utf-8"))
    lines = [f"`{speciality}` (`{file.name}`), quoted whole, each sentence marked by area:", ""]
    this, problems = [], []
    for n, text in enumerate(found, start=1):
        where = areas_of(marks.get(str(n)))
        bad = [w for w in where if w != area and not known_area(w, repo, workspace)]
        if not where:
            problems.append({"n": n, "why": "not marked"})
            tag = "[unmarked]"
        elif bad:
            problems += [{"n": n, "why": f"{w} is no area of cookbook/guidelines/"
                                     + (" and has no plan" if workspace else "")} for w in bad]
            tag = "[" + ", ".join(f"{w}'s?" for w in where) + "]"
        else:
            tag = "[" + ", ".join("this area's" if w == area else f"{w}'s" for w in where) + "]"
        if area in where:
            this.append({"n": n, "text": text})
        lines.append(f"> {n}. {text} {tag}")
    return {"markdown": "\n".join(lines) + "\n", "this_area": this, "problems": problems,
            "topics": _topics(area, speciality, workspace)}


def _topics(area: str, speciality: str, workspace: Path | None) -> list[str] | None:
    """This area's topics the worklist's building entries reach for the
    speciality, from the source unmeasured.json's `topics` uses (G77, 1.4.25);
    null when no workspace worklist can be read."""
    try:
        worklist = json.loads((workspace / "worklist.json").read_text(encoding="utf-8")) if workspace else None
    except (OSError, ValueError):
        worklist = None
    if not isinstance(worklist, dict):
        return None
    from unmeasured import building_topics      # unmeasured imports this module: import late
    return building_topics(area, worklist, speciality)


def workspace_of(marks_file: Path) -> Path | None:
    """The workspace W of a marks file at W/areas/<area...>/building-*.json:
    the nearest parent holding an `areas` folder above the file, else None."""
    return next((p.parent for p in marks_file.resolve().parents if p.name == "areas"), None)


KEPT = "marks kept (sentences unchanged)"


def template(speciality: str, found: list[str], keep: Path | None) -> tuple[dict | str | None, str]:
    """The marks template for `found`, carrying `keep`'s marks; `keep`'s own
    text (a str) when it holds marks for these very sentences; (None, why)
    when `keep` cannot be read as a marks file."""
    out = {"speciality": speciality,
           "sentences": [{"n": n, "text": s} for n, s in enumerate(found, start=1)],
           "marks": {str(n): None for n in range(1, len(found) + 1)}}
    if keep is None or not keep.is_file():
        return out, ""
    try:
        raw = keep.read_text(encoding="utf-8")
        old = json.loads(raw)
        texts = [s["text"] for s in old["sentences"]]
        every = [(s["n"], s["text"], old["marks"].get(str(s["n"]))) for s in old["sentences"]]
        marked = [m for m in every if areas_of(m[2])]
    except (OSError, ValueError, KeyError, TypeError, AttributeError) as e:
        return None, (f"quote_building.py: cannot read {keep} as a marks file ({e.__class__.__name__}: {e}); "
                      f"nothing written. Fix or remove it, then re-run.")
    if not marked:
        return out, ""
    if texts == found:      # G168: nothing to run
        return raw, (f"quote_building.py: {KEPT}: {keep} already marks these sentences and is printed as it "
                     f"is; marks kept; nothing to run.\n")
    # Marks travel by text, never by number. An old sentence keeps its mark
    # where the new text has it; old sentences the old splitter cut apart,
    # joined, carry every area their marks name to the one new sentence they
    # make (`joined`, G54); every other marked old sentence is `dropped`.
    pending: dict[str, list[int]] = {}
    for i, (_, text, _) in enumerate(every):
        pending.setdefault(text, []).append(i)
    used: set[int] = set()
    rest = []
    for n, text in enumerate(found, start=1):
        if pending.get(text):
            i = pending[text].pop(0)
            used.add(i)
            if areas_of(every[i][2]):
                out["marks"][str(n)] = every[i][2]
        else:
            rest.append((n, text))
    out["joined"] = []
    for n, text in rest:
        for start in range(len(every)):
            if start in used or not text.startswith(every[start][1]):
                continue
            run, joined = [start], every[start][1]
            while len(joined) < len(text) and run[-1] + 1 < len(every) and run[-1] + 1 not in used:
                run.append(run[-1] + 1)
                joined += " " + every[run[-1]][1]
            if joined == text and len(run) > 1:
                used.update(run)
                mark = _mark([a for i in run for a in areas_of(every[i][2])])
                if mark:
                    out["marks"][str(n)] = mark
                    out["joined"].append({"n": n, "from": [every[i][0] for i in run], "mark": mark})
                break
    out["dropped"] = sorted(({"n": every[i][0], "text": every[i][1], "mark": every[i][2]}
                             for i in range(len(every)) if i not in used and areas_of(every[i][2])),
                            key=lambda d: d["n"])
    return out, "".join(f"quote_building.py: new sentence {j['n']} joins old sentences {j['from']}: "
                        f"it carries {j['mark']}\n" for j in out["joined"]) + "".join(
                        f"quote_building.py: dropped the mark of old sentence {d['n']} ({d['mark']}), "
                        + ("one occurrence of a sentence the text now has fewer times: " if d["text"] in found
                           else "the text no longer has it: ") + f"{d['text']}\n" for d in out["dropped"])


def check(speciality: str, file: Path, keep: Path | None) -> int:
    """G54: what a re-quote with --keep would do to `keep`, writing nothing:
    {"file", "renumbered", "changed", "old_count", "new_count", "marks",
    "joined", "lost", "kept"}; exit 0 unchanged, 1 any change, 2 unreadable."""
    if keep is None or not keep.is_file():
        print(f"quote_building.py: --check needs --keep naming an existing marks file, not {keep}", file=sys.stderr)
        return 2
    try:
        found = sentences(file.read_text(encoding="utf-8"))
        old = json.loads(keep.read_text(encoding="utf-8"))
        texts = [s["text"] for s in old["sentences"]]
    except (OSError, ValueError, KeyError, TypeError, AttributeError) as e:
        print(f"quote_building.py: cannot read {file} or {keep} ({e.__class__.__name__}: {e})", file=sys.stderr)
        return 2
    out, said = template(speciality, found, keep)
    if out is None:
        print(said, file=sys.stderr)
        return 2
    same = texts == found
    out = old if isinstance(out, str) else out
    pending: dict[str, list[int]] = {}
    for n, text in enumerate(found, start=1):
        pending.setdefault(text, []).append(n)
    moved = False                  # N1: an old sentence kept at another number
    for n, text in enumerate(texts, start=1):
        if pending.get(text):
            moved = moved or pending[text].pop(0) != n
    result = {"file": str(keep), "renumbered": moved or len(texts) != len(found),
              "changed": [n for n, text in enumerate(found, start=1) if text not in texts],
              "old_count": len(texts), "new_count": len(found),
              "marks": out["marks"], "joined": out.get("joined", []), "lost": out.get("dropped", [])}
    result["kept"] = not result["lost"]     # G111: every mark carried (an append included)
    print(json.dumps(result, indent=2))
    return 0 if same else 1


def unknown_speciality(speciality: str, workspace: Path | None) -> str | None:
    """G158 (1.4.37): why `speciality` is refused, or None: it is refused only
    when W/speciality-map.json is readable and names no such speciality."""
    if workspace is None:
        return None
    m = workspace / "speciality-map.json"
    try:
        rows = json.loads(m.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None
    if not isinstance(rows, list):
        return None
    known = {r.get("speciality") for r in rows if isinstance(r, dict)}
    if speciality in known:
        return None
    near = sorted(k for k in known if isinstance(k, str) and k.rsplit("/", 1)[-1] == speciality.rsplit("/", 1)[-1])
    return (f"quote_building.py: --speciality {speciality} is no speciality of {m}"
            + (f" (did you mean {', '.join(near)}?)" if near else "") + "; give it as the map names it")


def _stale_homes(a, marks: Path | None) -> None:
    """G205 (1.4.39): name on stderr each home in `marks` (the --keep or
    --marks file) that names no topic (mark.stale_homes); never refuses."""
    ws = a.workspace or (workspace_of(marks) if marks is not None else None)
    if marks is None or ws is None or not a.area:
        return
    from mark import stale_homes      # mark imports this module: read lazily
    for r in stale_homes(Path(ws), a.area, a.repo):
        if r["file"] == marks.name:
            print(f"quote_building.py: stale_home {r['speciality']} {r['n']}={r['home']}: {r['why']}",
                  file=sys.stderr)


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    from repo_path import add_area, area_arg
    add_area(ap)
    ap.add_argument("--speciality", required=True)
    ap.add_argument("--file", type=Path, required=True)
    ap.add_argument("--repo", type=Path, help="with --marks; default: the nearest cookbook at or above this "
                    "directory (repo_path.py)")
    ap.add_argument("--marks", type=Path)
    ap.add_argument("--workspace", type=Path,
                    help="with --marks: the workspace (default: inferred from W/areas/<area>/building-*.json)")
    ap.add_argument("--keep", type=Path, help="the marks file a template run replaces")
    ap.add_argument("--check", action="store_true",
                    help="with --keep: write nothing, report renumbering and every mark it cannot carry")
    ap.add_argument("--quiet", action="store_true", help="with --marks: leave `markdown` out of the output (G168)")
    a = ap.parse_args(argv)
    a.area = area_arg(ap, a)
    if a.workspace is not None:
        from repo_path import check_area
        why = check_area("quote_building.py", a.workspace, a.area, a.repo)      # G198 (1.4.39)
        if why:
            print(why, file=sys.stderr)
            return 2
    why = unknown_speciality(a.speciality, a.workspace or next(
        (w for w in (workspace_of(p) for p in (a.marks, a.keep) if p is not None) if w is not None), None))
    if why:
        print(why, file=sys.stderr)
        return 2
    if not a.file.is_file():
        # G117 (1.4.33): a reference step 1.3 (or the home measure) has not
        # written yet: say how to write it, never a traceback.
        print(f"quote_building.py: {a.file} is not written yet: write it first with "
              f"$COOKR_PY <devteam>/speciality_reference.py {a.speciality} --out {a.file.parent}, then re-run",
              file=sys.stderr)
        return 2
    if a.check:
        return check(a.speciality, a.file, a.keep)
    if not a.marks:
        out, said = template(a.speciality, sentences(a.file.read_text(encoding="utf-8")), a.keep)
        if out is None:
            print(said)
            return 2
        print(said, end="", file=sys.stderr)
        _stale_homes(a, a.keep)
        print(out if isinstance(out, str) else json.dumps(out, indent=2), end="" if isinstance(out, str) else "\n")
        return 0
    quoted = a.marks.with_name(a.marks.stem + "-quoted.json")
    if a.quiet:          # G196 (1.4.39): a re-run never drops the markdown the quoted file holds
        try:
            held = "markdown" in json.loads(quoted.read_text(encoding="utf-8"))
        except (OSError, ValueError, TypeError):
            held = False
        if held:
            print(f"quote_building.py: --quiet refused: {quoted.name} holds `markdown`, which a --quiet re-run "
                  "would drop; re-run without --quiet (stage-1.md *A re-run*)", file=sys.stderr)
            return 2
    data = json.loads(a.marks.read_text(encoding="utf-8"))
    ws = a.workspace or workspace_of(a.marks)
    if a.repo is None:
        from repo_path import cookbook_repo
        try:
            a.repo = cookbook_repo(None, "quote_building.py")
        except SystemExit as e:
            print(e, file=sys.stderr)
            return 2
    out = render(a.area, a.speciality, a.file, data.get("marks", data), a.repo, workspace=ws)
    _stale_homes(a, a.marks)
    print(f"quote_building.py: quoted {a.speciality}: {len(sentences(a.file.read_text(encoding='utf-8')))} "
          f"sentences, {len(out['this_area'])} this area's, {len(out['problems'])} problems"
          + (" (markdown left out: --quiet)" if a.quiet else ""), file=sys.stderr)
    if a.quiet:
        out.pop("markdown")
    print(json.dumps(out, indent=2))
    return 2 if out["problems"] else 0


if __name__ == "__main__":
    from repo_path import run_main      # gapfix13 (G263, G271)
    run_main(main)
