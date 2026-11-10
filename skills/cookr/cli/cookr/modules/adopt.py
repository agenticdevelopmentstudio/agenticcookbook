"""`cookr adopt` — turn a repo into a cookr repo.

    cookr adopt --rdid R --root PATH:PLATFORM[:KIND[:GROUP]]... [--dependency LOCATION]...

`-p` names the repo to adopt (default: cwd). Runs `create`, then writes `.cookr.json`: the roots, and a dependency for each
LOCATION (a cookbook directory, relative to the repo or absolute), whose id and
rdid come from its `cookbook.json` (format 1 through `derive_index`). Prints
`cookr status`. Idempotent: the same arguments change nothing; an existing
`.cookr.json` that disagrees is refused (exit 1), one the new arguments only add
to is merged. An unreadable LOCATION, or a bad --root, exits 2.
"""

from __future__ import annotations

import argparse
import json
from dataclasses import replace
from pathlib import Path

from rich.markup import escape

from ..core.errors import CookbookError
from ..core.identity import MANIFEST, IdentityError, read_manifest
from ..core.repoconfig import (CONFIG_NAME, KINDS, PLATFORMS, ConfigError, Dependency, Root,
                               config_for_cookbook, load_repo_config, write_repo_config)
from ..core.upgrade import derive_index
from . import status
from .create import CreateRefused, create_cookbook

NAME = "adopt"
HELP = "Adopt a repo: create its cookbook and write .cookr.json (roots, dependencies)."
CREATES_REPO = True  # -p names the repo to adopt, which need hold no cookbook yet


class AdoptInput(CookbookError):
    """Malformed arguments or an unreadable dependency (exit 2)."""


def register(parser) -> None:
    parser.add_argument("--rdid", required=True, help="The cookbook's rdid.")
    parser.add_argument("--root", action="append", default=[],
                        metavar="PATH:PLATFORM[:KIND[:GROUP]]",
                        help="A code root (repeatable). KIND is ui or logic (default ui).")
    parser.add_argument("--dependency", action="append", default=[], metavar="LOCATION",
                        help="A dependency cookbook's directory (repeatable).")


def parse_root(spec: str, repo: Path) -> Root:
    parts = spec.split(":")
    if len(parts) < 2 or len(parts) > 4 or not parts[0] or not parts[1]:
        raise AdoptInput(f"--root {spec!r}: expected PATH:PLATFORM[:KIND[:GROUP]]")
    path, platform = parts[0].strip("/"), parts[1]
    kind = parts[2] if len(parts) > 2 and parts[2] else "ui"
    group = parts[3].strip("/") if len(parts) > 3 else ""
    if platform not in PLATFORMS:
        raise AdoptInput(f"--root {spec!r}: unknown platform `{platform}` "
                         f"(one of {', '.join(PLATFORMS)})")
    if kind not in KINDS:
        raise AdoptInput(f"--root {spec!r}: unknown kind `{kind}` (one of {', '.join(KINDS)})")
    if ".." in Path(path).parts or Path(path).is_absolute() or ".." in group.split("/"):
        raise AdoptInput(f"--root {spec!r}: path and group must stay inside the repo")
    if not (repo / path).is_dir():
        raise AdoptInput(f"--root {spec!r}: {path} is not a directory in {repo}")
    return Root(path, platform, kind, group)


def read_dependency(location: str, repo: Path) -> Dependency:
    cb = Path(location)
    cb = cb if cb.is_absolute() else repo / cb
    try:
        data = json.loads((cb / MANIFEST).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as e:
        raise AdoptInput(f"--dependency {location}: cannot read {cb / MANIFEST}: {e}") from e
    if not isinstance(data, dict):
        raise AdoptInput(f"--dependency {location}: {cb / MANIFEST} must be a JSON object")
    try:
        if data.get("format") == 2:
            ident = read_manifest(cb)
        else:
            ident = derive_index(cb).cookbook
    except (CookbookError, OSError) as e:  # NeedsUpgrade/UpgradeError/IdentityError, unreadable files
        raise AdoptInput(f"--dependency {location}: {e}") from e
    return Dependency(ident.id, ident.rdid, location)


def _merge(path: Path, repo: Path, rdid: str, roots: list, deps: list):
    """The existing config plus pure additions; CreateRefused on any conflict."""
    cfg = load_repo_config(repo)
    if cfg.cookbook != "cookbook" or cfg.identity.rdid != rdid:
        raise CreateRefused(f"{path} names the cookbook `{cfg.identity.rdid}` at "
                            f"`{cfg.cookbook}`, not `{rdid}`; refusing to change it")
    have_roots = {r.path: r for r in cfg.roots}
    for r in roots:
        old = have_roots.get(r.path)
        if old is not None and old != r:
            raise CreateRefused(f"{path} already has root {r.path} as {old.platform}/{old.kind}/"
                                f"{old.group or '-'}; refusing to change it")
    for d in deps:
        old = cfg.dependencies.get(d.id)
        if old is not None and old != d:
            raise CreateRefused(f"{path} already has dependency {d.id} as {old.rdid} at "
                                f"{old.location}; refusing to change it")
    merged = {**cfg.dependencies, **{d.id: d for d in deps}}
    return cfg, replace(cfg, roots=list(cfg.roots) + [r for r in roots if r.path not in have_roots],
                        dependencies=dict(sorted(merged.items())))


def run(args, ctx) -> int:
    repo = ctx.cwd.resolve()
    ctx.ui.title("cookr adopt")
    try:
        roots = [parse_root(s, repo) for s in args.root]
        deps = [read_dependency(loc, repo) for loc in args.dependency]
    except AdoptInput as e:
        ctx.ui.error(escape(str(e)))
        return 2
    path = repo / CONFIG_NAME
    try:
        # Judge the existing config first: a refused adopt leaves nothing behind.
        merged = _merge(path, repo, args.rdid, roots, deps) if path.is_file() else None
        create_cookbook(repo, args.rdid)
        if merged is not None:
            old, new = merged
            if new != old:
                write_repo_config(new)
                ctx.ui.ok(escape(f"updated {path.name}"))
            else:
                ctx.ui.skip(escape(f"{path.name} already up to date"))
        else:
            write_repo_config(replace(
                config_for_cookbook(repo / "cookbook"), repo_root=repo, roots=roots,
                dependencies=dict(sorted((d.id, d) for d in deps)), config_file=path))
            ctx.ui.ok(escape(f"wrote {path.name}"))
        config = load_repo_config(repo)
    except (CookbookError, IdentityError, ConfigError) as e:
        ctx.ui.error(escape(str(e)))
        return 1
    return status.run(argparse.Namespace(json=False),
                      replace(ctx, config=config, config_error=None))
