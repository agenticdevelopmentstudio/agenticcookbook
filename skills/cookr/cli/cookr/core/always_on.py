"""Always-on skills: the few compiled skills installed straight into a host's
skills dir instead of being reached through skill-router.

There is one: the principles skill. It lists every principle in a set, with
a one-line gist and the routed skill that holds its full text, and the
pipeline concerns (`workflows/pipeline-concerns.json`) every implementation
applies or asks about. It replaces a hand-kept list that went stale as
principles were added.

Its template (`data/templates/always/principles.md`) holds the prose and, in
its frontmatter, the description and the groups principles are sorted into
by tag. `data/templates/always/principles/hosts/` holds its tuning additions,
rendered for one target the same way a routed skill's are.
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path
from typing import Iterable, Optional

import yaml

from . import skill as skill_mod
from . import tuning
from .artifact import ArtifactError, load_folder

TEMPLATES = skill_mod.PACKAGED_TEMPLATES / "always"
PRINCIPLES = "principles"
CONCERNS = Path("workflows") / "pipeline-concerns.json"


class AlwaysOnError(ArtifactError):
    """A template, a concerns list, or a principle the skill cannot be built from."""


@dataclass(frozen=True)
class AlwaysOn:
    name: str
    text: str                   # the shared rendering, before any tuning
    hosts_dir: Path             # the template's tuning additions

    def render(self, chain: Iterable[str]) -> str:
        return tuning.render(self.text, tuning.layers([self.hosts_dir], chain))


def skill_name(library: Optional[str]) -> str:
    """`general-principles`, the name the hand-kept skill had, so instructions
    that load it keep working; a library cookbook's is `<library>-principles`."""
    if library in (None, skill_mod.DEFAULT_LIBRARY):
        return "general-principles"
    return f"{library}-principles"


def gist(summary: str) -> str:
    """A summary on one line: what a list of principles shows. The whole
    summary, since a first sentence alone often sets up the rule without
    stating it."""
    return " ".join(str(summary).split())


@lru_cache(maxsize=None)
def _template(root: Path) -> tuple[dict, str]:
    path = root / f"{PRINCIPLES}.md"
    try:
        fm, text = tuning.split(path.read_text(encoding="utf-8"))
    except OSError as e:
        raise AlwaysOnError(f"no always-on template: {e}") from e
    return yaml.safe_load("".join(fm or [])) or {}, text


def _group(tags: Iterable[str], groups: list[dict]) -> str:
    tags = set(tags)
    for g in groups:
        if tags & set(g.get("tags") or ()):
            return g["title"]
    return next(g["title"] for g in groups if g.get("default"))


def _link(line: str, name: Optional[str]) -> str:
    return f"{line} (`{name}`)" if name else line


def _names(folders: list[Path], library: Optional[str],
           compiled: Optional[dict[Path, str]]) -> dict[Path, Optional[str]]:
    """{folder: its routed skill}: the name compile gave it, or None when it
    did not compile; with no `compiled`, the name it would be given."""
    if compiled is not None:
        return {f: compiled.get(f.resolve()) for f in folders}
    return {f: skill_mod.skill_name(*skill_mod.path_below_type(f), library) for f in folders}


def _principles(folders: list[Path], names: dict[Path, Optional[str]],
                groups: list[dict]) -> tuple[str, int]:
    by_group: dict[str, list[str]] = {g["title"]: [] for g in groups}
    for folder in sorted(folders, key=lambda f: f.name):
        a = load_folder(folder)
        by_group[_group(a.meta.get("tags") or (), groups)].append(_link(
            f"- **{folder.name}**: {gist(a.meta.get('summary') or a.meta.get('title') or '')}",
            names[folder]))
    sections = [f"## {title}\n\n" + "\n".join(lines) for title, lines in by_group.items() if lines]
    return "\n\n".join(sections), sum(map(len, by_group.values()))


def _concern_skill(path: str, by_rel: dict[str, Path], names: dict[Path, Optional[str]]) -> Optional[str]:
    """The routed skill a concern's `guideline_path` names, or None when it
    names no artifact in the set that compiles."""
    rel = re.sub(r"^.*?\bcookbook/", "", path.replace("\\", "/"))
    rel = rel[:-3] if rel.endswith(".md") else rel
    folder = by_rel.get(rel)
    return None if folder is None else names[folder]


def _concerns(path: Optional[Path], folders: list[Path], names: dict[Path, Optional[str]]) -> dict[str, str]:
    """{"always": list, "ask": list} as markdown, empty when there is no list."""
    out = {"always": [], "ask": []}
    if path is not None and path.is_file():
        try:
            items = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as e:
            raise AlwaysOnError(f"{path}: {e}") from e
        by_rel = {}
        for f in folders:
            type_dir, rel = skill_mod.path_below_type(f)
            by_rel["/".join((type_dir, *rel))] = f
        seen = set()
        for item in sorted(items, key=lambda i: i.get("step", 0)):
            apply, concern = item.get("apply"), item.get("concern")
            if apply not in out or not concern or concern in seen:
                continue
            seen.add(concern)
            name = _concern_skill(str(item.get("guideline_path") or ""), by_rel, names)
            out[apply].append(_link(f"- **{concern}**: {gist(item.get('summary') or '')}", name))
    return {k: "\n".join(v) or "_None._" for k, v in out.items()}


def principles_skill(folders: list[Path], *, library: Optional[str] = None,
                     concerns: Optional[Path] = None,
                     compiled: Optional[dict[Path, str]] = None,
                     templates: Path = TEMPLATES) -> Optional[AlwaysOn]:
    """The principles skill for the principle folders among `folders`, or
    None when there are none. `concerns` is the pipeline concerns list; its
    entries link to the routed skill of any artifact in `folders`.
    `compiled` ({resolved folder: skill name}, from compiling the set) limits
    the links to skills that exist; a folder missing from it is listed unlinked."""
    library = skill_mod.library_name(library)
    principles = [f for f in folders if skill_mod.path_below_type(f)[0] == PRINCIPLES]
    if not principles:
        return None
    meta, body = _template(templates)
    groups = list(meta.get("groups") or ())
    if sum(bool(g.get("default")) for g in groups) != 1:
        raise AlwaysOnError("the always-on template needs exactly one default group")
    names = _names(folders, library, compiled)
    listed, count = _principles(principles, names, groups)
    lists = _concerns(concerns, folders, names)
    name = skill_name(library)
    description = " ".join(str(meta.get("description", "")).split()).replace("{{count}}", str(count))
    front = "\n".join(["---", f"name: {name}", f"description: {skill_mod._dq(description)}",
                       "metadata:", f"  source: {skill_mod._dq(library or skill_mod.DEFAULT_LIBRARY)}",
                       "  compiled-by: \"cookr\"", "---", ""])
    text = skill_mod.fill(body, {"principles": listed, "always": lists["always"],
                                 "ask": lists["ask"], "count": str(count)})
    return AlwaysOn(name=name, text=front + text, hosts_dir=templates / PRINCIPLES / tuning.HOSTS_DIR)
