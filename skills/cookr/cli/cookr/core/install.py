"""Put a compiled cookbook where agents reach it, check it is still there and
current, and take it away again.

Three kinds of item, each OK, MISSING, DRIFT or BROKEN:

    set        the routed skills, compiled into <home>/sets/<library>
    routed     that set, registered with skill-router as source <library>
    always-on  the principles skill, rendered for one target into the host's
               skills dir (`<skills_dir>/general-principles/SKILL.md`)

<home> is $COOKR_HOME, else ~/.cookr. Its `install.json` is the receipt:
every item install put somewhere, with what it wrote and the paths it was
installed from. Uninstall works from the receipt alone and touches nothing it
does not list. A skill dir already in a host's skills dir that cookr did not
install is BROKEN until `adopt` moves it to <home>/backup/, and uninstall puts
it back.

A library is installed from one set of paths. Installing it from others (a
second cookbook that defaults to the same library name, or a subdirectory of
the first) would replace every skill it installed, so it is refused until
`replace` says to.

The receipt is read, changed and written under a lock (`install.lock`), and
written atomically, also when an install fails part way.

skill-router is driven through its CLI (`skill-router-registry`, or the command
in $COOKR_SKILL_ROUTER_REGISTRY), never imported: it is a separate tool with
its own Python.
"""

from __future__ import annotations

import hashlib
import json
import os
import re
import shlex
import shutil
import subprocess
from contextlib import contextmanager
from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable, Iterator, Optional

try:
    import fcntl
except ImportError:  # Windows: no advisory locks; one install at a time is on the user
    fcntl = None

from . import always_on
from . import hosts as hosts_mod
from . import skill as skill_mod
from . import tuning

OK, MISSING, DRIFT, BROKEN = "ok", "missing", "drift", "broken"
RECEIPT = "install.json"
LOCK = "install.lock"
ROUTED = "routed"
ROUTER_ENV = "COOKR_SKILL_ROUTER_REGISTRY"
ROUTER_MIN = (0, 2, 0)          # register-dir --source/--replace/--new-keyword, unregister --source


class InstallError(ValueError):
    """A target, receipt or router that install cannot work with."""


def home() -> Path:
    return Path(os.environ.get("COOKR_HOME") or "~/.cookr").expanduser()


def sha256(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


@dataclass
class Status:
    item: str                   # set:<lib> | routed:<lib> | always-on:<host>:<name> | library:<lib>
    state: str
    detail: str = ""
    action: str = ""            # what was done, or with dry_run what would be

    @property
    def failed(self) -> bool:
        return self.state != OK

    def as_json(self) -> dict:
        return {"item": self.item, "state": self.state, "detail": self.detail, "action": self.action}


# ── receipt ──────────────────────────────────────────────────────────────────

def read_receipt(root: Path) -> dict[str, dict]:
    path = root / RECEIPT
    if not path.is_file():
        return {}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        raise InstallError(f"{path}: {e}") from e
    if data.get("format") != 1:
        raise InstallError(f"{path}: unknown receipt format {data.get('format')!r}")
    return dict(data.get("items", {}))


def write_receipt(root: Path, items: dict[str, dict]) -> None:
    """Write the receipt atomically (a reader never sees half of one), or
    remove it when it lists nothing."""
    path = root / RECEIPT
    if not items:
        if path.is_file():
            path.unlink()
        return
    root.mkdir(parents=True, exist_ok=True)
    tmp = root / f".{RECEIPT}.{os.getpid()}.tmp"
    tmp.write_text(skill_mod.dump_json({"format": 1, "items": dict(sorted(items.items()))}),
                   encoding="utf-8")
    os.replace(tmp, path)


@contextmanager
def _locked(root: Path) -> Iterator[None]:
    """Hold `<root>/install.lock`. When the receipt is gone on release, the
    lock file goes too (and <root> with it, once empty); a waiter that then
    holds the removed file sees it is no longer the lock and takes the new one."""
    root.mkdir(parents=True, exist_ok=True)
    path = root / LOCK
    while True:
        fd = os.open(path, os.O_RDWR | os.O_CREAT, 0o644)
        if fcntl is not None:
            fcntl.flock(fd, fcntl.LOCK_EX)
        try:
            current = os.fstat(fd).st_ino == os.stat(path).st_ino
        except FileNotFoundError:
            current = False
        if current:
            break
        os.close(fd)
    try:
        yield
    finally:
        empty = not (root / RECEIPT).exists()
        if empty and path.exists():
            path.unlink()
        os.close(fd)
        if empty:
            try:
                _prune_empty(root, root.parent)
            except OSError:  # another install started meanwhile
                pass


def _prune_empty(d: Path, stop: Path) -> None:
    """Remove `d` and its parents up to (not including) `stop` while empty."""
    while d != stop and d.is_dir() and not any(d.iterdir()):
        d.rmdir()
        d = d.parent


def _first_missing(d: Path) -> Optional[str]:
    """The topmost of `d` and its parents that does not exist yet: what
    creating `d` creates, and so what uninstall may remove once empty."""
    missing = None
    while not (d.exists() or d.is_symlink()):
        missing, d = d, d.parent
    return str(missing) if missing else None


def _exists(p: Path) -> bool:
    return p.exists() or p.is_symlink()


def set_digest(d: Path) -> str:
    """Every file of a compiled set, hashed: what skill-router indexed when
    the set was registered, so a set recompiled since then is noticed."""
    h = hashlib.sha256()
    for p in sorted(q for q in d.rglob("*") if q.is_file()) if d.is_dir() else ():
        h.update(p.relative_to(d).as_posix().encode("utf-8") + b"\0" + p.read_bytes() + b"\0")
    return h.hexdigest()


# ── skill-router ─────────────────────────────────────────────────────────────

class RouterError(RuntimeError):
    pass


class Router:
    """skill-router's registry CLI, run as a subprocess."""

    def __init__(self, command: list[str]):
        self.command = command
        self._version_ok = False

    @classmethod
    def find(cls) -> Optional["Router"]:
        cmd = os.environ.get(ROUTER_ENV)
        if cmd:
            return cls(shlex.split(cmd))
        exe = shutil.which("skill-router-registry")
        return cls([exe]) if exe else None

    def _exec(self, *args: str) -> subprocess.CompletedProcess:
        try:
            return subprocess.run([*self.command, *args], capture_output=True, text=True)
        except OSError as e:
            raise RouterError(f"cannot run {shlex.join(self.command)}: {e}") from e

    def require_version(self) -> None:
        """Refuse a skill-router older than ROUTER_MIN: it would reject the
        flags cookr passes, or (before `--version`) take them as something else."""
        if self._version_ok:
            return
        p = self._exec("--version")
        m = re.search(r"(\d+)\.(\d+)\.(\d+)", p.stdout) if p.returncode == 0 else None
        need = ".".join(map(str, ROUTER_MIN))
        if m is None or tuple(map(int, m.groups())) < ROUTER_MIN:
            found = f"is {m.group(0)}" if m else "has no --version, so predates it"
            raise RouterError(f"{shlex.join(self.command)} {found}; cookr needs skill-router "
                              f"{need} or later (register-dir --source --replace)")
        self._version_ok = True

    def _run(self, *args: str) -> dict:
        self.require_version()
        p = self._exec(*args, "--json")
        try:
            data = json.loads(p.stdout) if p.stdout.strip() else None
        except json.JSONDecodeError:
            data = None
        if data is None:
            raise RouterError((p.stderr or p.stdout).strip() or f"{args[0]} exited {p.returncode}")
        return data

    def listed(self, source: str) -> list[dict]:
        return list(self._run("list", "--source", source).get("skills", []))

    def register(self, set_dir: Path, source: str) -> dict:
        """A set's keywords are its library's directory names, reviewed in
        that repo, so near-duplicates (`service` beside `services`) are
        accepted and reported, not refused as a hand-typed one would be."""
        return self._run("register-dir", str(set_dir), "--source", source, "--replace", "--new-keyword")

    def unregister(self, source: str) -> None:
        self._run("unregister-skill", "--source", source)


# ── what to install ──────────────────────────────────────────────────────────

@dataclass(frozen=True)
class HostTarget:
    host: hosts_mod.Host
    chain: tuple[str, ...]

    @property
    def target(self) -> str:
        return self.chain[-1]

    @property
    def skills_dir(self) -> Path:
        return Path(self.host.skills_dir).expanduser()


def host_target(spec: str, hosts: dict) -> HostTarget:
    """A bare host (`claude`) is the host itself, not its default model: the
    always-on skill sits in a skills dir every model on the host reads."""
    name, dot, _ = spec.partition(".")
    if not dot:
        h = hosts_mod.host(name, hosts)
        return HostTarget(h, h.chain())
    chain = hosts_mod.parse_target(spec, hosts)
    return HostTarget(hosts_mod.host(chain[0], hosts), chain)


def select(specs: Optional[Iterable[str]], hosts: Optional[dict] = None,
           receipt: Optional[dict[str, dict]] = None) -> tuple[bool, list[HostTarget]]:
    """(routed?, host targets) for `--target` values. With none: the routed
    set, and each host whose home (the skills dir's parent) exists, at the
    target the receipt says it was installed for, else the host itself."""
    hosts = hosts_mod.manifest() if hosts is None else hosts
    if not specs:
        installed = {r.get("host"): r.get("target") for r in (receipt or {}).values()
                     if r.get("kind") == "always-on"}
        found = [h for h in hosts.values() if Path(h.skills_dir).expanduser().parent.is_dir()]
        return True, [host_target(installed.get(h.name) or h.name, hosts) for h in found]
    specs = list(specs)
    targets = [host_target(s, hosts) for s in specs if s != ROUTED]
    seen = [t.host.name for t in targets]
    dup = sorted({n for n in seen if seen.count(n) > 1})
    if dup:
        raise InstallError(f"one target per host: {', '.join(dup)} given more than once")
    return ROUTED in specs, targets


# ── the installer ────────────────────────────────────────────────────────────

@dataclass
class Installer:
    folders: list[Path]
    library: Optional[str] = None
    routed: bool = True
    targets: list[HostTarget] = field(default_factory=list)
    concerns: Optional[Path] = None
    router: Optional[Router] = None
    root: Path = field(default_factory=home)
    origin: tuple[str, ...] = ()    # the paths installed from; () checks no origin
    templates: Path = skill_mod.PACKAGED_TEMPLATES   # holding skill/ and always/

    def __post_init__(self):
        self.library = skill_mod.library_name(self.library)
        self.origin = tuple(self.origin)

    @property
    def source(self) -> str:
        return self.library or skill_mod.DEFAULT_LIBRARY

    @property
    def set_dir(self) -> Path:
        return self.root / "sets" / self.source

    @contextmanager
    def _receipt(self, dry_run: bool) -> Iterator[dict[str, dict]]:
        """The receipt, written back (under the lock) however the block ends."""
        if dry_run:
            yield read_receipt(self.root)
            return
        with _locked(self.root):
            receipt = read_receipt(self.root)
            try:
                yield receipt
            finally:
                write_receipt(self.root, receipt)

    def _record(self, kind: str, **rest) -> dict:
        rec = {"kind": kind, "library": self.source, **rest}
        if self.origin:
            rec["from"] = list(self.origin)
        return rec

    def _conflict(self, receipt: dict[str, dict]) -> Optional[Status]:
        """BROKEN when this library was installed from other paths."""
        if not self.origin:
            return None
        for rec in receipt.values():
            was = rec.get("from")
            if rec.get("library") == self.source and was is not None and was != list(self.origin):
                return Status(f"library:{self.source}", BROKEN,
                              f"library {self.source!r} was installed from {', '.join(was)}, not "
                              f"{', '.join(self.origin)}; --replace installs it from these instead, "
                              "or --library names a separate one")
        return None

    # states ------------------------------------------------------------------

    def _set_report(self, write: bool = False) -> skill_mod.SetReport:
        return skill_mod.compile_set(self.folders, self.set_dir, library=self.library, write=write,
                                     templates=self.templates / "skill")

    @staticmethod
    def _broken(rep: skill_mod.SetReport) -> list[str]:
        out = [f"{r.source}: {r.detail or r.status}" for r in rep.results if r.status in ("error", "broken")]
        out += [f"route {n or '(top)'} lists {c} skills, over the cap of {skill_mod.FANOUT_CAP}"
                for n, c in sorted(rep.over_cap.items())]
        return out

    def _set_status(self, rep: skill_mod.SetReport) -> Status:
        item = f"set:{self.source}"
        broken = self._broken(rep)
        if broken:
            more = f" (+{len(broken) - 1} more)" if len(broken) > 1 else ""
            return Status(item, BROKEN, broken[0] + more)
        if not (self.set_dir / skill_mod.RECEIPT).is_file():
            return Status(item, MISSING, str(self.set_dir))
        stale = [r for r in rep.results if r.status in ("stale", "missing")]
        if stale:
            return Status(item, DRIFT, f"{len(stale)} of {len(rep.results)} out of date")
        return Status(item, OK, str(self.set_dir))

    @staticmethod
    def _compiled(rep: skill_mod.SetReport) -> dict[Path, str]:
        """{folder: skill name} for every folder that compiles."""
        return {r.source.resolve(): r.dest.name for r in rep.results
                if r.status not in ("error", "broken") and r.detail != "no longer compiled"}

    def _expected_names(self, rep: skill_mod.SetReport) -> set[str]:
        return set(self._compiled(rep).values())

    def _routed_status(self, rep: skill_mod.SetReport, set_state: str, receipt: dict[str, dict]) -> Status:
        item = f"{ROUTED}:{self.source}"
        if self.router is None:
            return Status(item, BROKEN, "skill-router-registry not found; install skill-router "
                                        f"or set {ROUTER_ENV}")
        try:
            listed = self.router.listed(self.source)
        except RouterError as e:
            return Status(item, BROKEN, str(e))
        if set_state == BROKEN:
            return Status(item, BROKEN, "the set does not compile")
        if not listed:
            return Status(item, MISSING, f"no skills registered from source {self.source!r}")
        want, have = self._expected_names(rep), {e["name"] for e in listed}
        outside = [e["name"] for e in listed
                   if Path(e["path"]).resolve().parent != self.set_dir.resolve()]
        if want != have:
            return Status(item, DRIFT, f"{len(want - have)} to register, {len(have - want)} to remove")
        if outside:
            return Status(item, DRIFT, f"{len(outside)} registered from outside {self.set_dir}")
        if set_state != OK:
            return Status(item, DRIFT, "registered from a set that is out of date")
        if (receipt.get(item) or {}).get("digest") != set_digest(self.set_dir):
            return Status(item, DRIFT, "the set was compiled again since it was registered")
        return Status(item, OK, f"{len(have)} skills")

    def _always_on(self, rep: skill_mod.SetReport) -> Optional[always_on.AlwaysOn]:
        return always_on.principles_skill(self.folders, library=self.library, concerns=self.concerns,
                                          compiled=self._compiled(rep), templates=self.templates / "always")

    @staticmethod
    def _always_item(t: HostTarget, name: str) -> str:
        return f"always-on:{t.host.name}:{name}"

    @staticmethod
    def _edited(rec: Optional[dict]) -> bool:
        """The always-on file the receipt lists, changed since cookr wrote it."""
        if not rec:
            return False
        dest = Path(rec["path"])
        return dest.is_file() and sha256(dest.read_text(encoding="utf-8")) != rec.get("sha256")

    def _always_status(self, t: HostTarget, skill: always_on.AlwaysOn, text: str,
                       receipt: dict[str, dict]) -> Status:
        item = self._always_item(t, skill.name)
        problems = tuning.load_problems(text, t.host)
        if problems:
            return Status(item, BROKEN, f"would not load on {t.host.name}: " + "; ".join(problems))
        d = t.skills_dir / skill.name
        rec = receipt.get(item)
        if not _exists(d):
            return Status(item, MISSING, str(d / skill_mod.SKILL_FILE))
        if rec is None:
            return Status(item, BROKEN, f"{d} was not installed by cookr; adopting it moves it aside "
                                        "and uninstall puts it back")
        dest = d / skill_mod.SKILL_FILE
        if not dest.is_file():
            return Status(item, MISSING, str(dest))
        current = dest.read_text(encoding="utf-8")
        if current == text:
            return Status(item, OK, f"{dest} ({t.target})")
        if self._edited(rec):
            return Status(item, DRIFT, f"{dest} was edited since install")
        return Status(item, DRIFT, f"{dest} is out of date ({t.target})")

    def check(self) -> list[Status]:
        receipt = read_receipt(self.root)
        conflict = self._conflict(receipt)
        if conflict:
            return [conflict]
        out = []
        rep = self._set_report() if self.routed or self.targets else None
        if self.routed:
            s = self._set_status(rep)
            out += [s, self._routed_status(rep, s.state, receipt)]
        skill = self._always_on(rep) if self.targets else None
        for t in self.targets if skill else ():
            out.append(self._always_status(t, skill, skill.render(t.chain), receipt))
        return out

    # install -----------------------------------------------------------------

    def install(self, *, adopt: bool = False, force: bool = False, replace: bool = False,
                dry_run: bool = False) -> list[Status]:
        """`force` overwrites an always-on file edited since install;
        `replace` installs a library already installed from other paths."""
        with self._receipt(dry_run) as receipt:
            conflict = self._conflict(receipt)
            if conflict and not replace:
                return [conflict]
            out: list[Status] = []
            rep = self._set_report() if self.routed or self.targets else None
            if self.routed:
                out += self._install_routed(rep, receipt, dry_run)
            skill = self._always_on(rep) if self.targets else None
            planned = set()
            for t in self.targets if skill else ():
                planned.add(self._always_item(t, skill.name))
                out.append(self._install_always(t, skill, receipt, adopt, force, dry_run))
            hosts = {t.host.name for t in self.targets}
            for item, rec in sorted(receipt.items()):  # always-on items no longer built
                if (rec.get("kind") == "always-on" and rec.get("library") == self.source
                        and rec.get("host") in hosts and item not in planned):
                    out.append(self._remove_always(item, rec, receipt, force=False, dry_run=dry_run))
            return out

    def _install_routed(self, rep: skill_mod.SetReport, receipt: dict[str, dict],
                        dry_run: bool) -> list[Status]:
        s = self._set_status(rep)
        r = self._routed_status(rep, s.state, receipt)
        if s.state == BROKEN:
            return [s, r]
        if s.state != OK:
            if dry_run:
                s.action = "would compile"
            else:
                self._set_report(write=True)
                receipt[s.item] = self._record("set", dir=str(self.set_dir))
                s = Status(s.item, OK, str(self.set_dir), "compiled")
        elif not dry_run:
            receipt[s.item] = self._record("set", dir=str(self.set_dir))
        if r.state == OK or (r.state == BROKEN and self.router is None):
            if r.state == OK and not dry_run:
                receipt[r.item] = self._routed_record()
            return [s, r]
        if dry_run:
            r.action = "would register"
            return [s, r]
        try:
            done = self.router.register(self.set_dir, self.source)
        except RouterError as e:
            return [s, Status(r.item, BROKEN, str(e))]
        receipt[r.item] = self._routed_record()
        failed = done.get("failed") or []
        if failed:
            receipt[r.item].pop("digest")  # not all of it is registered: not current
            first = failed[0]
            return [s, Status(r.item, BROKEN, f"{len(failed)} failed to register; "
                                              f"{first.get('path')}: {first.get('error')}")]
        removed = done.get("removed") or []
        detail = f"{len(done.get('registered') or [])} skills" + (f", {len(removed)} removed" if removed else "")
        accepted = sorted({w.removeprefix("accepted ") for w in done.get("warnings") or []})
        if accepted:
            detail += f"; accepted near-duplicate keywords: {'; '.join(accepted)}"
        return [s, Status(r.item, OK, detail, "registered")]

    def _routed_record(self) -> dict:
        return self._record(ROUTED, source=self.source, dir=str(self.set_dir),
                            digest=set_digest(self.set_dir))

    def _install_always(self, t: HostTarget, skill: always_on.AlwaysOn, receipt: dict[str, dict],
                        adopt: bool, force: bool, dry_run: bool) -> Status:
        text = skill.render(t.chain)
        s = self._always_status(t, skill, text, receipt)
        if s.state == OK:
            if not dry_run and self.origin:
                receipt[s.item]["from"] = list(self.origin)
            return s
        if tuning.load_problems(text, t.host):
            return s                                # never written, adopted or not
        d = t.skills_dir / skill.name
        foreign = s.state == BROKEN and s.item not in receipt and _exists(d)
        if s.state == BROKEN and not (foreign and adopt):
            return s
        if s.state == DRIFT and self._edited(receipt.get(s.item)) and not force:
            return Status(s.item, DRIFT, s.detail + "; --force overwrites it")
        backup = receipt.get(s.item, {}).get("backup")
        if foreign:
            backup = str(self.root / "backup" / t.host.name / skill.name)
            if _exists(Path(backup)):
                return Status(s.item, BROKEN, f"cannot adopt {d}: {backup} already exists")
        if dry_run:
            s.action = "would adopt and write" if foreign else "would write"
            return s
        if foreign:
            Path(backup).parent.mkdir(parents=True, exist_ok=True)
            shutil.move(str(d), backup)
        dest = d / skill_mod.SKILL_FILE
        created = receipt.get(s.item, {}).get("created") or _first_missing(t.skills_dir)
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(text, encoding="utf-8")
        receipt[s.item] = self._record("always-on", host=t.host.name, target=t.target, name=skill.name,
                                       path=str(dest), sha256=sha256(text), backup=backup,
                                       created=created)
        return Status(s.item, OK, f"{dest} ({t.target})", "adopted" if foreign else "wrote")

    # uninstall ---------------------------------------------------------------

    def uninstall(self, *, force: bool = False, every_library: bool = False,
                  dry_run: bool = False) -> list[Status]:
        """Remove what the receipt lists for this library (every library's
        with `every_library`), narrowed to this installer's targets; needs no
        cookbook. `force` also removes an always-on file edited since install.
        A set stays while its registration could not be removed."""
        hosts = {t.host.name for t in self.targets}
        out = []
        with self._receipt(dry_run) as receipt:
            still_routed = set()
            for item, rec in sorted(receipt.items(), key=lambda kv: _ORDER.get(kv[1].get("kind"), 9)):
                kind, lib = rec.get("kind"), rec.get("library")
                if not every_library and lib != self.source:
                    continue
                if kind == "always-on" and rec.get("host") in hosts:
                    out.append(self._remove_always(item, rec, receipt, force, dry_run))
                elif kind == ROUTED and self.routed:
                    s = self._remove_routed(item, rec, receipt, dry_run)
                    if s.failed:
                        still_routed.add(lib)
                    out.append(s)
                elif kind == "set" and self.routed:
                    if lib in still_routed:
                        out.append(Status(item, BROKEN, f"kept {rec['dir']}: skill-router still lists "
                                                        "its skills"))
                    else:
                        out.append(self._remove_set(item, rec, receipt, dry_run))
        return out

    def _remove_always(self, item: str, rec: dict, receipt: dict, force: bool, dry_run: bool) -> Status:
        dest = Path(rec["path"])
        if self._edited(rec) and not force:
            return Status(item, DRIFT, f"{dest} was edited since install; --force removes it anyway")
        backup = Path(rec["backup"]) if rec.get("backup") else None
        restore = backup is not None and _exists(backup)
        others = sorted(p.name for p in dest.parent.iterdir() if p != dest) if dest.parent.is_dir() else []
        if restore and others:
            return Status(item, BROKEN, f"cannot restore {backup}: {dest.parent} also holds "
                                        f"{', '.join(others)}, which cookr did not write")
        if dry_run:
            return Status(item, OK, str(dest), "would remove" + (" and restore the original" if restore else ""))
        if dest.is_file():
            dest.unlink()
        created = rec.get("created")
        _prune_empty(dest.parent, Path(created).parent if created else dest.parent.parent)
        action = "removed"
        if restore:
            dest.parent.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(str(backup), str(dest.parent))
            _prune_empty(backup.parent, self.root)
            action = "removed, original restored"
        elif backup is not None:
            action = f"removed; the original was not at {backup} to restore"
        del receipt[item]
        return Status(item, OK, str(dest), action)

    def _remove_routed(self, item: str, rec: dict, receipt: dict, dry_run: bool) -> Status:
        if self.router is None:
            return Status(item, BROKEN, f"skill-router-registry not found; set {ROUTER_ENV}")
        source = rec["source"]
        try:
            listed = self.router.listed(source)
            if dry_run:
                return Status(item, OK, f"{len(listed)} skills", "would unregister" if listed else "")
            if listed:
                self.router.unregister(source)
        except RouterError as e:
            return Status(item, BROKEN, str(e))
        del receipt[item]
        return Status(item, OK, f"{len(listed)} skills", "unregistered" if listed else "")

    def _remove_set(self, item: str, rec: dict, receipt: dict, dry_run: bool) -> Status:
        d = Path(rec["dir"])
        old = skill_mod.read_receipt(d)
        if dry_run:
            return Status(item, OK, str(d), f"would remove {len(old)} skills")
        skill_mod.remove_stale(d, old, [])
        for rel in (skill_mod.RECEIPT, skill_mod.TARGETS_FILE):
            if (d / rel).is_file():
                (d / rel).unlink()
        _prune_empty(d, self.root)
        del receipt[item]
        return Status(item, OK, str(d), f"removed {len(old)} skills")


_ORDER = {"always-on": 0, ROUTED: 1, "set": 2}
