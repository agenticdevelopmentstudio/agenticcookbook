"""Guard: no test may resolve cookr's home to the user's real ~/.cookr."""

from __future__ import annotations

import json
import os
from pathlib import Path
from types import SimpleNamespace

from cookr.core import install, links
from cookr.core.identity import CookbookIdentity
from tests import conftest
from tests.conftest import REAL_COOKR_HOME, REAL_LOCATIONS_AT_START, real_locations


def _inside_real_home(path: Path) -> bool:
    path = Path(path).expanduser().resolve()
    return path == REAL_COOKR_HOME or REAL_COOKR_HOME in path.parents


def test_cookr_home_is_not_the_real_home():
    assert os.environ.get("COOKR_HOME")
    assert not _inside_real_home(Path(os.environ["COOKR_HOME"]))
    assert not _inside_real_home(install.home())
    assert not _inside_real_home(links._locations_path())


class _Reporter:
    def __init__(self):
        self.lines: list[str] = []

    def write_line(self, line, **_):
        self.lines.append(line)


def _session(reporter):
    manager = SimpleNamespace(get_plugin=lambda name: reporter if name == "terminalreporter" else None)
    return SimpleNamespace(config=SimpleNamespace(pluginmanager=manager), exitstatus=0)


def test_the_session_guard_fails_a_run_that_changed_the_real_file(monkeypatch):
    # The backstop the suite relies on: a changed real locations.json fails the
    # run and says so. An unchanged one leaves the run alone.
    reporter = _Reporter()
    session = _session(reporter)
    conftest.pytest_sessionfinish(session, 0)
    assert session.exitstatus == 0 and reporter.lines == []
    monkeypatch.setattr(conftest, "real_locations", lambda: b"changed by a test")
    conftest.pytest_sessionfinish(session, 0)
    assert session.exitstatus == 1
    assert len(reporter.lines) == 1 and "locations.json" in reporter.lines[0]


def test_the_session_guard_reports_on_stderr_without_a_terminal_reporter(monkeypatch, capsys):
    # Under `-p no:terminal` there is no reporter; the guard must not raise and
    # hide the real failure.
    session = _session(None)
    monkeypatch.setattr(conftest, "real_locations", lambda: b"changed by a test")
    conftest.pytest_sessionfinish(session, 0)
    assert session.exitstatus == 1
    assert "FAIL: a test changed" in capsys.readouterr().err


def test_remembering_a_location_with_no_cookr_home_writes_the_scratch_home(monkeypatch, tmp_path):
    # COOKR_HOME unset: cookr falls back to its default path, which the suite
    # repoints, and the write lands there; the real file is untouched.
    monkeypatch.delenv("COOKR_HOME")
    identity = CookbookIdentity("0b5e0000-0000-4000-8000-000000000001", "hermetic")
    links.remember_location(identity, tmp_path, None)
    assert not _inside_real_home(links._locations_path())
    stored = json.loads(links._locations_path().read_text(encoding="utf-8"))
    assert "0b5e0000-0000-4000-8000-000000000001" in json.dumps(stored)
    assert real_locations() == REAL_LOCATIONS_AT_START
