"""Sanity check that the install pipeline left behind a usable shim.

These don't reinstall — they verify the post-install state. If a contributor
hasn't run `./install` yet, the `cookbook_bin` fixture skips them."""

from __future__ import annotations

import os
from pathlib import Path


def test_shim_exists_and_is_executable(cookbook_bin):
    p = Path(cookbook_bin)
    assert p.is_file()
    assert os.access(p, os.X_OK)


def test_shim_points_at_local_bin(cookbook_bin):
    # ./install writes ~/.local/bin/cookbook. We can't assert the exact
    # location (CI might install elsewhere), but it must NOT live inside the
    # source tree — otherwise tests would silently use uninstalled code.
    p = Path(cookbook_bin).resolve()
    src_marker = Path(__file__).resolve().parents[4] / "scripts" / "cookbook" / "cookbook"
    assert src_marker not in p.parents, (
        f"`cookbook` resolves into the source tree at {p}; tests should run "
        "the installed shim, not the source. Run ./install first."
    )


def test_help_works(run_cookbook):
    r = run_cookbook(["--help"])
    assert r.returncode == 0
    assert "cookbook" in r.stdout.lower()


def test_each_module_has_help(run_cookbook):
    for name in ("create", "update", "lint", "validate", "plan"):
        r = run_cookbook([name, "--help"])
        assert r.returncode == 0, f"{name} --help failed: {r.stderr}"
