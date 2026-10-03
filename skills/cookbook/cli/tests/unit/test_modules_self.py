"""self update: error paths + happy path delegates to ./install."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

from cookbook.cli import main
from cookbook.modules import selfcmd as self_mod


def test_self_with_no_action_lists_actions(capsys, patch_refs):
    rc = main(["self"])
    assert rc == 0


def test_self_update_errors_when_stamp_missing(tmp_path, monkeypatch, patch_refs):
    # Point _pkg_dir at a dir that has no .install_source stamp.
    monkeypatch.setattr(self_mod, "_pkg_dir", lambda: tmp_path)
    rc = main(["self", "update"])
    assert rc == 1


def test_self_update_errors_when_stamped_path_missing_install(tmp_path, monkeypatch, patch_refs):
    fake_pkg = tmp_path / "pkg"
    fake_pkg.mkdir()
    fake_source = tmp_path / "moved-or-deleted"
    fake_source.mkdir()  # exists, but no install inside
    (fake_pkg / ".install_source").write_text(str(fake_source), encoding="utf-8")

    monkeypatch.setattr(self_mod, "_pkg_dir", lambda: fake_pkg)
    rc = main(["self", "update"])
    assert rc == 1


def test_self_update_invokes_install_from_stamped_path(tmp_path, monkeypatch, patch_refs):
    fake_pkg = tmp_path / "pkg"
    fake_pkg.mkdir()
    fake_source = tmp_path / "repo"
    fake_source.mkdir()
    (fake_source / "install").write_text("#!/usr/bin/env python3\nprint('mock')\n", encoding="utf-8")
    (fake_source / "install").chmod(0o755)
    (fake_pkg / ".install_source").write_text(str(fake_source), encoding="utf-8")

    captured = {}

    def fake_run(cmd, cwd, stdin, stdout, stderr):
        captured["cmd"] = cmd
        captured["cwd"] = cwd
        return subprocess.CompletedProcess(cmd, 0)

    monkeypatch.setattr(self_mod, "_pkg_dir", lambda: fake_pkg)
    monkeypatch.setattr(self_mod.subprocess, "run", fake_run)

    rc = main(["self", "update"])
    assert rc == 0
    assert captured["cmd"] == [sys.executable, str(fake_source / "install")]
    assert captured["cwd"] == fake_source
