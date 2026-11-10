"""YAML frontmatter parse / fill-missing / dump.

A markdown file with frontmatter starts with `---\\n`, contains YAML up to the next
`\\n---\\n`, and continues with the body. We never reorder existing keys; fills append
in a stable order at the end.
"""

from __future__ import annotations

import re
import uuid
from dataclasses import dataclass
from datetime import date
from pathlib import Path

from .deps import require

yaml = require("yaml")


REQUIRED_FIELDS = (
    "id",
    "title",
    "type",
    "version",
    "status",
    "language",
    "created",
    "modified",
    "author",
    "copyright",
    "license",
    "summary",
)

VALID_TYPES = {
    "principle",
    "guideline",
    "ingredient",
    "recipe",
    "cookbook",
    "workflow",
    "reference",
    "compliance",
}

VALID_STATUSES = {"wip", "draft", "review", "accepted", "deprecated"}

SEMVER_RE = re.compile(r"^\d+\.\d+\.\d+(?:-[0-9A-Za-z.-]+)?$")
UUID_RE = re.compile(
    r"^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$",
    re.IGNORECASE,
)


@dataclass
class Frontmatter:
    data: dict
    body: str
    had_frontmatter: bool


def parse(text: str) -> Frontmatter:
    if not text.startswith("---\n"):
        return Frontmatter(data={}, body=text, had_frontmatter=False)
    try:
        end = text.index("\n---\n", 4)
    except ValueError:
        return Frontmatter(data={}, body=text, had_frontmatter=False)
    raw = text[4:end]
    body = text[end + len("\n---\n") :]
    data = yaml.safe_load(raw) or {}
    if not isinstance(data, dict):
        return Frontmatter(data={}, body=text, had_frontmatter=False)
    return Frontmatter(data=data, body=body, had_frontmatter=True)


def parse_file(path: Path) -> Frontmatter:
    return parse(path.read_text(encoding="utf-8"))


def dump(fm: Frontmatter) -> str:
    yaml_text = yaml.safe_dump(fm.data, sort_keys=False, allow_unicode=True).rstrip("\n")
    return f"---\n{yaml_text}\n---\n{fm.body}"


def _h1_title(body: str) -> str | None:
    for line in body.splitlines():
        s = line.strip()
        if s.startswith("# "):
            return s[2:].strip()
    return None


def _infer_type(rel_path: Path) -> str:
    if not rel_path.parts:
        return "reference"
    head = rel_path.parts[0]
    mapping = {
        "principles": "principle",
        "guidelines": "guideline",
        "ingredients": "ingredient",
        "recipes": "recipe",
        "workflows": "workflow",
        "compliance": "compliance",
        "reference": "reference",
    }
    return mapping.get(head, "reference")


def fill_defaults(
    fm: Frontmatter,
    *,
    rel_path: Path,
    author: str = "",
    today: date | None = None,
) -> tuple[Frontmatter, list[str]]:
    """Fill missing required fields. Never overwrites existing values.

    Returns (frontmatter, fields_added).
    """
    today = today or date.today()
    today_s = today.isoformat()
    title = _h1_title(fm.body) or rel_path.stem.replace("-", " ").replace("_", " ").title()
    missing = lambda key: key not in fm.data or fm.data.get(key) in (None, "")  # noqa: E731
    defaults = {
        "id": str(uuid.uuid4()),
        "title": title,
        "type": _infer_type(rel_path),
        "version": "1.0.0",
        "status": "draft",
        "language": "en",
        "created": today_s,
        "modified": today_s,
        "author": author,
        "copyright": f"{today.year} {author}".strip(),
        "license": "MIT",
        "summary": title,
        "platforms": [],
        "tags": [],
        "depends-on": [],
        "related": [],
        "references": [],
    }
    added: list[str] = []
    for key, value in defaults.items():
        if missing(key):
            fm.data[key] = value
            added.append(key)
    if added and "modified" not in added:
        fm.data["modified"] = today_s
        added.append("modified*")
    return fm, added
