"""team_probe.py: whether a team can run, checked without starting one (E6)."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))

import team_probe  # noqa: E402


def dist(site: Path, name: str, requires: list[str]) -> None:
    """A fake installed distribution `name` providing the package `name`."""
    (site / name).mkdir()
    (site / name / "__init__.py").write_text("", encoding="utf-8")
    info = site / f"{name}-1.0.dist-info"
    info.mkdir()
    lines = [f"Metadata-Version: 2.1", f"Name: {name}", "Version: 1.0"] + [f"Requires-Dist: {r}" for r in requires]
    (info / "METADATA").write_text("\n".join(lines) + "\n", encoding="utf-8")
    (info / "top_level.txt").write_text(name + "\n", encoding="utf-8")
    (info / "RECORD").write_text(f"{name}/__init__.py,,\n", encoding="utf-8")


@pytest.fixture(scope="module")
def venv(tmp_path_factory) -> str:
    """A bare venv holding fakedoor (needs fakedep, and fakewin on Windows only,
    and fakedev for an extra) and fakedep; fakebroken needs fakegone."""
    root = tmp_path_factory.mktemp("venv")
    subprocess.run([sys.executable, "-m", "venv", "--without-pip", str(root)], check=True)
    python = root / "bin" / "python"
    site = Path(subprocess.run([str(python), "-c", "import sysconfig;print(sysconfig.get_paths()['purelib'])"],
                               capture_output=True, text=True, check=True).stdout.strip())
    dist(site, "fakedoor", ["fakedep>=1", 'fakewin; sys_platform == "win32"', 'fakedev; extra == "dev"'])
    dist(site, "fakedep", [])
    dist(site, "fakebroken", ["fakegone"])
    return str(python)


def front_door(tmp: Path, python: str) -> Path:
    f = tmp / "myteams"
    f.write_text(f"#!/bin/sh\n'''exec' {python} -I \"$0\" \"$@\"\n' '''\nraise SystemExit('a run started')\n",
                 encoding="utf-8")
    return f


def home(tmp: Path, team: str = "researchteam") -> Path:
    (tmp / "home" / team / "install").mkdir(parents=True)
    return tmp / "home"


def test_interpreter_is_read_from_the_exec_line(tmp_path):
    assert team_probe.interpreter(front_door(tmp_path, "/x/bin/python")) == "/x/bin/python"
    plain = tmp_path / "plain"
    plain.write_text("#!/usr/bin/env python3\nprint(1)\n", encoding="utf-8")
    assert team_probe.interpreter(plain) is None


def test_ok_when_the_team_is_installed_and_its_requirements_import(tmp_path, venv):
    got = team_probe.probe("researchteam", front_door(tmp_path, venv), home(tmp_path), package="fakedoor")
    assert got["ok"] is True, got
    assert got["missing"] == []


def test_a_missing_requirement_is_named(tmp_path, venv):
    got = team_probe.probe("researchteam", front_door(tmp_path, venv), home(tmp_path), package="fakebroken")
    assert got["ok"] is False and got["missing"] == ["fakegone"] and "fakegone" in got["why"]


def test_a_missing_team_or_front_door(tmp_path):
    got = team_probe.probe("researchteam", front_door(tmp_path, sys.executable), tmp_path / "nohome", package="pytest")
    assert got["ok"] is False and "not installed" in got["why"]
    got = team_probe.probe("researchteam", None, home(tmp_path), package="pytest")
    assert got["ok"] is False and "myteams" in got["why"]


def test_cli_never_runs_the_front_door(tmp_path, capsys, venv):
    door = front_door(tmp_path, venv)
    rc = team_probe.main(["researchteam", "--myteams", str(door), "--home", str(home(tmp_path)),
                          "--package", "fakedoor"])
    out = json.loads(capsys.readouterr().out)
    assert rc == 0 and out["ok"] is True
