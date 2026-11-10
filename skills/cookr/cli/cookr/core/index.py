"""The cookbook index: `index.json`, the cookbook's table of contents.

Entries are keyed by UUID and carry the readable rdid, the folder `path`, and
the authored `implementations`. Edited only through cookr, never by hand.
"""

from __future__ import annotations

import json
import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

from .artifact import find_folders
from .errors import CookbookError
from .identity import (MANIFEST, TYPE_DIRS, CookbookIdentity, IdentityError, artifact_rdid,
                       read_manifest)

INDEX_FILE = "index.json"
INDEX_FORMAT = 2
KINDS = ("principle", "guideline", "ingredient", "recipe", "check")
# Stored conformance states, in rank order (cookr.core.conformance ranks them).
STATES = ("planned", "unverified", "needs-validation", "confirmed")


class IndexFileError(CookbookError):
    """A malformed index, or two entries claiming one rdid."""


@dataclass
class Conformance:
    state: str
    version: Optional[str] = None
    hash: Optional[str] = None


@dataclass
class Implementation:
    platform: str
    location: Optional[str]  # None only when conformance.state == "planned"
    conformance: Conformance


@dataclass
class Entry:
    id: str
    kind: str
    rdid: str
    path: str  # folder relative to the cookbook; a check's is `<document>#<name>`
    implementations: list[Implementation] = field(default_factory=list)


@dataclass
class Index:
    cookbook: CookbookIdentity
    entries: dict[str, Entry] = field(default_factory=dict)
    foreign: dict[str, str] = field(default_factory=dict)
    catalog: Optional[str] = None

    def get(self, key: str) -> Optional[Entry]:
        if key in self.entries:
            return self.entries[key]
        return next((e for e in self.entries.values() if e.rdid == key), None)

    def by_path(self, path: str) -> Optional[Entry]:
        return next((e for e in self.entries.values() if e.path == path), None)

    def owners(self, rel: str) -> list[tuple[Entry, Implementation]]:
        """Implementations claiming source file `rel`: its own row, else its deepest directory's."""
        table: dict[str, list[tuple[Entry, Implementation]]] = {}
        for e in self.entries.values():
            for impl in e.implementations:
                if impl.location and "://" not in impl.location:
                    table.setdefault(impl.location, []).append((e, impl))
        if rel in table:
            return table[rel]
        parts = rel.split("/")
        for i in range(len(parts) - 1, 0, -1):
            found = table.get("/".join(parts[:i]) + "/")
            if found:
                return found
        return []


def _check_collisions(entries: dict[str, Entry]) -> None:
    seen: dict[str, Entry] = {}
    for e in entries.values():
        other = seen.get(e.rdid)
        if other is not None:
            raise IndexFileError(
                f"rdid {e.rdid!r} is claimed by two entries: {other.path} and {e.path}")
        seen[e.rdid] = e


def _impl_from(d: dict, where: str) -> Implementation:
    c = d.get("conformance") or {}
    impl = Implementation(platform=d["platform"], location=d.get("location"),
                          conformance=Conformance(state=c["state"], version=c.get("version"),
                                                  hash=c.get("hash")))
    state = impl.conformance.state
    if state not in STATES:
        raise IndexFileError(f"{where}: conformance state {state!r} is not one of "
                             f"{', '.join(STATES)}")
    if impl.location is None and state != "planned":
        raise IndexFileError(f"{where}: the {impl.platform} row has no location; only a "
                             f"planned row may lack one, and this one is {state!r}")
    return impl


def _entry_from(uid: str, e: dict, path: str) -> Entry:
    where = f"{path}: entry {uid}"
    if e["kind"] not in KINDS:
        raise IndexFileError(f"{where}: kind {e['kind']!r} is not one of {', '.join(KINDS)}")
    return Entry(id=uid.lower(), kind=e["kind"], rdid=e["rdid"], path=e["path"],
                 implementations=[_impl_from(i, where) for i in e.get("implementations", [])])


def _entries_from(raw: dict, path: str) -> dict[str, Entry]:
    entries: dict[str, Entry] = {}
    for uid, e in raw.items():
        if uid.lower() in entries:
            raise IndexFileError(f"{path}: entries {entries[uid.lower()].id} and {uid} differ "
                                 "only in case; an artifact has one id")
        entries[uid.lower()] = _entry_from(uid, e, path)
    return entries


def _impl_to(i: Implementation) -> dict:
    c = {"state": i.conformance.state}
    if i.conformance.version is not None:
        c["version"] = i.conformance.version
    if i.conformance.hash is not None:
        c["hash"] = i.conformance.hash
    out = {"platform": i.platform, "conformance": c}
    if i.location is not None:
        out["location"] = i.location
    return out


def load_index(cookbook_dir: Path) -> Index:
    path = Path(cookbook_dir) / INDEX_FILE
    try:
        return parse_index(path.read_text(encoding="utf-8"), str(path))
    except OSError as e:
        raise IndexFileError(f"{path}: {e!r}") from e


def parse_index(text: str, label: str = INDEX_FILE) -> Index:
    """An index from its JSON text; `label` names it in errors."""
    path = label
    try:
        data = json.loads(text)
        if data.get("format") != INDEX_FORMAT:
            raise IndexFileError(f"{path}: unsupported format {data.get('format')!r}")
        cb = data["cookbook"]
        entries = _entries_from(data.get("entries", {}), path)
        index = Index(cookbook=CookbookIdentity(id=cb["id"].lower(), rdid=cb["rdid"]), entries=entries,
                      foreign=dict(data.get("foreign", {})), catalog=data.get("catalog"))
    except (json.JSONDecodeError, KeyError, TypeError, AttributeError) as e:
        raise IndexFileError(f"{path}: {e!r}") from e
    _check_collisions(entries)
    return index


def save_index(index: Index, cookbook_dir: Path) -> None:
    path = Path(cookbook_dir) / INDEX_FILE
    data: dict = {
        "format": INDEX_FORMAT,
        "cookbook": {"id": index.cookbook.id, "rdid": index.cookbook.rdid},
        "entries": {
            uid: {"kind": e.kind, "rdid": e.rdid, "path": e.path,
                  "implementations": [_impl_to(i) for i in e.implementations]}
            for uid, e in index.entries.items()
        },
        "foreign": dict(index.foreign),
    }
    if index.catalog is not None:
        data["catalog"] = index.catalog
    tmp = path.with_name(path.name + ".tmp")
    try:
        tmp.write_text(json.dumps(data, indent=2, ensure_ascii=False, sort_keys=True) + "\n",
                       encoding="utf-8")
        os.replace(tmp, path)
    finally:
        tmp.unlink(missing_ok=True)  # gone after a replace; a failed write leaves nothing


def _folder_identity(folder: Path) -> Optional[tuple[str, str]]:
    """(uuid, type) from artifact.json meta, read directly so it works on any format."""
    try:
        meta = json.loads((folder / "artifact.json").read_text(encoding="utf-8")).get("meta", {})
    except (OSError, json.JSONDecodeError):
        return None
    uid = meta.get("id")
    return (str(uid).lower(), str(meta.get("type", ""))) if uid else None


def sync_from_folders(index: Index, cookbook_dir: Path) -> list[str]:
    """Bring non-check entries in line with the artifact folders; return change lines."""
    cookbook_dir = Path(cookbook_dir)
    found: dict[str, tuple[str, str]] = {}  # uuid -> (rel path, type)
    for folder in find_folders([cookbook_dir]):
        ident = _folder_identity(folder)
        if ident is None:
            continue
        rel = folder.relative_to(cookbook_dir).as_posix()
        if ident[0] in found:
            raise IndexFileError(
                f"artifact id {ident[0]} is used by two folders: {found[ident[0]][0]} and {rel}")
        found[ident[0]] = (rel, ident[1])

    changes: list[str] = []
    for uid in sorted(set(index.entries) - set(found)):
        if index.entries[uid].kind == "check":
            continue
        changes.append(f"dropped {index.entries[uid].rdid} ({index.entries[uid].path})")
        del index.entries[uid]
    for uid, (rel, type_) in sorted(found.items(), key=lambda kv: kv[1][0]):
        entry = index.entries.get(uid)
        if entry is None:
            first = rel.split("/")[0]
            kind = type_ if type_ in KINDS else TYPE_DIRS.get(first, type_)
            try:
                rdid = artifact_rdid(index.cookbook.rdid, kind, rel)
            except IdentityError as e:
                raise IndexFileError(f"{rel}: cannot derive the artifact's rdid: {e}") from e
            index.entries[uid] = Entry(id=uid, kind=kind, rdid=rdid, path=rel)
            changes.append(f"added {rdid} ({rel})")
        elif entry.path != rel:
            changes.append(f"moved {entry.rdid}: {entry.path} -> {rel}")
            entry.path = rel
    _check_collisions(index.entries)
    return changes


def current_index(cookbook_dir: Path) -> Index:
    """The cookbook's index as its folders stand: `index.json` (or, before cookr
    has written one, an empty index for the manifest's identity) synced in
    memory with the folders. Nothing is written."""
    cookbook_dir = Path(cookbook_dir)
    if (cookbook_dir / INDEX_FILE).is_file():
        index = load_index(cookbook_dir)
    else:
        index = Index(cookbook=read_manifest(cookbook_dir))
    sync_from_folders(index, cookbook_dir)
    return index


def cookbook_dir_of(path: Path) -> Optional[Path]:
    """The cookbook holding `path`: the nearest of it and its parents with a manifest."""
    path = Path(path).resolve()
    return next((d for d in (path, *path.parents) if (d / MANIFEST).is_file()), None)


class IndexCache:
    """Each cookbook's current index (`current_index`), read once, for whatever
    folders a command walks."""

    def __init__(self) -> None:
        self._by_dir: dict[Path, Optional[Index]] = {}

    def for_path(self, path: Path) -> Optional[Index]:
        """The current index of the cookbook holding `path`; None when there is no
        such cookbook or its manifest or index cannot be read."""
        cookbook = cookbook_dir_of(path)
        if cookbook is None:
            return None
        if cookbook not in self._by_dir:
            try:
                self._by_dir[cookbook] = current_index(cookbook)
            except CookbookError:
                self._by_dir[cookbook] = None
        return self._by_dir[cookbook]

    def entry(self, folder: Path, artifact_id: object) -> Optional[Entry]:
        index = self.for_path(folder)
        return index.entries.get(str(artifact_id or "").lower()) if index else None
