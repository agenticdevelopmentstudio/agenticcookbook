#!/usr/bin/env python3
"""Set building sentences' marks in a plan's marks file, validated.

    python3 mark.py <plan-area> --workspace W --repo R --speciality S --n N (--to AREA [AREA ...] | --clear)
    python3 mark.py <plan-area> --workspace W --repo R --speciality S --mark N=AREA[,AREA] [--mark ...]
    python3 mark.py <plan-area> --workspace W --repo R --speciality S --home N=TOPIC|N=AREA:TOPIC [--home ...]
    python3 mark.py <plan-area> --workspace W --repo R --held ID held|not
    python3 mark.py <plan-area> --workspace W --repo R --held-file FILE
    python3 mark.py <plan-area> --workspace W --repo R --lack TOPIC --source RELPATH#N --text SENTENCE --why WHY

The marks file is `W/areas/<plan-area>/building-<name>.json`, `<name>` the
speciality's basename (quote_building.py writes it). One `--to` area sets
the mark to that path; several set a sorted list, for a sentence spanning
areas (platform-windows 1: a UI clause and MSIX packaging), and each named
area gets the sentence in `marked_here`; `--clear` sets it to null.

`--mark N=AREA[,AREA]`, repeatable, sets many marks in one call (G70,
1.4.25): the areas after `=` as `--to` takes them, none (`N=`) clearing it.
Every mark is checked before the file is written; one bad mark writes none.

`--home N=TOPIC`, repeatable (G145, 1.4.36), records the home the plan chose
for sentence N (a topic name of this plan) in the file's `homes`, `N=`
clearing it. run_gaps.py tags that sentence's `home_unguessed` row
`home_recorded`; the row stays listed. It goes alone, without --n or --mark;
a re-quote that rewrites the file keeps `homes` only when it keeps the file
as it is (a lost home only re-lists the row untagged). G156 (1.4.37): TOPIC
must be a topic of this plan (its Proposed topics, or a folder holding
artifact.json); `N=AREA:TOPIC` records a home in another area, checked
against that area's topics, in this area's `A/homes.json` (no marks file
needed: N is checked against the saved A/run_gaps.json); run_gaps.py reads
both.

`--held ID held|not` (G159, 1.4.37) records the plan's verdict on one
`held_by_wording` row (its `id` in A/run_gaps.json) in `A/held.json`, with
the piece, the topic sentence, the rule sentence and the topic's text hash
it was judged on; run_gaps.py carries it only while all are unchanged
(G202, 1.4.39). `--held-file FILE` (G199, 1.4.39) records many in one call:
FILE is a JSON object {id: "held"|"not"}; an unknown id or verdict refuses
the whole file, naming each.

G203/G204 (1.4.39): `--home` needs `--speciality` ("give --speciality");
the same-area form `N=TOPIC` writes the building marks file's `homes`, the
cross-area form `N=AREA:TOPIC` writes A/homes.json, and a sentence holds one
home (a new one replaces the old). A home is recorded only for a sentence
the saved A/run_gaps.json lists in `home_unguessed`, the only rows
run_gaps.py tags `home_recorded`; any other sentence is refused, naming
where it is listed (`N=` clearing is never refused). `stale_homes` lists
each recorded home that names no topic (G205).

gapfix13 (1.4.42). Row ids `--held` takes (each from A/run_gaps.json, or
A/hand_lacks.json for a hand id), with the verdicts each takes:
  <speciality>:<n>@<topic>        held_by_wording: held | not (`not` moves it to lacking)
  lacking:<speciality>:<n>@<topic> lacking_pieces: held (the plan holds it; uncounted) | not (lack confirmed)
  short:<speciality>:<n>          short_sentences: not (lacking; counted) | held
  home:<speciality>:<n>@<topic>   home_lacking: held (uncounted) | not (lack confirmed)
  r9:<name>:<speciality>:<n>      r9_lacking: held (uncounted) | not (lack confirmed)
  hand:<speciality>:<n>@<topic>   hand_lacks: held (withdrawn) | not (confirmed)
Any id may end `#k` (the k-th row sharing it). `--why` (one line) is needed
for every verdict but `held` on a held_by_wording row or `not` on a short
one... and is kept with it. `--held-file FILE` is a JSON object {id: verdict}
or {id: {"verdict": V, "why": W}}. A run prints `changed` (verdict moved),
`refreshed` (same verdict, why or pin updated) and `unchanged` counts (G270).
Never edit held.json by hand (G255).

`--lack TOPIC --source RELPATH#N --text SENTENCE --why WHY` (G253) records a
lack judged by hand: sentence N of the reference RELPATH (below A, W or R;
its speciality the file's stem, `--` read as `/`), whose text must be
SENTENCE, lacking at TOPIC (a measured topic, a new topic with no folder, an
authored unmeasured topic or a home topic), in A/hand_lacks.json as
`hand:<speciality>:<n>@<topic>`. run_gaps.py counts it in measured_total and
its topic's `topic_totals` row. A sentence a measured row already holds is
refused, naming that row's id (judge that row instead).

gapfix14 (1.4.43). `--lack ... --piece K` records piece K of the sentence as
its own row (`...@<topic>#K`); a second `--lack` on an id is refused unless
`--refresh`; a wrong `--text` prints the expected sentence (G285). `--hold
TOPIC --source RELPATH#N --text SENTENCE --why WHY` records a hand hold at a
home topic in A/hand_holds.json, read as that sentence's verdict there (G276).
`--held ID held --counted-at AREA` records a non-owner hold counted at AREA
(G273); `--non-home-held` marks each non-home row whose home holds a recorded
verdict as held at that home, in one call (G284); `--clause C --cites S`,
repeatable, records a multi-clause hold clause by clause, each cited topic
sentence's modal checked (G280). A `not` needs `--why` (G288). One
`--held-file` may mix every id form. `--source` is e.g.
`reference/building--platform-windows.txt#10` (below A) (G287).

Refuses, exit 2, naming the problem and writing nothing: a marks file that
is missing, unreadable or of another speciality; an `n` with no sentence, or
one given twice; an area that is neither a folder of `R/cookbook/guidelines/`
nor a planned new area (one with `W/areas/<area>/area-plan.md`, G65). Otherwise
writes the file atomically and prints {"file", "n", "text", "was", "now"}
(`--n`) or {"file", "marks": [{"n", "text", "was", "now"}]} (`--mark`).
Stdlib only (G55, 1.4.24).
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from quote_building import _mark, known_area  # noqa: E402
from repo_path import PathHelpFormatter, add_area, area_arg  # noqa: E402

HOMES = "homes.json"      # run_gaps.HOMES
HELD = "held.json"        # run_gaps.HELD


def _refuse(why: str) -> int:
    print(f"mark.py: {why}; nothing written", file=sys.stderr)
    return 2


def _write(f: Path, data: dict) -> None:
    fd, tmp = tempfile.mkstemp(dir=f.parent, prefix=f".{f.name}.")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as out:
            json.dump(data, out, indent=2)
            out.write("\n")
        os.replace(tmp, f)
    except OSError:
        Path(tmp).unlink(missing_ok=True)
        raise


def _topics(area: str, repo: Path, workspace: Path) -> set[str]:
    """G156 (1.4.37): an area's topic names: its plan's Proposed topics rows
    and each folder of R/cookbook/guidelines/<area>/ holding artifact.json."""
    from stage_status import plan_rows      # stage_status is stdlib-only too
    root = repo / "cookbook" / "guidelines" / area
    return set(plan_rows(workspace / "areas" / area / "area-plan.md")) | (
        {p.name for p in root.iterdir() if (p / "artifact.json").is_file()} if root.is_dir() else set())


def _report_ns(a, sp: str) -> set | None:
    """The sentence numbers of speciality `sp` A/run_gaps.json names, or None when it cannot be read."""
    try:
        r = json.loads((a.workspace / "areas" / a.area / "run_gaps.json").read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None
    if not isinstance(r, dict):
        return None
    rows = [x for k in ("home_unguessed", "short_sentences", "held_by_wording") for x in r.get(k) or []]
    rows += [{"speciality": s.get("speciality"), "n": s.get("n")} for h in r.get("home_measures") or []
             if isinstance(h, dict) for s in h.get("sentences") or [] if isinstance(s, dict)]
    rows += [{"speciality": b.get("speciality"), **s} for b in r.get("building") or [] if isinstance(b, dict)
             for s in b.get("sentences") or [] if isinstance(s, dict)]
    return {x.get("n") for x in rows if isinstance(x, dict) and x.get("speciality") == sp}


def _names(area: str, repo: Path | None, workspace: Path) -> set[str]:
    """An area's topic names (`_topics`); with no repo, its plan's rows only."""
    if repo is not None:
        return _topics(area, repo, workspace)
    from stage_status import plan_rows
    return set(plan_rows(workspace / "areas" / area / "area-plan.md"))


def stale_homes(workspace: Path, area: str, repo: Path | None) -> list[dict]:
    """G205 (1.4.39): every recorded home that names no topic: a `homes`
    value in A/building-*.json that is no topic of this plan (an older bare
    name for another area's topic: give it as N=AREA:TOPIC), and an
    A/homes.json value not in AREA:TOPIC form or naming no topic of that
    area. Rows {"file", "speciality", "n", "home", "why"}; never dropped."""
    a = workspace / "areas" / area
    rows: list[dict] = []
    seen: dict[str, set[str]] = {}

    def topics(of: str) -> set[str]:
        if of not in seen:
            seen[of] = _names(of, repo, workspace)
        return seen[of]

    def cross(home: str) -> str | None:
        where, _, name = home.rpartition(":")
        if repo is not None and not known_area(where, repo, workspace) or not where:
            return f"{where or '(none)'} is no area of the cookbook and has no plan"
        if name not in topics(where):
            return f"{name or '(none)'} is no topic of {where}"
        return None

    def add(f: Path, sp, n, home: str, why: str | None) -> None:
        if why:
            rows.append({"file": f.name, "speciality": sp, "n": str(n), "home": home,
                         "why": why + ": re-record it with mark.py --home N=TOPIC (this area) or N=AREA:TOPIC"})
    for f in sorted(a.glob("building-*.json")):
        try:
            d = json.loads(f.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            continue
        homes = d.get("homes") if isinstance(d, dict) else None
        for n, home in sorted(homes.items()) if isinstance(homes, dict) else ():
            if isinstance(home, str) and home:
                add(f, d.get("speciality"), n, home, cross(home) if ":" in home else
                    (None if home in topics(area) else f"{home} is no topic of {area}"))
    try:
        other = json.loads((a / HOMES).read_text(encoding="utf-8"))
    except (OSError, ValueError):
        other = {}
    for sp, by_n in sorted(other.items()) if isinstance(other, dict) else ():
        for n, home in sorted(by_n.items()) if isinstance(by_n, dict) else ():
            if isinstance(home, str) and home:
                add(a / HOMES, sp, n, home, cross(home) if ":" in home else
                    f"{home} is not in AREA:TOPIC form, the form {HOMES} holds")
    return rows


def _unguessed(a, sp: str) -> tuple[set | None, dict]:
    """G203 (1.4.39), L8 (1.4.40): the sentence numbers of `sp` the saved
    A/run_gaps.json lists in `home_unguessed` (None when it cannot be read),
    and for every other number the home_measures row or the `home_guess`
    sentence where it is listed instead: both take a recorded home too, which
    run_gaps.py reads for every sentence (`home`, `home_topic`)."""
    try:
        r = json.loads((a.workspace / "areas" / a.area / "run_gaps.json").read_text(encoding="utf-8"))
        if not isinstance(r, dict):
            raise ValueError
    except (OSError, ValueError):
        return None, {}
    ns = {x.get("n") for x in r.get("home_unguessed") or [] if isinstance(x, dict) and x.get("speciality") == sp}
    where: dict = {}
    for b in r.get("building") or []:
        for x in (b.get("sentences") or []) if isinstance(b, dict) and b.get("speciality") == sp else []:
            if isinstance(x, dict) and x.get("home_guess"):
                where.setdefault(x.get("n"), f"a building sentence with home_guess {x['home_guess']}")
    for h in r.get("home_measures") or []:
        for x in (h.get("sentences") or []) if isinstance(h, dict) else []:
            if isinstance(x, dict) and x.get("speciality") == sp:
                where.setdefault(x.get("n"), f"a home_measures row at {h.get('topic')}")
    return ns, where


def _homes(a) -> int:
    """G145: set `homes[N]` to a topic of this plan, or clear it; every N
    checked first. G156 (1.4.37): `N=<area>:<topic>` names a home in another
    area: it goes in this area's A/homes.json (no marks file needed), the
    area known and the topic one of its topics; `N=` clears both."""
    repo, ws = a.repo.resolve(), a.workspace.resolve()
    f = (a.workspace / "areas" / a.area / f"building-{a.speciality.rsplit('/', 1)[-1]}.json").resolve()
    hf = (a.workspace / "areas" / a.area / HOMES).resolve()
    data, text = None, None
    if f.is_file():
        try:
            data = json.loads(f.read_text(encoding="utf-8"))
            text = {s["n"]: s["text"] for s in data["sentences"]}
        except (OSError, ValueError, KeyError, TypeError, AttributeError) as e:
            return _refuse(f"cannot read {f} as a marks file ({e.__class__.__name__}: {e})")
        if data.get("speciality") != a.speciality:
            return _refuse(f"{f} holds {data.get('speciality')}, not {a.speciality}")
    known = set(text) if text is not None else _report_ns(a, a.speciality)
    here = None
    wanted = []
    for h in a.home:
        n, eq, topic = h.partition("=")
        if not eq or not n.strip().isdigit() or topic != topic.strip():
            return _refuse(f"--home {h}: give it as N=TOPIC (a topic of this plan) or N=AREA:TOPIC")
        area, colon, name = topic.rpartition(":")
        if colon:
            if not known_area(area, repo, ws):
                return _refuse(f"--home {h}: {area} is no area of {repo / 'cookbook' / 'guidelines'} and has no "
                               f"plan under {ws / 'areas'}")
            if not name or "/" in name or name not in _topics(area, repo, ws):
                return _refuse(f"--home {h}: {name or '(none)'} is no topic of {area} (its plan's Proposed topics "
                               "or a folder holding artifact.json)")
        elif topic:
            if "/" in topic:
                return _refuse(f"--home {h}: give it as N=TOPIC (a topic of this plan) or N=AREA:TOPIC")
            if data is None:
                return _refuse(f"cannot read {f} as a marks file (a home in this area is recorded there; a home "
                               "in another area is N=AREA:TOPIC)")
            here = _topics(a.area, repo, ws) if here is None else here
            if topic not in here:
                return _refuse(f"--home {h}: {topic} is no topic of {a.area} (its plan's Proposed topics or a "
                               "folder holding artifact.json)")
        if known is None:
            return _refuse(f"--home {h}: no marks file {f} and no readable saved report to check sentence {n} "
                           "against: run step 1.3's run_gaps.py first")
        if int(n) not in known:
            return _refuse(f"{f if text is not None else 'the saved report'} has no sentence {n} of {a.speciality}")
        if topic:      # G203 (1.4.39), L8 (1.4.40): a building sentence of the saved report with a home to record
            unguessed, where = _unguessed(a, a.speciality)
            if unguessed is None:
                return _refuse(f"--home {h}: no readable saved A/run_gaps.json to check that sentence {n} is a "
                               "building sentence of it: run step 1.3's run_gaps.py first")
            if int(n) not in unguessed and int(n) not in where:
                return _refuse(f"--home {h}: sentence {n} of {a.speciality} is no home_unguessed or home_measures "
                               f"row and carries no home_guess in the saved A/run_gaps.json: a home is recorded "
                               "for a sentence that has one to change")
        wanted.append((int(n), topic, bool(colon)))
    ns = [n for n, _, _ in wanted]
    if len(set(ns)) != len(ns):
        return _refuse("a sentence is given two homes in one call")
    try:
        other = json.loads(hf.read_text(encoding="utf-8")) if hf.is_file() else {}
        if not isinstance(other, dict):
            raise ValueError("not a JSON object")
    except (OSError, ValueError) as e:
        return _refuse(f"cannot read {hf} ({e.__class__.__name__}: {e})")
    mine = other.setdefault(a.speciality, {})
    homes = data.setdefault("homes", {}) if data is not None else {}
    rows = []
    for n, topic, cross in wanted:
        was = mine.get(str(n)) or homes.get(str(n))
        if cross:
            mine[str(n)] = topic
            homes.pop(str(n), None)
        elif topic:
            homes[str(n)] = topic
            mine.pop(str(n), None)
        else:
            homes.pop(str(n), None)
            mine.pop(str(n), None)
        rows.append({"n": n, "text": text.get(n) if text else None, "was": was, "now": topic or None})
    if not mine:
        other.pop(a.speciality, None)
    if data is not None:
        _write(f, data)
    if other or hf.is_file():
        _write(hf, other)
    print(json.dumps({"file": str(f) if data is not None else None, "homes_file": str(hf), "homes": rows}))
    return 0


PINNED = ("text", "topic_sentence", "rule_sentence", "topic_hash")      # G202 (1.4.39): what a verdict rests on


ROW_LISTS = ("held_by_wording", "lacking_pieces", "short_sentences", "home_lacking", "r9_lacking",
             "hand_lacks")      # gapfix13 (1.4.42): G253, G254
HAND = "hand_lacks.json"        # run_gaps.HAND


def _topic_sents(a, topic: str) -> list[str] | None:
    """gapfix14 (G280b): every sentence of TOPIC's folder (`R/cookbook/guidelines/<area>/<topic>` first, else the
    one folder of that name in any area), or None when no folder holds it."""
    from paraphrase_hints import topic_sentences
    g = a.repo.resolve() / "cookbook" / "guidelines"
    name = topic.rpartition(":")[2]
    own = g / a.area / name
    folders = [own] if (own / "artifact.json").is_file() else sorted(
        f.parent for f in g.glob(f"**/{name}/artifact.json"))
    if not folders:
        return None
    return [t for f in folders for _, t in topic_sentences(f)]


def _clause_check(a, rid: str, row: dict, clauses: list) -> list[str]:
    """gapfix14 (G280a/b, 1.4.43): a multi-clause piece is held when each clause is stated, at an equal or stronger
    modal, by some sentence of the row's topic. Each {clause, cites} is checked: the cited sentence is the topic's
    (a whole sentence or a part of one) and its modal (its weakest; an imperative or a flat statement reads as MUST)
    is not weaker than the clause's (its own; else the piece's or its sentence's; else MUST). Each clause gets
    `modal_clause` and `modal_cites` added."""
    import run_gaps
    bad = []
    sents = _topic_sents(a, str(row.get("topic") or "")) if row.get("topic") else None
    norm = [" ".join(t.split()) for t in sents or []]
    for c in clauses:
        clause, cites = (c.get("clause") or "").strip(), (c.get("cites") or "").strip()
        if not clause or not cites:
            bad.append(f"{rid}: each --clause takes one --cites (the topic sentence stating it)")
            continue
        if sents is not None and not any(" ".join(cites.split()) in t for t in norm):
            bad.append(f"{rid}: --cites {cites!r} is no sentence of topic {row.get('topic')} (quote it as the "
                       "topic's rules state it)")
            continue
        mc, rc = run_gaps.modal(clause)
        if rc is None:
            for k in ("modal_piece", "modal_sentence"):
                if row.get(k):
                    mc, rc = row[k], run_gaps.modal(row[k])[1]
                    break
        if rc is None:
            mc, rc = "MUST", 3
        mt, rt = run_gaps.modal_weakest(cites)
        if rt is None:
            mt, rt = "MUST", 3
        if rt < rc:
            bad.append(f"{rid}: --cites {cites!r} states {mt}, weaker than the clause's {mc} ({clause!r}): "
                       "a weaker modal never holds (G160)")
            continue
        c.update({"clause": clause, "cites": cites, "modal_clause": mc, "modal_cites": mt})
    return bad


def _held(a, wanted: dict | None = None, extra: dict | None = None) -> int:
    """G159 (1.4.37): record a verdict in A/held.json for the row with this id
    of the saved A/run_gaps.json, with what it was judged on. 1.4.40 (G225,
    G226, G233): the ids of all three row lists take a verdict:
    `held_by_wording` (`held` or `not`; PINNED, G202), `lacking_pieces`
    (`held`: cookr measured the piece lacking, the plan holds it in other
    words) and `short_sentences` (`not`: the short piece is lacking; `held`).
    A verdict that moves the area's total (a lacking piece `held`, a short
    piece `not`) needs `--why`, one line, kept with it. `wanted`
    {id: (verdict, why)} is `--held-file`'s (G199): every id and verdict is
    checked first, and one bad one writes none.
    gapfix14 (1.4.43): a value may carry a third item, `counted_at` (G273 a,
    G289: `--counted-at AREA`, a `held` verdict only: the sentence is counted
    at that area, its owner); a `not` on a held_by_wording row moves the
    total and needs a why like every other verdict (G288)."""
    single = wanted is None
    if single:
        cl, ci = getattr(a, "clause", None) or [], getattr(a, "cites", None) or []
        pairs = [{"clause": x, "cites": y} for x, y in zip(cl, ci)] + [
            {"clause": x, "cites": ""} for x in cl[len(ci):]] + [{"clause": "", "cites": y} for y in ci[len(cl):]]
        wanted = {a.held[0]: (a.held[1], (a.why or "").strip(), getattr(a, "counted_at", None), pairs or None)}
    wanted = {rid: (tuple(v) + (None, None))[:4] for rid, v in wanted.items()}
    d = a.workspace / "areas" / a.area
    try:
        report = json.loads((d / "run_gaps.json").read_text(encoding="utf-8"))
        by_id: dict[str, tuple[str, dict]] = {}
        for kind in ROW_LISTS:
            for r in report.get(kind) or []:
                if isinstance(r, dict) and r.get("id"):
                    by_id[r["id"]] = (kind, r)
        report["held_by_wording"]
        hand = json.loads((d / HAND).read_text(encoding="utf-8")) if (d / HAND).is_file() else {}
        for rid, v in (hand.items() if isinstance(hand, dict) else ()):
            if isinstance(v, dict):      # a hand lack recorded since the last run is judged too
                by_id.setdefault(rid, ("hand_lacks", {"id": rid, **v}))
    except (OSError, ValueError, KeyError, TypeError, AttributeError) as e:
        return _refuse(f"cannot read held_by_wording from {d / 'run_gaps.json'} ({e.__class__.__name__}: {e})")
    unknown = [rid for rid in wanted if rid not in by_id]
    if unknown:
        return _refuse(f"no {', '.join(ROW_LISTS)} row "
                       f"{', '.join(repr(r) for r in unknown)} in {d / 'run_gaps.json'} "
                       "(re-run step 1.3's run_gaps.py and copy each row's `id`)")
    bad = []
    for rid, (v, why, at, clauses) in wanted.items():
        kind = by_id[rid][0]
        ok = ("held", "not")
        if clauses and v != "held":
            bad.append(f"{rid} {v}: --clause/--cites go with held only (each clause held by a topic sentence)")
        elif clauses:
            bad.extend(_clause_check(a, rid, by_id[rid][1], clauses))
        if v not in ok:
            bad.append(f"{rid} {v}: the verdict is held or not")
        elif at is not None and v != "held":
            bad.append(f"{rid} {v}: --counted-at goes with held only (held here, counted at the owner)")
        elif at is not None and not known_area(at, a.repo.resolve(), a.workspace.resolve()):
            bad.append(f"{rid}: --counted-at {at} is no area of {a.repo / 'cookbook' / 'guidelines'} and has no "
                       f"plan under {a.workspace / 'areas'}")
        elif not why and not (kind in ("held_by_wording", "short_sentences") and v == "held"):
            bad.append(f"{rid} {v}: give --why, one line saying where the plan holds it (or why it is lacking)" +
                       (": this verdict moves the area's gap total" if v == "held" or kind == "short_sentences"
                        else ": a `not` here moves the piece to lacking, raising the total (G288)"
                        if kind == "held_by_wording"
                        else ": a `not` here confirms the lack, which stays counted (G255)"))
    if bad:
        return _refuse("--held " + "; ".join(bad))
    f = d / HELD
    try:
        saved = json.loads(f.read_text(encoding="utf-8")) if f.is_file() else {}
        if not isinstance(saved, dict):
            raise ValueError("not a JSON object")
    except (OSError, ValueError) as e:
        return _refuse(f"cannot read {f} ({e.__class__.__name__}: {e})")
    changed = []
    for rid, (verdict, why, at, clauses) in wanted.items():
        old = saved.get(rid) if isinstance(saved.get(rid), dict) else None
        was = old.get("verdict") if old else None
        kind, row = by_id[rid]
        pinned = ({k: row.get(k) for k in PINNED if k in row or k in PINNED[:2]} if kind == "held_by_wording"
                  else {"text": row.get("text")})
        saved[rid] = {"verdict": verdict, **pinned, **({"why": why} if why else {}),
                      **({"counted_at": at} if at else {}), **({"clauses": clauses} if clauses else {})}
        how = "changed" if was != verdict else ("unchanged" if old == saved[rid] else "refreshed")      # G270
        changed.append({"id": rid, "was": was, "now": verdict, "how": how})
    _write(f, saved)
    counts = {k: sum(1 for c in changed if c["how"] == k) for k in ("changed", "refreshed", "unchanged")}
    moved = [c for c in changed if c["how"] != "unchanged"]
    print(json.dumps({"file": str(f), **{k: v for k, v in changed[0].items() if k != "how"}, **counts} if single
                     else {"file": str(f), **(extra or {}), "verdicts": len(changed), **counts,
                           **({"ids": [c["id"] for c in moved]} if getattr(a, "verbose", False) else {})}))
    return 0


def _norm(text: str) -> str:
    import re
    return " ".join(re.sub(r"[^a-z0-9]+", " ", (text or "").lower()).split())


def _lack(a, hold: bool = False) -> int:
    """gapfix13 (1.4.42, G253): `--lack TOPIC --source RELPATH#N --text
    SENTENCE --why WHY` records a hand lack in A/hand_lacks.json.
    gapfix14 (1.4.43): `--hold TOPIC` (same flags, G276) records a hand hold
    in A/hand_holds.json, `hold:<speciality>:<n>@<topic>`: the plan's `held`
    verdict on that sentence at that topic (a home no speciality measures),
    never counted. `--piece K` (G285) records piece K of the sentence as its
    own row (`...#K`, K from 2); an id already recorded is refused unless
    `--refresh` is given."""
    from quote_building import sentences
    d = a.workspace / "areas" / a.area
    flag, topic = ("--hold", a.hold) if hold else ("--lack", a.lack)
    if not (a.source and a.text and (a.why or "").strip()):
        return _refuse(f"{flag} needs --source RELPATH#N, --text SENTENCE and --why WHY (--source e.g. "
                       "reference/building--platform-windows.txt#10, below A)")
    if a.piece is not None and a.piece < 1:
        return _refuse(f"--piece {a.piece}: give the piece's number, 1 or more")
    rel, hash_, n = a.source.rpartition("#")
    if not hash_ or not n.isdigit():
        return _refuse(f"--source {a.source}: give it as RELPATH#N (N the sentence number)")
    n = int(n)
    f = next((b / rel for b in (d, a.workspace, a.repo) if (b / rel).is_file()), None)
    if f is None:
        return _refuse(f"--source {rel} is no file below {d}, {a.workspace} or {a.repo}")
    found = sentences(f.read_text(encoding="utf-8"))
    if not 1 <= n <= len(found):
        return _refuse(f"{rel} has no sentence {n} ({len(found)} sentences)")
    if _norm(found[n - 1]) != _norm(a.text):
        return _refuse(f"--text is not sentence {n} of {rel}, which reads: {found[n - 1]} (give it whole; a piece "
                       "of it is --piece K)")
    sp = f.stem.replace("--", "/")
    try:
        report = json.loads((d / "run_gaps.json").read_text(encoding="utf-8"))
        report = report if isinstance(report, dict) else {}
    except (OSError, ValueError):
        report = {}
    topics = _topics(a.area, a.repo, a.workspace)
    topics |= {t.get("topic") for t in report.get("topics") or [] if isinstance(t, dict)}
    topics |= {h.get("topic") for h in report.get("home_measures") or [] if isinstance(h, dict)}
    topics |= {r.get("topic") for r in report.get("r9_targets") or [] if isinstance(r, dict)}
    topics |= {str(x) for x in report.get("r9_missing") or []}
    if topic not in topics:
        return _refuse(f"{flag} {topic} is no topic of {a.area} (its plan's Proposed topics, a folder, a measured, "
                       f"home or R9 topic): {', '.join(sorted(t for t in topics if t))}")
    from run_gaps import measured_row, HOLDS
    dup = None if hold else measured_row(report, sp, n, topic)
    if dup:
        return _refuse(f"sentence {n} of {sp} is already the measured row {dup}: judge that row with --held "
                       f"{dup} not --why ... (a hand lack never doubles a measured row)")
    hf = d / (HOLDS if hold else HAND)
    try:
        hand = json.loads(hf.read_text(encoding="utf-8")) if hf.is_file() else {}
        if not isinstance(hand, dict):
            raise ValueError("not a JSON object")
    except (OSError, ValueError) as e:
        return _refuse(f"cannot read {hf} ({e.__class__.__name__}: {e})")
    rid = f"{'hold' if hold else 'hand'}:{sp}:{n}@{topic}" + (f"#{a.piece}" if a.piece and a.piece > 1 else "")
    was = hand.get(rid)
    if was is not None and not a.refresh:
        return _refuse(f"{rid} is already recorded ({was.get('why') if isinstance(was, dict) else was}): give "
                       "--refresh to re-record it, or --piece K for another piece of the sentence (G285)")
    hand[rid] = {"topic": topic, "source": a.source, "speciality": sp, "n": n, "text": found[n - 1],
                 **({"piece": a.piece} if a.piece else {}), "why": a.why.strip()}
    _write(hf, hand)
    print(json.dumps({"file": str(hf), "id": rid, "topic": topic, "speciality": sp, "n": n, "text": found[n - 1],
                      "now": "held" if hold else "lacking",
                      "how": "unchanged" if was == hand[rid] else ("refreshed" if was else "added")}))
    return 0


def _non_home_held(a) -> int:
    """gapfix14 (1.4.43, G284 c): judge `held` every non_home_lacking row of
    the saved A/run_gaps.json whose home has a verdict in any area's saved
    report (run_gaps.home_verdict: a hold, a hand hold, or a lack counted
    there), why "judged at home topic AREA:TOPIC (<id>: <verdict>)", in one
    write; a home in another area also gets `counted_at`. A row whose home
    has no verdict yet is left out and counted (G256), and named."""
    import run_gaps
    d = a.workspace / "areas" / a.area
    try:
        report = json.loads((d / "run_gaps.json").read_text(encoding="utf-8"))
        rows, pieces = report["non_home_lacking"], {r["id"]: r for r in report.get("lacking_pieces") or []}
    except (OSError, ValueError, KeyError, TypeError, AttributeError) as e:
        return _refuse(f"cannot read non_home_lacking from {d / 'run_gaps.json'} ({e.__class__.__name__}: {e}): "
                       "run step 1.3's run_gaps.py first")
    reports = run_gaps.saved_reports(a.workspace)
    wanted, skipped = {}, []
    for r in rows:
        p = pieces.get(r.get("id")) or {}
        owner, topic = run_gaps._home_record(a.area, str(r.get("home")))
        v = run_gaps.home_verdict(reports[owner][0], p.get("speciality"), p.get("n"), topic) \
            if owner in reports and p else None
        if v is None:
            skipped.append(r.get("id"))
            continue
        wanted[r["id"]] = ("held", f"judged at home topic {owner}:{topic} ({v['id']}: {v['verdict']})",
                           owner if owner != a.area else None)
    if not wanted:
        print(json.dumps({"file": str(d / HELD), "non_home_held": 0, "skipped_no_home_verdict": len(skipped),
                          **({"skipped": skipped} if a.verbose else {})}))
        return 0
    return _held(a, wanted, {"non_home_held": len(wanted), "skipped_no_home_verdict": len(skipped),
                             **({"skipped": skipped} if a.verbose else {})})


def _held_file(a) -> int:
    """G199 (1.4.39): `--held-file FILE`, a JSON object {id: verdict}; 1.4.40:
    a value is `held`, `not` or {"verdict": ..., "why": "..."}."""
    try:
        raw = json.loads(Path(a.held_file).read_text(encoding="utf-8"))
        if not isinstance(raw, dict) or not raw:
            raise ValueError("not a non-empty JSON object {id: held|not or {verdict, why}}")
        wanted = {}
        for rid, v in raw.items():
            at, clauses = None, None
            if isinstance(v, dict):
                v, why, at, clauses = v.get("verdict"), v.get("why") or "", v.get("counted_at"), v.get("clauses")
            else:
                why = ""
            if not isinstance(v, str) or not isinstance(why, str) or not isinstance(at, (str, type(None))) or not (
                    clauses is None or (isinstance(clauses, list) and all(isinstance(c, dict) for c in clauses))):
                raise ValueError(f"{rid}: a verdict is a string or {{verdict, why[, counted_at][, clauses: "
                                 "[{clause, cites}]]}}")
            wanted[rid] = (v, why.strip(), at, [dict(c) for c in clauses] if clauses else None)
    except (OSError, ValueError) as e:
        return _refuse(f"cannot read --held-file {a.held_file} ({e.__class__.__name__}: {e})")
    return _held(a, wanted)


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0], formatter_class=PathHelpFormatter)
    add_area(ap)
    ap.add_argument("--workspace", type=Path, required=True)
    ap.add_argument("--repo", type=Path, required=True)
    ap.add_argument("--speciality", help="required, except with --held and --held-file")
    ap.add_argument("--n", type=int)
    how = ap.add_mutually_exclusive_group()
    how.add_argument("--to", nargs="+", metavar="AREA")
    how.add_argument("--clear", action="store_true")
    ap.add_argument("--mark", action="append", metavar="N=AREA[,AREA]", help="repeatable: many marks in one call")
    ap.add_argument("--home", action="append", metavar="N=TOPIC|N=AREA:TOPIC",
                    help="repeatable, with --speciality: record the home topic the plan chose for sentence N, a "
                         "home_unguessed row of the saved A/run_gaps.json (G145, G203): a topic of this plan (kept in "
                         "the marks file's homes), or AREA:TOPIC for a home in another area (kept in A/homes.json, "
                         "G156); one home per sentence, a new one replacing it; N= clears it; a --home on any row, a "
                         "home_measures one too, adds the marks file's `homes` key, or A/homes.json (G287)")
    ap.add_argument("--held", nargs=2, metavar=("ID", "VERDICT"),
                    help="record a verdict, held or not, for one row; the id forms: <speciality>:<n>@<topic> "
                         "(held_by_wording), lacking:<speciality>:<n>@<topic> (lacking_pieces), "
                         "short:<speciality>:<n> (short_sentences), home:<speciality>:<n>@<topic> (home_lacking), "
                         "r9:<name>:<speciality>:<n> (r9_lacking), hand:<speciality>:<n>@<topic> (hand_lacks, "
                         "held withdraws it), any ending #k; held uncounts a lack, not confirms it (a held_by_wording "
                         "or short row not: counted lacking); a re-run keeps it while the sentences stand")
    ap.add_argument("--held-file", metavar="FILE",
                    help="record many verdicts, of every id form, in one call (one file may mix them): FILE is a JSON object {id: held|not} "
                         "or {id: {verdict, why}} ({\"verdict\": \"held\", \"why\": \"...\"}); one unknown id or verdict "
                         "writes none (G199)")
    ap.add_argument("--why", help="with --held or --lack: one line saying why, kept with the verdict; required for "
                                  "every verdict but held on a held_by_wording row or a short row")
    ap.add_argument("--lack", metavar="TOPIC", help="record a lack judged by hand at TOPIC (G253), with --source "
                    "RELPATH#N, --text SENTENCE and --why; counted in run_gaps.py's measured_total")
    ap.add_argument("--source", metavar="RELPATH#N", help="with --lack: the reference file (below A, W or R) and "
                    "its sentence number, e.g. reference/building--platform-windows.txt#10 (below A); "
                    "quote_building.py --area A --speciality S --file F --keep /dev/null prints each sentence "
                    "with its number (G287)")
    ap.add_argument("--text", metavar="SENTENCE", help="with --lack: sentence N's text, as quote_building.py cuts it")
    ap.add_argument("--hold", metavar="TOPIC", help="record a hold judged by hand at TOPIC (G276), with --source, "
                    "--text and --why quoting the topic's rule: the sentence's held verdict there (an unmeasured "
                    "home, most often), in A/hand_holds.json as hold:<speciality>:<n>@<topic>; never counted")
    ap.add_argument("--piece", type=int, metavar="K", help="with --lack or --hold: piece K of the sentence, its own "
                    "row (id ending #K from 2), when one sentence holds several gaps (G285)")
    ap.add_argument("--refresh", action="store_true", help="with --lack or --hold: re-record an id already "
                    "recorded (refused without it, G285)")
    ap.add_argument("--counted-at", metavar="AREA", help="with --held ID held: the sentence is held here and "
                    "counted at AREA, its owner (G273); kept as counted_at, so --check-homes and --check-verdicts "
                    "read it")
    ap.add_argument("--clause", action="append", metavar="CLAUSE", help="repeatable, with --held ID held: one "
                    "clause of a multi-clause piece, each followed by its --cites (G280)")
    ap.add_argument("--cites", action="append", metavar="SENTENCE", help="repeatable, after each --clause: the "
                    "topic sentence stating that clause, at a modal no weaker than the clause's; checked and kept "
                    "with the verdict as clauses (G280)")
    ap.add_argument("--non-home-held", action="store_true", help="judge held every non_home_lacking row whose "
                    "home has a verdict in any area, why 'judged at home topic AREA:TOPIC', in one call; prints the "
                    "count and leaves the rest counted (G284)")
    ap.add_argument("--verbose", action="store_true", help="with --held-file or --non-home-held: name the ids")
    a = ap.parse_args(argv)
    a.area = area_arg(ap, a)
    from repo_path import check_area
    why = check_area("mark.py", a.workspace, a.area, a.repo)      # G198 (1.4.39)
    if why:
        print(why, file=sys.stderr)
        return 2
    if a.lack is not None or a.hold is not None:
        if a.held or a.held_file or a.home or a.mark or a.n is not None or a.to or a.clear or a.counted_at or \
                a.non_home_held or (a.lack is not None and a.hold is not None):
            ap.error("--lack and --hold go alone, with --source, --text and --why (--piece, --refresh)")
        return _lack(a, hold=a.hold is not None)
    if a.piece is not None or a.refresh:
        ap.error("--piece and --refresh go with --lack or --hold")
    if a.non_home_held:
        if a.held or a.held_file or a.home or a.mark or a.n is not None or a.to or a.clear or a.counted_at:
            ap.error("--non-home-held goes alone")
        return _non_home_held(a)
    if (a.clause or a.cites) and not a.held:
        ap.error("--clause and --cites go with --held ID held (in --held-file, a value's clauses)")
    if a.counted_at and not a.held:
        ap.error("--counted-at goes with --held ID held (in --held-file, a value's counted_at)")
    if a.held or a.held_file:
        if a.home or a.mark or a.n is not None or a.to or a.clear or (a.held and a.held_file):
            ap.error("--held and --held-file go alone")
        return _held(a) if a.held else _held_file(a)
    if not a.speciality:
        ap.error("give --speciality: --n, --mark and --home each need it (only --held and --held-file go "
                 "without)")
    if a.home:
        if a.mark or a.n is not None or a.to or a.clear:
            ap.error("--home goes alone, without --n, --to, --clear or --mark")
        return _homes(a)
    if a.mark and (a.n is not None or a.to or a.clear):
        ap.error("--mark goes alone, without --n, --to or --clear")
    if not a.mark and (a.n is None or not (a.to or a.clear)):
        ap.error("give --n with --to or --clear, or one --mark or more")
    wanted: list[tuple[int, list[str]]] = []
    for m in a.mark or []:
        n, eq, areas = m.partition("=")
        if not eq or not n.strip().isdigit():
            return _refuse(f"--mark {m}: give it as N=AREA[,AREA] (x= is no sentence number)")
        wanted.append((int(n), [t for t in areas.split(",") if t] if areas else []))
    if not a.mark:
        wanted = [(a.n, [] if a.clear else a.to)]
    f = (a.workspace / "areas" / a.area / f"building-{a.speciality.rsplit('/', 1)[-1]}.json").resolve()
    try:
        data = json.loads(f.read_text(encoding="utf-8"))
        text = {s["n"]: s["text"] for s in data["sentences"]}
        marks = data["marks"]
    except (OSError, ValueError, KeyError, TypeError, AttributeError) as e:
        return _refuse(f"cannot read {f} as a marks file ({e.__class__.__name__}: {e})")
    if data.get("speciality") != a.speciality:
        return _refuse(f"{f} holds {data.get('speciality')}, not {a.speciality}")
    ns = [n for n, _ in wanted]
    twice = sorted({n for n in ns if ns.count(n) > 1})
    if twice:
        return _refuse(f"sentence {', '.join(map(str, twice))} is marked twice in one call")
    gone = [n for n in ns if n not in text]
    if gone:
        return _refuse(f"{f} has no sentence {', '.join(map(str, gone))}")
    guidelines = a.repo.resolve() / "cookbook" / "guidelines"
    bad = sorted({t for _, areas in wanted for t in areas if not known_area(t, a.repo.resolve(), a.workspace.resolve())})
    if bad:
        return _refuse(f"{', '.join(bad)} is no area of {guidelines} and has no plan under {a.workspace / 'areas'}")
    rows = []
    for n, areas in wanted:
        was, now = marks.get(str(n)), _mark(areas)
        marks[str(n)] = now
        rows.append({"n": n, "text": text[n], "was": was, "now": now})
    _write(f, data)
    print(json.dumps({"file": str(f), "marks": rows} if a.mark else {"file": str(f), **rows[0]}))
    return 0


if __name__ == "__main__":
    from repo_path import run_main      # gapfix13 (G263, G271)
    run_main(main)
