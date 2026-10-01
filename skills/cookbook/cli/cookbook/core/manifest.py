"""Materialize a `reference-manifest.json`: copy content-repo files into a package.

A manifest names a `destination` and a `source_root` (both relative to the repo
root) and a list of `files`, each `{"src", "dst", "type": "file"|"tree"}`; a
tree copies every file under `src` matching its `include` glob (default `*`).
An optional `embedded_dir`, relative to the manifest, is overlaid last.

This is the one materializer: install.sh runs it for the cookbook package's
manifest and every prompt module's, and tests run it to build the same tree.
Standard library only, since install.sh runs it before installing any deps.
"""

from __future__ import annotations

import json
import shutil
import sys
from pathlib import Path
from typing import Callable, Optional

from .errors import CookbookError


class ManifestError(CookbookError):
    """A manifest names a missing source, escapes its root, or has an unknown entry type."""


def wipe(directory: Path) -> None:
    """Empty `directory` except its `.gitkeep`, creating it if absent."""
    if not directory.exists():
        directory.mkdir(parents=True)
        return
    for child in directory.iterdir():
        if child.name == ".gitkeep":
            continue
        if child.is_dir():
            shutil.rmtree(child)
        else:
            child.unlink()


def _copy_tree(src: Path, dst: Path, include: str) -> None:
    dst.mkdir(parents=True, exist_ok=True)
    for f in src.rglob(include):
        if f.is_file():
            target = dst / f.relative_to(src)
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(f, target)


def materialize(manifest_path: Path, repo_root: Path, dest: Optional[Path] = None,
                log: Callable[[str], None] = lambda _line: None) -> Path:
    """Materialize `manifest_path` and return the destination it filled.

    `dest` overrides the manifest's `destination` (tests build into a temp
    dir); otherwise the destination must lie inside `repo_root`. The
    destination is emptied first, except its `.gitkeep`. Raises ManifestError.
    """
    manifest_path = manifest_path.resolve()
    repo_root = repo_root.resolve()
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    source_root = (repo_root / manifest["source_root"]).resolve()
    if dest is None:
        dest = (repo_root / manifest["destination"]).resolve()
        if not dest.is_relative_to(repo_root):
            raise ManifestError(f"manifest destination escapes repo root: {dest}")
    else:
        dest = dest.resolve()
    wipe(dest)

    for entry in manifest.get("files", []):
        src = (source_root / entry["src"]).resolve()
        dst = (dest / entry["dst"]).resolve()
        if not src.is_relative_to(source_root):
            raise ManifestError(f"manifest src escapes source_root: {entry['src']}")
        if not dst.is_relative_to(dest):
            raise ManifestError(f"manifest dst escapes destination: {entry['dst']}")
        kind = entry["type"]
        if kind == "file":
            if not src.is_file():
                raise ManifestError(f"MISSING file: {src}")
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, dst)
            log(f"+ {entry['dst']}")
        elif kind == "tree":
            if not src.is_dir():
                raise ManifestError(f"MISSING dir: {src}")
            _copy_tree(src, dst, entry.get("include", "*"))
            log(f"+ {entry['dst']}/ (tree)")
        else:
            raise ManifestError(f"unknown entry type: {kind}")

    embedded = manifest.get("embedded_dir")
    if embedded and (manifest_path.parent / embedded).is_dir():
        _copy_tree(manifest_path.parent / embedded, dest, "*")
        log(f"+ (overlay) {embedded}")
    return dest


def prompt_manifests(repo_root: Path, skills: list[str]) -> tuple[list[Path], list[Path]]:
    """Every prompt module's (references dirs, manifests) across `skills`' packages."""
    roots = [repo_root / "skills" / s / "cli" / s / "modules" / "prompt" / "prompts" for s in skills]
    roots = [r for r in roots if r.is_dir()]
    refs = [d for r in roots for d in sorted(r.glob("*/references")) if d.is_dir()]
    manifests = [m for r in roots for m in sorted(r.glob("*/reference-manifest.json"))]
    return refs, manifests


def main(argv: list[str]) -> int:
    """`manifest.py <repo_root> <manifest>` — or `<repo_root> --prompts <skill>...`,
    which empties every prompt module's references dir and materializes each
    prompt module's manifest."""
    repo_root = Path(argv[0]).resolve()
    say = lambda line: print(f"  {line}")  # noqa: E731
    try:
        if argv[1] == "--prompts":
            refs, manifests = prompt_manifests(repo_root, argv[2:])
            for d in refs:
                wipe(d)
            for m in manifests:
                materialize(m, repo_root)
                say(f"+ {m.relative_to(repo_root)}")
            say(f"materialized {len(manifests)} prompt-module manifest(s)")
        else:
            materialize(Path(argv[1]), repo_root, log=say)
    except ManifestError as e:
        print(f"  {e}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
