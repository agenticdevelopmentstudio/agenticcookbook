"""Convert single-file artifacts into source folders, and compile folders into targets.

`convert` is the one-way migration (doc → folder); `compile_doc` builds the
`doc` target (folder → doc). Both verify before they write: a convert whose
folder would not compose back to the normalized source is refused, so a
conversion can never lose content.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

from .artifact import (
    BOTH_EDITED,
    CURRENT,
    DOC_EDITED,
    FOLDER_EDITED,
    RECONCILE,
    ArtifactError,
    compose_document,
    doc_path,
    folder_for,
    is_folder,
    load_folder,
    normalize_document,
    occupied,
    doc_digest,
    read_document,
    record_sync,
    save_document,
    sync_state,
    unconverted,
    write_folder,
)
from .artifact_types import validate

TARGETS = ("doc", "skill")


@dataclass
class Result:
    source: Path
    dest: Path
    status: str  # converted | skipped | updated | compiled | unchanged | stale | missing | would-write | error | broken | unconverted
    detail: str = ""
    problems: list[str] = field(default_factory=list)  # type-shape problems; reported, not fatal

    @property
    def failed(self) -> bool:
        return self.status in ("error", "stale", "missing", "broken", "unconverted")

    def as_json(self) -> dict:
        return {"source": str(self.source), "dest": str(self.dest), "status": self.status,
                "detail": self.detail, "problems": self.problems}


def _dest(path: Path, base: Path, out: Optional[Path], local: Path) -> Path:
    """`local` (the in-place destination), or its mirror under `out`."""
    if out is None:
        return local
    try:
        rel = local.resolve().relative_to(base.resolve())
    except ValueError as e:
        raise ArtifactError(f"{path} is outside {base}; --out mirrors paths below it") from e
    return out / rel


def convert(docs: list[Path], *, base: Path, out: Optional[Path] = None, write: bool = True,
            remove_source: bool = False, update: bool = False, force: bool = False) -> list[Result]:
    """Convert each doc into its folder. An artifact that already has a folder
    is skipped, since the folder is the source and the doc its output, unless
    `update`: then edits made to the doc are folded into the folder
    (`save_document`), keeping the folder's other files. A folder edited since
    cookr wrote the doc is not overwritten unless `force`."""
    results = []
    for doc in docs:
        try:
            dest = _dest(doc, base, out, folder_for(doc))
            if is_folder(dest) and not update:
                results.append(Result(doc, dest, "skipped", "already a source folder"))
                continue
            text = doc.read_text(encoding="utf-8")
            artifact = read_document(text)
            if compose_document(artifact) != normalize_document(text):
                raise ArtifactError("the folder would not compose back to the source")
            if not is_folder(dest):
                problem = occupied(artifact, dest)
                if problem:
                    raise ArtifactError(f"{problem}; rename the section or the file")
            problems = validate(artifact)
            if not write:
                results.append(Result(doc, dest, "would-write", problems=problems))
                continue
            if is_folder(dest):
                state = sync_state(dest)
                if state in (FOLDER_EDITED, BOTH_EDITED) and not force:
                    raise ArtifactError(RECONCILE[state])
                before = compose_document(load_folder(dest))
                save_document(doc, text)
                status = "unchanged" if compose_document(load_folder(dest)) == before else "updated"
                results.append(Result(doc, dest, status, problems=problems))
                continue
            artifact.synced = doc_digest(compose_document(artifact))
            write_folder(artifact, dest)
            compiled = compose_document(load_folder(dest))
            if compiled != normalize_document(text):
                raise ArtifactError(f"{dest} does not compose back to the source")
            if remove_source:
                doc.unlink()
            elif out is None and compiled != text:
                doc.write_text(compiled, encoding="utf-8")  # the doc is now the folder's output
            results.append(Result(doc, dest, "converted", problems=problems))
        except (ArtifactError, OSError, UnicodeDecodeError) as e:
            results.append(Result(doc, doc, "error", str(e)))
    return results


UNCONVERTED = "has no source folder, so nothing compiles or checks it; run `cookr convert` on it"


def unconverted_results(paths: list[Path]) -> list[Result]:
    """A failed result for each artifact doc under `paths` with no source folder."""
    return [Result(doc, folder_for(doc), "unconverted", UNCONVERTED) for doc in unconverted(paths)]


def compile_doc(folders: list[Path], *, base: Path, out: Optional[Path] = None,
                write: bool = True, force: bool = False) -> list[Result]:
    """Write each folder's `doc`, or with write=False report whether it is current.
    A doc edited since cookr wrote it is not overwritten unless `force`."""
    results = []
    for folder in folders:
        try:
            dest = _dest(folder, base, out, doc_path(folder))
            artifact = load_folder(folder)
            text = compose_document(artifact)
            problems = validate(artifact)
            current = dest.read_text(encoding="utf-8") if dest.is_file() else None
            state = sync_state(folder) if out is None else None
            detail = RECONCILE.get(state, "")
            if current == text:
                status = "unchanged"
            elif not write:
                status = "missing" if current is None else "stale"
            elif state in (DOC_EDITED, BOTH_EDITED) and not force:
                raise ArtifactError(f"{dest}: {detail}")
            else:
                dest.parent.mkdir(parents=True, exist_ok=True)
                dest.write_text(text, encoding="utf-8")
                status, detail = "compiled", ""
            if write and out is None:
                record_sync(folder, text)
            results.append(Result(folder, dest, status, detail if status == "stale" else "",
                                  problems=problems))
        except (ArtifactError, OSError, UnicodeDecodeError) as e:
            results.append(Result(folder, folder, "error", str(e)))
    return results
