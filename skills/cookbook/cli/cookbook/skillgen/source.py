"""Load a cookbook-schema tree: its layout, and every doc with frontmatter.

Two layouts are recognised:

- `cookbook` — the agenticcookbook tree (`guidelines/<use-case>/<domain>/…`,
  `principles/`, `recipes/<category>/…`, …).
- `recipes` — a repo with a `.cookr.json` naming a flat recipes dir, a URI
  scheme, and the code roots the recipes describe (agentictoolkit).
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, field
from pathlib import Path

from ..core import frontmatter
from ..core.markdown import iter_markdown

COOKR_CONFIG = ".cookr.json"
COOKBOOK_MARKERS = ("guidelines", "principles")


@dataclass(frozen=True)
class Source:
    root: Path
    name: str
    layout: str
    code_roots: tuple = ()


@dataclass
class Doc:
    rel: Path
    data: dict
    body: str
    source_hash: str

    def _list(self, key: str) -> list[str]:
        value = self.data.get(key) or []
        if isinstance(value, str):
            value = [value]
        return sorted({str(v).strip() for v in value if str(v).strip()})

    @property
    def title(self) -> str:
        return str(self.data.get("title") or self.rel.stem.replace("-", " ").title())

    @property
    def summary(self) -> str:
        return " ".join(str(self.data.get("summary") or "").split())

    @property
    def type(self) -> str:
        return str(self.data.get("type") or "")

    @property
    def domain(self) -> str:
        return str(self.data.get("domain") or "")

    @property
    def platforms(self) -> list[str]:
        return self._list("platforms")

    @property
    def triggers(self) -> list[str]:
        return self._list("triggers")

    @property
    def tags(self) -> list[str]:
        return self._list("tags")

    @property
    def globs(self) -> list[str]:
        return self._list("globs")

    @property
    def files(self) -> list[str]:
        """Repo files the doc describes: `references:` entries that are paths.

        agentictoolkit writes them as `path/to/file.ts (agentictoolkit)`; URLs
        and cookbook URIs are citations, not files, and are left out.
        """
        out = set()
        for ref in self._list("references"):
            if "://" in ref:
                continue
            out.add(ref.split(" (", 1)[0].strip())
        return sorted(out)


@dataclass
class Loaded:
    source: Source
    docs: list[Doc] = field(default_factory=list)
    skipped: list[tuple[str, str]] = field(default_factory=list)


def resolve(path: Path, name: str | None = None) -> Source | None:
    """Work out what `path` is. None when it is neither layout."""
    path = path.resolve()
    config = path / COOKR_CONFIG
    if config.is_file():
        cfg = json.loads(config.read_text(encoding="utf-8"))
        return Source(
            root=path / cfg.get("recipes", "recipes"),
            name=name or cfg.get("scheme") or path.name,
            layout="recipes",
            code_roots=tuple(cfg.get("roots") or ()),
        )
    for candidate in (path, path / "cookbook"):
        if any((candidate / m).is_dir() for m in COOKBOOK_MARKERS):
            return Source(root=candidate, name=name or "cookbook", layout="cookbook")
    return None


def load(source: Source) -> Loaded:
    loaded = Loaded(source=source)
    for path in iter_markdown(source.root):
        rel = path.relative_to(source.root)
        raw = path.read_bytes()
        fm = frontmatter.parse(raw.decode("utf-8"))
        if not fm.had_frontmatter:
            loaded.skipped.append((rel.as_posix(), "no frontmatter"))
            continue
        loaded.docs.append(
            Doc(
                rel=rel,
                data=fm.data,
                body=fm.body,
                source_hash=hashlib.sha256(raw).hexdigest()[:16],
            )
        )
    return loaded
