"""Build and edit a format-2 cookbook in a test: specs are source folders, the
code they claim is recorded in `index.json`, and roots live in `.cookr.json`."""

from __future__ import annotations

import json
import shutil
import uuid
from pathlib import Path
from typing import Iterable, Optional

from cookr.core.artifact import (
    Artifact, compose_document, load_folder, read_document, split_body, write_folder,
)
from cookr.core.index import (
    Conformance, Entry, Implementation, Index, load_index, save_index, sync_from_folders,
)
from cookr.core.identity import check_rdid, check_uuid, read_manifest
from cookr.core.repoconfig import CONFIG_NAME, load_repo_config

Impl = tuple  # (platform, location[, state])


def cookbook_dir(repo: Path) -> Path:
    return repo / "cookbook"


def config(repo: Path):
    return load_repo_config(repo)


def _index(cb: Path) -> Index:
    return load_index(cb) if (cb / "index.json").is_file() else Index(cookbook=read_manifest(cb))


def implementations(rows: Iterable[Impl]) -> list[Implementation]:
    out = []
    for row in rows:
        platform, location, *rest = row
        out.append(Implementation(platform, location, Conformance(rest[0] if rest else "unverified")))
    return out


def set_implementations(repo: Path, rel: str, rows: Iterable[Impl]) -> None:
    """Record `rows` as the implementations of the spec at cookbook/<rel>."""
    cb = cookbook_dir(repo)
    index = _index(cb)
    sync_from_folders(index, cb)
    entry = index.by_path(rel)
    assert entry is not None, rel
    entry.implementations = implementations(rows)
    save_index(index, cb)


def add_spec(repo: Path, rel: str, *, type: str = "ingredient", status: str = "draft",
             body: str = "# Spec\n\nText.\n", impls: Iterable[Impl] = (),
             meta: Optional[dict] = None, artifact_id: Optional[str] = None) -> str:
    """A format-2 folder at cookbook/<rel>, indexed with `impls`; returns its id."""
    uid = artifact_id or str(uuid.uuid4())
    m = {"id": uid, "type": type, "status": status}
    m.update(meta or {})
    write_folder(Artifact(meta=m, parts=split_body(body)), cookbook_dir(repo) / rel)
    set_implementations(repo, rel, impls)
    return uid


def add_doc(repo: Path, rel: str, body: str, *, type: str = "recipe", **meta) -> Path:
    """A complete format-2 source folder at cookbook/<rel> with its compiled
    `<rel>.md` beside it, as a cookbook that has already been converted holds it.
    `body` is the document body; the cookbook's indexes are refreshed (`update`).
    Returns the folder."""
    from cookr.cli import main
    m = {"title": rel.rsplit("/", 1)[-1].replace("-", " ").title(), "version": "1.0.0",
         "language": "en", "created": "2026-05-15", "modified": "2026-05-15", "author": "Tester",
         "copyright": "2026 Tester", "license": "MIT", "summary": "A test artifact."}
    m.update(meta)
    add_spec(repo, rel, type=type, body=body, meta=m)
    folder = cookbook_dir(repo) / rel
    assert main(["compile", str(folder)]) == 0
    assert main(["update", "-p", str(cookbook_dir(repo)), "--author", "Tester"]) == 0
    return folder


def remove_spec(repo: Path, rel: str) -> None:
    shutil.rmtree(cookbook_dir(repo) / rel)


def add_root(repo: Path, path: str, platform: str, group: str, files: Iterable[str] = (),
             **extra) -> None:
    d = repo / path
    d.mkdir(parents=True, exist_ok=True)
    for f in files:
        (d / f).write_text("export {}\n", encoding="utf-8")
    p = repo / CONFIG_NAME
    data = json.loads(p.read_text(encoding="utf-8"))
    data["roots"].append({"path": path, "platform": platform, "group": group, **extra})
    p.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")


def new_repo(repo: Path, roots: Iterable[dict] = (), *, rdid: str = "test-repo",
             cookbook_id: str = "c0000000-0000-4000-8000-000000000000") -> Path:
    """An empty format-2 repo at `repo`: `cookbook/cookbook.json` and a
    `.cookr.json` with `roots` (each root's directory is created)."""
    cb = cookbook_dir(repo)
    cb.mkdir(parents=True, exist_ok=True)
    (cb / "cookbook.json").write_text(
        json.dumps({"format": 2, "id": cookbook_id, "rdid": rdid}), encoding="utf-8")
    roots = list(roots)
    for r in roots:
        (repo / r["path"]).mkdir(parents=True, exist_ok=True)
    (repo / CONFIG_NAME).write_text(
        json.dumps({"format": 2, "cookbook": "cookbook", "roots": roots}), encoding="utf-8")
    if not (cb / "index.json").is_file():
        save_index(Index(cookbook=read_manifest(cb)), cb)  # a format-2 cookbook has an index
    return repo


ADC_ID = "e7a40000-0000-4000-8000-000000000000"  # mini-repo's declared dependency


def add_dependency(repo: Path, rel: str, *, cookbook_id: str = ADC_ID, rdid: str = "adc",
                   checks: Iterable[tuple[str, str]] = ()) -> Path:
    """A reachable dependency cookbook at `<repo>/<rel>` (cookbook.json plus an
    index of `checks`, each `(document, name)`), declared in `.cookr.json` with
    that location. Returns the dependency's cookbook dir."""
    cb = repo / rel
    cb.mkdir(parents=True, exist_ok=True)
    (cb / "cookbook.json").write_text(
        json.dumps({"format": 2, "id": cookbook_id, "rdid": rdid}), encoding="utf-8")
    index = Index(cookbook=read_manifest(cb), catalog="compliance")
    for document, name in checks:
        uid = check_uuid(cookbook_id, document, name)
        index.entries[uid] = Entry(id=uid, kind="check", rdid=check_rdid(rdid, document, name),
                                   path=f"{document}#{name}")
    save_index(index, cb)
    edit_repo_config(repo, lambda data: data.setdefault("dependencies", {}).__setitem__(
        cookbook_id, {"rdid": rdid, "location": rel}))
    return cb


def edit_repo_config(repo: Path, edit) -> None:
    p = repo / CONFIG_NAME
    data = json.loads(p.read_text(encoding="utf-8"))
    edit(data)
    p.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")


class SpecDoc:
    """The spec folder at cookbook/<rel> read and written as one document, so a
    test can edit its frontmatter and sections as text."""

    def __init__(self, repo: Path, rel: str):
        self.folder = cookbook_dir(repo) / rel

    def read_text(self, encoding: str = "utf-8") -> str:
        return compose_document(load_folder(self.folder))

    def write_text(self, text: str, encoding: str = "utf-8") -> None:
        write_folder(read_document(text), self.folder)
