"""`cookr check [--hook]`: the rules of spec section 7, one test each."""

from __future__ import annotations

import json
import shutil
import subprocess

from cookr.cli import main
from cookr.core.changes import Change
from cookr.core.hookcheck import _version_past, analyze, base_index_at, run
from cookr.core.index import current_index
from cookr.core.links import resolver_for
from cookr.core.repoconfig import load_repo_config

from .cookbook_helpers import SpecDoc, add_spec, edit_repo_config, new_repo, set_implementations

ROOT = {"path": "web", "platform": "web", "kind": "ui", "group": "ui"}
X = "test-repo.ingredient.ui.x"
MISSING = "a0000000-0000-4000-8000-0000000000ff"
FOREIGN = "f0000000-0000-4000-8000-000000000000/a0000000-0000-4000-8000-0000000000aa"
HELP = "Whether and when to do it is your call while you work on these files. (cookr scope shows the full picture.)"
ART = "cookbook/ui/x/artifact.json"
PART = "cookbook/ui/x/spec.md"


def _git(repo, *args):
    return subprocess.run(["git", "-C", str(repo), *args], check=True, capture_output=True)


def _repo(tmp_path, meta=None):
    repo = new_repo(tmp_path / "r", [ROOT])
    (repo / "web" / "x.ts").write_text("export const a = 1\n", encoding="utf-8")
    add_spec(repo, "ui/x", meta={"version": "1.0.0", **(meta or {})},
             impls=[("web", "web/x.ts")])
    return repo


def _init(repo, branch="main"):
    _git(repo, "init", "-q", "-b", branch)
    _git(repo, "config", "user.email", "t@example.com")
    _git(repo, "config", "user.name", "Tester")


def _commit(repo):
    if not (repo / ".git").exists():
        _init(repo)
    _git(repo, "add", "-A")
    _git(repo, "commit", "-q", "-m", "base")


def _confirm(repo):
    assert main(["-p", str(repo), "confirm", X]) == 0


def _check(repo, *changes, base="", ref=None):
    """`ref`: the commit whose index.json is the base index (None: no base index)."""
    cfg = load_repo_config(repo)
    index = current_index(cfg.cookbook_dir)
    base_index = base_index_at(cfg, ref) if ref else None
    return run(cfg, index, resolver_for(cfg, index), list(changes), base, base_index)


def _kinds(findings):
    return [(f.kind, f.subject) for f in findings]


def _strays(repo, n):
    for i in range(n):
        (repo / "web" / f"s{i:02d}.ts").write_text("x\n", encoding="utf-8")


def test_code_change_with_no_recipe_change_is_update(tmp_path):
    repo = _repo(tmp_path)
    _confirm(repo)
    assert _kinds(_check(repo, Change("M", "web/x.ts"))) == [("update", X)]


def test_code_change_with_the_recipe_changed_is_not_update(tmp_path):
    repo = _repo(tmp_path)
    _confirm(repo)
    assert _check(repo, Change("M", "web/x.ts"), Change("M", ART)) == []


def test_index_change_alone_does_not_count_as_a_recipe_change(tmp_path):
    repo = _repo(tmp_path)
    _confirm(repo)
    got = _check(repo, Change("M", "web/x.ts"), Change("M", "cookbook/index.json"))
    assert _kinds(got) == [("update", X)]


def test_a_versions_freeze_does_not_count_as_a_recipe_change(tmp_path):
    repo = _repo(tmp_path)
    _confirm(repo)
    freeze = repo / "cookbook/ui/x/versions/0.9.0"
    freeze.mkdir(parents=True)
    (freeze / "artifact.json").write_text("{}", encoding="utf-8")
    got = _check(repo, Change("M", "web/x.ts"),
                 Change("A", "cookbook/ui/x/versions/0.9.0/artifact.json"))
    assert _kinds(got) == [("update", X)]


def test_uncovered_added_or_modified_file_is_create(tmp_path):
    repo = _repo(tmp_path)
    (repo / "web" / "stray.ts").write_text("x\n", encoding="utf-8")
    got = _check(repo, Change("A", "web/stray.ts"), Change("M", "web/stray.ts"),
                 Change("A", "outside/readme.txt"))
    assert _kinds(got) == [("create", "web/stray.ts")]


def test_ignored_and_out_of_root_files_are_not_create(tmp_path):
    repo = _repo(tmp_path)
    edit_repo_config(repo, lambda d: d.__setitem__("ignore", ["**/*.snap"]))
    assert _check(repo, Change("A", "web/a.snap"), Change("A", "elsewhere/b.ts")) == []


def test_deleted_covered_file_is_update_and_deleted_uncovered_is_nothing(tmp_path):
    repo = _repo(tmp_path)
    _confirm(repo)
    (repo / "web" / "x.ts").unlink()
    got = _check(repo, Change("D", "web/x.ts"), Change("D", "web/never-covered.ts"))
    assert _kinds(got) == [("update", X)]


def test_absorbed_pure_rename_is_nothing(tmp_path):
    repo = _repo(tmp_path)
    _confirm(repo)
    (repo / "web" / "x.ts").rename(repo / "web" / "y.ts")
    set_implementations(repo, "ui/x", [("web", "web/y.ts", "confirmed")])
    assert _check(repo, Change("R", "web/y.ts", "web/x.ts"),
                  Change("M", "cookbook/index.json")) == []


def test_rename_inside_a_directory_row_is_nothing(tmp_path):
    repo = new_repo(tmp_path / "r", [ROOT])
    (repo / "web" / "d").mkdir()
    (repo / "web" / "d" / "b.ts").write_text("x\n", encoding="utf-8")
    add_spec(repo, "ui/x", impls=[("web", "web/d/")])
    assert _check(repo, Change("R", "web/d/b.ts", "web/d/a.ts")) == []


def test_unabsorbed_rename_is_update_plus_create(tmp_path):
    repo = _repo(tmp_path)
    _confirm(repo)
    (repo / "web" / "x.ts").rename(repo / "web" / "y.ts")
    got = _check(repo, Change("R", "web/y.ts", "web/x.ts"))
    assert _kinds(got) == [("update", X), ("create", "web/y.ts")]


def test_touched_implementation_not_confirmed_is_validate(tmp_path):
    repo = _repo(tmp_path)                      # unverified
    got = _check(repo, Change("M", "web/x.ts"), Change("M", ART))
    assert [f.kind for f in got] == ["validate"]
    assert f"validate {X} against 1.0.0" in got[0].message


def test_confirmed_with_unchanged_code_needs_no_validate(tmp_path):
    repo = _repo(tmp_path)
    _confirm(repo)
    assert _check(repo, Change("M", "web/x.ts"), Change("M", ART)) == []


def test_code_edited_after_confirm_is_validate(tmp_path):
    repo = _repo(tmp_path)
    _confirm(repo)
    (repo / "web" / "x.ts").write_text("export const a = 2\n", encoding="utf-8")
    assert _kinds(_check(repo, Change("M", "web/x.ts"), Change("M", PART))) == [("validate", X)]


def test_validate_names_the_diff_from_the_confirmed_version(tmp_path):
    repo = _repo(tmp_path)
    _confirm(repo)
    doc = SpecDoc(repo, "ui/x")
    doc.write_text(doc.read_text().replace("version: 1.0.0", "version: 1.1.0"))
    got = _check(repo, Change("M", "web/x.ts"), Change("M", ART))
    assert [f.kind for f in got] == ["validate"]
    assert f"cookr diff {X} 1.0.0" in got[0].message
    assert "against 1.1.0" in got[0].message


def test_patch_behind_is_still_confirmed(tmp_path):
    repo = _repo(tmp_path)
    _confirm(repo)
    doc = SpecDoc(repo, "ui/x")
    doc.write_text(doc.read_text().replace("version: 1.0.0", "version: 1.0.1"))
    assert _check(repo, Change("M", "web/x.ts"), Change("M", ART)) == []


def test_an_untouched_stale_implementation_never_blocks(tmp_path):
    repo = _repo(tmp_path)                      # unverified, but nothing touched it
    assert _check(repo, Change("M", "README.md")) == []


def test_missing_and_malformed_dependencies_are_findings(tmp_path):
    repo = _repo(tmp_path, {"depends-on": [MISSING, "not-a-link"]})
    got = _check(repo, Change("M", ART))
    assert [f.kind for f in got] == ["dependency", "dependency"]
    assert {f.message for f in got} == {
        f"create or fix dependency {MISSING} of {X} (missing)",
        f"create or fix dependency not-a-link of {X} (unresolvable)"}


def test_unreachable_dependency_is_a_warning_not_a_finding(tmp_path):
    repo = _repo(tmp_path, {"depends-on": [FOREIGN]})
    cfg = load_repo_config(repo)
    index = current_index(cfg.cookbook_dir)
    result = analyze(cfg, index, resolver_for(cfg, index), [Change("M", ART)], "")
    assert result.findings == []
    assert len(result.unreachable) == 1 and FOREIGN in result.unreachable[0]


def test_dependencies_of_an_untouched_artifact_are_not_checked(tmp_path):
    repo = _repo(tmp_path, {"depends-on": [MISSING]})
    assert _check(repo, Change("M", "README.md")) == []


def test_content_changed_with_the_same_version_is_bump(tmp_path):
    repo = _repo(tmp_path)
    _commit(repo)
    base = _git(repo, "rev-parse", "HEAD").stdout.decode().strip()
    doc = SpecDoc(repo, "ui/x")
    doc.write_text(doc.read_text().replace("Text.", "Other text."))
    assert _kinds(_check(repo, Change("M", PART), base=base)) == [("bump", X)]
    assert _check(repo, Change("M", PART), base="") == []        # no base: skipped
    doc.write_text(doc.read_text().replace("version: 1.0.0", "version: 1.0.1"))
    assert _check(repo, Change("M", PART), base=base) == []


def test_a_new_artifact_needs_no_bump(tmp_path):
    repo = _repo(tmp_path)
    _commit(repo)
    base = _git(repo, "rev-parse", "HEAD").stdout.decode().strip()
    add_spec(repo, "ui/fresh", meta={"version": "1.0.0"})
    assert _check(repo, Change("A", "cookbook/ui/fresh/artifact.json"), base=base) == []


def test_findings_are_deduplicated_and_ordered(tmp_path):
    repo = new_repo(tmp_path / "r", [ROOT])
    for n in range(5):
        (repo / "web" / f"f{n}.ts").write_text("x\n", encoding="utf-8")
    add_spec(repo, "ui/x", impls=[("web", f"web/f{n}.ts") for n in range(5)])
    (repo / "web" / "stray.ts").write_text("x\n", encoding="utf-8")
    got = _check(repo, Change("M", "web/stray.ts"),
                 *(Change("M", f"web/f{n}.ts") for n in range(5)))
    assert _kinds(got) == [("update", X), ("create", "web/stray.ts"), ("validate", X)]


# --- the command ----------------------------------------------------------------


def test_hook_output_capped_at_15(tmp_path, capsys):
    repo = _repo(tmp_path)
    _confirm(repo)
    _commit(repo)
    _strays(repo, 20)
    capsys.readouterr()
    assert main(["-p", str(repo), "check", "--hook"]) == 2
    lines = capsys.readouterr().err.splitlines()
    assert lines[0] == "cookr: recipe work this change may owe:"
    assert len([ln for ln in lines if ln.startswith("  - ")]) == 15
    assert lines[16] == "  … and 5 more"
    assert lines[-1] == HELP and len(lines) == 18


def test_hook_silent_when_clean(tmp_path, capsys):
    repo = _repo(tmp_path)
    _confirm(repo)
    _commit(repo)
    capsys.readouterr()
    assert main(["-p", str(repo), "check", "--hook"]) == 0
    assert capsys.readouterr().err == ""


def test_hook_outside_a_cookr_repo_is_silent(tmp_path, capsys):
    assert main(["check", "--hook"]) == 0
    assert capsys.readouterr().err == ""


def test_hook_git_failure_blocks(tmp_path, capsys):
    repo = _repo(tmp_path)                      # not a git repo
    capsys.readouterr()
    assert main(["-p", str(repo), "check", "--hook"]) == 2
    assert capsys.readouterr().err.startswith("cookr: git failed")


def test_staged_mode_checks_only_the_staged_set(tmp_path, capsys):
    repo = _repo(tmp_path)
    _confirm(repo)
    _commit(repo)
    _strays(repo, 2)
    _git(repo, "add", "web/s00.ts")
    capsys.readouterr()
    assert main(["-p", str(repo), "check", "--staged", "--hook"]) == 2
    out = capsys.readouterr().err
    assert "web/s00.ts" in out and "web/s01.ts" not in out


def test_branch_diff_sees_committed_work_since_the_base(tmp_path, capsys):
    repo = _repo(tmp_path)
    _confirm(repo)
    _commit(repo)
    _git(repo, "checkout", "-q", "-b", "work")
    _strays(repo, 1)
    _git(repo, "add", "-A")
    _git(repo, "commit", "-q", "-m", "work")
    capsys.readouterr()
    assert main(["-p", str(repo), "check", "--hook"]) == 2
    assert "web/s00.ts" in capsys.readouterr().err


def test_no_base_checks_uncommitted_work_and_warns_outside_hook_mode(tmp_path, capsys):
    repo = _repo(tmp_path)
    _confirm(repo)
    _init(repo, "trunk")                        # no origin/main or main: no base
    _git(repo, "add", "-A")
    _git(repo, "commit", "-q", "-m", "base")
    doc = SpecDoc(repo, "ui/x")
    doc.write_text(doc.read_text().replace("Text.", "Other text."))   # would need a bump
    _strays(repo, 1)
    capsys.readouterr()
    assert main(["-p", str(repo), "check"]) == 1
    out = capsys.readouterr().out
    assert "version bumps were not checked" in " ".join(out.split())
    assert "web/s00.ts" in out and "bump" not in out.replace("version bumps", "")
    assert main(["-p", str(repo), "check", "--hook"]) == 2
    out = capsys.readouterr().err
    assert "web/s00.ts" in out and "bump" not in out


def test_plain_check_prints_a_table_and_exits_1_or_0(tmp_path, capsys):
    repo = _repo(tmp_path)
    _confirm(repo)
    _commit(repo)
    capsys.readouterr()
    assert main(["-p", str(repo), "check"]) == 0
    _strays(repo, 1)
    capsys.readouterr()
    assert main(["-p", str(repo), "check"]) == 1
    assert "create" in capsys.readouterr().out


def test_json_emits_the_findings(tmp_path, capsys):
    repo = _repo(tmp_path)
    _confirm(repo)
    _commit(repo)
    _strays(repo, 1)
    capsys.readouterr()
    assert main(["-p", str(repo), "check", "--json"]) == 1
    data = json.loads(capsys.readouterr().out)
    assert [(d["kind"], d["subject"]) for d in data] == [("create", "web/s00.ts")]


# --- fix round 1 ------------------------------------------------------------------


def test_delete_with_the_row_removed_is_still_update(tmp_path):
    repo = _repo(tmp_path)
    _confirm(repo)
    _commit(repo)
    (repo / "web" / "x.ts").unlink()
    set_implementations(repo, "ui/x", [])
    assert _check(repo, Change("D", "web/x.ts"), Change("M", "cookbook/index.json")) == []
    got = _check(repo, Change("D", "web/x.ts"), Change("M", "cookbook/index.json"), ref="HEAD")
    assert _kinds(got) == [("update", X)]


def test_a_deleted_artifact_folder_gives_no_false_update(tmp_path):
    repo = _repo(tmp_path)
    _confirm(repo)
    _commit(repo)
    (repo / "web" / "x.ts").unlink()
    shutil.rmtree(repo / "cookbook" / "ui" / "x")
    got = _check(repo, Change("D", "web/x.ts"), Change("D", ART), Change("D", PART),
                 Change("M", "cookbook/index.json"), ref="HEAD")
    assert got == []


def test_a_claimed_row_on_an_unchanged_file_is_validate(tmp_path):
    repo = _repo(tmp_path)
    (repo / "web" / "y.ts").write_text("export {}\n", encoding="utf-8")
    _commit(repo)
    set_implementations(repo, "ui/x", [("web", "web/x.ts"), ("web", "web/y.ts")])
    got = _check(repo, Change("M", "cookbook/index.json"), ref="HEAD")
    assert _kinds(got) == [("validate", X)]
    assert _check(repo, Change("M", "cookbook/index.json")) == []     # no base index: not seen


def test_a_guideline_owner_gives_no_finding(tmp_path):
    repo = new_repo(tmp_path / "r", [ROOT])
    (repo / "web" / "g.ts").write_text("x\n", encoding="utf-8")
    add_spec(repo, "ui/g", type="guideline", impls=[("web", "web/g.ts")])
    _commit(repo)
    assert _check(repo, Change("M", "web/g.ts"), Change("D", "web/g.ts"), ref="HEAD") == []
    set_implementations(repo, "ui/g", [("web", "web/g.ts"), ("web", "web/h.ts")])
    assert _check(repo, Change("M", "cookbook/index.json"), ref="HEAD") == []


def test_base_index_falls_back_when_missing_or_unusable(tmp_path):
    repo = _repo(tmp_path)
    cfg = load_repo_config(repo)
    assert base_index_at(cfg, "") is None
    _git(repo, "init", "-q", "-b", "main")
    assert base_index_at(cfg, "HEAD") is None                          # unborn HEAD
    (repo / "cookbook" / "index.json").write_text('{"format": 1}', encoding="utf-8")
    _commit(repo)
    assert base_index_at(cfg, "HEAD") is None                          # not format 2
    (repo / "cookbook" / "index.json").write_text("{nope", encoding="utf-8")
    _git(repo, "commit", "-qam", "bad")
    assert base_index_at(cfg, "HEAD") is None


def test_staged_check_refuses_a_path_that_differs_from_the_working_tree(tmp_path, capsys):
    repo = _repo(tmp_path)
    _confirm(repo)
    _commit(repo)
    (repo / "web" / "x.ts").write_text("export const a = 2\n", encoding="utf-8")
    _git(repo, "add", "web/x.ts")
    (repo / "web" / "x.ts").write_text("export const a = 3\n", encoding="utf-8")   # unstaged
    capsys.readouterr()
    assert main(["-p", str(repo), "check", "--staged", "--hook"]) == 2
    lines = capsys.readouterr().err.splitlines()
    assert lines[1] == "  - stage or revert web/x.ts first"        # the stage kind sorts first
    assert any("update" in ln for ln in lines)


def test_staged_check_is_clean_when_staged_equals_the_working_tree(tmp_path, capsys):
    repo = _repo(tmp_path)
    _confirm(repo)
    _commit(repo)
    capsys.readouterr()
    assert main(["-p", str(repo), "check", "--staged", "--hook"]) == 0


def test_version_past_with_an_unset_or_unparseable_base():
    assert _version_past("1.0.0", "")
    assert _version_past("1.0.0", "junk")
    assert not _version_past("", "1.0.0")
    assert not _version_past("junk", "")
    assert not _version_past("1.0.0", "1.0.0")
    assert _version_past("1.0.1", "1.0.0")
