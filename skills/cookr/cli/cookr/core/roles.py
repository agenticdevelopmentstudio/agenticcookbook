"""What a part's role means, and the census of what is wrong with a roled artifact.

A part may carry a role (`artifact.ROLES`), so the skills compiled from an
artifact can pick their parts by role. Four skills are compiled from a roled
artifact; SKILL_ROLES lists the roles each one carries (the intro is implicit),
and NEEDS the role without which it cannot be built. `rationale` and
`references` belong to no skill body. The intro and the history never carry a
role.

A rule in a `rules` part is a named requirement, one per named bullet:
`- **kebab-name**: … MUST|SHOULD|MAY …` (the word in any case), at the left
margin or indented. A bullet's indented lines below it, nested unnamed bullets
and numbered items included, belong to it, across blank lines. Names are unique
within the artifact. Outside a named bullet only an upper-case RFC keyword
states a requirement, so prose saying "may" or "should" in passing is allowed;
code is ignored (fences per CommonMark: `history.without_fences`). A
`build-bar` part cites a rule only by an item that opens with its name in
backticks and a colon: ``- `kebab-name`: …``; ``- `pytest` passes`` cites
nothing.

Findings, for a roled artifact only (one with no role never has a finding):
- `unknown-role`: a part's role is not one of ROLES, or the intro or the
  history carries a role.
- `unroled-part`: a part other than the intro and the history has no role.
- `missing-role`: no part carries the role a skill NEEDS; one per skill.
- `empty-part`: a part carrying a role a skill NEEDS has no text.
- `unnamed-rule`: a list item (a bullet or a numbered item) or a paragraph in a
  `rules` part states a requirement but is not a named bullet, or a `rules`
  part states no named rule.
- `duplicate-rule`: two named bullets share a name, requirement or not.
- `uncited-rule`: a rule no `build-bar` part cites.
- `unknown-citation`: a `build-bar` part cites a name that is no rule.
- `twin-not-folded`: it lives under `guidelines/<use-case>/<tail>` while
  `guidelines/reviewing/<tail>` exists; its roles replace the reviewing twin.
- `reviewing-folder`: it lives under `guidelines/reviewing/`, which is folded
  into each topic's `review-focus` and `review-bar`, never roled itself.
- `unroled-type`: it is an ingredient or a recipe, which describe a thing to
  build, not rules to keep. A guideline under any other use case, or a
  principle, may be roled.
- `name-collision`: one of its four skill names (`skill.roled_paths`, cut to
  the hosts' limit) is also derived for another artifact among the folders,
  the detail naming the other; or two of its own four skills derive one name
  (a topic under `verifying-build/` or `verifying-review/`).
- `tuned`: it has a `hosts/` directory, which compiling by role does not apply yet.
- `routed`: it sets `routes` in artifact.json; each of its four skills derives
  its own from its use case.
"""

from __future__ import annotations

import re
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

from .artifact import (ARTIFACT_FILE, HISTORY, INTRO, ROLES, Artifact, ArtifactError, Part, find_folders,
                       is_folder, load_folder)
from .errors import CookbookError
from .index import load_index
from .markdown import HOSTS_DIR, in_research, in_versions
from .history import split_lines, unfenced, without_fences
from .skill import NAME_MAX, TYPE_DIRS, USE_CASES, SkillError, path_below_type, roled_paths, skill_name
from .twins import _RULE as _KEYWORD

SKILL_ROLES: dict[str, tuple[str, ...]] = {
    "builder": ("rules", "how-to", "examples"),
    "build-verifier": ("build-bar",),
    "reviewer": ("rules", "review-focus"),
    "review-verifier": ("review-bar",),
}
NEEDS: dict[str, str] = {
    "builder": "rules",
    "build-verifier": "build-bar",
    "reviewer": "review-focus",
    "review-verifier": "review-bar",
}

RULES = "rules"
GUIDELINES, REVIEWING = "guidelines", "reviewing"
UNROLED_TYPES = ("ingredient", "recipe")
QUOTE = 40  # characters of an unnamed bullet quoted in its finding
_NAMED = re.compile(r"[ \t]*- \*\*([a-z0-9]+(?:-[a-z0-9]+)*)\*\*:\s")
_ITEM = re.compile(r"(?:[-*+]|\d+[.)])\s")
#: Inside a named bullet a requirement word counts in any case; elsewhere only
#: the upper-case keyword (`_KEYWORD`) does.
_REQUIREMENT = re.compile(r"(?<![A-Za-z])(must|should|may)(?![A-Za-z])", re.I)
_CITED = re.compile(r"^[ \t]*[-*+]\s+`([a-z0-9]+(?:-[a-z0-9]+)*)`:", re.M)
_NEEDED_BY = {role: kind for kind, role in NEEDS.items()}


@dataclass
class RoleFinding:
    folder: Path
    kind: str                 # see the module docstring
    detail: str


def _blocks(part: Part) -> tuple[list[str], list[str]]:
    """(the list items of a part, its paragraphs outside any item), outside
    code. An item is a bullet or numbered item at the left margin, or a named
    bullet at any indent, with the lines that continue it: indented ones, even
    after a blank line, and unindented ones right below it."""
    items: list[list[str]] = []
    prose: list[list[str]] = []
    current = paragraph = None
    blank = True
    for line in without_fences(part.text).splitlines():
        if not line.strip():
            blank, paragraph = True, None
            continue
        indented = line[0] in " \t"
        if _NAMED.match(line) or (not indented and _ITEM.match(line)):
            current, paragraph = [line], None
            items.append(current)
        elif current is not None and (indented or not blank):
            current.append(line)
        elif paragraph is not None:
            paragraph.append(line)
        else:
            current, paragraph = None, [line]
            prose.append(paragraph)
        blank = False
    return ["\n".join(b) for b in items], ["\n".join(b) for b in prose]


def _rule_parts(artifact: Artifact) -> list[Part]:
    return [p for p in artifact.parts if p.role == RULES]


def _named(artifact: Artifact) -> list[tuple[str, bool]]:
    """(name, states a requirement) for each named bullet in the `rules` parts, in order."""
    return [(m.group(1), bool(_REQUIREMENT.search(b[m.end():])))
            for p in _rule_parts(artifact) for b in _blocks(p)[0] if (m := _NAMED.match(b))]


def rule_texts(artifact: Artifact) -> dict[str, str]:
    """{name: the text of its named bullet, with the lines that continue it}
    for every named bullet in the `rules` parts; a name used twice joins both."""
    return named_bullets(_rule_parts(artifact))


def named_bullets(parts: Iterable[Part]) -> dict[str, str]:
    """{name: the text of its named bullet, with the lines that continue it}
    for every named bullet in `parts`; a name used twice joins both."""
    texts: dict[str, str] = {}
    for p in parts:
        for b in _blocks(p)[0]:
            if m := _NAMED.match(b):
                texts[m.group(1)] = (texts[m.group(1)] + "\n" + b) if m.group(1) in texts else b
    return texts


def states_requirement(bullet: str) -> bool:
    """True when named bullet `bullet` states a requirement: MUST, SHOULD or
    MAY, in any case, after its name."""
    m = _NAMED.match(bullet)
    return bool(m and _REQUIREMENT.search(bullet[m.end():]))


_EXPLAINED = re.compile(r"[ \t]*[-*+] (`[a-z0-9]+(?:-[a-z0-9]+)*`(?:,\s*`[a-z0-9]+(?:-[a-z0-9]+)*`)*):\s")


def part_units(part: Part) -> list[str]:
    """The units a part says things in: each list item (with the lines that
    continue it) and each paragraph line outside code, then each line of code
    (fences left out), so no part is ever judged as one block."""
    items, prose = _blocks(part)
    lines = split_lines(part.text)
    code = [line.strip() for (_, bare), line in zip(unfenced(lines), lines)
            if bare is None and line.strip() and not line.lstrip().startswith(("```", "~~~"))]
    return items + [line for para in prose for line in para.splitlines() if line.strip()] + code


def rationale_texts(artifact: Artifact) -> dict[str, str]:
    """{rule name: its rationale bullets (`- `name`: why`, or one naming several
    rules `- `a`, `b`: why`), joined} across the
    artifact's `rationale` parts."""
    texts: dict[str, str] = {}
    for p in artifact.parts:
        if p.role != "rationale":
            continue
        for b in _blocks(p)[0]:
            if m := _EXPLAINED.match(b):
                for name in re.findall(r"`([^`]+)`", m.group(1)):
                    texts[name] = (texts[name] + "\n" + b) if name in texts else b
    return texts


def rule_names(artifact: Artifact) -> list[str]:
    """The names of the rules in the artifact's `rules` parts, in order."""
    return [name for name, rule in _named(artifact) if rule]


def _citations(part: Part) -> list[str]:
    """The rule names a `build-bar` part cites, in order."""
    return _CITED.findall(without_fences(part.text))


def _quote(bullet: str) -> str:
    first = bullet.splitlines()[0]
    return f"'{first}'" if len(first) <= QUOTE else f"'{first[:QUOTE]}…'"


def _findings(folder: Path, artifact: Artifact) -> list[tuple[str, str]]:
    found: list[tuple[str, str]] = []
    for p in artifact.parts:
        if p.role is not None and p.name in (INTRO, HISTORY):
            found.append(("unknown-role", f"part '{p.name}' has role '{p.role}'; "
                                          f"the {p.name} never carries a role"))
        elif p.role is not None and p.role not in ROLES:
            found.append(("unknown-role", f"part '{p.name}' has role '{p.role}'"))
        elif p.role is None and p.name not in (INTRO, HISTORY):
            found.append(("unroled-part", f"part '{p.name}' has no role"))

    present = {p.role for p in artifact.parts}
    for kind, role in NEEDS.items():
        if role not in present:
            found.append(("missing-role", f"no '{role}' part, so no {kind} skill"))

    for p in artifact.parts:
        if p.role in _NEEDED_BY and not p.text.strip():
            found.append(("empty-part", f"part '{p.name}' with role '{p.role}' has no text, "
                                        f"so no {_NEEDED_BY[p.role]} skill"))

    for p in _rule_parts(artifact):
        if not p.text.strip():
            continue
        items, prose = _blocks(p)
        named = 0
        for b in items:
            m = _NAMED.match(b)
            if m and _REQUIREMENT.search(b[m.end():]):
                named += 1
            elif not m and _KEYWORD.search(b):
                found.append(("unnamed-rule", f"part '{p.name}': {_quote(b)} is not `- **name**: …`"))
        for para in prose:
            if _KEYWORD.search(para):
                found.append(("unnamed-rule", f"part '{p.name}': {_quote(para)} is not `- **name**: …`"))
        if not named:
            found.append(("unnamed-rule", f"part '{p.name}' states no named rule"))

    for name, n in Counter(name for name, _ in _named(artifact)).items():
        if n > 1:
            found.append(("duplicate-rule", f"rule '{name}' is named {n} times"))

    # The bar is checked against the rules only when both have text: else
    # `missing-role` or `empty-part` has already stopped the compile.
    bars = [p for p in artifact.parts if p.role == "build-bar" and p.text.strip()]
    if bars and any(p.text.strip() for p in _rule_parts(artifact)):
        rules = rule_names(artifact)
        cited = {name for p in bars for name in _citations(p)}
        found += [("uncited-rule", f"rule '{name}' has no line in a build-bar part")
                  for name in rules if name not in cited]
        found += [("unknown-citation", f"build-bar part '{p.name}' cites '{name}', which is no rule")
                  for p in bars for name in dict.fromkeys(_citations(p)) if name not in rules]

    for d in folder.parents:
        if d.parent.name == GUIDELINES:
            if d.name == REVIEWING:
                found.append(("reviewing-folder", f"it lives under {GUIDELINES}/{REVIEWING}/, which is "
                                                  "folded into its topic, never roled"))
                break
            twin = d.parent / REVIEWING / folder.relative_to(d)
            if twin.is_dir():
                base = d.parent.parent
                found.append(("twin-not-folded", f"{folder.relative_to(base)} has a twin at "
                                                 f"{twin.relative_to(base)}"))
            break
    if artifact.type in UNROLED_TYPES:
        article = "an" if artifact.type[:1] in "aeiou" else "a"
        found.append(("unroled-type", f"{article} {artifact.type} is never roled"))

    if (folder / HOSTS_DIR).is_dir():
        found.append(("tuned", f"it has a {HOSTS_DIR}/ directory"))
    if artifact.routes is not None:
        found.append(("routed", "a roled artifact derives its routes; it may not set `routes` in artifact.json"))
    return found


def _names(folder: Path, artifact: Artifact) -> dict[str, tuple[str, str]]:
    """{skill name: (skill kind, the folder's path from its type dir)} for the
    skills `folder` compiles to; empty when it is under no type dir."""
    try:
        type_dir, rel = path_below_type(folder)
    except SkillError:
        return {}
    where = "/".join((type_dir, *rel))
    if not artifact.roled:
        return {skill_name(type_dir, rel): ("", where)}
    return {skill_name(type_dir, r): (kind, where) for kind, r in roled_paths(type_dir, rel).items()}


def _own_collisions(folder: Path) -> dict[str, list[str]]:
    """{skill name: the kinds of this roled folder's own skills that share it}:
    a topic under a verifier's use case (`guidelines/verifying-build/…`)
    derives its builder's name and that verifier's alike. One under
    `reviewing/` is left to its `reviewing-folder` finding."""
    try:
        type_dir, rel = path_below_type(folder)
    except SkillError:
        return {}
    if type_dir == GUIDELINES and rel[:1] == (REVIEWING,):
        return {}
    kinds: dict[str, list[str]] = {}
    for kind, r in roled_paths(type_dir, rel).items():
        kinds.setdefault(skill_name(type_dir, r), []).append(kind)
    return {name: ks for name, ks in kinds.items() if len(ks) > 1}


def _collisions(loaded: list[tuple[Path, Artifact]]) -> dict[Path, list[tuple[str, str]]]:
    """{roled folder: its `name-collision` findings}: each of its skill names
    another folder also derives, naming that folder."""
    names = {folder: _names(folder, artifact) for folder, artifact in loaded}
    owners: dict[str, list[tuple[Path, str]]] = {}
    for folder, derived in names.items():
        for name, (_, where) in derived.items():
            owners.setdefault(name, []).append((folder, where))
    found: dict[Path, list[tuple[str, str]]] = {}
    for folder, artifact in loaded:
        if not artifact.roled:
            continue
        for name, kinds in _own_collisions(folder).items():
            found.setdefault(folder, []).append(
                ("name-collision", f"its {' and '.join(kinds)} skills are both named '{name}'"))
        for name, (kind, _) in names[folder].items():
            for other, where in owners[name]:
                if other != folder:
                    found.setdefault(folder, []).append(
                        ("name-collision", f"its {kind} skill '{name}' is also derived for {where}"))
    return found


def census(folders: Iterable[Path]) -> list[RoleFinding]:
    """Every finding on the roled artifacts among `folders`. A folder too
    broken to read is skipped: the compile check reports it."""
    loaded = []
    for folder in folders:
        try:
            loaded.append((folder, load_folder(folder)))
        except ArtifactError:
            continue
    collisions = _collisions(loaded) if any(a.roled for _, a in loaded) else {}
    findings = []
    for folder, artifact in loaded:
        if artifact.roled:
            findings += [RoleFinding(folder, kind, detail) for kind, detail in
                         _findings(folder, artifact) + collisions.get(folder, [])]
    return findings


def census_of(folder: Path, cookbook: Path) -> list[RoleFinding]:
    """`census` of the whole `cookbook`, kept to `folder`'s findings, without
    walking the cookbook. A collision needs another folder deriving one of
    `folder`'s skill names, so only the folders that could are read: those at
    each place the name splits back into a path below a type dir (`_derivers`),
    and those the index lists whose name ends the skill name. A name cut to
    NAME_MAX with a digest cannot be split back; then the whole cookbook is read."""
    cookbook = Path(cookbook).resolve()
    mine = cookbook / Path(folder).resolve().relative_to(cookbook)
    artifact = load_folder(mine)
    names = set(_names(mine, artifact)) | set(_own_collisions(mine))
    if not artifact.roled or any(_cut(n) for n in names):
        return [f for f in census(find_folders([cookbook])) if f.folder == mine]
    found = {mine} | {c for n in names for c in _derivers(n, cookbook)} | _indexed(names, cookbook)
    loaded = []
    for f in sorted(found):
        if f != mine and (not is_folder(f) or in_versions(f / ARTIFACT_FILE, cookbook)
                          or in_research(f / ARTIFACT_FILE, cookbook)):
            continue
        try:
            loaded.append((f, artifact if f == mine else load_folder(f)))
        except ArtifactError:
            continue
    collisions = _collisions(loaded)
    return [RoleFinding(mine, kind, detail)
            for kind, detail in _findings(mine, artifact) + collisions.get(mine, [])]


_DIGEST = re.compile(r"-[0-9a-f]{6}$")


def _cut(name: str) -> bool:
    """Whether `name` is, or could be, one cut to NAME_MAX and ended by a digest."""
    return len(name) >= NAME_MAX - 7 and bool(_DIGEST.search(name))


def _splits(name: str, under: Path) -> Iterable[Path]:
    """Each existing directory below `under` whose path, its segments joined
    by '-', is `name`."""
    tokens = name.split("-")
    for i in range(1, len(tokens) + 1):
        d = under / "-".join(tokens[:i])
        if not d.is_dir():
            continue
        if i == len(tokens):
            yield d
        else:
            yield from _splits("-".join(tokens[i:]), d)


def _derivers(name: str, cookbook: Path) -> set[Path]:
    """Every directory below a type dir of `cookbook` that `skill_name` could
    name `name`: as its builder or only skill (its own path), or, roled, as
    one of the others (its path with its use case swapped for theirs). A
    superset: each is read and its real names compared."""
    out: set[Path] = set()
    for type_dir, kind in TYPE_DIRS.items():
        top = cookbook / type_dir
        if not top.is_dir():
            continue
        forms = [name] + [name[len(u) + 1:] for u in USE_CASES.values() if name.startswith(u + "-")]
        for i, form in enumerate(forms):
            if form.startswith(kind + "-"):          # a one-segment path: `<kind>-<name>`
                out.add(top / form[len(kind) + 1:])
            if i == 0:
                out.update(_splits(form, top))
            else:                                     # any use case's topic with this tail
                for use_case in (d for d in top.iterdir() if d.is_dir()):
                    out.update(_splits(form, use_case))
    return out


def _indexed(names: set[str], cookbook: Path) -> set[Path]:
    """The folders the cookbook's index lists whose last segment ends one of
    `names`: any folder a skill name derives from ends it so, wherever it lies."""
    try:
        index = load_index(cookbook)
    except CookbookError:
        return set()
    return {cookbook / e.path for e in index.entries.values()
            if "#" not in e.path and any(n == (s := e.path.rsplit("/", 1)[-1]) or n.endswith("-" + s)
                                         for n in names)}


FIX = {
    "unknown-role": f"Give the part one of the roles: {', '.join(ROLES)}; the intro and the "
                    "history take none.",
    "unroled-part": "Give the part a role in artifact.json, or fold it into a part that has one.",
    "missing-role": "Add a part with that role, so the skill it names can be built.",
    "empty-part": "Write the part's text: the skill its role builds would carry nothing.",
    "unnamed-rule": "Write each rule as one bullet: `- **kebab-name**: … MUST|SHOULD|MAY …`.",
    "duplicate-rule": "Give each rule its own name.",
    "uncited-rule": "Add a build-bar line for the rule: ``- `kebab-name`: <what a build shows>``.",
    "unknown-citation": "Cite the rule by its name in the rules part, or drop the build-bar line.",
    "twin-not-folded": "Fold the reviewing twin into this artifact's review-focus and review-bar "
                       "parts, then remove the reviewing twin.",
    "tuned": "Remove the hosts/ directory: per-skill tuning of a roled artifact is not supported yet.",
    "routed": "Remove `routes` from artifact.json: each of the four skills is routed by its use case.",
    "reviewing-folder": "Fold it into its topic's review-focus and review-bar parts under its own use "
                        "case, then remove it.",
    "unroled-type": "Remove the roles: an ingredient or a recipe compiles to its one skill.",
    "name-collision": "Rename one of the two topics, or fold one into the other, so their skills' "
                      "names differ; a topic whose own two skills share a name moves out of the "
                      "verifier's use case (verifying-build/, verifying-review/).",
}
