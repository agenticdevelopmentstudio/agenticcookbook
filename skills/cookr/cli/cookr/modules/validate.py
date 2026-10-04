"""`cookr validate` — read-only Phase A checks + index drift detection."""

from __future__ import annotations

from pathlib import Path

from ..core import hosts, neutrality, payload, tuning
from ..core.artifact import ArtifactError, find_folders, load_folder
from ..core.artifact_build import compile_doc, unconverted_results
from ..core.checks import fix_for, phase_a
from ..core.errors import NoCookbookRootError
from ..core.skill import templates_root
from ..indexing import engine

NAME = "validate"
HELP = "Read-only validation: frontmatter + link checks + index drift."

_DRIFT_FIX = "Run `cookr update` to regenerate this index."
_MISSING_FIX = "Run `cookr update` to create this index."
_COMPILE_FIX = ("Edited the folder: run `cookr compile`. "
                "Edited the .md: run `cookr convert --update <doc>` to fold it into the folder.")


def register(parser) -> None:
    pass


def _drift(root: Path, configs_dir: Path, ui) -> int:
    if not configs_dir.is_dir():
        ui.warn(f"No index configs found at {configs_dir}; skipping drift checks.")
        return 0
    configs = engine.load_configs(configs_dir)
    if not configs:
        return 0

    drift_found = 0
    rows = []
    for c in configs:
        ok, reason = engine._applies(c.get("applies_when"), root)
        if not ok:
            rows.append([c.get("name", "?"), c["strategy"], "n/a", reason])
            continue
        text, _ = engine.render(c, root)
        out = root / c["output"]
        if not out.exists():
            rows.append([c.get("name", "?"), c["strategy"], "missing", str(out.relative_to(root))])
            drift_found += 1
            continue
        existing = out.read_text(encoding="utf-8")
        if existing.strip() != text.strip():
            rows.append([c.get("name", "?"), c["strategy"], "drift", str(out.relative_to(root))])
            drift_found += 1
        else:
            rows.append([c.get("name", "?"), c["strategy"], "ok", str(out.relative_to(root))])

    ui.table(["config", "strategy", "result", "output"], rows)
    if drift_found:
        ui.info(f"Fix: {_DRIFT_FIX}")
    return 1 if drift_found else 0


def run(args, ctx) -> int:
    if ctx.cookbook_root is None:
        raise NoCookbookRootError(
            "Could not find a cookbook root. Run from inside a cookbook dir, or pass -p."
        )
    root = ctx.cookbook_root
    ctx.ui.title(f"cookr validate · {root}")

    ctx.ui.section("Frontmatter & links")
    report = phase_a(root)
    if report.ok:
        ctx.ui.ok(f"All {report.files_checked} artifacts passed deterministic checks.")
        a_exit = 0
    else:
        rows = [[i.file, i.rule, i.detail, fix_for(i.rule)] for i in report.issues]
        ctx.ui.table(["file", "rule", "issue", "fix"], rows)
        ctx.ui.error(f"{len(report.issues)} issue(s) across {report.files_checked} files.")
        a_exit = 1

    ctx.ui.section("Index drift")
    b_exit = _drift(root, ctx.references_dir / "index-configs", ctx.ui)

    ctx.ui.section("Compiled docs")
    c_exit = _compiled(root, ctx.ui)

    folders = find_folders([root])
    ctx.ui.section("Neutrality")
    d_exit = _neutral(root, folders, ctx.ui)

    ctx.ui.section("Host additions")
    e_exit = _additions(root, folders, ctx.ui)

    ctx.ui.blank()
    failed = a_exit or b_exit or c_exit or d_exit or e_exit
    if failed:
        ctx.ui.error("Validation failed.")
    else:
        ctx.ui.ok("Validation passed.")
    return failed


def _compiled(root: Path, ui) -> int:
    """Every source folder's doc exists and matches what the folder compiles to.
    A doc edited by hand, not through its folder, shows here as stale."""
    folders = find_folders([root])
    stray = unconverted_results([root])
    if not folders and not stray:
        ui.info("No artifact source folders.")
        return 0
    results = compile_doc(folders, base=root, write=False)
    bad = ([[str(r.source.relative_to(root)), r.status, r.detail] for r in stray]
           + [[str(r.dest.relative_to(root)), r.status, r.detail] for r in results if r.failed])
    if not bad:
        ui.ok(f"All {len(results)} compiled docs match their source folders.")
        return 0
    ui.table(["doc", "result", "detail"], bad)
    ui.info(f"Fix: {_COMPILE_FIX}")
    return 1


def _neutral(root: Path, folders: list[Path], ui) -> int:
    """Shared text names no host or model unless the artifact says why."""
    findings = neutrality.census(folders)
    if not findings:
        listed = sum(1 for f in folders if _reason(f) is not None)
        ui.ok(f"No artifact names a host without saying why ({listed} say why).")
        return 0
    ui.table(["artifact", "finding", "names", "fix"],
             [[str(f.folder.relative_to(root)), f.kind, ", ".join(f.words), neutrality.FIX[f.kind]]
              for f in findings])
    return 1


def _reason(folder: Path):
    try:
        return load_folder(folder).names_hosts
    except ArtifactError:
        return None


def _additions(root: Path, folders: list[Path], ui) -> int:
    """The templates' and each artifact's hosts/ additions apply cleanly;
    stamped ones written against an older source are reported, not fatal."""
    declared = hosts.manifest()
    problems, stale, count = [], [], 0

    def where(path: Path) -> str:
        return str(path.relative_to(root)) if path.is_relative_to(root) else str(path)

    t = templates_root(root)
    levels = payload.template_levels(t / "skill", t / "always") + [payload.artifact_level(f) for f in folders]
    for lv in levels:
        name = where(lv.source_path) if lv.kind == payload.ARTIFACT else lv.name
        try:
            adds = lv.additions()
            current = tuning.source_hash(lv.source())
        except (tuning.TuningError, ArtifactError) as e:
            problems.append([name, str(e)])
            continue
        count += len(adds)
        problems += [[name, p] for p in tuning.addition_problems(adds, declared)]
        stale += [[where(a.path) if lv.kind == payload.ARTIFACT else f"{lv.name}/{a.path.name}", a.stamp[:12]]
                  for a in tuning.stale(adds, current)]
    if stale:
        ui.table(["addition", "written against"], stale)
        ui.warn(f"{len(stale)} addition(s) were written against an older source; re-tune them.")
    if problems:
        ui.table(["artifact", "problem"], problems)
        return 1
    if not stale:
        ui.ok(f"{count} host addition(s), all current.")
    return 0
