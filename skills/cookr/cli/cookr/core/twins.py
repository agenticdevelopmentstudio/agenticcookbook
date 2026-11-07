"""Two guideline censuses: twins that drifted apart, and guidelines with no rule.

**Twins.** One guideline often appears under several use cases, so
`guidelines/implementing/security/input-validation` and
`guidelines/reviewing/security/input-validation` are twins: the same path below
their use case. Twins are meant to say the same thing. When one is edited and
the other is not, they contradict each other quietly. Twins are compared by
their shared text, which leaves out the change history and treats a link to the
twin's own use case (`…://guidelines/reviewing/…` against
`…://guidelines/implementing/…`) as the same link. A twin rewritten on purpose,
such as a review checklist of its implementing guideline, records why in
`twin_differs` in its artifact.json. Twins with no reason must all match.

Findings:
- `drift`: twins with no reason that do not match.
- `stale`: a reason on a twin that matches all of its twins.
- `short`: a reason under MIN_REASON characters, which explains nothing.

**Rules.** A guideline states its requirements with RFC 2119 keywords in
capitals (MUST, SHOULD, MAY). One that states none, outside code and its
history, is flagged `no-rules`, unless it is purely informational and says so
in `informational` in its artifact.json. A reason on a guideline that does
state a rule is `stale`.
"""

from __future__ import annotations

import re
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Optional

from .artifact import HISTORY, Artifact, ArtifactError, load_folder
from .skill import SkillError, path_below_type

MIN_REASON = 16
GUIDELINES = "guidelines"

_OWN_USE_CASE = re.compile(r"(agenticdevelopercookbook://guidelines/)[a-z0-9-]+/")
_FENCED = re.compile(r"^(```|~~~).*?^\1", re.S | re.M)
_RULE = re.compile(r"(?<![A-Za-z])(MUST|SHOULD|MAY)(?![A-Za-z])")


@dataclass
class TwinFinding:
    key: str                  # the path below the use case, e.g. "security/input-validation"
    kind: str                 # "drift" | "stale" | "short"
    folders: list[Path]


@dataclass
class RuleFinding:
    folder: Path
    kind: str                 # "no-rules" | "stale" | "short"


def _guideline(folder: Path) -> Optional[tuple[Artifact, tuple[str, ...]]]:
    """(the artifact, its path below `guidelines/`) for a guideline folder;
    None for anything else, or a folder too broken to read, which the compile
    check reports."""
    try:
        artifact = load_folder(folder)
        type_dir, rel = path_below_type(folder)
    except (ArtifactError, SkillError):
        return None
    if artifact.type != "guideline" or type_dir != GUIDELINES:
        return None
    return artifact, rel


def comparable(artifact: Artifact) -> str:
    """The text twins must share: no history, links to a use case made
    use-case-neutral, trailing spaces and blank-line runs ignored."""
    text = _OWN_USE_CASE.sub(r"\1*/", artifact.shared_body())
    lines = [line.rstrip() for line in text.strip().splitlines()]
    return re.sub(r"\n{3,}", "\n\n", "\n".join(lines))


def twin_census(folders: Iterable[Path]) -> list[TwinFinding]:
    groups: dict[str, list[tuple[Path, Artifact]]] = defaultdict(list)
    for folder in folders:
        found = _guideline(folder)
        if found is None or len(found[1]) < 2:
            continue  # a guideline directly under guidelines/ has no use case
        artifact, rel = found
        groups["/".join(rel[1:])].append((folder, artifact))

    findings = []
    for key, members in sorted(groups.items()):
        if len(members) < 2:
            continue
        texts = {folder: comparable(a) for folder, a in members}
        plain = [f for f, a in members if a.twin_differs is None]
        if len({texts[f] for f in plain}) > 1:
            findings.append(TwinFinding(key, "drift", plain))
        for folder, a in members:
            if a.twin_differs is None:
                continue
            if all(texts[o] == texts[folder] for o in texts if o != folder):
                findings.append(TwinFinding(key, "stale", [folder]))
            elif len(a.twin_differs.strip()) < MIN_REASON:
                findings.append(TwinFinding(key, "short", [folder]))
    return findings


def states_a_rule(artifact: Artifact) -> bool:
    text = "".join(p.text for p in artifact.parts if p.name != HISTORY)
    return bool(_RULE.search(_FENCED.sub("", text)))


def rule_census(folders: Iterable[Path]) -> list[RuleFinding]:
    findings = []
    for folder in folders:
        found = _guideline(folder)
        if found is None:
            continue
        artifact = found[0]
        reason, has_rule = artifact.informational, states_a_rule(artifact)
        if reason is None and not has_rule:
            findings.append(RuleFinding(folder, "no-rules"))
        elif reason is not None and has_rule:
            findings.append(RuleFinding(folder, "stale"))
        elif reason is not None and len(reason.strip()) < MIN_REASON:
            findings.append(RuleFinding(folder, "short"))
    return findings


TWIN_FIX = {
    "drift": "Make the twins say the same thing, or, when one is rewritten on purpose (a review "
             "checklist, say), set `twin_differs` in its artifact.json to the reason.",
    "stale": "It matches its twins now: remove `twin_differs` from its artifact.json.",
    "short": f"Say why in at least {MIN_REASON} characters.",
}

RULE_FIX = {
    "no-rules": "State its requirements with MUST/SHOULD/MAY, or, when it is purely informational, "
                "set `informational` in its artifact.json to the reason.",
    "stale": "It states a rule now: remove `informational` from its artifact.json.",
    "short": f"Say why in at least {MIN_REASON} characters.",
}
