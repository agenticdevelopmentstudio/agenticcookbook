"""The worklist for converting every guideline topic to roles.

cookr inventories the cookbook itself, and joins three input files that say
everything it cannot know: who reviews each topic, how topics are batched, and
which topics are still to be written.

**Inventory.** A *topic* is a distinct guideline folder name. The same topic
often sits in several use-case folders; one folder survives and the others are
its *copies*, folded into it. The survivor is the first by use case:
`implementing/`, then `planning/`, `testing/`, `shipping/`, the other use cases
by name, and `reviewing/` last (a reviewing copy's text becomes review focus,
and no role may live under `reviewing/`). A topic held only under
`reviewing/<area>/` moves to `implementing/<area>/` (`new_home`).

Each copy is compared with the survivor on the twins' shared text
(`twins.comparable`) as a sequence of lines. A ratio of NEAR_IDENTICAL or more
is `identical`; `exact` says the text is byte-equal. `fold_check` marks a copy
to read before folding: one below FOLD_CHECK_BELOW, or one the batches file
lists (a different topic that shares a name, say).

**--map** `{"specialities": [every speciality], "assignments": [{"speciality",
"case", "specialists", "topic" (or null)}], "covers": [{"speciality", "specialist",
"via"}]}`. An assignment names the folder (below the cookbook dir) a
speciality stands on; a cover says a speciality builds whatever `via` stands
on. Every declared speciality must be assigned, covered, or claimed by a new
row, and every name used must be declared.

**--batches** `{"labels": {key: name}, "areas": {area: key}, "default": key,
"overrides": {path: {"batch": key, "new_home": path}}, "fold_check": [copy]}`.
A topic's area is the folder below its use case in its home
(`security` in `guidelines/implementing/security/x`), or the use case itself.

**--new-rows** `{"rows": [{"path", "kind", "specialities", "owner_decision",
"note"}]}`: topics to write. A speciality a new row claims is listed on that
row alone, never also on the topic its assignment names.

A topic no speciality stands on is `authored`: its review parts are written
new. Any error in an input file names the file and its offenders.
"""

from __future__ import annotations

import difflib
import json
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Optional

from .artifact import load_folder
from .errors import CookbookError
from .markdown import ARTIFACT_FILE, in_versions
from .twins import comparable

NEAR_IDENTICAL = 0.9
FOLD_CHECK_BELOW = 0.2
USE_CASE_ORDER = ("implementing", "planning", "testing", "shipping")
REVIEWING = "reviewing"
GUIDELINES = "guidelines"


def _leaf(path: str) -> str:
    return path.rstrip("/").rsplit("/", 1)[-1]


def rank(rel: str) -> tuple:
    """Survivor order for a path below `guidelines/`."""
    use_case = rel.split("/", 1)[0]
    if use_case in USE_CASE_ORDER:
        return (0, USE_CASE_ORDER.index(use_case), rel)
    return (2 if use_case == REVIEWING else 1, use_case, rel)


def area_key(home: str) -> str:
    parts = home.removeprefix(f"{GUIDELINES}/").split("/")
    return parts[1] if len(parts) > 2 else parts[0]


def similarity(a: str, b: str) -> float:
    return difflib.SequenceMatcher(None, a.splitlines(), b.splitlines(), autojunk=False).ratio()


# ── input files ──────────────────────────────────────────────────────────────

def _read(path: Path, what: str) -> Any:
    try:
        return json.loads(Path(path).read_text("utf-8"))
    except FileNotFoundError:
        raise CookbookError(f"{what} {path}: no such file") from None
    except (OSError, UnicodeDecodeError) as e:
        raise CookbookError(f"{what} {path}: cannot read: {e}") from None
    except json.JSONDecodeError as e:
        raise CookbookError(f"{what} {path}: not JSON: {e}") from None


def _need(cond: bool, path: Path, msg: str) -> None:
    if not cond:
        raise CookbookError(f"{path}: {msg}")


def _strs(v: Any) -> bool:
    return isinstance(v, list) and all(isinstance(x, str) for x in v)


def _objects(data: Any, key: str, fields: dict[str, type], path: Path) -> list[dict]:
    rows = data.get(key)
    _need(isinstance(rows, list), path, f"`{key}` must be a list")
    for i, row in enumerate(rows):
        _need(isinstance(row, dict), path, f"`{key}[{i}]` is not an object")
        for f, t in fields.items():
            if t is list:
                ok, kind = _strs(row.get(f)), "a list of names"
            elif t is None:
                ok, kind = row.get(f) is None or isinstance(row.get(f), str), "a path or null"
            else:
                ok, kind = isinstance(row.get(f), t), t.__name__
            _need(ok, path, f"`{key}[{i}]` needs `{f}` ({kind})")
    return rows


@dataclass
class Inputs:
    specialities: list[str]
    assignments: list[dict]
    covers: list[dict]
    labels: dict[str, str]
    areas: dict[str, str]
    default: str
    overrides: dict[str, dict]
    fold_check: list[str]
    new_rows: list[dict]
    paths: dict[str, Path]


def read_inputs(map_path: Path, batches_path: Path, new_rows_path: Path) -> Inputs:
    m = _read(map_path, "--map")
    _need(isinstance(m, dict), map_path, "must be an object with `specialities`, `assignments`, `covers`")
    specs = m.get("specialities")
    _need(_strs(specs) and bool(specs), map_path, "`specialities` must be a non-empty list of names")
    dupes = sorted({s for s in specs if specs.count(s) > 1})
    _need(not dupes, map_path, f"`specialities` declares twice: {', '.join(dupes)}")
    assignments = _objects(m, "assignments", {"speciality": str, "case": str, "specialists": list,
                                              "topic": None}, map_path)
    covers = _objects(m, "covers", {"speciality": str, "specialist": str, "via": str}, map_path)

    b = _read(batches_path, "--batches")
    _need(isinstance(b, dict), batches_path, "must be an object")
    labels = b.get("labels")
    _need(isinstance(labels, dict) and bool(labels) and all(isinstance(v, str) for v in labels.values()),
          batches_path, "`labels` must map each batch key to its name")
    areas = b.get("areas", {})
    _need(isinstance(areas, dict), batches_path, "`areas` must map an area to a batch key")
    default = b.get("default")
    overrides = b.get("overrides", {})
    _need(isinstance(overrides, dict) and all(isinstance(v, dict) for v in overrides.values()),
          batches_path, "`overrides` must map a topic path to {batch, new_home}")
    fold_check = b.get("fold_check", [])
    _need(_strs(fold_check), batches_path, "`fold_check` must be a list of copy folders")
    bad = sorted({str(k) for k in [default, *areas.values(),
                                    *(o["batch"] for o in overrides.values() if "batch" in o)]
                  if k not in labels})
    _need(not bad, batches_path, f"batch keys not in `labels`: {', '.join(bad)}")

    n = _read(new_rows_path, "--new-rows")
    _need(isinstance(n, dict), new_rows_path, "must be an object with `rows`")
    new_rows = _objects(n, "rows", {"path": str, "kind": str, "specialities": list}, new_rows_path)
    return Inputs(specs, assignments, covers, labels, areas, default, overrides, fold_check, new_rows,
                  {"map": map_path, "batches": batches_path, "new-rows": new_rows_path})


# ── the inventory ────────────────────────────────────────────────────────────

@dataclass
class _Topic:
    name: str
    survivor: str
    copies: list[str]
    roled: bool
    shared: dict[str, str]


def inventory(cookbook: Path) -> dict[str, _Topic]:
    root = cookbook / GUIDELINES
    groups: dict[str, list[str]] = defaultdict(list)
    for manifest in root.rglob(ARTIFACT_FILE):
        if in_versions(manifest):
            continue
        groups[manifest.parent.name].append(manifest.parent.relative_to(cookbook).as_posix())
    topics = {}
    for name, folders in sorted(groups.items()):
        folders.sort(key=lambda f: rank(f.removeprefix(f"{GUIDELINES}/")))
        arts = {f: load_folder(cookbook / f) for f in folders}
        topics[name] = _Topic(name, folders[0], folders[1:], arts[folders[0]].roled,
                              {f: comparable(a) for f, a in arts.items()})
    return topics


def _home(t: _Topic, overrides: dict[str, dict]) -> str:
    """Where the topic lives after conversion."""
    if "new_home" in overrides.get(t.survivor, {}):
        return overrides[t.survivor]["new_home"]
    parts = t.survivor.split("/")
    if parts[1] == REVIEWING and not t.copies and len(parts) == 4:
        return "/".join([GUIDELINES, "implementing", parts[2], parts[3]])
    return t.survivor


def _offenders(path: Path, msg: str, names) -> None:
    names = sorted(set(names))
    if names:
        raise CookbookError(f"{path}: {msg}: {', '.join(names)}")


# ── the worklist ─────────────────────────────────────────────────────────────

def build(cookbook: Path, inp: Inputs) -> dict:
    topics = inventory(cookbook)
    folders = {f: t for t in topics.values() for f in [t.survivor, *t.copies]}
    declared = set(inp.specialities)
    pm, pb, pn = inp.paths["map"], inp.paths["batches"], inp.paths["new-rows"]

    # new rows: unique, new, declared
    new_paths = [r["path"] for r in inp.new_rows]
    _offenders(pn, "paths listed twice", [p for p in new_paths if new_paths.count(p) > 1])
    _offenders(pn, "paths not under guidelines/", [p for p in new_paths if not p.startswith(f"{GUIDELINES}/")])
    _offenders(pn, "paths that already exist", [p for p in new_paths if (cookbook / p / ARTIFACT_FILE).is_file()])
    claimed: dict[str, str] = {}
    for r in inp.new_rows:
        for s in r["specialities"]:
            _offenders(pn, "a speciality claimed by two new rows", [s] if s in claimed else [])
            claimed[s] = r["path"]
    _offenders(pn, "specialities not declared in --map", set(claimed) - declared)

    # map: declared, assigned once, topics exist
    assigned = [a["speciality"] for a in inp.assignments]
    _offenders(pm, "specialities assigned twice", [s for s in assigned if assigned.count(s) > 1])
    _offenders(pm, "specialities not declared", (set(assigned) | {c["speciality"] for c in inp.covers}
                                                 | {c["via"] for c in inp.covers}) - declared)
    _offenders(pm, "topics in neither the cookbook nor --new-rows",
               [a["topic"] for a in inp.assignments
                if a["topic"] is not None and not (cookbook / a["topic"] / ARTIFACT_FILE).is_file()
                and a["topic"] not in new_paths])
    _offenders(pm, "specialities assigned to no topic or new row",
               declared - {a["speciality"] for a in inp.assignments if a["topic"] is not None}
               - set(claimed) - {c["speciality"] for c in inp.covers})

    # batches file: overrides and fold_check name real folders
    homes = {t.name: _home(t, inp.overrides) for t in topics.values()}
    known = {t.survivor for t in topics.values()} | set(homes.values()) | set(new_paths)
    _offenders(pb, "overrides for no topic", set(inp.overrides) - known)
    copies = {c for t in topics.values() for c in t.copies}
    _offenders(pb, "fold_check folders that are no copy", set(inp.fold_check) - copies)

    def batch(survivor: str, home: str) -> str:
        for key in (survivor, home):
            if "batch" in inp.overrides.get(key, {}):
                return str(inp.overrides[key]["batch"])
        return str(inp.areas.get(area_key(home), inp.default))

    # where each speciality stands: a claiming new row wins over its assignment
    stands: dict[str, str] = {}
    entries: dict[str, list[dict]] = defaultdict(list)     # row path -> devteam entries
    outside = 0
    for a in sorted(inp.assignments, key=lambda a: a["speciality"]):
        entry = {"speciality": a["speciality"], "case": a["case"], "specialists": list(a["specialists"])}
        s = a["speciality"]
        if s in claimed:
            path = claimed[s]
        elif a["topic"] in folders:
            path = homes[folders[a["topic"]].name]
        elif a["topic"] in new_paths:
            path = a["topic"]
        else:
            outside += 1             # a principle or other non-guideline artifact
            continue
        stands[s] = path
        entries[path].append(entry)
    by_spec = {a["speciality"]: a for a in inp.assignments}
    for s, path in claimed.items():
        stands[s] = path
        if s not in by_spec:
            entries[path].append({"speciality": s, "case": "new", "specialists": []})

    fold_check = set(inp.fold_check)
    rows = []
    for t in topics.values():
        home = homes[t.name]
        cs = []
        for c in t.copies:
            ratio = similarity(t.shared[t.survivor], t.shared[c])
            cs.append({"folder": c, "identical": ratio >= NEAR_IDENTICAL,
                       "exact": t.shared[c] == t.shared[t.survivor], "similarity": round(ratio, 3),
                       "fold_check": ratio < FOLD_CHECK_BELOW or c in fold_check})
        rows.append({"topic": t.name, "survivor": t.survivor,
                     **({"new_home": home} if home != t.survivor else {}),
                     "batch": batch(t.survivor, home), "copies": sorted(cs, key=lambda c: c["folder"]),
                     "devteam": entries.get(home) or "authored", "roled": t.roled, "new": False,
                     "kind": "existing", "owner_decision": False})
    for r in inp.new_rows:
        rows.append({"topic": _leaf(r["path"]), "survivor": r["path"], "batch": batch(r["path"], r["path"]),
                     "copies": [], "devteam": entries.get(r["path"]) or "authored", "roled": False,
                     "new": True, "kind": r["kind"], "owner_decision": bool(r.get("owner_decision", False)),
                     **({"note": r["note"]} if r.get("note") else {})})

    row_of = {r.get("new_home", r["survivor"]): r for r in rows}
    building, seen, on_outside = [], set(), 0
    for c in inp.covers:
        path = stands.get(c["via"])
        if path is None:
            on_outside += 1
            continue
        if (c["speciality"], path) in seen:
            continue
        seen.add((c["speciality"], path))
        building.append({"speciality": c["speciality"], "specialist": c["specialist"], "via": c["via"],
                         "topic": path, "batch": row_of[path]["batch"]})

    batches = []
    for key, name in inp.labels.items():
        mine = sorted((r for r in rows if r["batch"] == key),
                      key=lambda r: (r.get("new_home", r["survivor"]), r["topic"]))
        bmine = sorted((b for b in building if b["batch"] == key), key=lambda b: (b["speciality"], b["topic"]))
        batches.append({"batch": key, "name": name, "topics": mine, "building": bmine})

    existing = [r for r in rows if not r["new"]]
    all_copies = [c for r in existing for c in r["copies"]]
    kinds: dict[str, int] = defaultdict(int)
    for r in rows:
        if r["new"]:
            kinds[r["kind"]] += 1
    counts = {
        "topics": len(existing),
        "copies": len(all_copies),
        "copies_identical": sum(c["identical"] for c in all_copies),
        "copies_differing": sum(not c["identical"] for c in all_copies),
        "copies_exact": sum(c["exact"] for c in all_copies),
        "copies_fold_check": sum(c["fold_check"] for c in all_copies),
        "authored": sum(r["devteam"] == "authored" for r in existing),
        "roled": sum(r["roled"] for r in existing),
        "new": dict(sorted(kinds.items())),
        "owner_decision": sum(r["owner_decision"] for r in rows),
        "building": len(building),
        "assignments_outside_the_guidelines": outside,
        "covers_outside_the_guidelines": on_outside,
        "per_batch": {b["batch"]: {"topics": sum(not r["new"] for r in b["topics"]),
                                   "new": sum(r["new"] for r in b["topics"]),
                                   "building": len(b["building"])} for b in batches},
    }
    return {"counts": counts, "batches": batches}


def worklist(cookbook: Path, map_path: Path, batches_path: Path, new_rows_path: Path) -> dict:
    inp = read_inputs(map_path, batches_path, new_rows_path)
    return {"inputs": {k: str(v) for k, v in inp.paths.items()},
            "near_identical": NEAR_IDENTICAL, "fold_check_below": FOLD_CHECK_BELOW, **build(cookbook, inp)}
