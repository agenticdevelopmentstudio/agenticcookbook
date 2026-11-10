"""Compile on contact: keep a repo's cookbook, and the cookbooks it depends on,
installed as skill sets scoped to the repos that use them.

Each cookbook is its own set in `$COOKR_HOME/sets/<rdid>`, registered with
skill-router as source `<rdid>`. A cookbook with a `.cookr.json` beside it is
routed only in the repos that use it: the roots in its receipt, plus the repo
syncing now (the main checkout's root, so a worktree is covered by it). A
cookbook without one (the adc cookbook) is routed everywhere. A stale or
missing set is recompiled and registered; a current one is left alone. The
always-on skill is never touched.
"""

from __future__ import annotations

import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Iterable, Optional

from . import install as inst
from . import skill as skill_mod
from .artifact import find_folders
from .index import Index, current_index
from .links import resolver_for
from .repoconfig import CONFIG_NAME, Config

OK, COMPILED, REGISTERED, BROKEN = "ok", "compiled", "registered", "broken"


@dataclass
class SyncLine:
    action: str                 # ok | compiled | registered | broken
    rdid: str
    skills: int = 0
    detail: str = ""

    def as_json(self) -> dict:
        return {"action": self.action, "rdid": self.rdid, "skills": self.skills, "detail": self.detail}

    def text(self) -> str:
        if self.action == BROKEN:
            return f"broken {self.rdid}: {self.detail}"
        return f"{self.action} {self.rdid} ({self.skills} skills)"


def main_checkout_root(repo_root: Path) -> Path:
    """The root of the repo's main checkout: a worktree's skills route under
    it, and a path outside git is its own root."""
    repo_root = Path(repo_root).resolve()
    try:
        p = subprocess.run(["git", "-C", str(repo_root), "rev-parse", "--path-format=absolute",
                            "--git-common-dir"], capture_output=True, text=True)
    except OSError:
        return repo_root
    common = Path(p.stdout.strip()) if p.returncode == 0 and p.stdout.strip() else None
    return common.resolve().parent if common is not None and common.name == ".git" else repo_root


def _count(set_dir: Path) -> int:
    return len(list(set_dir.glob(f"*/{skill_mod.SKILL_FILE}"))) if set_dir.is_dir() else 0


def sync_one(cookbook_dir: Path, index: Index, add_scopes: Iterable[Path],
             router: Optional[inst.Router]) -> SyncLine:
    """Bring one cookbook's set up to date. `add_scopes` are the repo roots to
    add to the scopes it was registered with; none means a cookbook routed everywhere."""
    rdid = index.cookbook.rdid
    try:
        library = skill_mod.library_name(rdid)
        folders = find_folders([cookbook_dir])
        if not folders:
            return SyncLine(OK, rdid, 0)
        root = inst.home()
        add = [str(s) for s in add_scopes]
        scopes = (*inst.receipt_scopes(inst.read_receipt(root), library), *add) if add else ()
        i = inst.Installer(folders=folders, library=library, routed=True, router=router, root=root,
                           templates=skill_mod.templates_root(cookbook_dir), scopes=scopes)
        if all(s.state == inst.OK for s in i.check()):
            return SyncLine(OK, rdid, _count(i.set_dir))
        statuses = i.install()
    except (ValueError, inst.RouterError, OSError) as e:
        return SyncLine(BROKEN, rdid, detail=str(e))
    bad = [s for s in statuses if s.failed]
    if bad:
        return SyncLine(BROKEN, rdid, detail=f"{bad[0].item}: {bad[0].detail}")
    registered = any(s.action == "registered" for s in statuses)
    return SyncLine(REGISTERED if registered else COMPILED, rdid, _count(i.set_dir))


def sync(config: Config, warn: Callable[[str], None], router: Optional[inst.Router] = None) -> list[SyncLine]:
    """Sync the repo's cookbook, then each dependency cookbook it can reach;
    an unreachable one is warned about and skipped. A skill-router older than
    ROUTER_MIN raises RouterError once, before any library is touched."""
    router = router if router is not None else inst.Router.find()
    if router is not None:
        router.require_version()
    own = current_index(config.cookbook_dir)
    resolver = resolver_for(config, own)
    root = main_checkout_root(config.repo_root) if config.config_file is not None else None
    lines = [sync_one(config.cookbook_dir, own, [root] if root else [], router)]
    for dep in sorted(config.dependencies.values(), key=lambda d: d.rdid):
        path, index = resolver.dir_for(dep.id), resolver.index_for(dep.id)
        if path is None or index is None:
            warn(f"dependency {dep.rdid} ({dep.id}) is not reachable; its skills were not synced")
            continue
        # A dependency in a repo of its own is routed there too, whichever repo syncs it
        # first; one in an unscoped repo still gets the scope of the repo syncing it,
        # never routed everywhere.
        repo = path.parent
        roots = ([main_checkout_root(repo)] if (repo / CONFIG_NAME).is_file() else [])
        lines.append(sync_one(path, index, [*roots, *([root] if root else [])], router))
    return lines
