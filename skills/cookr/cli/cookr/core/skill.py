"""The `skill` target: an artifact folder compiled into a routed skill.

    <out>/
      targets.json                 the host table the router resolves a model with
      skills.json                  receipt: every skill this out dir holds, so a
                                   recompile prunes what no longer exists
      <name>/SKILL.md              the shared rendering; loads on every host
      <name>/targets/<target>.SKILL.md   a rendering for one target, written only where
                                   its additions change the text

A reader wanting `claude-opus-5-5` walks its chain most specific first
(`claude.opus-5-5`, `claude.opus`, `claude`) and takes the first variant that
exists, else `SKILL.md`. A variant is written only when it differs from the
rendering one step less specific, so a missing one always means "same as the
step before".

**Names** are the artifact's path below its type directory, joined with `-`
(`implementing-data-transactions-and-concurrency`); a one-segment path keeps its
type (`principle-simplicity`) and a library cookbook prefixes its library
(`adtoolkit-ui-controls-badge`). A name over the hosts' limit is cut and given
a hash of the full name, so it stays unique and stable.

**Routes** are derived from the path (`derive_routes`), unless `artifact.json`
gives `routes`. Every route node is held to FANOUT_CAP entries, so each step
of a drill-down is a list a model can read.

**Templates** (`data/templates/skill/<type>.md`) pick the parts: their
frontmatter lists the headings to `omit`, and their text wraps `{{body}}`.
`data/templates/skill/<type>/hosts/` holds the type's tuning additions, the
level applied before the artifact's own `hosts/`.
"""

from __future__ import annotations

import hashlib
import json
import os
import re
import shutil
from collections import defaultdict
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path
from typing import Iterable, Optional

import yaml

from . import hosts as hosts_mod
from . import tuning
from .artifact import ArtifactError, Artifact, load_folder
from .roots import MANIFEST as COOKBOOK_FILE

PACKAGED_TEMPLATES = Path(__file__).resolve().parent.parent / "data" / "templates"
TEMPLATES = PACKAGED_TEMPLATES / "skill"
# Where the templates live in the repo cookr ships from (agenticcookbook).
SOURCE_TEMPLATES = Path("skills") / "cookr" / "cli" / "cookr" / "data" / "templates"
TEMPLATES_ENV = "COOKR_TEMPLATES"
SKILL_FILE = "SKILL.md"
VARIANTS_DIR = "targets"
VARIANT_SUFFIX = ".SKILL.md"    # never <target>.md: claude.md is CLAUDE.md case-insensitively
RECEIPT = "skills.json"
TARGETS_FILE = "targets.json"
TYPE_DIRS = {"principles": "principle", "guidelines": "guideline",
             "ingredients": "ingredient", "recipes": "recipe"}
FANOUT_CAP = 50
NAME_MAX = 64
DESCRIPTION_MAX = 1024
DEFAULT_LIBRARY = "cookbook"
LIBRARY_MAX = 32
_LIBRARY = re.compile(r"[a-z0-9]+(?:-[a-z0-9]+)*")

# Hosts that forbid `<` and `>` in a description get the look-alike.
_ANGLE = (("<=", "≤"), (">=", "≥"), ("<", "‹"), (">", "›"))


class SkillError(ArtifactError):
    """An artifact that cannot become a skill."""


@dataclass(frozen=True)
class Template:
    omit: frozenset[str]
    text: str


@dataclass(frozen=True)
class Skill:
    name: str
    routes: tuple[str, ...]
    text: str                   # the shared SKILL.md
    folder: Path
    type: str


def templates_root(cookbook_root: Optional[Path] = None) -> Path:
    """The directory holding the `skill/` and `always/` templates: $COOKR_TEMPLATES;
    else, when the cookbook is the repo cookr ships from, that checkout's
    copy, so compiling renders and a tuning pass edits the source rather
    than the copy cookr was installed with; else that installed copy."""
    env = os.environ.get(TEMPLATES_ENV)
    if env:
        return Path(env).expanduser()
    if cookbook_root is not None:
        src = cookbook_root.resolve().parent / SOURCE_TEMPLATES
        if src.is_dir():
            return src
    return PACKAGED_TEMPLATES


# ── naming and routes ────────────────────────────────────────────────────────

def library_name(value: Optional[str]) -> Optional[str]:
    """A `--library` value as skill names use it: None for the default
    library (whose names carry no prefix, however it is spelled), else a
    lowercase, hyphenated name that can begin a skill name."""
    if value is None or value == DEFAULT_LIBRARY:
        return None
    if not _LIBRARY.fullmatch(value) or len(value) > LIBRARY_MAX:
        raise SkillError(f"library {value!r}: use lowercase letters, digits and single hyphens, "
                         f"at most {LIBRARY_MAX} characters (e.g. `adtoolkit`)")
    return value


def path_below_type(folder: Path) -> tuple[str, tuple[str, ...]]:
    """(type dir, the folder's path segments below it).

    A library cookbook groups its specs by concept, not by type, so a folder
    under no type directory is placed below its cookbook's root (the nearest
    directory holding cookbook.json), under the type dir of its own `type`."""
    resolved = folder.resolve()
    parts = resolved.parts
    for i in range(len(parts) - 1, -1, -1):
        if parts[i] in TYPE_DIRS:
            rel = parts[i + 1:]
            if rel:
                return parts[i], tuple(rel)
    root = next((d for d in resolved.parents if (d / COOKBOOK_FILE).is_file()), None)
    if root is not None:
        kind = load_folder(folder).type
        type_dir = next((d for d, k in TYPE_DIRS.items() if k == kind), None)
        if type_dir is None:
            raise SkillError(f"{folder}: type {kind!r} is not one of {', '.join(TYPE_DIRS.values())}")
        return type_dir, resolved.relative_to(root).parts
    raise SkillError(f"{folder}: not under a {', '.join(TYPE_DIRS)} directory or a cookbook "
                     f"({COOKBOOK_FILE})")


def skill_name(type_dir: str, rel: tuple[str, ...], library: Optional[str] = None) -> str:
    segments = list(rel) if len(rel) > 1 else [TYPE_DIRS[type_dir], *rel]
    if library:
        segments.insert(0, library)
    name = "-".join(segments)
    if len(name) <= NAME_MAX:
        return name
    digest = hashlib.sha256(name.encode("utf-8")).hexdigest()[:6]
    return f"{name[:NAME_MAX - 7].rstrip('-')}-{digest}"


def derive_routes(artifact: Artifact, type_dir: str, rel: tuple[str, ...],
                  library: Optional[str] = None) -> tuple[str, ...]:
    """The routes for an artifact with no `routes` of its own:

    - guideline: `coding/<phase>/<category>`, and per trigger
      `coding/when/<trigger>/<phase>/<category>`;
    - principle: `principles`;
    - ingredient or recipe: `components/<library>/<group…>`, and per platform
      `components/<library>/platform/<platform>/<group…>`.
    """
    if artifact.routes is not None:
        return tuple(artifact.routes)
    kind = TYPE_DIRS[type_dir]
    where = list(rel[:-1])
    if kind == "principle":
        return ("principles",)
    if kind == "guideline":
        triggers = artifact.meta.get("triggers") or []
        return ("/".join(["coding", *where]),
                *("/".join(["coding", "when", str(t), *where]) for t in triggers))
    lib = library or DEFAULT_LIBRARY
    platforms = artifact.meta.get("platforms") or []
    return ("/".join(["components", lib, *where]),
            *("/".join(["components", lib, "platform", str(p), *where]) for p in platforms))


def fanout(entries: Iterable[tuple[str, Iterable[str]]]) -> dict[str, int]:
    """Entries at every route node: its distinct next tiers plus the skills
    that stop there. Synonym tiers count once per synonym set, without the
    router's merging of overlapping sets, so this never under-counts."""
    children: dict[tuple, set] = defaultdict(set)
    here: dict[tuple, set] = defaultdict(set)
    for name, routes in entries:
        for route in routes:
            tiers = tuple(frozenset(w.strip().casefold() for w in t.split(","))
                          for t in route.split("/"))
            for n in range(len(tiers)):
                children[tiers[:n]].add(tiers[n])
            here[tiers].add(name)
    nodes = set(children) | set(here)
    return {"/".join(",".join(sorted(t)) for t in node): len(children[node]) + len(here[node])
            for node in nodes}


def over_cap(entries: Iterable[tuple[str, Iterable[str]]], cap: int = FANOUT_CAP) -> dict[str, int]:
    return {node: n for node, n in fanout(entries).items() if n > cap}


# ── composition ──────────────────────────────────────────────────────────────

@lru_cache(maxsize=None)
def template(kind: str, root: Path = TEMPLATES) -> Template:
    path = root / f"{kind}.md"
    try:
        fm, text = tuning.split(path.read_text(encoding="utf-8"))
    except OSError as e:
        raise SkillError(f"no skill template for {kind!r}: {e}") from e
    meta = yaml.safe_load("".join(fm or [])) or {}
    return Template(omit=frozenset(meta.get("omit") or ()), text=text)


def template_hosts(kind: str, root: Path = TEMPLATES) -> Path:
    return root / kind / tuning.HOSTS_DIR


def description(artifact: Artifact) -> str:
    text = " ".join(str(artifact.meta.get("summary") or artifact.meta.get("title") or "").split())
    triggers = artifact.meta.get("triggers") or []
    if triggers:
        text = f"{text.rstrip('.')}. Use when: {', '.join(map(str, triggers))}."
    for a, b in _ANGLE:
        text = text.replace(a, b)
    if len(text) > DESCRIPTION_MAX:
        text = text[:DESCRIPTION_MAX - 1].rstrip() + "…"
    return text


def _dq(s: str) -> str:
    return '"' + s.replace("\\", "\\\\").replace('"', '\\"') + '"'


def frontmatter(name: str, artifact: Artifact, routes: Iterable[str]) -> str:
    """Only `name` and `description` at the top, every cookr key under
    `metadata`, so the one rendering loads on every host."""
    meta = artifact.meta
    lines = ["---", f"name: {name}", f"description: {_dq(description(artifact))}", "metadata:",
             f"  version: {_dq(str(meta.get('version', '')))}",
             f"  id: {_dq(str(meta.get('id', '')))}",
             f"  source: {_dq(str(meta.get('domain', '')))}",
             f"  routes: {_dq('; '.join(routes))}", "---", ""]
    return "\n".join(lines)


_PLACEHOLDER = re.compile(r"\{\{(\w+)\}\}")


def fill(template: str, values: dict[str, str]) -> str:
    """`template` with each `{{key}}` of `values` replaced, in one pass: text
    a value brings in (an artifact quoting `{{version}}`, say) stays as written."""
    return _PLACEHOLDER.sub(lambda m: values.get(m.group(1), m.group(0)), template)


def compose(folder: Path, library: Optional[str] = None, templates: Path = TEMPLATES) -> Skill:
    library = library_name(library)
    artifact = load_folder(folder)
    type_dir, rel = path_below_type(folder)
    kind = TYPE_DIRS[type_dir]
    if artifact.type != kind:
        raise SkillError(f"{folder}: type {artifact.type!r} under {type_dir}/")
    t = template(kind, templates)
    body = "".join(p.text if p.heading is None else f"## {p.heading}\n{p.text}"
                   for p in artifact.parts if (p.heading or "").strip() not in t.omit)
    if not body.endswith("\n\n"):
        body = body.rstrip("\n") + "\n\n"
    text = fill(t.text.replace("{{body}}\n", "{{body}}"),
                {"body": body, "domain": str(artifact.meta.get("domain", "")),
                 "version": str(artifact.meta.get("version", ""))})
    name = skill_name(type_dir, rel, library)
    routes = derive_routes(artifact, type_dir, rel, library)
    return Skill(name=name, routes=routes, text=frontmatter(name, artifact, routes) + text,
                 folder=folder, type=kind)


def target_chains(hosts: Optional[dict] = None) -> dict[str, tuple[str, ...]]:
    """Every target rendered ahead of time, with its chain."""
    hosts = hosts_mod.manifest() if hosts is None else hosts
    out: dict[str, tuple[str, ...]] = {}
    for h in hosts.values():
        out[h.name] = (h.name,)
        for f in h.families:
            out[f"{h.name}.{f}"] = (h.name, f"{h.name}.{f}")
        for m in h.models:
            c = h.chain(m)
            out[c[-1]] = c
    return out


def variants(skill: Skill, templates: Path = TEMPLATES,
             hosts: Optional[dict] = None) -> tuple[dict[str, str], list[str]]:
    """({target: text} for each target whose text differs from the step less
    specific, [load-rule problems on any host])."""
    hosts = hosts_mod.manifest() if hosts is None else hosts
    levels = [template_hosts(skill.type, templates), skill.folder / tuning.HOSTS_DIR]
    rendered: dict[tuple[str, ...], str] = {(): skill.text}
    out: dict[str, str] = {}
    problems: list[str] = []
    for h in hosts.values():
        problems += [f"{h.name}: {p}" for p in tuning.load_problems(skill.text, h)]
    for target, chain in target_chains(hosts).items():
        for i in range(1, len(chain) + 1):
            step = chain[:i]
            if step not in rendered:
                rendered[step] = tuning.render(skill.text, tuning.layers(levels, step))
        text = rendered[chain]
        if text != rendered[chain[:-1]]:
            out[target] = text
            problems += [f"{target}: {p}" for p in tuning.load_problems(text, hosts[chain[0]])]
    return out, problems


def targets_table(hosts: Optional[dict] = None) -> dict:
    """What a reader needs to turn a model ID into a chain without cookr."""
    hosts = hosts_mod.manifest() if hosts is None else hosts
    return {"format": 1, "hosts": {
        h.name: {"model_prefix": h.model_prefix, "default_model": h.default_model,
                 "families": dict(h.families)} for h in hosts.values()}}


def dump_json(data: dict) -> str:
    return json.dumps(data, indent=2, ensure_ascii=False) + "\n"


# ── the out dir ──────────────────────────────────────────────────────────────

@dataclass
class Built:
    skill: Skill
    files: dict[str, str]       # path relative to the out dir → text
    problems: list[str]


def build(skill: Skill, templates: Path = TEMPLATES, hosts: Optional[dict] = None) -> Built:
    vs, problems = variants(skill, templates, hosts)
    files = {f"{skill.name}/{SKILL_FILE}": skill.text}
    files.update({f"{skill.name}/{VARIANTS_DIR}/{t}{VARIANT_SUFFIX}": text for t, text in vs.items()})
    return Built(skill, files, problems)


def read_receipt(out: Path) -> dict[str, dict]:
    path = out / RECEIPT
    if not path.is_file():
        return {}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        raise SkillError(f"{path}: {e}") from e
    return dict(data.get("skills", {}))


def receipt(built: list[Built], library: Optional[str]) -> dict:
    return {"format": 1, "library": library or DEFAULT_LIBRARY, "skills": {
        b.skill.name: {"source": str(b.skill.folder), "routes": list(b.skill.routes),
                       "files": sorted(b.files)} for b in built}}


def remove_stale(out: Path, old: dict[str, dict], built: list[Built]) -> list[str]:
    """Delete what the last compile wrote and this one does not: whole skills
    that are gone, and variant files no longer needed. Nothing the receipt
    does not list is touched."""
    keep = {f for b in built for f in b.files}
    removed = []
    for name, entry in old.items():
        for rel in entry.get("files", []):
            if rel not in keep and (out / rel).is_file():
                (out / rel).unlink()
                removed.append(rel)
        for d in (out / name / VARIANTS_DIR, out / name):
            if d.is_dir() and not any(d.iterdir()):
                shutil.rmtree(d)
    return removed


_SAFE = re.compile(r"^[a-z0-9][a-z0-9-]*(/[A-Za-z0-9._-]+)*$")


def write_files(out: Path, files: dict[str, str]) -> dict[str, str]:
    """Write each file whose text differs; {rel: "compiled" | "unchanged"}."""
    status = {}
    for rel, text in files.items():
        if not _SAFE.match(rel):
            raise SkillError(f"refusing to write outside a skill dir: {rel!r}")
        dest = out / rel
        if dest.is_file() and dest.read_text(encoding="utf-8") == text:
            status[rel] = "unchanged"
            continue
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(text, encoding="utf-8")
        status[rel] = "compiled"
    return status


def duplicate_names(skills: Iterable[Skill]) -> dict[str, list[Path]]:
    seen: dict[str, list[Path]] = defaultdict(list)
    for s in skills:
        seen[s.name].append(s.folder)
    return {n: fs for n, fs in seen.items() if len(fs) > 1}


@dataclass
class SetReport:
    results: list            # artifact_build.Result, one per artifact
    over_cap: dict[str, int]
    removed: list[str]

    @property
    def failed(self) -> bool:
        return bool(self.over_cap) or any(r.failed for r in self.results)


def compile_set(folders: list[Path], out: Path, *, library: Optional[str] = None,
                write: bool = True, templates: Path = TEMPLATES,
                hosts: Optional[dict] = None) -> SetReport:
    """Compile every folder into `out` as one skill set, or with write=False
    report whether `out` is current. A set with a duplicate name, a rendering
    that would not load on its host, or a route node over FANOUT_CAP fails."""
    from .artifact_build import Result

    library = library_name(library)
    results, skills = [], []
    for folder in folders:
        try:
            skills.append(compose(folder, library, templates))
        except (ArtifactError, OSError, UnicodeDecodeError, tuning.TuningError) as e:
            results.append(Result(folder, folder, "error", str(e)))
    dups = duplicate_names(skills)
    for name, fs in dups.items():
        for f in fs:
            results.append(Result(f, out / name, "error",
                                  f"name {name!r} also derived for {', '.join(str(o) for o in fs if o != f)}"))
    built = []
    for s in (s for s in skills if s.name not in dups):
        try:
            built.append(build(s, templates, hosts))
        except tuning.TuningError as e:
            results.append(Result(s.folder, out / s.name, "error", str(e)))
    capped = over_cap((b.skill.name, b.skill.routes) for b in built)
    old = read_receipt(out)
    shared = {TARGETS_FILE: dump_json(targets_table(hosts)), RECEIPT: dump_json(receipt(built, library))}
    removed: list[str] = []
    if write:
        out.mkdir(parents=True, exist_ok=True)
        removed = remove_stale(out, old, built)
    for b in built:
        if b.problems:
            results.append(Result(b.skill.folder, out / b.skill.name, "broken",
                                  "would not load: " + "; ".join(b.problems)))
            continue
        if write:
            status = write_files(out, b.files)
            results.append(Result(b.skill.folder, out / b.skill.name,
                                  "compiled" if "compiled" in status.values() else "unchanged"))
            continue
        current = [(out / rel).read_text(encoding="utf-8") if (out / rel).is_file() else None
                   for rel in b.files]
        extra = [rel for rel in old.get(b.skill.name, {}).get("files", []) if rel not in b.files]
        state = ("missing" if all(c is None for c in current) else
                 "stale" if current != list(b.files.values()) or extra else "unchanged")
        results.append(Result(b.skill.folder, out / b.skill.name, state))
    if write:
        for rel, text in shared.items():
            (out / rel).write_text(text, encoding="utf-8")
    else:
        gone = sorted(set(old) - {b.skill.name for b in built})
        removed = [f"{n} (would remove)" for n in gone]
        results += [Result(out / n, out / n, "stale", "no longer compiled") for n in gone]
        for rel, text in shared.items():
            p = out / rel
            if not p.is_file() or p.read_text(encoding="utf-8") != text:
                results.append(Result(p, p, "stale" if p.is_file() else "missing"))
    return SetReport(sorted(results, key=lambda r: str(r.source)), capped, removed)
