"""UUID links and cross-cookbook resolution.

A link is `<artifact-uuid>` (this cookbook) or `<cookbook-uuid>/<artifact-uuid>`.
Resolution never raises for an absent or unreadable dependency cookbook: that is
the `unreachable` state, a warning for callers, not an error.
"""

from __future__ import annotations

import json
import os
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

from .errors import CookbookError
from .identity import CookbookIdentity, is_rdid, is_uuid
from .index import INDEX_FILE, INDEX_FORMAT, Entry, Index, current_index, load_index
from .repoconfig import Dependency  # noqa: F401  (re-exported)

IN_TEXT = re.compile(r"\[([^\]]+)\]\(cookbook:([0-9A-Fa-f-]{36}(?:/[0-9A-Fa-f-]{36})?)\)")
LOCATIONS = Path("~/.cookr/locations.json")


@dataclass(frozen=True)
class Link:
    cookbook: Optional[str]
    artifact: str


@dataclass
class Resolved:
    link: Link
    state: str  # ok | missing | unreachable
    rdid: Optional[str]
    entry: Optional[Entry]


def parse_link(s: str) -> Link:
    parts = s.strip().lower().split("/")
    if len(parts) not in (1, 2) or not all(is_uuid(p) for p in parts):
        raise ValueError(f"{s!r} is not a UUID link")
    return Link(parts[0], parts[1]) if len(parts) == 2 else Link(None, parts[0])


def format_link(link: Link) -> str:
    return f"{link.cookbook}/{link.artifact}" if link.cookbook else link.artifact


def in_text_links(text: str) -> list[tuple[str, Link]]:
    found = []
    for m in IN_TEXT.finditer(text):
        try:
            found.append((m.group(1), parse_link(m.group(2))))
        except ValueError:
            continue
    return found


def relabel(text: str, labels: dict[Link, str]) -> str:
    def sub(m: re.Match) -> str:
        try:
            link = parse_link(m.group(2))
        except ValueError:
            return m.group(0)
        label = labels.get(link, m.group(1))
        return f"[{label}](cookbook:{m.group(2)})"
    return IN_TEXT.sub(sub, text)


def _locations_path() -> Path:
    home = os.environ.get("COOKR_HOME")
    return Path(home) / "locations.json" if home else LOCATIONS.expanduser()


def read_locations() -> dict[str, dict]:
    try:
        data = json.loads(_locations_path().read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}
    return data if isinstance(data, dict) else {}


def remember_location(identity: CookbookIdentity, path: Path, legacy_scheme: Optional[str]) -> None:
    locs = read_locations()
    entry: dict = {"rdid": identity.rdid, "path": str(path)}
    if legacy_scheme:
        entry["legacy_scheme"] = legacy_scheme
    locs[identity.id.lower()] = entry
    target = _locations_path()
    target.parent.mkdir(parents=True, exist_ok=True)
    tmp = target.with_name(target.name + ".tmp")
    tmp.write_text(json.dumps(locs, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    os.replace(tmp, target)


def _load_or_derive(cookbook_dir: Path) -> Optional[Index]:
    """The cookbook's index.json; for one not upgraded yet (no index.json, or a
    format-1 one), the index the upgrade would write, derived in memory. None
    when neither can be had: the dependency is unreachable."""
    path = cookbook_dir / INDEX_FILE
    try:
        fmt = json.loads(path.read_text(encoding="utf-8")).get("format") if path.is_file() else None
    except (OSError, json.JSONDecodeError, AttributeError):
        return None
    try:
        if fmt == INDEX_FORMAT:
            return load_index(cookbook_dir)
        from .upgrade import derive_index  # upgrade imports this module
        return derive_index(cookbook_dir)
    except (CookbookError, OSError, ValueError):
        return None


class Resolver:
    def __init__(self, repo_root: Path, own: Index, dependencies: dict[str, Dependency]):
        self.repo_root = Path(repo_root)
        self.own = own
        self.dependencies = dependencies
        self._cache: dict[str, Index] = {}
        self._dirs: dict[str, Path] = {}

    def _candidates(self, cookbook_id: str) -> list[Path]:
        paths: list[Path] = []
        dep = self.dependencies.get(cookbook_id)
        # A committed location is relative to the repo (a submodule, or a sibling
        # checkout); an absolute one is a path on one machine, never read from config.
        if dep and dep.location and "://" not in dep.location \
                and not Path(dep.location).expanduser().is_absolute():
            paths.append(self.repo_root / dep.location)
        loc = read_locations().get(cookbook_id)
        if isinstance(loc, dict) and loc.get("path"):
            paths.append(Path(loc["path"]).expanduser())
        return paths

    def index_for(self, cookbook_id: str) -> Optional[Index]:
        cookbook_id = cookbook_id.lower()
        if cookbook_id == self.own.cookbook.id:
            return self.own
        # Only a found index is cached: an unreachable cookbook is looked for again,
        # so one that arrives (a submodule checked out) is seen by this resolver.
        if cookbook_id not in self._cache:
            for path in self._candidates(cookbook_id):
                if not path.is_dir():
                    continue
                found = _load_or_derive(path)
                if found is not None:
                    self._dirs[cookbook_id] = path
                    self._cache[cookbook_id] = found
                    break
        return self._cache.get(cookbook_id)

    def dir_for(self, cookbook_id: str) -> Optional[Path]:
        """The directory a reachable dependency cookbook was loaded from."""
        cookbook_id = cookbook_id.lower()
        return self._dirs.get(cookbook_id) if self.index_for(cookbook_id) is not None else None

    def resolve(self, link: Link) -> Resolved:
        index = self.own if link.cookbook is None else self.index_for(link.cookbook)
        if index is None:
            return Resolved(link, "unreachable", None, None)
        entry = index.entries.get(link.artifact)
        if entry is None:
            return Resolved(link, "missing", None, None)
        return Resolved(link, "ok", entry.rdid, entry)


def resolver_for(config, own: Optional[Index] = None) -> Resolver:
    """A resolver for a repo config (`repoconfig.Config`): its cookbook's current
    index (or `own`) and its dependencies."""
    return Resolver(config.repo_root, own if own is not None else current_index(config.cookbook_dir),
                    config.dependencies)


def stale_labels(own: Index, resolver: Resolver) -> dict[str, tuple[str, str]]:
    stale: dict[str, tuple[str, str]] = {}
    for key, cached in own.foreign.items():
        try:
            res = resolver.resolve(parse_link(key))
        except ValueError:
            continue
        if res.state == "ok" and res.rdid != cached:
            stale[key] = (cached, res.rdid)
    return stale


# ── authoring by rdid ───────────────────────────────────────────────────────

AUTHORED_IN_TEXT = re.compile(r"\[([^\]]+)\]\(cookbook:([^)\s]+)\)")


def _cookbook_id(token: str, resolver: Resolver) -> str:
    if is_uuid(token):
        return token.lower()
    if token == resolver.own.cookbook.rdid:
        return resolver.own.cookbook.id
    for cid, dep in resolver.dependencies.items():
        if dep.rdid == token:
            return cid.lower()
    raise CookbookError(f"{token!r} matches no cookbook this repo knows")


def _entry_in(index: Index, token: str) -> Optional[Entry]:
    return index.get(token.lower() if is_uuid(token) else token)


def lookup(value: str, resolver: Resolver) -> tuple[Link, Entry]:
    """The link and index entry a UUID or rdid names; `<cookbook>/<artifact>`
    (each an rdid or UUID) reaches a dependency. Raises CookbookError naming
    `value` when nothing matches or the cookbook holding it is unreachable."""
    v = value.strip()
    own = resolver.own
    if "/" in v:
        parts = v.split("/")
        if len(parts) != 2 or not all(parts):
            raise CookbookError(f"{value!r} is not <cookbook>/<artifact>")
        cid = _cookbook_id(parts[0], resolver)
        index = resolver.index_for(cid)
        if index is None:
            raise CookbookError(f"{value!r}: cookbook {parts[0]} is unreachable")
        entry = _entry_in(index, parts[1])
        if entry is None:
            raise CookbookError(f"{value!r} matches no artifact in {parts[0]}")
        return Link(None if cid == own.cookbook.id else cid, entry.id), entry
    if not (is_uuid(v) or is_rdid(v)):
        raise CookbookError(f"{value!r} is neither a UUID nor an rdid")
    entry = _entry_in(own, v)
    if entry is not None:
        return Link(None, entry.id), entry
    if is_rdid(v):
        owners = [(cid, dep) for cid, dep in resolver.dependencies.items()
                  if v.startswith(dep.rdid + ".")]
        if owners:
            cid, dep = max(owners, key=lambda o: len(o[1].rdid))
            index = resolver.index_for(cid)
            if index is None:
                raise CookbookError(f"{value!r}: cookbook {dep.rdid} is unreachable")
            found = _entry_in(index, v)
            if found is None:
                raise CookbookError(f"{value!r} matches no artifact in {dep.rdid}")
            return Link(cid.lower(), found.id), found
    raise CookbookError(f"{value!r} matches no artifact")


def to_stored(value: str, resolver: Resolver) -> str:
    """The stored (UUID) form of a link authored as an rdid or a UUID. A value
    already in UUID form is returned as is (validate checks it exists); an rdid
    that cannot be resolved raises, so one is never stored."""
    try:
        return format_link(parse_link(value))
    except ValueError:
        pass
    return format_link(lookup(value, resolver)[0])


def is_authored_link(value: str) -> bool:
    """Whether `value` is shaped like something `to_stored` converts."""
    parts = value.strip().split("/")
    return len(parts) in (1, 2) and all(is_uuid(p) or is_rdid(p) for p in parts)


def to_stored_text(text: str, resolver: Resolver, problems: list[str]) -> str:
    """`text` with every `[label](cookbook:<rdid>)` made `[<rdid>](cookbook:<uuid>)`.
    A target that cannot be resolved stays as written and is added to `problems`."""
    def sub(m: re.Match) -> str:
        target = m.group(2)
        if not is_authored_link(target) or IN_TEXT.fullmatch(m.group(0)):
            return m.group(0)
        try:
            link, entry = lookup(target, resolver)
        except CookbookError as e:
            problems.append(str(e))
            return m.group(0)
        return f"[{entry.rdid}](cookbook:{format_link(link)})"
    return AUTHORED_IN_TEXT.sub(sub, text)
