"""Converting a topic to roles: give its parts roles, check it compiles to its
four skills, prove no sentence was lost, and fold a copy of it into it.

`cookr roles set|check|lossless` and `cookr fold` (modules/convert_roles.py,
modules/fold.py) are thin shells over this module.

A *sentence*, for `lossless` and for the fold's "does the topic lack this
text" test, is the pilot conversion's: each line of a part, list markers
stripped and whitespace collapsed, split after `.`, `!` or `?` where the next
sentence opens with a capital, a backtick or `*`. A sentence is kept when it
is a whole sentence of the topic's parts now (history excluded; struck text
and HTML comments removed, `unstruck`), on its own or
after a named rule's or rationale bullet's label (`now_sentences`), so a
sentence moved between parts, into a list or under a rule name still counts.
`lossless` reads no markdown-only line of the base (`_drop_markdown_only`):
a thematic break (`---`) or a heading that only restates the title (the
topic's or the copy's, now or at the base) says nothing to lose.

A sentence reworded on the way (into a named rule, say) is accounted for in
the topic's `lossless.json`, `{"base": rev, "copies": [...], "moved":
[{"sentence", "to", "judged"?, "retargeted"?}], "obsolete": [{"sentence",
"reason", "judged"?}], "retargets"?: [sentence, ...]}`. The gate does not prove meaning; it is an accounting plus
tripwires, and a judge's recorded, pinned verdict:

- `to` names at most three rules or non-rule parts that carry it now (a part
  judged by its best item or line). Together they hold at least 80% of its
  content words (function words dropped, light suffixes stemmed, rule names
  left out, `unlabeled`).
- Tripwires (`tripped`): each clause of the sentence (`clauses`: lines,
  sentences, `;`, `:`, dashes, parentheses, commas, " or ", " while ") is
  matched to the one clause of its targets that holds most of it, and that
  clause keeps its negations, its RFC 2119 levels, its numbers (number words
  too) and its FLIP_WORDS (a parenthetical gloss is read with the FLIP_WORD
  opening the clause it glosses when it holds none of its own,
  `_read_clauses`; a clause of keywords only joins its neighbour).
- A bare lead-in, or a framing one ("MUST follow:") whose rules all carry its
  level, passes on every rule it introduced instead (`lead_in`, `framing`,
  `_judge`), keeping its numbers; a framing's own words are all in its rules,
  one rule holding them all.
- `judged`, `{"by", "verdict": "pass"|"fail", "note", "pin"}`, is a judge's
  verdict. Its pin (`moved_pin`, `obsolete_pin`) is the sha256 of what the
  judge read, and the judge writes it with the verdict (`pin_for` prints it;
  nothing stamps one); a verdict whose pin is missing or differs is stale and
  counts as unjudged. A judged fail always fails; `require_judged` (the
  default; off for a draft) fails every reworded or obsolete entry with no
  fresh judged pass. A sentence equal to one whole sentence of a target
  (`verbatim_in`, normalised by `flat`: code spans kept as written, paired
  emphasis dropped) needs no judge.
- `retargeted`, `{"from", "to", "judged", "seal"}`, marks a moved entry whose
  judged fail named content carried by a rule or part not in its `to`: it was
  retargeted once, by `retarget` (`roles lossless --retarget`), the only
  writer of the record, which refuses a second. `from` is the `to` the entry
  had then, `judged` that fail, current (its pin matched `from`'s text), `to`
  the new targets (they exist, at most MAX_TARGETS, other than `from`), and
  `seal` (`_seal`) the sha256 of all four with the sentence, over canonical
  JSON. `retarget` refuses new targets that fail the 80% bar or a tripwire,
  writing nothing, so a bad target never spends the retarget. `retargets`, the
  file's ledger, names each sentence ever retargeted. A second retarget fails
  the entry by name (`_second_retarget`): a record whose seal does not match
  (written by hand), a `to` other than the record's, or a ledgered sentence
  with no record. Otherwise the entry is judged as any other: a fail whose pin
  matches fails it (the hard failure, no second retarget), a stale one is
  re-judged after the rewrite, and a pass clears it. An obsolete entry has no
  record.
- An obsolete sentence, one that only pointed at the topic it was folded into,
  must come from a copy (named in `copies` or `--copy`) and state no RFC
  keyword, negation or FLIP_WORD; it is shown, never silently passed.
- Every copy folded since the base is read (`_unread_copies`): a "Fold" history
  row's copy, and a same-named folder gone since the base, must be listed, and
  a listed copy must be gone.

An entry that accounts for nothing fails; one naming a sentence twice is
refused. No part names the file, so it never reaches a compiled doc or skill.
"""

from __future__ import annotations

import hashlib
import json
import re
import shutil
import subprocess
from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable, Optional

from . import history as hist
from .artifact import (
    HISTORY, INTRO, RESERVED, ROLES, ARTIFACT_FILE, Artifact, Part, _slug, compose_document,
    doc_path, dump_manifest, edit_text, find_folders, is_folder, load_folder, read_document,
    save_document,
)
from .bumping import BumpError, plan_against_base
from .markdown import uncited
from .errors import CookbookError
from .index import INDEX_FILE, IndexCache, current_index, load_index, save_index, sync_from_folders
from .linkedit import edit_links
from .roots import cookbook_of
from .roles import RULES as RULES_ROLE, census_of, part_units, rationale_texts, rule_names, rule_texts
from .skill import (
    TYPE_DIRS, SkillError, build, compose_all, templates_root, too_long,
)
from .versions import conflict, freeze

NONE = "none"   # `--part name=none` clears a part's role


class RoleworkError(CookbookError):
    """A conversion step that cannot be done; nothing was written."""


# ── where things are ────────────────────────────────────────────────────────

def _cookbook(folder: Path) -> Path:
    """The cookbook holding `folder` (roots.cookbook_of); refused outside one."""
    found = cookbook_of(folder)
    if found is None:
        raise RoleworkError(f"{folder}: not inside a cookbook (no cookbook.json and no "
                            f"{', '.join(TYPE_DIRS)} directory above it)")
    return found


def _folder(path: Path) -> Path:
    if not is_folder(path):
        raise RoleworkError(f"{path}: not an artifact source folder (no {ARTIFACT_FILE})")
    return path


# ── sentences ───────────────────────────────────────────────────────────────

_MARKER = re.compile(r"^\s*(?:[-*+]|\d+\.)\s+", re.M)
_SPLIT = re.compile(r"(?<=[.!?])\s+(?=[A-Z`*])")


def normalize(text: str) -> str:
    return re.sub(r"\s+", " ", _MARKER.sub("", text)).strip()


def sentences(text: str) -> list[str]:
    """Every sentence of `text`, in order (see the module docstring)."""
    return [s for line in text.splitlines() for s in _SPLIT.split(normalize(line)) if s]


def _now(artifact: Artifact) -> str:
    return normalize("\n".join(p.text for p in artifact.parts if p.name != HISTORY))


# A named rule's or a rationale bullet's label: `**name**: ` / `` `name`: `` / `` `a`, `b`: ``.
_NAME = r"(?:\*\*|`)[a-z0-9]+(?:-[a-z0-9]+)*(?:\*\*|`)"
_LABEL = re.compile(rf"^{_NAME}(?:,\s*{_NAME})*:\s+")


def unlabeled(text: str) -> str:
    """`text` with each line's list marker and rule or rationale label dropped,
    so a rule's name lends it no word, level or negation."""
    return "\n".join(_LABEL.sub("", normalize(line)) for line in text.splitlines())


def now_sentences(artifact: Artifact) -> set[str]:
    """Every sentence of the artifact's parts now (history excluded), each also
    without the label of the named rule or rationale bullet it opens. Struck
    text and HTML comments are not kept (`unstruck`, over each part whole)."""
    found = set()
    for p in artifact.parts:
        if p.name == HISTORY:
            continue
        for s in sentences(unstruck(p.text)):
            found.add(s)
            found.add(_LABEL.sub("", s))
    return found


# ── set ─────────────────────────────────────────────────────────────────────

def parse_spec(spec: str) -> tuple[str, Optional[str]]:
    name, sep, role = spec.partition("=")
    if not sep or not name.strip() or not role.strip():
        raise RoleworkError(f"--part {spec!r}: write it as <part>=<role> (role `{NONE}` clears it)")
    role = role.strip()
    return name.strip(), None if role == NONE else role


def set_roles(folder: Path, specs: Iterable[tuple[str, Optional[str]]],
              twin_differs: Optional[str] = None) -> Artifact:
    """Give each named part its role (None clears it) and write the manifest.
    Refuses, writing nothing, a part the folder lacks, a role not in ROLES, or a
    role on the intro or the history."""
    artifact = load_folder(_folder(folder))
    problems = []
    wanted = list(specs)
    for name, role in wanted:
        part = artifact.part(name)
        if part is None:
            problems.append(f"no part '{name}' (parts: {', '.join(p.name for p in artifact.parts)})")
        elif role is not None and name in (INTRO, HISTORY):
            problems.append(f"the {name} never carries a role")
        elif role is not None and role not in ROLES:
            problems.append(f"'{role}' is not a role ({', '.join(ROLES)}, or {NONE})")
    if problems:
        raise RoleworkError(f"{folder}: " + "; ".join(problems))
    for name, role in wanted:
        artifact.part(name).role = role
    if twin_differs is not None:
        artifact.twin_differs = twin_differs or None
    (folder / ARTIFACT_FILE).write_text(dump_manifest(artifact), encoding="utf-8")
    return artifact


# ── check ───────────────────────────────────────────────────────────────────

@dataclass
class CheckReport:
    folder: Path
    findings: list[tuple[str, str]] = field(default_factory=list)
    skills: list[dict] = field(default_factory=list)
    rules: int = 0

    @property
    def ok(self) -> bool:
        return not self.findings and len(self.skills) == 4

    def as_json(self) -> dict:
        return {"folder": str(self.folder), "ok": self.ok, "rules": self.rules,
                "findings": [{"kind": k, "detail": d} for k, d in self.findings],
                "skills": self.skills}


def check(folder: Path) -> CheckReport:
    """The role census of `folder` (name collisions judged against its whole
    cookbook) and, when it is clean, its four compiled skills with their sizes."""
    folder = _folder(folder)
    report = CheckReport(folder)
    artifact = load_folder(folder)
    if not artifact.roled:
        report.findings.append(("not-roled", "no part carries a role"))
        return report
    cookbook = _cookbook(folder)
    report.findings = [(f.kind, f.detail) for f in census_of(folder, cookbook)]
    report.rules = len(rule_names(artifact))
    if report.findings:
        return report
    templates = templates_root(cookbook) / "skill"
    try:
        skills = compose_all(folder, templates=templates, indexes=IndexCache(one_folder=True))
    except SkillError as e:
        report.findings.append(("compile", str(e)))
        return report
    built = [build(s, templates) for s in skills]
    for b in built:
        report.findings += [("compile", p) for p in b.problems]
    report.findings += [("too-long", f"{rel}: {n} lines") for rel, n in too_long(built).items()]
    report.skills = [{"kind": s.kind, "name": s.name, "chars": len(s.text),
                      "lines": s.text.count("\n")} for s in skills]
    return report


# ── lossless ────────────────────────────────────────────────────────────────

def _git(top: Path, *args: str) -> subprocess.CompletedProcess:
    return subprocess.run(["git", "-C", str(top), *args], capture_output=True, text=True)


def _top(path: Path) -> Path:
    here = Path(path).resolve()
    existing = next(d for d in (here, *here.parents) if d.is_dir())
    out = _git(existing, "rev-parse", "--show-toplevel")
    if out.returncode:
        raise RoleworkError(f"{path}: not in a git work tree")
    return Path(out.stdout.strip()).resolve()


def base_parts(folder: Path, rev: str) -> list[str]:
    """The text of each `.md` in `folder` at `rev`, history.md excluded.
    Refuses a revision git does not know and a folder `rev` lacks."""
    top = _top(folder)
    if _git(top, "rev-parse", "--verify", "--quiet", f"{rev}^{{commit}}").returncode:
        raise RoleworkError(f"--base {rev!r} is not a commit")
    rel = Path(folder).resolve().relative_to(top).as_posix()
    listed = _git(top, "ls-tree", "--name-only", f"{rev}:{rel}")
    if listed.returncode:
        raise RoleworkError(f"{rel} is not in {rev}")
    names = [n for n in listed.stdout.split() if n.endswith(".md") and n != f"{HISTORY}.md"]
    return [_git(top, "show", f"{rev}:{rel}/{n}").stdout for n in names]


ACCOUNTING = "lossless.json"   # beside artifact.json; never compiled (no part names it)
OVERLAP = 0.8                    # the cookbook gap measure's share, of content words
LEAD_IN = 8                      # most content words a bare lead-in ("Rules for X:") has
MAX_TARGETS = 3                  # most rules or parts one sentence (not a lead-in) may map to


# Function words carry no content of a sentence; negations and RFC keywords
# are kept, so "do not use it" still needs its `not`.
FUNCTION_WORDS = frozenset("""
a an the and or but if then so of to in on at by for with from as into onto than
that this these those it its they them their there here is are was were be been
being do does did has have had you your we our us i can will would which what
""".split())

# Words that only announce a list ("Rules for X:", "the following three"): a
# lead-in's own content is what is left without them.
LEAD_IN_WORDS = frozenset("""
rule rules follow following followed below above list these those three two four
five six seven eight nine ten several some all each every step steps here
""".split())

# Words that announce a list of rules ("MUST follow:", "these rules", "any"): a
# normative lead-in with one of them only frames the rules it introduces.
FRAMING_WORDS = frozenset("rule rules follow following followed below these".split())
FRAMING_GENERIC = LEAD_IN_WORDS | {"any", "apply", "applies"}
RFC_WORDS = frozenset("must shall should may not never required recommended optional".split())

# Negation, and RFC 2119 levels (negated ones matched first). Upper-case MAY and
# OPTIONAL only: lower-case "may" is nearly always "might". "without" is a
# negation for `negated` (a lead-in, an obsolete sentence) but is counted as a
# meaning word on the matched clause, so it never stands in for a lost "never".
_NEGATION = re.compile(r"\b(?:not|never|no|cannot|without|nor|none)\b|n't\b", re.I)
_NEGATOR = re.compile(r"\b(?:not|never|no|cannot|nor|none)\b|n't\b", re.I)
_LEVELS = (
    ("MUST NOT", re.compile(r"\b(?:must|shall)(?:\s+not|\s+never|n't)\b|\bmay\s+NOT\b", re.I)),
    ("SHOULD NOT", re.compile(r"\bshould(?:\s+not|\s+never|n't)\b|\bNOT\s+RECOMMENDED\b", re.I)),
    ("MUST", re.compile(r"\b(?:must|shall|required)\b", re.I)),
    ("SHOULD", re.compile(r"\b(?:should|recommended)\b", re.I)),
    ("MAY", re.compile(r"\b(?:MAY|OPTIONAL)\b")),
)
_UNIT = (r"%|x|ms|s|sec|secs|seconds?|minutes?|mins?|hours?|hrs?|h|days?|weeks?|bytes?|bits?|"
         r"[kmgt]i?b|[kmgt]bps|bit|rows?|times")
_NUMBER = re.compile(rf"(?<![a-z0-9.])(\d+(?:[.,]\d+)*)\s?-?\s?({_UNIT})?(?![a-z0-9])", re.I)
# One spelling per unit, so "5 min" and "5 minutes" are one number.
_UNIT_ALIAS = {"sec": "s", "secs": "s", "second": "s", "seconds": "s", "min": "min", "mins": "min",
               "minute": "min", "minutes": "min", "hour": "h", "hours": "h", "hr": "h", "hrs": "h",
               "day": "d", "days": "d", "week": "w", "weeks": "w", "byte": "b", "bytes": "b",
               "bit": "bit", "bits": "bit", "row": "row", "rows": "row", "times": "x"}

# Number words count as numbers: "three" is 3, "twice" is 2x, "half" is 0.5.
_SMALL = ("zero one two three four five six seven eight nine ten eleven twelve thirteen fourteen "
          "fifteen sixteen seventeen eighteen nineteen twenty").split()
_TENS = {w: 10 * n for n, w in enumerate("_ _ twenty thirty forty fifty sixty seventy eighty ninety"
                                          .split()) if w != "_"}
_SCALE = {"hundred": 100, "thousand": 1000, "million": 1000000}
_ALONE = {"once": "1x", "twice": "2x", "single": "1", "double": "2x", "half": "0.5"}
_NUMBER_WORD = "|".join([*_SMALL, *_TENS, *_SCALE])
_NUMBER_WORDS = re.compile(rf"\b(?:{_NUMBER_WORD})(?:[\s-]+(?:{_NUMBER_WORD}))*\b|"
                           rf"\b(?:{'|'.join(_ALONE)})\b", re.I)

# Words that turn a rule's meaning when swapped or dropped: a source clause's
# one must be in its matched clause. Each is (name, pattern).
FLIP_WORDS = tuple((w, re.compile(p, re.I)) for w, p in (
    ("avoid", r"\bavoid(?:s|ed|ing|ance)?\b"), ("only", r"\bonly\b"),
    ("at least", r"\bat\s+least\b"), ("at most", r"\bat\s+most\b"),
    ("before", r"\bbefore\b"), ("after", r"\bafter\b"), ("until", r"\buntil\b"),
    ("unless", r"\bunless\b"), ("except", r"\bexcept\b"), ("without", r"\bwithout\b"),
    ("instead", r"\binstead\b"), ("prefer", r"\bprefer(?:s|red|ring|ably|able|ence|ences)?\b"),
    ("minimum", r"\bminimum\b"), ("maximum", r"\bmaximum\b"),
    ("more than", r"\bmore\s+than\b"), ("less than", r"\bless\s+than\b"),
    ("fewer than", r"\bfewer\s+than\b"),
))


def _words(text: str) -> list[str]:
    """The gap measure's words: lower-cased runs of letters and digits."""
    return re.sub(r"[^a-z0-9]+", " ", text.lower()).split()


def _stem(word: str) -> str:
    """A light suffix strip, so 'used'/'use', 'causes'/'cause' and
    'migrations'/'migration' count as one word; digits are left alone."""
    if word.isdigit() or len(word) <= 3:
        return word
    if word.endswith("sses"):
        word = word[:-2]
    elif word.endswith("ies") and len(word) > 4:
        word = word[:-3] + "y"
    elif word.endswith("s") and not word.endswith(("ss", "us", "is")):
        word = word[:-1]
    if word.endswith("ing") and len(word) > 5:
        word = word[:-3]
    elif word.endswith("ed") and len(word) > 4:
        word = word[:-2]
    return word.rstrip("e") or word


def content_words(text: str) -> list[str]:
    """The gap measure's words of `text`, function words dropped."""
    return [w for w in _words(text) if w not in FUNCTION_WORDS]


def _verbatim(sentence: str, target: str) -> bool:
    """`sentence`'s words appear as a whole run of `target`'s words."""
    return f" {' '.join(_words(sentence))} " in f" {' '.join(_words(target))} "


def overlap(sentence: str, target: str, words: Optional[list[str]] = None) -> float:
    """The share of `sentence`'s content words (or `words`) that `target`
    holds, compared after `_stem`: 1.0 for a sentence with none, or one
    `target` holds whole, as the gap measure."""
    if _verbatim(sentence, target):
        return 1.0
    words = content_words(sentence) if words is None else words
    if not words:
        return 1.0
    held = {_stem(w) for w in _words(target)}
    return sum(_stem(w) in held for w in words) / len(words)


def negated(text: str) -> bool:
    return bool(_NEGATION.search(text))


def levels(text: str) -> set[str]:
    """The RFC 2119 levels `text` states."""
    found = set()
    for level, pattern in _LEVELS:
        if pattern.search(text):
            found.add(level)
            text = pattern.sub(" ", text)
    return found


def _number_value(words: str) -> str:
    """The digits a run of number words spells ("twenty-five" 25, "three
    hundred" 300, "once" 1x)."""
    low = words.lower()
    if low in _ALONE:
        return _ALONE[low]
    total = current = 0
    for w in re.split(r"[\s-]+", low):
        if w in _SCALE:
            current = (current or 1) * _SCALE[w]
            if _SCALE[w] >= 1000:
                total, current = total + current, 0
        elif w in _TENS:
            current += _TENS[w]
        else:
            current += _SMALL.index(w)
    return str(total + current)


def _digits(text: str) -> str:
    return _NUMBER_WORDS.sub(lambda m: _number_value(m.group(0)), text)


def numbers(text: str) -> set[str]:
    """Every number in `text`, number words as digits, with the unit or `%`
    written beside it (one spelling per unit)."""
    found = set()
    for n, u in _NUMBER.findall(_digits(text)):
        u = (u or "").lower()
        found.add(f"{n.replace(',', '')}{_UNIT_ALIAS.get(u, u)}")
    return found


def negations(text: str) -> int:
    """How many negations `text` states ("without" aside: it is a FLIP_WORD)."""
    return len(_NEGATOR.findall(text))


def flips(text: str) -> set[str]:
    """The FLIP_WORDS `text` holds."""
    return {w for w, pattern in FLIP_WORDS if pattern.search(text)}


_EMPHASIS = re.compile(r"\*\*|__|(?<!\w)[*_](?=\S)|(?<=\S)[*_](?!\w)")
# Text that does not say anything now: a struck-through span, an HTML
# comment; either may cover several sentences and lines.
_STRUCK = re.compile(r"~~.*?~~|<!--.*?-->", re.S)
# Sentence ends; `;` and `:`; an em dash, or a spaced en dash (an unspaced one
# is a range, "500–1000ms"); a parenthesis; a comma; " or " and " while ".
_CLAUSE_SPLIT = re.compile(r"(?<=[.!?])\s+(?=[A-Z`(\"'])|[;:]\s+|\s*—\s*|\s+–\s+|"
                           r"\s+\(|\)(?=[\s.,;:!?]|$)|,\s+|\s+(?:or|while)\s+")


def unstruck(text: str) -> str:
    """`text` with its struck-through spans (`~~…~~`) and HTML comments
    (`<!-- … -->`) removed, across lines: what it no longer says; and with each
    rule's research citation removed (`uncited`), which says where a rule came
    from, not what it says, so a rule that gains one is still verbatim. The one
    removal for the sentences kept now, the clauses and the verbatim test."""
    return uncited(_STRUCK.sub("", text))


def clauses(text: str) -> list[str]:
    """`text` split into clauses: each line (a bullet or item), its sentences,
    and their parts at `;`, `:`, a dash, a parenthesis, a comma, " or " and
    " while "; emphasis markers and struck-through text dropped."""
    return [c for c, _ in _read_clauses(text)]


# A parenthetical gloss: " (…)" ending at a space, punctuation or the line's end.
_GLOSS = re.compile(r"(\s\([^()]*\))(?=[\s.,;:!?]|$)")


def _opening_flips(clause: str) -> set[str]:
    """The FLIP_WORDS that open `clause` ("After applying …" opens with "after")."""
    return {w for w, pattern in FLIP_WORDS if pattern.match(clause)}


# The meaning words a gloss may inherit from the clause it glosses: the
# ordering ones, whose phrase ("after applying server records") a gloss can
# restate. "only" binds to what follows it, never to an aside.
GLOSS_INHERITS = frozenset({"before", "after", "until"})
# A clause with only these words says nothing on its own ("Never", "MUST NOT").
_KEYWORDS = RFC_WORDS | {"no", "cannot", "nor", "none"}


def _bare(clause: str) -> bool:
    """`clause` holds no content word but RFC keywords and negations."""
    return all(w in _KEYWORDS for w in content_words(clause))


def _joined(pieces: list[str]) -> list[str]:
    """`pieces`, each one that is only keywords ("Never", "MUST") joined to the
    one after it, or at the end to the one before, so it never stands alone."""
    out: list[str] = []
    carry = ""
    for c in pieces:
        c = f"{carry} {c}" if carry else c
        if _bare(c):
            carry = c
            continue
        carry = ""
        out.append(c)
    if carry:
        if out:
            out[-1] = f"{out[-1]} {carry}"
        else:
            out.append(carry)
    return out


def _read_clauses(text: str) -> list[tuple[str, set[str]]]:
    """`clauses(text)`, each with the FLIP_WORDS it is read with besides its
    own: a parenthetical gloss restates the clause it follows, so it is read
    with the ordering FLIP_WORD (GLOSS_INHERITS) that opens that clause ("After
    applying server records (step 5 of the sync cycle)" says "after step 5"),
    unless it holds a FLIP_WORD of its own. Nothing else carries over. A clause
    of keywords only joins its neighbour (`_joined`)."""
    found: list[tuple[str, set[str]]] = []

    def split(segment: str, inherited: set[str]) -> None:
        pieces = [c.strip() for c in _CLAUSE_SPLIT.split(segment)]
        for c in _joined([c for c in pieces if re.search(r"\w", c)]):
            found.append((c, inherited))

    for line in unstruck(text).splitlines():
        host: set[str] = set()
        for i, segment in enumerate(_GLOSS.split(_EMPHASIS.sub("", normalize(line)))):
            if i % 2:
                gloss = segment.strip()[1:-1]
                split(gloss, set() if flips(gloss) else host & GLOSS_INHERITS)
            else:
                start = len(found)
                split(segment, set())
                if len(found) > start:
                    host = _opening_flips(found[-1][0])
    return found


def _matched(clause: str, candidates: list[str]) -> str:
    """The candidate clause that holds most of `clause`; a tie goes to the one
    `clause` holds most of (the tighter match)."""
    return max(candidates, key=lambda c: (overlap(clause, c), overlap(c, clause)))


def tripped(sentence: str, texts: list[str]) -> list[str]:
    """What each clause of `sentence` loses in the one clause of `texts` it is
    matched to: a negation, an RFC 2119 level, a number, a FLIP_WORD (a gloss
    keeps the one that opens the clause it glosses, `_read_clauses`)."""
    read: dict[str, set[str]] = {}       # a clause read twice keeps only what both readings carry
    for c, inherited in (c for t in texts for c in _read_clauses(t)):
        read[c] = read[c] & inherited if c in read else inherited
    candidates = list(read) or [""]
    lost = []
    for clause in clauses(sentence):
        match = _matched(clause, candidates)
        why = []
        if negations(clause) > negations(match):
            why.append("its negation")
        gone = levels(clause) - levels(match)
        if gone:
            why.append("its " + ", ".join(sorted(gone)))
        gone = numbers(clause) - numbers(match)
        if gone:
            why.append("the number(s) " + ", ".join(sorted(gone)))
        gone = flips(clause) - flips(match) - read.get(match, set())
        if gone:
            why.append("the word(s) " + ", ".join(map(repr, sorted(gone))))
        if why:
            lost.append(f"{'; '.join(why)} (in {match!r})")
    return lost


# A code span: a run of backticks, its text, the same run (CommonMark).
_CODE = re.compile(r"(?<!`)(`+)(?!`)(.+?)(?<!`)\1(?!`)")
# A pair of emphasis markers around words: opened where no word or marker
# precedes it and text follows, closed where text precedes it and no word or
# marker follows. A lone `_` or `*`, or one inside a word, is no marker.
_PAIRED = re.compile(r"(?<![\w*_])(\*\*|__|\*|_)(?=[^\s*_])(.+?)(?<=[^\s*_])\1(?![\w*_])")


def _unemphasised(prose: str) -> str:
    """`prose` (no code in it) with each pair of emphasis markers dropped,
    innermost last ("**a *b* c**")."""
    while True:
        out = _PAIRED.sub(r"\2", prose)
        if out == prose:
            return out
        prose = out


_HELD = "\ue000"   # where a code span sits while the prose around it is normalised


def flat(text: str) -> str:
    """`text` normalised for the verbatim test and the pin: struck-through
    text and HTML comments removed (`unstruck`), list markers dropped, paired
    emphasis markers dropped, whitespace collapsed outside code, and each code
    span's backticks dropped with its text kept exactly as written."""
    lines = []
    for line in unstruck(text).splitlines():
        code = [m.group(2) for m in _CODE.finditer(line)]
        prose = _CODE.sub(_HELD, _MARKER.sub("", line).replace(_HELD, ""))
        prose = re.sub(r"\s+", " ", _unemphasised(prose).replace("`", "")).strip()
        held = iter(code)
        line = re.sub(_HELD, lambda _: next(held), prose)
        if line:
            lines.append(line)
    return " ".join(lines)


def verbatim_in(sentence: str, target: str) -> bool:
    """`sentence`, normalised (`flat`), equals one whole sentence of `target`,
    normalised. A sentence inside a longer one, or only in struck-through
    text, is not verbatim."""
    s = flat(sentence)
    return bool(s) and any(flat(t) == s for t in sentences(unstruck(target)))


@dataclass
class LosslessReport:
    checked: int = 0
    missing: list[str] = field(default_factory=list)     # absent, and not accounted for
    moved: list[dict] = field(default_factory=list)      # accounted for, and the target carries it
    obsolete: list[dict] = field(default_factory=list)   # absent on purpose, with the reason
    failures: list[dict] = field(default_factory=list)   # accounted for, but the account fails
    unused: list[dict] = field(default_factory=list)     # accounts for no absent sentence: fails
    copies: list[str] = field(default_factory=list)      # copies read (--copy and lossless.json's), from the repo root
    counts: dict = field(default_factory=lambda: dict.fromkeys(JUDGED_COUNTS, 0))
    draft: bool = False                                  # judged verdicts not required (--draft)

    @property
    def ok(self) -> bool:
        return not self.missing and not self.failures and not self.unused


# How each entry stands with the judge. A moved entry is word for word one
# sentence of a target (no judge needed), reworded with a judged pass, reworded
# and not yet judged, or judged fail (a failure, draft or not). `stale` counts
# the verdicts whose pin is missing or no longer matches: each also counts as
# unjudged. An obsolete entry is judged (a pinned pass) or unjudged.
JUDGED_COUNTS = ("verbatim", "reworded_judged", "reworded_unjudged", "judged_fail", "stale",
                 "obsolete_judged", "obsolete_unjudged")
VERDICTS = ("pass", "fail")
_PIN = re.compile(r"[0-9a-f]{64}")


def _commit(folder: Path, rev: str) -> Optional[str]:
    out = _git(_top(folder), "rev-parse", "--verify", "--quiet", f"{rev}^{{commit}}")
    return out.stdout.strip() if not out.returncode else None


def _targets(to) -> list[str]:
    """`to` as a list of names: one name, or a non-empty list of them; [] when malformed."""
    if isinstance(to, str) and to:
        return [to]
    if isinstance(to, list) and to and all(isinstance(t, str) and t for t in to):
        return list(to)
    return []


def lead_in(sentence: str) -> bool:
    """A bare lead-in: a sentence ending in a colon (bold or not), with no RFC
    keyword and no negation and at most LEAD_IN content words, which
    introduces the rules below it."""
    return (sentence.rstrip("* ").endswith(":") and not levels(sentence)
            and not negated(sentence) and len(content_words(sentence)) <= LEAD_IN)


def framing(sentence: str) -> bool:
    """A framing lead-in: a sentence ending in a colon, with at most LEAD_IN
    content words, an RFC 2119 level, a word that announces the rules below it
    (FRAMING_WORDS), and no negation beyond its level's own NOT ("MUST follow:",
    "MUST follow these rules for any migration in a sync schema:")."""
    if not sentence.rstrip("* ").endswith(":") or len(content_words(sentence)) > LEAD_IN:
        return False
    rest = sentence
    for _, pattern in _LEVELS:
        rest = pattern.sub(" ", rest)
    return (bool(levels(sentence)) and not negated(rest)
            and any(w in FRAMING_WORDS for w in _words(sentence)))


def _judged_ok(judged) -> bool:
    """A `judged` record: {"by": str, "verdict": "pass"|"fail", "note": str,
    "pin"?: 64 hex digits}."""
    return (isinstance(judged, dict) and isinstance(judged.get("by"), str) and judged["by"].strip()
            and judged.get("verdict") in VERDICTS and isinstance(judged.get("note"), str)
            and ("pin" not in judged or (isinstance(judged["pin"], str)
                                         and _PIN.fullmatch(judged["pin"]) is not None)))


def _entries(data: dict, key: str, target: str) -> bool:
    items = data.get(key, [])
    return isinstance(items, list) and all(
        isinstance(m, dict) and isinstance(m.get("sentence"), str)
        and ("judged" not in m or _judged_ok(m["judged"]))
        and (bool(_targets(m.get("to"))) if target == "to"
             else isinstance(m.get("reason"), str) and bool(m["reason"].strip())
             and "retargeted" not in m)
        for m in items)


def read_accounting(folder: Path) -> Optional[dict]:
    """`<folder>/lossless.json` — `{"base": rev, "copies": [path at rev, from the
    repo root], "moved": [{"sentence", "to", "judged"?, "retargeted"?}],
    "obsolete": [{"sentence", "reason", "judged"?}], "retargets"?: [sentence,
    ...]}`, `judged` being `{"by", "verdict": "pass"|"fail", "note", "pin"?}`
    and `retargeted` the record `retarget` writes (its content is checked by
    `lossless`, by name) — or None when there is none. A malformed one (an
    obsolete entry with a `retargeted` record, a `retargets` other than a list
    of sentences), or one naming a sentence twice, is refused."""
    path = Path(folder) / ACCOUNTING
    if not path.is_file():
        return None
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        raise RoleworkError(f"{path}: not JSON ({e})") from e
    copies = data.get("copies", []) if isinstance(data, dict) else None
    if (not isinstance(data, dict) or not isinstance(data.get("base"), str)
            or not isinstance(copies, list) or not all(isinstance(c, str) and c for c in copies)
            or not isinstance(data.get("moved", []), list)
            or not _entries(data, "moved", "to") or not _entries(data, "obsolete", "reason")
            or not (isinstance(data.get("retargets", []), list)
                    and all(isinstance(s, str) and s.strip() for s in data.get("retargets", [])))):
        judged = '{"by": "...", "verdict": "pass" or "fail", "note": "...", "pin": "<sha256>"}'
        raise RoleworkError(f'{path}: expected {{"base": "<rev>", "copies": ["<folder at rev>", ...], '
                            f'"moved": [{{"sentence": "...", '
                            f'"to": "<rule or part>" or ["<rule or part>", ...], '
                            f'"judged" (optional): {judged}, '
                            f'"retargeted" (optional, written by --retarget only)}}], '
                            f'"obsolete": [{{"sentence": "...", "reason": "...", '
                            f'"judged" (optional): {judged}}}], '
                            f'"retargets" (optional, written by --retarget only): ["<sentence>", ...]}}')
    seen: set[str] = set()
    for m in [*data.get("moved", []), *data.get("obsolete", [])]:
        s = normalize(m["sentence"])
        if s in seen:
            raise RoleworkError(f"{path}: accounts for {s!r} more than once")
        seen.add(s)
    return data


def _best_unit(sentence: str, part: Part) -> str:
    """The one item or line of `part` that holds most of `sentence`."""
    units = part_units(part) or [""]
    return max(units, key=lambda u: overlap(sentence, u))


def _judge(s: str, names: list[str], artifact: Artifact, rules: dict[str, str],
           why: dict[str, str]) -> tuple[Optional[str], Optional[str]]:
    """(why the mapping of `s` to `names` fails, or None; "lead_in" or
    "framing" when it passed as one). A lead-in may name every rule it
    introduced; any other mapping names at most MAX_TARGETS."""
    shaped = lead_in(s) or framing(s)
    if not shaped and len(names) > MAX_TARGETS:
        return f"maps to {len(names)} targets; at most {MAX_TARGETS}", None
    parts = {p.name: p for p in artifact.parts if p.name != HISTORY and p.role != RULES_ROLE}
    gone = [n for n in names if n not in rules and n not in parts]
    if gone:
        return f"no rule or non-rule part named {', '.join(map(repr, gone))}", None
    if shaped:
        if not all(n in rules for n in names):
            return "a lead-in maps to the rules it introduced", None
        kind = "lead_in" if lead_in(s) else "framing"
        if kind == "framing":
            need = levels(s)
            weaker = [n for n in names if not need <= levels(rules[n])]
            if weaker:
                return (f"framing lead-in ({', '.join(sorted(need))}): "
                        f"{', '.join(map(repr, weaker))} lack(s) that level"), None
        carried = "\n".join(rules[n] + "\n" + why.get(n, "") for n in names)
        generic = LEAD_IN_WORDS if kind == "lead_in" else FRAMING_GENERIC | RFC_WORDS
        own = [w for w in content_words(s) if w not in generic]
        wrong = []
        # A bare lead-in's words may be its rules' names ("Access methods:" ->
        # `platform-access-methods`): each name, split at its hyphens, counts.
        named = carried + "\n" + "\n".join(n.replace("-", " ") for n in names)
        if kind == "lead_in" and own and overlap(s, named, own) < OVERLAP:
            lacks = sorted({w for w in own if _stem(w) not in {_stem(x) for x in _words(named)}})
            wrong.append(f"its rules (their names and rationale) lack {', '.join(lacks)}")
        if kind == "framing" and own:
            # Every one of its own words is in its rules, and one rule (with its
            # rationale) holds them all: the framing's phrase survives whole, not
            # scattered a word per rule. A rule broader than the framing's scope
            # ("each migration", under "any migration in a sync schema") may
            # leave the scope out.
            lacks = sorted({w for w in own if _stem(w) not in {_stem(x) for x in _words(carried)}})
            if lacks:
                wrong.append(f"its rules (and their rationale) lack {', '.join(lacks)}")
            elif not any({_stem(w) for w in own} <= {_stem(x) for x in _words(rules[n] + "\n" + why.get(n, ""))}
                         for n in names):
                wrong.append(f"no one rule (with its rationale) holds all of {', '.join(own)}")
        gone = numbers(s) - numbers(carried)
        if gone:
            wrong.append(f"its rules (and their rationale) drop the number(s) {', '.join(sorted(gone))}")
        if wrong:
            return f"{kind.replace('_', '-')}: " + "; ".join(wrong), None
        return None, kind
    texts = [rules[n] if n in rules else unlabeled(_best_unit(s, parts[n])) for n in names]
    target = "\n".join(texts)
    share = overlap(s, target)
    if share < OVERLAP:
        return (f"{names if len(names) > 1 else names[0]!r} holds {share:.0%} of its content "
                f"words; at least {OVERLAP:.0%} needed"), None
    if len(texts) > 1:
        idle = [n for n, t in zip(names, texts) if overlap(s, t) == 0]
        if idle:
            return f"{', '.join(map(repr, idle))} hold(s) none of its content words", None
    lost = tripped(s, texts)
    if lost:
        return "the matched clause drops " + " | ".join(lost), None
    return None, None


# ── pins ────────────────────────────────────────────────────────────────────
#
# A judged verdict holds the pin of what the judge read, which the judge
# writes with its verdict (`pin_for` prints it). The pin of a moved entry is
# the sha256 of the JSON `[sentence, sorted to-list, the flat full text of each
# target in that order]`; of an obsolete entry, of `[sentence, the copy it came
# from (from the repo root), reason, the flat full text of the topic's parts
# (history excluded)]`. A verdict whose pin is missing or differs is stale, and
# counts as unjudged.

def _sha(payload: list) -> str:
    return hashlib.sha256(json.dumps(payload, ensure_ascii=False).encode("utf-8")).hexdigest()


def _target_text(name: str, rules: dict[str, str], artifact: Artifact) -> Optional[str]:
    """A target's full text: the rule's (its label dropped), or the non-rule
    part's whole; None when there is no such rule or part."""
    if name in rules:
        return rules[name]
    part = next((p for p in artifact.parts if p.name == name and p.name != HISTORY
                 and p.role != RULES_ROLE), None)
    return None if part is None else unlabeled(part.text)


def moved_pin(sentence: str, to, rules: dict[str, str], artifact: Artifact) -> Optional[str]:
    """The pin of a moved entry, or None when a target does not exist."""
    names = sorted(_targets(to))
    texts = [_target_text(n, rules, artifact) for n in names]
    if not names or any(t is None for t in texts):
        return None
    return _sha([normalize(sentence), names, [flat(t) for t in texts]])


def topic_text(artifact: Artifact) -> str:
    """The topic's text an obsolete sentence is judged against: its parts
    (history excluded), whole, `flat`."""
    return flat("\n".join(p.text for p in artifact.parts if p.name != HISTORY))


def obsolete_pin(sentence: str, copy: str, reason: str, topic: str) -> str:
    """The pin of an obsolete entry: its sentence, the copy it came from, its
    reason, and the topic text (`topic_text`) that made it redundant."""
    return _sha([normalize(sentence), copy, reason, topic])


# Why a verdict is stale.
NO_PIN, CHANGED = "no pin", "changed"


def _verdict(judged: Optional[dict], pin: Optional[str]) -> tuple[Optional[dict], Optional[str]]:
    """(the verdict that stands — None when unjudged or stale —, why it is
    stale: NO_PIN, CHANGED, or None)."""
    if not judged:
        return None, None
    if "pin" not in judged:
        return None, NO_PIN
    if pin is None or judged["pin"] != pin:
        return None, CHANGED
    return judged, None


def _stale_reason(kind: str, stale: str) -> str:
    """The failure of a reworded or obsolete entry whose verdict is stale."""
    if stale == NO_PIN:
        return f"{kind}, and its judged verdict is stale (no pin): re-judge it and write its pin"
    return (f"{kind}, and its judged verdict is stale (the text it judged has changed since it was "
            f"pinned): re-judge it")


def _seal(sentence: str, record) -> Optional[str]:
    """The seal `retarget` writes into a `retargeted` record: the sha256 of the
    sentence, `from`, `to` and the fail, taken over canonical JSON (sorted
    keys, fixed separators) so a file re-serialised with other key order or
    spacing keeps it; or None when the record is not that shape (from and to
    named targets, judged a pinned fail)."""
    if not isinstance(record, dict):
        return None
    old, new, judged = _targets(record.get("from")), _targets(record.get("to")), record.get("judged")
    if not (old and new and _judged_ok(judged) and judged["verdict"] == "fail" and "pin" in judged):
        return None
    payload = ["retarget", normalize(sentence), sorted(old), sorted(new), judged]
    return hashlib.sha256(json.dumps(payload, ensure_ascii=False, sort_keys=True,
                                     separators=(",", ":")).encode("utf-8")).hexdigest()


def _second_retarget(s: str, m: dict, ledger: set[str]) -> Optional[str]:
    """Why moved entry `m` (sentence `s`) shows a second retarget, or None: a
    `retargeted` record `retarget` did not write (its seal does not match), a
    `to` other than the one it was retargeted to, or a sentence the ledger
    names with no record."""
    refused = "a second retarget is refused (an entry is retargeted once, by `roles lossless --retarget`)"
    if "retargeted" not in m:
        return (f"retargeted once (lossless.json's `retargets` names it) but its `retargeted` record is "
                f"gone: {refused}" if s in ledger else None)
    r = m["retargeted"]
    seal = _seal(s, r)
    if seal is None or not isinstance(r, dict) or r.get("seal") != seal:
        return f"its `retargeted` record was not written by `--retarget` (its seal does not match): {refused}"
    if sorted(_targets(m["to"])) != sorted(_targets(r["to"])):
        return (f"its `to` {m['to']!r} is not the {r['to']!r} it was retargeted to "
                f"from {r['from']!r}: {refused}")
    return None


# ── what was read at the base ───────────────────────────────────────────────

@dataclass
class _Base:
    copies: list[Path]                 # the copies read, resolved
    absent: list[str]                  # base sentences in no part now, in order
    own: set[str]                      # the topic's own base sentences: never obsolete
    origin: dict[str, str]             # a copy's sentence -> the copy it came from (from the repo root)
    checked: int


def _rel(path: Path, top: Path) -> str:
    return path.relative_to(top).as_posix() if path.is_relative_to(top) else str(path)


_THEMATIC_BREAK = re.compile(r"^\s*([-*_])(?:\s*\1){2,}\s*$")
_HEADING = re.compile(r"^\s*#{1,6}\s+(.*?)\s*#*\s*$")


def _drop_markdown_only(text: str, titles: set[str]) -> str:
    """`text` without its markdown-only lines, which say nothing a reader would
    lose: a thematic break (`---`, `***`, `___`) and a heading whose text only
    restates one of `titles` (case ignored). Any other heading is kept."""
    folded = {t.strip().casefold() for t in titles}
    def says_nothing(line: str) -> bool:
        if _THEMATIC_BREAK.match(line):
            return True
        m = _HEADING.match(line)
        return bool(m) and m.group(1).casefold() in folded
    return "\n".join(line for line in text.splitlines() if not says_nothing(line))


def _base_title(folder: Path, rev: str) -> Optional[str]:
    """`folder`'s meta title at `rev` (None when git or the JSON cannot say)."""
    top = _top(folder)
    shown = _git(top, "show", f"{rev}:{_rel(Path(folder).resolve(), top)}/{ARTIFACT_FILE}")
    if shown.returncode:
        return None
    try:
        title = json.loads(shown.stdout).get("meta", {}).get("title")
    except (ValueError, AttributeError):
        return None
    return title if isinstance(title, str) else None


def _read_base(folder: Path, rev: str, copies: Iterable[Path], accounting: Optional[dict]) -> _Base:
    top = _top(folder)
    wanted = [Path(c).resolve() for c in copies]
    wanted += [top / c for c in (accounting or {}).get("copies", [])]
    read = list(dict.fromkeys(p.resolve() for p in wanted))
    current = load_folder(folder)
    now = now_sentences(current)
    absent: list[str] = []
    own: set[str] = set()
    origin: dict[str, str] = {}
    checked = 0
    for old in (folder, *read):
        titles = {t for t in (current.meta.get("title"), _base_title(old, rev)) if t}
        for text in base_parts(old, rev):
            for s in sentences(_drop_markdown_only(text, titles)):
                checked += 1
                if old is folder:
                    own.add(s)
                else:
                    origin.setdefault(s, _rel(old, top))
                if s not in now and s not in absent:
                    absent.append(s)
    return _Base(read, absent, own, origin, checked)


# A history row's fold, as `fold` writes it ("Fold <path> into this topic…",
# or "…; Fold <path> into this topic…" when the row already existed).
_FOLD_ROW = re.compile(r"(?:^|[|;])\s*Fold (\S+) into this topic")


def _unread_copies(folder: Path, rev: str, read: list[Path]) -> list[str]:
    """Why a copy folded since `rev` would go unread, one reason each:
    a "Fold <path>" history row added since `rev` whose copy is not read; an
    artifact folder at `rev` that is gone now and has the topic's folder name
    (a twin) that is not read; a read copy that still exists (not folded)."""
    top = _top(folder)
    folder = Path(folder).resolve()
    listed = set(read)
    cookbook = _cookbook(folder)
    why = []
    hist_file = folder / f"{HISTORY}.md"
    now_rows = hist_file.read_text(encoding="utf-8").splitlines() if hist_file.is_file() else []
    at_base = _git(top, "show", f"{rev}:{_rel(hist_file, top)}")
    base_rows = set(at_base.stdout.splitlines()) if not at_base.returncode else set()
    for row in now_rows:
        if row in base_rows:
            continue
        for m in _FOLD_ROW.finditer(row):
            path = (cookbook / m.group(1)).resolve()
            if path not in listed:
                why.append(f"folded copy {_rel(path, top)} is not read: add it to \"copies\"")
    listed_at_base = _git(top, "ls-tree", "-r", "--name-only", rev, "--", _rel(cookbook, top))
    for line in listed_at_base.stdout.splitlines():
        if not line.endswith(f"/{ARTIFACT_FILE}"):
            continue
        twin = (top / line).parent.resolve()
        if twin.name == folder.name and twin != folder and not twin.exists() and twin not in listed:
            why.append(f"folded copy {_rel(twin, top)} (a twin of this topic, gone since --base) "
                       f"is not read: add it to \"copies\"")
    for c in read:
        if c.exists():
            why.append(f"copy {_rel(c, top)} still exists: a copy is a folder folded away since --base")
    return list(dict.fromkeys(why))


def lossless(folder: Path, rev: str, copies: Iterable[Path] = (),
             require_judged: bool = True) -> LosslessReport:
    """Each sentence of `folder` and `copies` at `rev` that is no sentence of
    `folder` now passes only when `folder`'s lossless.json (its `copies` read
    as `copies`) accounts for it:

    - `moved` to at most MAX_TARGETS rules, or non-rule parts (judged by the one
      item or line that holds most of it), that exist and together hold at
      least OVERLAP of its content words, each of its clauses keeping its
      negations, RFC 2119 levels, numbers and FLIP_WORDS in its matched clause
      (`tripped`); a lead-in or framing lead-in mapped to the rules it
      introduced passes when they carry its words and numbers, and is marked;
      a `judged` fail fails it; and unless it is word for word one sentence of
      a target (`verbatim_in`), `require_judged` (the default; off for a
      draft) fails it without a judged pass whose pin matches;
    - or `obsolete` with a reason: a copy's sentence only, with no RFC
      keyword, negation or FLIP_WORD, and (with `require_judged`) a judged
      pass whose pin matches.

    Every copy folded since `rev` is read: a "Fold" history row's copy, and a
    same-named twin folder gone since `rev`, must be listed, and a listed copy
    must be gone (`_unread_copies`). Unaccounted sentences are `missing`;
    failed accounts are `failures`; entries for no absent sentence are
    `unused`. `counts` tallies the entries by JUDGED_COUNTS."""
    folder = _folder(folder)
    artifact = load_folder(folder)
    report = LosslessReport(draft=not require_judged)
    accounting = read_accounting(folder)
    top = _top(folder)
    base = _read_base(folder, rev, copies, accounting)
    report.copies = [_rel(c, top) for c in base.copies]
    report.checked = base.checked
    report.failures += [{"sentence": None, "to": None, "reason": r}
                        for r in _unread_copies(folder, rev, base.copies)]

    moved: dict[str, dict] = {}
    dropped: dict[str, dict] = {}
    ledger: set[str] = set()
    if accounting is not None:
        if _commit(folder, accounting["base"]) != _commit(folder, rev):
            report.failures.append({"sentence": None, "to": None, "reason":
                                    f"{ACCOUNTING} accounts for base {accounting['base']!r}, "
                                    f"not --base {rev!r}"})
        else:
            moved = {normalize(m["sentence"]): m for m in accounting.get("moved", [])}
            dropped = {normalize(m["sentence"]): m for m in accounting.get("obsolete", [])}
            ledger = {normalize(x) for x in accounting.get("retargets", [])}

    rules = {n: unlabeled(t) for n, t in rule_texts(artifact).items()}
    why = {n: unlabeled(t) for n, t in rationale_texts(artifact).items()}
    for s in base.absent:
        if s in dropped:
            _obsolete_entry(report, s, dropped[s], s in base.own, base.origin.get(s), require_judged,
                            topic_text(artifact))
            continue
        m = moved.get(s)
        if m is None:
            report.missing.append(s)
            continue
        to = m["to"]
        names = _targets(to)
        retargeted = "retargeted" in m
        second = _second_retarget(s, m, ledger)
        if second:
            report.failures.append({"sentence": s, "to": to, **({"retargeted": True} if retargeted else {}),
                                    "reason": second})
            continue
        reason, shape = _judge(s, names, artifact, rules, why)
        verdict, stale = _verdict(m.get("judged"), moved_pin(s, to, rules, artifact))
        entry = {"sentence": s, "to": to, **({shape: True} if shape else {}),
                 **({"judged": m["judged"]} if m.get("judged") else {}),
                 **({"retargeted": True} if retargeted else {})}
        if reason:
            report.failures.append({"sentence": s, "to": to, **({"retargeted": True} if retargeted else {}),
                                    "reason": reason})
            continue
        if verdict and verdict["verdict"] == "fail":
            report.counts["judged_fail"] += 1
            final = " after its one retarget (no second retarget)" if retargeted else ""
            report.failures.append({**entry, "reason": f"judged fail by {verdict['by']}{final}: "
                                                      f"{verdict['note']}"})
        elif not shape and _verbatim_move(s, names, rules, artifact):
            report.counts["verbatim"] += 1
            report.moved.append({**entry, "verbatim": True})
        elif verdict:
            report.counts["reworded_judged"] += 1
            report.moved.append(entry)
        else:
            report.counts["reworded_unjudged"] += 1
            report.counts["stale"] += bool(stale)
            if stale:
                entry["stale"] = True
            if require_judged:
                report.failures.append({**entry, "reason": (
                    _stale_reason("reworded", stale) if stale else "reworded, and no judged pass")})
            else:
                report.moved.append(entry)
    report.unused = ([{"sentence": s, "to": m["to"]} for s, m in moved.items() if s not in base.absent]
                     + [{"sentence": s, "obsolete": m["reason"]} for s, m in dropped.items()
                        if s not in base.absent])
    return report


def _obsolete_entry(report: LosslessReport, s: str, m: dict, own: bool, origin: Optional[str],
                    require_judged: bool, topic: str) -> None:
    """Judge one obsolete entry into `report`."""
    reason = m["reason"]
    refused = _never_obsolete(s, own)
    if refused:
        report.failures.append({"sentence": s, "obsolete": reason, "reason": refused})
        return
    verdict, stale = _verdict(m.get("judged"), obsolete_pin(s, origin, reason, topic) if origin else None)
    entry = {"sentence": s, "reason": reason, **({"judged": m["judged"]} if m.get("judged") else {})}
    if verdict and verdict["verdict"] == "fail":
        report.failures.append({"sentence": s, "obsolete": reason,
                                "reason": f"judged fail by {verdict['by']}: {verdict['note']}"})
        return
    if verdict:
        report.counts["obsolete_judged"] += 1
        report.obsolete.append(entry)
        return
    report.counts["obsolete_unjudged"] += 1
    report.counts["stale"] += bool(stale)
    if stale:
        entry["stale"] = True
    if require_judged:
        report.failures.append({"sentence": s, "obsolete": reason, **({"stale": True} if stale else {}),
                                "reason": (_stale_reason("obsolete", stale) if stale
                                           else "obsolete, and no judged pass")})
    else:
        report.obsolete.append(entry)


def _never_obsolete(s: str, own: bool) -> Optional[str]:
    """Why `s` may not be declared obsolete, or None: only a folded copy's
    sentence with no RFC keyword, negation or FLIP_WORD may be."""
    if own:
        return "a sentence of the topic's own base is never obsolete; only a folded copy's may be"
    said = sorted(levels(s)) + (["a negation"] if negated(s) else []) + [repr(w) for w in sorted(flips(s))]
    if said:
        return f"states a rule ({', '.join(said)}); a rule is never obsolete"
    return None


def _verbatim_move(s: str, names: list[str], rules: dict[str, str], artifact: Artifact) -> bool:
    """`s` is word for word one sentence of one of its targets (a rule's text,
    or a non-rule part's)."""
    parts = {p.name: p for p in artifact.parts if p.name != HISTORY and p.role != RULES_ROLE}
    return any(verbatim_in(s, rules[n] if n in rules else unlabeled(parts[n].text)) for n in names)


def pin_for(folder: Path, entry: int, copies: Iterable[Path] = ()) -> dict:
    """The pin of entry `entry` (from 1: `moved` in order, then `obsolete`) of
    `folder`'s lossless.json, for its judge to write beside its verdict:
    `{"entry", "kind", "sentence", "pin"}`. Writes nothing. Refuses an entry
    that does not exist and one whose pin cannot be taken (a target, or the
    copy it came from, is gone). Nothing ever stamps a pin on a verdict: a
    verdict without one is stale until its judge writes it."""
    folder = _folder(folder)
    accounting = read_accounting(folder)
    if accounting is None:
        raise RoleworkError(f"{folder}: no {ACCOUNTING}")
    entries = [("moved", m) for m in accounting.get("moved", [])]
    entries += [("obsolete", m) for m in accounting.get("obsolete", [])]
    if not 1 <= entry <= len(entries):
        raise RoleworkError(f"{folder / ACCOUNTING}: no entry {entry} (it has {len(entries)}, "
                            f"numbered from 1: moved, then obsolete)")
    kind, m = entries[entry - 1]
    s = normalize(m["sentence"])
    artifact = load_folder(folder)
    if kind == "moved":
        rules = {n: unlabeled(t) for n, t in rule_texts(artifact).items()}
        now = moved_pin(s, m["to"], rules, artifact)
    else:
        origin = _read_base(folder, accounting["base"], copies, accounting).origin
        now = obsolete_pin(s, origin[s], m["reason"], topic_text(artifact)) if s in origin else None
    if now is None:
        raise RoleworkError(f"{folder / ACCOUNTING}: entry {entry} ({s!r}) cannot be pinned "
                            f"(a target, or the copy it came from, is gone)")
    return {"entry": entry, "kind": kind, "sentence": s, "pin": now}


def retarget(folder: Path, entry: int, to) -> dict:
    """Retarget moved entry `entry` (from 1, as `pin_for` counts) of `folder`'s
    lossless.json once, after its judged fail named content carried outside
    its `to`, when the new targets already pass the deterministic check (the
    80% bar and the tripwires, `_judge`, as `--draft` runs them): its `to` and that fail move into `"retargeted": {"from", "to",
    "judged", "seal"}`, its `to` becomes `to`, its `judged` goes (the new
    targets wait for a fresh judge), and its sentence joins the file's
    `retargets` ledger. Refuses, writing nothing, an entry that is not moved,
    one already retargeted or ledgered (a second retarget), one with no fail
    whose pin matches its targets now, and a `to` that names a missing rule or
    part, more than MAX_TARGETS, or the targets it has, or that fails the bar
    or a tripwire (a bad target never spends the one retarget). `{"entry", "sentence",
    "from", "to"}`."""
    folder = _folder(folder)
    accounting = read_accounting(folder)
    if accounting is None:
        raise RoleworkError(f"{folder}: no {ACCOUNTING}")
    path = folder / ACCOUNTING
    moved = accounting.get("moved", [])
    total = len(moved) + len(accounting.get("obsolete", []))
    if not 1 <= entry <= total:
        raise RoleworkError(f"{path}: no entry {entry} (it has {total}, numbered from 1: moved, then obsolete)")
    if entry > len(moved):
        raise RoleworkError(f"{path}: entry {entry} is obsolete; only a moved entry is retargeted")
    m = moved[entry - 1]
    s = normalize(m["sentence"])
    if "retargeted" in m or s in {normalize(x) for x in accounting.get("retargets", [])}:
        raise RoleworkError(f"{path}: entry {entry} ({s!r}) was retargeted once already: "
                            f"a second retarget is refused")
    artifact = load_folder(folder)
    rules = {n: unlabeled(t) for n, t in rule_texts(artifact).items()}
    verdict, _ = _verdict(m.get("judged"), moved_pin(s, m["to"], rules, artifact))
    if not verdict or verdict["verdict"] != "fail":
        raise RoleworkError(f"{path}: entry {entry} ({s!r}) has no judged fail whose pin matches its "
                            f"targets now; only such a fail is retargeted")
    names = _targets(to)
    if not names or len(names) > MAX_TARGETS:
        raise RoleworkError(f"{path}: entry {entry} ({s!r}): give 1 to {MAX_TARGETS} targets, "
                            f"not {len(names)}")
    if sorted(names) == sorted(_targets(m["to"])):
        raise RoleworkError(f"{path}: entry {entry} ({s!r}) already names {m['to']!r}; a retarget changes it")
    if moved_pin(s, names, rules, artifact) is None:
        missing = [n for n in names if _target_text(n, rules, artifact) is None]
        raise RoleworkError(f"{path}: entry {entry} ({s!r}): no rule or part named {', '.join(missing)}")
    why = {n: unlabeled(t) for n, t in rationale_texts(artifact).items()}
    tripped, _ = _judge(s, names, artifact, rules, why)
    if tripped:
        raise RoleworkError(f"{path}: entry {entry} ({s!r}): the new targets fail the deterministic "
                            f"check, so nothing is retargeted (the one retarget is not spent): {tripped}")
    new = names if len(names) > 1 or isinstance(to, list) else names[0]
    record = {"from": m["to"], "to": new, "judged": m.pop("judged")}
    record["seal"] = _seal(s, record)
    m["retargeted"], m["to"] = record, new
    accounting["retargets"] = [*accounting.get("retargets", []), m["sentence"]]
    path.write_text(json.dumps(accounting, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return {"entry": entry, "sentence": s, "from": record["from"], "to": new}


# ── fold ────────────────────────────────────────────────────────────────────

@dataclass
class FoldReport:
    redirected: list[str]
    parts_added: list[str]
    identical: bool

    def as_json(self) -> dict:
        return {"redirected": self.redirected, "parts_added": self.parts_added,
                "identical": self.identical}


def _unique(name: str, taken: set[str]) -> str:
    base, n = name, 2
    while name in taken or name in RESERVED:
        name, n = f"{base}-{n}", n + 1
    return name


def _lacking(copy: Artifact, topic: Artifact) -> list[Part]:
    """The copy's parts (history aside) holding a sentence the topic lacks,
    as new unroled parts named like a doc would name them."""
    now = now_sentences(topic)
    taken = {p.name for p in topic.parts}
    added = []
    for p in copy.parts:
        if p.name == HISTORY or all(s in now for s in sentences(p.text)):
            continue
        heading = p.heading or "Introduction"
        text = p.text if p.heading is not None else "\n" + p.text
        name = _unique(_slug(heading), taken)
        taken.add(name)
        added.append(Part(name, text if text.endswith("\n") else text + "\n", heading))
    return added


def _id(artifact: Artifact, folder: Path) -> str:
    uid = str(artifact.meta.get("id") or "").lower()
    if not uid:
        raise RoleworkError(f"{folder}: no id in {ARTIFACT_FILE}")
    return uid


def _is(value: str, uid: str) -> bool:
    return value.strip().lower().split("/")[-1] == uid


def _record(topic: Path, summary: str, level: Optional[str], author: str, day: str) -> None:
    """Add the topic's Change History row, freezing its base version as
    `cookr bump` does. When the branch already bumped it at this level or
    higher, the newest row's summary gains the fold instead."""
    doc = doc_path(topic)
    try:
        plan, frozen = plan_against_base(doc, level=level, summary=summary, author=author, day=day)
    except BumpError as e:
        raise RoleworkError(f"{topic}: cannot record the fold: {e}") from e
    if frozen is not None:
        why = conflict(frozen.folder, frozen.version, frozen.files)
        if why:
            raise RoleworkError(f"{topic}: cannot freeze its base version: {why}")
        freeze(frozen.folder, frozen.version, frozen.files)
    text = plan.text
    if plan.noop:
        table = hist.read(text)
        newest = table.newest
        if newest is None:
            raise RoleworkError(f"{topic}: no Change History row to record the fold in")
        cells = list(newest.cells) + [""] * (len(hist.COLUMNS) - len(newest.cells))
        i = hist.COLUMNS.index("Summary")
        cells[i] = f"{cells[i]}; {summary}" if cells[i] else summary
        text = hist.replace_newest_row(table, newest.version, cells)
    save_document(doc, text)


def _readable(cookbook: Path) -> None:
    """Refuse, before anything is written, a cookbook with an artifact the
    link edits could not read."""
    for f in find_folders([cookbook]):
        try:
            if doc_path(f).is_file():
                read_document(edit_text(doc_path(f)))
            else:
                load_folder(f)
        except (CookbookError, ValueError, OSError) as e:
            raise RoleworkError(f"{f}: cannot be read, so its links could not be redirected "
                                f"({e}); nothing was written") from e


def fold(copy: Path, topic: Path, *, author: str, day: str) -> FoldReport:
    """Fold `copy` into `topic`: the copy's text the topic lacks becomes new
    unroled parts (so the census names them until each gets a role), the fold
    is recorded in the topic's history, the copy is deleted and every link to it
    across the cookbook points at the topic. Refuses a roled copy."""
    copy, topic = _folder(copy), _folder(topic)
    if copy.resolve() == topic.resolve():
        raise RoleworkError(f"{copy}: a folder cannot be folded into itself")
    copy_art, topic_art = load_folder(copy), load_folder(topic)
    if copy_art.roled:
        raise RoleworkError(f"{copy}: it is roled; fold an unroled copy into the roled topic, "
                            "never a roled artifact")
    copy_id, topic_id = _id(copy_art, copy), _id(topic_art, topic)
    cookbook = _cookbook(topic)
    if _cookbook(copy) != cookbook:
        raise RoleworkError(f"{copy} and {topic} are in different cookbooks")
    base = cookbook.parent
    copy_rel = copy.resolve().relative_to(cookbook.resolve()).as_posix()

    labels: dict[str, str] = {}
    try:
        index = current_index(cookbook)
        old, new = index.entries.get(copy_id), index.entries.get(topic_id)
        if old and new:
            labels[old.rdid] = new.rdid
    except CookbookError:
        pass   # no manifest: links are redirected, their labels left as written

    _readable(cookbook)   # every link edit below must be able to land: check before writing
    in_text = re.compile(r"(\[([^\]]+)\]\()?cookbook:((?:[0-9A-Fa-f-]{36}/)?)" + re.escape(copy_id)
                         + r"(?![0-9A-Fa-f-])(\))?", re.I)

    added = _lacking(copy_art, topic_art)
    at = next((i for i, p in enumerate(topic_art.parts) if p.name == HISTORY), len(topic_art.parts))
    topic_art.parts[at:at] = added
    for key in ("depends-on", "related"):   # its link to the copy would be a link to itself
        values = topic_art.meta.get(key)
        if isinstance(values, list):
            topic_art.meta[key] = [v for v in values if not (isinstance(v, str) and _is(v, copy_id))]
    for p in topic_art.parts:   # ...and so would an in-text one: its label stays as plain text
        p.text = in_text.sub(lambda m: m.group(2) if m.group(1) and m.group(4) else m.group(0), p.text)
    save_document(doc_path(topic), compose_document(topic_art))

    names = [p.name for p in added]
    summary = (f"Fold {copy_rel} into this topic; its text this lacked added unroled as "
               f"{', '.join(names)}" if added else
               f"Fold {copy_rel} into this topic (identical text); links to it redirected here")
    _record(topic, summary, None if added else "patch", author, day)

    def text_fn(text: str) -> str:
        def sub(m: re.Match) -> str:
            opener = ""
            if m.group(1):
                opener = f"[{labels.get(m.group(2), m.group(2))}]("
            return f"{opener}cookbook:{m.group(3)}{topic_id}{m.group(4) or ''}"
        return in_text.sub(sub, text)

    def value_fn(value: str) -> str:
        if not _is(value, copy_id):
            return value
        head, _, _ = value.strip().rpartition("/")
        return f"{head}/{topic_id}" if head else topic_id

    changed = [f for f in edit_links(cookbook, value_fn, text_fn, dedupe=True)
               if f.resolve() != copy.resolve()]
    shutil.rmtree(copy)   # last: a failure above leaves the copy, and every link to it, whole
    if doc_path(copy).is_file():
        doc_path(copy).unlink()
    if (cookbook / INDEX_FILE).is_file():
        index = load_index(cookbook)
        sync_from_folders(index, cookbook)
        save_index(index, cookbook)
    return FoldReport(
        redirected=sorted(f.resolve().relative_to(base.resolve()).as_posix() for f in changed),
        parts_added=names, identical=not added)
