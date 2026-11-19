#!/usr/bin/env python3
"""What a merged copy holds that its survivor does not, before the fold.

    python3 copy_check.py <area> --workspace W --repo R

The worklist's `identical`/`exact` compare text loosely: a copy it calls
identical may differ in link targets, version, history or meta references,
and folding deletes a copy whose UUID other guidelines link to (G58,
1.4.24). For each copy of this area (a `merged` row of `W/areas/<area>/
area-plan.md` whose Artifact is another folder, and each worklist `copies`
folder in this area: `direction` "out"; and each worklist copy, from any
area, planned or not, whose survivor is in this area: "in", G74), this
compares the copy folder with its survivor and prints JSON: {"area",
"twin_differs": [{"copy", "survivor", "copy_says", "survivor_says"}] (every
copy where either side's artifact.json records `twin_differs`, an owner's
intended difference: reported first, an owner question before any fold),
"copies": [{"twin_differs": {"copy_says", "survivor_says"} | null, "topic",
"copy", "survivor", "direction", "from" (["plan"], ["worklist"] or both),
"worklist_says": {"identical", "exact"} | null, "identical": bool, "top":
[{"key", "copy", "survivor"}] (every other top-level artifact.json key that
differs, `twin_differs` among them, stamps aside), "parts": {"only_copy", "only_survivor", "differ":
[{"part", "diff": [unified diff lines, survivor to copy: `+` is the
copy's]}] (carried parts), "differ_uncarried": [the same, for `history`
and `intro`, which a fold never carries as content, G107]}, "meta":
[{"key", "copy", "survivor"}] (every artifact.json meta key that differs,
`id` and stamps aside: `triggers` and `platforms` among them), "stamps":
[{"key", "copy", "survivor"}] (top `synced` and meta `approved-by`,
`approved-date`, `modified` as `meta.<key>`: never carried, never against
`identical`, G106), "kept": bool (the copy's own area plan keeps it as a
twin, G107), "links": {"only_copy", "only_survivor"} (link targets and
`cookbook:<uuid>` references in the parts' text), "linked_by": [every file
under R/cookbook, outside the copy's own folder, naming the copy's UUID],
"linked_by_folded": [{"file", "copy"}] (each of those files that is itself
in a copy a fold deletes, a worklist copy or a `merged` copy of any area's
plan: its link moves with that fold too)}],
"moved": [{"topic", "copy", "survivor"}] (a copy whose folder does not
exist: a record of a move, nothing to fold), "unreadable": [{"folder",
"why"}]}. Step 3 lists this under Overlaps; the fold carries everything it
names. `--summary` prints the same rows with names only (`differ`,
`differ_uncarried`, `meta`, `top`, `stamps` as lists of names), no diff
lines; G143 (1.4.36): each `meta` row keeps its copy and survivor values,
each cut to 80 characters, and each `differ_uncarried` part its first
changed line (`first_line`; `-` is the survivor's line, `+` the copy's).
G175 (1.4.37): a --summary row leaves out every field with nothing in it
(an empty list or object, null, false), keeping topic, copy, survivor,
direction, from and `identical`. `--digest` (G133, 1.4.36) prints one line,
`copy_check.py <area>: copies N; identical N; moved N; unreadable N;
twin_differs N; differ_uncarried <copy:part,...|none>; result <hash>`, the
hash over the whole result: the plan records it under Overlaps and
stage_status.py's `stale_copy_check` compares it with a fresh run. `--area`
names the area as the positional does (G139). A missing worklist exits 2,
naming it. Stdlib only.
"""

from __future__ import annotations

import argparse
import difflib
import hashlib
import json
import os
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from repo_path import add_area, area_arg  # noqa: E402
from stage_status import plan_rows  # noqa: E402

_LINK = re.compile(r"\]\(([^)\s]+)\)|(cookbook:[0-9a-f-]{36})|(?<![(\w])(https?://[^\s)>\]]+)")


def _folder(path: str) -> str:
    path = path.strip().strip("`").rstrip("/")
    return "cookbook/" + path if path.startswith("guidelines/") else path


TOP_SKIP = ("meta", "parts", "format")   # artifact.json keys compared elsewhere, or not content
# G106 (1.4.33): stamps a fold never carries (the survivor keeps its own):
# listed under `stamps`, never against `identical`.
STAMPS_TOP = ("synced",)
STAMPS_META = ("approved-by", "approved-date", "modified")
# G107 (1.4.33): parts a fold never carries as content (the survivor's
# history gets its own bump line; its intro stays): `parts.differ_uncarried`.
UNCARRIED = ("history", "intro")


def _read(d: Path) -> tuple[dict, dict[str, str], dict]:
    """(meta, {part: text}, the other top-level keys, `twin_differs` among them)."""
    data = json.loads((d / "artifact.json").read_text(encoding="utf-8"))
    parts = {}
    for p in data.get("parts", []):
        f = d / f"{p['part']}.md"
        parts[p["part"]] = f.read_text(encoding="utf-8") if f.is_file() else ""
    return data.get("meta", {}), parts, {k: v for k, v in data.items() if k not in TOP_SKIP}


def _links(parts: dict[str, str]) -> set[str]:
    return {next(g for g in m.groups() if g) for text in parts.values() for m in _LINK.finditer(text)}


def _worklist_copies(worklist: dict):
    """(copy folder, worklist copy entry, survivor folder) for every worklist copy."""
    for batch in worklist.get("batches", []):
        for t in batch.get("topics", []):
            for c in t.get("copies") or []:
                if isinstance(c, dict) and c.get("folder") and t.get("survivor"):
                    yield _folder(c["folder"]), c, _folder(t["survivor"])


def pairs(area: str, workspace: Path) -> list[dict]:
    """Every copy of this area (`direction` "out") and every worklist copy,
    from any area, planned or not, whose survivor is in this area
    ("in", G74), each with its survivor, from the plan and the worklist."""
    prefix = f"cookbook/guidelines/{area}/"
    found: dict[str, dict] = {}
    for t, r in plan_rows(workspace / "areas" / area / "area-plan.md").items():
        copy = prefix + t
        if r["action"] == "merged" and r["artifact"] != copy:
            found[copy] = {"topic": t, "copy": copy, "survivor": _folder(r["artifact"]), "direction": "out",
                           "from": ["plan"], "worklist_says": None}
    worklist = json.loads((workspace / "worklist.json").read_text(encoding="utf-8"))
    for copy, c, survivor in _worklist_copies(worklist):
        if not (copy.startswith(prefix) or survivor.startswith(prefix)):
            continue
        says = {"identical": c.get("identical"), "exact": c.get("exact")}
        row = found.setdefault(copy, {"topic": copy.rsplit("/", 1)[-1], "copy": copy, "survivor": survivor,
                                      "direction": "out" if copy.startswith(prefix) else "in",
                                      "from": [], "worklist_says": None})
        row["from"].append("worklist")
        row["worklist_says"] = says
    return [found[k] for k in sorted(found)]


def folded(area: str, workspace: Path) -> set[str]:
    """Every copy folder a fold deletes: each worklist copy, any area, and
    each plan's `merged` copies, every area's plan (1.4.26, M6), this one's
    included."""
    worklist = json.loads((workspace / "worklist.json").read_text(encoding="utf-8"))
    areas = workspace / "areas"
    planned = {f.parent.relative_to(areas).as_posix() for f in areas.rglob("area-plan.md")} | {area}
    return {copy for copy, _, _ in _worklist_copies(worklist)} | {
        r["copy"] for a in sorted(planned) for r in pairs(a, workspace) if "plan" in r["from"]}


def linked_by(repo: Path, copy: str, uid: str) -> list[str]:
    out = []
    root = repo / "cookbook"
    for dirpath, _, files in os.walk(root):
        rel = Path(dirpath).relative_to(repo).as_posix()
        if rel == copy or rel.startswith(copy + "/"):
            continue
        for name in files:
            if name.endswith((".md", ".json")):
                try:
                    if uid in (Path(dirpath) / name).read_text(encoding="utf-8"):
                        out.append(f"{rel}/{name}")
                except (OSError, UnicodeDecodeError):
                    continue
    return sorted(out)


def compare(repo: Path, row: dict, gone: set[str] = frozenset()) -> dict:
    cmeta, cparts, ctop = _read(repo / row["copy"])
    smeta, sparts, stop = _read(repo / row["survivor"])
    differ_all = [{"part": p, "diff": list(difflib.unified_diff(
        sparts[p].splitlines(), cparts[p].splitlines(), f"{row['survivor']}/{p}.md", f"{row['copy']}/{p}.md",
        lineterm=""))} for p in sorted(set(cparts) & set(sparts)) if cparts[p] != sparts[p]]
    differ = [d for d in differ_all if d["part"] not in UNCARRIED]
    meta_all = [{"key": k, "copy": cmeta.get(k), "survivor": smeta.get(k)}
                for k in sorted(set(cmeta) | set(smeta)) if k != "id" and cmeta.get(k) != smeta.get(k)]
    top_all = [{"key": k, "copy": ctop.get(k), "survivor": stop.get(k)}
               for k in sorted(set(ctop) | set(stop)) if ctop.get(k) != stop.get(k)]
    top = [t for t in top_all if t["key"] not in STAMPS_TOP]
    meta = [m for m in meta_all if m["key"] not in STAMPS_META]
    stamps = [t for t in top_all if t["key"] in STAMPS_TOP] + [
        {**m, "key": f"meta.{m['key']}"} for m in meta_all if m["key"] in STAMPS_META]
    says = {"copy_says": ctop.get("twin_differs", cmeta.get("twin_differs")),
            "survivor_says": stop.get("twin_differs", smeta.get("twin_differs"))}
    cl, sl = _links(cparts), _links(sparts)
    out = {"twin_differs": says if says["copy_says"] or says["survivor_says"] else None, **row, "top": top,
           "parts": {"only_copy": sorted(set(cparts) - set(sparts)),
                     "only_survivor": sorted(set(sparts) - set(cparts)), "differ": differ,
                     "differ_uncarried": [d for d in differ_all if d["part"] in UNCARRIED]},
           "meta": meta, "stamps": stamps, "links": {"only_copy": sorted(cl - sl), "only_survivor": sorted(sl - cl)},
           "linked_by": linked_by(repo, row["copy"], cmeta["id"]) if cmeta.get("id") else []}
    out["linked_by_folded"] = [{"file": f, "copy": c} for f in out["linked_by"] for c in sorted(gone)
                               if f.startswith(c + "/")]
    out["identical"] = not (differ_all or meta or top or out["parts"]["only_copy"] or out["parts"]["only_survivor"])
    return out


def kept(copy: str, workspace: Path) -> bool:
    """G107 (1.4.33): the copy's own area plan keeps it (its row's Artifact
    is the copy itself): a twin beside the survivor, not a fold."""
    parts = copy.split("/")
    if len(parts) < 4 or parts[:2] != ["cookbook", "guidelines"]:
        return False
    row = plan_rows(workspace / "areas" / "/".join(parts[2:-1]) / "area-plan.md").get(parts[-1])
    return bool(row) and _folder(row["artifact"]) == copy


def _cut(v, n: int = 80):
    """A value as JSON text cut to n characters (G143); None stays None."""
    if v is None:
        return None
    t = v if isinstance(v, str) else json.dumps(v, ensure_ascii=False)
    return t if len(t) <= n else t[:n - 1] + "…"


def _first_line(diff: list[str]) -> str | None:
    """The first changed line of a unified diff, its `+`/`-` kept (G143)."""
    return next((d for d in diff if d[:1] in "+-" and not d.startswith(("+++", "---"))), None)


WHO = ("topic", "copy", "survivor", "direction", "from")


def summary(result: dict) -> dict:
    """G107 (1.4.33): `--summary`: every row with the names of what differs
    (parts, meta, top, stamps keys; links as listed), no diff lines. G143
    (1.4.36): each meta key with its copy and survivor values cut to 80
    characters, and each differ_uncarried part with its first changed line.
    G175 (1.4.37): a field with no difference in it is left out (WHO and
    `identical` stay), so an identical copy is a short row."""
    def names(c: dict) -> dict:
        return {**c, "parts": {**c["parts"], "differ": [d["part"] for d in c["parts"]["differ"]],
                               "differ_uncarried": [{"part": d["part"], "first_line": _first_line(d["diff"])}
                                                    for d in c["parts"]["differ_uncarried"]]},
                "meta": [{"key": m["key"], "copy": _cut(m["copy"]), "survivor": _cut(m["survivor"])}
                         for m in c["meta"]], "top": [t["key"] for t in c["top"]],
                "stamps": [t["key"] for t in c["stamps"]]}

    def lean(c: dict) -> dict:
        # G175 (1.4.37): who the row is and `identical` always; every other
        # field only when something is in it (an empty list, dict, null or
        # false says no difference).
        out = {}
        for k, v in c.items():
            if isinstance(v, dict) and k in ("parts", "links"):
                v = {s: x for s, x in v.items() if x}
            if k in WHO or k == "identical" or v:
                out[k] = v
        return out
    return {**result, "copies": [lean(names(c)) for c in result["copies"]]}


def digest(result: dict) -> str:
    """G133 (1.4.36): the one line the plan records under Overlaps."""
    h = hashlib.sha1(json.dumps(result, sort_keys=True, default=str).encode("utf-8")).hexdigest()[:12]
    unc = ",".join(f"{c['copy'].rsplit('/', 1)[-1]}:{d['part']}" for c in result["copies"]
                   for d in c["parts"]["differ_uncarried"]) or "none"
    return (f"copy_check.py {result['area']}: copies {len(result['copies'])}; "
            f"identical {sum(1 for c in result['copies'] if c['identical'])}; moved {len(result['moved'])}; "
            f"unreadable {len(result['unreadable'])}; twin_differs {len(result['twin_differs'])}; "
            f"differ_uncarried {unc}; result {h}")


def check(area: str, workspace: Path, repo: Path) -> dict:
    result = {"area": area, "twin_differs": [], "copies": [], "moved": [], "unreadable": []}
    gone = folded(area, workspace)
    for row in pairs(area, workspace):
        if not (repo / row["copy"]).is_dir():
            result["moved"].append({k: row[k] for k in ("topic", "copy", "survivor")})
            continue
        try:
            result["copies"].append({**compare(repo, row, gone), "kept": kept(row["copy"], workspace)})
        except (OSError, ValueError, KeyError, TypeError) as e:
            result["unreadable"].append({"folder": row["copy"], "why": f"{e.__class__.__name__}: {e}"})
    result["twin_differs"] = [{"copy": c["copy"], "survivor": c["survivor"], **c["twin_differs"]}
                              for c in result["copies"] if c["twin_differs"]]
    return result


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    add_area(ap)
    ap.add_argument("--workspace", type=Path, required=True)
    ap.add_argument("--repo", type=Path, required=True)
    ap.add_argument("--summary", action="store_true",
                    help="names of what differs, meta values cut to 80 characters and each differ_uncarried "
                         "part's first changed line, no diff lines (G107, G143)")
    ap.add_argument("--digest", action="store_true",
                    help="one line to record under Overlaps; stage_status.py compares it (G133)")
    a = ap.parse_args(argv)
    a.area = area_arg(ap, a)
    from repo_path import check_area
    why = check_area("copy_check.py", a.workspace, a.area, getattr(a, "repo", None))      # G198 (1.4.39)
    if why:
        print(why, file=sys.stderr)
        return 2
    try:
        result = check(a.area, a.workspace.resolve(), a.repo.resolve())
    except (OSError, ValueError) as e:
        print(f"copy_check.py: cannot read {a.workspace.resolve() / 'worklist.json'} "
              f"({e.__class__.__name__}: {e})", file=sys.stderr)
        return 2
    if a.digest:
        print(digest(result))
    else:
        print(json.dumps(summary(result) if a.summary else result, indent=2))
    return 0


if __name__ == "__main__":
    from repo_path import run_main      # gapfix13 (G263, G271)
    run_main(main)
