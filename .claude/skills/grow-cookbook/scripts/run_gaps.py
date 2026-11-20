#!/usr/bin/env python3
"""Step 1.3's gaps, measured: every `cookr roles gaps` command the area owes,
built from its reference and unmeasured files, run, and summed per topic.

    $COOKR_PY run_gaps.py --area <area> --workspace <workspace> --repo <repo> [--out DIR] [--hints] [--check]
        [--devteam DIR]

A run saves its JSON itself (G90), atomically, as `A/run_gaps.json` when
`--out` is the default `A/gaps`, and as `<out>/run_gaps.json` inside any
other `--out` folder (1.4.26: a scratch run never overwrites the area's
report); a run that exits 2 saves it too. A refused input (exit 2 before any
run, naming it) and `--check` never write it. A run that lists any
`stale_reference` saves its report and exits 1, naming each on stderr
(1.4.28). Every report records `reference_format`, the
reference_format.REFERENCE_FORMAT it was measured under (1.4.29):
stage_status.py lists a saved report with none, or a lower one, in its
`stale_reference`, and a fresh run clears that. An `--out` that resolves to the area folder, to a folder holding
it (1.4.27), or to a folder inside it other than A/gaps or below (1.4.28) is
refused (exit 2);
one that resolves to `A/gaps` is the default, whatever its spelling. With no `--repo`, the repo is the nearest folder at or above the
working directory holding `cookbook/guidelines/` (repo_path.py).

Reads `A/reference.json`, `A/unmeasured.json`, `<workspace>/worklist.json`
and, when it exists, `A/area-plan.md` (A is `<workspace>/areas/<area>`).
Each topic folder is measured against (each file once, in this order):
- the `file` of every `A/reference.json` row whose `topic` is the folder,
  an `against_survivor` row on its `survivor`, a `survivor_elsewhere` row
  never (the survivor's plan measures it);
- the file of every speciality the folder's worklist topic (its `survivor`
  or `new_home` in the area) names in its `devteam` entries;
- the `file` of every `building` row, at each of its `via` topics.
A topic name resolves to its folder through the plan's Proposed topics row
(its Artifact), else the worklist (a `new_home` names its `survivor`), else
itself. A folder whose plan row is `merged` with its Artifact in another
area is measured by that area's plan (G36): it is listed in
`measured_elsewhere` with that `plan`, not run, not counted. A folder that
does not exist (a `new` topic) is listed in `unmeasurable` (G35): its
building sentences are its gaps, quoted in its Why cell and its research
questions. Two folders with one basename exit 2: each writes
`<out>/<basename>.json`. Every plan row `merged` with its Artifact in another
area is in `measured_elsewhere`, whatever its speciality (`specialities` []
when no speciality of this area names it: G46). With no topic to measure,
`why_empty` says why ("area has no speciality", every topic merged or
measured elsewhere, ...); it is null otherwise. A speciality that a `new`
worklist topic of this area claims, but whose reference row names a folder
outside the area, is that new topic's R9 target (G53): listed in
`r9_targets` as {"topic", "candidate", "speciality", "file", "out":
"new-<name>.json"}, owed in `r9_missing` until that file exists, and never
measured as an existing topic.

Each command runs under `write_on_success.py` (`PYTHONPATH=<cli> $COOKR_PY
-P -m cookr`, `<cli>` being `<repo>/skills/cookr/cli` when it holds cookr) into a
scratch file in `--out` (default `A/gaps`); the file gains, per reference,
`lacking_numbers`: beside each `lacking_sentences` piece, the number
quote_building.py gives the sentence holding it (cookr also cuts at `;` and
`:`, so one quote_building sentence may hold several pieces: G34). Only then
does it replace `<out>/<topic>.json`, in one atomic step. A run that exits
non-zero, prints no JSON or names a file it cannot read keeps the previous
file, is listed in `failed` and makes the exit 2.

Each building sentence (G33, 1.4.19 I1, I2; 1.4.20) gets `home_guess`, `held_at` and
`lacking_at`. `home_guess` is advisory: a measured topic that holds it, else
the measured topic sharing most of its words, at least HOME_SHARE of them;
null below that, and when two topics tie (its home may be a topic not
measured: outside `via`, or a new topic). The plan names each home and
judges the sentence there. `gap_candidates` lists the measured sentences
marked for this area (its own `A/building-<name>.json` or another plan's
`marked_here`) held at no measured topic, before the held-in-other-words
notes. A sentence is `measured` only when cookr measured every piece of
it: `unmeasured_sentences` lists every sentence, whatever its mark, as
{"n", "marked_for": <its mark: an area, a list of areas, or null>} (G48,
G64: the plan judges its own and leaves another area's to it), with any piece cookr did not measure (a piece under six words,
named in the sentence's `unmeasured_parts`, or the file measured at no
topic: `measured_at` is []) or any piece no one sentence could be given
(`unplaced_parts`): each is judged by hand at its home topic and is a gap
unless held. Such a sentence never reads as held: its own `held_at` and
`lacking_at` stay [] (1.4.22). One measured in part keeps its measured
pieces' verdicts under `measured_pieces`: {"held_at", "lacking_at"}, which
is not a verdict on the sentence (`by_hand` says so on the entry), keeps
the `home_guess` drawn from them, and is never a gap candidate (1.4.21).
A piece `numbers()` gives no sentence is never dropped (1.4.22): the
entry's `unplaced_pieces` lists it as {"text", "measured", "verdict",
"topic", "sentences"}: a piece cookr did not measure once (`verdict` and
`topic` null), a measured one once per measured topic (`verdict` "lacking"
at each `topic` whose `lacking_sentences` lists it, numbered there or not,
1.4.23; else "held"). `sentences` numbers each sentence its words
overlap: each one gets `unplaced_parts` and is judged by hand; [] means no
sentence can be chosen and the piece is judged by hand alone. A topic row
and each of its references count their lacking pieces with no number in
`unplaced`. `other_area` lists the ones marked for
other areas only (never this area's gap); `unmarked` the ones with no mark.
A mark may be a list of areas (mark.py, G55): it is this area's when the
list names it. `unplaced_pieces` is always there, [] when none (G56). Each
sentence held at no measured topic, or with a piece not measured, gets
`lacking_candidates`: up to 3 {"topic", "share"}, every topic folder of
the area ranked by the share of its words they hold, folders no speciality
names included; with no `home_guess` yet, the first at HOME_SHARE or more,
untied, becomes it (G50, advisory). `same_text` groups one lacking piece's
text found in several specialities as {"text", "specialities", "topics"}:
one hand judgement covers the group, and each speciality still lists it
(G51).
While any topic `failed`, each building entry carries `partial`: those
topics, so its figures are not the area's. `--hints` adds, to each sentence
held at no measured topic (so to every sentence with a piece not measured,
whatever its measured pieces say), paraphrase_hints.py's top 3 topic sentences
(`hints`, each naming its `topic`): at its `home_guess` (`hints_at` names
it), or, with no guess, over every measured topic (`hints_at`: "every
measured topic"; a topic whose run failed is never ranked, 1.4.21). A
`home_guess` may be any topic folder of the area, one no speciality names
too: its hints are ranked there (G66). A failing advisory part (hints)
never stops the run: it is listed in `advisory_failed` as {"part",
"speciality", "n", "why"}, named on stderr, every file is still written,
and the exit is unchanged (G66, G82).

`short_sentences` (G72) lists every piece cookr leaves out of the measure
(under six words) of every speciality's file, direct, building, R9 or
home-measured, measured at a topic or not, as {"speciality", "n", "text"}
(`n` is quote_building's number, null when no one sentence holds it):
each is judged by hand.

`home_measures` (G68): each building sentence whose `home_guess` is a topic
its file was not measured at (most often a topic no speciality names), and
each sentence of a `marked_here` speciality with no building row, is
measured at that home: one `<out>/home--<name>.json` per home (two
hyphens: no topic folder's own file can take that name, 1.4.26), written and
cleared as the topic files are (never an R9 `new-*`). A `marked_here`
speciality's reference is rewritten on every run (it has no
A/reference.json row to stamp; 1.4.27, never reused) into `A/reference/`
(`DIR/reference` with `--out DIR`) by `<devteam>/speciality_reference.py`
(`--devteam`, default `<repo>/../..`; `--check` writes it into its scratch
folder); with no such script an existing file is used and listed in
`stale_reference`, else the speciality is listed in `missing_files`; its sentences' home is guessed as `lacking_candidates`
guesses, and a sentence with none is listed in `home_unguessed`. A
`marked_here` row is checked by its text, not its number alone (1.4.26):
when the reference's sentence `n` is not the row's `text` (normalised as
quote_building compares), or the row has no text, it is listed in
`numbering_differs` as {"speciality", "n", "text", "now" (the sentence now
at n, or null), "found_at" (every number whose sentence is the text),
"measured_as"} and measured as the one sentence its text names, by `n` when
it has no text, and not at all (`measured_as` null) otherwise: such a row
is in `home_unguessed` too, judged by hand or re-marked (1.4.27). A row two
plans mark is listed and measured once (1.4.27). `stale_reference` lists
each A/reference.json row older than reference_format.REFERENCE_FORMAT
(1.4.27); `--check` counts a non-empty one as a change. Each stale row
names its `reason` (1.4.29): "old_format" for an A/reference.json row,
"no_writer" for a `marked_here` reference no script could rewrite (none, or one whose FORMAT is older, 1.4.46). Rows:
{"topic", "folder", "gaps_file", "specialities", "sentences": [{"speciality",
"n", "verdict": "held" | "lacking" | "not measured"}]} ("not measured": a
piece of it is under six words, judged by hand, or the home file holds no
row for its reference: that row then names the file in
`unmeasured_references`, 1.4.26). A home measure that fails is in `failed`.

Before measuring, a run clears from `<out>` each file no topic of this set
writes that it wrote itself (it carries `"written_by": "run_gaps.py"`, or,
written before 1.4.24, every reference has `lacking_numbers`), and
lists them in `cleared`; an R9 `new-<name>.json` is never cleared (G45).
`stale_gaps` lists each other `<out>/*.json` no topic of this set writes,
an R9 `new-<name>.json` excepted (G32). `--check` writes nothing: it
measures into a scratch folder, compares that with the saved report
(`report_path`: `A/run_gaps.json`, or `DIR/run_gaps.json` under
`--check --out DIR`, 1.4.27; every key but `out`, `note`,
`cleared`/`would_clear`, `hints` and the hints, `advisory_failed` compared
too, 1.4.26, but only when the saved run's `hints` matches the check's,
else it is named in `not_compared`, 1.4.27: a missing report is a change) and with the saved `<out>` files,
counts a non-empty `would_clear` as a change (G67), and prints {"area", "check": "changed" | "unchanged", "out", "report", "would_clear",
"failed", "unplaced", "stale_reference", "not_compared"?, "new_keys"?, "changes": [{"path", "was", "now"} | {"path", "added",
"removed"}]}; exit 0 unchanged, 1 changed, 2 a run failed or `unplaced` is
not empty (G45; fix round 2). `r9_missing` lists each `new` plan row
owed an R9 measure with no `<out>/new-<name>.json`: R9 measures are run by
hand. A new topic is owed one when its worklist entry's `kind` is
`shared-different` (a candidate survivor to measure against), or when the
worklist has no entry for it; a `checklist`, `variant` or `none` one is
not (1.4.20). Prints JSON: {"area", "out",
"note", "topics": [{"topic", "folder", "gaps_file", "pieces", "held",
"lacking", "unplaced", "references": [{"speciality", "file", "pieces", "held", "lacking",
"lacking_numbers", "unplaced"}], "lacking_by_home_guess": [{"speciality", "n",
"home_guess", "measured": false?}]}] (`measured`: false marks a sentence
measured only in part); each topic also has `own` and
`building_marked_elsewhere`, {"pieces", "held", "lacking"} each, summing to
its totals: the second counts building pieces whose sentence is marked for
other areas only (G52). "building": [{"speciality", "file", "measured_at", "sentences": [{"n",
"mark", "measured", "unmeasured_parts"?, "unplaced_parts"?, "home_guess", "lacking_candidates"?, "held_at", "lacking_at",
"measured_pieces"?, "by_hand"?, "hints"?, "hints_at"?}],
"gap_candidates", "unmeasured_sentences", "other_area", "unmarked",
"unplaced_pieces": [{"text", "measured", "verdict", "topic", "sentences"}],
"partial"?}], "same_text", "why_empty", "cleared" | "would_clear", "r9_targets", "measured_elsewhere": [{"topic", "folder", "plan",
"specialities"}], "unmeasurable": [{"topic", "folder", "specialities"}],
"missing_files": [{"speciality", "why"}], "stale_gaps", "r9_missing",
"failed": [{"topic", "why"} | {"speciality", "why"}], "unplaced": [{"topic",
"folder", "why"}], "short_sentences", "home_measures", "home_unguessed": [{"speciality", "n", "text",
"why"}], "advisory_failed", "stale_reference": [{"speciality", "file", "format", "want",
"why", "reason"}], "reference_format", "hints", "r9_stale": [{"file", "input", "reference",
"recorded", "current", "reason", "why"}] (G94: an R9 file measured on another
reference text than A/reference holds now, or, 1.4.34, on a survivor folder
since changed; stage_status holds the area at plan),
"markers" (G72: pieces that are only a list marker), "repeat_of":
[{"speciality", "text", "sentences", "topics"}] (G104: a lacking sentence
restating an earlier one; advisory, each still counts where it stands)}.
`short_sentences` rows carry `marked_for`, `topic`/`topics`, `fragment` and
`kind` ("label": a heading label or procedure opener, G103); a home guess
carries `home_shared_words` (G121). `--check` adds "hints" and "hints_from"
("flag" or "report": without --hints/--no-hints it runs as the saved report
ran, G96). `--keys`/`--summary` prints each output key with its shape only
(json_keys.py, G119); `--digest` prints the one line the plan records (a
run adds one line per topic it names, G120). 1.4.36: `--keys`, `--summary`,
`--digest` and `--rows KEY` without `--check` read the saved report and
never run or write (exit 2 naming step 1.3's command when there is none),
and a write run with neither hints flag keeps the saved report's `hints`
(G122); `--rows KEY` prints one key whole (G138); "held_by_wording":
[{"speciality", "n", "text", "topic", "marked_for", "number_differs"}],
every cookr hold, re-judged by the plan (G132); `kind` is "marker", "cut",
"heading", "label", "opener" or "piece", an uncertain one "piece" (G125);
`marked_for` is never null: resolved from every plan's marks, else
"unmarked" or "unknown" (G123, G124); a row marked for other areas only is
tagged `count_only`, a home recorded with `mark.py --home` is
`home_recorded` (G145); a `repeat_of` row carries `review_focus_pair` and
`pieces` (G146); a saved view does not repeat `r9_stale` stderr (G140).
1.4.37: a held_by_wording row also carries `id` and `topic_sentence` (the
topic's sentence nearest the piece), and `verdict` when `mark.py --held`
recorded one for this very sentence pair, else `verdict_was` and
`verdict_why` (G159); `home_recorded` also reads A/homes.json, a home in
another area as `<area>:<topic>` (G156); an "opener" is a piece starting
Review or Closing, or a procedure lead (Before, After, When ...) ending in
`:` (G161); a --check change to a short_sentences row whose kind changed
carries `kind_changed` [old, new] (G180); `--check --out DIR` with no
DIR/run_gaps.json is refused, exit 2 (G172). (a building file cookr cannot cut fails under its
`speciality`; a topic folder that cannot be read is listed in `unplaced`
with its error, never left out, and exits 2). A relative speciality file
is refused. A missing or unreadable
input exits 2, naming it.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from json_keys import cap, keys as output_keys, owner_of, split_keys  # noqa: E402
from mark import stale_homes  # noqa: E402
from paraphrase_hints import rank, topic_sentences, words  # noqa: E402
from paraphrase_hints import rank as nearest_rank  # noqa: E402  (G159: not the hints' advisory rank)
from quote_building import _mark, areas_of, sentences  # noqa: E402
from reference_format import (NO_WRITER, NO_WRITER_WHY, REFERENCE_FORMAT, WHY as STALE_WHY, blob_hash,  # noqa: E402
                              is_current, r9_stale, stale_reference, writer_format)
from repo_path import check_area, cookbook_repo, python_hint, skill_version  # noqa: E402
from stage_status import _area_of, plan_rows  # noqa: E402
from unmeasured import changes, plan_marks  # noqa: E402


WRITTEN_BY = "run_gaps.py"


class Refused(Exception):
    """An input that stops the run: exit 2, naming it."""


class Clash(Refused):
    """Two topic folders with one basename: each would write one gaps file."""


HOME_SHARE = 0.4   # below it, no measured topic is guessed as the home
BY_HAND = ("judged by hand at its home topic: measured_pieces covers only the pieces cookr measured, "
           "and is not a verdict on the sentence")
R9_KINDS = {"shared-different"}   # a new topic's worklist kind that owes an R9 measure


def note() -> str:
    """The output's advisory note, naming the HOME_SHARE in force."""
    return ("home_guess and gap_candidates are an advisory guess, before the held-in-other-words notes: "
            "the plan names each sentence's home topic and judges it there. home_guess is null when no "
            f"measured topic holds the sentence or shares {HOME_SHARE:.0%} of its words (its home may be a "
            "topic not measured: outside `via`, or a new topic), and when two topics tie. Each "
            "unmeasured_sentences sentence (a piece cookr did not measure, or one no sentence could be "
            "given) is judged by hand at its home topic and is a gap unless held: its held_at and lacking_at "
            "are empty. Where some of its pieces were measured, their verdicts are under measured_pieces: "
            "they cover those pieces only and are not a verdict on the sentence, which is not held until "
            "judged by hand (a lacking_by_home_guess row for it carries measured: false). Each "
            "unplaced_pieces entry is a piece no one sentence could be given: judge it by hand, with each "
            "sentence its `sentences` names; none of them is held because of it.")


def _folder(path: str) -> str:
    path = path.strip().strip("`").rstrip("/")
    return "cookbook/" + path if path.startswith("guidelines/") else path


def _load(path: Path):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError) as e:
        raise Refused(f"run_gaps.py: cannot read {path} ({e.__class__.__name__}: {e})") from e


def _plan_names(plan: dict, action: str) -> list[str]:
    return [n for n, r in plan.items() if r.get("action") == action]


def measures(area: str, workspace: Path, repo: Path) -> dict:
    """The area's measurement set: {"topics": {basename: {"topic", "folder",
    "against": [(speciality, file)]}}, "measured_elsewhere", "unmeasurable",
    "missing_files"}. Raises Refused on a missing input or a basename clash."""
    a = workspace / "areas" / area
    rows = _load(a / "reference.json")
    if not isinstance(rows, list) or not all(isinstance(r, dict) for r in rows):
        raise Refused(f"run_gaps.py: {a / 'reference.json'} is not a list of rows; rewrite it (step 1.1)")
    unmeasured = _load(a / "unmeasured.json")
    for r in [*rows, *unmeasured.get("building", [])]:   # M2: cookr runs in the scripts folder
        if isinstance(r, dict) and r.get("file") and not Path(r["file"]).is_absolute():
            raise Refused(f"run_gaps.py: {r['file']} ({r.get('speciality')}) is a relative path, which cookr "
                          "would read from the scripts folder; write it absolute")
    wl = workspace / "worklist.json"
    worklist = _load(wl) if wl.is_file() else {}
    plan = plan_rows(a / "area-plan.md")
    survivor_of = {r["speciality"]: _folder(r["survivor"]) for r in unmeasured.get("against_survivor", [])}
    elsewhere_sp = {r["speciality"] for r in unmeasured.get("survivor_elsewhere", [])}
    wtopics = [t for b in worklist.get("batches", []) for t in b.get("topics", []) if t.get("survivor")]
    home_of = {_folder(t["new_home"]): _folder(t["survivor"]) for t in wtopics if t.get("new_home")}
    file_of = {r["speciality"]: r["file"] for r in rows if r.get("file") and r.get("topic")}
    prefix = f"cookbook/guidelines/{area}/"
    new_of = {}     # G53: speciality -> the new worklist topic of this area claiming it
    for t in wtopics:
        if t.get("new") and _folder(t["survivor"]).startswith(prefix) and isinstance(t.get("devteam"), list):
            for d in t["devteam"]:
                if isinstance(d, dict) and d.get("speciality"):
                    new_of.setdefault(d["speciality"], _folder(t["survivor"]).rsplit("/", 1)[-1])
    r9_targets = []

    def resolve(folder: str) -> tuple[str, str]:
        """(name, folder) for a topic folder named any way."""
        name = folder.rsplit("/", 1)[-1]
        if name in plan:
            return name, _folder(plan[name]["artifact"])
        if not (repo / folder).is_dir() and folder in home_of:
            return name, home_of[folder]
        return name, folder

    order: list[tuple[str, str]] = []
    against: dict[tuple[str, str], list[tuple[str, str]]] = {}
    missing = []

    def add(folder: str, speciality: str, file: str | None):
        key = resolve(folder)
        if not file:
            missing.append({"speciality": speciality, "why": f"no file for {key[1]}: write it with "
                            "speciality_reference.py <speciality> --out A/reference"})
            return
        if key not in against:
            order.append(key)
            against[key] = []
        if all(f != file for _, f in against[key]):
            against[key].append((speciality, file))

    for r in rows:
        if r.get("topic") and r.get("file") and r["speciality"] not in elsewhere_sp:
            folder = survivor_of.get(r["speciality"], _folder(r["topic"]))
            if r["speciality"] in new_of and not folder.startswith(prefix):
                # G53: a new topic's candidate survivor outside the area is its
                # R9 target (new-<name>.json), never an existing topic's gaps file
                name = new_of[r["speciality"]]
                r9_targets.append({"topic": name, "candidate": folder, "speciality": r["speciality"],
                                   "file": r["file"], "out": f"new-{name}.json"})
                continue
            add(folder, r["speciality"], r["file"])
    for t in wtopics:
        here = [_folder(t[k]) for k in ("survivor", "new_home") if t.get(k)]
        if not any(f.startswith(prefix) for f in here) or not isinstance(t.get("devteam"), list):
            continue
        for d in t["devteam"]:
            s = d.get("speciality") if isinstance(d, dict) else None
            if s in file_of and s not in elsewhere_sp and not any(x["speciality"] == s for x in r9_targets):
                add(_folder(t["survivor"]), s, file_of[s])
    for b in unmeasured.get("building", []):
        for v in b.get("via", []):
            add(_folder(v["topic"]), b["speciality"], b.get("file"))
        if not b.get("file") and not b.get("via"):
            missing.append({"speciality": b["speciality"], "why": "no file: write it with "
                            "speciality_reference.py <speciality> --out A/reference"})
    kind_of = {_folder(t["survivor"]): t.get("kind") for t in wtopics if t.get("new")}

    out = {"topics": {}, "measured_elsewhere": [], "unmeasurable": [], "missing_files": missing,
           "stale_reference": stale_reference(rows),      # R-I-1 (1.4.27)
           # 1.4.46: the files whose text opens with the speciality's own Review focus (a format-3
           # roled row's `copied` names it: its file starts at Build focus instead)
           "own_review_focus": sorted(r["file"] for r in rows if r.get("file")
                                      and "Review focus" not in (r.get("copied") or [])),
           "building": unmeasured.get("building", []), "marked_here": unmeasured.get("marked_here", []),
           "new_topics": _plan_names(plan, "new"), "r9_targets": r9_targets,
           "specialities": bool([r for r in rows if r.get("file")] or unmeasured.get("building")),
           "r9_owed": [n for n in _plan_names(plan, "new")
                       if kind_of.get(_folder(plan[n]["artifact"]), "shared-different") in R9_KINDS]}
    out["r9_owed"] += sorted({x["topic"] for x in r9_targets} - set(out["r9_owed"]))
    seen: dict[str, str] = {}
    for name, folder in order:
        sps = [s for s, _ in against[(name, folder)]]
        row = plan.get(name, {})
        if row.get("action") == "merged" and not folder.startswith(prefix):
            out["measured_elsewhere"].append({"topic": name, "folder": folder, "plan": _area_of(folder),
                                              "specialities": sps})
            continue
        if not (repo / folder).is_dir():
            out["unmeasurable"].append({"topic": name, "folder": folder, "specialities": sps})
            continue
        base = folder.rsplit("/", 1)[-1]
        if base in seen and seen[base] != folder:
            raise Clash(f"run_gaps.py: {seen[base]} and {folder} would both write {base}.json; "
                          "name the topics apart in the plan's Proposed topics")
        seen[base] = folder
        if base in out["topics"]:
            out["topics"][base]["against"] += [x for x in against[(name, folder)]
                                               if x not in out["topics"][base]["against"]]
        else:
            out["topics"][base] = {"topic": name, "folder": folder, "against": list(against[(name, folder)])}
    listed = {r["topic"] for r in out["measured_elsewhere"]}
    for name, row in plan.items():   # G46: every merged row elsewhere, whatever its speciality
        folder = _folder(row["artifact"])
        if row.get("action") == "merged" and not folder.startswith(prefix) and name not in listed:
            out["measured_elsewhere"].append({"topic": name, "folder": folder, "plan": _area_of(folder),
                                              "specialities": []})
    return out


def why_empty(m: dict, unmeasured_rows: list) -> str | None:
    """Why the area measures no topic (G46), or None when it measures one."""
    if m["topics"]:
        return None
    if not m["specialities"]:
        return "area has no speciality"
    why = [text for key, text in (
        ("measured_elsewhere", "every topic is merged into another area's plan (measured_elsewhere)"),
        ("survivor_elsewhere", "every speciality is measured against a survivor in another area "
                               "(survivor_elsewhere)"),
        ("unmeasurable", "its topics are new, with no folder to measure (unmeasurable)"),
        ("r9_targets", "its specialities are R9 targets of new topics (r9_targets)"),
        ("missing_files", "speciality files are missing (missing_files)"))
        if m.get(key) or (key == "survivor_elsewhere" and unmeasured_rows)]
    return "; ".join(why) or "no speciality of this area names a topic folder"


def ours(path: Path) -> bool:
    """Whether a gaps file is one run_gaps.py wrote: it says so (`written_by`,
    references empty or not: fix round 1, M6), or, written before that, every
    reference carries `lacking_numbers`, or (G110, 1.4.33) cookr wrote it
    before `lacking_numbers`: no `written_by`, a `folder`, and every reference
    cookr's own counts (`sentences`, `held`, `lacking`, `lacking_sentences`)
    with no `lacking_numbers`. A hand-built R9 `new-<name>.json` is never
    cleared, nor a hand file of any other shape."""
    if path.name.startswith("new-"):
        return False
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        refs = data.get("references")
    except (OSError, ValueError, AttributeError):
        return False
    if data.get("written_by") == WRITTEN_BY and isinstance(refs, list):
        return True
    if not (isinstance(refs, list) and refs and all(isinstance(r, dict) for r in refs)):
        return False
    if all("lacking_numbers" in r for r in refs):
        return True
    return ("written_by" not in data and isinstance(data.get("folder"), str) and all(
        "lacking_numbers" not in r and all(isinstance(r.get(k), int) for k in ("sentences", "held", "lacking"))
        and isinstance(r.get("lacking_sentences"), list) for r in refs))


HOME = "home--"     # a home file's prefix: no topic folder's basename starts with "-" (M1)
REPORT = "run_gaps.json"


def stale(out_dir: Path, topics) -> list[str]:
    """Gaps files in `out_dir` no topic of the set writes (R9 `new-*` kept;
    a `home--*` file is the run's own home measure, G68, handled after it;
    a saved report in a `--out` folder is no gaps file, M4)."""
    if not out_dir.is_dir():
        return []
    return sorted(p.name for p in out_dir.glob("*.json")
                  if p.stem not in topics and p.name != REPORT and not p.name.startswith(("new-", HOME)))


def _norm(text: str) -> str:
    return " ".join(re.sub(r"[^a-z0-9]+", " ", text.lower()).split())


def numbers(pieces: list[str], text: str) -> list[int | None]:
    """quote_building's number of the sentence holding each piece, in order.
    A piece is sought from the last hit on, then from the start; each hit uses
    up that text, so a piece the text repeats maps to each sentence in turn."""
    found = [f" {_norm(s)} " for s in sentences(text)]
    out, cursor = [], 0
    for piece in pieces:
        want = f" {_norm(piece)} "
        hit = next((i for i in range(cursor, len(found)) if want in found[i]), None)
        if hit is None:
            hit = next((i for i in range(len(found)) if want in found[i]), None)
        out.append(None if hit is None else hit + 1)
        if hit is not None:
            found[hit] = found[hit].replace(want, " | ", 1)
            cursor = hit
    return out


def could_hold(piece: str, found: list[str]) -> list[int]:
    """The number of every sentence of `found` that `piece` may belong to:
    each one its words overlap, wherever in the text they appear in order
    (across a sentence boundary too). [] when they appear nowhere."""
    want = _norm(piece).split()
    tokens = [(w, n) for n, s in enumerate(found, start=1) for w in _norm(s).split()]
    out: set[int] = set()
    for i in range(len(tokens) - len(want) + 1 if want else 0):
        if all(tokens[i + j][0] == w for j, w in enumerate(want)):
            out.update(n for _, n in tokens[i:i + len(want)])
    return sorted(out)


def _write_json(path: Path, data: dict) -> None:
    fd, tmp = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent)
    with os.fdopen(fd, "w", encoding="utf-8") as f:
        f.write(json.dumps(data, indent=2) + "\n")
    os.replace(tmp, path)


def cookr_pieces(file: str, cookr_py: str, cli: Path | None) -> list[list]:
    """Every piece cookr cuts `file` into, in order, as [piece, measured]:
    measured false for one it drops (under MIN_WORDS words). A piece with
    no words is left out. Raises ValueError when cookr cannot cut it."""
    env = dict(os.environ)
    if cli is not None:
        env["PYTHONPATH"] = str(cli)
    code = ("import json, sys; from cookr.core.gaps import MIN_WORDS, pieces; "
            "t = open(sys.argv[1], encoding='utf-8').read(); "
            "print(json.dumps([[p, len(n.split()) >= MIN_WORDS] for p, n in pieces(t)]))")
    # -P: never the working directory on the path (G44), and a fixed cwd too
    r = subprocess.run([cookr_py, "-P", "-c", code, file], capture_output=True, text=True, env=env,
                       cwd=HERE)
    if r.returncode != 0:
        raise ValueError(f"cookr could not cut {file}: {(r.stderr.strip().splitlines() or ['?'])[-1]}"
                         + python_hint(r.stderr, cookr_py))
    return json.loads(r.stdout)


def _measure(t: dict, target: Path, repo: Path, cookr_py: str, cli: Path | None,
             texts: dict) -> tuple[dict | None, str]:
    """Run one topic's command into a scratch file under write_on_success.py,
    number its lacking pieces, then put it in place at `target` in one
    atomic replace: (data, "") or (None, why)."""
    scratch = target.parent / f".{target.name}.run"
    command = [sys.executable, "-I", str(HERE / "write_on_success.py"), str(scratch.resolve()), "--"]
    if cli is not None:
        command.append(f"PYTHONPATH={cli}")
    command += [cookr_py, "-P", "-m", "cookr", "-p", str(repo), "roles", "gaps", t["folder"]]
    for _, f in t["against"]:
        command += ["--against", f]
    command.append("--json")
    try:
        r = subprocess.run(command, capture_output=True, text=True, cwd=HERE)
        if r.returncode != 0:
            return None, f"exited {r.returncode}:\n{r.stdout}{r.stderr}" + python_hint(r.stderr, cookr_py)
        data = _numbered(json.loads(scratch.read_text(encoding="utf-8")), texts)
        data["written_by"] = WRITTEN_BY     # M6: ours() clears it even with no references
        _write_json(target, data)
        return data, ""
    except (OSError, ValueError, KeyError, TypeError) as e:
        return None, f"{e.__class__.__name__}: {e}"
    finally:
        if scratch.exists():
            scratch.unlink()


def _numbered(data: dict, texts: dict) -> dict:
    for ref in data.get("references", []):
        f = ref["file"]
        if f not in texts:
            texts[f] = Path(f).read_text(encoding="utf-8")
        ref["lacking_numbers"] = numbers(ref.get("lacking_sentences", []), texts[f])
    return data


def _saved(target: Path, texts: dict) -> tuple[dict | None, str]:
    """The saved gaps file at `target`, numbered as a run numbers it (--check)."""
    if not target.is_file():
        return None, "no saved file"
    try:
        return _numbered(json.loads(target.read_text(encoding="utf-8")), texts), ""
    except (OSError, ValueError, KeyError, TypeError, AttributeError) as e:
        return None, f"{e.__class__.__name__}: {e}"


def _unreadable(result: dict, topic: str, folder: str, e: SystemExit) -> None:
    """I3 (fix round 1): a topic folder that cannot be read is a row in
    `unplaced` with its error, never silently left out."""
    if any(u["folder"] == folder for u in result["unplaced"]):
        return
    result["unplaced"].append({"topic": topic, "folder": folder, "why": str(e)})
    print(f"run_gaps.py: topic {topic} ({folder}) cannot be read, listed in unplaced: {e}", file=sys.stderr)


def _area_topics(area: str, repo: Path, m: dict, failed: list[str], result: dict) -> dict:
    """{topic: (words, sentences)} for every topic folder of the area (G50),
    named as the measurement set names it, else by its folder's basename; a
    folder that cannot be read goes to result's `unplaced`."""
    name_of = {t["folder"]: t["topic"] for t in m["topics"].values()}
    root = repo / "cookbook" / "guidelines" / area
    out = {}
    for d in sorted(root.iterdir()) if root.is_dir() else []:
        if not (d / "artifact.json").is_file():
            continue
        name = name_of.get(f"cookbook/guidelines/{area}/{d.name}", d.name)
        if name in failed:
            continue
        try:
            found = topic_sentences(d)
        except SystemExit as e:
            _unreadable(result, name, f"cookbook/guidelines/{area}/{d.name}", e)
            continue
        out[name] = (words(" ".join(t for _, t in found)), found)
    return out


def _hint(s: dict, text: str, topic_words: dict, area_words: dict) -> None:
    """paraphrase_hints' top 3 for a sentence held at no measured topic (one
    with a piece not measured never is): at its home_guess, a measured topic
    or any topic folder of the area (G66), else over every measured topic
    (Minor 1, 1.4.20)."""
    at = [s["home_guess"]] if s["home_guess"] else list(topic_words)
    pool = {**area_words, **topic_words}
    found = [{"topic": t, **h} for t in at for h in rank(text, pool[t][1], 3)]
    s["hints"] = sorted(found, key=lambda h: -h["score"])[:3]
    s["hints_at"] = s["home_guess"] or "every measured topic"


def _advise(result: dict, speciality: str, n: int, part: str, do) -> None:
    """Run one advisory part; a failure is listed in `advisory_failed` and
    named on stderr, and the run goes on (G66, G82): it never stops the run
    after its writes, and never changes the exit."""
    try:
        do()
    except Exception as e:  # noqa: BLE001 - advisory: any failure is recorded, never raised
        why = f"{e.__class__.__name__}: {e}"
        result["advisory_failed"].append({"part": part, "speciality": speciality, "n": n, "why": why})
        print(f"run_gaps.py: {part} for {speciality} sentence {n} failed, listed in advisory_failed: {why}",
              file=sys.stderr)


def run(area: str, workspace: Path, repo: Path, out_dir: Path, cookr_py: str, cli: Path | None,
        hints: bool = False, mode: str = "write", scratch: Path | None = None,
        devteam: Path | None = None) -> tuple[dict, int]:
    """mode "write" measures into `out_dir`, first clearing the stale files it
    wrote there itself; "fresh" measures into `scratch`, touching nothing in
    `out_dir`; "saved" reads `out_dir`'s files instead of measuring (G45)."""
    m = measures(area, workspace, repo)
    a = workspace / "areas" / area
    unmeasured_rows = _load(a / "unmeasured.json").get("survivor_elsewhere", [])
    clear = [n for n in stale(out_dir, m["topics"]) if ours(out_dir / n)]
    if mode == "write":
        out_dir.mkdir(parents=True, exist_ok=True)
        for n in clear:
            (out_dir / n).unlink()
    result = {"area": area, "out": str(out_dir), "note": note(),
              "reference_format": REFERENCE_FORMAT,      # N3-I-1 (1.4.29): what this report was measured under
              "skill_version": skill_version(),          # gapfix13 (G269): stage_status says when to refresh it
              "why_empty": why_empty(m, unmeasured_rows),
              "topics": [], "building": [], "same_text": [],
              "measured_elsewhere": m["measured_elsewhere"], "unmeasurable": m["unmeasurable"],
              "missing_files": m["missing_files"], "stale_reference": list(m["stale_reference"]),
              "hints": hints,
              **({"cleared": clear} if mode == "write" else {"would_clear": clear}),
              "stale_gaps": [n for n in stale(out_dir, m["topics"]) if n not in clear],
              "r9_targets": m["r9_targets"],
              "r9_missing": [n for n in m["r9_owed"] if not (out_dir / f"new-{n}.json").is_file()],
              "r9_stale": r9_stale(out_dir, repo),  # G94 (1.4.33), 1.4.34: R9 files not measured on their inputs as they are
              "failed": [], "unplaced": [], "short_sentences": [], "markers": [], "repeat_of": [], "held_by_wording": [],
              "home_measures": [], "home_unguessed": [], "numbering_differs": [], "advisory_failed": [],
              "lacking_pieces": []}
    same: dict[str, dict] = {}                     # G51: normalised lacking text -> its group
    texts: dict[str, str] = {}
    lacking: dict[str, dict[str, set[int]]] = {}   # file -> topic -> numbers
    lost: dict[str, dict[str, list[str]]] = {}     # file -> topic -> lacking pieces with no number
    listed: dict[str, dict[str, set[str]]] = {}    # file -> topic -> every lacking piece, normalised
    lacking_rows: list[tuple] = []                 # 1.4.40 (G225): (speciality, file, topic, piece, n), every lacking piece
    for base, t in m["topics"].items():
        target = out_dir / f"{base}.json"
        if mode == "saved":
            data, why = _saved(target, texts)
        else:
            data, why = _measure(t, (scratch if mode == "fresh" else out_dir) / f"{base}.json",
                                 repo, cookr_py, cli, texts)
        if data is None:
            print(f"run_gaps.py: {t['topic']} ({t['folder']}) failed, its previous file kept: {why}",
                  file=sys.stderr)
            result["failed"].append({"topic": t["topic"], "why": why.splitlines()[0]})
            continue
        speciality = {f: s for s, f in t["against"]}
        row = {"topic": t["topic"], "folder": t["folder"], "gaps_file": target.name,
               "pieces": 0, "held": 0, "lacking": 0, "unplaced": 0, "references": [],
               "lacking_by_home_guess": []}
        for ref in data.get("references", []):
            f = ref["file"]
            # 1.4.22 Minor 2: a lacking piece with no number is kept apart,
            # never dropped: it goes to the building entry's `unplaced_pieces`.
            numbered = list(zip(ref.get("lacking_sentences", []), ref["lacking_numbers"]))
            lacking.setdefault(f, {})[t["topic"]] = {n for _, n in numbered if n is not None}
            lost.setdefault(f, {})[t["topic"]] = [piece for piece, n in numbered if n is None]
            listed.setdefault(f, {})[t["topic"]] = {_norm(piece) for piece, _ in numbered}
            lacking_rows += [(speciality.get(f) or f, f, t["topic"], piece, n) for piece, n in numbered]
            row["references"].append({"speciality": speciality.get(f), "file": f, "pieces": ref["sentences"],
                                       "held": ref["held"], "lacking": ref["lacking"],
                                       "lacking_numbers": ref["lacking_numbers"],
                                       "unplaced": len(lost[f][t["topic"]])})
            for k in ("pieces", "held", "lacking"):
                row[k] += ref["sentences" if k == "pieces" else k]
            row["unplaced"] += len(lost[f][t["topic"]])
            for piece in ref.get("lacking_sentences", []):
                g = same.setdefault(_norm(piece), {"text": piece, "specialities": set(), "topics": set()})
                g["specialities"].add(speciality.get(f) or f)
                g["topics"].add(t["topic"])
        result["topics"].append(row)
    result["same_text"] = [{"text": g["text"], "specialities": sorted(g["specialities"]),
                            "topics": sorted(g["topics"])}
                           for _, g in sorted(same.items()) if len(g["specialities"]) > 1]
    if result["r9_missing"]:
        print("run_gaps.py: no R9 file for new topic(s) " + ", ".join(result["r9_missing"]) +
              ": run each R9 command by hand (stage-1.md, R9)",
              file=sys.stderr)
    for r in result["r9_stale"] if mode != "saved" else []:     # G140: --check reads saved then fresh: once
        print(f"run_gaps.py: r9_stale {r['file']} ({r['reference']}): {r['why']}", file=sys.stderr)
    failed = [x["topic"] for x in result["failed"]]
    topic_words = {}
    for t in m["topics"].values():
        if t["topic"] in failed:
            continue          # Nit 1, 1.4.21: a failed topic is not measured, never hinted
        try:
            found = topic_sentences(repo / t["folder"])
        except SystemExit as e:
            found = []
            _unreadable(result, t["topic"], t["folder"], e)
        topic_words[t["topic"]] = (words(" ".join(s for _, s in found)), found)
    area_words = _area_topics(area, repo, m, failed, result)
    pieces_of: dict[str, tuple[list[int], dict[int, object]]] = {}   # G52: file -> (kept numbers, marks)
    cuts: dict[str, list[list]] = {}                                   # file -> cookr's pieces
    for b in m["building"]:
        f = b.get("file")
        if not f:
            continue          # listed in missing_files, with or without a `via`
        marks_file = a / f"building-{b['speciality'].split('/', 1)[-1]}.json"
        marks = _load(marks_file).get("marks", {}) if marks_file.is_file() else {}
        here = {x["n"] for x in m["marked_here"] if x.get("speciality") == b["speciality"]}
        at = lacking.get(f, {})   # no measured topic: none of its text is measured
        try:
            if f not in texts:
                texts[f] = Path(f).read_text(encoding="utf-8")
            pieces = _cut(f, cuts, cookr_py, cli) if at else []
        except (OSError, ValueError) as e:
            result["failed"].append({"speciality": b["speciality"], "why": str(e).splitlines()[0]})
            continue
        found = sentences(texts[f])
        measured, dropped = set(), {}       # sentence numbers; number -> pieces cookr drops
        unplaced, adrift = [], {}           # `unplaced_pieces`; number -> pieces it may hold

        def unplace(piece: str, kept: bool, verdict: str | None, topic: str | None) -> None:
            """List a piece no one sentence holds, and name it at each sentence
            it could belong to: none of them reads as held because of it."""
            row = {"text": piece, "measured": kept, "verdict": verdict, "topic": topic,
                   "sentences": could_hold(piece, found)}
            same = [u for u in unplaced if _norm(u["text"]) == _norm(piece) and u["topic"] == topic]
            if not same:
                unplaced.append(row)
            for k in row["sentences"]:
                if all(_norm(x) != _norm(piece) for x in adrift.setdefault(k, [])):
                    adrift[k].append(piece)

        for (piece, kept), n in zip(pieces, numbers([p for p, _ in pieces], texts[f])):
            if n is not None and kept:
                measured.add(n)
            elif n is not None:
                dropped.setdefault(n, []).append(piece)
            elif not kept:
                unplace(piece, False, None, None)    # Nit 3, 1.4.21: judged by hand, never ignored
            else:                                     # Minor 2, 1.4.22: a measured piece, with its verdicts
                for t in at:  # 1.4.23: lacking wherever cookr listed it lacking, numbered there or not
                    unplace(piece, True, "lacking" if _norm(piece) in listed[f][t] else "held", t)
        for t in at:      # a lacking piece numbered in neither pass above is still never dropped
            for piece in lost[f][t]:
                unplace(piece, True, "lacking", t)
        entry = {"speciality": b["speciality"], "file": f, "measured_at": list(at), "sentences": [], "gap_candidates": [],
                 "unmeasured_sentences": [], "other_area": [], "unmarked": [], "unplaced_pieces": unplaced}
        if failed:
            entry["partial"] = failed
        kept_numbers = [n for (piece, kept), n in zip(pieces, numbers([p for p, _ in pieces], texts[f]))
                        if kept and n is not None]
        pieces_of[f] = (kept_numbers, {})
        for n, text in enumerate(found, start=1):
            mark = marks.get(str(n)) or (area if n in here else None)
            pieces_of[f][1][n] = mark
            s = {"n": n, "mark": mark, "measured": n in measured and n not in dropped and n not in adrift}
            if n in dropped:
                s["unmeasured_parts"] = dropped[n]
            if n in adrift:
                s["unplaced_parts"] = adrift[n]
            s.update({"home_guess": None, "held_at": [], "lacking_at": []})
            entry["sentences"].append(s)
            mine = area in areas_of(mark)
            if not areas_of(mark):
                entry["unmarked"].append(n)
            elif not mine:
                entry["other_area"].append(n)
            if not s["measured"]:     # G48: every one, whatever its mark, saying whose it is
                entry["unmeasured_sentences"].append({"n": n, "marked_for": mark})
            if n not in measured:     # no piece measured: no verdict to keep
                _candidates(s, text, area_words)
                if hints:
                    _advise(result, b["speciality"], n, "hints",
                            lambda s=s, text=text: _hint(s, text, topic_words, area_words))
                continue
            verdict = {"held_at": [t for t in at if n not in at[t]], "lacking_at": [t for t in at if n in at[t]]}
            if s["measured"]:
                s.update(verdict)
            else:
                # Minor 1, 1.4.21 and 1.4.22: a sentence measured in part keeps
                # its measured pieces' verdicts, but apart: its own `held_at`
                # stays [], so it never reads as held, and is no gap candidate.
                s["measured_pieces"] = verdict
                s["by_hand"] = BY_HAND
            want = words(text)

            def overlap(t: str) -> float:
                return len(want & topic_words[t][0]) / len(want) if want else 0.0
            pool = sorted(verdict["held_at"] or verdict["lacking_at"], key=overlap, reverse=True)
            tie = len(pool) > 1 and overlap(pool[0]) == overlap(pool[1])
            if not tie and (verdict["held_at"] or overlap(pool[0]) >= HOME_SHARE):
                s["home_guess"] = pool[0]
                s["home_shared_words"] = sorted(want & topic_words[pool[0]][0])     # G121
            if not s["held_at"]:
                _candidates(s, text, area_words)
            if mine and not s["held_at"] and s["measured"]:
                entry["gap_candidates"].append(n)
            if hints and not s["held_at"]:
                _advise(result, b["speciality"], n, "hints",
                        lambda s=s, text=text: _hint(s, text, topic_words, area_words))
            for row in result["topics"]:
                if row["topic"] in verdict["lacking_at"]:
                    row["lacking_by_home_guess"].append({"speciality": b["speciality"], "n": n,
                                                         "home_guess": s["home_guess"],
                                                         **({} if s["measured"] else {"measured": False})})
        result["building"].append(entry)
    _split(result["topics"], pieces_of, area)
    result["lacking_pieces"] = _lacking_rows(lacking_rows, pieces_of, area)
    extra = _home_measures(area, a, repo, m, result, out_dir, (cookr_py, cli), mode, scratch, devteam,
                           (texts, cuts), area_words)
    result["short_sentences"], result["markers"] = _short(m, extra, result, texts, cuts, cookr_py, cli)
    result["repeat_of"] = _repeats(result["topics"], texts, set(m.get("own_review_focus", [])))
    result["held_by_wording"] = _held(m, result, listed, (texts, cuts), topic_words, (cookr_py, cli)) + \
        result["held_by_wording"]
    _resolve_marks(result, workspace, m, texts)
    _tag_unguessed(result, a)
    _held_rule(result, {**area_words, **topic_words}, texts, recorded_homes(a))
    _held_verdicts(result, a)
    _short_ids(result)
    result["short_not_owed"] = short_not_owed(result)      # gapfix13b (platform-integration#5)
    _lacking_verdicts(result, a)
    result["hand_holds"] = hand_holds(a)      # gapfix14 (1.4.43, G276)
    _home_rows(result, recorded_homes(a))      # gapfix13 (1.4.42): G253, G254
    result["r9_lacking"] = _r9_rows(out_dir)
    _hand_rows(result, a)
    r9_once(result)      # gapfix14 (G281a): after _hand_rows, so the R9 rows carry their verdicts
    _judge_new_rows(result, a)
    result["non_home_lacking"] = non_home_lacking(result, recorded_homes(a))
    result["topic_totals"] = topic_totals(result)
    result["measured_total"] = measured_total(result)
    result["missing_subjects"] = missing_subjects(a / "area-plan.md")      # gapfix14 (G286): beside, never inside
    result["stale_home"] = stale_homes(workspace, area, repo)      # G205 (1.4.39): listed, never dropped
    for r in result["stale_home"] if mode != "saved" else []:      # --check reads saved then fresh: once
        print(f"run_gaps.py: stale_home {r['file']} {r['speciality']} {r['n']}={r['home']}: {r['why']}",
              file=sys.stderr)
    return result, (2 if result["failed"] or result["unplaced"] else 0)   # N-A: an unplaced topic stops it


def _cut(f: str, cuts: dict, cookr_py: str, cli: Path | None) -> list[list]:
    """cookr_pieces, each file cut once per run."""
    if f not in cuts:
        cuts[f] = cookr_pieces(f, cookr_py, cli)
    return cuts[f]


def _short(m: dict, extra: list, result: dict, texts: dict, cuts: dict, cookr_py: str,
           cli: Path | None) -> tuple[list[dict], list[dict]]:
    """G72: every piece cookr leaves out of the measure (under six words), of
    every speciality's file, direct, building, R9 or home-measured, measured
    at a topic or not: [{"speciality", "n", "text", "marked_for", "topic",
    "fragment", "kind"}], each judged by hand. `n` is quote_building's
    sentence number (null when no one sentence holds it). G101 (1.4.33):
    `marked_for` is the sentence's mark (a building or `marked_here`
    speciality; null unmarked), this area for a direct or R9 speciality;
    `topic` the topic it is measured at, the first when several (all in
    `topics`); a building sentence's is its home_guess, `topics` the topics
    it was measured at. G102, G103:
    `fragment` and `kind` from `piece_kind` (advisory: never dropped). A piece
    that is only a list marker goes to the second list (`markers`), never
    dropped silently. A file cookr cannot cut is listed in `failed` under its speciality."""
    area = result["area"]
    topics_of: dict[tuple, list[str]] = {}
    for t in m["topics"].values():
        for sp, f in t["against"]:
            topics_of.setdefault((sp, f), []).append(t["topic"])
    for r in m["r9_targets"]:
        topics_of.setdefault((r["speciality"], r["file"]), []).append(r["topic"])
    marks: dict[tuple, dict[int, object]] = {}          # (speciality, file) -> n -> mark, home guess
    guesses: dict[tuple, dict[int, object]] = {}
    for b in result["building"]:
        marks[(b["speciality"], b["file"])] = {x["n"]: x["mark"] for x in b["sentences"]}
        guesses[(b["speciality"], b["file"])] = {x["n"]: x["home_guess"] for x in b["sentences"]}
    here = {(x.get("speciality"), x.get("n")) for x in m["marked_here"] if isinstance(x, dict)}
    files = [x for t in m["topics"].values() for x in t["against"]]
    files += [(b["speciality"], b["file"]) for b in m["building"] if b.get("file")]
    files += [(r["speciality"], r["file"]) for r in m["r9_targets"]] + extra
    building = {b["speciality"] for b in m["building"]} | {sp for sp, _ in extra}
    rows, markers, seen = [], [], set()
    for sp, f in files:
        if (sp, f) in seen:
            continue
        seen.add((sp, f))
        try:
            pieces = _cut(f, cuts, cookr_py, cli)
            if f not in texts:
                texts[f] = Path(f).read_text(encoding="utf-8")
        except (OSError, ValueError) as e:
            if not any(x.get("speciality") == sp for x in result["failed"]):
                result["failed"].append({"speciality": sp, "why": str(e).splitlines()[0]})
            continue
        prev = ""
        for (piece, kept), n in zip(pieces, numbers([p for p, _ in pieces], texts[f])):
            after_vs, prev = prev.rstrip().lower().endswith(("vs.", " vs")), piece
            if kept:
                continue
            kind = piece_kind(piece, after_vs)
            if kind == "marker":
                row = {"speciality": sp, "n": n, "text": piece}
                if row not in markers:
                    markers.append(row)
                continue
            at = sorted(set(topics_of.get((sp, f), [])))
            if sp in building:      # a building sentence's topic is its home guess, never a topic it was measured at
                mark = marks.get((sp, f), {}).get(n) or (area if (sp, n) in here else None)
                topic = guesses.get((sp, f), {}).get(n)
            else:
                mark, topic = area, (at[0] if at else None)
            row = {"speciality": sp, "n": n, "text": piece, "marked_for": mark, "topic": topic,
                   **({"topics": at} if len(at) > 1 else {}),
                   "fragment": fragment(piece, after_vs), "kind": kind}
            if not any((r["speciality"], r["n"], r["text"]) == (sp, n, piece) for r in rows):
                rows.append(row)
    key = lambda r: (r["speciality"], r["n"] is None, r["n"] or 0, r["text"])      # noqa: E731
    return sorted(rows, key=key), sorted(markers, key=key)


def _numerals(text: str) -> set[str]:
    return set(re.findall(r"\d+(?:[.,]\d+)?", text))


def _held(m: dict, result: dict, listed: dict, cache: tuple, topic_words: dict, cookr: tuple) -> list[dict]:
    """G132 (1.4.36): every piece cookr holds at a measured topic, which rests
    on wording alone (G118 asks the plan to re-judge each): [{"speciality",
    "n", "text", "topic", "marked_for", "number_differs"}], `number_differs`
    True when the piece holds a numeral the topic's text never says ("5+
    files" vs "more than 5 files" is not flagged; "30" vs "60" is). A piece
    held at its home (`home_measures`) is listed the same way. Never filtered."""
    texts, cuts = cache
    area = result["area"]
    sp_of: dict[str, str] = {}
    for t in m["topics"].values():
        for sp, f in t["against"]:
            sp_of.setdefault(f, sp)
    building = {b["speciality"] for b in m["building"]}
    for b in m["building"]:
        if b.get("file"):
            sp_of[b["file"]] = b["speciality"]
    marks = {b["speciality"]: {x["n"]: x["mark"] for x in b["sentences"]} for b in result["building"]}
    here = {(x.get("speciality"), x.get("n")) for x in m["marked_here"] if isinstance(x, dict)}
    rows = []
    for f, by_topic in sorted(listed.items()):
        try:
            pieces = _cut(f, cuts, *cookr)
            if f not in texts:
                texts[f] = Path(f).read_text(encoding="utf-8")
        except (OSError, ValueError):
            continue          # listed in `failed` by `_short`
        sp = sp_of.get(f) or f
        numbered = list(zip(pieces, numbers([p for p, _ in pieces], texts[f])))
        for t, lack in sorted(by_topic.items()):
            said = _numerals(" ".join(x for _, x in topic_words.get(t, (None, []))[1]))
            for (piece, kept), n in numbered:
                if not kept or _norm(piece) in lack:
                    continue
                mark = (marks.get(sp, {}).get(n) or (area if (sp, n) in here else None)) if sp in building else area
                row = {"speciality": sp, "n": n, "text": piece, "topic": t, "marked_for": mark,
                       "number_differs": bool(_numerals(piece) - said),
                       "topic_sentence": _nearest(piece, topic_words.get(t, (None, []))[1])}
                if row not in rows:
                    rows.append(row)
    return rows


def _nearest(piece: str, found: list) -> str | None:
    """G159 (1.4.37): the topic sentence sharing most of the piece's words (paraphrase_hints.rank), or None."""
    best = nearest_rank(piece, list(found), 1)
    return best[0]["text"] if best else None


HELD = "held.json"

# G200/G201 (1.4.39): RFC 2119 strength, multi-word forms first (MUST NOT before MUST).
MODALS = (("MUST NOT", 3), ("SHALL NOT", 3), ("DO NOT", 3), ("SHOULD NOT", 2), ("MUST", 3), ("SHALL", 3),
          ("REQUIRED", 3), ("NEVER", 3), ("ALWAYS", 3), ("SHOULD", 2), ("RECOMMENDED", 2), ("PREFER", 2),
          ("AVOID", 2), ("MAY", 1), ("OPTIONAL", 1), ("CONSIDER", 1),
          # gapfix13 (G260, 1.4.42): the word forms a topic writes a rule in.
          ("PREFERRED", 2), ("PREFERABLY", 2), ("OPTIONALLY", 1))
_MODAL = re.compile(r"\b(" + "|".join(w.replace(" ", r"\s+") for w, _ in MODALS) + r")\b", re.I)
_RANK = dict(MODALS)

# G224 (1.4.40): a checklist row's Severity cell is its modal.
SEVERITY = (("FAIL", "MUST"), ("WARN", "SHOULD"), ("INFO", "MAY"))
_SEVERITY = dict(SEVERITY)
_SEP_CELL = re.compile(r":?-{3,}:?$")

# G249 (1.4.40): a sentence that opens with one of these is an imperative: with no modal word it reads as a MUST.
IMPERATIVES = frozenset(
    "add allow apply ask assert assign avoid back bind build cache call capture catch check choose clean clear close "
    "collect compare compute configure confirm connect consider construct convert copy count create declare define "
    "delete deny derive describe design detect disable document drop enable encode ensure enumerate escape evaluate "
    "exclude execute expose extract fail fetch filter fix follow generate give group guard handle hash hide "
    "identify ignore implement import include initialize inject inspect install isolate keep label limit list load "
    "lock log make map mark measure merge mock move name normalize note omit open order override pass pin place "
    "plan prefer prevent print probe produce prove provide publish put read record redact refuse register reject "
    "release remove render replace report represent require reserve reset resolve restrict retry return reuse "
    "review revoke run sanitize save scope seed select send separate serialize set show sign split stop store "
    "stub supply tag take target test throw track treat trim trust try update use validate verify version wait "
    "warn wrap write "
    # gapfix13 (G260, 1.4.42)
    "respect honor honour favor favour support emit"
    # gapfix14 (G279, 1.4.43)
    " quote cite".split())


def table_rows(text: str | None) -> list[str] | None:
    """G224 (1.4.40): the rows (`| a | b |`) of a markdown table `quote_building.sentences` kept as one sentence
    (header first, then each data row; no separator row), one row when the text is a single row, None when it is
    not a table. The sentence numbering never changes: only the rule reads a row."""
    t = (text or "").strip()
    if not (len(t) > 2 and t.startswith("|") and t.endswith("|")):
        return None
    toks = [c.strip() for c in t[1:-1].split("|")]
    sep = [i for i, c in enumerate(toks) if _SEP_CELL.match(c)]
    if not sep:
        return [t]
    start = sep[0]
    n = 0
    while start + n < len(toks) and _SEP_CELL.match(toks[start + n]):
        n += 1
    head_end = start - 1 if start >= 1 and toks[start - 1] == "" else start
    rows = [toks[max(head_end - n, 0):head_end]]
    pos = start + n
    if pos < len(toks) and toks[pos] == "":
        pos += 1
    while pos < len(toks):
        rows.append(toks[pos:pos + n])
        pos += n
        if pos < len(toks) and toks[pos] == "":
            pos += 1
    return ["| " + " | ".join(r) + " |" for r in rows]


# gapfix14 (G275, 1.4.43): a lowercase modal word is the rule's only when it is not inside a code span, a quote or
# a parenthesis, not in a relative clause ("identifiers that should have been updated"), not epistemic ("may have
# bypassed"), and a lowercase "avoid" past the opener negates its clause under the sentence's own modal. A negated
# lowercase modal ("no path ... may point", "may not", "must never") is MUST NOT.
_RELATIVE = re.compile(r"\b(?:that|which|who|whom|whose|where)\s*$", re.I)
_PERFECT = re.compile(r"\s+(?:not\s+)?have\b", re.I)
_NEGATED = re.compile(r"\b(?:no|none|nothing|neither|nor)\b[^.;:!?()]{0,80}$", re.I)
_SPANS = re.compile("`[^`]*`|\\([^()]*\\)|\"[^\"]*\"|\u201c[^\u201d]*\u201d")


def _shielded(text: str) -> list[tuple[int, int]]:
    return [m.span() for m in _SPANS.finditer(text)]


def _mentioned(text: str) -> set[int]:
    """gapfix14 (G279): the starts of modal words listed three or more in a row ("MUST, MUST NOT, ... MAY, or
    OPTIONAL"): a list naming the keywords mentions them and uses none."""
    ms = list(_MODAL.finditer(text))
    out: set[int] = set()
    run = ms[:1]
    for prev, m in zip(ms, ms[1:]):
        if re.fullmatch(r"[\s,;/`*]*(?:(?:or|and)[\s`*]*)?", text[prev.end():m.start()], re.I):
            run.append(m)
            continue
        if len(run) >= 3:
            out |= {x.start() for x in run}
        run = [m]
    if len(run) >= 3:
        out |= {x.start() for x in run}
    return out


def _word_modals(text: str) -> list[tuple[str, int]]:
    out = []
    spans = _shielded(text)
    opener = _opener(text)
    listed = _mentioned(text)
    for m in _MODAL.finditer(text):
        if m.start() in listed:
            continue
        raw = m.group(1)
        w = " ".join(raw.upper().split())
        if raw != raw.upper():                      # a lowercase word: the rule's only in the main clause
            if any(a <= m.start() < b for a, b in spans):
                continue
            before, after = text[:m.start()], text[m.end():]
            if _RELATIVE.search(before) or (w in ("MAY", "MUST", "SHOULD") and _PERFECT.match(after)):
                continue
            if w in ("REQUIRED", "OPTIONAL", "RECOMMENDED", "PREFERRED") and re.match(
                    r"\s+(?!(?:to|by|for|when|if|that|in|unless|and|or|but|on|at|only|where)\b)[A-Za-z]", after):
                continue          # gapfix14 (G279): "All required sections", "an optional field": an adjective
            if w == "AVOID" and not (opener == "avoid" and before.strip(" \t|>*_`-+.)(").strip() == ""):
                continue
            if w == "MAY" and (re.match(r"\s+not\b", after, re.I) or _NEGATED.search(before)):
                w = "MUST NOT"
            elif w in ("MUST", "SHOULD") and re.match(r"\s+never\b", after, re.I):
                w = w + " NOT"
        out.append((w, _RANK[w]))
    return out


def modals(text: str | None) -> list[tuple[str, int]]:
    """G227 (1.4.40): every RFC 2119 word of `text`, in order, with its rank; a table row with a Severity cell
    (FAIL, WARN, INFO) gives that cell's modal instead of its words (G224)."""
    rows = table_rows(text)
    if rows is None:
        return _word_modals(text or "")
    out: list[tuple[str, int]] = []
    for r in rows:
        cells = [c.strip(" *`").upper() for c in r.strip("|").split("|")]
        sev = [_SEVERITY[c] for c in cells if c in _SEVERITY]
        out += [(w, _RANK[w]) for w in sev] if sev else _word_modals(r)
    return out


def modal(text: str | None) -> tuple[str | None, int | None]:
    """G200 (1.4.39): the strongest RFC 2119 word `text` holds, case-folded,
    with its rank (3 MUST/SHALL/REQUIRED/NEVER/ALWAYS/DO NOT, 2 SHOULD/
    RECOMMENDED/PREFER/AVOID, 1 MAY/OPTIONAL/CONSIDER); (None, None) when none.
    A checklist row reads its Severity cell (G224, 1.4.40)."""
    best: tuple[str | None, int | None] = (None, None)
    for w, r in modals(text):
        if best[1] is None or r > best[1]:
            best = (w, r)
    return best


def modal_weakest(text: str | None) -> tuple[str | None, int | None]:
    """G227 (1.4.40): the weakest modal word of `text` (the topic side reads its weakest)."""
    best: tuple[str | None, int | None] = (None, None)
    for w, r in modals(text):
        if best[1] is None or r < best[1]:
            best = (w, r)
    return best


def _opener(text: str) -> str:
    m = re.match(r"[\s|>*_`\-+\d.)(\[]*([A-Za-z]+)", text or "")
    return m.group(1).lower() if m else ""


_SUBJECT = re.compile(r"[\s|>*_`\-+\d.)(\[]*[A-Za-z]+(?:\s+[A-Za-z-]+)?\s+(?:is|are|was|were|has|have|had|does|"
                      r"can|will|would)\b", re.I)


def imperative(text: str | None) -> bool:
    """G249 (1.4.40): the sentence opens with a verb of IMPERATIVES (a list item's marker and markup skipped).
    gapfix14 (G279, 1.4.43): not when that word is a subject ("Version control is the history.")."""
    return _opener(text or "") in IMPERATIVES and not _SUBJECT.match(text or "")


def no_finite_verb(text: str | None) -> bool:
    """G249 (1.4.40): no finite verb, for this rule: not a table row and no sentence end (`.`, `!`, `?`): a
    heading, a label or a bullet's fragment."""
    t = (text or "").strip()
    return bool(t) and table_rows(t) is None and not re.search(r"[.!?][\s*_`\"')\]]*$", t)


def _stem(w: str) -> str:
    for suf in ("ing", "ed", "es", "s"):
        if len(w) > len(suf) + 3 and w.endswith(suf) and not w.endswith("ss"):
            return w[:-len(suf)] if suf != "es" or w[-3] in "sxz" or w.endswith(("ches", "shes")) else w[:-1]
    return w


def _stems(text: str) -> set[str]:
    from paraphrase_hints import words
    return {_stem(w) for w in words(text)}


def _row_id(row: str, k: int) -> str:
    first = row.strip("|").split("|")[0].strip(" *`")
    return first if re.fullmatch(r"[A-Z]{1,4}-?\d{1,3}", first) else f"{k}"


def _rule_candidates(found: list) -> list[dict]:
    """gapfix13 (G260, 1.4.42): each topic sentence, a multi-row table as its data rows, with where it is:
    `<part> sentence N` (N counted within the part) and ` row <id>` for a row (its ID cell, else its number)."""
    out, seen = [], {}
    for part, text in found:
        seen[part] = seen.get(part, 0) + 1
        at = f"{part} sentence {seen[part]}"
        rows = table_rows(text)
        if rows and len(rows) > 1:
            out += [{"text": r, "at": f"{at} row {_row_id(r, k)}", "sentence": text}
                    for k, r in enumerate(rows[1:], start=1)]
        else:
            out.append({"text": text, "at": at, "sentence": text})
    return out


def _score(want: set[str], text: str) -> float:
    return len(want & _stems(text)) / len(want) if want else 0.0


NEAR_TIE = 0.85      # gapfix13 (G260): a candidate holding 85% of the best's share of the piece's words ties it
SCOPE_SHARE = 1 / 3  # gapfix13 (G260): a fragment's scope sentence holds at least a third of the fragment's share


_CODE = re.compile(r"\s*(```|~~~)")
_CHECKBOX = re.compile(r"\s*[-*+]\s*\[[ xX]\]\s")
_LABEL = re.compile(r"[\s>\-+\d.)]*\*\*(?P<label>[^*]+?)\*\*\s*(?:\u2014|\u2013|--|:)\s*(?P<body>.+)$")
_LABEL_IN = re.compile(r"[\s>\-+\d.)]*\*\*(?P<label>[^*\u2014\u2013]+?)\s*(?:\u2014|\u2013|--)\s*(?P<body>[^*]+?):?"
                       r"\*\*\s*:?\s*$")
FALL_SHARE = 1 / 2   # gapfix14 (G279): a prose sentence holding half a code block's share is the rule over it


def labelled(text: str | None) -> str | None:
    """gapfix14 (G279, 1.4.43): the body of a labelled item ("**Specific** -- a failure points to one cause",
    "**Naming -- use descriptive names:**"), else None. A labelled item is its own rule: it never takes a sibling
    item's modal, and an imperative body reads as a MUST."""
    m = _LABEL.match(text or "") or _LABEL_IN.match(text or "")
    return m.group("body").strip() if m else None


def _rule_core(piece: str) -> str:
    """gapfix14 (G279, 1.4.43): the piece without its parentheticals and a trailing `since`/`because` reason: the
    reason ("version control is the history") is never what picks the rule."""
    core = re.sub(r"\([^()]*\)", " ", piece)
    core = re.split(r",?\s+\b(?:since|because)\b", core)[0]
    return core if _stems(core) else piece


def _weight(want: set[str], text: str) -> int:
    """gapfix14 (G279): the letters of the piece's stems `text` holds: of candidates holding as many words, the
    one sharing the piece's longer (rarer) words ("commented-out code" over "leave ... behind") holds it."""
    return sum(len(w) for w in want & _stems(text))


def rule_pick(piece: str, found: list) -> dict:
    """G227 (1.4.40): the topic sentence holding the piece is the rule: `rule_sentence`, the row of a table
    holding it, never a neighbour. `nearest_modal_sentence` names the neighbour G202 chose; a sentence opening
    with a verb and holding no modal word reads as a MUST (`implied`).
    gapfix13 (G260, 1.4.42): the rule is ranked over every sentence and every row of every table of the topic,
    on the piece's word stems (so "imports" meets "import"); of candidates holding nearly as many of the piece's
    words as the best (NEAR_TIE), the strongest modal is the rule (a piece any rule states at its strength is
    held there), then the shortest. `rule_at` names it (`<part> sentence N[ row <id>]`). A fragment holding no
    modal (a heading, a label) is judged against the nearest modal candidate only when that one holds at least
    SCOPE_SHARE of the fragment's share of the piece's words; a code block never is. Otherwise the fragment is
    the rule and no modal is read from an unrelated row.
    gapfix14 (G279, 1.4.43): the piece is ranked without its parenthetical or `since` reason; a code block is the
    rule only when no prose sentence holds FALL_SHARE of its share; ties go to the topic sentence (one wording,
    one rule); a labelled item is its own rule (an imperative body reads as a MUST); a checklist row (`- [ ]`)
    with no modal is judged at the nearest modal sentence, as a fragment is."""
    core = _rule_core(piece)
    holding = _nearest(core, found)
    want = _stems(core)
    cands = _rule_candidates(found)
    scored = [(_score(want, c["text"]), c) for c in cands]
    best = max((sc for sc, _ in scored), default=0.0)
    prose = [(sc, c) for sc, c in scored if not _CODE.match(c["text"])]
    prose_best = max((sc for sc, _ in prose), default=0.0)
    if best > 0 and prose_best < best and prose_best >= best * FALL_SHARE - 1e-9:
        scored, best = prose, prose_best          # a code block never outranks prose holding the piece
        if holding and _CODE.match(holding):
            holding = _nearest(core, [(pt, x) for pt, x in found if not _CODE.match(x)])

    def strength(text: str) -> int:
        body = labelled(text)
        return modal(text)[1] or (3 if imperative(text) or (body and imperative(body)) else 0)

    pick = None
    if best > 0:
        top = [c for sc, c in scored if sc >= best * NEAR_TIE - 1e-9]
        pick = max(top, key=lambda c: (strength(c["text"]), _weight(want, c["text"]), c["sentence"] == holding,
                                       -len(_stems(c["text"]))))
    ruled = [(sc, c) for sc, c in scored if sc > 0 and modals(c["text"])]
    near_c = max(ruled, key=lambda x: (x[0], modal(x[1]["text"])[1] or 0, x[1]["sentence"] == holding),
                 default=(0.0, None))
    near = near_c[1]["text"] if near_c[1] else None
    rule, at = (pick["text"], pick["at"]) if pick else (holding, None)
    if rule is not None and near_c[1] and not modals(rule):      # the tied modal sentence nearest the rule itself
        tied = [c for sc, c in ruled if sc >= near_c[0] * NEAR_TIE - 1e-9]
        alt = max(tied, key=lambda c: (_score(_stems(rule), c["text"]), modal(c["text"])[1] or 0))
        near_c, near = (near_c[0], alt), alt["text"]
    implied = False
    if rule is not None and not modals(rule):
        body = labelled(rule)
        if imperative(rule) or (body is not None and imperative(body)):
            implied = True
        elif (body is None and (no_finite_verb(rule) or _CHECKBOX.match(rule)) and near_c[1]
              and near_c[0] >= best * SCOPE_SHARE - 1e-9 and not _CODE.match(rule)):
            rule, at = near, near_c[1]["at"]
    return {"rule_sentence": rule, "rule_at": at, "nearest_modal_sentence": near, "topic_sentence": holding,
            "implied": implied}


def severity(text: str | None) -> str | None:
    """gapfix14 (G279, 1.4.43): a checklist row's Severity cell (FAIL, WARN, INFO), else None."""
    rows = table_rows(text)
    if not rows or len(rows) != 1:
        return None
    cells = [c.strip(" *`").upper() for c in rows[0].strip("|").split("|")]
    return next((c for c in cells if c in _SEVERITY), None)


def rule_sentence(piece: str, found: list) -> str | None:
    """G202 (1.4.39), G227 (1.4.40): the topic sentence a verdict is judged against (`rule_pick`)."""
    return rule_pick(piece, found)["rule_sentence"]


def clause_of(text: str | None, piece: str) -> str | None:
    """gapfix14 (G280b, 1.4.43): the `;`-clause of `text` sharing most of the piece's words; `text` itself when it
    has one clause. A flat clause is read by its own modal, never by a later MAY/SHOULD clause of its sentence."""
    if not text:
        return text
    parts = [c for c in re.split(r";\s+", text) if c.strip()]
    if len(parts) < 2:
        return text
    want = _stems(piece)
    return max(parts, key=lambda c: (_score(want, c), -parts.index(c)))


def topic_hash(found: list) -> str:
    """G202 (1.4.39): a short hash of every topic sentence: a verdict rests on all of them."""
    import hashlib
    return hashlib.sha1("\n".join(x for _, x in found).encode("utf-8")).hexdigest()[:12]


def _held_rule(result: dict, words_of: dict, texts: dict | None = None, homes: dict | None = None) -> None:
    """G201/G202 (1.4.39), G223/G227 (1.4.40): give each held_by_wording row
    `rule_sentence` (the topic sentence holding the piece, G227),
    `nearest_modal_sentence`, `rule_is_topic_sentence`, `topic_hash`,
    `modal_piece` (the strongest word of the piece), `modal_piece_all` (every
    one), `modal_sentence` (the modal of the building sentence the piece was
    cut from, G223), `modal_topic` (the rule sentence's weakest, or MUST with
    `modal_topic_implied` for an imperative with none), and `modal_differs`:
    the topic's rule is weaker than the piece's, so the row is `not` (stage-1.md
    step 1.3). The piece reads its own modal, else its sentence's, else MUST.
    `home_topic` says whether the topic is the sentence's home: a
    non-building speciality's topic always is; a building sentence's is its
    `home_guess` or the home the plan recorded (`home`, from `homes`: every
    sentence's recorded home, L8, not only a home_unguessed row's). `counted`
    (L28): false when the row is no home of its sentence and the home topic
    holds the sentence (its hold there is the one that counts). `texts` is
    each file's text (the building sentences)."""
    guess = {(b["speciality"], x["n"]): x.get("home_guess") for b in result["building"]
             for x in b.get("sentences", [])}
    recorded = {**(homes or {}), **{(r["speciality"], r["n"]): r["home_recorded"] for r in result["home_unguessed"]
                                    if r.get("home_recorded")}}
    held_at = {(b["speciality"], x["n"]): set(x.get("held_at") or []) for b in result["building"]
               for x in b.get("sentences", [])}
    held_rows = {(r["speciality"], r["n"], r["topic"]) for r in result["held_by_wording"]}
    building = {b["speciality"] for b in result["building"]}
    source: dict[tuple, str] = {}
    for b in result["building"]:
        if b.get("file") and b["file"] in (texts or {}):
            for i, text in enumerate(sentences(texts[b["file"]]), start=1):
                source[(b["speciality"], i)] = text
    for r in result["held_by_wording"]:
        found = words_of.get(r["topic"], (None, []))[1]
        pick = rule_pick(r["text"], found)
        rule = pick["rule_sentence"]
        allm = modals(r["text"])
        mp, rp = modal(r["text"])
        flat = mp is None                     # gapfix14 (G280b): a flat piece reads its own clause, not the sentence's
        src = source.get((r["speciality"], r["n"]))
        ms, rs = modal(clause_of(src, r["text"]) if flat else src) if r["speciality"] in building else (None, None)
        part = clause_of(rule, r["text"]) if flat else rule
        mt, rt = modal_weakest(part)
        if pick["implied"] or (part != rule and mt is None):
            mt, rt = "MUST", 3                # a flat clause of a rule states its requirement unconditionally
        home = recorded.get((r["speciality"], r["n"])) or guess.get((r["speciality"], r["n"]))
        r.update({"modal_piece": mp, "modal_piece_all": list(dict.fromkeys(w for w, _ in allm)),
                  "modal_sentence": ms, "modal_topic": mt, "modal_topic_implied": pick["implied"],
                  "modal_differs": rt is not None and rt < (rp or rs or 3),
                  "home_topic": r["speciality"] not in building or (home is not None and r["topic"] in
                                                                     (home, home.rpartition(":")[2] if
                                                                      home.rpartition(":")[0] == result["area"]
                                                                      else home)),
                  "home": home if r["speciality"] in building else r["topic"],
                  "rule_sentence": rule, "rule_at": pick["rule_at"], "rule_severity": severity(rule),
                  "nearest_modal_sentence": pick["nearest_modal_sentence"],
                  "rule_is_topic_sentence": rule == pick["topic_sentence"], "topic_hash": topic_hash(found)})
        key = (r["speciality"], r["n"])
        at_home = home.rpartition(":")[2] if home and home.rpartition(":")[0] in ("", result["area"]) else None
        named = _named(r.get("marked_for"))       # gapfix14 (G284b): marked for other areas only: counted there
        r["counted"] = not (named and result["area"] not in named) and bool(
            r["home_topic"] or not at_home or at_home == r["topic"] or not (
                at_home in held_at.get(key, ()) or (key[0], key[1], at_home) in held_rows))


def _held_verdicts(result: dict, a: Path) -> None:
    """G159 (1.4.37): give each held_by_wording row its `id`
    (`<speciality>:<n>@<topic>`, `#k` added from the second row sharing it) and
    the verdict `mark.py --held` recorded in A/held.json: `verdict` while the
    piece and the topic sentence are byte-identical to those it was recorded
    on, else `verdict_was` and `verdict_why`. The row is listed either way.
    G202 (1.4.39): a verdict is pinned to the topic's whole text too
    (`topic_hash`) and the rule sentence: any change resets it; a record made
    before (no `topic_hash`) keeps its verdict, `verdict_unpinned` true.
    G189 (1.4.39): a `not` verdict moves its piece from held to lacking in the
    topic's figures (its `own` or `building_marked_elsewhere` share and its
    reference's), counted in `not_held_by_verdict`.
    G251 (1.4.41): a reset verdict (`verdict_was`, no `verdict`) counts as a
    `not` until re-judged."""
    try:
        saved = json.loads((a / HELD).read_text(encoding="utf-8"))
        saved = saved if isinstance(saved, dict) else {}
    except (OSError, ValueError):
        saved = {}
    seen: dict[str, int] = {}
    for r in result["held_by_wording"]:
        base = f"{r['speciality']}:{r['n']}@{r['topic']}"
        seen[base] = seen.get(base, 0) + 1
        r["id"] = base if seen[base] == 1 else f"{base}#{seen[base]}"
        v = saved.get(r["id"])
        if not isinstance(v, dict) or v.get("verdict") not in ("held", "not"):
            continue
        reset = verdict_reset(v, r)
        if reset:
            r["verdict_was"] = v["verdict"]
            r["verdict_why"] = reset
            _stale_counts(result, r)
        else:
            r["verdict"] = v["verdict"]
            if "topic_hash" not in v:
                r["verdict_unpinned"] = True
            if v["verdict"] == "not":
                _not_held(result, r)
                _not_at_home(result, r)


def verdict_reset(v: dict, r: dict) -> str | None:
    """Why the held.json record `v` no longer stands for held_by_wording row
    `r` (G159, G202), else None. stage_status.py's stale_verdicts reads it
    against the live held.json (gapfix13, G269)."""
    # gapfix15 (G304): say which one changed, never "the text" for a moved rule_sentence
    moved = ""
    if "topic_hash" in v and v.get("rule_sentence", r.get("rule_sentence")) != r.get("rule_sentence"):
        moved = f'rule_sentence moved (was "{v.get("rule_sentence")}", now "{r.get("rule_sentence")}")'
    what = [w for w, bad in (("piece text changed", v.get("text") != r.get("text")),
                             ("topic sentence changed", v.get("topic_sentence") != r.get("topic_sentence"))) if bad]
    if what or moved:
        return ("; ".join([*what, *([moved] if moved else [])]) + ": the verdict was recorded on other text, so "
                "judge it again and record it with mark.py --held (G159, G202)")
    if "topic_hash" in v and v["topic_hash"] != r.get("topic_hash"):
        return ("the topic's text (another rule of the topic) changed since the verdict was recorded: judge it "
                "again and record it with mark.py --held (G202)")
    return None


def _stale_counts(result: dict, r: dict) -> None:
    """G251 (1.4.41): a row whose recorded verdict reset (`verdict_was`) counts
    lacking until re-judged, as a `not` does: a recorded `not` never vanishes
    from the total and a reset `held` is no hold on the new text. A reset can
    only raise `measured_total`, never lower it (over-reporting beats missing)."""
    _not_held(result, r)
    _not_at_home(result, r)


def _not_at_home(result: dict, r: dict) -> None:
    """L24 (1.4.40): a `not` verdict on a piece of a sentence measured at a
    home (`home_measures`) makes the sentence lacking in that measure, with
    `verdict_by` the row's id: one verdict per sentence at a topic, never
    `held` there and `not` in held_by_wording."""
    for h in result["home_measures"]:
        if h["topic"] != r["topic"]:
            continue
        for x in h["sentences"]:
            if (x["speciality"], x["n"]) == (r["speciality"], r["n"]) and x["verdict"] == "held":
                x["verdict"] = "lacking"
                x["verdict_by"] = r["id"]


def _not_held(result: dict, r: dict) -> None:
    """G189 (1.4.39): count a `not` row's piece lacking, not held, at its topic."""
    for row in result["topics"]:
        if row["topic"] != r["topic"]:
            continue
        named = _named(r.get("marked_for"))
        part = "building_marked_elsewhere" if named and result["area"] not in named else "own"
        if part == "own" and r.get("counted") is False:      # gapfix14 (G284b): the home holds it: never own
            part = None
            row["not_held_uncounted"] = row.get("not_held_uncounted", 0) + 1
        for figures in (row, row.get(part) if part else None):
            if isinstance(figures, dict) and figures.get("held", 0) > 0:
                figures["held"] -= 1
                figures["lacking"] += 1
        row["not_held_by_verdict"] = row.get("not_held_by_verdict", 0) + 1
        for ref in row["references"]:
            if ref.get("speciality") == r["speciality"]:
                if ref.get("held", 0) > 0:
                    ref["held"] -= 1
                    ref["lacking"] += 1
                ref.setdefault("not_held_by_verdict", []).append(r["n"])
                break


def _lacking_rows(rows: list[tuple], pieces_of: dict, area: str) -> list[dict]:
    """1.4.40 (G225, G226): one row per lacking piece per topic, the pieces
    `own.lacking` and `building_marked_elsewhere.lacking` add up to: `id`
    `lacking:<speciality>:<n or ->@<topic>` (`#k` from the second row
    sharing it), `counted` true for a piece `own` holds (a piece of a
    sentence marked for other areas only is held out of it). `mark.py --held
    ID held --why ...` records that the plan holds the piece in other words."""
    out, seen = [], {}
    for sp, f, topic, piece, n in rows:
        marks = pieces_of[f][1] if f in pieces_of else {}
        away = n is not None and bool(areas_of(marks.get(n))) and area not in areas_of(marks.get(n))
        base = f"lacking:{sp}:{n if n is not None else '-'}@{topic}"
        seen[base] = seen.get(base, 0) + 1
        out.append({"id": base if seen[base] == 1 else f"{base}#{seen[base]}", "speciality": sp, "n": n,
                    "topic": topic, "text": piece, "counted": not away,
                    **({"marked_for": marks.get(n), "counted_at": sorted(areas_of(marks.get(n)))} if away else {})})
    return out


def _short_ids(result: dict) -> None:
    """1.4.40 (G225): each `short_sentences` row's `id`
    (`short:<speciality>:<n or ->`, `#k` from the second) and whether its
    sentence is this area's (`counted`: unmarked, unknown or marked for it)."""
    seen: dict[str, int] = {}
    for r in result["short_sentences"]:
        base = f"short:{r['speciality']}:{r['n'] if r.get('n') is not None else '-'}"
        seen[base] = seen.get(base, 0) + 1
        r["id"] = base if seen[base] == 1 else f"{base}#{seen[base]}"
        named = _named(r.get("marked_for"))
        r["counted"] = not (named and result["area"] not in named)


def short_not_owed(result: dict) -> list[dict]:
    """gapfix13b (1.4.42, platform-integration#5): each short_sentences row
    that owes no verdict here (`counted` false: its sentence is marked for
    another area only): {id, topic, marked_for, counted_at, why}, so the
    rows owing one are the rest."""
    out = []
    for r in result.get("short_sentences") or []:
        if r.get("counted", True):
            continue
        at = sorted(_named(r.get("marked_for")))
        out.append({"id": r.get("id"), "topic": r.get("topic"), "marked_for": r.get("marked_for"), "counted_at": at,
                    "why": f"marked for {', '.join(at)} only, so it is counted there: no verdict is owed here"})
    return out


def _record(a: Path, rows: list[dict], pins: tuple, kind: str):
    """The verdict `mark.py --held` recorded for each row of `rows`, set as
    `verdict` and `why` while the row's text still is what it was judged on,
    else as `verdict_was`/`verdict_why`; yields each row that kept one."""
    try:
        saved = json.loads((a / HELD).read_text(encoding="utf-8"))
        saved = saved if isinstance(saved, dict) else {}
    except (OSError, ValueError):
        saved = {}
    for r in rows:
        v = saved.get(r["id"])
        if not isinstance(v, dict) or v.get("verdict") not in ("held", "not"):
            continue
        # gapfix14: a pin recorded as null or absent (a 1.4.42 home row had no text) is not checked
        if any(v.get(k) is not None and v.get(k) != r.get(k) for k in pins):
            r["verdict_was"] = v["verdict"]
            r["verdict_why"] = (f"the {kind} changed since the verdict was recorded: judge it again and record it "
                                "with mark.py --held (G225)")
            continue
        r["verdict"] = v["verdict"]
        if v.get("why"):
            r["why"] = v["why"]
        yield r


def _lacking_verdicts(result: dict, a: Path) -> None:
    """1.4.40 (G225, G226): apply the hand verdicts. A lacking piece the plan
    holds in other words (`held`) moves from lacking to held at its topic,
    in `own` or `building_marked_elsewhere` (`counted`) and in its
    reference's figures (`lacking_held_by_verdict`), exactly as a `not` on a
    held row moves the other way. A short piece verdict `not` is counted in
    `measured_total`; `held` changes nothing."""
    area_dir = a
    for r in _record(area_dir, result["lacking_pieces"], ("text",), "piece"):
        if r["verdict"] != "held":
            continue
        for row in result["topics"]:
            if row["topic"] != r["topic"]:
                continue
            part = "own" if r["counted"] else "building_marked_elsewhere"
            for figures in (row, row.get(part)):
                if isinstance(figures, dict) and figures.get("lacking", 0) > 0:
                    figures["lacking"] -= 1
                    figures["held"] += 1
            row["lacking_held_by_verdict"] = row.get("lacking_held_by_verdict", 0) + 1
            for ref in row["references"]:
                if ref.get("speciality") == r["speciality"] or ref.get("speciality") is None and \
                        r["speciality"] == ref.get("file"):
                    if ref.get("lacking", 0) > 0:
                        ref["lacking"] -= 1
                        ref["held"] += 1
                    ref.setdefault("lacking_held_by_verdict", []).append(r["n"])
                    break
    for _ in _record(area_dir, result["short_sentences"], ("text",), "short piece"):
        pass


def measured_total(result: dict) -> int:
    """1.4.40 (G225, G226): the area's gap total in one unit: the lacking
    pieces `own` holds after every recorded verdict (a `not` on a held row
    is already in `own`, a `held` on a lacking piece already out of it),
    plus each short piece judged `not` held that is this area's.
    gapfix13 (1.4.42, G253, G254): plus each lacking home-measure sentence
    this area owns (`home_lacking`), each lacking piece of the area's own R9
    files (`r9_lacking`) and each hand lack (`hand_lacks`), less those judged
    `held`: the sum of `topic_totals`. The unit is the topic row: a piece
    lacking at three topics counts three until each row has a verdict (G256)."""
    return sum(t["total"] for t in topic_totals(result))


def _open(r: dict) -> bool:
    """A row of the gapfix13 lists that counts: `counted`, and no `held` verdict."""
    return bool(r.get("counted", True)) and r.get("verdict") != "held"


def topic_totals(result: dict) -> list[dict]:
    """gapfix13 (1.4.42, G253): `measured_total` per topic: {topic,
    measured (own.lacking), short, home, r9, hand, total}; a new or unmeasured
    topic a hand lack, home measure or R9 file names gets its own row, a
    short piece with no topic the row "(no topic)". The totals add up to
    `measured_total`."""
    per: dict[str, dict[str, int]] = {}

    def add(topic, key, n=1):
        row = per.setdefault(topic or "(no topic)", {"measured": 0, "short": 0, "home": 0, "r9": 0, "hand": 0})
        row[key] += n
    for t in result.get("topics") or []:
        if isinstance(t.get("own"), dict):
            add(t["topic"], "measured", t["own"].get("lacking", 0))
    for r in result.get("short_sentences") or []:
        if r.get("verdict") == "not" and r.get("counted", True):
            add(r.get("topic"), "short")
    for key, kind in (("home_lacking", "home"), ("r9_lacking", "r9"), ("hand_lacks", "hand")):
        for r in result.get(key) or []:
            if _open(r):
                add(r.get("topic"), kind)
    return [{"topic": t, **c, "total": sum(c.values())} for t, c in per.items()]


def non_home_lacking(result: dict, homes: dict) -> list[dict]:
    """gapfix13 (1.4.42, G256): each counted, unjudged lacking piece of a
    building sentence at a topic that is not the sentence's home (its
    recorded home, else its home_guess): {id, topic, home}. Each still
    counts (a verdict per row moves it); listed so the rows are seen."""
    guess = {(b.get("speciality"), x.get("n")): x.get("home_guess")
             for b in result.get("building") or [] for x in b.get("sentences") or []}
    out = []
    for r in result.get("lacking_pieces") or []:
        key = (r.get("speciality"), r.get("n"))
        if key not in guess or not _open(r) or r.get("verdict"):
            continue
        rec = homes.get(key)
        if isinstance(rec, str):
            where, _, topic = rec.rpartition(":")
            home = topic if where in ("", result["area"]) else rec
        else:
            home = guess[key]
        if home and home != r.get("topic"):
            row = {"id": r["id"], "topic": r.get("topic"), "home": home}
            v = home_verdict(result, key[0], key[1], home) if ":" not in home else None
            if v:      # gapfix14 (G276): the home's verdict here, a hand hold too
                row["home_verdict"] = v
            out.append(row)
    return out


HAND = "hand_lacks.json"      # gapfix13 (1.4.42, G253): mark.py --lack


def _home_rows(result: dict, homes: dict) -> None:
    """gapfix13 (1.4.42, G254 b): each lacking home-measure sentence is a row
    of `home_lacking`: {id (`home:<speciality>:<n>@<topic>`), speciality, n,
    topic, text, counted, counted_at, why_not_counted?}. `counted_at` is the
    area owning its home (the area of a home recorded as AREA:TOPIC, else
    this one, whose topic measured it); it is counted here when owned here
    and not already in a topic's own figures (a `not` row's `verdict_by` at a
    measured topic). One owned by another area says `counted at <area>` and
    is not counted here. `mark.py --held` judges the rows; home_measures
    keeps its shape."""
    area, names = result["area"], {t.get("topic") for t in result.get("topics") or []}
    flat, seen = [], {}
    for h in result.get("home_measures") or []:
        for x in h.get("sentences") or []:
            if x.get("verdict") != "lacking":
                continue
            base = f"home:{x.get('speciality')}:{x.get('n')}@{h.get('topic')}"
            seen[base] = seen.get(base, 0) + 1
            rec = homes.get((x.get("speciality"), x.get("n")))
            owner = (rec.rpartition(":")[0] if isinstance(rec, str) else "") or area
            inside = bool(x.get("verdict_by")) and h.get("topic") in names
            at = rec.rpartition(":")[2] if isinstance(rec, str) and owner == area else None
            hold = held_at_home(result, x.get("speciality"), x.get("n"), at) if at and at != h.get("topic") else None
            row = {"id": base if seen[base] == 1 else f"{base}#{seen[base]}", "speciality": x.get("speciality"),
                   "n": x.get("n"), "topic": h.get("topic"),
                   "text": x.get("text"), **({"pieces": x["pieces"]} if x.get("pieces") else {}),
                   "counted": owner == area and not inside and not hold, "counted_at": owner}
            if owner != area:
                row["why_not_counted"] = f"counted at {owner}: its recorded home is {rec}"
            elif hold:      # gapfix14 (G277): the recorded home wins over the word-match topic
                row["why_not_counted"] = (f"held at its recorded home {at} by {hold}: the word-match topic "
                                          f"{h.get('topic')} is no home of it")
            elif inside:
                row["why_not_counted"] = f"counted in {h.get('topic')}'s own figures by {x['verdict_by']}"
            flat.append(row)
    result["home_lacking"] = flat


def _judge_new_rows(result: dict, a: Path) -> None:
    """gapfix13 (1.4.42): apply A/held.json to home_lacking, r9_lacking and
    hand_lacks; a `held` row is uncounted (a hand lack: withdrawn), with the
    why; a `not` confirms it, still counted."""
    for key, kind in (("home_lacking", "home sentence"), ("r9_lacking", "R9 piece"), ("hand_lacks", "hand lack")):
        for r in _record(a, result.get(key) or [], ("text",), kind):
            if r["verdict"] == "held" and r.get("counted"):
                r["counted"], r["held_out"] = False, True      # held_out: counted but for the verdict
                r["why_not_counted"] = "judged held" + (f": {r['why']}" if r.get("why") else "")


def _r9_rows(out_dir: Path) -> list[dict]:
    """gapfix13 (1.4.42, G254 a): one row per lacking piece of the area's own
    R9 files (`new-<name>.json` in the gaps folder), counted at topic
    <name>: `id` `r9:<name>:<speciality>:<n, else the piece's place>`."""
    rows, seen = [], {}
    for f in sorted(out_dir.glob("new-*.json")) if out_dir.is_dir() else []:
        try:
            data = json.loads(f.read_text(encoding="utf-8"))
            refs = data.get("references") or []
        except (OSError, ValueError, AttributeError):
            continue
        name = f.stem[len("new-"):]
        for ref in refs if isinstance(refs, list) else []:
            if not isinstance(ref, dict):
                continue
            sp = Path(str(ref.get("file") or "")).stem.replace("--", "/")
            nums = ref.get("lacking_numbers") if isinstance(ref.get("lacking_numbers"), list) else []
            for k, piece in enumerate(ref.get("lacking_sentences") or [], start=1):
                n = nums[k - 1] if k <= len(nums) and isinstance(nums[k - 1], int) else None
                base = f"r9:{name}:{sp}:{n if n is not None else k}"
                seen[base] = seen.get(base, 0) + 1
                rows.append({"id": base if seen[base] == 1 else f"{base}#{seen[base]}", "speciality": sp, "n": n,
                             "topic": name, "text": piece, "file": f.name, "counted": True})
    return rows


def missing_subjects(plan: Path) -> int:
    """gapfix14 (1.4.43, G286): the top-level items of the plan's `## Missing subjects` section. A Missing subject
    has no source sentence, so it is no `--lack` row and never in `measured_total`; it is carried by a Research
    question (or `### No host`). Shown beside measured_total; 0 with no plan or no section."""
    from stage_status import _ITEM, _sections_of
    try:
        text = plan.read_text(encoding="utf-8")
    except OSError:
        return 0
    return sum(1 for head, body in _sections_of(text) if head.lower() == "missing subjects"
               for line in body if _ITEM.match(line))


def r9_once(result: dict) -> None:
    """gapfix14 (1.4.43, G281a): a lacking piece of a topic row that an R9
    row of this area holds too (same speciality, same text) counts once, at
    the R9 row: the topic row gets `counted` false, `counted_at` "r9" and
    `counted_by` (the R9 row's id), and leaves its topic's `own.lacking`
    (`lacking_counted_at_r9` counts them). A piece already judged held, or
    counted at another area, is left as it is."""
    r9 = {(r.get("speciality"), " ".join(str(r.get("text") or "").split())): r["id"]
          for r in result.get("r9_lacking") or []}
    for r in result.get("lacking_pieces") or []:
        by = r9.get((r.get("speciality"), " ".join(str(r.get("text") or "").split())))
        if not by or not r.get("counted") or r.get("verdict") == "held":
            continue
        r.update({"counted": False, "counted_at": "r9", "counted_by": by})
        for row in result["topics"]:
            if row["topic"] == r["topic"]:
                for figures in (row, row.get("own")):
                    if isinstance(figures, dict) and figures.get("lacking", 0) > 0:
                        figures["lacking"] -= 1
                row["lacking_counted_at_r9"] = row.get("lacking_counted_at_r9", 0) + 1
                break


MEASURED_ROWS = ("lacking_pieces", "held_by_wording", "short_sentences", "home_lacking", "r9_lacking")


def measured_row(result: dict, sp: str, n, topic: str | None = None) -> str | None:
    """The id of the first measured row of sentence (sp, n), else None (G253: a hand lack never doubles one).
    gapfix14 (1.4.43, G285): with `topic`, a row holding the sentence at another topic (a held_by_wording row
    standing, any row judged `held`) blocks nothing: a hold elsewhere is no lack here."""
    for key in MEASURED_ROWS:
        for r in result.get(key) or []:
            if isinstance(r, dict) and r.get("speciality") == sp and r.get("n") == n and r.get("id"):
                if topic is not None and r.get("topic") != topic and (
                        r.get("verdict") == "held" or key == "held_by_wording" and r.get("verdict") != "not"):
                    continue
                return r["id"]
    for h in result.get("home_measures") or []:      # a report saved before home_lacking
        for x in h.get("sentences") or []:
            if x.get("speciality") == sp and x.get("n") == n and x.get("verdict") == "lacking":
                return x.get("id") or f"home:{sp}:{n}@{h.get('topic')}"
    return None


def _hand_rows(result: dict, a: Path) -> None:
    """gapfix13 (1.4.42, G253): each hand lack `mark.py --lack` recorded in
    A/hand_lacks.json, a row of `hand_lacks` counted at its topic; withdrawn
    by a `held` verdict (`mark.py --held <id> held --why`), and not counted
    (`duplicate_of`) once a measured row holds its sentence."""
    try:
        saved = json.loads((a / HAND).read_text(encoding="utf-8"))
        saved = saved if isinstance(saved, dict) else {}
    except (OSError, ValueError):
        saved = {}
    rows = []
    for rid, v in saved.items():
        if not isinstance(v, dict):
            continue
        row = {"id": rid, "speciality": v.get("speciality"), "n": v.get("n"), "topic": v.get("topic"),
               "text": v.get("text"), "source": v.get("source"), "lack_why": v.get("why"), "counted": True}
        dup = measured_row(result, row["speciality"], row["n"], row["topic"])
        if dup:
            row["counted"], row["duplicate_of"] = False, dup
        rows.append(row)
    result["hand_lacks"] = rows


UNMARKED, UNKNOWN = "unmarked", "unknown"


def _resolve_marks(result: dict, workspace: Path, m: dict, texts: dict) -> None:
    """G124 (1.4.36): every `marked_for` this area leaves null is read from
    every plan's marks files (unmeasured.plan_marks), matched by the
    sentence's text: the areas they name; "unmarked" when a marks file holds
    the speciality and none marks the sentence; "unknown" when no plan has a
    marks file for it, or the piece is in no one sentence. Never null."""
    area = result["area"]
    try:
        plans, _ = plan_marks(workspace, area)
    except SystemExit:
        plans = {}
    by_sp: dict[str, list[dict]] = {}
    for files in plans.values():
        for d in files:
            if isinstance(d.get("sentences"), list) and isinstance(d.get("marks"), dict):
                by_sp.setdefault(d["speciality"], []).append(d)
    file_of = {b["speciality"]: b["file"] for b in m["building"] if b.get("file")}
    here = {(x.get("speciality"), x.get("n")) for x in m["marked_here"] if isinstance(x, dict)}

    def resolve(sp: str, n) -> object:
        if not isinstance(n, int):
            return UNKNOWN
        f = file_of.get(sp)
        found = sentences(texts[f]) if f in texts else []
        text = found[n - 1] if 1 <= n <= len(found) else None
        named = [area] if (sp, n) in here else []
        for d in by_sp.get(sp, []):
            for x in d["sentences"]:
                if isinstance(x, dict) and (_norm(x.get("text") or "") == _norm(text) if text is not None
                                            else x.get("n") == n):
                    named += areas_of(d["marks"].get(str(x.get("n"))))
        return _mark(named) or (UNMARKED if by_sp.get(sp) else UNKNOWN)
    rows = [*result["home_unguessed"], *result["short_sentences"], *result["held_by_wording"],
            *(x for h in result["home_measures"] for x in h["sentences"]),
            *(x for b in result["building"] for x in b["unmeasured_sentences"])]
    for b in result["building"]:
        for x in b["unmeasured_sentences"]:
            x.setdefault("speciality", b["speciality"])
    for r in rows:
        if r.get("marked_for") is None:
            r["marked_for"] = resolve(r["speciality"], r.get("n"))
    for b in result["building"]:
        for x in b["unmeasured_sentences"]:
            del x["speciality"]


def _named(mark) -> list[str]:
    """The areas a resolved mark names: never "unmarked" or "unknown"."""
    return [x for x in areas_of(mark) if x not in (UNMARKED, UNKNOWN)]


HOMES = "homes.json"


def recorded_homes(a: Path) -> dict[tuple, str]:
    """(speciality, n) -> the home the plan recorded for that building
    sentence: A/building-*.json `homes` and A/homes.json (`mark.py --home`)."""
    homes: dict[tuple, str] = {}
    for f in sorted(a.glob("building-*.json")):
        try:
            d = json.loads(f.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            continue          # an unreadable marks file stops unmeasured.py, never this tag
        if isinstance(d, dict) and isinstance(d.get("homes"), dict):
            for n, topic in d["homes"].items():
                if topic:
                    homes[(d.get("speciality"), int(n) if str(n).isdigit() else n)] = topic
    try:      # G156 (1.4.37): a home in another area, `<area>:<topic>`, from mark.py --home
        other = json.loads((a / HOMES).read_text(encoding="utf-8"))
    except (OSError, ValueError):
        other = {}
    for sp, by_n in (other.items() if isinstance(other, dict) else ()):
        for n, topic in (by_n.items() if isinstance(by_n, dict) else ()):
            if topic:
                homes[(sp, int(n) if str(n).isdigit() else n)] = topic
    return homes


def _tag_unguessed(result: dict, a: Path) -> None:
    """G123 (1.4.36): a `home_unguessed` row marked for other areas only is
    tagged `count_only` (G91: counted, never judged here), never removed.
    G145: a home the plan recorded with `mark.py --home` is `home_recorded`;
    the row stays listed."""
    area = result["area"]
    homes = recorded_homes(a)
    for r in result["home_unguessed"]:
        named = _named(r["marked_for"])
        if named and area not in named:
            r["count_only"] = True
            r["why"] += f"; marked for {', '.join(named)} only: counted, never judged here (G91)"
        if (r["speciality"], r["n"]) in homes:
            r["home_recorded"] = homes[(r["speciality"], r["n"])]


_MARKER = re.compile(r"^\s*(?:[-*+\u2022\u2013]+|\(?(?:[0-9]{1,3}|[a-zA-Z]|[ivxIVX]{1,4})[.)])\s*$")
_LABEL_VERBS = {"must", "should", "shall", "may", "never", "always", "is", "are", "be", "do", "does", "use",
                "keep", "make", "avoid", "prefer", "ensure", "require", "requires", "run", "set", "add",
                "check", "write", "cannot", "can", "will", "has", "have", "not"}


# Fix round 1 (1.4.36, review I1): the colon is required, inside or after the bold;
# a colonless bold line is a whole rule, a piece.
_BOLD_LABEL = re.compile(r"^\s*(?:[-*+]\s+)?\*\*[^*]+(?::\*\*|\*\*\s*:)\s*$")
_HEADING = re.compile(r"^\s*#{1,6}\s+\S")
# G161 (1.4.37): Review / Closing, or a procedure lead ending in a colon; a
# piece ending in "pass" is no opener (it may be a rule).
_OPENER = re.compile(r"^\s*(?:Review|Closing)\b|^\s*(?:Before|After|When|Once|Finally|Then|Next|First|"
                     r"During|Lastly|Afterwards)\b[^:]*:\s*$")
_CODE_TOKEN = re.compile(r"[\w#./-]*[_0-9#][\w#./-]*:\s*$")


def piece_kind(piece: str, after_vs: bool = False) -> str:
    """G103 (1.4.33), G125 (1.4.36): the kind of a short piece, checked in
    this order. "marker": only a list marker (`-`, `1.`, `(a)`). "cut":
    cookr's cut made it meaningless alone: an odd number of backticks (cut
    inside a code span), at or after `vs.`, or a code token before a closing
    `:` (`sha256:`, `frozen_string_literal:`, `# type:`); judged with its
    sentence (G102). "heading": a `#` line. "label": a heading label (ends in
    `:` with no verb of _LABEL_VERBS) or a `- **name**:` rule label, whatever
    its words; a bold line with no colon is a piece (fix round 1). "opener": a procedure opener ("Review ...", "Closing ...",
    or a procedure lead such as "Before merging:", G161, 1.4.37), checked before the label. Else "piece": any kind left uncertain is a piece,
    counted. Only a label and an opener take the held-by-part rule (G103).
    A heuristic, advisory: every row is still listed and counted unless judged."""
    if _MARKER.match(piece):
        return "marker"
    text = piece.rstrip()
    low = text.lower()
    if (text.count("`") % 2 == 1 or after_vs or low.endswith(("vs.", " vs")) or _CODE_TOKEN.search(text)
            or (_HEADING.match(text) and text.endswith(":"))):       # `# type:`: a comment cut at its colon
        return "cut"
    if _HEADING.match(text):
        return "heading"
    if _BOLD_LABEL.match(text):
        return "label"
    verbs = set(re.findall(r"[a-z']+", low)) & _LABEL_VERBS
    if _OPENER.search(text) and not verbs:      # G161: before the colon label, so "Before merging:" opens
        return "opener"
    if text.endswith(":") and not verbs:
        return "label"
    return "piece"


def fragment(piece: str, after_vs: bool = False) -> bool:
    """G102 (1.4.33): a piece cookr's cut made meaningless on its own, or a
    label naming a part: `piece_kind` "cut" or "label" (G125, 1.4.36). Judged
    with the sentence it was cut from (its `n`); listed and counted unless judged held."""
    return piece_kind(piece, after_vs) in ("cut", "label")


REPEAT_SHARE = 0.75     # G104: the share of the shorter sentence's words the longer one holds: a restatement


def _repeats(topics: list[dict], texts: dict, own_review_focus: set[str] = frozenset()) -> list[dict]:
    """G104 (1.4.33): within one speciality, each lacking sentence that
    restates an earlier lacking one (the same text, or the longer holding
    REPEAT_SHARE of the shorter's words, as "A complete review must establish
    that ..." restates a rule): [{"speciality", "text", "sentences", "topics",
    "review_focus_pair", "pieces"}], the shape of `same_text`. G146 (1.4.36):
    `review_focus_pair` is True for sentences [1, 2], the format-2 Review
    focus and its restatement (every direct speciality has it), tagged, never
    skipped, only for a file in `own_review_focus` (1.4.46: a format-3 roled
    reference leaves its copied Review focus out, so its sentences 1 and 2 are
    other text, and a file with no A/reference.json row is never assumed to
    open with one); `pieces` names each sentence's text and the topics it is counted
    at. Advisory: every sentence still counts where it stands."""
    lacking: dict[tuple, dict[int, set[str]]] = {}      # (speciality, file) -> n -> topics
    for t in topics:
        for r in t["references"]:
            for n in r["lacking_numbers"]:
                if isinstance(n, int):
                    lacking.setdefault((r["speciality"] or r["file"], r["file"]), {}).setdefault(n, set()).add(
                        t["topic"])
    out = []
    for (sp, f), by_n in sorted(lacking.items()):
        if f not in texts:
            continue
        found = sentences(texts[f])
        ns = sorted(n for n in by_n if 1 <= n <= len(found))
        groups: dict[int, list[int]] = {}
        for j, n in enumerate(ns):
            w = words(found[n - 1])
            for i in ns[:j]:
                v = words(found[i - 1])
                same = _norm(found[i - 1]) == _norm(found[n - 1])
                if same or (w and v and len(w & v) / min(len(w), len(v)) >= REPEAT_SHARE):
                    root = next((r for r, g in groups.items() if i in g), i)
                    groups.setdefault(root, [root]).append(n)
                    break
        for root, g in sorted(groups.items()):
            ns_ = sorted(set(g))
            out.append({"speciality": sp, "text": found[root - 1], "sentences": ns_,
                        "topics": sorted(set().union(*(by_n[n] for n in g))),
                        # G146: the Review focus restated; 1.4.46: only where the file opens with it
                        "review_focus_pair": ns_ == [1, 2] and f in own_review_focus,
                        "pieces": [{"n": n, "text": found[n - 1], "topics": sorted(by_n[n])} for n in ns_]})
    return out


def _default_out(out_dir: Path, a: Path) -> bool:
    """Whether `out_dir` is the area's A/gaps, by any spelling (R-M-1)."""
    return out_dir.resolve() == (a / "gaps").resolve()


def _reference(sp: str, a: Path, mode: str, scratch: Path | None, devteam: Path | None,
               cookr_py: str, out_dir: Path | None = None) -> tuple[Path | None, str, bool]:
    """G68: a `marked_here` speciality's reference file, (file, why, stale).
    It has no A/reference.json row to stamp, so a run writes it afresh with
    `<devteam>/speciality_reference.py` every time (R-I-1, R-M-3, 1.4.27):
    into A/reference on a run, into DIR/reference on a run with its own
    `--out DIR` (never into the area), into the scratch folder under
    --check. "saved" mode reads DIR/reference, then A/reference. With no
    speciality_reference.py, an existing file is used as it is and `stale`
    is True (its format unknown); so is it with a speciality_reference.py
    whose FORMAT is older than REFERENCE_FORMAT, which is never run (1.4.46)."""
    name = sp.replace("/", "--") + ".txt"
    own = out_dir / "reference" if out_dir is not None and not _default_out(out_dir, a) else None
    here = [d / name for d in (own, a / "reference") if d is not None and (d / name).is_file()]
    script = devteam / "speciality_reference.py" if devteam else None
    if mode == "saved":
        return (here[0], "", False) if here else (
            None, f"no A/reference/{name}: a run writes it with speciality_reference.py", False)
    if script is None or not script.is_file():
        if here:
            return here[0], "", True
        return None, (f"no A/reference/{name}, and no {script} to write it: write it with "
                      f"speciality_reference.py {sp} --out A/reference"), False
    if not is_current(writer_format(script)):      # 1.4.46: an unpulled devteam writes an older format
        if here:
            return here[0], "", True
        return None, (f"no A/reference/{name}, and {script} writes a reference format older than "
                      f"{REFERENCE_FORMAT}: pull the devteam checkout, then run again"), False
    out = (own or a / "reference") if mode == "write" else scratch / "reference"
    try:
        r = subprocess.run([cookr_py, str(script), sp, "--out", str(out)], capture_output=True, text=True,
                           cwd=script.parent)
    except OSError as e:     # N1: the python cannot start
        return None, f"speciality_reference.py {sp} could not run: {e}", False
    if r.returncode != 0 or not (out / name).is_file():
        return None, (f"speciality_reference.py {sp} exited {r.returncode}: "
                      f"{(r.stderr.strip().splitlines() or ['no file written'])[-1]}"), False
    return out / name, "", False


def _home_measures(area: str, a: Path, repo: Path, m: dict, result: dict, out_dir: Path, cookr: tuple,
                   mode: str, scratch: Path | None, devteam: Path | None, cache: tuple,
                   area_words: dict) -> list[tuple[str, str]]:
    """G68: each building sentence whose home_guess is a topic its file was
    not measured at (a topic no speciality names, most often), and each
    sentence of a `marked_here` speciality with no building row (its
    reference written when missing; its home guessed as `_candidates` does,
    `home_unguessed` when none), measured at that home: one
    `gaps/home--<name>.json` per home, run_gaps' own file, cleared like the
    rest when no sentence is homed there any more. Rows go to
    `home_measures`; returns the extra (speciality, file) pairs measured."""
    cookr_py, cli = cookr
    texts, cuts = cache
    want: dict[str, dict] = {}

    marked_for: dict[tuple, object] = {}      # G100: (speciality, file, n) -> its mark

    def home(h: str, sp: str, f: str, n: int, mark) -> None:
        g = want.setdefault(h, {"against": [], "sentences": []})
        if (sp, f) not in g["against"]:
            g["against"].append((sp, f))
        if (sp, f, n) not in g["sentences"]:      # R-N-1: once, however often it is marked
            g["sentences"].append((sp, f, n))
        marked_for.setdefault((sp, f, n), mark)
    for e in result["building"]:
        found = sentences(texts[e["file"]]) if e["file"] in texts else []
        for s in e["sentences"]:
            if s["home_guess"] and s["home_guess"] not in e["measured_at"]:
                home(s["home_guess"], e["speciality"], e["file"], s["n"], s["mark"])
            elif s["home_guess"] is None and not s["held_at"]:
                # G95 (1.4.33): no home guessed and no measured topic holds it,
                # whatever its mark (G91: one marked elsewhere is counted, never judged).
                lack = s["lacking_at"] or s.get("measured_pieces", {}).get("lacking_at", [])
                result["home_unguessed"].append({
                    "speciality": e["speciality"], "n": s["n"],
                    "text": found[s["n"] - 1] if s["n"] <= len(found) else None, "marked_for": s["mark"],
                    "why": (f"measured, lacking at every topic it was measured at ({', '.join(lack)}), and no "
                            "home guessed: the plan names its home" if lack else      # G145 (1.4.36)
                            "no home guessed and no measured topic holds it: the plan names its home")})
    has_row = {b["speciality"] for b in m["building"]}
    extra_rows: dict[str, list] = {}
    for x in m["marked_here"]:
        if isinstance(x, dict) and x.get("speciality") and x["speciality"] not in has_row:
            rows_of = extra_rows.setdefault(x["speciality"], [])
            if all((y.get("n"), y.get("text")) != (x.get("n"), x.get("text")) for y in rows_of):
                rows_of.append(x)      # R-N-1: the same row from two marking plans, once
    extra = []
    for sp, rows in sorted(extra_rows.items()):
        f, why, old = _reference(sp, a, mode, scratch, devteam, cookr_py, out_dir)
        if f is None:
            result["missing_files"].append({"speciality": sp, "why": why})
            continue
        if old:      # R-I-1: used as it is, never as current
            result["stale_reference"].append({"speciality": sp, "file": str(f), "format": None,
                                              "want": REFERENCE_FORMAT,
                                              "why": f"{NO_WRITER_WHY}; {STALE_WHY}",
                                              "reason": NO_WRITER})      # N3-M-2: read by stage_status
        texts[str(f)] = f.read_text(encoding="utf-8")
        extra.append((sp, str(f)))
        found = sentences(texts[str(f)])
        for x in rows:
            n, text = x.get("n"), x.get("text")
            at = [i for i, s in enumerate(found, start=1) if text is not None and _norm(s) == _norm(text)]
            now = found[n - 1] if isinstance(n, int) and 1 <= n <= len(found) else None
            if text is None or now is None or _norm(now) != _norm(text):
                # I2: the marks numbered another text; measure the sentence the
                # row's text names (one place only), never the one now at n.
                to = n if text is None and now is not None else (at[0] if len(at) == 1 else None)
                result["numbering_differs"].append({"speciality": sp, "n": n, "text": text, "now": now,
                                                    "found_at": at, "measured_as": to})
                if to is None:      # R-I-2: judged by hand, with every other unmeasured sentence
                    result["home_unguessed"].append({
                        "speciality": sp, "n": n, "text": text, "marked_for": area,
                        "why": "numbering differs: its text is not found once in the reference; judge it by "
                               "hand or re-mark it"})
                    continue
                n = to
            s = {"home_guess": None}
            _candidates(s, found[n - 1], area_words)
            if s["home_guess"] is None:
                result["home_unguessed"].append({"speciality": sp, "n": n, "text": found[n - 1],
                                                 "marked_for": area,
                                                 "why": "no topic folder of the area shares enough of its words"})
                continue
            home(s["home_guess"], sp, str(f), n, area)
    folder_of = {t["topic"]: t["folder"] for t in m["topics"].values()}
    names = set()
    for h, g in sorted(want.items()):
        folder = folder_of.get(h, f"cookbook/guidelines/{area}/{h}")
        name = f"{HOME}{folder.rsplit('/', 1)[-1]}.json"
        names.add(name)
        t = {"topic": h, "folder": folder, "against": g["against"]}
        if mode == "saved":
            data, why = _saved(out_dir / name, texts)
        else:
            data, why = _measure(t, (scratch if mode == "fresh" else out_dir) / name, repo, cookr_py, cli, texts)
        if data is None:
            print(f"run_gaps.py: home measure at {h} ({folder}) failed, its previous file kept: {why}",
                  file=sys.stderr)
            result["failed"].append({"topic": h, "why": why.splitlines()[0]})
            continue
        lacking = {r["file"]: set(r["lacking_numbers"]) for r in data.get("references", [])}
        verdicts = []
        for sp, f, n in g["sentences"]:
            try:
                pieces = _cut(f, cuts, cookr_py, cli)
            except (OSError, ValueError) as e:     # N1
                pieces = []
                if not any(x.get("speciality") == sp for x in result["failed"]):
                    result["failed"].append({"speciality": sp, "why": str(e).splitlines()[0]})
            cut = list(zip(pieces, numbers([p for p, _ in pieces], texts[f])))
            whole = any(k for (_, k), x in cut if x == n) and all(k for (_, k), x in cut if x == n)
            if f not in lacking:      # M2: the home file never measured this reference
                verdict = "not measured"
            else:
                verdict = "lacking" if n in lacking[f] else ("held" if whole else "not measured")
            whole_text = sentences(texts[f])
            verdicts.append({"speciality": sp, "n": n, "verdict": verdict,
                             "marked_for": marked_for.get((sp, f, n)),       # G100: never filtered
                             # gapfix14 (G302): a lacking sentence carries its text and its lacking pieces, so
                             # its home_lacking row reads alone
                             **({"text": whole_text[n - 1] if 1 <= n <= len(whole_text) else None,
                                 "pieces": [pc for (pc, kept), x in cut if kept and x == n]}
                                if verdict == "lacking" else {})})
            if verdict == "held":      # G132 (1.4.36): a hold at its home rests on wording too
                said = _numerals(" ".join(x for _, x in area_words.get(h, (None, []))[1]))
                for (piece, kept), x in cut:
                    if kept and x == n:
                        result["held_by_wording"].append({
                            "speciality": sp, "n": n, "text": piece, "topic": h,
                            "marked_for": marked_for.get((sp, f, n)), "number_differs": bool(_numerals(piece) - said),
                            "topic_sentence": _nearest(piece, area_words.get(h, (None, []))[1])})
        row = {"topic": h, "folder": folder, "gaps_file": name,
               "specialities": sorted({sp for sp, _ in g["against"]}),
               "sentences": sorted(verdicts, key=lambda v: (v["speciality"], v["n"]))}
        missing = sorted({f for _, f in g["against"] if f not in lacking})
        if missing:
            row["unmeasured_references"] = missing
        result["home_measures"].append(row)
    gone = sorted(p.name for p in out_dir.glob(f"{HOME}*.json") if p.name not in names) if out_dir.is_dir() else []
    key = "cleared" if mode == "write" else "would_clear"
    for n in gone:
        if ours(out_dir / n):
            if mode == "write":
                (out_dir / n).unlink()
            result[key].append(n)
        else:
            result["stale_gaps"].append(n)
    return extra


def _candidates(s: dict, text: str, area_words: dict) -> None:
    """G50: `lacking_candidates`, the area's topic folders (any, a folder no
    speciality names included) ranked by the share of the sentence's words
    each holds, top 3 above 0; and `home_guess`, when none was guessed, the
    first of them at HOME_SHARE or more, never on a tie. Advisory."""
    want = words(text)
    if not want:
        s["lacking_candidates"] = []
        return
    ranked = sorted(((len(want & w) / len(want), name) for name, (w, _) in area_words.items()),
                    key=lambda x: (-x[0], x[1]))
    ranked = [(share, name) for share, name in ranked if share > 0]
    s["lacking_candidates"] = [{"topic": name, "share": round(share, 2)} for share, name in ranked[:3]]
    tie = len(ranked) > 1 and ranked[0][0] == ranked[1][0]
    if s["home_guess"] is None and ranked and not tie and ranked[0][0] >= HOME_SHARE:
        s["home_guess"] = ranked[0][1]
        s["home_shared_words"] = sorted(want & area_words[ranked[0][1]][0])      # G121


def _split(topics: list[dict], pieces_of: dict, area: str) -> None:
    """G52: each topic's pieces, held and lacking split into `own` and
    `building_marked_elsewhere` (a building piece whose sentence is marked
    for other areas only); the totals stay as they are."""
    for row in topics:
        away = {"pieces": 0, "held": 0, "lacking": 0}
        for ref in row["references"]:
            if ref["file"] not in pieces_of:
                continue
            kept, marks = pieces_of[ref["file"]]

            def elsewhere(n) -> bool:
                return n is not None and bool(areas_of(marks.get(n))) and area not in areas_of(marks.get(n))
            p = sum(1 for n in kept if elsewhere(n))
            lk = sum(1 for n in ref["lacking_numbers"] if elsewhere(n))
            away["pieces"] += p
            away["lacking"] += lk
            away["held"] += max(0, p - lk)
        row["building_marked_elsewhere"] = away
        row["own"] = {k: row[k] - away[k] for k in away}


def report_path(out_dir: Path, area_dir: Path) -> Path:
    """Where a run saves its JSON (G90): A/run_gaps.json for the default
    A/gaps; inside any other `--out` folder, so a scratch run never
    overwrites the area's report (M4)."""
    return area_dir / REPORT if _default_out(out_dir, area_dir) else out_dir / REPORT


def _comparable(result: dict) -> dict:
    """A result as --check compares it: without `out`, `note`, the files a
    run clears or would clear (compared on their own), and the advisory
    hints, which --hints alone adds. `advisory_failed` is compared (M3): a
    hint that failed then and works now, or the reverse, is a change."""
    out = {k: v for k, v in result.items()
           if k not in ("out", "note", "cleared", "would_clear", "hints")}
    out["building"] = [{**e, "sentences": [{k: v for k, v in s.items() if k not in ("hints", "hints_at")}
                                           for s in e.get("sentences", [])]}
                       for e in out.get("building", [])]
    return out


HELD_FIELDS = ("id", "topic_sentence", "verdict", "verdict_was", "verdict_why")
RULE_FIELDS = ("modal_piece", "modal_topic", "modal_differs", "home_topic", "home", "rule_sentence", "topic_hash",
               "verdict_unpinned")      # G201/G202 (1.4.39)
MODAL_FIELDS = ("modal_piece_all", "modal_sentence", "modal_topic_implied", "nearest_modal_sentence",
                "rule_is_topic_sentence", "counted")      # 1.4.40 (G223, G227, L28)
NEW_LISTS = ("lacking_pieces", "home_lacking", "r9_lacking", "hand_lacks", "non_home_lacking",
             "topic_totals", "short_not_owed", "hand_holds")       # 1.4.40 (G225), gapfix13 (1.4.42): a list an older report has no key for
SHORT_FIELDS = ("id", "counted", "verdict", "why", "verdict_was", "verdict_why")      # 1.4.40 (G225)


def _older_held(was: dict, now: dict, new_keys: list) -> None:
    """G159 (1.4.37): a report saved before held_by_wording rows carried
    HELD_FIELDS is compared on the fields it has; each field the fresh rows
    add is listed in `new_keys`, never a change (1.4.34, review M3). A row
    added or dropped is still a change."""
    for key in NEW_LISTS + ("measured_total", "skill_version", "missing_subjects"):      # 1.4.40: a key an older report lacks is new, never a change
        if key not in was and key in now:
            now.pop(key)
            new_keys.append(key)
    old = was.get("lacking_pieces")      # gapfix13 (1.4.42, G254): `counted_at` on a piece marked elsewhere
    if isinstance(old, list) and not any(isinstance(r, dict) and "counted_at" in r for r in old):
        rows = now.get("lacking_pieces") or []
        if any(isinstance(r, dict) and "counted_at" in r for r in rows):
            new_keys.append("lacking_pieces.counted_at")
            now["lacking_pieces"] = [{k: v for k, v in r.items() if k != "counted_at"} if isinstance(r, dict)
                                     else r for r in rows]
    old = was.get("short_sentences")
    if isinstance(old, list) and not any(isinstance(r, dict) and "id" in r for r in old):
        rows = now.get("short_sentences") or []
        if any(isinstance(r, dict) and k in r for r in rows for k in SHORT_FIELDS):
            new_keys.extend(f"short_sentences.{k}" for k in SHORT_FIELDS
                            if any(isinstance(r, dict) and k in r for r in rows))
            now["short_sentences"] = [{k: v for k, v in r.items() if k not in SHORT_FIELDS} if isinstance(r, dict)
                                      else r for r in rows]
    old = was.get("held_by_wording")
    if not isinstance(old, list):
        return
    for fields, marker in ((HELD_FIELDS, "topic_sentence"), (RULE_FIELDS, "topic_hash"),
                           (MODAL_FIELDS, "modal_sentence"),    # G202 (1.4.39), 1.4.40 too
                           (("rule_at",), "rule_at"),            # gapfix13 (G260, 1.4.42)
                           (("rule_severity",), "rule_severity")):  # gapfix14 (G279, 1.4.43)
        if any(isinstance(r, dict) and marker in r for r in old):
            continue
        rows = now.get("held_by_wording") or []
        added = sorted({k for r in rows if isinstance(r, dict) for k in fields if k in r})
        now["held_by_wording"] = [{k: v for k, v in r.items() if k not in fields} if isinstance(r, dict) else r
                                  for r in rows]
        new_keys.extend(f"held_by_wording.{k}" for k in added)


def _kind_changed(found: list[dict]) -> None:
    """G180 (1.4.37): a short_sentences change whose kind changed says so:
    `kind_changed` [old, new] on a `.kind` change, and on each added row whose
    removed twin (same speciality, n and text) had another kind."""
    for c in found:
        if not c["path"].startswith("short_sentences"):
            continue
        if c["path"].endswith(".kind") and "was" in c:
            c["kind_changed"] = [c["was"], c["now"]]
        elif "added" in c:
            gone = {(r.get("speciality"), r.get("n"), r.get("text")): r.get("kind")
                    for r in c["removed"] if isinstance(r, dict)}
            c["added"] = [{**r, "kind_changed": [gone[k], r.get("kind")]}
                          if isinstance(r, dict) and (k := (r.get("speciality"), r.get("n"), r.get("text"))) in gone
                          and gone[k] != r.get("kind") else r for r in c["added"]]


def check(area: str, workspace: Path, repo: Path, out_dir: Path, cookr_py: str, cli: Path | None,
          hints: bool | None = False, devteam: Path | None = None) -> tuple[dict, int]:
    """G45, G67: a fresh measure (into a scratch folder) compared with the
    saved report (`report_path`: A/run_gaps.json, or DIR/run_gaps.json under
    `--out DIR`, R2-N-1; every key, so no --out run is needed; a missing one
    is a change) and with the saved gaps files; any file it
    would clear is a change too. Writes nothing. Exit 0 unchanged, 1
    changed, 2 failed or any `unplaced` row, new or unchanged (N-A).
    G96 (1.4.33): `hints` None (no --hints or --no-hints) runs as the saved
    report ran (its `hints`; False when it records none), `hints_from`
    "report"; a flag given is `hints_from` "flag". 1.4.34 (review M3): a key
    the saved report lacks whose fresh value is empty is no change, listed
    in `new_keys` (unmeasured.changes); a non-empty one is a change."""
    rp = report_path(out_dir, workspace / "areas" / area)
    hints_from = "flag" if hints is not None else "report"
    if hints is None:
        try:
            recorded = json.loads(rp.read_text(encoding="utf-8")).get("hints")
        except (OSError, ValueError, AttributeError):
            recorded = None
        hints = recorded is True
    saved, _ = run(area, workspace, repo, out_dir, cookr_py, cli, hints, mode="saved", devteam=devteam)
    with tempfile.TemporaryDirectory(prefix="run_gaps-check-") as tmp:
        fresh, code = run(area, workspace, repo, out_dir, cookr_py, cli, hints, mode="fresh",
                          scratch=Path(tmp), devteam=devteam)
    not_compared, new_keys = [], []          # 1.4.34, review M3: empty keys the saved report lacks
    try:
        report = json.loads(rp.read_text(encoding="utf-8"))
        was, now = _comparable(report), _comparable(fresh)
        _older_held(was, now, new_keys)
        if isinstance(report, dict) and report.get("hints") is not hints:     # R-M-2
            was.pop("advisory_failed", None)
            now.pop("advisory_failed", None)
            then = {True: "ran with --hints", False: "ran without --hints"}.get(
                report.get("hints"), "does not record --hints")
            not_compared.append(f"advisory_failed: the saved report {then}, this check "
                                f"{'with' if hints else 'without'}")
        found = changes(was, now, new_keys=new_keys)
    except FileNotFoundError:
        found = [{"path": "run_gaps.json", "was": None, "now": "missing"}]
    except (OSError, ValueError, AttributeError) as e:
        found = [{"path": "run_gaps.json", "was": None, "now": f"unreadable: {e.__class__.__name__}: {e}"}]
    paths = {c["path"] for c in found}
    found += [c for c in changes(_comparable(saved), _comparable(fresh)) if c["path"] not in paths]
    _kind_changed(found)
    if fresh["would_clear"]:
        found.append({"path": "would_clear", "was": [], "now": fresh["would_clear"]})
    if fresh["r9_stale"] and not any(c["path"].split("[")[0] == "r9_stale" for c in found):    # G94: once
        found.append({"path": "r9_stale", "was": [], "now": [r["file"] for r in fresh["r9_stale"]]})
    if fresh["stale_reference"] and not any(                                # R-I-1; R2-N-2: once
            c["path"].split("[")[0].split(".")[0] == "stale_reference" for c in found):
        found.append({"path": "stale_reference", "was": [],
                      "now": [r["speciality"] for r in fresh["stale_reference"]]})
    try:
        saved_total = report.get("measured_total", sum(t["own"]["lacking"] for t in report["topics"]))
    except (NameError, KeyError, TypeError, AttributeError):
        saved_total = None
        report = {}
    gap_total = gap_totals(workspace / "areas" / area / "area-plan.md", fresh["measured_total"], saved_total)
    changed_verdicts = verdict_changes(report if isinstance(report, dict) else {}, fresh)
    counted = counted_rows(fresh, workspace / "areas" / area)
    differ = counted_rows_differ(fresh, counted)
    figure = figure_change(gap_total, fresh["measured_total"], counted, changed_verdicts)
    newer = {k.split(".", 1)[1] for k in new_keys if k.startswith("held_by_wording.")}
    if not any(isinstance(r, dict) and "rule_severity" in r for r in (report or {}).get("held_by_wording") or []):
        newer.add("rule_severity")                     # 1.4.43 added it: an older report is new, not missing
    missing = missing_fields(fresh["held_by_wording"], "fresh") + missing_fields(
        (report or {}).get("held_by_wording") if isinstance(report, dict) else [], "saved", newer)
    return ({"area": area, "check": "changed" if found else "unchanged", "out": str(out_dir),
             "report": str(rp), "would_clear": fresh["would_clear"], "failed": fresh["failed"],
             "unplaced": fresh["unplaced"], "stale_reference": fresh["stale_reference"],
             "r9_stale": fresh["r9_stale"], "hints": hints, "hints_from": hints_from, "gap_total": gap_total,
             "measured_total": fresh["measured_total"], "missing_subjects": fresh["missing_subjects"],
             "saved_total": saved_total,
             "verdict_changes": changed_verdicts, "counted_rows": counted, "counted_rows_differ": differ,
             "counted_with_prior_verdict": figure["counted_with_prior_verdict"],
             "counted_never_judged": figure["counted_never_judged"], "figure_change": figure,
             **({"not_compared": not_compared} if not_compared else {}),
             **({"new_keys": sorted(set(new_keys))} if new_keys else {}),
             **({"missing_fields": missing} if missing else {}), "changes": found},
            2 if code or missing else (1 if found else 0))     # N-A: code is 2 on any unplaced row, new or not


REQUIRED_ROW_FIELDS = ("id", "modal_piece", "modal_piece_all", "modal_sentence", "modal_topic", "modal_topic_implied",
                       "modal_differs", "rule_sentence", "rule_at", "rule_severity", "nearest_modal_sentence",
                       "rule_is_topic_sentence", "topic_hash", "home_topic", "home", "counted")    # gapfix14 (G279)


def missing_fields(rows, where: str, skip: set | frozenset = frozenset()) -> list[dict]:
    """gapfix14 (G279, 1.4.43): each held_by_wording row lacking a field of REQUIRED_ROW_FIELDS (a field an older
    report never had, `skip`, is a new key, not missing): {id, missing, in}."""
    out = []
    for r in rows if isinstance(rows, list) else []:
        if isinstance(r, dict):
            gone = [k for k in REQUIRED_ROW_FIELDS if k not in r and k not in skip]
            if gone:
                out.append({"id": r.get("id"), "missing": gone, "in": where})
    return out


def counted_rows(result: dict, a: Path) -> list[dict]:
    """gapfix13 (1.4.42, G257): each row `measured_total` counts, with the
    last verdict A/held.json records for its id (kept even when it reset)
    and its `verdict_was`, each `none` when there is none: {id,
    last_verdict, verdict_was}. The jump from an old stated figure is the
    rows judged before (`counted_with_prior_verdict`) and those never
    judged (`counted_never_judged`)."""
    try:
        saved = json.loads((a / HELD).read_text(encoding="utf-8"))
        saved = saved if isinstance(saved, dict) else {}
    except (OSError, ValueError):
        saved = {}
    rows = [r for r in result.get("held_by_wording") or []
            if r.get("verdict") == "not" or ("verdict_was" in r and "verdict" not in r)]
    rows += [r for r in result.get("lacking_pieces") or [] if r.get("counted", True) and r.get("verdict") != "held"]
    rows += [r for r in result.get("short_sentences") or [] if r.get("counted", True) and r.get("verdict") == "not"]
    rows += [r for k in ("home_lacking", "r9_lacking", "hand_lacks") for r in result.get(k) or [] if _open(r)]
    out = []
    for r in rows:
        v = saved.get(r.get("id"))
        out.append({"id": r.get("id"), "last_verdict": v.get("verdict", "none") if isinstance(v, dict) else "none",
                    "verdict_was": r.get("verdict_was", "none")})
    return out
_KINDS = ("held_by_wording", "lacking_pieces", "short_sentences", "home_lacking", "r9_lacking", "hand_lacks")


def figure_change(gap_total: list[dict], measured: int, counted: list[dict], changes: list[dict]) -> dict:
    """gapfix14 (1.4.43, G300): the plan's stated figure, the measured one, their difference and what explains it:
    the counted rows judged before, those never judged, and the verdict changes (their count and summed
    total_delta). `stated` is the plan's figure line (a `form: figure` row, else another form's number), the
    measured figure when no row differs, None when the plan states none."""
    rows = [r for r in gap_total or [] if isinstance(r, dict)]
    stated = next((r.get("stated") for r in rows if r.get("form") == "figure"), None)
    if stated is None:
        stated = next((r.get("stated") for r in rows if r.get("stated") is not None), None)
    if stated is None and not any(r.get("form") == "missing" for r in rows) and not rows:
        stated = measured
    return {"stated": stated, "measured": measured,
            "difference": None if stated is None else measured - stated,
            "counted_with_prior_verdict": sum(1 for r in counted if r["last_verdict"] != "none"
                                              or r["verdict_was"] != "none"),
            "counted_never_judged": sum(1 for r in counted if r["last_verdict"] == "none"
                                        and r["verdict_was"] == "none"),
            "verdict_changes": len(changes), "verdict_changes_delta": sum(r.get("total_delta", 0) for r in changes)}


def counted_rows_differ(result: dict, counted: list[dict]) -> list[dict]:
    """gapfix14 (1.4.43, G283): every row behind a difference between `counted_rows` and `measured_total`:
    {id, topic, why}. A listed row that moves no figure: a `not` (or reset) held_by_wording row whose sentence is
    marked for other areas only, whose home holds it (`counted` false), or whose topic is a home-measure topic (its
    home_lacking row counts it). A topic whose total exceeds its listed rows: {id null, topic, why}. With these,
    len(counted_rows) - (rows with an id) + (the topics' excess) == measured_total."""
    rows = {r.get("id"): (k, r) for k in _KINDS for r in result.get(k) or [] if isinstance(r, dict)}
    measured = {t.get("topic") for t in result.get("topics") or []}
    out, listed = [], {}
    for c in counted:
        kind, r = rows.get(c.get("id"), (None, {}))
        why = None
        if kind == "held_by_wording":
            named = _named(r.get("marked_for"))
            if named and result.get("area") not in named:
                why = (f"its sentence is marked for another area only ({', '.join(sorted(named))}): its `not` "
                       "counts there, never here")
            elif r.get("counted") is False:
                why = "counted false: the sentence's home holds it (G284b), so its `not` moves no figure here"
            elif r.get("topic") not in measured:
                why = (f"topic {r.get('topic')} is a home-measure topic: the sentence's home_lacking row is "
                       "the one counted")
        if why:
            out.append({"id": c.get("id"), "topic": r.get("topic"), "why": why})
        else:
            t = r.get("topic") or "(no topic)"
            listed[t] = listed.get(t, 0) + 1
    for t in topic_totals(result):
        extra = t["total"] - listed.get(t["topic"], 0)
        if extra:
            out.append({"id": None, "topic": t["topic"], "why": f"topic total {t['total']}, {listed.get(t['topic'], 0)} "
                        f"counted row(s) listed: {extra:+d} with no row of its own"})
    return out


HOLDS = "hand_holds.json"     # gapfix14 (1.4.43, G276): mark.py --hold
_COUNTED_AT = re.compile(r"\b(?:counted at|the owner is)\s+`?([a-z0-9][\w-]*(?:/[\w-]+)+)", re.I)


def verdict_counted_at(v) -> str | None:
    """gapfix14 (1.4.43, G273 a): the area a non-owner `held` verdict says the
    sentence is counted at: its `counted_at` (mark.py --held ... --counted-at
    AREA), else an older free-text why's "counted at <area>" or "the owner is
    <area>"; None for any other verdict."""
    if not isinstance(v, dict) or v.get("verdict") != "held":
        return None
    if isinstance(v.get("counted_at"), str) and v["counted_at"]:
        return v["counted_at"]
    m = _COUNTED_AT.search(str(v.get("why") or ""))
    return m.group(1).rstrip(".") if m else None


def hand_holds(a: Path) -> list[dict]:
    """gapfix14 (1.4.43, G276): each hand hold `mark.py --hold` recorded in
    A/hand_holds.json: {id (`hold:<speciality>:<n>@<topic>[#k]`), speciality,
    n, topic, text, source, why}: the plan's `held` verdict for that sentence
    at that topic (a home no speciality measures, most often). Never counted;
    read as the home's verdict by non_home_lacking and --check-homes."""
    try:
        saved = json.loads((a / HOLDS).read_text(encoding="utf-8"))
        saved = saved if isinstance(saved, dict) else {}
    except (OSError, ValueError):
        saved = {}
    return [{"id": rid, "speciality": v.get("speciality"), "n": v.get("n"), "topic": v.get("topic"),
             "text": v.get("text"), "source": v.get("source"), "why": v.get("why")}
            for rid, v in saved.items() if isinstance(v, dict)]


def held_at_home(result: dict, sp, n, topic) -> str | None:
    """gapfix14 (1.4.43, G276, G277): the id of a hold of sentence (sp, n) at
    `topic` in this area's report, else None: a hand hold, a held_by_wording
    row standing held (no `not`, not reset), a lacking or home row judged
    `held`, or a home measure or measured topic holding it."""
    same = lambda r: isinstance(r, dict) and (r.get("speciality"), r.get("n"), r.get("topic")) == (sp, n, topic)
    for r in result.get("hand_holds") or []:
        if same(r):
            return r["id"]
    for r in result.get("held_by_wording") or []:
        if same(r) and r.get("verdict") != "not" and not ("verdict_was" in r and "verdict" not in r):
            return r.get("id") or f"{sp}:{n}@{topic}"
    for key in ("lacking_pieces", "home_lacking", "r9_lacking"):
        for r in result.get(key) or []:
            if same(r) and r.get("verdict") == "held":
                return r.get("id")
    for h in result.get("home_measures") or []:
        if h.get("topic") == topic and any((x.get("speciality"), x.get("n"), x.get("verdict")) == (sp, n, "held")
                                           for x in h.get("sentences") or []):
            return f"home_measures:{sp}:{n}@{topic}"
    for b in result.get("building") or []:
        if b.get("speciality") == sp:
            for x in b.get("sentences") or []:
                if x.get("n") == n and topic in (x.get("held_at") or []):
                    return f"held_at:{sp}:{n}@{topic}"
    return None


def home_verdict(result: dict, sp, n, topic) -> dict | None:
    """gapfix14 (1.4.43, G273 b, G276): this area's verdict on sentence (sp,
    n) at `topic`: {id, verdict} -- `held` (held_at_home), else `lacking` (a
    lacking, home, R9 or hand row there standing, or a held_by_wording row
    judged `not` or reset); None when the area has neither."""
    hold = held_at_home(result, sp, n, topic)
    if hold:
        return {"id": hold, "verdict": "held"}
    same = lambda r: isinstance(r, dict) and (r.get("speciality"), r.get("n"), r.get("topic")) == (sp, n, topic)
    for r in result.get("held_by_wording") or []:
        if same(r):
            return {"id": r.get("id"), "verdict": "lacking"}
    for key in ("home_lacking", "lacking_pieces", "r9_lacking", "hand_lacks"):
        for r in result.get(key) or []:
            if same(r):
                return {"id": r.get("id"), "verdict": "lacking"}
    return None


def _home_record(area: str, rec: str) -> tuple[str, str]:
    """A recorded home as (owner area, topic): a bare topic is the recording area's."""
    where, _, topic = rec.rpartition(":")
    return (where or area, topic)


def saved_reports(workspace: Path) -> dict[str, tuple[dict, Path, dict]]:
    """gapfix14 (1.4.43): every area's saved A/run_gaps.json (a gaps folder's
    own skipped), its rows rebuilt from the area's held.json, hand_lacks.json,
    hand_holds.json and recorded homes as a run builds them: {area: (report,
    A, recorded homes)}. Read-only; an unreadable report is left out."""
    root = workspace / "areas"
    out = {}
    for rp in sorted(root.glob("**/run_gaps.json")) if root.is_dir() else []:
        if "gaps" in rp.relative_to(root).parts[:-1]:
            continue
        a = rp.parent
        area = a.relative_to(root).as_posix()
        try:
            report = json.loads(rp.read_text(encoding="utf-8"))
            if not isinstance(report, dict):
                continue
        except (OSError, ValueError):
            continue
        report["area"] = area
        report.setdefault("topics", [])
        homes = recorded_homes(a)
        report["hand_holds"] = hand_holds(a)
        _home_rows(report, homes)
        _hand_rows(report, a)
        report.setdefault("r9_lacking", [])
        _judge_new_rows(report, a)
        out[area] = (report, a, homes)
    return out


_ROW_KEYS = ("held_by_wording", "lacking_pieces", "short_sentences", "home_lacking", "r9_lacking", "hand_lacks")


_VERDICT_PREFIXES = ("lacking:", "short:", "home:", "hand:", "hold:")


def verdict_key(rid: str) -> tuple[str, str] | None:
    """gapfix14 (G280 c): (piece, topic) of a verdict id: `<speciality>:<n>[#k]` and the topic its `@` names (an
    `r9:<name>:...` id: <name>); None for an id naming no topic (a short row)."""
    if rid.startswith("r9:"):
        parts = rid.split(":")
        return (":".join(parts[2:]), parts[1]) if len(parts) >= 4 else None
    for pre in _VERDICT_PREFIXES:
        if rid.startswith(pre):
            rid = rid[len(pre):]
            break
    left, at, topic = rid.rpartition("@")
    if not at or ":" not in left:
        return None
    if "#" in topic:                     # a `#k` after the topic belongs to the piece
        topic, _, k = topic.partition("#")
        left = f"{left}#{k}"
    return left, topic.rpartition(":")[2]


def id_kind(rid: str) -> str:
    """gapfix15 (G303): the kind of a verdict id: `plain` (`<spec>:<n>@<topic>`), or its prefix (`lacking`,
    `short`, `home`, `hand`, `hold`, `r9`). Rows of different kinds are different ids and never compared."""
    for pre in ("r9", *(p.rstrip(":") for p in _VERDICT_PREFIXES)):
        if rid.startswith(pre + ":"):
            return pre
    return "plain"


def check_verdicts(workspace: Path, area: str | None = None) -> list[dict]:
    """gapfix14 (1.4.43, G280 c): read-only, the whole workspace: each piece
    judged at one topic in two areas or more with different verdicts (every
    A/held.json, and A/hand_holds.json as `held`), leaving out a hold whose
    `counted_at`, or older why ("counted at <area>", "the owner is <area>"),
    names the area counting it (G273 a: held here by design, counted there). Each row {piece, topic, verdicts: [{area, id, verdict,
    why}]}, sorted; with `area`, the rows it has a verdict in."""
    base = workspace / "areas"
    seen: dict[tuple, list[dict]] = {}
    for f in sorted(list(base.rglob(HELD)) + list(base.rglob(HOLDS))):
        try:
            data = json.loads(f.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            continue
        name = f.parent.relative_to(base).as_posix()
        for rid, v in (data.items() if isinstance(data, dict) else ()):
            if not isinstance(v, dict):
                continue
            verdict = "held" if f.name == HOLDS else v.get("verdict")
            key = verdict_key(rid)
            key = key and (*key, id_kind(rid))       # G303: compare within one id kind only
            if key is None or verdict not in ("held", "not") or (f.name == HELD and verdict_counted_at(v)):
                continue      # a hold counted at another area, structured or in an older why (G273 a)
            seen.setdefault(key, []).append({"area": name, "id": rid, "verdict": verdict,
                                             "why": str(v.get("why") or "")})
    rows = []
    for (piece, topic, kind), vs in sorted(seen.items()):
        if len({v["area"] for v in vs}) > 1 and len({v["verdict"] for v in vs}) > 1 and (
                area is None or any(v["area"] == area for v in vs)):
            rows.append({"piece": piece, "topic": topic, "kind": kind, "verdicts": vs})
    return rows


def check_homes(workspace: Path, area: str | None = None) -> list[dict]:
    """gapfix13 (1.4.42, G254 c); gapfix14 (1.4.43, G273, G277, G282, G289):
    the home sentences of every area's saved A/run_gaps.json that are a real
    problem, read-only. A sentence's owner is the area its recorded home
    names (a bare topic: the recording area's), else the area that measured
    it at its home; its home topic is the recorded one (it wins over a
    word-match topic, G277), else the measured one. The owner's verdict there
    (`home_verdict`: a hold, a hand hold too, or a lack) decides: a sentence
    held at its home is never listed. A lacking one, or one no verdict
    judges, is listed when counted in no area (`counted_nowhere`, a sentence
    measured lacking at a home only) or in more than one (`counted_twice`).
    Two areas recording different homes for one sentence is its own row
    (`home_conflict`, the owner's record first). Each row: {speciality, n,
    kind, owner, home_topic, measured_in, owner_verdict {id, verdict}, counting
    {area: [row ids]}, why} (a conflict: records instead of counting). With
    `area`, only rows touching it (its owner, measurer, a counting area or a
    record's)."""
    reports = saved_reports(workspace)
    records: dict[tuple, list[dict]] = {}
    measured: dict[tuple, tuple[str, str]] = {}
    hand: dict[tuple, tuple[str, str]] = {}
    counting: dict[tuple, dict[str, list[str]]] = {}
    for name, (report, a, homes) in reports.items():
        for key, rec in sorted(homes.items(), key=lambda kv: (str(kv[0][0]), str(kv[0][1]))):
            if isinstance(rec, str) and rec:
                records.setdefault(key, []).append({"area": name, "home": rec})
        for r in report.get("home_lacking") or []:
            measured.setdefault((r["speciality"], r["n"]), (name, r["topic"]))
        for k in ("hand_holds", "hand_lacks"):
            for r in report.get(k) or []:
                hand.setdefault((r["speciality"], r["n"]), (name, r["topic"]))
        by_id = {r.get("id"): r for k in _ROW_KEYS for r in report.get(k) or [] if isinstance(r, dict)}
        for c in counted_rows(report, a):
            r = by_id.get(c["id"]) or {}
            counting.setdefault((r.get("speciality"), r.get("n")), {}).setdefault(name, []).append(c["id"])
    out = []
    for key in sorted(set(records) | set(measured) | set(hand), key=lambda k: (str(k[0]), str(k[1]))):
        sp, n = key
        recs = records.get(key, [])
        norm = [_home_record(r["area"], r["home"]) for r in recs]
        if norm:
            owners = [o for o, _ in norm]
            owner = max(sorted(set(owners)), key=owners.count)
            mine = [r for r, (o, _) in zip(recs, norm) if o == owner]
            first = next((r for r in mine if r["area"] == owner), mine[0])
            topic = _home_record(first["area"], first["home"])[1]
        else:
            owner, topic = measured.get(key) or hand[key]
            first = None
        rows = []
        if len(set(norm)) > 1:
            rest = [r for r in recs if r is not first]
            rows.append({"speciality": sp, "n": n, "kind": "home_conflict", "owner": owner, "home_topic": topic,
                         "records": [first, *rest],
                         "why": f"{len(set(norm))} homes recorded for one sentence: keep the owner's ({owner}:"
                                f"{topic}) and record it in each other area with mark.py --area <area> "
                                f"--speciality {sp} --home {n}={owner}:{topic}"})
        report = reports.get(owner, ({},))[0]
        verdict = home_verdict(report, sp, n, topic) or {"id": None, "verdict": "unjudged"}
        where = counting.get(key, {})
        listed = verdict["verdict"] == "lacking" and len(where) != 1 or \
            verdict["verdict"] == "unjudged" and (len(where) > 1 or not where and key in measured)
        if listed:
            kind = "counted_nowhere" if not where else "counted_twice"
            vid = verdict["id"]
            if not where and verdict["verdict"] == "lacking":
                why = (f"lacking at its home {owner}:{topic} ({vid}) and counted in no area: re-run run_gaps.py "
                       f"--area {owner}, and if it is still uncounted judge {vid} not --why ... there (G255)")
            elif not where:
                why = (f"measured lacking, no verdict at its home {owner}:{topic} and counted in no area: judge it "
                       f"there: mark.py --area {owner} --hold {topic} --source <reference>#{n} --text ... --why "
                       f"... if the topic holds it, else --lack {topic} ... (G276, G253)")
            else:
                others = [(x, ids) for x, ids in sorted(where.items()) if x != owner]
                keep = owner if owner in where else sorted(where)[0]
                why = (f"counted in {len(where)} areas ({', '.join(sorted(where))}): {keep} keeps its count; "
                       + "; ".join(f"in {x} judge {i} held: mark.py --area {x} --held {i} held --why \"counted at "
                                   f"{owner}\" --counted-at {owner}" for x, ids in others if x != keep for i in ids)
                       + (" (no verdict at the home yet: judge it there first)" if verdict["verdict"] == "unjudged"
                          else ""))
            rows.append({"speciality": sp, "n": n, "kind": kind, "owner": owner, "home_topic": topic,
                         "measured_in": (measured.get(key) or (None,))[0], "owner_verdict": verdict,
                         "counting": {x: ids for x, ids in sorted(where.items())}, "why": why})
        for row in rows:
            touch = {row["owner"], row.get("measured_in"), *row.get("counting", {}),
                     *(r["area"] for r in row.get("records", []))}
            if area is None or area in touch:
                out.append(row)
    return out


# gapfix14 (G294): a line states a figure only when the phrase is followed by a number (bold and a colon between
# allowed, and a parenthetical such as `(by hand)`, G259); prose naming this area's gaps with no number after it is
# never read as one.
_GAP_LINE = re.compile(r"This area['\u2019]s gaps\b(?:\s*\([^)\n]*\))?(?:\*\*)?\s*:?\s*(?:\*\*)?\s*\d", re.I)
_GAP_STRICT = re.compile(r"^(?:[-*+]\s+)?(?:\*\*)?This area['\u2019]s gaps:(?:\*\*)?\s*(\d+)(?:\*\*)?\.?$")
# gapfix13 (G259, 1.4.42): the accepted form, quoted by every row and by stage-1.md step 3.
GAP_FORM = ("`This area's gaps: N` on a line of its own, N a number; allowed: a leading list dash, bold around "
            "the label (`**This area's gaps:** N`), around the whole line (`**This area's gaps: N**`) or around N, "
            "and a final full stop")
_QUOTED = re.compile(r"`[^`]*`|\"[^\"]*\"|\u201c[^\u201d]*\u201d")


def gap_totals(plan: Path, counted: int, saved: int | None) -> list[dict]:
    """G189 (1.4.39); 1.4.40 (G225, G226, G233, L15): the plan states its gap
    total in one form, `This area's gaps: N` (bold and a final full stop
    allowed), N being `measured_total`: the lacking pieces after every
    recorded verdict. A row for each line stating another N (`form`
    "figure"), each `This area's gaps` line in any other form ("other": a
    parenthesis, a "by hand" term, a changed wording), and, when the area has
    lacking pieces, a plan with no such line ("missing"). The Step-4 re-check
    section, a `>` quote and a backticked or quoted span are skipped (they
    quote the form). Advisory: never changes the exit."""
    try:
        text = plan.read_text(encoding="utf-8")
    except OSError:
        return []
    rows, found, skip = [], False, None
    for line in text.splitlines():
        head = re.match(r"^(#{1,6})\s+(.*)$", line)
        if head:
            level = len(head.group(1))
            if skip is not None and level <= skip:
                skip = None
            if skip is None and re.search(r"re-?check", head.group(2), re.I):
                skip = level
            continue
        if skip is not None or line.lstrip().startswith(">"):
            continue
        bare = _QUOTED.sub("", line)
        if not _GAP_LINE.search(bare):
            continue
        found = True
        strict = _GAP_STRICT.match(bare.strip())
        gave = re.search(r"gaps:?(?:\*\*)?\s*(\d+)", bare)
        stated = int(strict.group(1)) if strict else (int(gave.group(1)) if gave else None)
        if strict and stated == counted:
            continue
        base = {"stated": stated, "counted": counted, "saved": saved, "line": line.strip()}
        if not strict:
            rows.append({**base, "form": "other",
                         "why": f"the line `{line.strip()}` names this area's gaps followed by a number, so it "
                                "states a figure (G294), and is not in the accepted form, "
                                f"{GAP_FORM}: write the "
                                f"measured total {counted} in that form alone; any other line giving this "
                                "area's gaps a number is flagged (prose without one is not); a judgment that moves it is recorded with "
                                "mark.py --held ... --why, never written beside the figure (G225)"})
        else:
            rows.append({**base, "form": "figure",
                         "why": f"the plan states {stated}, run_gaps.py's measured total is {counted} (lacking "
                                f"pieces after every recorded verdict; the saved report "
                                f"{saved if saved is not None else 'unreadable'}): write {counted}, or record the "
                                "judgment that makes it differ with mark.py --held ... --why"})
    if not found and counted:
        rows.append({"stated": None, "counted": counted, "saved": saved, "line": None, "form": "missing",
                     "why": f"the plan has no `This area's gaps: N` line and run_gaps.py counts {counted} lacking "
                            f"piece(s): write `This area's gaps: {counted}` (0 is the line of an empty area)"})
    return rows


def _delta(kind: str, row: dict, verdict: str | None, area: str) -> int:
    """What `verdict` adds to `measured_total` for a row of list `kind`."""
    if kind == "lacking_pieces":
        return -1 if verdict == "held" and row.get("counted", True) else 0
    if kind == "short_sentences":
        return 1 if verdict == "not" and row.get("counted", True) else 0
    if kind in ("home_lacking", "r9_lacking", "hand_lacks"):      # gapfix13 (1.4.42)
        return -1 if verdict == "held" and (row.get("counted", True) or row.get("held_out")) else 0
    named = _named(row.get("marked_for"))
    return 1 if verdict == "not" and not (named and area not in named) else 0


def verdict_changes(saved: dict, fresh: dict) -> list[dict]:
    """1.4.40 (G247): each row id whose recorded verdict differs between the
    saved report and a fresh measure, with what it did to `measured_total`:
    {id, kind, was, now, total_delta}; a change that moves no figure is
    listed too (delta 0)."""
    out = []
    for kind in ("held_by_wording", "lacking_pieces", "short_sentences", "home_lacking", "r9_lacking", "hand_lacks"):
        was = {r.get("id"): r for r in (saved.get(kind) or []) if isinstance(r, dict)}
        now = {r.get("id"): r for r in (fresh.get(kind) or []) if isinstance(r, dict)}
        for rid in [*now, *[i for i in was if i not in now]]:
            w, n = was.get(rid), now.get(rid)
            wv, nv = (w or {}).get("verdict"), (n or {}).get("verdict")
            if wv != nv:
                out.append({"id": rid, "kind": kind, "was": wv, "now": nv,
                            "total_delta": _delta(kind, n or {}, nv, fresh["area"]) -
                            _delta(kind, w or {}, wv, fresh["area"])})
    return out


def digest(result: dict, code: int, checked: bool, saved: bool = False, gap_rows: list | None = None) -> str:
    """G120 (1.4.33): the line the plan's Step-4 re-check records: the verdict
    (--check), the exit, the count of every list the output holds (`not_compared`
    0 when absent), the hints setting and the saved report's git blob hash
    ("-" when no report is saved), so a later check is compared with it. A run
    (not --check) adds a line per topic: its short_sentences rows, its
    home_measures rows and the building sentences whose first lacking
    candidate it is (L27)."""
    lists = {k: len(v) for k, v in result.items() if isinstance(v, list) and k != "gap_total"}
    rows = result.get("gap_total") if gap_rows is None else gap_rows
    if rows is not None:      # 1.4.40 (L16): the plan's gap-total rows, then the measured total they compare with
        lists["gap_total_rows"] = len(rows)
    if isinstance(result.get("measured_total"), int):
        lists["measured_total"] = result["measured_total"]
    if isinstance(result.get("missing_subjects"), int):      # gapfix14 (G286): beside it, never in it
        lists["missing_subjects"] = result["missing_subjects"]
    if checked:
        lists.setdefault("not_compared", 0)
        for k in ("counted_with_prior_verdict", "counted_never_judged"):      # gapfix13 (G257)
            if isinstance(result.get(k), int):
                lists[k] = result[k]
    fig = result.get("figure_change")
    if checked and isinstance(fig, dict) and fig.get("stated") is not None:      # gapfix14 (G300)
        lists["stated"] = (f"{fig['stated']} -> measured {fig['measured']} ({fig['difference']:+d}: "
                           f"counted_with_prior_verdict {fig['counted_with_prior_verdict']}, counted_never_judged "
                           f"{fig['counted_never_judged']}, verdict_changes {fig['verdict_changes']})")
    differ = result.get("counted_rows_differ")
    if checked and isinstance(differ, list) and differ:      # gapfix14 (G283): name each row behind the gap
        lists["counted_rows_differ"] = f"{len(differ)} (" + "; ".join(
            f"{r.get('id') or 'topic ' + str(r.get('topic'))}: {r.get('why')}" for r in differ) + ")"
    rp = Path(result["report"]) if result.get("report") else None
    head = (f"run_gaps.py --check {result['area']}: {result['check']}, exit {code}" if checked
            else f"run_gaps.py {result['area']}: saved report" if saved     # G122: read, never run
            else f"run_gaps.py {result['area']}: exit {code}")
    hints = "on" if result.get("hints") else "off"
    if checked:
        hints += f" ({result['hints_from']})"
    line = "; ".join([head, *(f"{k} {n}" for k, n in lists.items()), f"hints {hints}",
                      f"report {blob_hash(rp) if rp and rp.is_file() else '-'}"])
    if checked:
        return line
    # L27: a run adds one line per topic that short_sentences, home_measures or
    # a building sentence's first lacking candidate names, so no scratch script
    # is needed to read them per topic.
    per: dict[str, dict[str, int]] = {}

    def add(topic, key):
        if topic:
            per.setdefault(topic, {"short_sentences": 0, "home_measures": 0, "first_candidate": 0})[key] += 1
    for r in result.get("short_sentences", []):
        add(r.get("topic"), "short_sentences")
    for r in result.get("home_measures", []):
        add(r.get("topic"), "home_measures")
    for b in result.get("building", []):
        for x in b.get("sentences", []):
            if x.get("lacking_candidates"):
                add(x["lacking_candidates"][0]["topic"], "first_candidate")
    return "\n".join([line, *(f"  {t}: " + ", ".join(f"{k} {n}" for k, n in c.items())
                               for t, c in sorted(per.items()))])


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("area_pos", nargs="?", metavar="area", help="the area, as --area gives it (gapfix14 G299: "
                    "as unmeasured.py and copy_check.py take it)")
    ap.add_argument("--area", help="the area's path below cookbook/guidelines/ (required, except with "
                    "--check-homes or --check-verdicts, where it keeps the rows touching it)")
    ap.add_argument("--check-homes", action="store_true", help="read-only, the whole workspace: list every "
                    "sentence lacking (or unjudged) at its home and counted in no area or in more than one, and "
                    "every sentence two areas record different homes for, each row naming the owner, the home "
                    "topic, the owner's verdict and the mark.py command that settles it; a sentence its owner "
                    "holds at its home is never listed; with --area, the rows touching that area only (exit 1 if "
                    "any row, gapfix13 G254, gapfix14 G273)")
    ap.add_argument("--check-verdicts", action="store_true", help="read-only, the whole workspace: list each "
                    "piece judged at one topic with different verdicts in different areas (every held.json and "
                    "hand_holds.json), leaving out a hold whose counted_at names its counting area; with --area, the "
                    "rows it has a verdict in (exit 1 if any row, gapfix14 G280)")
    ap.add_argument("--workspace", help="default: <repo>/docs/grow-cookbook")
    ap.add_argument("--repo", help="default: the nearest cookbook at or above this directory (repo_path.py)")
    ap.add_argument("--out", help="the gaps folder (default A/gaps)")
    ap.add_argument("--cookr-py", default=sys.executable, help="default: this python ($COOKR_PY)")
    ap.add_argument("--cookr-cli", help="default: <repo>/skills/cookr/cli when it holds cookr")
    ap.add_argument("--digest", action="store_true", help="print one line instead of the JSON: the verdict, "
                    "exit, each list's count, hints and the saved report's hash, for the plan (G120)")
    ap.add_argument("--keys", "--summary", action="store_true", help="print each output key only, never dropping one: a list as {\"rows\": N} or [], a dict as its keys, a scalar as it is (json_keys.py); without --check, of the saved report, never a run (G122)")
    ap.add_argument("--rows", metavar="KEY", help="print output key KEY whole; without --check, of the saved "
                    "report (G138)")
    ap.add_argument("--check", action="store_true", help="write nothing: measure into a scratch folder and "
                    "print what changed from the saved gaps files (exit 0 unchanged, 1 changed, 2 failed or unplaced)")
    ap.add_argument("--devteam", help="the devteam whose speciality_reference.py writes a missing reference "
                    "(default: <repo>/../.., the devteam that holds the cookbook)")
    ap.add_argument("--hints", action=argparse.BooleanOptionalAction, default=None,
                    help="paraphrase hints for each sentence held at no measured topic: at its home_guess, else over "
                    "every measured topic (a run and --check: as the saved report ran unless given, G122)")
    a = ap.parse_args(argv)
    if a.area_pos and a.area and a.area_pos != a.area:
        ap.error(f"two areas: {a.area_pos} and --area {a.area}")
    a.area = a.area or a.area_pos
    try:
        repo = Path(os.path.abspath(os.path.expanduser(a.repo))) if a.repo else cookbook_repo(None, "run_gaps.py")
    except SystemExit as e:
        print(e, file=sys.stderr)
        return 2
    ws = Path(os.path.abspath(os.path.expanduser(a.workspace))) if a.workspace else repo / "docs" / "grow-cookbook"
    if a.check_homes:      # gapfix14 (G273 c, G282): --area keeps the rows touching it, and its exit covers them
        rows = check_homes(ws, a.area)
        print(json.dumps({"workspace": str(ws), **({"area": a.area} if a.area else {}), "check_homes": rows},
                         indent=2))
        return 1 if rows else 0
    if a.check_verdicts:   # gapfix14 (G280 c): one piece, one topic, two verdicts in two areas
        rows = check_verdicts(ws, a.area)
        print(json.dumps({"workspace": str(ws), **({"area": a.area} if a.area else {}), "check_verdicts": rows},
                         indent=2))
        return 1 if rows else 0
    if not a.area:
        ap.error("give --area AREA (only --check-homes and --check-verdicts go without)")
    why = check_area("run_gaps.py", ws, a.area, repo)      # G198 (1.4.39): never an empty run
    if why:
        print(why, file=sys.stderr)
        return 2
    out = Path(os.path.abspath(a.out)) if a.out else ws / "areas" / a.area / "gaps"
    cli = Path(a.cookr_cli) if a.cookr_cli else repo / "skills" / "cookr" / "cli"
    cli = cli if (cli / "cookr").is_dir() else None
    devteam = Path(os.path.abspath(os.path.expanduser(a.devteam))) if a.devteam else repo.parent.parent
    area_dir = (ws / "areas" / a.area).resolve()
    gaps_dir, where = area_dir / "gaps", out.resolve()
    if (where == area_dir or where in area_dir.parents       # R-M-1: the area, or a folder holding it
            or (area_dir in where.parents and where != gaps_dir and gaps_dir not in where.parents)):  # R2-M-1
        print(f"run_gaps.py: --out {a.out} is the area folder {area_dir}, holds it, or is inside it other "
              "than A/gaps: a run would write into the area's own files. Pass A/gaps (the default), a "
              "folder below it, or a folder outside the area", file=sys.stderr)
        return 2
    rp = report_path(out, ws / "areas" / a.area)
    if a.check and a.out and where != gaps_dir.resolve() and not rp.is_file():
        print(f"run_gaps.py: --check --out {a.out} compares {rp}, which does not exist: drop --out to check the "
              f"area's saved files, or save a run there first (run_gaps.py --area {a.area} --out {a.out}) (G172)",
              file=sys.stderr)
        return 2
    if (a.keys or a.digest or a.rows is not None) and not a.check:      # G122 (1.4.36): a view of the saved report, never a run
        try:
            saved = json.loads(rp.read_text(encoding="utf-8"))
            if not isinstance(saved, dict):
                raise ValueError("not a JSON object")
        except (OSError, ValueError) as e:
            print(f"run_gaps.py: --keys, --summary and --digest without --check print the saved {rp}, which "
                  f"cannot be read ({e.__class__.__name__}): save it first with step 1.3's run, "
                  f"run_gaps.py --area {a.area} --hints (or measure without writing: --check)", file=sys.stderr)
            return 2
        code = 2 if saved.get("failed") or saved.get("unplaced") else (1 if saved.get("stale_reference") else 0)
        newer = sorted(f.name for f in [*rp.parent.glob("building-*.json"), rp.parent / HELD, rp.parent / HOMES,
                                        rp.parent / HAND, rp.parent / HOLDS]      # gapfix14 (G291): hand files too
                       if f.is_file() and f.stat().st_mtime > rp.stat().st_mtime)
        if newer:          # G207 (1.4.39): a view of the saved report says when its inputs moved on
            print(f"run_gaps.py: read saved report, not re-run ({', '.join(newer)} newer than {rp.name}): "
                  f"refresh it with $COOKR_PY run_gaps.py --area {a.area} --workspace {ws} --repo {repo} --hints "
                  "(step 1.3), or --check to compare", file=sys.stderr)
        gap = gap_totals(ws / "areas" / a.area / "area-plan.md", _measured(saved), _measured(saved))
        if a.rows is not None:
            return _rows({**saved, "gap_total": gap}, a.rows, code)
        if a.digest:
            print(digest({**saved, "area": a.area, "report": str(rp)}, code, False, saved=True, gap_rows=gap))
        else:
            print(json.dumps(output_keys(saved), indent=2))
        return code
    hints = a.hints
    if hints is None and not a.check:      # G122: a run with no hints flag runs as the saved report ran
        try:
            hints = json.loads(rp.read_text(encoding="utf-8")).get("hints") is True
        except (OSError, ValueError, AttributeError):
            hints = False
    try:
        result, code = (check(a.area, ws, repo, out, a.cookr_py, cli, a.hints, devteam=devteam) if a.check
                        else run(a.area, ws, repo, out, a.cookr_py, cli, hints, devteam=devteam))
    except Refused as e:
        print(e, file=sys.stderr)
        return 2
    if not a.check:      # G90: a run keeps its report, a run's exit 2 too; a refusal and --check write nothing
        _write_json(report_path(out, ws / "areas" / a.area), result)
        if result["stale_reference"]:      # R2-M-4 (1.4.28): figures measured on a stale reference
            for r in result["stale_reference"]:
                print(f"run_gaps.py: stale_reference {r['speciality']}: {r['why']}", file=sys.stderr)
            code = code or 1
    if a.check and result.get("new_keys"):      # G218 (1.4.39): name what `new_keys N` counts
        print(f"run_gaps.py: new_keys: {', '.join(result['new_keys'])}", file=sys.stderr)
    if a.digest:
        if not a.check:
            result = {**result, "report": str(report_path(out, ws / "areas" / a.area))}
        gap = None if a.check else gap_totals(ws / "areas" / a.area / "area-plan.md", result["measured_total"],
                                              result["measured_total"])
        print(digest(result, code, a.check, gap_rows=gap))
        return code
    if a.rows is not None:
        return _rows(result if a.check else {**result, "gap_total": gap_totals(
            ws / "areas" / a.area / "area-plan.md", result["measured_total"], result["measured_total"])},
            a.rows, code)
    # G271 (gapfix13, 1.4.42): a check prints at most 40 rows a key; --rows prints them whole.
    print(json.dumps(output_keys(result) if a.keys else cap(result) if a.check else result, indent=2))
    return code


def _measured(report: dict) -> int | None:
    """A saved report's `measured_total`, else the sum of its topics' own.lacking (a report written before 1.4.40)."""
    try:
        return report["measured_total"] if isinstance(report.get("measured_total"), int) else \
            sum(t["own"]["lacking"] for t in report["topics"])
    except (KeyError, TypeError):
        return None


def _rows(result: dict, key: str, code: int) -> int:
    """G138 (1.4.36): `--rows KEY`: that key whole; 2 naming the keys when absent. L17 (1.4.40): `--rows a,b`
    prints each, in order, as stage_status.py does (json_keys.split_keys)."""
    for k in split_keys(key):
        if k not in result:
            owner = owner_of(k, "run_gaps.py")      # G220 (1.4.39)
            print(f"run_gaps.py: no output key {k!r}" + (f"; {owner}" if owner else "") +
                  f"; keys: {', '.join(result)}", file=sys.stderr)
            return 2
    print(json.dumps({k: result[k] for k in split_keys(key)}, indent=2))
    return code


if __name__ == "__main__":
    from repo_path import run_main      # gapfix13 (G263, G271)
    run_main(main)
