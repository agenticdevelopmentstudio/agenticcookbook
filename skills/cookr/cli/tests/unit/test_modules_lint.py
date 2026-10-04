"""Lint module: Phase A pass/fail; Phase B skipped when claude unavailable."""

from __future__ import annotations

import pytest

import subprocess

from cookr.cli import main
from cookr.modules import lint as lint_mod


# Every tmp_path here is a git repo, as a real cookbook checkout is.
pytestmark = pytest.mark.usefixtures("git_tmp_path")


def test_lint_green_on_clean_cookbook(tmp_path, monkeypatch, patch_refs):
    monkeypatch.chdir(tmp_path)
    assert main(["create"]) == 0
    cb = tmp_path / "cookbook"
    (cb / "recipes" / "ok.md").write_text("# Ok\n", encoding="utf-8")
    assert main(["update", "-p", str(cb), "--author", "T"]) == 0
    assert main(["lint", "-p", str(cb), "--no-llm"]) == 0


def test_lint_phase_a_reports_issues(tmp_path, monkeypatch, patch_refs):
    monkeypatch.chdir(tmp_path)
    assert main(["create"]) == 0
    cb = tmp_path / "cookbook"
    # Recipe with no frontmatter at all.
    (cb / "recipes" / "bad.md").write_text("# Just a header\n", encoding="utf-8")
    # Do NOT run update — leave frontmatter missing so Phase A complains.
    rc = main(["lint", "-p", str(cb), "--no-llm"])
    assert rc != 0


def test_lint_skips_phase_b_when_claude_missing(tmp_path, monkeypatch, patch_refs, capsys):
    monkeypatch.chdir(tmp_path)
    assert main(["create"]) == 0
    cb = tmp_path / "cookbook"
    (cb / "recipes" / "ok.md").write_text("# Ok\n", encoding="utf-8")
    assert main(["update", "-p", str(cb), "--author", "T"]) == 0
    monkeypatch.setattr(lint_mod, "claude_available", lambda: False)
    # Without --no-llm, but claude is unavailable: should still exit 0 and warn.
    rc = main(["lint", "-p", str(cb)])
    assert rc == 0


def test_lint_since_and_files_are_mutually_exclusive(tmp_path, monkeypatch, patch_refs):
    monkeypatch.chdir(tmp_path)
    assert main(["create"]) == 0
    cb = tmp_path / "cookbook"
    (cb / "recipes" / "ok.md").write_text("# Ok\n", encoding="utf-8")
    assert main(["update", "-p", str(cb), "--author", "T"]) == 0
    monkeypatch.setattr(lint_mod, "claude_available", lambda: True)
    rc = main(["lint", "-p", str(cb), "--since", "HEAD", str(cb / "recipes" / "ok.md")])
    assert rc == 2


def test_lint_since_resolves_changed_files(tmp_path, monkeypatch, patch_refs):
    monkeypatch.chdir(tmp_path)
    assert main(["create"]) == 0
    cb = tmp_path / "cookbook"
    (cb / "recipes" / "ok.md").write_text("# Ok\n", encoding="utf-8")
    assert main(["update", "-p", str(cb), "--author", "T"]) == 0

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
    (cb / "recipes" / "new.md").write_text(
        "---\nid: 11111111-2222-3333-4444-555555555555\ntitle: New\n"
        "domain: agenticdevelopercookbook://cookbook/recipes/new\ntype: recipe\n"
        "version: 1.0.0\nstatus: draft\nlanguage: en\ncreated: 2026-05-15\n"
        "modified: 2026-05-15\nauthor: T\ncopyright: 2026 T\nlicense: MIT\n"
        "summary: a new one\n---\n# New\n",
        encoding="utf-8",
    )
    _g("add", "cookbook/recipes/new.md")
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
