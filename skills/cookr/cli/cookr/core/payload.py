"""What a model needs to tune the cookbook for itself, and the stamping that
keeps its additions honest.

A **level** is anything that owns a `hosts/` directory of additions:

    template:<kind>        a skill type template   (templates/skill/<kind>.md)
    always:<name>          an always-on template   (templates/always/<name>.md)
    <artifact folder>      one artifact            (<folder>/artifact.json)

Each level has a **source**, the shared text its additions are written
against: the template file, or the artifact's shared body. An addition
stamped with the source's hash goes stale when the source changes
(core/tuning.py). `survey` lists every level with the additions it already has
along one target chain; `stamp_addition` records the current source on an
addition a model just wrote or re-checked.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Optional

from . import always_on
from . import skill as skill_mod
from . import tuning
from .artifact import ArtifactError, is_folder, load_folder

TEMPLATE, ALWAYS, ARTIFACT = "template", "always", "artifact"


class PayloadError(ArtifactError):
    """An addition with no level cookr can find the source of."""


@dataclass(frozen=True)
class Level:
    name: str           # template:guideline | always:principles | the artifact folder
    kind: str           # TEMPLATE | ALWAYS | ARTIFACT
    source_path: Path
    hosts_dir: Path

    def source(self) -> str:
        if self.kind == ARTIFACT:
            return load_folder(self.source_path).shared_body()
        return self.source_path.read_text(encoding="utf-8")

    def additions(self, chain: Optional[Iterable[str]] = None) -> list[tuning.Addition]:
        found = tuning.additions(self.hosts_dir)
        if chain is None:
            return list(found.values())
        return [found[(t, k)] for t in chain for k in tuning.KINDS if (t, k) in found]


def template_levels(skill_templates: Path = skill_mod.TEMPLATES,
                    always_templates: Path = always_on.TEMPLATES) -> list[Level]:
    """Every template as a tuning level. A command run on a cookbook passes
    `skill_mod.templates_root(cookbook)`'s `skill/` and `always/`: see there."""
    out = []
    for kind, root in ((TEMPLATE, skill_templates), (ALWAYS, always_templates)):
        for p in sorted(root.glob("*.md")):
            out.append(Level(f"{kind}:{p.stem}", kind, p, root / p.stem / tuning.HOSTS_DIR))
    return out


def artifact_level(folder: Path) -> Level:
    return Level(str(folder), ARTIFACT, folder, folder / tuning.HOSTS_DIR)


def level_of(addition: Path, templates: Iterable[Level] = ()) -> Level:
    """The level an addition file belongs to: its `hosts/` dir's owner."""
    hosts_dir = addition.parent
    if hosts_dir.name != tuning.HOSTS_DIR:
        raise PayloadError(f"{addition} is not in a {tuning.HOSTS_DIR}/ directory")
    for lv in templates or template_levels():
        if lv.hosts_dir.resolve() == hosts_dir.resolve():
            return lv
    owner = hosts_dir.parent
    if is_folder(owner):
        return artifact_level(owner)
    raise PayloadError(f"{addition}: {owner} is neither an artifact folder nor a template")


def describe(level: Level, chain: tuple[str, ...], *, text: bool = False) -> dict:
    """One level as the survey reports it: its source hash, and each addition
    along `chain` with whether it went stale."""
    source = level.source()
    digest = tuning.source_hash(source)
    adds = level.additions(chain)
    stale = {a.path for a in tuning.stale(adds, digest)}
    out = {
        "level": level.name, "kind": level.kind, "source": str(level.source_path),
        "source_sha256": digest, "hosts_dir": str(level.hosts_dir),
        "additions": [{"target": a.target, "kind": a.kind, "path": str(a.path),
                       "stamped": a.stamp is not None, "stale": a.path in stale}
                      for a in adds],
    }
    if text:
        out["text"] = source
    return out


def survey(chain: tuple[str, ...], folders: list[Path], *, templates: Iterable[Level] = (),
           template_text: bool = True) -> dict:
    """The tuning picture for one target chain: templates first (with their
    text, which is what a model reads to tune them), then every artifact."""
    templates = list(templates) or template_levels()
    return {
        "chain": list(chain),
        "templates": [describe(lv, chain, text=template_text) for lv in templates],
        "artifacts": [describe(artifact_level(f), chain) for f in folders],
    }


def worklist(chain: tuple[str, ...], folders: list[Path], library: Optional[str] = None,
             templates: Path = skill_mod.TEMPLATES) -> list[dict]:
    """One entry per artifact: the skill as `chain` receives it today (its
    template's and its own additions applied), and where an addition for the
    most specific target would go."""
    out = []
    for f in folders:
        s = skill_mod.compose(f, library, templates)
        levels = [skill_mod.template_hosts(s.type, templates), f / tuning.HOSTS_DIR]
        lv = artifact_level(f)
        out.append({
            "artifact": str(f), "skill": s.name, "type": s.type,
            "source_sha256": tuning.source_hash(lv.source()),
            "write_to": str(f / tuning.HOSTS_DIR / tuning.addition_name(chain[-1], ".md")),
            "existing": [str(a.path) for a in lv.additions(chain)],
            "text": tuning.render(s.text, tuning.layers(levels, chain)),
        })
    return out


def stamp_addition(path: Path, templates: Iterable[Level] = ()) -> tuple[Level, bool]:
    """Stamp `path` with its level's current source hash. (level, changed)."""
    parsed = tuning.parse_name(path.name)
    if parsed is None:
        raise PayloadError(f"{path} is not an addition (<target>{tuning.MARK}.md or .yaml)")
    level = level_of(path, templates)
    old = path.read_text(encoding="utf-8")
    new = tuning.stamp(old, parsed[1], tuning.source_hash(level.source()))
    if new != old:
        path.write_text(new, encoding="utf-8")
    return level, new != old
