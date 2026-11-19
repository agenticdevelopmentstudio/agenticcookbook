#!/usr/bin/env python3
"""Where an area stands in /grow-cookbook: which stage files exist, per topic.

    stage_status.py <area> [--workspace DIR] [--repo DIR]

<area> is the area's path below cookbook/guidelines/. A relative DIR is
relative to the current directory; --workspace defaults to
<repo>/docs/grow-cookbook. Prints JSON:

    {"area", "dir", "plan": bool, "approval": "missing"|"current"|"stale",
     "approval_why": None|"no_record"|"plan_changed"|"reference_hash"|"reference_format",
     "reference_hash": str|None,
     "cookr": {"version": str|None, "minimum": "0.21.4", "ok": bool},
     "topics": {name: {"artifact": path, "folder": bool, "research": bool,
                       "second_check": bool,
                       "written": bool, "owner_list": bool,
                       "review": "missing"|"pass"|"fail",
                       "lint": "clean"|"fail"|"missing"|"malformed"|"no-section"|None,
                       "rounds": int, "owner": [finding ids, or for an
                                 integrated topic its routed findings],
                       "fold": [copy folders], "integrated": bool,
                       "merged": folder|None,
                       "next": stage|"stop"|None, "why": str}},
     "incoming": [{"topic", "plan", "copy", "artifact", "via"?}],
     "incoming_unplanned": [{"via", "topic", "copy", "survivor", "plan", "why"}],
     "conflicts": [{"topic", "plan", "copy", "artifact", "why"}
                   | {"kind": "double-keep", "topic", "plans", "artifact", "why"}],
     "pending_target": [{"kind": "merge", "topic", "plan", "copy", "artifact", "why"}
                        | {"kind": "keep", "topic", "plans", "artifact", "why"}],
     "speciality_points_at_copy": [{"speciality", "topic", "survivor", "why"}],
     "stale_gaps": [gaps file names] | {"refused": why},
     "stale_reference": [{"speciality", "file", "format", "want", "why", "reason"}],
     "next": stage|None, "next_why": str}

`stale_reference` (1.4.27, R-I-1) lists each A/reference.json row written
before reference_format.REFERENCE_FORMAT (`reason` "old_format"), each
`marked_here` reference A/run_gaps.json lists stale by its `reason`
"no_writer", never by the wording of its `why` (R2-M-2, 1.4.28; N3-M-2,
1.4.29), and A/run_gaps.json itself (`speciality` null, `reason`
"old_report") when it exists and its `reference_format` is missing, lower
than REFERENCE_FORMAT or unreadable (N3-I-1, 1.4.29): a `marked_here`
reference it measured may be stale with no run having listed it. The
same row stands for a report saved while it listed a stale row, an
"old_format" one or one with no `reason` (N4-I-1, 1.4.30): rewriting
A/reference.json without a re-run leaves a measure on the stale reference.
A fresh run_gaps.py run saves the report again and clears that row; with no
report nothing is listed. An A/reference.json that cannot be read as a
list of rows (invalid JSON, not a list, or holding a row that is not an
object), or absent beside an area-plan.md (step 1.1 always writes one,
`[]` for an area with no speciality; 1.4.32), is one row, `reason`
"unreadable_reference" (N5-I-1, 1.4.31): its
`reference_hash` is null and no approval of it is current. So is a report
whose `stale_reference` is not a list ("old_report", N5-M-1). It holds the area and every
topic not merged elsewhere at `next: plan`, approved or not (R2-I-1, 1.4.28):
the plan was measured on it, so steps 1.1-1.3 and step 4 re-run and the plan
goes back to the owner. `next_why` leads with it.

`approval` is `current` when a line of A/approval.md names the plan's
`git hash-object` and, on that same line, `reference-hash <hash>`, the
`git hash-object` of A/reference.json as it is now (N4-I-2, 1.4.30): any
rewrite of the rows changes the file, a format bump included, so the plan
goes back to the owner with nobody having to remember. `reference_hash` is
that hash for the owner to copy, null when the file is absent and null
while `stale_reference` lists any row: nobody approves over a stale
reference. `approval_why` says why an approval is not current:
"no_record", "plan_changed" (no line names the plan's hash),
"reference_hash" (none on that line, or not the file's) or
"reference_format" (the line records `reference-format`, the 1.4.29 form,
which approves nothing now). The owner's new approval is a new line; the
earlier lines stay as history.

`next_why` (G75) is one line saying why `next` is what it is ("no
area-plan.md yet", "...; every row merged elsewhere: approval is a record",
"<topics> owe <stage>", "no topic owes a stage here"), led by the
pending_target note when any row waits on a plan.

`incoming_unplanned` (G75) lists each worklist fold into this area that no
plan stands behind: a copy (its folder existing) or a `new_home` in another
area, whose survivor is in this area, that area having no plan yet, or a
plan with no row for it, or a row that does not merge it into this
survivor (1.4.26).

A merged row whose copy is a worklist `new_home` (no folder of its own: the
topic is reached through new_home, not as a copy) is a merge like a copy's,
never a record of a move: it is `incoming` in the survivor's area and
`pending_target` while that plan does not exist, with `"via": "new_home"`.

`speciality_points_at_copy` (G75) lists each `<workspace>/speciality-map.json`
row whose topic is a copy a fold deletes (a worklist copy no plan keeps, or
a plan's `merged` copy whose folder exists), the copy or its survivor in
this area: an owner item, who repoints it being the owner's.

`pending_target` (G47, 1.4.24) lists each merge into or out of this area
whose survivor's area has no plan yet, and each artifact this plan keeps in
an area with no plan yet: no conflict can be found there, so neither reads
as confirmed. While it is not empty, `next_why` leads with it (and the script
prints it on stderr); re-check once that plan is written.

`stale_gaps` lists each A/gaps/*.json that no topic of the area's current
measurement set (run_gaps.py: A/reference.json, A/unmeasured.json, the plan)
writes, an R9 `new-<name>.json` excepted: a gaps file a re-run did not
produce, never quoted or counted (1.4.18, G32). When two topic folders share a basename
the set is unknown: `stale_gaps` is {"refused": why} (1.4.19, M3).

A topic is any folder of the area in the cookbook, any topic under
<dir>/topics/, or any topic the plan proposes. Its `artifact` (its source
folder, relative to the repo) is the one the plan's "## Proposed topics" table
gives in its `Artifact` column, so a topic folded into or created under another
area is found there; a topic the plan does not place is
`cookbook/guidelines/<area>/<topic>`.

A topic whose plan row's `Action` is `merged` and whose `Artifact` folder is
in another area (not under `cookbook/guidelines/<area>/`) runs only under the
plan whose area holds that folder: here it is `merged` into that folder, its
`next` is None and its `why` is `merged into <folder>`. It owes nothing in
this area, not approval and not research, and the area's `next` ignores it.
Merged into a folder of this area, it runs here as usual (`merged` None).

A topic is `written` when base.txt exists, its artifact has a part of each of
the roles rules, review-focus, review-bar and build-bar, and every named rule
in its rules parts cites research (`(claim: …)`/`(claims: …)`): a topic roled
before research began is not written until stage 3 rewrites it.

`review` is review.md's effective verdict: `pass` only when its verdict line
says pass and its `## Lint` ends with `lint: clean`, so a round that cannot
pass never reads `pass`. `lint` is that `## Lint` line's state
(review_findings.lint_of); None with no review.md.

`rounds` counts the saved review rounds (review-N.md, write_brief.py append).
Once a written topic's review.md is counted, its `next` follows
review_findings.py status: a failed round below the cap owes "write" (the
author's next round), a pass or a recorded lossless failure's round passed
owes "integrate", a failed third round owes "integrate" with its open
findings listed in `owner` for integrate.md's "## For the owner"
(review_findings.py owner), and a lint error standing at the cap, a failed
round that a lossless failure opened, or a second lossless failure is "stop",
with `why`: it never goes to the owner. A lossless failure recorded by
write_brief.py lossless owes "write". A review.md not yet counted owes
"review" (stage 4's count step).

A topic is `integrated` when its integrate.md has the line `integrated:
<date>`, which stage 5 writes last; an integrate.md holding only findings for
the owner is not. An integrated topic is done (`next` None) before anything
else is looked at: its review files no longer route it. Its `owner` lists
each finding in a `## From <sibling>'s review` section of its integrate.md,
as `from <sibling>'s review: <finding>` (review_findings.routed): a finding
a sibling routed there after its stage 5 ran has no stage left to deliver it.

`fold` lists every merged copy stage 5 folds into the topic (`roles
lossless --copy`), whatever its `fold_check`: the `copies` of the
<workspace>/worklist.json batch topic whose `survivor` is this artifact,
except one that a plan's row keeps as an artifact of its own (its Artifact
is the copy's folder, its Action not `merged`), and the folder of every
topic another area's plan lists `merged` into this artifact, when that
folder exists.

`incoming` lists each topic another area's plan (any
<workspace>/areas/**/area-plan.md) lists `merged` into a folder of this area:
its `plan` (that area), its `copy` (`cookbook/guidelines/<plan>/<topic>`)
and its `artifact`. A merge is a `conflict`, an owner item, when the copy's
folder exists (one that does not is a record of a move, nothing to merge),
the plan of the area holding its artifact exists, and no row of its "## Proposed topics"
table names the copy (`<plan>/<topic>`, in any cell): the two plans disagree
on what the copy becomes. The plan names it as `<plan>/<topic>`, as
`guidelines/<plan>/<topic>` or as `cookbook/guidelines/<plan>/<topic>`, a whole path, in a cell of a
"## Proposed topics" row (prose and other tables do not count). `conflicts`
lists those touching this area, both the merges into it and this plan's merges
into another area, and every artifact this plan and another both keep (Action
`kept`): `{"kind": "double-keep", "topic", "plans", "artifact", "why"}`.

`cookr` is the repo's own cookr version (skills/cookr/SKILL.md's `version`);
`ok` is false below MINIMUM, and /grow-cookbook stops then.

`next` is the first stage a topic still owes, but "plan" for every topic until
the plan exists and "approve" until its approval is current; the area's `next`
is the same, else the earliest stage any topic owes. Exit 0; a missing area is not an error.

1.4.33: `old_report` also lists a plan with no saved A/run_gaps.json (G99);
the area is held at "plan" by `r9_stale` (G94: an R9 file measured on another
reference text or, 1.4.34, survivor folder) and `plan_sections` (G97/G105: a
required plan section missing, misspelled or out of order, or a Missing
subject not carried by its bold lead phrase into a Research question, as
stage-1.md step 3 says; 1.4.34), each a list of rows; `legacy_null` rows (a
`stale_reference` row with a null file) are counted apart in `next_why` (G108).
`--keys`/`--summary` prints each output key with its shape only (G119).

1.4.36: `plan_sections` also lists each topic of the plan's Topics table
that no Owner question about the research bar names (G128), each bold-led
Missing-subjects paragraph that is not a list item and each second bold
phrase of an item (G126); a Missing subject is carried only by its bold lead
phrase as a whole bold span or a whole list item, outside headings (G127: a
plain mention is "named but not carried"). `stale_copy_check` (G133, holds at
plan): the copy_check.py --digest line recorded under Overlaps is missing
(when the area has copies) or differs from a fresh run.
`other_plans_changed` (G134, advisory): each other area plan this plan cites
whose hash differs from the one recorded in Step-4 re-check, or, with none
recorded, that is newer than this plan. `survivor_carries` (G130, advisory):
each Research question of a copy-only plan whose first 60 characters no
survivor plan holds. `--keys` prints the rows of every hold and advisory
list (json_keys.ROW_KEYS); `--rows K` prints key K whole; `--digest` prints
one line for Step-4 re-check (G137); `--area A` names the area as the
positional does (G139).
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import review_findings  # noqa: E402
from json_keys import keys as output_keys  # noqa: E402
from reference_format import (NO_REPORT_WHY, NO_WRITER, REPORT_STALE_WHY, is_current, r9_stale, report_row,  # noqa: E402
                              stale_reference, unreadable_row)
from repo_path import add_area, area_arg, check_area, cookbook_repo, skill_version  # noqa: E402

MINIMUM = "0.21.4"
ROLES = ("rules", "review-focus", "review-bar", "build-bar")
_RULE = re.compile(r"^[-*+] \*\*[a-z0-9]+(?:-[a-z0-9]+)*\*\*:", re.M)
_CITATION = re.compile(r"\(claims?:[ \t]*[^)\n]*\)")
_ROW = re.compile(r"^\|(.*)\|\s*$")


def _version(text: str) -> tuple[int, ...]:
    return tuple(int(n) for n in re.findall(r"\d+", text)[:3])


def cookr(repo: Path) -> dict:
    """The repo's own cookr version, and whether it is at least MINIMUM."""
    f = repo / "skills" / "cookr" / "SKILL.md"
    m = re.search(r'^version:\s*"?([0-9.]+)"?\s*$', f.read_text(encoding="utf-8"), re.M) if f.is_file() else None
    version = m.group(1) if m else None
    return {"version": version, "minimum": MINIMUM,
            "ok": version is not None and _version(version) >= _version(MINIMUM)}


def plan_rows(plan: Path) -> dict[str, dict[str, str]]:
    """{topic: {"artifact": path, "action": lowercased Action or ""}} from the
    plan's "## Proposed topics" table (columns include `Topic` and `Artifact`,
    and may include `Action`; backticks around a cell are dropped)."""
    if not plan.is_file():
        return {}
    section = re.split(r"^## ", plan.read_text(encoding="utf-8"), flags=re.M)
    body = next((s for s in section if s.lower().startswith("proposed topics")), "")
    rows = [[c.strip().strip("`").strip() for c in m.group(1).split("|")]
            for m in map(_ROW.match, body.splitlines()) if m]
    if not rows:
        return {}
    head = [c.lower() for c in rows[0]]
    if "topic" not in head or "artifact" not in head:
        return {}
    ti, ai = head.index("topic"), head.index("artifact")
    ci = head.index("action") if "action" in head else None
    return {r[ti]: {"artifact": r[ai].rstrip("/"),
                    "action": r[ci].lower() if ci is not None and len(r) > ci else ""}
            for r in rows[1:]
            if len(r) > max(ti, ai) and r[ti] and r[ai] and not set(r[ti]) <= set("-: ")}


def plan_cells(plan: Path) -> list[str]:
    """Each "## Proposed topics" row's cells, joined, for a name search."""
    if not plan.is_file():
        return []
    section = re.split(r"^## ", plan.read_text(encoding="utf-8"), flags=re.M)
    body = next((s for s in section if s.lower().startswith("proposed topics")), "")
    return [m.group(1) for m in map(_ROW.match, body.splitlines()) if m]


def _names(rows: list[str], copy: str) -> bool:
    """Whether a row names `copy` (`<area>/<topic>`) as a whole path:
    `<area>/<topic>`, the worklist's `guidelines/<area>/<topic>` or
    `cookbook/guidelines/<area>/<topic>`, a trailing `/` allowed, never inside
    a longer path (`.../python-typing`, `x/<copy>`, `<copy>/part`)."""
    pattern = re.compile(rf"(?<![\w./-])(?:(?:cookbook/)?guidelines/)?{re.escape(copy)}(?!/?[\w-])")
    return any(pattern.search(r) for r in rows)


def all_merges(workspace: Path) -> list[dict]:
    """Every `merged` row of every plan under <workspace>/areas/ whose
    Artifact is not the topic's own folder: {"topic", "plan", "copy",
    "artifact"}, the plan's area as `plan`."""
    root = workspace / "areas"
    out = []
    for f in sorted(root.rglob("area-plan.md")) if root.is_dir() else []:
        plan_area = f.parent.relative_to(root).as_posix()
        for t, r in plan_rows(f).items():
            copy = f"cookbook/guidelines/{plan_area}/{t}"
            if r["action"] == "merged" and r["artifact"] != copy:
                out.append({"topic": t, "plan": plan_area, "copy": copy, "artifact": r["artifact"]})
    return out


def _area_of(folder: str) -> str:
    return folder.removeprefix("cookbook/guidelines/").rsplit("/", 1)[0]


def _cb(folder: str) -> str:
    folder = str(folder or "").strip().strip("`").rstrip("/")
    return folder if folder.startswith("cookbook/") or not folder else "cookbook/" + folder


def _worklist_topics(workspace: Path) -> list[dict]:
    try:
        batches = json.loads((workspace / "worklist.json").read_text(encoding="utf-8")).get("batches", [])
        return [t for b in batches for t in b.get("topics", []) if isinstance(t, dict) and t.get("survivor")]
    except (OSError, ValueError, AttributeError):
        return []


def new_homes(workspace: Path) -> dict[str, str]:
    """{new_home folder: survivor folder} from the worklist, `cookbook/`-prefixed."""
    return {_cb(t["new_home"]): _cb(t["survivor"]) for t in _worklist_topics(workspace) if t.get("new_home")}


def _live(m: dict, repo: Path, homes: dict) -> dict | None:
    """A merge to check, or None for a record of a move: its copy folder
    exists, or the copy is a worklist `new_home` (G75: reached through
    new_home, with no folder of its own; the row carries `via`)."""
    if (repo / m["copy"]).is_dir():
        return m
    return {**m, "via": "new_home"} if m["copy"] in homes else None


def kept_by(workspace: Path) -> dict[str, list[str]]:
    """{artifact: [plan areas]} for every plan row whose Action is `kept`."""
    root = workspace / "areas"
    out: dict[str, list[str]] = {}
    for f in sorted(root.rglob("area-plan.md")) if root.is_dir() else []:
        for r in plan_rows(f).values():
            if r["action"] == "kept":
                out.setdefault(r["artifact"], []).append(f.parent.relative_to(root).as_posix())
    return out


def cross_check(area: str, workspace: Path, repo: Path) -> tuple[list[dict], list[dict]]:
    """(incoming, conflicts) for `area`: merges into its folders, and every
    merge into or out of it that the target plan does not list, or whose copy
    another plan keeps as its own artifact (Action `kept`). Only a copy whose
    folder exists is a merge: a merged row whose copy folder does not exist
    records a move, as `fold` treats it. An artifact two or more plans keep,
    this area's among them, is a conflict too (two runs of one artifact), with
    fields of its own: {"kind": "double-keep", "topic", "plans" (every keeping
    plan, sorted), "artifact", "why"}, the same entry in every keeping area. A
    merge conflict has no `kind`."""
    incoming, conflicts = [], []
    kept = kept_by(workspace)
    homes = new_homes(workspace)
    for m in all_merges(workspace):
        target = _area_of(m["artifact"])
        m = _live(m, repo, homes)
        if m is None or target == m["plan"]:
            continue  # a record of a move, or a merge within one area (its own plan lists it)
        if target == area:
            incoming.append(m)
        if area not in (target, m["plan"]):
            continue
        plan = workspace / "areas" / target / "area-plan.md"
        copy = m["copy"].removeprefix("cookbook/guidelines/")
        why = [f"the {target} plan does not list {m['copy']}"
               if plan.is_file() and not _names(plan_cells(plan), copy) else None]
        why += [f"{k} keeps {m['copy']}, {m['plan']} merges it into {m['artifact']}"
                for k in kept.get(m["copy"], [])]
        if any(why):
            conflicts.append({**m, "why": "; ".join(w for w in why if w)})
    for artifact, plans in sorted(kept.items()):
        plans = sorted(set(plans))
        if len(plans) > 1 and area in plans:
            conflicts.append({"kind": "double-keep", "topic": artifact.rsplit("/", 1)[-1], "plans": plans,
                              "artifact": artifact, "why": f"{' and '.join(plans)} both keep {artifact}"})
    return incoming, conflicts


def pending_target(area: str, workspace: Path, repo: Path) -> list[dict]:
    """G47: every row touching `area` that cross_check cannot confirm because
    the plan it needs does not exist yet: a merge into or out of the area whose
    survivor's area has no plan ({"kind": "merge", "topic", "plan", "copy",
    "artifact", "why"}), and an artifact this plan keeps in an area with no
    plan ({"kind": "keep", "topic", "plans", "artifact", "why"}). Not a
    conflict, never clean: it is re-checked once that plan is written."""
    out = []
    homes = new_homes(workspace)
    for m in all_merges(workspace):
        target = _area_of(m["artifact"])
        m = _live(m, repo, homes)
        if m is None or target == m["plan"] or area not in (target, m["plan"]):
            continue
        if not (workspace / "areas" / target / "area-plan.md").is_file():
            out.append({"kind": "merge", **m,
                        "why": f"the {target} plan does not exist yet: nothing confirms this merge"})
    for artifact, plans in sorted(kept_by(workspace).items()):
        target = _area_of(artifact)
        if area in plans and target != area and not (workspace / "areas" / target / "area-plan.md").is_file():
            out.append({"kind": "keep", "topic": artifact.rsplit("/", 1)[-1], "plans": sorted(set(plans)),
                        "artifact": artifact, "why": f"the {target} plan does not exist yet: "
                                                     "nothing confirms no other plan keeps it"})
    return out


def incoming_unplanned(area: str, workspace: Path, repo: Path) -> list[dict]:
    """G75: every worklist fold into this area that no plan stands behind: a
    copy (its folder existing) or a `new_home` in another area whose
    survivor is in this area, that area having no plan yet, or (1.4.26, M7)
    a plan with no row for it or a row that does not merge it into this
    survivor. {"via": "copy" | "new_home", "topic", "copy", "survivor",
    "plan", "why"}."""
    out = []
    for t in _worklist_topics(workspace):
        survivor = _cb(t["survivor"])
        if _area_of(survivor) != area:
            continue
        found = [("copy", _cb(c["folder"])) for c in t.get("copies") or []
                 if isinstance(c, dict) and c.get("folder") and (repo / _cb(c["folder"])).is_dir()]
        found += [("new_home", _cb(t["new_home"]))] if t.get("new_home") else []
        for via, copy in found:
            plan = _area_of(copy)
            if plan == area or copy == survivor:
                continue
            path = workspace / "areas" / plan / "area-plan.md"
            base = copy.rsplit("/", 1)[-1]
            row = plan_rows(path).get(base)
            if not path.is_file():
                why = f"the {plan} plan does not exist yet: no plan stands behind this fold"
            elif row is None:      # M7 (1.4.26): a plan that omits the fold
                why = f"the {plan} plan does not list {copy}: no plan row stands behind this fold"
            elif row["action"] != "merged" or _cb(row["artifact"]) != survivor:
                why = (f"the {plan} plan lists {base} as {row['action'] or 'no action'}"
                       + (f" into {_cb(row['artifact'])}" if row["action"] == "merged" else "")
                       + f", not merged into {survivor}")
            else:
                continue
            out.append({"via": via, "topic": t.get("topic") or base, "copy": copy,
                        "survivor": survivor, "plan": plan, "why": why})
    return sorted(out, key=lambda r: (r["copy"], r["via"]))


def speciality_points_at_copy(area: str, workspace: Path, repo: Path) -> list[dict]:
    """G75: each `<workspace>/speciality-map.json` row whose topic is a copy a
    fold deletes (a worklist copy no plan keeps, or a plan's `merged` copy
    whose folder exists), the copy or its survivor in this area. Each is an
    owner item: who repoints the speciality is the owner's."""
    try:
        rows = json.loads((workspace / "speciality-map.json").read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return []
    kept = set(kept_by(workspace))
    survivor_of = {_cb(c["folder"]): _cb(t["survivor"]) for t in _worklist_topics(workspace)
                   for c in t.get("copies") or [] if isinstance(c, dict) and c.get("folder")}
    survivor_of = {c: v for c, v in survivor_of.items() if c not in kept and c != v}
    for m in all_merges(workspace):
        if (repo / m["copy"]).is_dir():
            survivor_of.setdefault(m["copy"], m["artifact"])
    out = []
    for r in rows if isinstance(rows, list) else []:
        copy = _cb(r.get("topic")) if isinstance(r, dict) else ""
        if copy in survivor_of and area in (_area_of(copy), _area_of(survivor_of[copy])):
            out.append({"speciality": r.get("speciality"), "topic": copy, "survivor": survivor_of[copy],
                        "why": f"the fold deletes {copy}: who repoints the speciality is the owner's"})
    return sorted(out, key=lambda r: (r["topic"], str(r["speciality"])))


_NEW_APPROVAL = ("record a new approval naming the plan's hash and `reference-hash <reference_hash>` on one line "
                 "(the earlier approval stays on record as history)")
APPROVAL_WHY = {
    "no_record": "the plan has no approval record",
    "plan_changed": "the plan changed since its approval",
    "reference_hash": ("the approval does not name A/reference.json as it is now (no `reference-hash`, or the file "
                       f"changed since, or it is missing): {_NEW_APPROVAL}"),
    "reference_format": f"the approval records `reference-format`, which approves nothing since 1.4.30: {_NEW_APPROVAL}",
}


def next_why(nxt: str | None, appr_why: str | None, topics: dict, pending: list, plan: bool = True,
             stale_ref: list | None = None, holds: dict | None = None, carries: dict | None = None) -> str:
    """G75: one line saying why the area's `next` is what it is, the
    pending_target note (G47) first when any row waits on a plan."""
    if nxt == "plan":
        why = "no area-plan.md yet" if not plan else (
            "the plan was measured on a stale reference: re-run steps 1.1 to 1.3, then the step-4 checks, "
            "then hand the plan back to the owner for a new approval (the earlier approval stays on record "
            "as history)"
            if stale_ref else "the plan's measure is re-run before approval")
    elif nxt == "approve":
        why = APPROVAL_WHY[appr_why]
        if topics and all(t["merged"] for t in topics.values()):
            why += "; every row merged elsewhere: approval is a record"
    elif nxt is None:
        why = "no topic owes a stage here"
    else:
        owing = sorted(n for n, t in topics.items() if t["next"] == nxt)
        why = f"{', '.join(owing)} {'owes' if len(owing) == 1 else 'owe'} {nxt}"
    if stale_ref:
        reasons = sorted({r.get("reason") or "old_format" for r in stale_ref})
        legacy = sum(1 for r in stale_ref if r.get("reason") == "legacy_null")    # G108 (1.4.33)
        if "unreadable_reference" not in reasons:
            head = f"{len(stale_ref)} row(s) older than reference format {stale_ref[0]['want']}" + (
                f" ({legacy} legacy_null: drops on rewrite, no re-measure)" if legacy else "")
        elif reasons == ["unreadable_reference"]:
            head = "A/reference.json cannot be read as rows (re-run step 1.1)"
        else:
            head = f"{len(stale_ref)} row(s) ({', '.join(reasons)})"
        why = f"stale_reference: {head}; {why}"
    holds = holds or {}
    for k, rows_ in (carries or {}).items():          # G214 (1.4.39)
        subj = sum(1 for r in rows_ if r["kind"] == "subject")
        if subj:
            labels = len(rows_) - subj
            why = (f"{k}: {subj} subject row(s) unsettled ({labels} research_label row(s), advisory: they never "
                   "clear) (stage-1.md step 3, G214); " + why)
    if holds.get("stale_verdicts"):
        why = (f"stale_verdicts: {len(holds['stale_verdicts'])} held_by_wording row(s) whose recorded verdict reset "
               "(the piece or the topic's text changed): each counts lacking until judged again; record it with "
               f"mark.py --held (stage-1.md step 1.3, G251); {why}")
    if holds.get("cite_moved"):
        why = (f"cite_moved: {len(holds['cite_moved'])} cited question number(s) now name another lead phrase in "
               f"the plan they cite: re-read each cite (G232); {why}")
    if holds.get("host_check"):
        why = (f"host_check: {len(holds['host_check'])} subject(s) placed against the host rule: a host sharing "
               "no specific word, or a No-host subject a topic shares one with (stage-1.md step 3, G188); "
               f"{why}")
    if holds.get("plan_sections"):
        why = (f"plan_sections: {len(holds['plan_sections'])} row(s): a required section of area-plan.md is "
               "missing, misspelled or out of order, a Missing subject is not carried by its bold lead "
               "phrase into a Research question, or a topic has no research-bar Owner question "
               f"(stage-1.md step 3); {why}")
    if holds.get("stale_copy_check"):
        why = ("stale_copy_check: the copy_check.py --digest line under Overlaps is missing or differs from a "
               f"fresh run: re-run copy_check.py, rewrite Overlaps and record the new line (G133); {why}")
    if holds.get("r9_stale"):
        files = len({r["file"] for r in holds["r9_stale"]})
        why = (f"r9_stale: {files} R9 file(s) not measured on their reference and survivor folder as they are "
               f"now ({len(holds['r9_stale'])} row(s); re-run each R9 command, then r9_stamp.py on it); {why}")
    if pending:
        why = (f"pending_target: {len(pending)} row(s) wait on a plan not written yet "
               f"({', '.join(sorted({p['topic'] for p in pending}))}); not clean until re-checked; {why}")
    return why


def placed(plan: Path) -> dict[str, str]:
    """{topic: artifact path} from the plan's "## Proposed topics" table."""
    return {t: r["artifact"] for t, r in plan_rows(plan).items()}


def merged_elsewhere(plan: Path, area: str) -> dict[str, str]:
    """{topic: folder} for each plan row whose Action is `merged` and whose
    Artifact folder lies outside `cookbook/guidelines/<area>/`: that topic
    runs only under the plan whose area holds the folder."""
    here = f"cookbook/guidelines/{area.strip('/')}/"
    return {t: r["artifact"] for t, r in plan_rows(plan).items()
            if r["action"] == "merged" and not (r["artifact"] + "/").startswith(here)}


def written(folder: Path, tdir: Path) -> bool:
    """base.txt exists, the artifact has every role in ROLES, and every named
    rule of its rules parts cites research."""
    if not (tdir / "base.txt").is_file():
        return False
    try:
        parts = json.loads((folder / "artifact.json").read_text(encoding="utf-8"))["parts"]
    except (OSError, ValueError, KeyError, TypeError):
        return False
    if not set(ROLES) <= {p.get("role") for p in parts if isinstance(p, dict)}:
        return False
    rules = []
    for p in parts:
        if isinstance(p, dict) and p.get("role") == "rules":
            f = folder / f"{p.get('part')}.md"
            text = f.read_text(encoding="utf-8") if f.is_file() else ""
            starts = [m.start() for m in _RULE.finditer(text)] + [len(text)]
            rules += [text[a:b] for a, b in zip(starts, starts[1:])]
    return bool(rules) and all(_CITATION.search(r) for r in rules)


def git_blob_hash(path: Path) -> str:
    """The hash `git hash-object <path>` prints."""
    data = path.read_bytes()
    return hashlib.sha1(b"blob %d\0" % len(data) + data).hexdigest()


_REFERENCE_HASH = re.compile(r"(?<![a-z])reference[- ]hash:?[ \t]*`?([0-9a-f]{40})(?![0-9a-f])", re.I)
_REFERENCE_FORMAT = re.compile(r"(?<![a-z])reference[- ]format", re.I)


def reference_hash(dir_: Path) -> str | None:
    """`git hash-object A/reference.json`, None when there is no such file
    or it cannot be read as rows (N5-I-1: a broken reference is never approved)."""
    ref = dir_ / "reference.json"
    return git_blob_hash(ref) if ref.is_file() and _rows_of(ref)[1] else None


def approval_state(dir_: Path) -> tuple[str, str | None]:
    """(`approval`, `approval_why`). Current only when a line of approval.md
    names the plan's hash and, on that line, `reference-hash` with the hash
    of A/reference.json as it is now (N4-I-2, 1.4.30). The hash is recorded
    with the approval it belongs to, so an earlier approval's line stays in
    the file as history and approves nothing. A line recording
    `reference-format` (1.4.29) and no hash is stale, whatever follows the
    word (N4-M-1)."""
    plan, record = dir_ / "area-plan.md", dir_ / "approval.md"
    if not record.is_file() or not plan.is_file():
        return "missing", "no_record"
    h = git_blob_hash(plan)
    lines = [ln for ln in record.read_text(encoding="utf-8").splitlines() if h in ln]
    if not lines:
        return "stale", "plan_changed"
    named = {m.group(1).lower() for ln in lines for m in _REFERENCE_HASH.finditer(ln)}
    if reference_hash(dir_) in named:
        return "current", None
    if not named and any(_REFERENCE_FORMAT.search(ln) for ln in lines):
        return "stale", "reference_format"
    return "stale", "reference_hash"


def approval(dir_: Path) -> str:
    return approval_state(dir_)[0]


def review(tdir: Path) -> tuple[str, str | None]:
    """review.md's effective verdict and its lint state: `pass` only when the
    verdict line says pass and `## Lint` ends with `lint: clean` (lint fails
    closed, review_findings.lint_of); `missing` with no file or verdict line."""
    f = tdir / "review.md"
    if not f.is_file():
        return "missing", None
    parsed = review_findings.parse(f.read_text(encoding="utf-8"))
    lint = parsed["lint"]["state"]
    if parsed["verdict"] is None:
        return "missing", lint
    return ("pass" if parsed["verdict"] == "pass" and lint == "clean" else "fail"), lint


def fold(workspace: Path, artifact: str, repo: Path | None = None) -> list[str]:
    """Every merged copy of `artifact`: its worklist.json copies, whatever
    their fold_check, less any a plan keeps as its own artifact (Action
    `kept`; dropped, split or new still folds), and the existing folders of
    the topics plans merge into it, a kept one included: `cross_check`
    reports it as a conflict, and it is folded until the owner settles it."""
    f = workspace / "worklist.json"
    try:
        batches = json.loads(f.read_text(encoding="utf-8")).get("batches", [])
    except (OSError, ValueError, AttributeError):
        batches = []
    root = workspace / "areas"
    kept = {r["artifact"] for p in (root.rglob("area-plan.md") if root.is_dir() else [])
            for r in plan_rows(p).values() if r["action"] == "kept"}
    out = []
    for batch in batches:
        for t in batch.get("topics", []):
            if f"cookbook/{t.get('survivor', '')}".rstrip("/") == artifact:
                out += [f"cookbook/{c['folder']}".rstrip("/") for c in t.get("copies", []) if c.get("folder")]
    out = [c for c in out if c not in kept]
    out += [m["copy"] for m in all_merges(workspace)
            if m["artifact"] == artifact and m["copy"] not in out
            and (repo is None or (repo / m["copy"]).is_dir())]
    return out


def topic(folder: Path, tdir: Path, artifact: str, workspace: Path | None = None,
          repo: Path | None = None) -> dict:
    research = folder / "research"
    verdict, lint = review(tdir)
    t = {
        "artifact": artifact,
        "folder": (folder / "artifact.json").is_file(),
        "research": (research / "research.json").is_file() and (research / "research.md").is_file(),
        "second_check": (tdir / "second-check.md").is_file(),
        "written": written(folder, tdir),
        "owner_list": (tdir / "owner-list.md").is_file(),
        "review": verdict,
        "lint": lint,
        "integrated": integrated(tdir),
        "fold": fold(workspace, artifact, repo) if workspace else [],
    }
    rounds = review_findings.status(tdir) if tdir.is_dir() else {"rounds": 0, "next": "review", "open": []}
    t["rounds"] = rounds["rounds"]
    t["why"] = rounds.get("why", "")
    t["owner"] = [f["id"] for f in rounds["open"]] if rounds["next"] == "owner" and not t["integrated"] else []
    if t["integrated"]:
        # A finding a sibling routed here after this topic's stage 5 ran has
        # no stage left to deliver it: it is an owner item.
        t["owner"] = review_findings.routed((tdir / "integrate.md").read_text(encoding="utf-8"))
        t["next"] = None
    elif not (t["research"] and t["second_check"]):
        t["next"] = "research"
    elif not (t["written"] and t["owner_list"]):
        t["next"] = "write"
    elif t["review"] != "missing" and not counted(tdir):
        t["next"] = "review"
    elif rounds["next"] in ("review", "write", "stop"):
        t["next"] = rounds["next"]
    else:
        t["next"] = "integrate"
    if t["next"] != "stop":
        t["why"] = ""
    return t


def counted(tdir: Path) -> bool:
    """Whether review.md is saved as the latest review-N.md (write_brief.py append)."""
    saved = sorted((int(m.group(1)), p) for p in tdir.glob("review-*.md")
                   if (m := re.match(r"^review-(\d+)\.md$", p.name)))
    return bool(saved) and saved[-1][1].read_text(encoding="utf-8") == (tdir / "review.md").read_text(encoding="utf-8")


def integrated(tdir: Path) -> bool:
    f = tdir / "integrate.md"
    return f.is_file() and re.search(r"(?m)^integrated:\s*\S", f.read_text(encoding="utf-8")) is not None


ORDER = ("plan", "approve", "research", "write", "review", "integrate", "stop")


def status(area: str, workspace: Path, repo: Path) -> dict:
    dir_ = workspace / "areas" / area
    root = repo / "cookbook" / "guidelines" / area
    names = {p.name for p in root.iterdir() if p.is_dir()} if root.is_dir() else set()
    if (dir_ / "topics").is_dir():
        names |= {p.name for p in (dir_ / "topics").iterdir() if p.is_dir()}
    where = placed(dir_ / "area-plan.md")
    elsewhere = merged_elsewhere(dir_ / "area-plan.md", area)
    names |= set(where)
    paths = {n: where.get(n, f"cookbook/guidelines/{area}/{n}") for n in names}
    topics = {n: topic(repo / paths[n], dir_ / "topics" / n, paths[n], workspace, repo) for n in sorted(names)}
    plan = (dir_ / "area-plan.md").is_file()
    appr, appr_why = approval_state(dir_)
    rows, readable = _rows_of(dir_ / "reference.json")
    stale_ref = (stale_reference(rows) + ([] if readable else [unreadable_row(str(dir_ / "reference.json"))])
                 + _report_stale(dir_))
    # R-I-1, R2-I-1 (1.4.28): a stale reference holds every area at `plan`, approved
    # or not: its plan was measured on it, so steps 1.1-1.3 and step 4 re-run and
    # the plan goes back to the owner (N4-I-2: the rewrite changes the file's hash, so the approval is stale).
    # G94 (1.4.33): an R9 measure taken on another reference holds the area at plan too.
    holds = {"r9_stale": r9_stale(dir_ / "gaps", repo),
             # G97, G105 (1.4.33): a plan missing a section can drop owner items.
             "plan_sections": plan_sections(dir_ / "area-plan.md", frozenset(elsewhere)) if plan else [],
             # G133 (1.4.36): an Overlaps recorded on another copy_check result.
             "stale_copy_check": stale_copy_check(area, workspace, repo) if plan else [],
             # G188, G208, G209 (1.4.39): a subject placed against the host rule.
             "host_check": host_check(area, workspace, repo) if plan else [],
             # G232 (1.4.40): a cited question number whose lead phrase moved.
             "cite_moved": cite_moved(area, workspace) if plan else [],
             # G251 (1.4.41): a recorded verdict that reset and is not re-judged.
             "stale_verdicts": stale_verdicts(dir_, repo, paths) if plan else []}
    # G214 (1.4.39): a carry row of kind `subject` holds the area at plan; a
    # research_label row stays advisory and is printed after the subject rows.
    carries = {"survivor_carries": _subjects_first(survivor_carries(area, workspace, elsewhere) if plan else []),
               "carries_asked": _subjects_first(carries_asked(area, workspace))}
    held = bool(stale_ref or any(holds.values())
                or any(r["kind"] == "subject" for rows_ in carries.values() for r in rows_))
    gate = "plan" if not plan or held else "approve" if appr != "current" else None
    for n, t in topics.items():
        t["merged"] = elsewhere.get(n)
        if t["merged"]:
            # Owes nothing here: its folder's own area runs it.
            t.update(next=None, why=f"merged into {t['merged']}", owner=[])
        elif gate:
            t["next"] = gate
    if not plan or held:
        nxt = "plan"
    elif appr != "current":
        nxt = "approve"
    else:
        owed = [t["next"] for t in topics.values() if t["next"]]
        nxt = min(owed, key=ORDER.index) if owed else None
    incoming, conflicts = cross_check(area, workspace, repo)
    pending = pending_target(area, workspace, repo)
    return {"area": area, "dir": str(dir_), "plan": plan, "approval": appr, "approval_why": appr_why,
            # N4-I-2: the hash to copy into the approval, never given over a stale reference.
            "reference_hash": None if stale_ref else reference_hash(dir_), "cookr": cookr(repo),
            "topics": topics, "incoming": incoming, "incoming_unplanned": incoming_unplanned(area, workspace, repo),
            "conflicts": conflicts, "pending_target": pending,
            "speciality_points_at_copy": speciality_points_at_copy(area, workspace, repo),
            "stale_gaps": stale_gaps(area, workspace, repo), "stale_reference": stale_ref, **holds,
            # G134, G130 (1.4.36): advisory, never a hold. G151 (1.4.37): carries_asked,
            # the survivor's side of survivor_carries, advisory too.
            "other_plans_changed": other_plans_changed(area, workspace) if plan else [],
            **carries,
            # G190, G216 (1.4.39): advisory.
            "shared_no_host": shared_no_host(area, workspace) if plan else [],
            "stale_pointer": stale_pointer(area, workspace) if plan else [],
            # gapfix13 (G256, G269, 1.4.42): advisory.
            "non_home_lacking": non_home_lacking(dir_) if plan else [],
            "short_not_owed": short_not_owed(dir_) if plan else [],      # gapfix13b (platform-integration#5)
            "report_refresh": report_refresh(dir_) if plan else [],
            "next": nxt,
            "next_why": next_why(nxt, appr_why, topics, pending, plan, stale_ref, holds, carries)}


def _subjects_first(rows: list[dict]) -> list[dict]:
    """G214 (1.4.39): `subject` rows first, then `research_label` rows, each in its order."""
    return sorted(rows, key=lambda r: r.get("kind") != "subject")


PLAN_SECTIONS = ("Topics", "Gaps", "Missing subjects", "Overlaps", "Proposed topics", "Research questions",
                 "Owner questions", "Step-4 re-check")
_FENCE = re.compile(r"^\s*(```|~~~)")
_ITEM = re.compile(r"^(?:\d+[.)]|[-*])\s+(.*\S)")
_BOLD = re.compile(r"\*\*(.+?)\*\*")


def _loose(text: str) -> str:
    """A heading compared loosely: lowercased, every run of characters that
    are neither letters nor digits one space. Non-ASCII letters are kept
    (fix round 2, 1.4.35, re-review Minor 2)."""
    return " ".join(re.sub(r"[\W_]+", " ", text.lower()).split())


def _sections(plan: Path) -> list[tuple[str, list[str]]]:
    """[(heading, its body lines)] for each `## ` heading outside a fenced block, in order."""
    return _sections_of(plan.read_text(encoding="utf-8"))


def _sections_of(text: str) -> list[tuple[str, list[str]]]:
    """_sections of a plan's text."""
    out: list[tuple[str, list[str]]] = []
    fenced = False
    for line in text.splitlines():
        if _FENCE.match(line):
            fenced = not fenced
        elif not fenced and line.startswith("## "):
            out.append((line[3:].strip(), []))
            continue
        if out:
            out[-1][1].append(line)
    return out


def plan_sections(plan: Path, copies: frozenset[str] = frozenset()) -> list[dict]:
    """G97 (1.4.33): [{"section", "found", "why"}] for each PLAN_SECTIONS
    heading of area-plan.md that is missing (`found` null), misspelled
    (`found` the heading that matches it loosely: case, hyphens, spaces) or
    out of order (after a heading that follows it in PLAN_SECTIONS). G105: the
    Missing-subjects rows of _subject_rows. [] when the plan cannot be read:
    stage_status reads it elsewhere."""
    try:
        found = _sections(plan)
    except (OSError, UnicodeDecodeError):
        return []
    rows, at = [], {}
    for want in PLAN_SECTIONS:
        exact = [i for i, (h, _) in enumerate(found) if h == want]
        if exact:
            at[want] = exact[0]
            continue
        loose = [i for i, (h, _) in enumerate(found) if _loose(h) == _loose(want)]
        if loose:
            at[want] = loose[0]
            rows.append({"section": want, "found": found[loose[0]][0],
                         "why": f"misspelled: the heading is `## {found[loose[0]][0]}`, step 3 says `## {want}`"})
        else:
            rows.append({"section": want, "found": None,
                         "why": f"missing: no `## {want}` heading (stage-1.md step 3 lists every section, in order)"})
    last = -1
    for want in PLAN_SECTIONS:
        if want not in at:
            continue
        if at[want] < last:
            rows.append({"section": want, "found": found[at[want]][0],
                         "why": "out of order: it stands after a section step 3 puts after it"})
        last = max(last, at[want])
    body = {want: "\n".join(found[at[want]][1]) for want in PLAN_SECTIONS if want in at}
    rows.extend(_subject_rows(body))
    rows.extend(_bar_rows(body, copies))      # G128 (1.4.36); fix round 1: copies owe none
    return rows


NO_HOST = "carried, no host"
_CODE_SPAN = re.compile(r"`[^`\n]*`")


def _split(text: str) -> list[tuple[int, str, bool]]:
    """_chunks before loosening: [(top, the chunk's lines joined, whether it is a list item)]."""
    out: list[tuple[int, list[str], bool]] = [(0, [], False)]
    top = 0
    for line in text.splitlines():
        s = line.lstrip()
        if _ITEM.match(s) or s.startswith("#"):
            if line[:1] not in (" ", "\t"):
                top += 1
            out.append((top, [], bool(_ITEM.match(s))))
            if s.startswith("#"):
                continue
        out[-1][1].append(line)
    return [(t, " ".join(x.strip() for x in lines), item) for t, lines, item in out]


def _chunks(text: str) -> list[tuple[int, str, set[str], str | None]]:
    """`text` split into items, each (top, loosened text, its loosened bold
    spans, the loosened whole item or None): a list item at any depth with the
    lines that follow it up to the next item or `#` heading; text before the
    first item is a chunk of its own. `top` numbers the top-level item (a list
    item at indent 0, or a `#` heading) a chunk belongs to, so a nested
    sub-bullet counts with its parent (fix round 2, 1.4.35). G127 (1.4.36): a
    heading's own text is in no chunk, so it never carries or marks."""
    res = []
    for t, raw, item in _split(text):
        if not _loose(raw):
            continue
        whole = _loose(_ITEM.match(raw).group(1)) if item and _ITEM.match(raw) else None
        res.append((t, _loose(raw), {_loose(b) for b in _BOLD.findall(raw)}, whole))
    return res


def _found(chunks: list, k: str) -> tuple[set[int], bool]:
    """G127 (1.4.36): (the tops of the chunks that carry loosened phrase `k`,
    as a whole bold span inside a list item or as a whole list item; whether
    any chunk names it in plain text). Fix round 1 (review 5): a bold span in
    a loose paragraph never carries; it is named only."""
    return ({t for t, _, bolds, whole in chunks if (whole is not None and k in bolds) or whole == k},
            any(f" {k} " in f" {c} " for _, c, _, _ in chunks))


def _key(phrase: str) -> str:
    """A bold phrase as reported: trimmed, a trailing `.` or `:` dropped (G126)."""
    return phrase.strip().rstrip(".:").strip() or phrase.strip()


def _subject_rows(body: dict[str, str]) -> list[dict]:
    """G105 (1.4.33), fix round 1 (1.4.34): one {"section": "Missing subjects",
    "item", "found": null, "why"} for each top-level numbered or bulleted item
    under Missing subjects that stage-1.md step 3 does not see carried. The key
    is the item's bold lead phrase, matched verbatim (case and punctuation
    aside) with no fuzzy match, a trailing `.` or `:` dropped (G126, 1.4.36).
    Research questions and Owner questions are searched apart, never across
    their join; G127 (1.4.36): a phrase is carried there only as a whole bold
    span or a whole list item, never inside a heading:
    - no bold lead: its own row, never matched on its text;
    - a bold-led paragraph that is not a list item: its own row (G126);
    - a second bold phrase in an item: checked as a subject of its own (G126);
    - a bold lead with no letter or digit (empty key): its own row, never
      skipped (fix round 2, 1.4.35); non-ASCII letters stay in the key;
    - carried by no Research question: "named only under Owner questions"
      when Owner questions carry it, "named but not carried" when a Research
      question names it in plain text, else "carried nowhere";
    - carried by a Research question whose top-level item (its nested
      sub-bullets included) says "carried, no host" but not carried under
      Owner questions: its own row."""
    research = _chunks(body.get("Research questions", ""))
    owner = _chunks(body.get("Owner questions", ""))
    no_host = f" {_loose(NO_HOST)} "
    rows = []
    prev = ""
    for raw in body.get("Missing subjects", "").splitlines():
        # G165 (1.4.37): bold inside a code span is code, never a subject (a
        # code span holding no bold stays: it can be part of one); only a
        # paragraph's first line (after a blank line) can be bold-led.
        line, first = _CODE_SPAN.sub(lambda c: "" if "**" in c.group(0) else c.group(0), raw), not prev.strip()
        prev = raw
        m = _ITEM.match(line)
        if not m:
            lead = _BOLD.match(line) if first else None
            if lead:
                rows.append({"section": "Missing subjects", "item": _key(lead.group(1)), "found": None,
                             "why": "a bold-led paragraph, not a list item: its carry is never checked; make it "
                                    "a numbered item (stage-1.md step 3, G126)"})
            continue
        bold = _BOLD.match(m.group(1))
        if not bold:
            rows.append({"section": "Missing subjects", "item": m.group(1).strip(), "found": None,
                         "why": "no bold lead phrase (stage-1.md step 3 asks for one): lead the subject "
                                "with its bold name and carry that name verbatim (1.4.34)"})
            continue
        keys = []
        for b in _BOLD.finditer(m.group(1)):
            if _key(b.group(1)) not in keys:
                keys.append(_key(b.group(1)))
        for i, key in enumerate(keys):
            k = _loose(key)
            if not k:
                rows.append({"section": "Missing subjects", "item": key, "found": None,
                             "why": "bold lead phrase with no letter or digit: name the subject in words and "
                                    "carry that name verbatim (stage-1.md step 3, 1.4.35)"})
                continue
            tops, named = _found(research, k)
            otops, onamed = _found(owner, k)
            second = "" if i == 0 else "a second bold phrase of the item, checked as a subject (G126): "
            if not tops:
                why = ("named only under Owner questions: carry it into a Research question, its bold lead "
                       "phrase verbatim (stage-1.md step 3, G105)" if otops else
                       "named but not carried: a Research question names it in plain text only; carry it as "
                       "a whole bold span or a whole list item (stage-1.md step 3, G127)" if named else
                       "carried nowhere: its bold lead phrase is in no Research question (stage-1.md step 3, "
                       "G105)" + ("; Owner questions name it in plain text only" if onamed else ""))
            elif any(no_host in f" {c} " for t, c, _, _ in research if t in tops) and not otops:
                why = ("carried, no host but not under Owner questions: a subject no topic answers is also "
                       "listed there, as a whole bold span or list item, as a candidate new topic "
                       "(stage-1.md step 3, G105, G127)")
            else:
                continue
            rows.append({"section": "Missing subjects", "item": key, "found": None, "why": second + why})
    return rows


_EVERY_TOPIC = re.compile(r"\b(?:every|each|all)(?: of the| the)? topics?\b")
_EXCEPT = re.compile(r"\b(?:except|but|other than)\b")


def _topic_names(topics_body: str, column: str | None = None) -> list[str]:
    """G128 (1.4.36): the first cell (or, with `column`, the cell under that
    header, case aside) of each table row (header and separator rows aside),
    backticks, bold and link targets dropped; a path reads as its last
    segment; a trailing parenthetical note ("(new)") is dropped (fix round 1).
    G166 (1.4.37): only the first table is read; a later one names no topics."""
    names, head = [], None
    for line in topics_body.splitlines():
        if not line.lstrip().startswith("|"):
            if head is not None:
                break
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if all(re.fullmatch(r":?-{2,}:?", c.replace(" ", "")) for c in cells if c):
            continue
        if head is None:
            head = [c.lower().strip("`* ") for c in cells]
            continue
        at = 0 if column is None else head.index(column) if column in head else None
        if at is None or at >= len(cells):
            continue
        cell = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", cells[at]).replace("`", "").replace("**", "").strip()
        cell = cell.rstrip("/").rsplit("/", 1)[-1].strip()
        cell = re.sub(r"\s*\([^()]*\)\s*$", "", cell)  # "x (new)": the note is not the name (fix round 1)
        if _loose(cell) and not set(cell) <= set("-: ") and cell not in names:
            names.append(cell)
    return names


def _bar_rows(body: dict[str, str], copies: frozenset[str] = frozenset()) -> list[dict]:
    """G128 (1.4.36): one row per topic that no top-level Owner question
    mentioning the research bar names. The topics are the Topics table's
    first column; fix round 1 (review I2): with no table there, Proposed
    topics' Topic column; with neither, one row ("Topics lists no table the
    research-bar check can read"), never a silent pass. One question naming
    every, each or all topics names them all, unless a topic name or an
    except / but / other than follows that phrase in it: then it names only
    the topics it names before the exception word. Fix round 1 (review 6): a
    topic in `copies` (merged into another area) owes no question: the
    survivor's research bar governs it. No Owner questions section: [] (its
    missing-section row holds the area already)."""
    if "Owner questions" not in body:
        return []
    names = _topic_names(body.get("Topics", "")) or _topic_names(body.get("Proposed topics", ""), "topic")
    texts: dict[int, list[str]] = {}
    for t, c, _, _ in _chunks(body.get("Owner questions", "")):
        texts.setdefault(t, []).append(c)
    bars = []
    for b in (" ".join(v) for v in texts.values()):
        if " research bar" not in f" {b} ":
            continue
        m = _EVERY_TOPIC.search(b)
        if m:
            tail = b[m.end():]
            cut = _EXCEPT.search(tail)
            if not cut and not any(f" {_loose(n)} " in f" {tail} " for n in names):
                return []
            if cut:
                b = b[:m.end() + cut.start()]
        bars.append(b)
    if not names:
        return [{"section": "Topics", "item": None, "found": None,
                 "why": "Topics lists no table the research-bar check can read, and Proposed topics has no Topic "
                        "column: make Topics a table with one topic per row, or ask one research-bar Owner "
                        "question naming every topic (stage-1.md step 3, G128)"}]
    skip = {_loose(c.rstrip("/").rsplit("/", 1)[-1]) for c in copies}
    return [{"section": "Owner questions", "item": n, "found": None,
             "why": "no Owner question about the research bar names this topic: ask one top-level item per "
                    "topic, naming the topic, or one naming every topic (stage-1.md step 3, G116, G128, G166)"}
            for n in names if _loose(n) not in skip and not any(f" {_loose(n)} " in f" {b} " for b in bars)]


def stale_copy_check(area: str, workspace: Path, repo: Path) -> list[dict]:
    """G133 (1.4.36): [{"recorded", "current", "why"}] when the plan's
    Overlaps records no `copy_check.py <area>: ...` digest line and the area
    has copies, or records one that differs from a fresh run's. [] with no
    worklist (copy_check.py cannot run); a worklist it cannot read is a row."""
    import copy_check  # copy_check imports this module: import it here, not at the top
    plan = workspace / "areas" / area / "area-plan.md"
    if not (workspace / "worklist.json").is_file():
        return []
    try:
        body = dict(_sections(plan)).get("Overlaps", "")
        body = "\n".join(body) if isinstance(body, list) else body
    except (OSError, UnicodeDecodeError):
        return []
    found = re.findall(rf"copy_check\.py {re.escape(area)}: [^`\n]*", body)
    recorded = found[-1].strip() if found else None
    try:
        result = copy_check.check(area, workspace, repo)
    except (OSError, ValueError) as e:
        return [{"recorded": recorded, "current": None,
                 "why": f"copy_check.py cannot run ({e.__class__.__name__}: {e})"}]
    current = copy_check.digest(result)
    if recorded == current or (recorded is None and not (result["copies"] or result["moved"]
                                                         or result["unreadable"])):
        return []
    return [{"recorded": recorded, "current": current,
             "why": ("no copy_check.py --digest line under Overlaps" if recorded is None else
                     "the copy_check.py result changed since Overlaps recorded it")
                    + ": re-run copy_check.py, rewrite Overlaps from it and record the line (stage-1.md step 3, G133)"}]


_HEX40 = re.compile(r"\b[0-9a-f]{40}\b")


def _changed_sections(old: str, new: str) -> list[str]:
    """G153 (1.4.37): the `## ` headings whose body differs between two texts
    of a plan, in the new text's order, then those only the old text has;
    "(before the first heading)" when the text above the first heading differs."""
    def parts(text: str) -> dict[str, str]:
        head = text.split("\n## ", 1)[0] if not text.startswith("## ") else ""
        return {"(before the first heading)": head.strip(),
                **{h: "\n".join(b).strip() for h, b in _sections_of(text)}}
    a, b = parts(old), parts(new)
    return [h for h in b if a.get(h) != b[h]] + [h for h in a if h not in b]


def _old_text(where: Path, blob: str) -> str | None:
    """The text git holds under hash `blob` (any repo `where` lies in), or None."""
    import subprocess
    try:
        r = subprocess.run(["git", "-C", str(where), "cat-file", "-p", blob], capture_output=True, timeout=30)
    except (OSError, subprocess.SubprocessError):
        return None
    if r.returncode != 0:
        return None
    try:
        return r.stdout.decode("utf-8")
    except UnicodeDecodeError:
        return None


def content_text(text: str) -> str:
    """G186 (1.4.39): a plan's text with its whole `## Step-4 re-check`
    section (heading to the next `## ` heading outside a fenced block)
    removed: what a hash recorded in another plan stands for."""
    out, fenced, skip = [], False, False
    for line in text.splitlines(keepends=True):
        if _FENCE.match(line):
            fenced = not fenced
        elif not fenced and line.startswith("## "):
            skip = _loose(line[3:]) == _loose("Step-4 re-check")
        if not skip:
            out.append(line)
    return "".join(out)


def content_hash_of(text: str) -> str:
    """G186 (1.4.39): the git blob hash of content_text(text)."""
    data = content_text(text).encode("utf-8")
    return hashlib.sha1(b"blob %d\0" % len(data) + data).hexdigest()


def content_hash(path: Path) -> str:
    """G186 (1.4.39): content_hash_of a plan file, its bytes as written."""
    return content_hash_of(path.read_bytes().decode("utf-8"))


# G191 (1.4.39): a record is `<area>/area-plan.md <40-hex>` inside backticks
# (an `areas/` or longer workspace prefix allowed) on a Step-4 re-check line.
_RECORD = re.compile(r"`(?:[^`\s]*?(?<![\w-])areas/)?([\w.-]+(?:/[\w.-]+)*?)/area-plan\.md ([0-9a-f]{40})`")
_QUESTION_NO = re.compile(r"\bquestions?\s*#?\d+|\bRQ\s*#?\d+|\btopic\s+\d+\s*[-\u2013]\s*\d+", re.I)
_CITE = re.compile(r"\b(?P<owner>owner\s+|its\s+)?questions?\s*#?(?P<nums>\d+(?:\s*(?:,|and|or|/|-|\u2013)\s*\d+)*)"
                   r"|\bRQ\s*#?(?P<rq>\d+)|\btopic\s+(?P<g>\d+)\s*[-\u2013]\s*(?P<m>\d+)", re.I)


def _records(step4: list[str]) -> tuple[dict[str, str], set[str]]:
    """G191 (1.4.39): ({plan: its recorded hash}, {plans named with a hash
    outside backticks}) from Step-4 re-check's lines. Of several records of a
    plan the last wins, so the last `### ` subsection's (the newest section
    goes last)."""
    recs: dict[str, str] = {}
    loose: set[str] = set()
    for line in step4:
        found = [(m.group(1), m.group(2)) for m in _RECORD.finditer(line)]
        for name, h in found:
            recs[name] = h
        rest = _RECORD.sub("", line)
        for m in re.finditer(r"(?:(?<![\w/.-])|(?<=areas/))([\w.-]+(?:/[\w.-]+)*?)/area-plan\.md\W+([0-9a-f]{40})",
                             rest):
            loose.add(m.group(1))
    return recs, loose


def _snapshot(dir_: Path, name: str, h: str) -> Path:
    """G193 (1.4.39): where --record-others keeps a cited plan's text."""
    return dir_ / "other-plans" / f"{name.replace('/', '--')}.{h}.md"


def _numbered_lines(text: str) -> list[tuple[int, str, str]]:
    """[(line number, its `## ` section or "", the line)], fences aware."""
    out, section, fenced = [], "", False
    for i, line in enumerate(text.splitlines(), 1):
        if _FENCE.match(line):
            fenced = not fenced
        elif not fenced and line.startswith("## "):
            section = line[3:].strip()
            continue
        out.append((i, section, line))
    return out


def _cited(area: str, workspace: Path) -> list[dict]:
    """Each other area plan this plan names or records: {"name", "path",
    "rec", "loose", "cited_at", "question_cites"} (G134, G154, G186, G191,
    G194, G211)."""
    plan = workspace / "areas" / area / "area-plan.md"
    try:
        text = plan.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return []
    lines = _numbered_lines(text)
    recs, loose = _records([x for _, s, x in lines if _loose(s) == _loose("Step-4 re-check")])
    out = []
    for other in sorted((workspace / "areas").glob("**/area-plan.md")):
        name = other.parent.relative_to(workspace / "areas").as_posix()
        if name == area:
            continue
        # Fix round 1 (review 4): an `areas/` prefix is allowed; a single-segment
        # name cites only as a path (`<name>/`, `areas/<name>`) or in backticks.
        n_ = re.escape(name)
        cite = re.compile(rf"(?:(?<![\w/.-])|(?<=areas/)){n_}(?![\w-])" if "/" in name else
                          rf"(?<![\w/.-]){n_}/|(?<=areas/){n_}(?![\w-])|`{n_}/?`")
        alias = re.compile(rf"(?<![\w/.-]){n_}\s+(?:area\s+)?plan\b", re.I)
        # 1.4.40 (G232); gapfix13 (G258, 1.4.42): "<name> plan" with the exact area name only ("the brainstorming
        # plan", "the planning/ui plan"), never its last segment ("the testing plan" named four plans)
        at = [(i, x) for i, s, x in lines if _loose(s) != _loose("Step-4 re-check")
              and (cite.search(x) or (alias and alias.search(x)))]
        if name not in recs and name not in loose and not at and not cite.search(text):
            continue
        out.append({"name": name, "path": other, "rec": recs.get(name), "loose": name in loose,
                    "cite_lines": [(i, x) for i, x in at if _QUESTION_NO.search(x)],
                    "cited_at": [i for i, _ in at],
                    "question_cites": [i for i, x in at if _QUESTION_NO.search(x)]})
    return out


def _lead(item: dict) -> str:
    """The lead phrase a cite stands for: the bold subject, else the first words of the item."""
    return item.get("subject") or re.sub(r"\s+", " ", item["text"])[:40]


def _cite_targets(text: str) -> dict[str, list[str]]:
    """1.4.40 (G232): the lead phrases of a plan's cited lists: "research" its Research questions in order,
    "owner" its Owner questions, "group" the `### ` groups' items (a list per group)."""
    items = research_items(text)
    groups: dict[tuple, list[str]] = {}
    for it in items:
        groups.setdefault((tuple(it["topics"]), it["no_host"]), []).append(_lead(it))
    owner = dict(_sections_of(text)).get("Owner questions", [])
    return {"research": [_lead(i) for i in items], "group": list(groups.values()),
            "owner": [_lead({"text": m.group(1).strip(), "subject": (_key(b.group(1)) if (b := _BOLD.match(m.group(1).strip())) else None)})
                      for line in owner if (m := _ITEM.match(line))]}


def _cites_of(line: str) -> list[tuple[str, str, int, int | None]]:
    """[(cite text, "research"|"owner"|"group", N, M)] the numbers a line cites."""
    out = []
    for m in _CITE.finditer(line):
        if m.group("g"):
            out.append((m.group(0), "group", int(m.group("g")), int(m.group("m"))))
            continue
        kind = "owner" if m.group("owner") else "research"
        if m.group("rq"):
            out.append((m.group(0), "research", int(m.group("rq")), None))
            continue
        for part in re.split(r"\s*(?:,|and|or|/)\s*", m.group("nums")):      # gapfix13 (G258): 6/7/8, 6 or 7
            span = [int(x) for x in re.split(r"\s*[-\u2013]\s*", part)]
            lo, hi = span[0], span[-1]
            for n in range(lo, min(hi, lo + 20) + 1):
                out.append((f"{m.group('owner') or ''}question {n}", kind, n, None))
    return out


def _held_json(dir_: Path) -> dict:
    try:
        saved = json.loads((dir_ / "held.json").read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}
    return saved if isinstance(saved, dict) else {}


def stale_verdicts(dir_: Path, repo: Path | None = None, folders: dict | None = None) -> list[dict]:
    """G251 (1.4.41), holds at plan: each held_by_wording row of the saved
    A/run_gaps.json whose verdict reset (G159, G202) and was not judged again.
    run_gaps counts the row lacking meanwhile, so the total can only rise.
    gapfix13 (G269, 1.4.42): read against the live A/held.json, not the
    report's copy: a row re-recorded since the report was saved (the record
    matching the row's text and pins) is no longer listed, and a recorded
    verdict the row's text no longer matches is, before any re-run. A
    re-measure can reset more (report_refresh says when).
    gapfix13b (language#3, 1.4.42): each row carries the piece (`text`), the
    rule and topic sentence its verdict was recorded on (`*_was`, from
    held.json) and the current ones (`*_now`), `rule_at`, and `topic_files`:
    the part files (`folders`: topic -> its repo path) the sentences are read
    from. The digest reads STALE_DIGEST_FIELDS only."""
    folders = folders or {}
    try:
        report = json.loads((dir_ / "run_gaps.json").read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return []
    import run_gaps  # run_gaps imports this module: import it here, not at the top
    rows = report.get("held_by_wording") if isinstance(report, dict) else None
    live = _held_json(dir_)
    out = []
    for r in rows if isinstance(rows, list) else []:
        if not isinstance(r, dict):
            continue
        v = live.get(r.get("id"))
        if isinstance(v, dict) and v.get("verdict") in ("held", "not"):
            why = run_gaps.verdict_reset(v, r)
            was = v["verdict"] if why else None
        else:
            why, was = r.get("verdict_why"), (r.get("verdict_was") if not r.get("verdict") else None)
        if was:
            rec = v if isinstance(v, dict) else {}
            out.append({"id": r.get("id"), "speciality": r.get("speciality"), "n": r.get("n"),
                        "topic": r.get("topic"), "verdict_was": was, "why": why,
                        # gapfix13b (language#3): what to judge it again on, and where the topic text is.
                        "text": r.get("text"), "rule_sentence_was": rec.get("rule_sentence"),
                        "rule_sentence_now": r.get("rule_sentence"), "rule_at": r.get("rule_at"),
                        # gapfix14 (G279): a checklist rule row's Severity cell, then and now
                        "rule_severity_was": run_gaps.severity(rec.get("rule_sentence")),
                        "rule_severity_now": run_gaps.severity(r.get("rule_sentence")),
                        "topic_sentence_was": rec.get("topic_sentence"), "topic_sentence_now": r.get("topic_sentence"),
                        "topic_files": _topic_files(repo, folders.get(r.get("topic"))) if repo else []})
    return out


STALE_DIGEST_FIELDS = ("id", "speciality", "n", "topic", "verdict_was", "why")      # gapfix13b: the digest's fields


def _topic_files(repo: Path, folder: str | None) -> list[str]:
    """gapfix13b (1.4.42, language#3): the repo-relative part files a topic's
    sentences are read from (paraphrase_hints.topic_sentences: each part
    artifact.json lists, but history, that exists), so a reset row is judged
    on the text run_gaps read, with no compile."""
    if not folder:
        return []
    base = folder.rstrip("/")
    try:
        parts = json.loads((repo / base / "artifact.json").read_text(encoding="utf-8"))["parts"]
    except (OSError, ValueError, KeyError, TypeError):
        return []
    names = [p.get("part") for p in parts if isinstance(p, dict)]
    return [f"{base}/{n}.md" for n in names if n and n != "history" and (repo / base / f"{n}.md").is_file()]


# gapfix14 (G291, 1.4.43): what a stale A/run_gaps.json leaves stale: the stage_status keys read from it and
# run_gaps' figures.
STALE_VIEWS = ("stale_verdicts", "non_home_lacking", "short_not_owed", "measured_total", "topic_totals")


def report_refresh(dir_: Path) -> list[dict]:
    """gapfix13 (G269, 1.4.42), advisory: one row when A/run_gaps.json's views
    may be out of date: saved by another skill version (a re-measure may reset
    verdicts it cannot show), or older than A/held.json or A/hand_lacks.json
    (verdicts recorded since: stale_verdicts reads them live; its figures do
    not). The row names the command that refreshes it."""
    path = dir_ / "run_gaps.json"
    try:
        report = json.loads(path.read_text(encoding="utf-8"))
        made = path.stat().st_mtime
    except (OSError, ValueError):
        return []
    whys = []
    saved_by = report.get("skill_version") if isinstance(report, dict) else None
    now = skill_version()
    if saved_by != now:
        whys.append(f"saved by grow-cookbook {saved_by or 'before 1.4.42'}, the skill is {now}: a re-measure may "
                    "reset verdicts this report cannot show")
    for name in ("held.json", "hand_lacks.json", "hand_holds.json"):      # gapfix14 (G291): a hand hold too
        try:
            if (dir_ / name).stat().st_mtime > made:
                whys.append(f"{name} changed after it was saved: its figures (measured_total, topic_totals) do not "
                            "count those verdicts yet")
        except OSError:
            pass
    if not whys:
        return []
    area = report.get("area") if isinstance(report, dict) and report.get("area") else "<area>"
    return [{"report": str(path), "saved_by": saved_by, "skill": now, "stale_views": list(STALE_VIEWS),
             "command": f"$COOKR_PY run_gaps.py --area {area} --workspace <workspace> --repo <repo> --hints",
             "why": "; ".join(whys) + f": run `$COOKR_PY run_gaps.py --area {area} --workspace <workspace> --repo "
                    "<repo> --hints` (step 1.3) to refresh it"}]


def _saved_rows(dir_: Path, key: str) -> list[dict]:
    """The dict rows of the saved A/run_gaps.json's list `key` ([] when unreadable)."""
    try:
        report = json.loads((dir_ / "run_gaps.json").read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return []
    rows = report.get(key) if isinstance(report, dict) else None
    return [r for r in rows if isinstance(r, dict)] if isinstance(rows, list) else []


def short_not_owed(dir_: Path) -> list[dict]:
    """gapfix13b (1.4.42, platform-integration#5), advisory: the saved
    report's short_not_owed rows, each a short piece marked for another area
    only, so it owes no verdict here; the short_sentences rows owing one are
    the rest."""
    return _saved_rows(dir_, "short_not_owed")


def non_home_lacking(dir_: Path) -> list[dict]:
    """gapfix13 (G256, 1.4.42), advisory: the saved report's non_home_lacking
    rows, each a counted, unjudged lacking piece at a topic that is not its
    sentence's home. Each counts until a verdict is recorded for it."""
    try:
        report = json.loads((dir_ / "run_gaps.json").read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return []
    rows = report.get("non_home_lacking") if isinstance(report, dict) else None
    return [r for r in rows if isinstance(r, dict)] if isinstance(rows, list) else []


def cite_moved(area: str, workspace: Path) -> list[dict]:
    """G232 (L10), G245 (L23), 1.4.40, holds at plan: [{"plan", "cite", "at",
    "was", "now", "why"}] for each question number this plan cites in another
    plan (question N, owner question N, its question N, RQ N, questions N-M,
    topic N-M: the Nth Research item, Owner item, or the Mth item of the
    Nth `### ` group) whose lead phrase in that plan now differs from the
    one the snapshot --record-others saved (A/other-plans/, else git's text
    at the recorded hash) holds. A plan with no snapshot is read by
    other_plans_changed's `unrecorded` row alone."""
    dir_ = workspace / "areas" / area
    rows = []
    for c in _cited(area, workspace):
        if not c["rec"] or not c["cite_lines"]:
            continue
        snap = _snapshot(dir_, c["name"], c["rec"])
        try:
            old = snap.read_text(encoding="utf-8") if snap.is_file() else _old_text(c["path"].parent, c["rec"])
            new = c["path"].read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            continue
        if old is None or content_hash_of(new) == c["rec"]:
            continue
        was_, now_ = _cite_targets(content_text(old)), _cite_targets(content_text(new))

        def pick(t: dict, kind: str, n: int, m: int | None) -> str | None:
            try:
                return t["group"][n - 1][m - 1] if kind == "group" else t[kind][n - 1]
            except IndexError:
                return None
        for i, line in c["cite_lines"]:
            for cite, kind, n, m in _cites_of(line):
                was, now = pick(was_, kind, n, m), pick(now_, kind, n, m)
                if was is not None and was != now:
                    num = f"{n}-{m}" if m else str(n)
                    rows.append({"plan": c["name"], "cite": cite, "at": i, "was": was, "now": now,
                                 "why": f"cite {num}: was '{was}', now '{now or '(none)'}' in {c['name']} (line {i} "
                                        "of this plan cites it): re-read the line and its number, then re-record "
                                        f"the plan's hash (stage_status.py --record-others; G232)"})
    return rows


def other_plans_changed(area: str, workspace: Path) -> list[dict]:
    """G134 (1.4.36), advisory: [{"plan", "recorded", "current", "sections",
    "cited_at", "question_cites", "why"}] for each other area plan
    (W/areas/**/area-plan.md) this plan names (its area, as a whole path,
    `areas/` before it allowed; a single-segment area only as `<name>/`,
    `areas/<name>` or in backticks: fix round 1) or records in Step-4
    re-check, whose content hash (G186, 1.4.39: the git blob hash of the plan
    with its Step-4 re-check section removed, so recording hashes never moves
    it) differs from the one recorded for it. G191 (1.4.39): a record is a
    Step-4 line holding `` `<area>/area-plan.md <hash>` `` in backticks; the
    last one wins (the last `### ` subsection's). A recorded hash equal to the
    plan's whole-file git hash (the pre-1.4.39 record) counts as current too.
    G154 (1.4.37): that whole path, never the tail of a longer one. G152
    (1.4.37): with no hash recorded it is listed `unrecorded`. G153 (1.4.37),
    G193 (1.4.39): `sections` names the `## ` sections whose text changed
    since the recorded hash, read from the snapshot --record-others saved
    (A/other-plans/) or from git, else "unknown"; the row is never dropped.
    G194, G211 (1.4.39): `cited_at` the plan's line numbers naming it
    (outside Step-4 re-check), `question_cites` those naming a question number."""
    dir_ = workspace / "areas" / area
    rows = []
    for c in _cited(area, workspace):
        try:
            raw = c["path"].read_bytes().decode("utf-8")
            whole = git_blob_hash(c["path"])
        except (OSError, UnicodeDecodeError):
            continue
        current, rec, name = content_hash_of(raw), c["rec"], c["name"]
        if rec in (current, whole):
            continue
        if rec:
            snap = _snapshot(dir_, name, rec)
            try:
                old = snap.read_text(encoding="utf-8") if snap.is_file() else _old_text(c["path"].parent, rec)
            except (OSError, UnicodeDecodeError):
                old = None
            sections = (_changed_sections(content_text(old), content_text(raw.replace("\r\n", "\n")))
                        if old is not None else "unknown")
            why = "changed since Step-4 re-check recorded its hash"
        else:
            sections = "unknown"
            why = "unrecorded: Step-4 re-check records no hash of it, so whether it changed is unknown" + (
                " (a Step-4 line names its hash outside backticks: not read since 1.4.39, G191)"
                if c["loose"] else "")
        cited = (f"cited at {line_ranges(c['cited_at'])}" if c["cited_at"]
                 else "named only in Step-4 re-check")
        if c["question_cites"]:
            cited += (f"; question numbers cited at {', '.join(f'line {i}' for i in c['question_cites'])}: "
                      "check they still point at the same questions (G211)")
        rows.append({"plan": name, "recorded": rec, "current": current, "sections": sections,
                     "cited_at": c["cited_at"], "question_cites": c["question_cites"],
                     "why": f"{why} ({cited}): re-read what this plan quotes or asks from the cited plan, even when "
                            "nothing in it concerns this area"
                            + (f" (its sections {sections} changed)" if isinstance(sections, list) and sections
                               else "") + ", then record the line "
                            f"`{name}/area-plan.md {current}` in the last `### ` subsection of Step-4 re-check "
                            "(stage_status.py --record-others prints it; G118, G134, G152, G186, G191)"})
    return rows


def line_ranges(lines: list[int]) -> str:
    """gapfix14 (G296, 1.4.43): `N lines: 3-5, 9` -- the count and every run of consecutive line numbers."""
    runs: list[list[int]] = []
    for n in sorted(set(lines)):
        if runs and n == runs[-1][1] + 1:
            runs[-1][1] = n
        else:
            runs.append([n, n])
    count = len(set(lines))
    return (f"{count} line{'' if count == 1 else 's'}: "
            + ", ".join(str(a) if a == b else f"{a}-{b}" for a, b in runs))


def write_records(plan: Path, lines: list[str]) -> str | None:
    """G236 (L14, 1.4.40): put `lines` (record lines, `- `<plan>/area-plan.md <hash>``) into the last `### `
    subsection of the plan's Step-4 re-check: a line recording the same plan is replaced where it stands, a plan
    with no line there gets one after the subsection's last text. The rest of the file is byte-identical; the
    file is replaced through a temp file and a rename. Returns why it refused (no such subsection), else None."""
    text = plan.read_text(encoding="utf-8")
    rows = text.splitlines(keepends=True)
    start = end = None
    fenced = False
    for i, line in enumerate(rows):
        if _FENCE.match(line):
            fenced = not fenced
        elif not fenced and line.startswith("## "):
            if start is not None and end is None:
                end = i
            if _loose(line[3:]) == _loose("Step-4 re-check"):
                start = i
    if start is None:
        return "the plan has no Step-4 re-check section"
    end = len(rows) if end is None else end
    subs = [i for i in range(start + 1, end) if rows[i].startswith("### ")]
    if not subs:
        return "Step-4 re-check has no `### ` subsection: add one (a heading for this run) and run it again"
    lo = subs[-1] + 1
    names = {}
    for ln in lines:
        m = _RECORD.search(ln)
        if m:
            names[m.group(1)] = ln if ln.endswith("\n") else ln + "\n"
    body, placed_, first = [], set(), None
    for line in rows[lo:end]:
        m = _RECORD.search(line)
        if m and m.group(1) in names:
            if first is None:
                first = len(body)
            continue
        body.append(line)
    if first is None:
        last = max((k for k, x in enumerate(body) if x.strip()), default=-1)
        first = last + 1
        if first and not body[first - 1].endswith("\n"):
            body[first - 1] += "\n"
        if first and not _RECORD.search(body[first - 1]) and not re.match(r"\s*[-*+]\s", body[first - 1]):
            body.insert(first, "\n")      # gapfix14 (G295): a new list after prose is set off by a blank line
            first += 1
    new_rows = rows[:lo] + body[:first] + list(names.values()) + body[first:] + rows[end:]
    out = "".join(new_rows)
    if out != text:
        tmp = plan.with_name(plan.name + f".tmp{os.getpid()}")
        tmp.write_text(out, encoding="utf-8")
        os.replace(tmp, plan)
    return None


def record_others(area: str, workspace: Path) -> list[str]:
    """G193 (1.4.39): for each other plan this plan cites, save its text as
    A/other-plans/<plan, `/` as `--`>.<content hash>.md and return the line
    to record in Step-4 re-check."""
    dir_ = workspace / "areas" / area
    out = []
    for c in _cited(area, workspace):
        try:
            raw = c["path"].read_bytes().decode("utf-8")
        except (OSError, UnicodeDecodeError):
            continue
        h = content_hash_of(raw)
        snap = _snapshot(dir_, c["name"], h)
        snap.parent.mkdir(parents=True, exist_ok=True)
        snap.write_bytes(raw.encode("utf-8"))
        out.append(f"- `{c['name']}/area-plan.md {h}`")
    return out


_CARRY_NOTE = re.compile(r"\s*\((?:carried|hosted)\b[^()]*\)\s*$", re.I)
# G184 (1.4.38): where a lead phrase may end: " (", ":", ".", ",", " —", " -" or the item's end.
_LEAD_END = re.compile(r" \(|:|\.|,| —| -|\s*$")
RESEARCH_LABELS = ("Best practices", "Known solutions", "Platform guidelines", "The expert's view")


def _leads(item: str, k: str) -> bool:
    """G184 (1.4.38): whether a list item's text (after its marker) starts with
    loosened phrase `k` followed by a lead boundary (_LEAD_END). Bold markers
    fall away in _loose; a phrase that only starts a longer word or phrase is
    no lead."""
    text = item.strip()
    return any(_loose(text[:e.start()]) == k for e in _LEAD_END.finditer(text))


def _carried(text: str, k: str) -> bool:
    """G184 (1.4.38), the one matcher of survivor_carries and carries_asked:
    whether section `text` (its headings excluded) carries loosened phrase `k`
    as a whole bold span in a list item, a whole list item (_found), or the
    lead of a list item (_leads)."""
    return bool(_found(_chunks(text), k)[0]) or any(
        _leads(_ITEM.match(raw).group(1), k) for _, raw, item in _split(text) if item and _ITEM.match(raw))


def _kind(item: str) -> str:
    """G185 (1.4.38): "research_label" for an item led by one of the four
    research labels (_leads), else "subject". Neither drops the row."""
    return "research_label" if any(_leads(item, _loose(lb)) for lb in RESEARCH_LABELS) else "subject"


def _carry_rows(area: str, workspace: Path, elsewhere: dict[str, str]) -> list[dict]:
    """G150 (1.4.37): for a copy-only plan, [{"question", "subject", "kind",
    "survivors", "why"}] for each top-level Research question whose subject a
    survivor it names (every owner when it names none) does not carry. The
    subject is the item's lead bold span with any trailing "(carried ...)" or
    "(hosted ...)" note stripped (no lead bold: the whole item); a survivor
    carries it when that whole span, case and punctuation aside, is a bold
    span, a whole list item or the lead of a list item in its Research
    questions or Owner questions (_carried, G184, 1.4.38); a survivor with no
    plan carries nothing. `kind` is "research_label" for an item led by a
    research label, else "subject" (G185, 1.4.38); no row is dropped, and a
    row whose subject is a research label or a plan section name (as
    "Missing subjects") is never cleared: it names no subject."""
    plan = workspace / "areas" / area / "area-plan.md"
    rows_ = plan_rows(plan)
    if not rows_ or set(rows_) - set(elsewhere):
        return []
    owners = sorted({"/".join(f.split("/")[2:-1]) for f in elsewhere.values()})
    chunks: dict[str, list] = {}
    for o in owners:
        try:
            s = dict(_sections(workspace / "areas" / o / "area-plan.md"))
        except (OSError, UnicodeDecodeError):
            s = {}
        chunks[o] = ["\n".join(s.get(h, [])) for h in ("Research questions", "Owner questions")]
    try:
        research = dict(_sections(plan)).get("Research questions", [])
    except (OSError, UnicodeDecodeError):
        return []
    out = []
    for line in research:
        m = _ITEM.match(line)
        if not m:
            continue
        lead = _BOLD.match(m.group(1))
        subject = _CARRY_NOTE.sub("", _key(lead.group(1)) if lead else m.group(1).strip()) or m.group(1).strip()
        named = [o for o in owners if re.search(rf"(?<![\w/-]){re.escape(o)}(?![\w-])", m.group(1))]
        k, kind = _loose(subject), _kind(m.group(1))
        # G185 (1.4.38): a research label or a plan section name names no subject: never cleared.
        label = kind == "research_label" or k in {_loose(h) for h in PLAN_SECTIONS}
        lack = [o for o in (named or owners) if label or not k or not any(_carried(c, k) for c in chunks[o])]
        if lack:
            out.append({"question": m.group(1).strip(), "subject": subject, "kind": kind,
                        "survivors": lack,
                        "why": "a survivor plan does not carry this subject as a bold span or list item in its "
                               "Research or Owner questions: an owner item naming that plan and the subject it "
                               "must gain (stage-1.md step 3, G84, G130, G150)"})
    return out


def survivor_carries(area: str, workspace: Path, elsewhere: dict[str, str]) -> list[dict]:
    """G130 (1.4.36), advisory: _carry_rows of this copy-only plan (G150, 1.4.37)."""
    return _carry_rows(area, workspace, elsewhere)


def carries_asked(area: str, workspace: Path) -> list[dict]:
    """G151 (1.4.37), advisory, never a hold: the survivor's side of
    survivor_carries. [{"plan", "question", "subject", "kind", "why"}] for
    each subject another, copy-only plan asks this area to carry and this
    area's plan does not carry yet (no plan here: every such subject); the
    same matcher (_carried) and `kind` as survivor_carries (G184, G185, 1.4.38)."""
    root = workspace / "areas"
    out = []
    for other in sorted(root.glob("**/area-plan.md")) if root.is_dir() else []:
        name = other.parent.relative_to(root).as_posix()
        if name == area:
            continue
        for r in _carry_rows(name, workspace, merged_elsewhere(other, name)):
            if area in r["survivors"]:
                out.append({"plan": name, "question": r["question"], "subject": r["subject"], "kind": r["kind"],
                            "why": f"{name}'s plan asks this area to carry this subject: add it here as a bold "
                                   "span or list item under Research questions or Owner questions (stage-1.md "
                                   "step 3, G151)"})
    return out


# G188, G208, G209 (1.4.39): the host rule's words. A word never counts when it
# is a stop word (paraphrase_hints._COMMON), a word of the area's own path, or
# one of GENERIC; words match on _stem.
GENERIC = frozenset("strategy strategies design designs management manage pattern patterns guideline guidelines "
                    "practice practices approach approaches system systems framework frameworks general basics "
                    "basic overview overviews quality driven configuration based "
                    "cross choose target agent".split())      # 1.4.40 (G229): cross, choos, target, agent
_TOKEN = re.compile(r"[^\W_]+")


def _stem(word: str) -> str:
    """G188 (1.4.39): a simple stem: lowercased; `ies` -> `y`, else one
    trailing `ing`, `ed`, `es` or `s` (never `ss`) stripped while three
    letters remain; then a trailing `e` while more than three remain, so
    "caches", "cache" and "caching" all read "cach"."""
    w = word.lower()
    if len(w) > 4 and w.endswith("ies"):
        w = w[:-3] + "y"
    else:
        for suf in ("ing", "ed", "es", "s"):
            if w.endswith(suf) and len(w) - len(suf) >= 3 and not (suf == "s" and w.endswith("ss")):
                w = w[:-len(suf)]
                break
    return w[:-1] if len(w) > 3 and w.endswith("e") else w


_GENERIC_STEMS = frozenset(_stem(w) for w in GENERIC)


def stems(text: str) -> list[str]:
    """Every word of `text`, stemmed, in order (G190: the stem-matched key)."""
    return [_stem(w) for w in _TOKEN.findall(text.lower())]


def area_words(area: str) -> frozenset[str]:
    """G209 (1.4.39): the stems of every segment of the area's path, split at `/` and `-`."""
    return frozenset(stems(area.replace("/", " ").replace("-", " ")))


_PAIR = re.compile(r"(?<![\w/])([A-Za-z])/([A-Za-z])(?![\w/])")


def specific_words(text: str, area: str, drop: frozenset[str] = frozenset()) -> set[str]:
    """G188 (1.4.39): the stems of `text` that can host: no stop word, no
    area word, no GENERIC word, no number. 1.4.40 (G229, G241): a one-letter
    pair around a slash is one token (`A/B` is `ab`), and `drop` (the stems
    every topic folder name of the plan shares) never counts."""
    from paraphrase_hints import _COMMON
    text = _PAIR.sub(r"\1\2", text)
    return {_stem(w) for w in _TOKEN.findall(text.lower())
            if w not in _COMMON and not w.isdigit() and len(w) > 1} - _GENERIC_STEMS - area_words(area) - drop


def shared_by_folders(topics: dict[str, dict]) -> frozenset[str]:
    """1.4.40 (G229): the stems of the words every topic folder name of the
    plan holds (`checklist` of skill-, agent- and rule-checklist), when it
    has two topics or more: such a word names no coverage."""
    each = [set(stems(t["artifact"].rstrip("/").rsplit("/", 1)[-1].replace("-", " "))) for t in topics.values()]
    return frozenset(set.intersection(*each)) if len(each) > 1 else frozenset()


def qualified(common: set[str], folder_words: set[str]) -> bool:
    """1.4.40 (G229): a topic hosts a subject when they share two stems, or
    one stem that is a whole word of the topic's folder name."""
    return len(common) >= 2 or bool(common and common <= folder_words)


def topic_words(area: str, workspace: Path, repo: Path) -> dict[str, dict]:
    """G209 (1.4.39): {topic: {"artifact", "merged", "words"}} for each row of
    the plan's Proposed topics; "title" is the folder name and the artifact
    title (artifact.json meta.title), both; words as specific_words."""
    out = {}
    for t, r in plan_rows(workspace / "areas" / area / "area-plan.md").items():
        title = ""
        try:
            meta = json.loads((repo / r["artifact"] / "artifact.json").read_text(encoding="utf-8")).get("meta") or {}
            title = str(meta.get("title") or "")
        except (OSError, ValueError, AttributeError):
            pass
        folder = r["artifact"].rstrip("/").rsplit("/", 1)[-1]
        out[t] = {"artifact": r["artifact"], "merged": r["action"] == "merged", "title": title,
                  "words": specific_words(f"{t} {folder} {title}".replace("-", " "), area),
                  "folder_words": set(stems(folder.replace("-", " ")))}
    common = shared_by_folders(out)      # 1.4.40 (G229): a word every folder name holds names no coverage
    for v in out.values():
        v["words"] = v["words"] - common
        v["folder_words"] = v["folder_words"] - common
    return out


_NEW_SUFFIX = re.compile(r"\s*\((?:new|proposed)\)\s*$", re.I)


def research_items(text: str) -> list[dict]:
    """G188 (1.4.39): each top-level list item under Research questions, its
    continuation lines joined: {"topics": the names its `### ` heading lists
    (comma-separated, backticks dropped; [] before any), "no_host": under
    `### No host`, "text", "subject": its lead bold span, a carry note
    stripped, or None, "carried_no_host": it says "carried, no host"}."""
    body = dict(_sections_of(text)).get("Research questions", [])
    items: list[dict] = []
    topics: list[str] = []
    no_host, fenced, open_ = False, False, False
    for line in body:
        if _FENCE.match(line):
            fenced = not fenced
            continue
        if fenced:
            continue
        if line.startswith("### "):
            head = line[4:].strip()
            no_host = _loose(head) == "no host"
            # gapfix13 (G264, 1.4.42): a plan-proposed topic's heading may say `(new)`; the name is before it.
            head = _NEW_SUFFIX.sub("", head)
            topics = [] if no_host else [_NEW_SUFFIX.sub("", x.strip().strip("`* ")) for x in head.split(",")
                                         if x.strip().strip("`* ")]
            open_ = False
            continue
        m = _ITEM.match(line)
        if m:
            items.append({"topics": list(topics), "no_host": no_host, "text": m.group(1).strip()})
            open_ = True
        elif open_ and line.strip() and line[:1] in (" ", "\t"):
            items[-1]["text"] += " " + line.strip()
        elif line.strip():
            open_ = False
    for it in items:
        lead = _BOLD.match(it["text"])
        it["subject"] = (_CARRY_NOTE.sub("", _key(lead.group(1))) or _key(lead.group(1))) if lead else None
        it["carried_no_host"] = f" {_loose(NO_HOST)} " in f" {_loose(it['text'])} "
    return items


def host_check(area: str, workspace: Path, repo: Path) -> list[dict]:
    """G188, G208, G209 (1.4.39), G228, G229 (1.4.40), holds at plan:
    [{"subject", "host", "shares", "why"}] for each Research-question subject
    placed against the host rule (stage-1.md step 3). 1.4.40: every bold-led
    item under a topic's `### ` heading or under `### No host` is checked
    (not only a "carried, no host" one; an item led by a research label is
    skipped), a topic shares a word only with two shared stems or one that is
    a whole word of its folder name (`qualified`), and a word every folder
    name holds is dropped (`shared_by_folders`). A bold-led item under a
    topic's `### ` heading whose topics share no specific word with it (specific_words),
    or are merged copies only (G162), or that another topic shares more words
    with, or that ties with a topic the item does not name or that Owner
    questions do not carry; and a bold-led item under `### No host` that a
    topic shares a specific word with. `shares` is {topic: [stems]} for each
    topic sharing any."""
    plan = workspace / "areas" / area / "area-plan.md"
    try:
        text = plan.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return []
    tw = topic_words(area, workspace, repo)
    common = shared_by_folders(tw)
    hosts = {t: v["words"] for t, v in tw.items() if not v["merged"]}
    owner = _chunks("\n".join(dict(_sections_of(text)).get("Owner questions", [])))
    # gapfix13 (G264, 1.4.42): a bold lead naming a plan section or a topic of the plan is a label, no subject.
    labels = {_loose(h) for h in PLAN_SECTIONS} | {_loose(t) for t in tw} | {_loose(v["title"]) for v in tw.values()
                                                                            if v.get("title")}
    rows = []
    for it in research_items(text):
        if not it["subject"] or not (it["no_host"] or it["topics"]) or _kind(it["text"]) == "research_label":
            continue      # 1.4.40 (G228): every hosted subject; an item led by a research label is no subject
        if _loose(it["subject"]) in labels:
            continue
        words = specific_words(it["subject"], area, common)
        shares = {t: sorted(words & w) for t, w in hosts.items() if words & w and qualified(words & w, tw[t]["folder_words"])}
        best = max((len(v) for v in shares.values()), default=0)
        tying = sorted(t for t, v in shares.items() if len(v) == best)
        why, extra = None, {}
        if it["no_host"]:
            if best:
                why = (f"under `### No host`, yet {', '.join(tying)} share{'s' if len(tying) == 1 else ''} the "
                       f"specific word(s) {', '.join(shares[tying[0]])} with it: host it there"
                       + (" (a tie: name every tying topic in the item and list it under Owner questions)"
                          if len(tying) > 1 else "") + " (stage-1.md step 3, G164, G208)")
        else:
            placed = it["topics"]
            merged = [t for t in placed if tw.get(t, {}).get("merged")]
            live = [t for t in placed if t in hosts]
            got = max((len(shares.get(t, [])) for t in live), default=0)
            named = lambda t: t in placed or names_topic(it["text"], t, tw)
            if not live:
                why = ((f"hosted in {', '.join(merged)}, a merged copy, which is never a host (G162)" if merged else
                        f"hosted under {', '.join(placed)}, no topic of this plan")
                       + (f"; {', '.join(tying)} share(s) {', '.join(shares[tying[0]])}" if best else
                          "; no topic shares a specific word: put it under `### No host`")
                       + " (stage-1.md step 3, G188)")
            elif got == 0:
                why = (f"hosted in {', '.join(placed)}, which share(s) no specific word with it (stop words, the "
                       "area's own words and generic words such as strategy or design never count)"
                       + (f"; {', '.join(tying)} share(s) {', '.join(shares[tying[0]])}: host it there" if best else
                          ": put it under `### No host`") + " (stage-1.md step 3, G164, G188)")
            elif got < best:
                why = (f"hosted in {', '.join(placed)}, but {', '.join(tying)} share(s) more specific words with "
                       f"it ({', '.join(shares[tying[0]])}): host it there (stage-1.md step 3, G209)")
            elif len(tying) > 1 and (not all(named(t) for t in tying) or not _found(owner, _loose(it["subject"]))[0]):
                # gapfix13b (language#5): the row says which half is missing.
                unnamed = [t for t in tying if not named(t)]
                owner_item = bool(_found(owner, _loose(it["subject"]))[0])
                why = (f"a tie: {', '.join(tying)} share {best} specific word(s) with it: the item names every "
                       "tying topic (any case; a hyphen may join a word, as Swift-import names swift) and the "
                       "subject is the whole bold lead of an Owner questions item (stage-1.md step 3, G209); "
                       + (f"not named: {', '.join(unnamed)}" if unnamed else "every tying topic is named")
                       + ("; an Owner questions item leads with it" if owner_item else
                          f"; no Owner questions item's whole bold lead is **{it['subject']}**"))
                extra = {"unnamed": unnamed, "owner_item": owner_item}
        if why:
            # gapfix13 (G264): a tie is listed as `tie`, every tying topic named.
            rows.append({"subject": it["subject"], "host": None if it["no_host"] else ", ".join(it["topics"]),
                         "shares": shares, "tie": tying if len(tying) > 1 else [], "why": why, **extra})
    return rows


def names_topic(text: str, t: str, topics) -> bool:
    """gapfix13b (1.4.42, language#5): whether `text` names topic `t`: the
    name case-folded, at a word start, ending at a word end or before a
    hyphen joining a word (Swift-import names swift), unless the hyphenated
    run is, or starts with, another topic's name (swift-concurrency names
    that topic, not swift)."""
    low = text.lower()
    others = [o.lower() for o in topics if o.lower() != t.lower()]
    for m in re.finditer(rf"(?<![\w-]){re.escape(t.lower())}(?!\w)", low):
        run = re.match(r"[\w-]*", low[m.start():]).group(0).rstrip("-")
        if run == t.lower() or not any(run == o or run.startswith(o + "-") for o in others
                                       if o.startswith(t.lower() + "-")):
            return True
    return False


def shared_no_host(area: str, workspace: Path) -> list[dict]:
    """G190 (1.4.39), advisory: [{"plan", "subject", "other_subject", "why"}]
    for each other plan whose `### No host` list carries a subject this
    plan's `### No host` list carries, the bold leads compared case-folded
    and stem-matched (stems)."""
    def no_host(p: Path) -> dict[tuple, str]:
        try:
            text = p.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            return {}
        return {tuple(stems(i["subject"])): i["subject"] for i in research_items(text)
                if i["no_host"] and i["subject"] and stems(i["subject"])}
    root = workspace / "areas"
    mine = no_host(root / area / "area-plan.md")
    try:        # 1.4.40 (G244): the Owner questions' text, case-folded, to say whether a row is handled
        mine_text = "\n".join(dict(_sections_of((root / area / "area-plan.md").read_text(encoding="utf-8")))
                              .get("Owner questions", [])).lower()
    except (OSError, UnicodeDecodeError):
        mine_text = ""
    rows = []
    for other in sorted(root.glob("**/area-plan.md")) if mine and root.is_dir() else []:
        name = other.parent.relative_to(root).as_posix()
        if name == area:
            continue
        theirs = no_host(other)
        for k, subject in mine.items():
            if k in theirs:
                named = name.lower() in mine_text and (subject.lower() in mine_text
                                                       or all(w in mine_text for w in map(str, k)))
                rows.append({"plan": name, "subject": subject, "other_subject": theirs[k], "named_in_owner": named,
                             "why": f"{name} also carries this subject under `### No host`: one owner answer "
                                    "settles both; name that plan in the owner question (stage-1.md step 3, G190); "
                                    f"named_in_owner {str(named).lower()}: the row stays listed, true once an Owner "
                                    "question names the plan and the subject (G244)"})
    return rows


def _cite_spans(line: str, pc: re.Pattern) -> list[tuple[int, int]]:
    """gapfix13 (G258, 1.4.42): where a line that is no list item can cite a
    folder (tools.md, "cite"): a table cell holding the path alone (bare or
    backticked) and a link target `](...)`."""
    spans = []
    if line.lstrip().startswith("|"):
        pos = 0
        for cell in line.split("|"):
            core = cell.strip().strip("`").strip()
            if core and pc.fullmatch(core):
                spans.append((pos, pos + len(cell)))
            pos += len(cell) + 1
    spans += [(m.start(1), m.end(1)) for m in re.finditer(r"\]\(([^)\s]*)\)", line)]
    return spans


def stale_pointer(area: str, workspace: Path) -> list[dict]:
    """G216 (1.4.39), advisory: [{"pointer", "survivor", "section", "line",
    "why"}] for each cite, outside Overlaps, Proposed topics and Step-4
    re-check, of a topic folder the worklist folds (a copy) or a plan merges
    into a survivor, whose list item or paragraph does not name that
    survivor. gapfix13 (G258, 1.4.42): only a cite is read (tools.md): the
    folder in a list item, as a whole table cell, or as a link target; prose
    paragraphs, headings, whole-bold heading lines and table cells holding
    more than the path are not."""
    plan = workspace / "areas" / area / "area-plan.md"
    try:
        text = plan.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return []
    folded: dict[str, str] = {}
    for t in _worklist_topics(workspace):
        surv = _cb(t["survivor"])
        for c in t.get("copies") or []:
            folder = _cb(c.get("folder") if isinstance(c, dict) else c)
            if folder and folder != surv:
                folded[folder] = surv
    for m in all_merges(workspace):
        folded.setdefault(m["copy"], _cb(m["artifact"]))
    rel = lambda f: f.removeprefix("cookbook/guidelines/")
    pat = lambda f: re.compile(rf"(?<![\w./-])(?:(?:cookbook/)?guidelines/)?{re.escape(rel(f))}(?!/?[\w-])")
    pats = {c: (pat(c), pat(s)) for c, s in folded.items()}
    skip = {_loose(h) for h in ("Overlaps", "Proposed topics", "Step-4 re-check")}
    specs = {str(r.get("speciality")) for r in _rows_of(plan.parent / "reference.json")[0] if r.get("speciality")}
    fold = re.compile(r"\bfold(?:s|ed|ing)?\b|\bmerged into\b", re.I)
    blocks, cur, ctx = [], None, False      # 1.4.40 (G234, G235): one list item or paragraph, wrapped lines joined
    for i, section, line in _numbered_lines(text):
        if _loose(section) in skip:
            cur = None
            continue
        if not line.strip():
            cur = None
            continue
        head, item = line.startswith("#"), bool(_ITEM.match(line.lstrip()))
        if cur is None or head or item:
            cur = {"section": section, "lines": [], "list": item, "head": head}
            blocks.append(cur)
        cur["lines"].append((i, line))
    rows = []
    for blk in blocks:
        whole = " ".join(x.strip() for _, x in blk["lines"])
        has_fold = bool(fold.search(whole))
        if not blk["list"]:
            ctx = has_fold          # a paragraph or heading saying the copies are folded covers the items under it
        if has_fold or (blk["list"] and ctx) or whole.startswith(">"):
            continue
        for c, (pc, ps) in pats.items():
            if not pc.search(whole) or ps.search(whole):
                continue
            hit = None
            for i, line in blk["lines"]:
                spans = None if blk["list"] else _cite_spans(line, pc)
                for m in pc.finditer(line):
                    if spans is not None and not any(a <= m.start() and m.end() <= b for a, b in spans):
                        continue        # gapfix13 (G258): prose, a heading, a cell of more than the path
                    ticked = line[:m.start()].endswith("`") and line[m.end():].startswith("`")
                    if ticked and (rel(c) in specs or re.search(r"\bspecialit", whole, re.I)):
                        continue        # a speciality id, never a folder
                    hit = hit or (i, m.start() + 1, m.group(0))
            if hit:
                rows.append({"pointer": rel(c), "survivor": rel(folded[c]), "section": blk["section"],
                             "line": hit[0], "column": hit[1], "matched": hit[2],
                             "why": f"cites {rel(c)} at line {hit[0]} column {hit[1]}, folded or merged into "
                                    f"{rel(folded[c])}: the whole list item or paragraph is read (wrapped lines "
                                    "joined): name the survivor in it, or say `folded`, `fold` or `merged into` "
                                    "beside the copy; a cite is the folder in a list item, as a whole table cell "
                                    "or as a link target (tools.md): prose, headings and longer cells are not read; "
                                    "a backticked speciality id, a list under a line saying the copies are folded "
                                    "and a `>` quoted line are skipped (G216, G234, G235, G258)"})
    return rows


def _report_stale(dir_: Path) -> list:
    """What A/run_gaps.json makes stale. With no report: [] when there is no
    plan yet (the plan step runs it), else one OLD_REPORT row, NO_REPORT_WHY
    (G99, 1.4.33: a plan saved before 1.4.26 or never measured).

    N3-I-1 (1.4.29): a report saved under an older reference format, or
    recording none, or unreadable, is one row (reference_format.report_row):
    a `marked_here` reference has no stamp on disk, so only a report of the
    current format vouches for it. A fresh run_gaps.py run clears the row.

    N4-I-1 (1.4.30): so is a current report that lists a stale row, an
    OLD_FORMAT one or one with no `reason`: it was saved by a run that
    measured a stale reference (exit 1), and rewriting A/reference.json
    without a re-run leaves that measure in place.

    R2-M-2, N3-M-2: a current report's own `marked_here` rows, the ones
    run_gaps.py could not rewrite, picked by `reason` NO_WRITER and never by
    the wording of `why`."""
    path = dir_ / "run_gaps.json"
    if not path.is_file():      # G99 (1.4.33): a plan no saved report vouches for
        return [report_row(str(path), None, NO_REPORT_WHY)] if (dir_ / "area-plan.md").is_file() else []
    try:
        report = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return [report_row(str(path), None)]
    fmt = report.get("reference_format") if isinstance(report, dict) else None
    if not is_current(fmt):
        return [report_row(str(path), fmt)]
    rows = report.get("stale_reference")
    if rows is not None and not isinstance(rows, list):      # N5-M-1 (1.4.31): what it listed is unknown
        return [report_row(str(path), fmt, REPORT_STALE_WHY)]
    rows = rows or []
    no_writer = [r for r in rows if isinstance(r, dict) and r.get("reason") == NO_WRITER]
    return ([report_row(str(path), fmt, REPORT_STALE_WHY)] if len(no_writer) < len(rows) else []) + no_writer


def _rows_of(path: Path) -> tuple[list, bool]:
    """(A/reference.json's rows, whether it reads as rows). An absent file is
    ([], False) beside a plan: step 1.1 always writes one ([] for an area
    with no speciality), so its absence holds the area; with no plan yet it
    is ([], True), nothing to read. Invalid JSON or a non-list is ([], False);
    a list holding any non-dict is (its dicts, False) (N5-I-1, 1.4.31)."""
    if not path.is_file():
        return [], not (path.parent / "area-plan.md").is_file()
    try:
        rows = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return [], False
    if not isinstance(rows, list):
        return [], False
    dicts = [r for r in rows if isinstance(r, dict)]
    return dicts, len(dicts) == len(rows)


def stale_gaps(area: str, workspace: Path, repo: Path) -> list[str] | dict:
    """Each A/gaps/*.json that the area's current measurement set
    (run_gaps.py) does not write, an R9 `new-<name>.json` excepted; [] when
    A/reference.json or A/unmeasured.json is missing or unreadable;
    {"refused": why} when two topic folders share a basename (the set is
    unknown, so no file can be called current)."""
    import run_gaps  # run_gaps imports this module: import it here, not at the top
    try:
        topics = run_gaps.measures(area, workspace, repo)["topics"]
    except run_gaps.Clash as e:
        return {"refused": str(e)}
    except run_gaps.Refused:
        return []
    return run_gaps.stale(workspace / "areas" / area / "gaps", topics)


# G153 (1.4.37): the advisory lists (other_plans_changed, survivor_carries,
# carries_asked) are out: a sibling plan's rewrite never moves this plan's digest.
# G188 (1.4.39): host_check is a hold, so it is in the digest.
DIGEST_KEYS = ("plan_sections", "stale_reference", "r9_stale", "stale_copy_check", "host_check", "cite_moved",
               "stale_verdicts")
ADVISORY_KEYS = ("other_plans_changed", "survivor_carries", "carries_asked", "shared_no_host", "stale_pointer",
                 "non_home_lacking", "report_refresh", "short_not_owed")


def digest(result: dict) -> str:
    """G137 (1.4.36): one line for Step-4 re-check: `next`, the count of each
    hold, and a hash of their rows; nothing else of the plan is in it, so
    recording it, or any hash, in Step-4 re-check leaves it unchanged (G155,
    G183, 1.4.37). The advisory lists are not in it (G153)."""
    picked = {"next": result["next"], **{k: result[k] for k in DIGEST_KEYS}}
    # gapfix13b (language#3): a stale_verdicts row's texts are for judging; the digest keeps its 1.4.41 fields.
    picked["stale_verdicts"] = [{k: r.get(k) for k in STALE_DIGEST_FIELDS} if isinstance(r, dict) else r
                                for r in picked["stale_verdicts"]]
    h = hashlib.sha1(json.dumps(picked, sort_keys=True, default=str).encode("utf-8")).hexdigest()[:12]
    counts = "; ".join(f"{k} {len(result[k])}" for k in DIGEST_KEYS)
    stale = ""
    for r in result.get("report_refresh") or []:      # gapfix14 (G291): a stale view says so, outside the hash
        if isinstance(r, dict):
            stale = (f"; report_refresh 1 (stale: {', '.join(r.get('stale_views') or STALE_VIEWS)}; refresh: "
                     f"{r.get('command') or 'run_gaps.py --hints (step 1.3)'})")
    return f"stage_status.py {result['area']}: next {result['next']}; {counts}; result {h}{stale}"


def _run(cmd: list[str]) -> tuple[int, str, str]:
    import subprocess
    r = subprocess.run(cmd, capture_output=True, text=True)
    return r.returncode, r.stdout, r.stderr


def first_check(area: str, ws: Path, repo: Path, runner=_run) -> int:
    """gapfix13 (G262, G267, 1.4.42): write A/first-check.txt, the re-run's first check: the digest line (the
    last stdout line) of `unmeasured.py --check --digest`, `run_gaps.py --check --hints --digest` and
    `stage_status.py --digest`, in that order, one per line, nothing else. An old first-check.txt is first saved
    as A/first-check-before-<running skill version>.txt; a backup of that name already there is kept as it is.
    A check that exits 2 or more (1 is a check's "rows found") writes nothing. Each command runs under this
    python (sys.executable): run this under $COOKR_PY."""
    here = Path(__file__).resolve().parent
    flags = ["--area", area, "--workspace", str(ws), "--repo", str(repo)]
    lines = []
    for script, extra in (("unmeasured.py", ["--check", "--digest"]),
                          ("run_gaps.py", ["--check", "--hints", "--digest"]),
                          ("stage_status.py", ["--digest"])):
        code, out, err = runner([sys.executable, str(here / script), *extra, *flags])
        rows = [x for x in out.splitlines() if x.strip()]
        if code > 1 or not rows:
            sys.stderr.write(err)
            print(f"stage_status.py: --first-check: {script} {' '.join(extra)} exited {code}"
                  + ("" if rows else " with no digest line") + "; nothing written", file=sys.stderr)
            return 2
        lines.append(rows[-1])
    d = ws / "areas" / area
    old = d / "first-check.txt"
    if old.is_file():
        keep = d / f"first-check-before-{skill_version()}.txt"
        if keep.exists():
            print(f"stage_status.py: --first-check: {keep.name} is already there; kept as it is (first-check.txt "
                  "rewritten below; G290)", file=sys.stderr)
        else:
            keep.write_bytes(old.read_bytes())
            print(f"stage_status.py: --first-check: the old first-check.txt saved as {keep}", file=sys.stderr)
    tmp = old.with_name(old.name + f".tmp{os.getpid()}")
    tmp.write_text("".join(x + "\n" for x in lines), encoding="utf-8")
    os.replace(tmp, old)
    for x in lines:
        print(x)
    print(f"stage_status.py: --first-check: written to {old}", file=sys.stderr)
    return 0


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    add_area(ap)
    ap.add_argument("--workspace", help="default: <repo>/docs/grow-cookbook")
    ap.add_argument("--keys", "--summary", action="store_true", help="print each output key, never dropping one: the rows of every hold and advisory list whole (json_keys.ROW_KEYS), any other list as {\"rows\": N} or [], a dict as its keys, a scalar as it is (json_keys.py)")
    ap.add_argument("--rows", metavar="KEY[,KEY]", help="print each output key named whole (G138; several, "
                    "comma-separated, G219)")
    ap.add_argument("--record-others", action="store_true",
                    help="save each other plan this plan cites as A/other-plans/<plan>.<hash>.md and print the "
                         "lines to record in the last ### subsection of Step-4 re-check (G186, G193)")
    ap.add_argument("--write", action="store_true",
                    help="with --record-others: put those lines into the last ### subsection of Step-4 re-check "
                         "of A/area-plan.md, replacing a line that records the same plan; refuses when it has none "
                         "(G236)")
    ap.add_argument("--digest", action="store_true",
                    help="print one line to record in Step-4 re-check; it does not read that record (G137)")
    ap.add_argument("--first-check", action="store_true",
                    help="write A/first-check.txt: the digest lines of unmeasured.py --check --digest, run_gaps.py "
                         "--check --hints --digest and stage_status.py --digest, in that order; an old one is first "
                         "saved as A/first-check-before-<this skill version>.txt (gapfix13, G262, G267)")
    ap.add_argument("--repo", help="default: the nearest cookbook at or above this directory (repo_path.py)")
    a = ap.parse_args(argv)
    a.area = area_arg(ap, a)
    # A relative path is relative to the current directory, as any shell file
    # argument is; both are made absolute here so `dir` names one place.
    try:
        repo = Path(os.path.abspath(os.path.expanduser(a.repo))) if a.repo else cookbook_repo(None, "stage_status.py")
    except SystemExit as e:
        print(e, file=sys.stderr)
        return 2
    ws = Path(os.path.abspath(os.path.expanduser(a.workspace))) if a.workspace else repo / "docs" / "grow-cookbook"
    # A repo with no cookbook would read as an area with nothing done (every
    # artifact missing, cookr None): say so and stop instead.
    lacks = [what for what, there in (("no cookbook/ directory", (repo / "cookbook").is_dir()),
                                      ("no skills/cookr/SKILL.md", (repo / "skills/cookr/SKILL.md").is_file()))
             if not there]
    if lacks:
        print(f"stage_status.py: --repo {repo} holds no cookbook ({', '.join(lacks)}). Pass the cookbook "
              "checkout's root: git -C ${CLAUDE_SKILL_DIR} rev-parse --show-toplevel", file=sys.stderr)
        return 2
    why = check_area("stage_status.py", ws, a.area, repo)         # G198 (1.4.39)
    if why:
        print(why, file=sys.stderr)
        return 2
    if a.first_check:
        return first_check(a.area, ws, repo)
    if a.record_others:
        lines = record_others(a.area, ws)
        for line in lines:
            print(line)
        if a.write:
            plan = ws / "areas" / a.area / "area-plan.md"
            before = plan.read_bytes() if plan.is_file() else b""
            why = write_records(plan, lines) if lines else None
            if why:
                print(f"stage_status.py: --write: {why}; nothing written", file=sys.stderr)
                return 2
            # gapfix13 (G265, 1.4.42): say what --write did; a no-op is `no change`, exit 0.
            print("stage_status.py: --write: " + ("no change: every recorded hash is current" if plan.is_file() and plan.read_bytes() == before
                                                    else f"written to the last ### subsection of {plan}"),
                  file=sys.stderr)
        return 0
    if a.write:
        print("stage_status.py: --write goes with --record-others", file=sys.stderr)
        return 2
    result = status(a.area, ws, repo)
    from json_keys import split_keys
    wanted = split_keys(a.rows)
    for k in wanted:
        if k not in result:
            from json_keys import owner_of
            print(f"stage_status.py: no output key {k!r}" + (f"; {owner_of(k, 'stage_status.py')}"
                                                              if owner_of(k, "stage_status.py") else "")
                  + f"; keys: {', '.join(result)}", file=sys.stderr)
            return 2
    if result["pending_target"]:
        print(f"stage_status.py: {a.area}: {result['next_why']}", file=sys.stderr)
    if a.digest:
        # G195 (1.4.39): the advisory lists the digest leaves out, counted apart. gapfix13 (G261): before the
        # digest line, which prints last.
        print("stage_status.py: advisory (not in the digest): "
              + "; ".join(f"{k} {len(result[k])}" for k in ADVISORY_KEYS), file=sys.stderr)
        sys.stderr.flush()
        print(digest(result))
    elif a.rows is not None:
        print(json.dumps({k: result[k] for k in wanted}, indent=2))
    else:
        out = output_keys(result) if a.keys else result
        if a.keys:      # G219 (1.4.39): --rows other_plans_changed prints the rows
            rows_ = result["other_plans_changed"]
            out["other_plans_changed"] = {"rows": len(rows_), "plans": [r["plan"] for r in rows_]} if rows_ else []
            # gapfix14 (G298, 1.4.43): a stale_verdicts row's topic files as a count; --rows keeps the paths
            out["stale_verdicts"] = [{**r, "topic_files": {"files": len(r["topic_files"]),
                                                           "paths": "--rows stale_verdicts"}}
                                     if isinstance(r.get("topic_files"), list) else r
                                     for r in result["stale_verdicts"]]
        print(json.dumps(out, indent=2))
    return 0


if __name__ == "__main__":
    from repo_path import run_main      # gapfix13 (G263, G271)
    run_main(main)
