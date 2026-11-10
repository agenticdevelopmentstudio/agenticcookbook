"""In-source versions: requirement diffs, level-proposing `bump`, the `versions/` freeze, `diff`."""

from __future__ import annotations

import json
import subprocess

from cookr.cli import main
from cookr.core.artifact import find_documents, find_folders
from cookr.core.markdown import iter_markdown
from cookr.core.versions import RequirementDiff, diff, propose_level, requirements

from .cookbook_helpers import add_spec, new_repo

BODY = """# Spec

## Requirements

- **keep-a**: The widget MUST do A.
- **keep-b**: The widget MUST do B.

## Change History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 1.0.0 | 2026-01-01 | A | first |
"""
META = {"version": "1.0.0", "modified": "2026-01-01", "title": "Spec"}
ARGS = ["--summary", "Changed it", "--author", "Tester", "--date", "2026-09-25"]


def _git(repo, *args):
    subprocess.run(["git", "-C", str(repo), *args], check=True, capture_output=True)


def _repo(tmp_path):
    """A cookbook with one committed ingredient on main, then a feature branch."""
    repo = new_repo(tmp_path / "r")
    uid = add_spec(repo, "ui/x", meta=dict(META), body=BODY)
    _git(repo, "init", "-q", "-b", "main")
    _git(repo, "config", "user.email", "t@example.com")
    _git(repo, "config", "user.name", "Tester")
    _git(repo, "add", "-A")
    _git(repo, "commit", "-q", "-m", "base")
    _git(repo, "checkout", "-q", "-b", "feat")
    return repo, repo / "cookbook" / "ui" / "x", uid


def _edit(folder, old, new):
    part = folder / "requirements.md"
    part.write_text(part.read_text(encoding="utf-8").replace(old, new), encoding="utf-8")


def _bump(folder, *extra):
    return main(["bump", str(folder), *ARGS, *extra])


def _manifest(folder):
    return json.loads((folder / "artifact.json").read_text(encoding="utf-8"))


def test_requirements_parsed_outside_fences():
    text = (
        "- **a-one**: First   thing\n"
        "* **b-two**: Second\n"
        "  **c-3**:  Third\n"
        "```\n- **fenced**: not a requirement\n```\n"
        "~~~\n- **tilde-fenced**: not a requirement\n~~~\n"
        "**Not Kebab**: nope\n"
        "plain **bold**: text\n"
    )
    assert requirements(text) == {"a-one": "First thing", "b-two": "Second", "c-3": "Third"}


def test_a_requirement_may_carry_a_variant_tag_which_is_part_of_its_text():
    text = (
        "- **hide-on-close-unmount** (full-featured): Content MUST unmount.\n"
        "- **plain**  (lightweight)  :  Stays.\n"
        "- **not-a-tag** (unclosed: nope\n"
    )
    assert requirements(text) == {
        "hide-on-close-unmount": "(full-featured) Content MUST unmount.",
        "plain": "(lightweight) Stays.",
    }
    # changing only the tag changes the requirement
    old = "- **x** (a): Same.\n"
    assert diff(old, "- **x** (b): Same.\n").changed == ["x"]


def test_propose_level_rules():
    assert propose_level(RequirementDiff(changed=["a"]), True) == "major"
    assert propose_level(RequirementDiff(removed=["a"], added=["b"]), True) == "major"
    assert propose_level(RequirementDiff(added=["b"]), True) == "minor"
    assert propose_level(RequirementDiff(), True) == "patch"
    assert propose_level(RequirementDiff(), False) == "none"
    d = diff("- **a-a**: x\n- **b-b**: y\n", "- **a-a**: x2\n- **c-c**: z\n")
    assert (d.added, d.changed, d.removed) == (["c-c"], ["a-a"], ["b-b"])


def test_bump_freezes_base_version(tmp_path):
    repo, folder, _ = _repo(tmp_path)
    before = {n: (folder / n).read_bytes() for n in ("artifact.json", "requirements.md")}
    _edit(folder, "MUST do A.", "MUST do A, always.")           # a requirement changed: major
    assert _bump(folder) == 0
    assert _manifest(folder)["meta"]["version"] == "2.0.0"
    frozen = folder / "versions" / "1.0.0"
    assert {n: (frozen / n).read_bytes() for n in before} == before   # byte for byte
    assert not (folder / "versions" / "2.0.0").exists()
    assert "MUST do A, always." in (folder / "requirements.md").read_text(encoding="utf-8")


def test_second_bump_same_level_is_noop(tmp_path):
    repo, folder, _ = _repo(tmp_path)
    _edit(folder, "MUST do B.", "MUST do B well.")              # major
    assert _bump(folder) == 0
    snapshot = {p.name: p.read_bytes() for p in folder.iterdir() if p.is_file()}
    assert _bump(folder, "--level", "minor") == 0                # lower than major
    assert _bump(folder) == 0                                    # same proposal
    assert {p.name: p.read_bytes() for p in folder.iterdir() if p.is_file()} == snapshot
    assert _manifest(folder)["meta"]["version"] == "2.0.0"


def test_second_bump_higher_level_relevels(tmp_path):
    repo, folder, _ = _repo(tmp_path)
    (folder / "intro.md").write_text("# Spec, reworded\n\n", encoding="utf-8")   # wording: patch
    assert _bump(folder) == 0
    assert _manifest(folder)["meta"]["version"] == "1.0.1"
    _edit(folder, "MUST do B.\n", "MUST do B.\n- **new-c**: The widget MUST do C.\n")   # added: minor
    assert _bump(folder) == 0
    assert _manifest(folder)["meta"]["version"] == "1.1.0"
    text = (folder / "history.md").read_text(encoding="utf-8")
    assert text.count("| 1.1.0 |") == 1 and "| 1.0.1 |" not in text and "| 1.0.0 |" in text
    assert (folder / "versions" / "1.0.0").is_dir()
    assert not (folder / "versions" / "1.0.1").exists()


def test_new_artifact_freezes_nothing(tmp_path):
    repo, folder, _ = _repo(tmp_path)
    add_spec(repo, "ui/y", meta=dict(META), body=BODY)
    other = repo / "cookbook" / "ui" / "y"
    assert _bump(other) == 0
    assert _manifest(other)["meta"]["version"] == "1.0.1"
    assert not (other / "versions").exists()


def test_freeze_conflict_is_refused_and_writes_nothing(tmp_path, capsys):
    repo, folder, _ = _repo(tmp_path)
    (folder / "versions" / "1.0.0").mkdir(parents=True)
    (folder / "versions" / "1.0.0" / "artifact.json").write_text("{}", encoding="utf-8")
    _edit(folder, "MUST do B.", "MUST do B well.")
    assert _bump(folder) == 1
    assert _manifest(folder)["meta"]["version"] == "1.0.0"
    assert "already exists" in capsys.readouterr().out.replace("\n", " ")


def test_nothing_changed_proposes_nothing(tmp_path):
    repo, folder, _ = _repo(tmp_path)
    assert _bump(folder) == 0
    assert _manifest(folder)["meta"]["version"] == "1.0.0"
    assert not (folder / "versions").exists()


def test_versions_dir_not_compiled(tmp_path):
    repo, folder, _ = _repo(tmp_path)
    _edit(folder, "MUST do A.", "MUST do A, always.")
    assert _bump(folder) == 0
    assert (folder / "versions" / "1.0.0" / "requirements.md").is_file()
    cb = repo / "cookbook"
    assert find_folders([cb]) == [folder]
    assert all("versions" not in p.parts for p in find_documents([cb]))
    assert all("versions" not in p.parts for p in iter_markdown(cb))
    out = tmp_path / "out"
    assert main(["compile", str(folder), "--out", str(out)]) == 0
    compiled = "".join(p.read_text(encoding="utf-8") for p in out.rglob("*.md"))
    assert "MUST do A, always." in compiled and "MUST do A.\n" not in compiled


def test_diff_between_versions(tmp_path, capsys):
    repo, folder, uid = _repo(tmp_path)
    _edit(folder, "MUST do B.\n", "MUST do B.\n- **new-c**: The widget MUST do C.\n")
    _edit(folder, "- **keep-a**: The widget MUST do A.\n", "")
    assert _bump(folder) == 0
    capsys.readouterr()
    assert main(["-p", str(repo), "diff", uid, "1.0.0"]) == 0
    out = capsys.readouterr().out
    assert "added" in out and "new-c" in out and "removed" in out and "keep-a" in out
    assert "keep-b" not in out
    assert main(["-p", str(repo), "diff", uid, "1.0.0", "2.0.0"]) == 0
    capsys.readouterr()
    assert main(["-p", str(repo), "diff", uid, "1.0.0", "1.0.0"]) == 0
    assert "No requirement differs" in capsys.readouterr().out
    assert main(["-p", str(repo), "diff", uid, "9.9.9"]) == 1
    assert "1.0.0" in capsys.readouterr().out


def test_replace_newest_row_keeps_every_other_byte():
    import pytest
    from cookr.core import history
    text = ("## Change History\n\n| Version | Date | Author | Summary |\n|---|---|---|---|\r\n"
            "| 1.1.0 | d | a | two |\r\n| 1.0.0 | d | a | one |\n")
    table = history.read(text)
    out = history.replace_newest_row(table, (2, 0, 0), ("2.0.0", "d2", "b", "re"))
    assert out == text.replace("| 1.1.0 | d | a | two |", "| 2.0.0 | d2 | b | re |")
    with pytest.raises(history.HistoryError):
        history.replace_newest_row(table, (2, 0, 0), ("2.1.0", "d", "a", "x"))


def test_cookbook_freeze_is_not_inventoried_or_hashed_but_code_named_versions_is(tmp_path):
    from cookr.core.conformance import location_hash
    from cookr.core.inventory import _walk, ignore_set
    none = ignore_set(())
    (tmp_path / "web" / "ui" / "versions" / "1.0.0").mkdir(parents=True)
    (tmp_path / "web" / "ui" / "artifact.json").write_text("{}", encoding="utf-8")
    (tmp_path / "web" / "ui" / "b.ts").write_text("export {}\n", encoding="utf-8")
    (tmp_path / "web" / "versions").mkdir()
    (tmp_path / "web" / "versions" / "c.ts").write_text("export {}\n", encoding="utf-8")
    before = location_hash(tmp_path, "web/ui/", none)
    (tmp_path / "web" / "ui" / "versions" / "1.0.0" / "a.ts").write_text("x\n", encoding="utf-8")
    assert location_hash(tmp_path, "web/ui/", none) == before
    seen = set(_walk(tmp_path, "web", none))
    assert seen == {"web/ui/b.ts", "web/versions/c.ts"}
    assert location_hash(tmp_path, "web/versions/", none) != location_hash(tmp_path, "web/nothing/", none)


def test_no_base_branch_warns_and_bumps_from_current(tmp_path, capsys):
    repo, folder, _ = _repo(tmp_path)
    _git(repo, "branch", "-m", "main", "trunk")                 # no origin/main, no main
    (folder / "intro.md").write_text("# Spec, reworded\n\n", encoding="utf-8")
    assert _bump(folder) == 0
    out = " ".join(capsys.readouterr().out.split())
    assert "no base branch found (origin/main, main)" in out
    assert "current version 1.0.0, level patch, nothing frozen" in out
    assert _manifest(folder)["meta"]["version"] == "1.0.1"
    assert not (folder / "versions").exists()


def test_git_failure_is_an_error_not_a_new_artifact(tmp_path, capsys, monkeypatch):
    from cookr.core import versions
    repo, folder, _ = _repo(tmp_path)
    _edit(folder, "MUST do A.", "MUST do A, always.")
    real = versions._run

    def failing(root, *args):
        return (128, b"", "fatal: object database is corrupt") if args[0] == "ls-tree" else real(root, *args)

    monkeypatch.setattr(versions, "_run", failing)
    assert _bump(folder) == 1
    assert "corrupt" in " ".join(capsys.readouterr().out.split())
    assert _manifest(folder)["meta"]["version"] == "1.0.0"
    assert not (folder / "versions").exists()


def test_not_a_repo_is_an_error(tmp_path, capsys):
    repo = new_repo(tmp_path / "plain")
    add_spec(repo, "ui/x", meta=dict(META), body=BODY)
    folder = repo / "cookbook" / "ui" / "x"
    assert _bump(folder) == 1
    assert "git failed" in " ".join(capsys.readouterr().out.split())
    assert _manifest(folder)["meta"]["version"] == "1.0.0"


def test_versions_is_not_a_spec_name():
    from cookr.core.markdown import reserved_name
    assert "versions" in reserved_name("ui/versions")
