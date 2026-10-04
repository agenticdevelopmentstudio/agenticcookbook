"""Run the CLI against the named fixture cookbooks in `cookbook-tests`.

Each fixture in `cookbook-tests/fixtures/<name>/` is a pre-shaped cookbook
representing a realistic starting state. The test file declares the expected
outcome of `update` / `validate` / `lint --no-llm` for each fixture.

If `cookbook-tests` cannot be cloned (no network, no SSH key), the entire
file is skipped via the `cookbook_tests_repo` fixture in conftest.py.
"""

from __future__ import annotations

import pytest

# Each entry: (fixture_name, validate_expected_rc, lint_expected_rc)
# - "valid": the cookbook is consistent; both validate and lint --no-llm should be green.
# - "drift": INDEX files are stale; validate fails, lint may pass (Phase A only).
# - "broken": one or more deterministic check rules fail; both lint and validate fail.
FIXTURES = [
    ("empty-client", 0, 0),
    ("recipes-only-valid", 0, 0),
    ("with-drift", 1, 0),
    ("broken-frontmatter", 1, 1),
]


@pytest.mark.parametrize("name,validate_rc,lint_rc", FIXTURES)
def test_fixture_matches_expected(name, validate_rc, lint_rc, fixture_cookbook, run_cookr):
    cb_root = fixture_cookbook(name) / "cookbook"
    assert cb_root.is_dir(), f"fixture {name} missing `cookbook/` subdir"

    v = run_cookr(["validate", "-p", str(cb_root)])
    assert v.returncode == validate_rc, (
        f"{name}: expected validate rc={validate_rc}, got {v.returncode}\n"
        f"stdout:\n{v.stdout}\nstderr:\n{v.stderr}"
    )

    l = run_cookr(["lint", "-p", str(cb_root), "--no-llm"])
    assert l.returncode == lint_rc, (
        f"{name}: expected lint rc={lint_rc}, got {l.returncode}\n"
        f"stdout:\n{l.stdout}\nstderr:\n{l.stderr}"
    )


def test_update_then_validate_fixes_drift(fixture_cookbook, run_cookr):
    """`with-drift` is intentionally stale. After `update`, validate should be green."""
    cb_root = fixture_cookbook("with-drift") / "cookbook"

    pre = run_cookr(["validate", "-p", str(cb_root)])
    assert pre.returncode != 0

    upd = run_cookr(["update", "-p", str(cb_root), "--author", "Tester"])
    assert upd.returncode == 0, upd.stdout

    post = run_cookr(["validate", "-p", str(cb_root)])
    assert post.returncode == 0, post.stdout
