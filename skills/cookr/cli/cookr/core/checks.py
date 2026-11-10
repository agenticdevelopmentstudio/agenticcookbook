"""Shared deterministic checks used by `lint` Phase A and `validate`.

Format 2: an artifact is a source folder whose identity is its `id` (a UUID);
its `depends-on`, `related` and in-text links (`[<rdid>](cookbook:<uuid>)`)
are UUIDs resolved through the cookbook index (`links.Resolver`). A link the
index does not hold is an issue; one into a cookbook that cannot be reached
here is a warning. The code that implements an artifact is listed in the
index (`implementations`), and each row's platform and location are checked.
A markdown doc with no source folder is still checked for its frontmatter and
relative links.
"""

from __future__ import annotations

import re
from collections import defaultdict
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

from . import history
from .artifact import ArtifactError, find_folders, folder_for, is_folder, load_folder
from .errors import CookbookError
from .frontmatter import (
    REQUIRED_FIELDS,
    SEMVER_RE,
    UUID_RE,
    VALID_STATUSES,
    VALID_TYPES,
    parse_file,
)
from .identity import MANIFEST
from .links import Resolver, in_text_links, parse_link, resolver_for
from .markdown import iter_markdown
from .repoconfig import CONFIG_NAME, PLATFORMS, Config, config_for_cookbook, find_repo, load_repo_config


# Per-rule fix-it hints. Keyed on the `rule` slug emitted below.
# `required-field:<name>` is matched by prefix.
_FIX_ITS: dict[str, str] = {
    "frontmatter-present": (
        "Add a YAML frontmatter block (between `---` lines) at the top of the file. "
        "Run `cookr update` to scaffold a minimal one."
    ),
    "folder-loads": (
        "Fix the source folder's `artifact.json`; a format-1 folder is upgraded with `cookr upgrade`."
    ),
    "id-uuid": "Replace `id` with a UUID4: `python -c 'import uuid; print(uuid.uuid4())'`.",
    "id-unique": "Two artifacts share the same `id`. Regenerate one with `python -c 'import uuid; print(uuid.uuid4())'`.",
    "version-semver": "Use a semver string for `version` (e.g. `1.0.0`).",
    "type-valid": f"`type` must be one of: {', '.join(sorted(VALID_TYPES))}.",
    "status-valid": f"`status` must be one of: {', '.join(sorted(VALID_STATUSES))}.",
    "index-valid": "Fix the cookbook's `index.json`, or run `cookr update` to rebuild it from the folders.",
    "reference-implementation-exists": (
        "Fix the implementation's location in the cookbook index (relative to the repository "
        "root; a directory ends with `/`) with `cookr implements`, or mark it planned. After "
        "moving code, `cookr relink` rewrites the locations git recorded as renamed."
    ),
    "reference-implementation-platform": (
        f"Use one of: {', '.join(PLATFORMS)}."
    ),
    "link-resolves": (
        "Fix or remove the link, or create what it points to. A `depends-on`/`related` entry is "
        "a UUID (`<cookbook-uuid>/<uuid>` for another cookbook's artifact); a link in the text "
        "is `[<rdid>](cookbook:<uuid>)`; a relative link names a file."
    ),
    "link-format": (
        "Rewrite the `<scheme>://<path>` link as `[<rdid>](cookbook:<uuid>)`; "
        "`cookr upgrade` converts a format-1 cookbook's links."
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
            f"`cookr update` will fill required fields with sensible defaults."
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
    warnings: list[CheckIssue] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return not self.issues

    def add(self, file: Path | str, rule: str, detail: str) -> None:
        self.issues.append(CheckIssue(file=str(file), rule=rule, detail=detail))

    def warn(self, file: Path | str, rule: str, detail: str) -> None:
        self.warnings.append(CheckIssue(file=str(file), rule=rule, detail=detail))


_MD_LINK_RE = re.compile(r"\[[^\]]*\]\(([^)]+)\)")
# Code shows links without making them: an inline code span (a fenced block is
# dropped by `_prose`).
_CODE_SPAN_RE = re.compile(r"(`+)[^`].*?(?<!`)\1(?!`)", re.S)
# An absolute URI: `https://…`, `mailto:…`, `cookbook:…`, or a format-1 domain
# identifier `<scheme>://<path>`.
_URI_RE = re.compile(r"^[a-z][a-z0-9+.-]*:", re.IGNORECASE)
# Web and mail schemes never name a cookbook artifact.
_WEB_SCHEMES = frozenset({"http", "https", "mailto", "ftp", "file", "data", "tel"})
_LINK_FIELDS = ("depends-on", "related")


def _prose(body: str) -> str:
    """`body` without its fenced code blocks and inline code spans."""
    lines = history.split_lines(body)
    kept = "\n".join(bare for _, bare in history.unfenced(lines) if bare is not None)
    return _CODE_SPAN_RE.sub("", kept)


def _is_url(location: str) -> bool:
    return "://" in location


def _config_for(root: Path) -> Optional[Config]:
    """The repo config whose cookbook is `root`, else one for `root` alone; None
    when `root` has no format-2 manifest (nothing to resolve UUID links with)."""
    if not (root / MANIFEST).is_file():
        return None
    repo = find_repo(root)
    if repo is not None and (repo / CONFIG_NAME).is_file():
        try:
            cfg = load_repo_config(repo)
            if cfg.cookbook_dir.resolve() == root.resolve():
                return cfg
        except CookbookError:
            pass
    try:
        return config_for_cookbook(root)
    except CookbookError:
        return None


def _check_link(rel, where: str, link_text: str, resolver: Optional[Resolver],
                report: CheckReport) -> None:
    """One UUID link: malformed or missing is an issue, unreachable a warning."""
    try:
        link = parse_link(link_text)
    except ValueError:
        report.add(rel, "link-resolves", f"{where} `{link_text}` is not a UUID link")
        return
    if resolver is None:
        return
    res = resolver.resolve(link)
    if res.state == "missing":
        report.add(rel, "link-resolves", f"{where} `{link_text}` names no artifact in its cookbook")
    elif res.state == "unreachable":
        report.warn(rel, "link-resolves",
                    f"{where} `{link_text}`: cookbook {link.cookbook} cannot be reached here")


def _check_meta(rel, data: dict, report: CheckReport, id_owners: dict[str, list[str]]) -> None:
    for f in REQUIRED_FIELDS:
        if f not in data or data.get(f) in (None, ""):
            report.add(rel, f"required-field:{f}", f"missing or empty `{f}`")

    uid = data.get("id")
    if isinstance(uid, str):
        if UUID_RE.match(uid):
            id_owners[uid.lower()].append(str(rel))
        else:
            report.add(rel, "id-uuid", f"`id` is not a valid UUID: {uid}")

    if isinstance(data.get("version"), str) and not SEMVER_RE.match(data["version"]):
        report.add(rel, "version-semver", f"`version` not semver: {data['version']}")

    t = data.get("type")
    if t and t not in VALID_TYPES:
        report.add(rel, "type-valid", f"unknown `type`: {t}")

    s = data.get("status")
    if s and s not in VALID_STATUSES:
        report.add(rel, "status-valid", f"unknown `status`: {s}")


def _check_links(rel, data: dict, body: str, base: Path, root: Path,
                 resolver: Optional[Resolver], report: CheckReport) -> None:
    """`depends-on`/`related` and every link in the prose. Relative links are
    resolved from `base` (where the doc sits), then from the cookbook root."""
    for name in _LINK_FIELDS:
        values = data.get(name) or []
        for value in values if isinstance(values, list) else [values]:
            _check_link(rel, f"`{name}` entry", str(value), resolver, report)

    prose = _prose(body)
    for _, link in in_text_links(prose):
        target = f"{link.cookbook}/{link.artifact}" if link.cookbook else link.artifact
        _check_link(rel, "link", target, resolver, report)

    for m in _MD_LINK_RE.finditer(prose):
        target = m.group(1).split("#", 1)[0].strip()
        if not target:
            continue
        if _URI_RE.match(target):
            scheme = target.split(":", 1)[0].lower()
            if scheme == "cookbook":
                if not in_text_links(m.group(0)):
                    report.add(rel, "link-resolves", f"`{target}` is not a `cookbook:<uuid>` link")
            elif "://" in target and scheme not in _WEB_SCHEMES:
                report.add(rel, "link-format", f"format-1 domain link `{target}`")
            continue
        if (base / target).resolve().exists() or (root / target).resolve().exists():
            continue
        report.add(rel, "link-resolves", f"broken link to `{target}`")


def _check_implementations(config: Config, resolver: Resolver, report: CheckReport) -> None:
    """Every index implementation row: a known platform, and a location that
    exists in the repo unless it is a URL or the row is planned."""
    for entry in sorted(resolver.own.entries.values(), key=lambda e: e.path):
        rel = f"index.json ({entry.rdid})"
        for impl in entry.implementations:
            if impl.platform not in PLATFORMS:
                report.add(rel, "reference-implementation-platform",
                           f"implementation platform `{impl.platform}` is not one of "
                           f"{', '.join(PLATFORMS)}")
            loc = impl.location
            if not loc or _is_url(loc) or impl.conformance.state == "planned":
                continue
            if not (config.repo_root / loc).exists():
                report.add(rel, "reference-implementation-exists",
                           f"implementation location `{loc}` does not exist")


def phase_a(root: Path, config: Optional[Config] = None) -> CheckReport:
    """Check every artifact under cookbook `root`. `config` is the repo config
    whose cookbook is `root`; derived when not given."""
    root = Path(root)
    report = CheckReport()
    id_owners: dict[str, list[str]] = defaultdict(list)

    if config is None or config.cookbook_dir.resolve() != root.resolve():
        config = _config_for(root)
    resolver: Optional[Resolver] = None
    if config is None:
        report.warn(f"{root.name}/{MANIFEST}", "links-unchecked",
                    f"no readable format-2 {MANIFEST}: UUID links and index implementations "
                    "were not checked")
    else:
        try:
            resolver = resolver_for(config)
        except CookbookError as e:
            report.add(f"{root.name}/index.json", "index-valid", str(e))

    folders = find_folders([root])
    for folder in folders:
        rel = f"{folder.relative_to(root).as_posix()}/"
        try:
            art = load_folder(folder)
        except ArtifactError as e:
            report.add(rel, "folder-loads", str(e))
            continue
        _check_meta(rel, art.meta, report, id_owners)
        _check_links(rel, art.meta, art.body(), folder.parent, root, resolver, report)

    docs = [md for md in iter_markdown(root) if not is_folder(folder_for(md))]
    for md in docs:
        rel = md.relative_to(root)
        fm = parse_file(md)
        if not fm.had_frontmatter:
            report.add(rel, "frontmatter-present", "no YAML frontmatter block found")
            continue
        _check_meta(rel, fm.data, report, id_owners)
        _check_links(rel, fm.data, fm.body, md.parent, root, resolver, report)

    if config is not None and resolver is not None:
        _check_implementations(config, resolver, report)

    report.files_checked = len(folders) + len(docs)
    for uid, owners in id_owners.items():
        if len(owners) > 1:
            report.add(", ".join(owners), "id-unique",
                       f"duplicate id `{uid}` across {len(owners)} files")
    return report


def show(report: CheckReport, ui) -> int:
    """Print a Phase A report: warnings (never fatal), then issues. 1 on issues."""
    if report.warnings:
        ui.table(["file", "rule", "warning"],
                 [[w.file, w.rule, w.detail] for w in report.warnings])
        ui.warn(f"{len(report.warnings)} warning(s): checked as far as this checkout allows.")
    if report.ok:
        ui.ok(f"All {report.files_checked} artifacts passed deterministic checks.")
        return 0
    ui.table(["file", "rule", "issue", "fix"],
             [[i.file, i.rule, i.detail, fix_for(i.rule)] for i in report.issues])
    ui.error(f"{len(report.issues)} issue(s) across {report.files_checked} files.")
    return 1
