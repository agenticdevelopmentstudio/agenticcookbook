#!/usr/bin/env python3
"""The specialities stage 1 cannot measure with `cookr roles gaps`, placed in
their areas, so an area plan quotes the whole text of each one it must cover.

    python3 unmeasured.py <area> --workspace <workspace> --reference A/reference.json

A speciality is unmeasured when its row of `A/reference.json` has no topic,
or when `speciality-map.json` gives it none (A/reference.json lists only
this area's specialities: G57, 1.4.24; such a row's `file` is null).
All of its text is lacking, and the worklist places it:

- a `building-split` speciality (its `case` in `<workspace>/speciality-map.json`)
  goes to every area that a `building` entry of a `<workspace>/worklist.json`
  batch maps it to (`topic` is `guidelines/<area>/<topic>`);
- any other goes to the area of the one `new: true` worklist topic whose
  `devteam` entries name it (its `survivor`, `guidelines/<area>/<topic>`).

`new_topics` lists every `new: true` worklist topic of this area, one row per
speciality its `devteam` entries name (`speciality` null when they name
none), whatever that speciality's reference row says: a row naming a topic
outside the area names the new topic's candidate survivor, its R9 target
(G53, 1.4.24). `kind` is the worklist entry's.

A building entry reaches an area directly (its `topic` is in the area) or
by `new_home`: its topic is the `new_home` of a worklist topic whose
`survivor` is in the area, or the `survivor` of one whose `new_home` is.
`topics` are this area's topics it reaches, `by_new_home` the entry topics
that reached it through a `new_home`, and `measured_by` the worklist topics
whose `devteam` entries name it: empty, `roles gaps` never measures it, and
its quoted text is all the plan has of it. A worklist entry's `via` (the
speciality whose topic the mapping went through) is not a measure: the row
stays unmeasured, and `via` lists each `{"speciality", "topic"}` of this
area's topics it reached that way, so the plan measures it against that topic.
Its `file` is null when this area's reference run did not write it.

Other plans' marks: every `<workspace>/areas/<plan>/building-<name>.json`
holding `speciality`, `sentences` and `marks` (quote_building.py's marks
file) is read. A mark is an area path, a list of area paths (a sentence
that spans areas: each area gets it), or null. `marked_here` lists each
sentence other plans mark as this area's, once per (speciality, n), every
such plan in `marked_by` (G49, 1.4.24); `mark_conflicts` lists each
sentence two or more plans mark for different areas (two lists differ only
when their areas do, order aside: G55), when this area is one of the plans
or one of the areas, with every plan's mark: the owner settles it. Each
conflict row carries `agrees_for` (the areas every side's mark names) and
`differs_for` (the areas some side leaves out): a row whose `differs_for`
does not name this area agrees for it (G71, 1.4.25). A
`mark_conflicts` row with `reason: "numbering differs"` names two plans
whose marks files number one speciality differently (one is stale: the
same text at another n, or one n with another text), with each plan's n,
text and mark (fix round 2), and no `agrees_for`/`differs_for`: its marks
are for different sentences, so it is always this plan's to resolve
(1.4.26).

`--check` writes nothing: it compares this fresh result with the saved
`<workspace>/areas/<area>/unmeasured.json` and prints `{"area", "check":
"unchanged"|"changed", "saved_file", "stale_reference", "changes": [{"path", "added", "removed"} |
{"path", "was", "now"}]}`, exit 0 unchanged, 1 changed, 2 when the saved
file or an input cannot be read (G45, 1.4.24) or, as a run does, when
`unplaced` is not empty. `stale_reference` (1.4.27) lists each
`--reference` row written before reference_format.REFERENCE_FORMAT; a
non-empty one is a change. A run names each such row on stderr. A key the
saved file lacks whose fresh value is empty ([], {}, null, false), at any
depth, is no change: its path is listed in `new_keys` (present only when
non-empty), which never sets the exit (1.4.34, review M3).

A speciality whose topic in `speciality-map.json` is a worklist copy (a
`copies` folder of a topic with another `survivor`) is measured in the
survivor's area against the survivor, never in the copy's: in that area it is
in `against_survivor` (`{"speciality", "copy", "survivor", "file"}`, `file`
null when this area's reference run did not write it); in the copy's area,
when the survivor's is another, in `survivor_elsewhere`.

Prints JSON: `{"area", "new_topics": [{"speciality", "topic", "file", "kind"}],
"building": [{"speciality", "topics", "by_new_home", "measured_by", "via", "file"}],
"unplaced": [{"speciality", "why"}], "marked_here": [{"speciality", "n",
"text", "marked_by"}], "mark_conflicts": [{"speciality", "n", "text", "marks"} |
{"speciality", "reason", "plans": [{"plan", "n", "text", "mark"}]}],
"against_survivor": [...], "survivor_elsewhere": [...], "unread_marks": [...], "ignored_marks": [...]}`, with all but
`unplaced` only this area's. `unplaced` is every speciality, in any area, that
the worklist cannot place; when it is not empty the stage stops: exit 2,
naming them. A missing or unreadable input, this area's marks file
included, exits 2, naming it. Another area's marks file that cannot be read
(a run there may be mid-edit) is skipped and listed in `unread_marks`
(`{"file", "plan", "why"}`), and named on stderr.

1.4.36: `--area A` names the area as the positional does, and
`--reference` defaults to `<workspace>/areas/<area>/reference.json` (G139).
`--check --digest` prints one line for Step-4 re-check, `unmeasured.py
<area>: check <changed|unchanged>; changes N; new_keys N; stale_reference N;
result <hash>`, the hash over what the check found (G137); `--keys` /
`--summary` print each output key with its shape, `changes`, `new_keys` and
`stale_reference` whole (json_keys.py, G138). Each exits as the run does.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from quote_building import areas_of  # noqa: E402  (G55: a mark may list areas)
from reference_format import stale_reference  # noqa: E402  (R-I-1, 1.4.27)
from json_keys import cap, keys as output_keys  # noqa: E402
from repo_path import add_area, area_arg, cookbook_repo  # noqa: E402

NO_BUILDING = "a building speciality no worklist building entry maps to a topic"
NO_NEW_ROW = "no new row claims it"


def _area(path: str) -> str:
    return path.removeprefix("guidelines/").rsplit("/", 1)[0]


def _load(path: Path):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError) as e:
        raise SystemExit(f"unmeasured.py: cannot read {path} ({e.__class__.__name__})") from e


def _same(a, b) -> bool:
    """Whether two marks name the same areas (a list's order aside)."""
    return sorted(set(areas_of(a))) == sorted(set(areas_of(b)))


def _key(item):
    """A list item's identity for `changes`: its (speciality, n), topic,
    speciality, n or file, else None (compared as whole JSON)."""
    if isinstance(item, dict):
        if "speciality" in item and "n" in item:
            return f"{item['speciality']}#{item['n']}"
        for k in ("topic", "speciality", "n", "file"):
            if k in item and not isinstance(item[k], (dict, list)):
                return str(item[k])
    return None


def _empty(v) -> bool:
    """[], {}, None or False: a value a new key may take without being a change."""
    return v is None or v is False or (isinstance(v, (list, dict)) and not v)


def changes(old, new, path: str = "", new_keys: list[str] | None = None) -> list[dict]:
    """What changed from `old` to `new`: {"path", "was", "now"} for a value,
    {"path", "added", "removed"} for a list. A list of objects each with one
    identity (see `_key`) is compared item by item, `path[<key>]`.
    Fix round 1 (1.4.34, review M3): a key `old` lacks whose new value is
    empty ([], {}, None, False), at any depth, is no change; its path goes in
    `new_keys` (when given), so an additive release does not flip every check.
    A new key with any other value is a change, as before."""
    if isinstance(old, dict) and isinstance(new, dict):
        out = []
        for k in list(old) + [k for k in new if k not in old]:
            sub = f"{path}.{k}" if path else str(k)
            if k not in new:
                out.append({"path": sub, "was": old[k], "now": None})
            elif k not in old:
                if _empty(new[k]):
                    if new_keys is not None:
                        new_keys.append(sub)
                else:
                    out.append({"path": sub, "was": None, "now": new[k]})
            else:
                out += changes(old[k], new[k], sub, new_keys)
        return out
    if isinstance(old, list) and isinstance(new, list):
        ko, kn = [_key(x) for x in old], [_key(x) for x in new]
        if old and new and None not in ko + kn and len(set(ko)) == len(ko) and len(set(kn)) == len(kn):
            by_o, by_n = dict(zip(ko, old)), dict(zip(kn, new))
            out = [{"path": path, "added": [by_n[k] for k in kn if k not in by_o],
                    "removed": [by_o[k] for k in ko if k not in by_n]}]
            out = [c for c in out if c["added"] or c["removed"]]
            for k in ko:
                if k in by_n:
                    out += changes(by_o[k], by_n[k], f"{path}[{k}]", new_keys)
            return out
        so = [json.dumps(x, sort_keys=True) for x in old]
        sn = [json.dumps(x, sort_keys=True) for x in new]
        added = [x for x, j in zip(new, sn) if j not in so]
        removed = [x for x, j in zip(old, so) if j not in sn]
        return [{"path": path, "added": added, "removed": removed}] if added or removed else []
    return [] if old == new else [{"path": path, "was": old, "now": new}]


def _paths(worklist: dict):
    for batch in worklist.get("batches", []):
        yield from batch.get("topics", [])


def place(area: str, worklist: dict, speciality_map: list, references: list,
          plan_marks: dict[str, list[dict]] | None = None) -> dict:
    cases = {row["speciality"]: row.get("case") for row in speciality_map}
    new_rows: dict[str, list[str]] = defaultdict(list)
    builds: dict[str, list[str]] = defaultdict(list)
    vias: dict[str, list[tuple[str, str]]] = defaultdict(list)  # speciality: [(via, topic)]
    measured: dict[str, set[str]] = defaultdict(set)
    for t in _paths(worklist):
        if isinstance(t.get("devteam"), list):
            for entry in t["devteam"]:
                measured[entry["speciality"]].add(t["survivor"])
                if t.get("new"):
                    new_rows[entry["speciality"]].append(t["survivor"])
    homes = _homes(worklist)
    for batch in worklist.get("batches", []):
        for entry in batch.get("building", []):
            builds[entry["speciality"]].append(entry["topic"])
            if entry.get("via"):
                vias[entry["speciality"]].append((entry["via"], entry["topic"]))
    result = {"area": area, "new_topics": [], "building": [], "unplaced": [],
              "marked_here": [], "mark_conflicts": [], "against_survivor": [], "survivor_elsewhere": []}
    files = _files(references)
    for t in _paths(worklist):     # G53: every new worklist topic of this area
        if not t.get("new") or _area(t["survivor"]) != area:
            continue
        sps = [e["speciality"] for e in t["devteam"]] if isinstance(t.get("devteam"), list) else []
        for sp in sps or [None]:
            result["new_topics"].append({"speciality": sp, "topic": t["survivor"],
                                         "file": files.get(sp) if sp else None, "kind": t.get("kind")})
    listed = {r["speciality"] for r in references}
    # G57: A/reference.json holds only this area's rows; every topicless
    # speciality of speciality-map.json is still placed (or unplaced) here.
    topicless = [r for r in references if r.get("topic") is None] + [
        {"speciality": r["speciality"], "topic": None, "file": None}
        for r in speciality_map if not r.get("topic") and r["speciality"] not in listed]
    for row in topicless:
        key = row["speciality"]
        if cases.get(key) == "building-split":
            if not builds[key]:
                result["unplaced"].append({"speciality": key, "why": NO_BUILDING})
                continue
            reached, via = _reach(area, builds[key], homes)
            if reached:
                result["building"].append({"speciality": key, "topics": sorted(set(reached.values())),
                                           "by_new_home": sorted(via), "measured_by": sorted(measured[key]),
                                           "via": [{"speciality": v, "topic": reached[t]}
                                                   for v, t in sorted(set(vias[key])) if t in reached],
                                           "file": row["file"]})
            continue
        claims = sorted(set(new_rows[key]))
        if not claims:
            result["unplaced"].append({"speciality": key, "why": NO_NEW_ROW})
        elif len(claims) > 1:
            result["unplaced"].append({"speciality": key,
                                       "why": "two or more new rows claim it: " + ", ".join(claims)})
    _marks(area, plan_marks or {}, result)
    _copies(area, worklist, speciality_map, references, result)
    return result


def _homes(worklist: dict) -> dict[str, str]:
    """survivor <-> new_home, both ways, for every worklist topic with one."""
    homes: dict[str, str] = {}
    for t in _paths(worklist):
        if t.get("new_home"):
            homes[t["new_home"]] = t["survivor"]
            homes[t["survivor"]] = t["new_home"]
    return homes


def _reach(area: str, entry_topics: list[str], homes: dict[str, str]) -> tuple[dict[str, str], set[str]]:
    """({entry topic: this area's topic it reaches}, the entry topics that
    reached it through a `new_home`): directly, or by new_home."""
    here = {t for t in entry_topics if _area(t) == area}
    via = {t for t in entry_topics if t in homes and _area(homes[t]) == area}
    return {t: t for t in here} | {t: homes[t] for t in via}, via


def building_topics(area: str, worklist: dict, speciality: str) -> list[str]:
    """This area's topics the worklist's building entries reach for one
    speciality: the `topics` of its unmeasured.json `building` row
    (quote_building.py --marks prints them, G77, 1.4.25)."""
    entries = [e["topic"] for b in worklist.get("batches", []) for e in b.get("building", [])
               if e.get("speciality") == speciality]
    return sorted(set(_reach(area, entries, _homes(worklist))[0].values()))


def _files(references: list) -> dict:
    """{speciality: its file}; a null-file row never hides a path another row
    of the same speciality gives (fix round 1, M5)."""
    files: dict = {}
    for r in references:
        if r.get("file") or r["speciality"] not in files:
            files[r["speciality"]] = r.get("file")
    return files


def _marks(area: str, plan_marks: dict[str, list[dict]], result: dict) -> None:
    """Fill `marked_here` and `mark_conflicts` from every plan's marks files."""
    by_sentence: dict[tuple[str, int], dict] = {}   # I1: one row per sentence, not per text
    here: dict[tuple[str, int], dict] = {}
    for plan in sorted(plan_marks):
        for f in plan_marks[plan]:
            for s in f["sentences"]:
                mark = f["marks"].get(str(s["n"]))
                if not areas_of(mark):
                    continue
                if area in areas_of(mark) and plan != area:
                    row = here.get((f["speciality"], s["n"]))
                    if row is None:
                        row = here[(f["speciality"], s["n"])] = {"speciality": f["speciality"], "n": s["n"],
                                                                 "text": s["text"], "marked_by": []}
                        result["marked_here"].append(row)
                    row["marked_by"].append(plan)
                seen = by_sentence.setdefault((f["speciality"], s["n"]), {"text": s["text"], "marks": {}})
                seen["marks"][plan] = mark
    renumbered = _renumbered(plan_marks)
    for (speciality, n), seen in by_sentence.items():
        if speciality in renumbered:      # G114: n pairs different sentences; compared by text below
            continue
        marks = seen["marks"]
        named = {a for m in marks.values() for a in areas_of(m)}
        first = next(iter(marks.values()))
        if any(not _same(first, m) for m in marks.values()) and (area in marks or area in named):
            result["mark_conflicts"].append({"speciality": speciality, "n": n, "text": seen["text"],
                                             "marks": dict(sorted(marks.items())), **_agreement(marks.values())})
    result["mark_conflicts"] += _by_text(area, plan_marks, renumbered)
    result["mark_conflicts"] += _numbering(area, plan_marks)


def _renumbered(plan_marks: dict[str, list[dict]]) -> set[str]:
    """G114 (1.4.33): each speciality two plans' marks files number
    differently (one n with two texts, or one text at two n). Fix round 1
    (1.4.34, review M5): every plan's numbering is compared with every
    other's, never only with the first plan seen."""
    seen: dict[str, list[dict[int, str]]] = {}
    for plan in sorted(plan_marks):
        for f in plan_marks[plan]:
            seen.setdefault(f["speciality"], []).append({s["n"]: s["text"] for s in f["sentences"]})
    out = set()
    for speciality, numberings in seen.items():
        for i, a in enumerate(numberings):
            for b in numberings[i + 1:]:
                if (any(a.get(n, t) != t for n, t in b.items())
                        or {t: n for n, t in a.items() if t in b.values()}
                        != {t: n for n, t in b.items() if t in a.values()}):
                    out.add(speciality)
    return out


def _by_text(area: str, plan_marks: dict[str, list[dict]], renumbered: set[str]) -> list[dict]:
    """G114 (1.4.33): for a renumbered speciality, one `mark_conflicts` row per
    sentence text that two plans mark differently (each side marked), this
    area's as by number: {"speciality", "n" (the first plan's), "text",
    "marks", "agrees_for", "differs_for", "compared": "by text", "n_by_plan"}.
    Its `numbering differs` rows still follow, so each disagreement is listed once
    by text and the renumbering once by number."""
    by_text: dict[tuple[str, str], dict] = {}
    for plan in sorted(plan_marks):
        for f in plan_marks[plan]:
            if f["speciality"] not in renumbered:
                continue
            for s in f["sentences"]:
                mark = f["marks"].get(str(s["n"]))
                if not areas_of(mark):
                    continue
                seen = by_text.setdefault((f["speciality"], s["text"]), {"n": s["n"], "marks": {}, "at": {}})
                seen["marks"][plan] = mark
                seen["at"][plan] = s["n"]
    rows = []
    for (speciality, text), seen in by_text.items():
        marks = seen["marks"]
        named = {a for m in marks.values() for a in areas_of(m)}
        first = next(iter(marks.values()))
        if any(not _same(first, m) for m in marks.values()) and (area in marks or area in named):
            rows.append({"speciality": speciality, "n": seen["n"], "text": text,
                         "marks": dict(sorted(marks.items())), **_agreement(marks.values()),
                         "compared": "by text", "n_by_plan": dict(sorted(seen["at"].items()))})
    return rows


def _agreement(marks) -> dict:
    """G71 (1.4.25): `agrees_for`, the areas every side's mark names, and
    `differs_for`, the areas some side's mark leaves out. A plan whose area
    is not in `differs_for` agrees with every side for itself."""
    sets = [set(areas_of(m)) for m in marks]
    every, some = set.intersection(*sets), set.union(*sets)
    return {"agrees_for": sorted(every), "differs_for": sorted(some - every)}


def _numbering(area: str, plan_marks: dict[str, list[dict]]) -> list[dict]:
    """N-B (fix round 2): two plans' marks files for one speciality that
    number it differently, one of them stale. A row per sentence whose text
    one file has at another n (copies paired in order), and per n the two
    files give different text; only where either side is marked and the row
    is this area's (a plan of it, or a mark naming it).
    Each row: {"speciality", "reason": "numbering differs", "plans": [{"plan",
    "n", "text", "mark"}, ...]}, with no `agrees_for`/`differs_for` (1.4.26:
    the two marks are for different sentences, so no side agrees)."""
    files: dict[str, dict[str, dict]] = {}
    for plan in sorted(plan_marks):
        for f in plan_marks[plan]:
            files.setdefault(f["speciality"], {})[plan] = f
    rows = []
    for speciality, by_plan in files.items():
        plans = sorted(by_plan)
        for i, pa in enumerate(plans):
            for pb in plans[i + 1:]:
                a, b = by_plan[pa], by_plan[pb]
                ta = {s["n"]: s["text"] for s in a["sentences"]}
                tb = {s["n"]: s["text"] for s in b["sentences"]}
                pairs = {(n, n) for n in ta if n in tb and ta[n] != tb[n]}   # one n, two texts
                at_b: dict[str, list[int]] = {}
                for n in sorted(tb):
                    at_b.setdefault(tb[n], []).append(n)
                for n in sorted(ta):                                         # one text, two n
                    if at_b.get(ta[n]):
                        m = at_b[ta[n]].pop(0)
                        if m != n:
                            pairs.add((n, m))
                for na, nb in sorted(pairs):
                    ma, mb = a["marks"].get(str(na)), b["marks"].get(str(nb))
                    named = set(areas_of(ma)) | set(areas_of(mb))
                    if not named or not (area in (pa, pb) or area in named):
                        continue
                    rows.append({"speciality": speciality, "reason": "numbering differs", "plans": [
                        {"plan": pa, "n": na, "text": ta[na], "mark": ma},
                        {"plan": pb, "n": nb, "text": tb[nb], "mark": mb}]})   # M5: no agreement fields
    return rows


def _copies(area: str, worklist: dict, speciality_map: list, references: list, result: dict) -> None:
    """Fill `against_survivor` and `survivor_elsewhere`: a speciality whose
    topic is a copy is measured in its survivor's area, against the survivor."""
    survivor_of = {c["folder"]: t["survivor"] for t in _paths(worklist)
                   for c in t.get("copies", []) if c.get("folder") and c["folder"] != t["survivor"]}
    files = _files(references)
    for row in speciality_map:
        copy = str(row.get("topic") or "").removeprefix("cookbook/").rstrip("/")
        if copy not in survivor_of:
            continue
        survivor = survivor_of[copy]
        names = {"speciality": row["speciality"], "copy": f"cookbook/{copy}", "survivor": f"cookbook/{survivor}"}
        if _area(survivor) == area:
            result["against_survivor"].append({**names, "file": files.get(row["speciality"])})
        elif _area(copy) == area:
            result["survivor_elsewhere"].append(names)


IGNORED_WHY = ("not an area folder: it has no area-plan.md or reference.json, or lies inside another area's "
               "folder (a backup?); its marks are not read. Keep old outputs in the scratchpad under a "
               "per-area name (stage-1.md, A re-run)")


def _is_area(folder: Path, root: Path, area: str) -> bool:
    """G109 (1.4.33): this area's own folder, or a folder holding area-plan.md
    or reference.json that lies inside no other such folder below `root`."""
    if folder == root / area:
        return True
    if not ((folder / "area-plan.md").is_file() or (folder / "reference.json").is_file()):
        return False
    return not any((up / "area-plan.md").is_file() or (up / "reference.json").is_file()
                   for up in folder.parents if root in up.parents)


def plan_marks(workspace: Path, area: str, ignored: list | None = None) -> tuple[dict[str, list[dict]], list[dict]]:
    """({plan area: [marks files]}, unread) from each <workspace>/areas/<area>/building-*.json
    directly in an area folder (`_is_area`); any other is appended to `ignored`
    ({"file", "why"}), never read (G109). This area's unreadable file exits 2;
    another area's is skipped, listed in unread."""
    root = workspace / "areas"
    out: dict[str, list[dict]] = defaultdict(list)
    unread = []
    for f in sorted(root.rglob("building-*.json")) if root.is_dir() else []:
        if not _is_area(f.parent, root, area):
            if ignored is not None and not f.name.endswith("-quoted.json"):
                ignored.append({"file": str(f), "why": IGNORED_WHY})
            continue
        plan = f.parent.relative_to(root).as_posix()
        try:
            data = json.loads(f.read_text(encoding="utf-8"))
        except (OSError, ValueError) as e:
            if plan == area:
                raise SystemExit(f"unmeasured.py: cannot read {f} ({e.__class__.__name__})") from e
            unread.append({"file": str(f), "plan": plan, "why": e.__class__.__name__})
            continue
        if isinstance(data, dict) and {"speciality", "sentences", "marks"} <= set(data):
            out[plan].append(data)
    return out, unread


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    add_area(parser)
    parser.add_argument("--workspace", type=Path, required=True)
    parser.add_argument("--reference", type=Path, help="default: <workspace>/areas/<area>/reference.json (G139)")
    parser.add_argument("--repo", help="the cookbook repo, as every script takes it (G76); this script reads "
                        "only the workspace, so it is checked, not inferred")
    parser.add_argument("--check", action="store_true",
                        help="write nothing: compare with the saved A/unmeasured.json and print what changed")
    parser.add_argument("--digest", action="store_true", help="one line for Step-4 re-check, of a --check (G137); "
                        "alone it is --check --digest (gapfix13 G261)")
    parser.add_argument("--rows", metavar="KEY[,KEY]", help="print each output key named whole (with --check, of "
                        "the check) (gapfix13 G261)")
    parser.add_argument("--keys", "--summary", action="store_true",
                        help="each output key with its shape; changes, new_keys, stale_reference whole (G138)")
    args = parser.parse_args(argv)
    args.area = area_arg(parser, args)
    from repo_path import check_area
    why = check_area("unmeasured.py", args.workspace, args.area, getattr(args, "repo", None))      # G198 (1.4.39)
    if why:
        print(why, file=sys.stderr)
        return 2
    if args.digest:
        args.check = True       # gapfix13 (G261): a digest is always a check's
    if args.reference is None:
        args.reference = args.workspace / "areas" / args.area / "reference.json"
    saved_file = args.workspace / "areas" / args.area / "unmeasured.json"
    try:
        if args.repo is not None:
            cookbook_repo(args.repo, "unmeasured.py")
        ignored: list[dict] = []
        marks, unread = plan_marks(args.workspace, args.area, ignored)
        references = _load(args.reference)
        result = place(args.area, _load(args.workspace / "worklist.json"),
                       _load(args.workspace / "speciality-map.json"), references, marks)
    except SystemExit as e:
        print(e, file=sys.stderr)
        return 2
    result["unread_marks"] = unread
    result["ignored_marks"] = ignored          # G109 (1.4.33)
    for u in ignored:
        print(f"unmeasured.py: ignored {u['file']}: {u['why']}", file=sys.stderr)
    for u in unread:
        print(f"unmeasured.py: skipped {u['file']}, another area's marks file ({u['why']})", file=sys.stderr)
    if args.check:
        try:
            saved = _load(saved_file)
        except SystemExit as e:
            print(e, file=sys.stderr)
            return 2
        new_keys: list[str] = []
        found = changes(saved, result, new_keys=new_keys)
        stale = stale_reference(references)      # R-I-1: never compared as if current
        if stale:
            found.append({"path": "stale_reference", "added": [r["speciality"] for r in stale], "removed": []})
        out = {"area": args.area, "check": "changed" if found else "unchanged", "saved_file": str(saved_file),
               "stale_reference": stale, "changes": found, **({"new_keys": new_keys} if new_keys else {})}
        code = _unplaced(result) or (1 if found else 0)    # M4: as a run does
        if args.digest:
            sys.stderr.flush()
            print(digest(out))      # gapfix13 (G261): the digest line prints last
        elif args.rows is not None:
            return _rows(out, args.rows, code)
        else:
            json.dump(output_keys(out) if args.keys else cap(out), sys.stdout, indent=2)
            print()
        return code
    for r in stale_reference(references):
        print(f"unmeasured.py: A/reference.json row {r['speciality']} is stale, {r['why']}", file=sys.stderr)
    if args.rows is not None:
        return _rows(result, args.rows, _unplaced(result))
    json.dump(output_keys(result) if args.keys else result, sys.stdout, indent=2)
    print()
    return _unplaced(result)


def _rows(result: dict, key: str, code: int) -> int:
    """gapfix13 (G261, 1.4.42): `--rows a,b` prints each key whole, in order,
    as stage_status.py and run_gaps.py do; 2 naming the owner of an unknown one."""
    from json_keys import owner_of, split_keys
    for k in split_keys(key):
        if k not in result:
            owner = owner_of(k, "unmeasured.py")
            print(f"unmeasured.py: no output key {k!r}" + (f"; {owner}" if owner else "")
                  + f"; keys: {', '.join(result)}", file=sys.stderr)
            return 2
    print(json.dumps({k: result[k] for k in split_keys(key)}, indent=2))
    return code


def digest(out: dict) -> str:
    """G137 (1.4.36): one line for Step-4 re-check, a hash over what the
    check found (its saved_file path aside)."""
    picked = {k: out.get(k, []) for k in ("check", "changes", "new_keys", "stale_reference")}
    h = hashlib.sha1(json.dumps(picked, sort_keys=True, default=str).encode("utf-8")).hexdigest()[:12]
    return (f"unmeasured.py {out['area']}: check {out['check']}; changes {len(out['changes'])}; "
            f"new_keys {len(out.get('new_keys', []))}; stale_reference {len(out['stale_reference'])}; result {h}")


def _unplaced(result: dict) -> int:
    """2, naming each speciality the worklist places in no area; else 0."""
    if result["unplaced"]:
        names = ", ".join(u["speciality"] for u in result["unplaced"])
        print(f"unmeasured.py: the worklist places no area for: {names}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    from repo_path import run_main      # gapfix13 (G263, G271)
    run_main(main)
