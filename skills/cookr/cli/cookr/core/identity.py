"""Identity: the UUID is the identity, the rdid is a readable name.

An rdid is dotted lowercase segments (`adhsdk.recipe.ui.web-panel`); its first
segment is the cookbook's rdid. A cookbook holds the pair in `cookbook.json`.
Compliance checks get deterministic identity from their cookbook and name.
"""

from __future__ import annotations

import json
import os
import re
import uuid
from dataclasses import dataclass
from pathlib import Path

from .errors import CookbookError

MANIFEST = "cookbook.json"
MANIFEST_FORMAT = 2
RDID_RE = re.compile(r"^[a-z][a-z0-9-]*(\.[a-z0-9][a-z0-9-]*)+$")
COOKBOOK_RDID_RE = re.compile(r"^[a-z][a-z0-9-]*$")
TYPE_DIRS = {"principles": "principle", "guidelines": "guideline",
             "ingredients": "ingredient", "recipes": "recipe"}


class IdentityError(CookbookError):
    """A malformed identity or cookbook manifest."""


def is_rdid(s: str) -> bool:
    return isinstance(s, str) and RDID_RE.match(s) is not None


def is_cookbook_rdid(s: str) -> bool:
    return isinstance(s, str) and COOKBOOK_RDID_RE.match(s) is not None


def is_uuid(s: str) -> bool:
    if not isinstance(s, str):
        return False
    try:
        return str(uuid.UUID(s)) == s.lower()
    except ValueError:
        return False


def _dotted(path: str) -> str:
    return ".".join(p for p in path.strip("/").split("/") if p)


def _valid(rdid: str) -> str:
    if not is_rdid(rdid):
        raise IdentityError(f"{rdid!r} is not a valid rdid")
    return rdid


def artifact_rdid(cookbook_rdid: str, type_: str, rel: str) -> str:
    """`rel` is the folder path below the cookbook; a leading type dir is stripped."""
    parts = [p for p in rel.strip("/").split("/") if p]
    if parts and parts[0] in TYPE_DIRS:
        parts = parts[1:]
    return _valid(".".join([cookbook_rdid, type_, *parts]))


def check_rdid(cookbook_rdid: str, document: str, name: str) -> str:
    return _valid(f"{cookbook_rdid}.check.{_dotted(document)}.{name}")


def check_uuid(cookbook_id: str, document: str, name: str) -> str:
    return str(uuid.uuid5(uuid.UUID(cookbook_id), f"check:{document}#{name}"))


@dataclass(frozen=True)
class CookbookIdentity:
    id: str
    rdid: str


def read_manifest(cookbook_dir: Path) -> CookbookIdentity:
    path = Path(cookbook_dir) / MANIFEST
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as e:
        raise IdentityError(f"{path}: {e}") from e
    if not isinstance(data, dict) or data.get("format") != MANIFEST_FORMAT:
        raise IdentityError(f"{path}: not a format {MANIFEST_FORMAT} cookbook manifest")
    cid, rdid = data.get("id"), data.get("rdid")
    if not is_uuid(cid):
        raise IdentityError(f"{path}: id {cid!r} is not a UUID")
    if not is_cookbook_rdid(rdid):
        raise IdentityError(f"{path}: rdid {rdid!r} is not a valid rdid")
    return CookbookIdentity(id=cid.lower(), rdid=rdid)


def write_manifest(cookbook_dir: Path, identity: CookbookIdentity,
                   extra: dict | None = None) -> None:
    """Write cookbook.json, keeping the other keys already there (and `extra`)."""
    path = Path(cookbook_dir) / MANIFEST
    data: dict = {}
    if path.is_file():
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as e:
            raise IdentityError(f"{path}: {e}") from e
    if not is_uuid(identity.id) or not is_cookbook_rdid(identity.rdid):
        raise IdentityError(f"{path}: invalid cookbook identity {identity!r}")
    data.update(extra or {})
    data.update({"format": MANIFEST_FORMAT, "id": identity.id.lower(), "rdid": identity.rdid})
    tmp = path.with_name(path.name + ".tmp")
    tmp.write_text(json.dumps(data, indent=2, ensure_ascii=False, sort_keys=True) + "\n",
                   encoding="utf-8")
    os.replace(tmp, path)
