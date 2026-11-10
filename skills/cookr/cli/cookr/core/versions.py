"""In-source versions: requirement-level diffs and the `versions/` freeze.

A source folder is the current version. When `cookr bump` raises the version, the
previous one is frozen byte for byte into `<folder>/versions/<X.Y.Z>/` (its
`artifact.json` and part files), so `cookr diff` can compare two versions without
git. Semver means something here: a `patch` is wording only, a `minor` adds a
named requirement, a `major` changes or removes one.

The git helpers read the version a branch started from (its merge base with main)
so a bump is computed from there, whatever the branch has done since. They call
git with argument lists and `cwd=repo_root`, never through a shell.
"""

from __future__ import annotations

import json
import re
import subprocess
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

from .artifact import (
    ARTIFACT_FILE, HISTORY, Artifact, ArtifactError, Part, authored_text, compose_document,
    parse_frontmatter, read_document,
)
from .errors import CookbookError
from .history import parse_version, split_lines, unfenced
from .markdown import VERSIONS_DIR

# `**name**: text`, or `**name** (variant): text` — a variant tag is part of the requirement's text.
_REQUIREMENT = re.compile(
    r"^\s*[-*]?\s*\*\*([a-z0-9][a-z0-9-]*)\*\*(?:\s*(\([^()\n]*\))\s*)?:\s*(.+)$")
_UNVERSIONED = ("version", "modified")


class FreezeError(CookbookError):
    """A version cannot be frozen: its directory already holds other bytes."""


# ── requirements ─────────────────────────────────────────────────────────────

def requirements(text: str) -> dict[str, str]:
    """Every named requirement outside code fences, name -> its text with
    whitespace collapsed. A name that repeats keeps its last text."""
    found: dict[str, str] = {}
    for _, bare in unfenced(split_lines(text)):
        m = _REQUIREMENT.match(bare) if bare is not None else None
        if m:
            tag, rest = m.group(2), m.group(3)
            found[m.group(1)] = " ".join(f"{tag} {rest}".split() if tag else rest.split())
    return found


@dataclass
class RequirementDiff:
    added: list[str] = field(default_factory=list)
    changed: list[str] = field(default_factory=list)
    removed: list[str] = field(default_factory=list)

    def __bool__(self) -> bool:
        return bool(self.added or self.changed or self.removed)


def diff(old: str, new: str) -> RequirementDiff:
    """How the requirements of doc text `new` differ from those of `old`."""
    a, b = requirements(old), requirements(new)
    return RequirementDiff(
        added=[n for n in b if n not in a],
        changed=[n for n in b if n in a and a[n] != b[n]],
        removed=[n for n in a if n not in b],
    )


def propose_level(d: RequirementDiff, content_changed: bool) -> str:
    """The semver level a change warrants: `major` when a requirement changed or
    went, `minor` when one was added, `patch` when only other content changed,
    `none` when nothing did."""
    if d.changed or d.removed:
        return "major"
    if d.added:
        return "minor"
    return "patch" if content_changed else "none"


def authored_view(text: str) -> tuple[dict, list[tuple[str, str]]]:
    """What a bump compares: the doc's metadata without version/modified, and its
    parts without Change History or derived sections."""
    artifact = read_document(authored_text(text))
    meta = {k: v for k, v in artifact.meta.items() if k not in _UNVERSIONED}
    return meta, [(p.name, p.text) for p in artifact.parts if p.name != HISTORY]


def content_changed(old: str, new: str) -> bool:
    return authored_view(old) != authored_view(new)


def version_of(text: str) -> str:
    """The `version` in a doc's frontmatter; "" when it has none."""
    m = re.match(r"\A---\n(.*?)\n?---\n", text, re.S)
    meta = parse_frontmatter(m.group(1)) if m else {}
    return str(meta.get("version", "") or "")


# ── files and composing ──────────────────────────────────────────────────────

def compose_files(files: dict[str, bytes]) -> str:
    """The doc a folder's `files` (as `base_files`/`folder_files` return them) compose to."""
    try:
        data = json.loads(files[ARTIFACT_FILE].decode("utf-8"))
        parts = [Part(name=e["part"], text=files[f"{e['part']}.md"].decode("utf-8"),
                      heading=e.get("heading")) for e in data.get("parts", [])]
        return compose_document(Artifact(meta=dict(data.get("meta", {})), parts=parts))
    except (KeyError, ValueError, TypeError, AttributeError) as e:
        raise ArtifactError(f"cannot compose a version from its files: {e!r}") from e


def folder_files(folder: Path) -> Optional[dict[str, bytes]]:
    """A source folder's `artifact.json` and listed parts, as bytes; None when unreadable."""
    try:
        manifest = (folder / ARTIFACT_FILE).read_bytes()
        files = {ARTIFACT_FILE: manifest}
        for e in json.loads(manifest.decode("utf-8")).get("parts", []):
            files[f"{e['part']}.md"] = (folder / f"{e['part']}.md").read_bytes()
        return files
    except (OSError, ValueError, KeyError, TypeError, AttributeError):
        return None


# ── git ──────────────────────────────────────────────────────────────────────

class GitError(CookbookError):
    """git itself failed (missing, not a repo, corrupt): not the same as 'nothing there'."""


def _run(root: Path, *args: str) -> tuple[int, bytes, str]:
    """(exit code, stdout, stderr) of `git args` in `root`; GitError when git cannot run."""
    try:
        proc = subprocess.run(["git", *args], cwd=root, capture_output=True, check=False)
    except OSError as e:
        raise GitError(f"cannot run git: {e}") from e
    return proc.returncode, proc.stdout, proc.stderr.decode("utf-8", "replace").strip()


def git(root: Path, *args: str) -> bytes:
    """stdout of `git args`; GitError (with git's message) on any failure."""
    code, out, err = _run(root, *args)
    if code != 0:
        raise GitError(f"git {' '.join(args[:2])} failed ({code}): {err or 'no message'}")
    return out


def repo_root(path: Path) -> Path:
    """The git work tree holding `path` (a directory), resolved. GitError outside one."""
    out = git(path, "rev-parse", "--show-toplevel").decode("utf-8").strip()
    if not out:
        raise GitError(f"git rev-parse --show-toplevel printed nothing in {path}")
    return Path(out).resolve()


def base_ref(repo_root: Path) -> str:
    """The commit the branch started from: its merge base with `origin/main`, else
    with `main`. "" when neither branch exists (no base branch); GitError when git
    fails for any other reason."""
    for target in ("origin/main", "main"):
        code, _, err = _run(repo_root, "rev-parse", "--verify", "--quiet", f"{target}^{{commit}}")
        if code == 1 and not err:
            continue                       # no such branch
        if code != 0:
            raise GitError(f"git rev-parse {target} failed ({code}): {err or 'no message'}")
        code, out, err = _run(repo_root, "merge-base", "HEAD", target)
        if code == 1 and not err:
            continue                       # no common ancestor
        if code != 0:
            raise GitError(f"git merge-base HEAD {target} failed ({code}): {err or 'no message'}")
        return out.decode("utf-8").strip()
    return ""


def _show(root: Path, ref: str, path: str) -> Optional[bytes]:
    """The bytes of `path` at `ref`; None when the ref has no such path; GitError when git fails."""
    if not git(root, "ls-tree", "--name-only", ref, "--", path).strip():
        return None
    return git(root, "show", f"{ref}:{path}")


def file_at(root: Path, ref: str, path: str) -> Optional[bytes]:
    """The bytes of `path` at `ref`; None when the ref has no such path or no `ref`
    exists yet (an unborn HEAD); GitError when git fails."""
    if not ref:
        return None
    return _show(root, ref, path)


def has_commit(root: Path, ref: str) -> bool:
    return _run(root, "rev-parse", "--verify", "--quiet", f"{ref}^{{commit}}")[0] == 0


def _rel(repo_root: Path, path: Path) -> Optional[str]:
    try:
        return path.resolve().relative_to(Path(repo_root).resolve()).as_posix()
    except ValueError:
        return None


def base_files(repo_root: Path, folder: Path, ref: str) -> Optional[dict[str, bytes]]:
    """The folder's `artifact.json` and parts as of `ref`; None when it had none."""
    rel = _rel(repo_root, folder)
    if rel is None or not ref:
        return None
    manifest = _show(repo_root, ref, f"{rel}/{ARTIFACT_FILE}")
    if manifest is None:
        return None
    files = {ARTIFACT_FILE: manifest}
    try:
        for e in json.loads(manifest.decode("utf-8")).get("parts", []):
            part = _show(repo_root, ref, f"{rel}/{e['part']}.md")
            if part is None:
                raise ArtifactError(f"the base's {rel}/{e['part']}.md is listed but missing")
            files[f"{e['part']}.md"] = part
    except (ValueError, KeyError, TypeError, AttributeError) as e:
        raise ArtifactError(f"the base's {rel}/{ARTIFACT_FILE} is unreadable: {e!r}") from e
    return files


def base_text(repo_root: Path, folder: Path, ref: str) -> Optional[str]:
    """The artifact's composed doc as of `ref` (from its folder there, else from
    a single-file doc beside it); None when it did not exist."""
    files = base_files(repo_root, folder, ref)
    if files is not None:
        return compose_files(files)
    rel = _rel(repo_root, folder)
    if rel is None or not ref:
        return None
    doc = _show(repo_root, ref, f"{rel}.md")
    return doc.decode("utf-8") if doc is not None else None


# ── versions/ ────────────────────────────────────────────────────────────────

def _frozen(dest: Path) -> dict[str, bytes]:
    return {p.relative_to(dest).as_posix(): p.read_bytes()
            for p in sorted(dest.rglob("*")) if p.is_file()}


def conflict(folder: Path, version: str, files: dict[str, bytes]) -> Optional[str]:
    """Why `files` cannot be frozen as `version`, or None (free, or already frozen identically)."""
    if parse_version(version) is None:
        return f"{version!r} is not X.Y.Z"
    dest = folder / VERSIONS_DIR / version
    if dest.exists() and (not dest.is_dir() or _frozen(dest) != files):
        return f"{dest} already exists with different contents"
    return None


def freeze(folder: Path, version: str, files: dict[str, bytes]) -> Path:
    """Write `files` to `folder/versions/<version>/`. Freezing the same bytes
    again changes nothing; a directory holding other bytes is refused."""
    problem = conflict(folder, version, files)
    if problem:
        raise FreezeError(problem)
    dest = folder / VERSIONS_DIR / version
    if not dest.is_dir():
        dest.mkdir(parents=True)
        for name, data in files.items():
            (dest / name).write_bytes(data)
    return dest


def frozen_versions(folder: Path) -> list[str]:
    """Versions kept in `folder/versions/`, oldest first."""
    d = folder / VERSIONS_DIR
    names = [p.name for p in d.iterdir() if p.is_dir() and parse_version(p.name)] if d.is_dir() else []
    return sorted(names, key=lambda n: parse_version(n))


def version_text(folder: Path, version: str) -> Optional[str]:
    """The doc text of `version`: the working copy when it is the current one,
    else the frozen copy; None when the folder has neither."""
    files = folder_files(folder)
    if files is not None:
        text = compose_files(files)
        if version_of(text) == version:
            return text
    if parse_version(version) is not None and (folder / VERSIONS_DIR / version).is_dir():
        frozen = folder_files(folder / VERSIONS_DIR / version)
        if frozen is not None:
            return compose_files(frozen)
    return None
