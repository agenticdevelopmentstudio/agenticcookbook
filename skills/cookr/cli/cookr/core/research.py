"""The research an artifact is written from, and the census of what is wrong with it.

Every artifact is written from research on its topic, kept beside its parts in
`research/` (`markdown.RESEARCH_DIR`), which nothing compiles, walks or reads as
a spec:

- `research/research.json`: the research-results document
  (`guidelines/researching/evidence/research-results-document`). An object whose
  `claims` list holds one record per claim, each with every field CLAIM_FIELDS
  names, and a `verdicts` list, one per rule checked, which rules on every
  claim a rule cites:
  `{"rule", "verdict" (one of VERDICTS), "claims": [claim ids]}`. A verdict
  names the rule as it stood when checked, so a rule the write drops or
  renames keeps its verdict.
- `research/research.md`: the same, readable, under the four question
  headings (HEADINGS), in that order.

A rule cites the claims it stands on at the end of its named bullet, once:
`- **kebab-name**: … MUST … (claim: <claim-id>)`, or several:
`(claims: <id>, <id>)` (`markdown.CITATION`). A claim id is kebab-case and
unique in its research. The citation is provenance: compiled skills leave it
out, and `cookr roles lossless` reads a rule without it.

**Which artifacts are checked.** A cookbook with an EXEMPT_FILE
(`{"why", "topics": [paths below the cookbook dir]}`) is research-first: every
artifact in it needs its `research/` folder, except the topics the file lists,
which are owed research still. The file is emptied as their research lands; a
listed topic that has its `research/` folder, or that is no artifact, is
refused by name (`stale-exemption`). A cookbook without the file checks only
the artifacts the research-first work has touched: every artifact with a
`research/` folder, and every roled artifact, which must have one.

**Rules the research does not support.** Research that cannot support an
existing rule records the rule itself as a claim, its source the cookbook's
own text at the topic's base commit, with an `unsupported` verdict (or a
`contradicted` one, when the research finds against it) naming that claim.
A rule kept for the owner to decide cites that claim. It passes, and
`owner_rules` reports it (`owner-decides`), a warning that validate prints
and does not fail on. Only a rule citing such a prior claim is reported, never
one citing a research claim that shares its verdict.

**The research-only check.** `research_only` reports a folder's research
findings without the rule-citation ones (RULE_KINDS): it is what
`cookr validate --research <folder>` runs at the end of research, before any
rule cites it.

Citations are required of every named rule: the `rules` parts' named bullets
in a roled artifact, and every named bullet stating MUST, SHOULD or MAY in any
other part of an unroled one.

Findings:
- `no-research`: an artifact that needs research (above), not exempt, with no
  `research/` folder.
- `missing-research-file`: `research/` lacks research.json or research.md.
- `unreadable-research`: research.json is not JSON, or not an object with a
  `claims` list of objects.
- `incomplete-claim`: a claim lacks a field, or has an id that is not
  kebab-case, a question, trust score or independence out of range, or a
  citation lacking one of CITATION_FIELDS.
- `duplicate-claim`: two claims share an id.
- `bad-verdict`: a verdict that is not one of VERDICTS, names no claim, or
  cites an id that is no claim of the research.
- `missing-question`: research.md lacks one of HEADINGS, or puts them out of order.
- `rule-cites-nothing`: a rule cites no claim.
- `citation-not-at-end`: a rule's citation is not the end of its bullet, or
  it has more than one.
- `unknown-claim`: a rule cites an id that is no claim in research.json.
- `unverdicted-claim`: a rule cites a claim no verdict names.
- `stale-exemption`: a topic in EXEMPT_FILE has its research, or is no artifact.
- `duplicate-exemption`: EXEMPT_FILE lists a topic more than once.
- `unreadable-exemption`: EXEMPT_FILE is not `{"topics": [paths]}`.

Warning (`owner_rules`), never a failure:
- `owner-decides`: a rule cites a prior-cookbook-text claim (PRIOR_SOURCE) that
  a verdict rules OWNER_VERDICTS. A research claim in such a verdict is not
  enough: only the old rule itself is the owner's.
"""

from __future__ import annotations

import json
import re
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Optional

from .artifact import ARTIFACT_FILE, HISTORY, INTRO, Artifact, ArtifactError, is_folder, load_folder
from .errors import CookbookError
from .markdown import CITATION, RESEARCH_DIR
from .roles import named_bullets, rule_texts, states_requirement

RESEARCH_JSON = "research.json"
RESEARCH_MD = "research.md"
EXEMPT_FILE = "research-exempt.json"

#: The four questions every topic's research answers, and research.md's headings for them.
QUESTIONS: tuple[tuple[str, str], ...] = (
    ("best-practices", "Best practices"),
    ("known-solutions", "Known solutions"),
    ("platform-guidelines", "Platform guidelines"),
    ("experts-view", "The expert's view"),
)
HEADINGS = tuple(f"## {title}" for _, title in QUESTIONS)

#: What each claim carries (research-results-document's per-claim record).
CLAIM_TEXT = ("claim", "source_type", "quote", "generated_by", "query")
CITATION_FIELDS = ("title", "author", "publisher", "date", "url", "accessed")
CLAIM_FIELDS = ("id", "question", *CLAIM_TEXT, "citations", "trust", "independence")
INDEPENDENCE = ("multi-independent", "single", "uncorroborated")
VERDICTS = ("supported", "contradicted", "unsupported", "new")
#: The source_type of a claim that records the cookbook's own rule before research.
PRIOR_SOURCE = "prior cookbook text"

#: The verdicts that leave a rule citing them for the owner to decide.
OWNER_VERDICTS = ("unsupported", "contradicted")
#: The findings on a rule's citations: the research-only check leaves them out.
RULE_KINDS = frozenset({"rule-cites-nothing", "citation-not-at-end", "unknown-claim", "unverdicted-claim"})

_ID = re.compile(r"[a-z0-9]+(?:-[a-z0-9]+)*\Z")


@dataclass
class ResearchFinding:
    folder: Path
    kind: str                 # see the module docstring
    detail: str


def citations(text: str) -> list[str]:
    """The claim ids a rule's text cites, in order."""
    return [i.strip() for m in CITATION.finditer(text) for i in m.group(1).split(",") if i.strip()]


def cited_at_end(text: str) -> bool:
    """True when `text` has no citation, or one only, ending it."""
    found = list(CITATION.finditer(text))
    return not found or (len(found) == 1 and found[0].end() == len(text.rstrip()))


def rules_of(artifact: Artifact) -> dict[str, str]:
    """{rule name: its bullet} for every rule that must cite its research."""
    if artifact.roled:
        texts = rule_texts(artifact)
    else:
        texts = named_bullets(p for p in artifact.parts if p.name not in (INTRO, HISTORY))
    return {name: text for name, text in texts.items() if states_requirement(text)}


def _blank(value) -> bool:
    return not isinstance(value, str) or not value.strip()


def _claim_problems(n: int, claim) -> tuple[Optional[str], list[str]]:
    """(the claim's id, or None when it has no usable one; what is wrong with it)."""
    if not isinstance(claim, dict):
        return None, [f"claim {n} is not an object"]
    cid = claim.get("id")
    if _blank(cid):
        return None, [f"claim {n}: no 'id'"]
    if not _ID.match(cid):
        return None, [f"claim {n}: id {cid!r} is not kebab-case"]
    where = f"claim {cid!r}"
    out = []
    question = claim.get("question")
    if question not in dict(QUESTIONS):
        out.append(f"{where}: question {question!r} is not one of {', '.join(k for k, _ in QUESTIONS)}")
    out += [f"{where}: no {f!r}" for f in CLAIM_TEXT if _blank(claim.get(f))]
    cites = claim.get("citations")
    if not isinstance(cites, list) or not cites:
        out.append(f"{where}: no 'citations'")
    else:
        for i, c in enumerate(cites, 1):
            missing = [f for f in CITATION_FIELDS if not isinstance(c, dict) or _blank(c.get(f))]
            out += [f"{where}: citation {i} has no {f!r}" for f in missing]
    trust = claim.get("trust")
    score = trust.get("score") if isinstance(trust, dict) else None
    if not isinstance(score, int) or isinstance(score, bool):
        out.append(f"{where}: no 'trust' score")
    elif not 0 <= score <= 100:
        out.append(f"{where}: trust score {score} is not 0-100")
    if not isinstance(trust, dict) or _blank(trust.get("basis")):
        out.append(f"{where}: no 'trust' basis")
    if claim.get("independence") not in INDEPENDENCE:
        out.append(f"{where}: independence {claim.get('independence')!r} is not one of "
                   f"{', '.join(INDEPENDENCE)}")
    return cid, out


def _read(path: Path) -> Optional[dict]:
    try:
        doc = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, ValueError):
        return None
    if not isinstance(doc, dict) or not isinstance(doc.get("claims"), list):
        return None
    return doc


def _headings(text: str) -> list[tuple[str, str]]:
    lines = [line.rstrip() for line in text.splitlines()]
    missing = [h for h in HEADINGS if h not in lines]
    if missing:
        return [("missing-question", f"{RESEARCH_DIR}/{RESEARCH_MD} has no \"{h}\" heading") for h in missing]
    if [line for line in lines if line in HEADINGS] != list(HEADINGS):
        return [("missing-question", f"{RESEARCH_DIR}/{RESEARCH_MD} puts its question headings out of order")]
    return []


def _findings(folder: Path, artifact: Artifact, exempt: Optional[set[Path]]) -> list[tuple[str, str]]:
    """`exempt` is None in a cookbook with no EXEMPT_FILE: only a roled artifact needs research there."""
    d = folder / RESEARCH_DIR
    if not d.is_dir():
        if exempt is None:
            return [("no-research", f"a roled artifact with no {RESEARCH_DIR}/ folder")] if artifact.roled else []
        if folder not in exempt:
            return [("no-research", f"no {RESEARCH_DIR}/ folder, and not listed in {EXEMPT_FILE}")]
        return []
    found = [("missing-research-file", f"{RESEARCH_DIR}/ has no {name}")
             for name in (RESEARCH_JSON, RESEARCH_MD) if not (d / name).is_file()]
    doc = _read(d / RESEARCH_JSON) if (d / RESEARCH_JSON).is_file() else None
    if (d / RESEARCH_JSON).is_file() and doc is None:
        found.append(("unreadable-research", f"{RESEARCH_DIR}/{RESEARCH_JSON} is not an object "
                                             "with a 'claims' list"))
    if (d / RESEARCH_MD).is_file():
        found += _headings((d / RESEARCH_MD).read_text(encoding="utf-8"))
    if doc is None:
        return found

    ids = []
    for n, claim in enumerate(doc["claims"], 1):
        cid, problems = _claim_problems(n, claim)
        found += [("incomplete-claim", p) for p in problems]
        if cid is not None:
            ids.append(cid)
    found += [("duplicate-claim", f"claim {cid!r} appears {k} times")
              for cid, k in Counter(ids).items() if k > 1]
    known = set(ids)

    ruled = set()
    for n, v in enumerate(doc.get("verdicts") or [], 1):
        if not isinstance(v, dict) or v.get("verdict") not in VERDICTS:
            found.append(("bad-verdict", f"verdict {n} is not one of {', '.join(VERDICTS)}"))
            continue
        if not v.get("claims"):
            found.append(("bad-verdict", f"verdict {n} names no claim"))
        found += [("bad-verdict", f"verdict {n} cites {c!r}, which is no claim")
                  for c in v.get("claims") or [] if c not in known]
        ruled.update(c for c in v.get("claims") or [] if isinstance(c, str))

    for name, text in rules_of(artifact).items():
        cited = citations(text)
        if not cited:
            found.append(("rule-cites-nothing", f"rule '{name}' cites no research claim"))
        elif not cited_at_end(text):
            found.append(("citation-not-at-end", f"rule '{name}' has a citation before its end"))
        for c in dict.fromkeys(cited):
            if c not in known:
                found.append(("unknown-claim", f"rule '{name}' cites '{c}', which is no claim in "
                                               f"{RESEARCH_DIR}/{RESEARCH_JSON}"))
            elif c not in ruled:
                found.append(("unverdicted-claim", f"rule '{name}' cites '{c}', which no verdict rules on"))
    return found


def _verdicts_by_claim(folder: Path) -> dict[str, list[str]]:
    """{claim id: the verdicts naming it}, from `folder`'s research.json ({} when unreadable)."""
    doc = _read(folder / RESEARCH_DIR / RESEARCH_JSON)
    out: dict[str, list[str]] = {}
    for v in (doc or {}).get("verdicts") or []:
        if isinstance(v, dict) and v.get("verdict") in VERDICTS:
            for c in v.get("claims") or []:
                if isinstance(c, str):
                    out.setdefault(c, []).append(v["verdict"])
    return out


def _prior_claims(folder: Path) -> set[str]:
    """The ids of `folder`'s claims whose source is the cookbook's own text
    before research (source_type PRIOR_SOURCE)."""
    doc = _read(folder / RESEARCH_DIR / RESEARCH_JSON)
    return {c["id"] for c in (doc or {}).get("claims") or []
            if isinstance(c, dict) and isinstance(c.get("id"), str)
            and c.get("source_type") == PRIOR_SOURCE}


def owner_rules(root: Path, folders: Iterable[Path]) -> list[ResearchFinding]:
    """A warning for each rule of `folders` that cites the prior cookbook text
    (a PRIOR_SOURCE claim) of a verdict the research rules unsupported or
    contradicted: an old rule kept for the owner to decide. A rule citing a
    research claim that sits in such a verdict is not the owner's."""
    found = []
    for folder in folders:
        if not (folder / RESEARCH_DIR).is_dir():
            continue
        try:
            artifact = load_folder(folder)
        except ArtifactError:
            continue
        verdicts = _verdicts_by_claim(folder)
        prior = _prior_claims(folder)
        for name, text in rules_of(artifact).items():
            for c in dict.fromkeys(citations(text)):
                if c not in prior:
                    continue
                for v in dict.fromkeys(verdicts.get(c, [])):
                    if v in OWNER_VERDICTS:
                        found.append(ResearchFinding(folder, "owner-decides",
                                                     f"rule '{name}' cites '{c}', which the research rules {v}"))
    return found


class NotAnArtifactError(CookbookError):
    """`research_only` was given a path that is no artifact source folder."""


def research_only(root: Path, folder: Path) -> list[ResearchFinding]:
    """The findings on `folder`'s research alone, at the end of research and
    before its rules cite it: no rule-citation finding (RULE_KINDS), and
    `no-research` whether or not the folder is roled or exempt. A path that is
    no artifact source folder (a typo) is refused by name, never `no-research`."""
    if not is_folder(folder):
        raise NotAnArtifactError(f"{folder}: not an artifact source folder (no {ARTIFACT_FILE})")
    if not (folder / RESEARCH_DIR).is_dir():
        return [ResearchFinding(folder, "no-research", f"no {RESEARCH_DIR}/ folder")]
    try:
        artifact = load_folder(folder)
    except ArtifactError as e:
        return [ResearchFinding(folder, "unreadable-research", f"the artifact does not load: {e}")]
    _, stale = exemptions(root)
    return ([ResearchFinding(folder, k, d) for k, d in _findings(folder, artifact, None)
             if k not in RULE_KINDS]
            + [f for f in stale if f.folder.resolve() == folder.resolve()])


def exemptions(root: Path) -> tuple[Optional[list[str]], list[ResearchFinding]]:
    """(the topics `root`'s EXEMPT_FILE lists, below `root`, or None when it
    has no such file; its findings)."""
    path = root / EXEMPT_FILE
    if not path.is_file():
        return None, []
    try:
        topics = json.loads(path.read_text(encoding="utf-8")).get("topics")
    except (OSError, UnicodeDecodeError, ValueError, AttributeError):
        topics = None
    if not isinstance(topics, list) or not all(isinstance(t, str) for t in topics):
        return [], [ResearchFinding(root, "unreadable-exemption",
                                    f"{EXEMPT_FILE} is not {{\"topics\": [paths]}}")]
    found = [ResearchFinding(root / t, "duplicate-exemption", f"{t} is listed {k} times in {EXEMPT_FILE}")
             for t, k in Counter(topics).items() if k > 1]
    for t in dict.fromkeys(topics):
        folder = root / t
        if not is_folder(folder):
            found.append(ResearchFinding(folder, "stale-exemption",
                                         f"{t} is listed in {EXEMPT_FILE} but is no artifact"))
        elif (folder / RESEARCH_DIR).is_dir():
            found.append(ResearchFinding(folder, "stale-exemption",
                                         f"{t} is listed in {EXEMPT_FILE} but has its {RESEARCH_DIR}/ folder"))
    return topics, found


def census(root: Path, folders: Iterable[Path]) -> list[ResearchFinding]:
    """Every finding on the research of `folders` (artifacts below cookbook
    `root`), then on `root`'s exemption list. A folder too broken to read is
    skipped: the compile check reports it."""
    topics, stale = exemptions(root)
    exempt = None if topics is None else {(root / t) for t in topics}
    findings = []
    for folder in folders:
        try:
            artifact = load_folder(folder)
        except ArtifactError:
            continue
        findings += [ResearchFinding(folder, k, d) for k, d in _findings(folder, artifact, exempt)]
    return findings + stale


FIX = {
    "no-research": f"Research the topic (`/grow-cookbook`, stage 2) into {RESEARCH_DIR}/{RESEARCH_JSON} "
                   f"and {RESEARCH_DIR}/{RESEARCH_MD}.",
    "missing-research-file": f"Write both {RESEARCH_DIR}/{RESEARCH_JSON} and {RESEARCH_DIR}/{RESEARCH_MD}.",
    "unreadable-research": f"Make {RESEARCH_JSON} a JSON object with a 'claims' list.",
    "incomplete-claim": "Give the claim every field the research-results document requires: "
                        + ", ".join(CLAIM_FIELDS) + "; each citation: " + ", ".join(CITATION_FIELDS) + ".",
    "duplicate-claim": "Give each claim its own id.",
    "bad-verdict": "Each verdict is one of " + ", ".join(VERDICTS) + " and names claims of the research "
                   "(a rule the research cannot support is itself a claim: its source, the cookbook's text).",
    "missing-question": f"Put the four question headings in {RESEARCH_MD}, in order: " + "; ".join(HEADINGS) + ".",
    "rule-cites-nothing": "End the rule with the claims it stands on: `(claim: <id>)` or `(claims: <id>, <id>)`.",
    "citation-not-at-end": "Put the rule's one citation at the end of its bullet: "
                           "`(claim: <id>)` or `(claims: <id>, <id>)`.",
    "unverdicted-claim": f"Give each claim a rule cites a verdict in {RESEARCH_JSON}'s 'verdicts': "
                         "one of " + ", ".join(VERDICTS) + ", naming the claim in its 'claims'.",
    "duplicate-exemption": f"List the topic once in {EXEMPT_FILE}.",
    "unknown-claim": f"Cite a claim id from {RESEARCH_JSON}, or add the claim to the research.",
    "stale-exemption": f"Remove the topic from {EXEMPT_FILE}: it has its research, which is checked now, "
                       "or it is no artifact (moved, folded or deleted).",
    "owner-decides": "The owner decides the rule: keep it as it is, reword it, or drop it.",
    "unreadable-exemption": f"Make {EXEMPT_FILE} a JSON object: {{\"why\": …, \"topics\": [paths]}}.",
}
