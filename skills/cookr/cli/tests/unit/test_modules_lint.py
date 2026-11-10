"""Lint module: Phase A pass/fail; Phase B skipped when claude unavailable."""

from __future__ import annotations

import json
import subprocess

import pytest

from cookr.cli import main
from cookr.modules import lint as lint_mod

from .cookbook_helpers import add_doc


# Every tmp_path here is a git repo, as a real cookbook checkout is.
pytestmark = pytest.mark.usefixtures("git_tmp_path")


def test_lint_green_on_clean_cookbook(tmp_path, monkeypatch, patch_refs):
    monkeypatch.chdir(tmp_path)
    assert main(["create", "--rdid", "testbook"]) == 0
    cb = tmp_path / "cookbook"
    add_doc(tmp_path, "recipes/ok", "# Ok\n")
    assert main(["lint", "-p", str(cb), "--no-llm"]) == 0


def test_lint_phase_a_reports_issues(tmp_path, monkeypatch, patch_refs):
    monkeypatch.chdir(tmp_path)
    assert main(["create", "--rdid", "testbook"]) == 0
    cb = tmp_path / "cookbook"
    (cb / "recipes").mkdir()
    # Recipe with no frontmatter at all.
    (cb / "recipes" / "bad.md").write_text("# Just a header\n", encoding="utf-8")
    # Do NOT run update — leave frontmatter missing so Phase A complains.
    rc = main(["lint", "-p", str(cb), "--no-llm"])
    assert rc != 0


def test_lint_skips_phase_b_when_claude_missing(tmp_path, monkeypatch, patch_refs, capsys):
    monkeypatch.chdir(tmp_path)
    assert main(["create", "--rdid", "testbook"]) == 0
    cb = tmp_path / "cookbook"
    add_doc(tmp_path, "recipes/ok", "# Ok\n")
    monkeypatch.setattr(lint_mod, "claude_available", lambda: False)
    # Without --no-llm, but claude is unavailable: should still exit 0 and warn.
    rc = main(["lint", "-p", str(cb)])
    assert rc == 0


def test_lint_since_and_files_are_mutually_exclusive(tmp_path, monkeypatch, patch_refs):
    monkeypatch.chdir(tmp_path)
    assert main(["create", "--rdid", "testbook"]) == 0
    cb = tmp_path / "cookbook"
    add_doc(tmp_path, "recipes/ok", "# Ok\n")
    monkeypatch.setattr(lint_mod, "claude_available", lambda: True)
    rc = main(["lint", "-p", str(cb), "--since", "HEAD", str(cb / "recipes" / "ok.md")])
    assert rc == 2


def test_lint_since_resolves_changed_files(tmp_path, monkeypatch, patch_refs):
    monkeypatch.chdir(tmp_path)
    assert main(["create", "--rdid", "testbook"]) == 0
    cb = tmp_path / "cookbook"
    add_doc(tmp_path, "recipes/ok", "# Ok\n")

    def _g(*args: str) -> None:
        subprocess.run(["git", *args], cwd=tmp_path, check=True, capture_output=True, text=True)

    _g("init", "-q", "-b", "main")
    _g("config", "user.email", "t@t")
    _g("config", "user.name", "T")
    _g("add", ".")
    _g("commit", "-q", "-m", "seed")
    base = subprocess.run(
        ["git", "rev-parse", "HEAD"], cwd=tmp_path, capture_output=True, text=True, check=True
    ).stdout.strip()
    # Add a file with full frontmatter + commit, so Phase A stays clean and we
    # can prove --since picks up exactly the new file.
    add_doc(tmp_path, "recipes/new", "# New\n", summary="a new one")
    _g("add", "cookbook/recipes/new", "cookbook/recipes/new.md")
    _g("commit", "-q", "-m", "add new")

    captured = []
    monkeypatch.setattr(lint_mod, "claude_available", lambda: True)

    def fake_claude_p(prompt, timeout=600):
        captured.append(prompt)
        from cookr.core.shell import ShellResult
        return ShellResult(0, "ok", "")

    monkeypatch.setattr(lint_mod, "claude_p", fake_claude_p)
    rc = main(["lint", "-p", str(cb), "--since", base])
    assert rc == 0
    # Phase B was scoped to the one changed file.
    assert len(captured) == 1
    assert "recipes/new.md" in captured[0]


def test_lint_since_maps_a_changed_part_to_its_artifact_once(tmp_path, monkeypatch, patch_refs):
    monkeypatch.chdir(tmp_path)
    assert main(["create", "--rdid", "testbook"]) == 0
    cb = tmp_path / "cookbook"
    folder = add_doc(tmp_path, "recipes/ok", "# Ok\n\n## Notes\n\nText.\n")

    def _g(*args: str) -> None:
        subprocess.run(["git", *args], cwd=tmp_path, check=True, capture_output=True, text=True)

    _g("init", "-q", "-b", "main")
    _g("config", "user.email", "t@t")
    _g("config", "user.name", "T")
    _g("add", ".")
    _g("commit", "-q", "-m", "seed")
    base = subprocess.run(["git", "rev-parse", "HEAD"], cwd=tmp_path, capture_output=True,
                          text=True, check=True).stdout.strip()
    # Edit only source parts and the manifest; the compiled doc is untouched.
    parts = sorted(p for p in folder.glob("*.md"))
    assert len(parts) >= 2
    for part in parts:
        part.write_text(part.read_text() + "\nMore.\n")
    manifest = folder / "artifact.json"
    manifest.write_text(manifest.read_text().replace('"summary": "A test artifact."',
                                                       '"summary": "Changed."'))
    _g("add", ".")
    _g("commit", "-q", "-m", "edit parts")

    captured = []
    monkeypatch.setattr(lint_mod, "claude_available", lambda: True)

    def fake_claude_p(prompt, timeout=600):
        captured.append(prompt)
        from cookr.core.shell import ShellResult
        return ShellResult(0, "ok", "")

    monkeypatch.setattr(lint_mod, "claude_p", fake_claude_p)
    main(["lint", "-p", str(cb), "--since", base])
    assert len(captured) == 1
    assert "recipes/ok.md" in captured[0]


# ── a fresh checkout: source folders only, no compiled docs ──────────────────

def _g(root, *args: str) -> str:
    return subprocess.run(["git", *args], cwd=root, check=True, capture_output=True,
                          text=True).stdout.strip()


def _fresh(tmp_path, monkeypatch):
    """A committed cookbook of source folders whose compiled docs are not committed
    (a fresh checkout), with Phase B's claude call recorded."""
    monkeypatch.chdir(tmp_path)
    assert main(["create", "--rdid", "testbook"]) == 0
    cb = tmp_path / "cookbook"
    folders = [add_doc(tmp_path, rel, "# Ok\n\n## Notes\n\nSome text.\n")
               for rel in ("recipes/ok", "recipes/other")]
    for folder in folders:
        folder.with_suffix(".md").unlink()  # compiled docs are never committed
    (cb / "recipes" / "plain.md").write_text("# Plain\n\nNot an artifact.\n", encoding="utf-8")
    _g(tmp_path, "init", "-q", "-b", "main")
    _g(tmp_path, "config", "user.email", "t@t")
    _g(tmp_path, "config", "user.name", "T")
    _g(tmp_path, "add", ".")
    _g(tmp_path, "commit", "-q", "-m", "seed")
    captured: list[str] = []
    monkeypatch.setattr(lint_mod, "claude_available", lambda: True)

    def fake_claude_p(prompt, timeout=600):
        captured.append(prompt)
        from cookr.core.shell import ShellResult
        return ShellResult(0, "ok", "")
    monkeypatch.setattr(lint_mod, "claude_p", fake_claude_p)
    return cb, folders, captured


def test_full_lint_reviews_source_folders_with_no_compiled_doc(tmp_path, monkeypatch, patch_refs):
    cb, folders, captured = _fresh(tmp_path, monkeypatch)
    main(["lint", "-p", str(cb)])
    assert len(captured) == 3
    composed = [p for p in captured if "Some text." in p]
    assert len(composed) == 2  # each folder composed in memory, as compile does
    assert not folders[0].with_suffix(".md").exists()  # nothing written


def test_since_relints_an_artifact_whose_part_was_deleted(tmp_path, monkeypatch, patch_refs):
    cb, folders, captured = _fresh(tmp_path, monkeypatch)
    base = _g(tmp_path, "rev-parse", "HEAD")
    notes = next(p for p in folders[0].glob("*.md") if p.name != "overview.md"
                 and "Some text." in p.read_text())
    _g(tmp_path, "rm", "-q", str(notes))
    manifest = folders[0] / "artifact.json"
    data = json.loads(manifest.read_text(encoding="utf-8"))
    kept = [p for p in data["parts"] if p.get("part") != notes.stem]
    assert len(kept) == len(data["parts"]) - 1
    data["parts"] = kept
    manifest.write_text(json.dumps(data, indent=2), encoding="utf-8")
    _g(tmp_path, "add", "-A")
    _g(tmp_path, "commit", "-q", "-m", "drop a part")
    # The deleted part on its own maps to its artifact, not just the manifest edit.
    assert lint_mod._unit_for(cb.resolve(), notes.resolve()) == folders[0].resolve()
    main(["lint", "-p", str(cb), "--since", base])
    assert len(captured) == 1 and "recipes/ok.md" in captured[0]


def test_since_maps_a_host_addition_to_its_artifact(tmp_path, monkeypatch, patch_refs):
    cb, folders, captured = _fresh(tmp_path, monkeypatch)
    base = _g(tmp_path, "rev-parse", "HEAD")
    hosts = folders[1] / "hosts"
    hosts.mkdir()
    (hosts / "claude.md").write_text("Use the Claude tools.\n", encoding="utf-8")
    _g(tmp_path, "add", "-A")
    _g(tmp_path, "commit", "-q", "-m", "host addition")
    main(["lint", "-p", str(cb), "--since", base])
    assert len(captured) == 1 and "recipes/other.md" in captured[0]
