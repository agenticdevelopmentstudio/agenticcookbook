"""Shared deterministic checks used by `lint` Phase A and `validate`."""

from __future__ import annotations

import functools
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
from . import history, refimpl
from .markdown import iter_markdown
from .scheme import COOKBOOK_SCHEME, SchemeError, cookbook_scheme, up_to_repo_top


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
        "Update `domain` to `<scheme>://<path>`: the scheme names the repo the file "
        "lives in (the cookbook index.md's `domain` scheme, else the repo's name) and "
        "the path is the file's path without `.md`. The issue shows the expected value."
    ),
    "reference-implementation-exists": (
        "Fix the path in `## Reference Implementations` (relative to the repository root; "
        "a directory ends with `/`), or remove the row. After moving code, `cookr relink` "
        "rewrites the paths git recorded as renamed."
    ),
    "reference-implementation-platform": (
        "Use one of: web, apple, android, windows, python."
    ),
    "link-resolves": (
        "Fix or remove the link target, or create the file it points to. A "
        "`<scheme>://<path>` link in this repo's own scheme must name a file in it."
    ),
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
# Code shows links without making them: an inline code span (a fenced block is
# dropped by `_prose`).
_CODE_SPAN_RE = re.compile(r"(`+)[^`].*?(?<!`)\1(?!`)", re.S)


def _prose(body: str) -> str:
    """`body` without its fenced code blocks and inline code spans."""
    lines = history.split_lines(body)
    kept = "\n".join(bare for _, bare in history.unfenced(lines) if bare is not None)
    return _CODE_SPAN_RE.sub("", kept)
# An absolute URI: `https://…`, `mailto:…`, or a domain identifier
# `<scheme>://<path>` (conventions.md, "URL-Based Domain Identifiers").
_URI_RE = re.compile(r"^[a-z][a-z0-9+.-]*:", re.IGNORECASE)
# Web and mail schemes never name a file in a cookbook.
_WEB_SCHEMES = frozenset({"http", "https", "mailto", "ftp", "file", "data", "tel"})


class _Schemes:
    """This cookbook's own scheme, derived once and only when a check needs it.

    None when it cannot be derived (a cookbook outside git whose index.md declares
    none): domain links then go unresolved, as nothing says which are this repo's.
    """

    def __init__(self, root: Path) -> None:
        self._root = root

    @functools.cached_property
    def own(self) -> str | None:
        try:
            return cookbook_scheme(self._root)
        except SchemeError:
            return None


def _near_miss(a: str, b: str) -> bool:
    """True when `a` is one or two edits from `b` but not `b` — a likely typo."""
    if a == b or abs(len(a) - len(b)) > 2:
        return False
    prev = list(range(len(b) + 1))
    for i, ca in enumerate(a, 1):
        cur = [i]
        for j, cb in enumerate(b, 1):
            cur.append(min(prev[j] + 1, cur[j - 1] + 1, prev[j - 1] + (ca != cb)))
        prev = cur
    return prev[-1] <= 2


def _domain_link_problem(target: str, root: Path, schemes: _Schemes) -> str | None:
    """Why the domain link `target` (`<scheme>://<path>`, fragment removed) is
    broken, or None.

    A link in this cookbook's own scheme names a file: `<path>.md` or `<path>`
    under the cookbook root, or under a parent of it up to the repo's top (a root
    passed as `-p recipes` sits below the directory its domain paths start from).
    Another repo's scheme cannot be checked here and passes, unless it is one or
    two edits from this repo's scheme or the cookbook's (`agenticdevelopercookbok`),
    which is a typo.
    """
    scheme, _, path = target.partition("://")
    own = schemes.own
    if own is None:
        return None
    if scheme != own:
        for known in (own, COOKBOOK_SCHEME):
            if _near_miss(scheme, known):
                return f"unknown scheme `{scheme}://` in `{target}`; did you mean `{known}://`?"
        return None
    path = path.strip("/")
    if not path:
        return None
    for base in up_to_repo_top(root):
        if (base / f"{path}.md").is_file() or (base / path).exists():
            return None
    return f"broken link to `{target}`: no `{path}.md` in this repo"


def _check_one(md: Path, root: Path, report: CheckReport, id_owners: dict[str, list[str]],
               schemes: _Schemes) -> None:
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
        expected = f"`{schemes.own}://{expected_domain_suffix}`" if schemes.own else (
            f"`<scheme>://{expected_domain_suffix}`")
        report.add(
            rel, "domain-matches-path",
            f"domain `{domain}` does not end with `{expected_domain_suffix}`; "
            f"expected {expected}",
        )

    # Resolve relative links and this repo's own domain links (skip web URLs and
    # anchors).
    for m in _MD_LINK_RE.finditer(_prose(fm.body)):
        target = m.group(1).split("#", 1)[0].strip()
        if not target:
            continue
        if _URI_RE.match(target):
            if "://" in target and target.split(":", 1)[0].lower() not in _WEB_SCHEMES:
                problem = _domain_link_problem(target, root, schemes)
                if problem:
                    report.add(rel, "link-resolves", problem)
            continue
        if (md.parent / target).resolve().exists():
            continue
        if (root / target).resolve().exists():
            continue
        report.add(rel, "link-resolves", f"broken link to `{target}`")

    for impl in refimpl.implementations(fm.body):
        if impl.platform not in refimpl.PLATFORMS:
            report.add(rel, "reference-implementation-platform",
                       f"Reference Implementations platform `{impl.platform}` is not one of "
                       f"{', '.join(refimpl.PLATFORMS)}")
        if not (_repo_top(root) / impl.path).exists():
            report.add(rel, "reference-implementation-exists",
                       f"Reference Implementations path `{impl.path}` does not exist")


@functools.cache
def _repo_top(root: Path) -> Path:
    """The top of the checkout holding `root`, which Reference Implementations
    paths are relative to; `root` itself outside git."""
    return up_to_repo_top(root)[-1]


def phase_a(root: Path) -> CheckReport:
    report = CheckReport()
    id_owners: dict[str, list[str]] = defaultdict(list)
    files = iter_markdown(root)
    report.files_checked = len(files)
    schemes = _Schemes(root)
    for md in files:
        _check_one(md, root, report, id_owners, schemes)
    for uid, files_list in id_owners.items():
        if len(files_list) > 1:
            report.add(
                ", ".join(files_list), "id-unique",
                f"duplicate id `{uid}` across {len(files_list)} files",
            )
    return report
