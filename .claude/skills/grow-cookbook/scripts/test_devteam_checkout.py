"""devteam_checkout.py: stage 1 without a devteam checkout exits with one plain message (1.4.45)."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))

import devteam_checkout  # noqa: E402

SCRIPT = Path(__file__).resolve().parent / "devteam_checkout.py"


def cookbook(tmp_path: Path) -> Path:
    repo = tmp_path / "dt" / "external" / "agenticcookbook"
    (repo / "cookbook" / "guidelines").mkdir(parents=True)
    return repo


def test_the_checkout_two_folders_above_the_repo_is_the_default(tmp_path):
    repo = cookbook(tmp_path)
    (tmp_path / "dt" / "speciality_reference.py").write_text("")
    assert devteam_checkout.devteam_checkout(None, repo) == tmp_path / "dt"


def test_a_given_checkout_is_used(tmp_path):
    repo = cookbook(tmp_path)
    (tmp_path / "other").mkdir()
    (tmp_path / "other" / "speciality_reference.py").write_text("")
    assert devteam_checkout.devteam_checkout(str(tmp_path / "other"), repo) == tmp_path / "other"


@pytest.mark.parametrize("given", [None, "elsewhere"])
def test_no_checkout_exits_2_with_one_plain_message(tmp_path, given):
    repo = cookbook(tmp_path)
    argv = [sys.executable, str(SCRIPT), "--repo", str(repo)] + (["--devteam", str(tmp_path / given)] if given else [])
    r = subprocess.run(argv, capture_output=True, text=True)
    assert r.returncode == 2 and r.stdout == "", r
    err = r.stderr.strip()
    assert len(err.splitlines()) == 1 and "Traceback" not in err, err
    assert "agenticdevteam checkout" in err and "speciality_reference.py" in err and "--devteam" in err, err
    assert str(tmp_path / given if given else tmp_path / "dt") in err, err
