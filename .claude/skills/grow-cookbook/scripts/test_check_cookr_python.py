"""check_cookr_python.py: whether the running Python can run cookr.

    python3 -m pytest .claude/skills/grow-cookbook/scripts -q
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import check_cookr_python  # noqa: E402

SCRIPT = Path(__file__).resolve().parent / "check_cookr_python.py"


def test_cookr_needs_rich_questionary_and_yaml_on_3_11():
    assert check_cookr_python.REQUIRED == ("rich", "questionary", "yaml")
    assert check_cookr_python.MINIMUM == (3, 11)


def test_a_python_with_every_module_is_ok():
    result = check_cookr_python.check(("json", "re"), (3, 0))
    assert result == {"python": sys.executable, "version": "%d.%d.%d" % sys.version_info[:3],
                      "missing": [], "too_old": False, "ok": True}


def test_a_missing_module_is_named():
    result = check_cookr_python.check(("json", "no_such_module_for_cookr"), (3, 0))
    assert result["missing"] == ["no_such_module_for_cookr"] and result["ok"] is False


def test_an_old_python_is_not_ok():
    result = check_cookr_python.check(("json",), (99, 0))
    assert result["too_old"] is True and result["ok"] is False


def test_the_script_prints_json_and_exits_2_with_a_clear_message_when_not_ok(monkeypatch, capsys):
    monkeypatch.setattr(check_cookr_python, "REQUIRED", ("json", "no_such_module_for_cookr"))
    code = check_cookr_python.main()
    out, err = capsys.readouterr()
    assert code == 2 and json.loads(out)["ok"] is False
    assert "no_such_module_for_cookr" in err and "COOKR_PY" in err


def test_the_script_exits_0_when_ok(monkeypatch, capsys):
    monkeypatch.setattr(check_cookr_python, "REQUIRED", ("json",))
    monkeypatch.setattr(check_cookr_python, "MINIMUM", (3, 0))
    assert check_cookr_python.main() == 0 and json.loads(capsys.readouterr().out)["ok"] is True


def test_it_runs_as_a_script():
    r = subprocess.run([sys.executable, str(SCRIPT)], capture_output=True, text=True)
    assert r.returncode in (0, 2) and "ok" in json.loads(r.stdout)
