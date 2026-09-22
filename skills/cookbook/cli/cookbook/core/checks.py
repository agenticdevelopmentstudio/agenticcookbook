"""Shared deterministic checks used by `lint` Phase A and `validate`."""

from __future__ import annotations

import re
from collections import defaultdict
from dataclasses import dataclass, field
from pathlib import Path

from .frontmatter import (
    REQUIRED_FIELDS,
    SEMVER_RE,
    UUID_RE,
    VALID_STATUSES,
    VALID_TYPES,
    parse_file,
)
from .markdown import iter_markdown


# Per-rule fix-it hints. Keyed on the `rule` slug emitted by `_check_one` /
# `phase_a` below. `required-field:<name>` is matched by prefix.
_FIX_ITS: dict[str, str] = {
    "frontmatter-present": (
        "Add a YAML frontmatter block (between `---` lines) at the top of the file. "
        "Run `cookbook update` to scaffold a minimal one."
    ),
    "id-uuid": "Replace `id` with a UUID4: `python -c 'import uuid; print(uuid.uuid4())'`.",
    "id-unique": "Two artifacts share the same `id`. Regenerate one with `python -c 'import uuid; print(uuid.uuid4())'`.",
    "version-semver": "Use a semver string for `version` (e.g. `1.0.0`).",
    "type-valid": f"`type` must be one of: {', '.join(sorted(VALID_TYPES))}.",
    "status-valid": f"`status` must be one of: {', '.join(sorted(VALID_STATUSES))}.",
    "domain-matches-path": (
        "Update `domain` so it ends with the file's path (without `.md`). "
        "Example: `agenticdevelopercookbook://recipes/auth-cookie`."
    ),
    "link-resolves": "Fix or remove the link target, or create the file it points to.",
}


def fix_for(rule: str) -> str:
    """Return a one-line fix-it hint for a rule slug, or '' if none applies."""
    if rule in _FIX_ITS:
        return _FIX_ITS[rule]
    if rule.startswith("required-field:"):
        field_name = rule.split(":", 1)[1]
        return (
            f"Add the missing `{field_name}` field. "
            f"`cookbook update` will fill required fields with sensible defaults."
        )
    return ""


@dataclass
class CheckIssue:
    file: str
    rule: str
    detail: str


@dataclass
class CheckReport:
    files_checked: int = 0
    issues: list[CheckIssue] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return not self.issues

    def add(self, file: Path | str, rule: str, detail: str) -> None:
        self.issues.append(CheckIssue(file=str(file), rule=rule, detail=detail))


_MD_LINK_RE = re.compile(r"\[[^\]]*\]\(([^)]+)\)")
# An absolute URI: `https://…`, `mailto:…`, or a domain identifier such as
# `agenticdevelopercookbook://…` or `<other-repo>://…` (conventions.md,
# "URL-Based Domain Identifiers"). None of these name a file to resolve.
_URI_RE = re.compile(r"^[a-z][a-z0-9+.-]*:")


def _check_one(md: Path, root: Path, report: CheckReport, id_owners: dict[str, list[str]]) -> None:
    rel = md.relative_to(root)
    fm = parse_file(md)

    if not fm.had_frontmatter:
        report.add(rel, "frontmatter-present", "no YAML frontmatter block found")
        return

    for f in REQUIRED_FIELDS:
        if f not in fm.data or fm.data.get(f) in (None, ""):
            report.add(rel, f"required-field:{f}", f"missing or empty `{f}`")

    if isinstance(fm.data.get("id"), str) and not UUID_RE.match(fm.data["id"]):
        report.add(rel, "id-uuid", f"`id` is not a valid UUID: {fm.data['id']}")
    if isinstance(fm.data.get("id"), str) and UUID_RE.match(fm.data["id"]):
        id_owners[fm.data["id"]].append(str(rel))

    if isinstance(fm.data.get("version"), str) and not SEMVER_RE.match(fm.data["version"]):
        report.add(rel, "version-semver", f"`version` not semver: {fm.data['version']}")

    t = fm.data.get("type")
    if t and t not in VALID_TYPES:
        report.add(rel, "type-valid", f"unknown `type`: {t}")

    s = fm.data.get("status")
    if s and s not in VALID_STATUSES:
        report.add(rel, "status-valid", f"unknown `status`: {s}")

    expected_domain_suffix = rel.with_suffix("").as_posix()
    domain = fm.data.get("domain", "")
    if isinstance(domain, str) and not domain.endswith(expected_domain_suffix):
        report.add(
            rel, "domain-matches-path",
            f"domain `{domain}` does not end with `{expected_domain_suffix}`",
        )

    # Resolve relative markdown links (skip absolute URLs and anchors).
    for m in _MD_LINK_RE.finditer(fm.body):
        target = m.group(1).split("#", 1)[0].strip()
        if not target or _URI_RE.match(target):
            continue
        if (md.parent / target).resolve().exists():
            continue
        if (root / target).resolve().exists():
            continue
        report.add(rel, "link-resolves", f"broken link to `{target}`")


def phase_a(root: Path) -> CheckReport:
    report = CheckReport()
    id_owners: dict[str, list[str]] = defaultdict(list)
    files = iter_markdown(root)
    report.files_checked = len(files)
    for md in files:
        _check_one(md, root, report, id_owners)
    for uid, files_list in id_owners.items():
        if len(files_list) > 1:
            report.add(
                ", ".join(files_list), "id-unique",
                f"duplicate id `{uid}` across {len(files_list)} files",
            )
    return report
