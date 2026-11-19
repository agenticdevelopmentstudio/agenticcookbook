"""write_on_success.py: a command's stdout written to a file only when it succeeds.

    python3 -m pytest .claude/skills/grow-cookbook/scripts -q
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import pytest

SCRIPT = Path(__file__).resolve().parent / "write_on_success.py"


def run(out: Path, *command: str) -> subprocess.CompletedProcess:
    return subprocess.run([sys.executable, str(SCRIPT), str(out), "--", *command],
                          capture_output=True, text=True)


def test_a_success_writes_stdout_creating_the_folders_with_mkdir(tmp_path):
    out = tmp_path / "areas" / "a" / "gaps" / "t.json"
    r = subprocess.run([sys.executable, str(SCRIPT), "--mkdir", str(out), "--", sys.executable, "-c", "print('{}')"],
                       capture_output=True, text=True)
    assert r.returncode == 0
    assert out.read_text() == "{}\n"
    assert sorted(p.name for p in out.parent.iterdir()) == ["t.json"]


def test_a_failure_leaves_no_file_and_keeps_its_exit_code_and_stderr(tmp_path):
    out = tmp_path / "gaps" / "t.json"
    out.parent.mkdir()
    r = run(out, sys.executable, "-c", "import sys; print('partial'); sys.stderr.write('bad path\\n'); sys.exit(2)")
    assert r.returncode == 2
    assert "bad path" in r.stderr
    assert list(out.parent.iterdir()) == []


def test_a_failure_keeps_the_previous_file(tmp_path):
    out = tmp_path / "t.json"
    out.write_text("old\n")
    r = run(out, sys.executable, "-c", "import sys; sys.exit(1)")
    assert r.returncode == 1 and out.read_text() == "old\n"
    assert [p.name for p in tmp_path.iterdir()] == ["t.json"]


def test_leading_assignments_are_the_commands_environment(tmp_path):
    out = tmp_path / "t.txt"
    r = run(out, "GROW_COOKBOOK_PROBE=yes", sys.executable, "-c",
            "import os; print(os.environ['GROW_COOKBOOK_PROBE'])")
    assert r.returncode == 0 and out.read_text() == "yes\n"


def test_a_missing_command_exits_2(tmp_path):
    r = subprocess.run([sys.executable, str(SCRIPT), str(tmp_path / "t.json")], capture_output=True, text=True)
    assert r.returncode == 2
    assert not (tmp_path / "t.json").exists()


def test_a_command_that_cannot_run_exits_127_and_leaves_no_file(tmp_path):
    out = tmp_path / "t.json"
    r = run(out, str(tmp_path / "no-such-program"))
    assert r.returncode == 127 and "cannot run" in r.stderr
    assert list(tmp_path.iterdir()) == []


def test_the_file_is_readable_like_any_other(tmp_path):
    out = tmp_path / "t.json"
    run(out, sys.executable, "-c", "print(1)")
    assert out.stat().st_mode & 0o044 == 0o044


def test_a_failures_stdout_is_shown_not_kept(tmp_path):
    # cookr prints its errors on stdout; the message that names a bad path must reach the reader.
    out = tmp_path / "t.json"
    r = run(out, sys.executable, "-c", "import sys; print('x: not an artifact source folder'); sys.exit(2)")
    assert r.returncode == 2 and "x: not an artifact source folder" in r.stdout
    assert list(tmp_path.iterdir()) == []


def test_the_skills_command_form_pythonpath_then_python_dash_m(tmp_path):
    # 1.4.13, G17: the form SKILL.md and stage-1.md show,
    # `-- PYTHONPATH=<repo>/skills/cookr/cli $COOKR_PY -m cookr ...`, with the
    # assignment as the first word after `--` (no `env`), imports the module
    # from that PYTHONPATH.
    cli = tmp_path / "cli"
    (cli / "probe_cookr").mkdir(parents=True)
    (cli / "probe_cookr" / "__init__.py").write_text("")
    (cli / "probe_cookr" / "__main__.py").write_text("import sys; print('roles gaps', sys.argv[1:])\n")
    out = tmp_path / "gaps" / "t.json"
    out.parent.mkdir()
    r = run(out, f"PYTHONPATH={cli}", sys.executable, "-m", "probe_cookr", "-p", "/repo", "roles", "gaps")
    assert r.returncode == 0, r.stderr
    assert out.read_text() == "roles gaps ['-p', '/repo', 'roles', 'gaps']\n"


def test_the_env_form_works_too(tmp_path):
    out = tmp_path / "t.txt"
    r = run(out, "env", "GROW_COOKBOOK_PROBE=yes", sys.executable, "-c",
            "import os; print(os.environ['GROW_COOKBOOK_PROBE'])")
    assert r.returncode == 0 and out.read_text() == "yes\n"


def test_an_identical_output_leaves_the_file_untouched(tmp_path):
    # 1.4.18, G38: a success that prints the file's own bytes does not rewrite
    # it (its mtime stays), so an idempotent re-run touches nothing.
    import os
    out = tmp_path / "t.json"
    out.write_text("same\n")
    os.utime(out, (1_000_000_000, 1_000_000_000))
    r = run(out, sys.executable, "-c", "print('same')")
    assert r.returncode == 0 and out.read_text() == "same\n"
    assert out.stat().st_mtime == 1_000_000_000
    assert [p.name for p in tmp_path.iterdir()] == ["t.json"]
    r = run(out, sys.executable, "-c", "print('new')")
    assert r.returncode == 0 and out.read_text() == "new\n"


def test_a_failure_printing_the_files_own_bytes_still_shows_its_output(tmp_path):
    # 1.4.19, N3: the identical-bytes skip is for a success only; a failing
    # command whose output equals the file still shows that output, and its exit.
    out = tmp_path / "t.json"
    out.write_text("same\n")
    r = run(out, sys.executable, "-c", "import sys; print('same'); sys.exit(1)")
    assert r.returncode == 1 and r.stdout == "same\n" and out.read_text() == "same\n"


def test_a_relative_out_file_is_refused_with_exit_2(tmp_path):
    # G44 (1.4.24): a relative <out-file> would land wherever the caller
    # stands; it is refused, nothing is run and nothing is written.
    marker = tmp_path / "ran"
    r = subprocess.run([sys.executable, str(SCRIPT), "gaps/t.json", "--", sys.executable, "-c",
                        f"open({str(marker)!r}, 'w')"], capture_output=True, text=True, cwd=tmp_path)
    assert r.returncode == 2
    assert "absolute" in r.stderr
    assert not marker.exists() and not (tmp_path / "gaps").exists()


def test_a_missing_folder_is_refused_and_nothing_is_created(tmp_path):
    # G174 (N25): no --mkdir: a target whose folder is missing exits 2 and
    # creates nothing; a folder that cannot hold a temporary file is one line.
    out = tmp_path / "no" / "such" / "t.json"
    r = run(out, sys.executable, "-c", "print('{}')")
    assert r.returncode == 2 and "does not exist" in r.stderr and not (tmp_path / "no").exists(), r.stderr
    r = run(Path("/dev/null/x.json"), sys.executable, "-c", "print('{}')")
    assert r.returncode == 2 and "Traceback" not in r.stderr and len(r.stderr.strip().splitlines()) == 1, r.stderr


def test_a_folder_that_cannot_hold_a_temporary_file_is_one_line(tmp_path):
    # G174 (N25): the folder exists but refuses a temporary file (read-only):
    # exit 2 with one line, no traceback; with --mkdir, a folder that cannot
    # be created is one line too.
    import os
    ro = tmp_path / "ro"
    ro.mkdir()
    ro.chmod(0o500)
    try:
        if os.access(ro, os.W_OK):
            pytest.skip("running as a user who can write a read-only folder")
        r = run(ro / "t.json", sys.executable, "-c", "print('{}')")
        assert r.returncode == 2 and "Traceback" not in r.stderr and len(r.stderr.strip().splitlines()) == 1, r.stderr
        assert "temporary file" in r.stderr and not (ro / "t.json").exists()
    finally:
        ro.chmod(0o700)
    r = subprocess.run([sys.executable, str(SCRIPT), "--mkdir", "/dev/null/a/t.json", "--", sys.executable, "-c",
                        "print('{}')"], capture_output=True, text=True)
    assert r.returncode == 2 and "Traceback" not in r.stderr and len(r.stderr.strip().splitlines()) == 1, r.stderr


def test_a_write_into_a_planned_area_without_a_first_check_warns(tmp_path):
    # G215 (L30): step 1.1 rewrites the saved reports; the first check
    # (A/first-check.txt) is taken before it. A write into an area with a plan
    # and no first-check.txt warns on stderr; it still writes.
    a = tmp_path / "areas" / "implementing" / "x"
    (a / "reference").mkdir(parents=True)
    (a / "area-plan.md").write_text("# plan\n")
    out = a / "reference.json"
    r = run(out, sys.executable, "-c", "print('[]')")
    assert r.returncode == 0 and out.read_text() == "[]\n"
    assert "first-check.txt" in r.stderr, r.stderr
    (a / "first-check.txt").write_text("digests\n")
    r = run(out, sys.executable, "-c", "print('[1]')")
    assert r.returncode == 0 and "first-check" not in r.stderr
    fresh = tmp_path / "areas" / "shipping"
    fresh.mkdir()
    r = run(fresh / "reference.json", sys.executable, "-c", "print('[]')")
    assert r.returncode == 0 and "first-check" not in r.stderr        # no plan yet: nothing to check first


# --- gapfix12 (1.4.40) ---------------------------------------------------------------------------


def test_a_command_that_edits_out_in_place_is_refused_and_its_edit_kept(tmp_path):
    # G231 (L9): `sed -i`-style editors write `out` themselves and print nothing:
    # the wrapper would replace the edit with their (empty) stdout. It exits 2,
    # says so and leaves the edit.
    out = tmp_path / "area-plan.md"
    out.write_text("before\n")
    r = run(out, sys.executable, "-c", f"open({str(out)!r}, 'a').write('edited\\n')")
    assert r.returncode == 2 and "edited" in r.stderr and "in place" in r.stderr, r
    assert out.read_text() == "before\nedited\n"
    assert [p.name for p in tmp_path.iterdir()] == ["area-plan.md"]


def test_a_command_that_creates_out_itself_is_refused_too(tmp_path):
    out = tmp_path / "t.json"
    r = run(out, sys.executable, "-c", f"open({str(out)!r}, 'w').write('mine')")
    assert r.returncode == 2 and "in place" in r.stderr, r
    assert out.read_text() == "mine"


def test_a_command_that_prints_and_leaves_out_alone_still_writes_it(tmp_path):
    out = tmp_path / "t.json"
    out.write_text("old\n")
    r = run(out, sys.executable, "-c", "print('new')")
    assert r.returncode == 0 and out.read_text() == "new\n"


def test_writing_first_check_itself_does_not_warn_that_it_is_missing(tmp_path):
    # gapfix13 (G267, 1.4.42): the warning is for the reports the first check must precede, not the check itself.
    a = tmp_path / "areas" / "implementing" / "x"
    a.mkdir(parents=True)
    (a / "area-plan.md").write_text("plan\n")
    r = subprocess.run([sys.executable, str(SCRIPT), str(a / "first-check.txt"), "--", sys.executable, "-c",
                        "print('d')"], capture_output=True, text=True)
    assert r.returncode == 0 and "first-check" not in r.stderr, r.stderr


@pytest.mark.parametrize("command", [("",), ("X=1", ""), ("  ", "arg")])
def test_an_empty_command_word_is_refused_with_exit_2_and_no_file(tmp_path, command):
    # gapfix14 (G299, 1.4.43): an unset variable as the command (`-- "$COOKR_PY" ...` with it empty) ran nothing
    # and exited 127 with "cannot run : Permission denied"; it is now a usage error naming the empty word.
    out = tmp_path / "t.json"
    r = run(out, *command)
    assert r.returncode == 2 and not out.exists(), r
    assert "the command is empty" in r.stderr and "COOKR_PY" in r.stderr, r.stderr
