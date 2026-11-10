"""`.cookr.json` format 2: the repo config. It holds what the cookbook does not.

{"format": 2, "cookbook": "cookbook",
 "dependencies": {"<cookbook-uuid>": {"rdid": "adhsdk", "location": "external/adhsdk/cookbook"}},
 "roots": [{"path": "App/Sources", "platform": "macos", "kind": "ui", "group": "app"}],
 "ignore": ["**/Generated/**"]}

A cookbook with no `.cookr.json` still loads (`config_for_cookbook`) with no roots.
A format-1 `.cookr.json`, or a `cookbook.json` still carrying a `code` block, raises
`NeedsUpgrade`, which carries the offending path.
"""

from __future__ import annotations

import json
import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

from .errors import CookbookError
from .identity import MANIFEST, CookbookIdentity, IdentityError, is_uuid, read_manifest

PLATFORMS = ("macos", "ios", "apple", "web", "android", "windows", "linux", "python")
KINDS = ("ui", "logic")
CONFIG_NAME = ".cookr.json"
CONFIG_FORMAT = 2
COOKBOOK_DIR = "cookbook"


class ConfigError(CookbookError):
    """Raised when a config or manifest is missing, malformed, or names a bad path."""


class NeedsUpgrade(ConfigError):
    """A pre-format-2 file; `path` is the file to upgrade."""

    def __init__(self, path: Path, message: str = ""):
        self.path = Path(path)
        super().__init__(message or f"{path}: older format; run `cookr upgrade`")


@dataclass(frozen=True)
class Dependency:
    id: str
    rdid: str
    location: Optional[str] = None


@dataclass(frozen=True)
class Root:
    path: str
    platform: str
    kind: str = "ui"
    group: str = ""
    ignore: tuple = ()

    @property
    def tier(self) -> str:
        return self.group.split("/", 1)[0]


@dataclass(frozen=True)
class Config:
    repo_root: Path
    cookbook_dir: Path
    identity: CookbookIdentity
    roots: list = field(default_factory=list)
    ignore: list = field(default_factory=list)
    dependencies: dict = field(default_factory=dict)
    config_file: Optional[Path] = None

    @property
    def cookbook(self) -> str:
        return self.cookbook_dir.relative_to(self.repo_root).as_posix()

    def root_for(self, rel: str) -> Optional[Root]:
        best = None
        for r in self.roots:
            if rel == r.path or rel.startswith(r.path.rstrip("/") + "/"):
                if best is None or len(r.path) > len(best.path):
                    best = r
        return best

    def is_group(self, tier: str) -> bool:
        tier = tier.strip("/")
        return bool(tier) and ((self.cookbook_dir / tier).is_dir() or any(
            r.group == tier or r.group.startswith(tier + "/") for r in self.roots))

    @property
    def tiers(self) -> list[str]:
        listed = self.cookbook_dir.iterdir() if self.cookbook_dir.is_dir() else ()
        seen = {d.name for d in listed if d.is_dir() and not d.name.startswith(".")}
        seen |= {r.tier for r in self.roots if r.tier}
        return sorted(seen)


def find_repo(start: Path) -> Optional[Path]:
    start = Path(start).resolve()
    for d in (start, *start.parents):
        if (d / CONFIG_NAME).is_file() or (d / COOKBOOK_DIR / MANIFEST).is_file():
            return d
    return None


def _strings(v: object) -> bool:
    return isinstance(v, list) and all(isinstance(s, str) for s in v)


def _identity(cookbook_dir: Path) -> CookbookIdentity:
    path = cookbook_dir / MANIFEST
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as e:
        raise ConfigError(f"{path}: {e}") from e
    if isinstance(data, dict) and data.get("format") != 2 and "code" in data:
        raise NeedsUpgrade(path, f"{path}: format 1 cookbook.json; run `cookr upgrade`")
    try:
        return read_manifest(cookbook_dir)
    except IdentityError as e:
        raise ConfigError(str(e)) from e


def config_for_cookbook(cookbook_dir: Path) -> Config:
    cookbook_dir = Path(cookbook_dir)
    cookbook_dir = cookbook_dir.parent.resolve() / cookbook_dir.name
    return Config(repo_root=cookbook_dir.parent, cookbook_dir=cookbook_dir,
                  identity=_identity(cookbook_dir))


def in_repo_path(name: str) -> bool:
    """Whether a repo-relative path stays inside the repo: no `..` segment, not
    absolute, and no leading `~` (a shell expands it to a home directory).
    Lexical, so it holds for a path that does not exist yet."""
    p = Path(name)
    return ".." not in p.parts and not p.is_absolute() and not (p.parts and p.parts[0].startswith("~"))


def cookbook_dir_named(repo_root: Path, data: dict, path: Path) -> Path:
    """The cookbook directory a format-2 config's `cookbook` key names, confined
    to the repo: ConfigError for `..`, an absolute path or a non-string."""
    name = data.get("cookbook", COOKBOOK_DIR)
    if not isinstance(name, str) or not name or not in_repo_path(name):
        raise ConfigError(f"{path}: `cookbook` must be a directory inside the repo")
    return Path(repo_root) / name


@dataclass(frozen=True)
class ConfigFields:
    """A format-2 `.cookr.json`, validated, without the cookbook's identity (which
    a cookbook still on format 1 cannot give)."""
    cookbook_dir: Path
    roots: list
    ignore: list
    dependencies: dict
    config_file: Path


def config_format(data: dict, path: Path) -> Optional[int]:
    """A `.cookr.json`'s `format`: None (format 1) or an integer. Anything else
    ("2", 2.0, true) is a malformed config, never read as an older format."""
    fmt = data.get("format")
    if fmt is not None and type(fmt) is not int:
        raise ConfigError(f"{path}: `format` must be the integer {CONFIG_FORMAT}, "
                          f"not {json.dumps(fmt)}")
    return fmt


def load_repo_config(repo_root: Path) -> Config:
    f = read_config_fields(repo_root)
    return Config(Path(repo_root).resolve(), f.cookbook_dir, _identity(f.cookbook_dir), f.roots,
                  f.ignore, f.dependencies, f.config_file)


def read_config_fields(repo_root: Path) -> ConfigFields:
    """Every field of the repo's format-2 `.cookr.json`, validated as
    `load_repo_config` does; the cookbook's manifest is not read."""
    repo_root = Path(repo_root).resolve()
    path = repo_root / CONFIG_NAME
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except OSError as e:
        raise ConfigError(f"{path}: {e}") from e
    except json.JSONDecodeError as e:
        raise ConfigError(f"{path}: invalid JSON — {e}") from e
    if not isinstance(data, dict):
        raise ConfigError(f"{path}: top level must be an object")
    fmt = config_format(data, path)
    if fmt != CONFIG_FORMAT:
        raise NeedsUpgrade(path, f"{path}: format {fmt if fmt is not None else 1} config; "
                                 "run `cookr upgrade`")
    cookbook_dir = cookbook_dir_named(repo_root, data, path)

    deps: dict[str, Dependency] = {}
    raw_deps = data.get("dependencies", {})
    if not isinstance(raw_deps, dict):
        raise ConfigError(f"{path}: `dependencies` must be an object")
    for key, d in raw_deps.items():
        if not is_uuid(key):
            raise ConfigError(f"{path}: dependency key {key!r} is not a UUID")
        if not isinstance(d, dict) or not isinstance(d.get("rdid"), str) or not d["rdid"]:
            raise ConfigError(f"{path}: dependency {key} needs a string `rdid`")
        loc = d.get("location")
        if loc is not None and not isinstance(loc, str):
            raise ConfigError(f"{path}: dependency {key} `location` must be a string")
        if loc is not None and "://" not in loc and Path(loc).expanduser().is_absolute():
            raise ConfigError(f"{path}: dependency {key} `location` {loc!r} must be a path "
                              "relative to the repo or a URL; a path on one machine belongs "
                              "in ~/.cookr/locations.json")
        deps[key.lower()] = Dependency(key.lower(), d["rdid"], loc)

    raw_roots = data.get("roots", [])
    if not isinstance(raw_roots, list):
        raise ConfigError(f"{path}: `roots` must be a list")
    roots = []
    for i, r in enumerate(raw_roots):
        where = f"{path}: roots[{i}]"
        if not isinstance(r, dict):
            raise ConfigError(f"{where} must be an object")
        for k in ("path", "platform"):
            if not isinstance(r.get(k), str) or not r[k]:
                raise ConfigError(f"{where}.{k} must be a non-empty string")
        if r["platform"] not in PLATFORMS:
            raise ConfigError(f"{where}.platform `{r['platform']}` is not one of "
                              f"{', '.join(PLATFORMS)}")
        kind = r.get("kind", "ui")
        if kind not in KINDS:
            raise ConfigError(f"{where}.kind `{kind}` is not one of {', '.join(KINDS)}")
        group = r.get("group", "")
        if not isinstance(group, str) or ".." in group.split("/"):
            raise ConfigError(f"{where}.group must be a directory inside the cookbook")
        if not _strings(r.get("ignore", [])):
            raise ConfigError(f"{where}.ignore must be a list of strings")
        if not in_repo_path(r["path"]):
            raise ConfigError(f"{where}.path must be a directory inside the repo")
        rel = r["path"].strip("/")
        if not (repo_root / rel).is_dir():
            raise ConfigError(f"{where}.path not found: {r['path']}")
        roots.append(Root(rel, r["platform"], kind, group.strip("/"),
                          tuple(r.get("ignore", []))))

    ignore = data.get("ignore", [])
    if not _strings(ignore):
        raise ConfigError(f"{path}: `ignore` must be a list of strings")
    return ConfigFields(cookbook_dir, roots, list(ignore), deps, path)


def write_repo_config(config: Config) -> None:
    path = config.config_file or config.repo_root / CONFIG_NAME
    data: dict = {"format": CONFIG_FORMAT, "cookbook": config.cookbook}
    data["dependencies"] = {
        k: {"rdid": d.rdid, **({"location": d.location} if d.location else {})}
        for k, d in config.dependencies.items()}
    data["roots"] = [
        {"path": r.path, "platform": r.platform, "kind": r.kind,
         **({"group": r.group} if r.group else {}),
         **({"ignore": list(r.ignore)} if r.ignore else {})} for r in config.roots]
    data["ignore"] = list(config.ignore)
    tmp = path.with_name(path.name + ".tmp")
    tmp.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    os.replace(tmp, path)
