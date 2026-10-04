import pytest

from cookr.cli import main


# Every tmp_path here is a git repo, as a real cookbook checkout is.
pytestmark = pytest.mark.usefixtures("git_tmp_path")


def test_create_scaffolds_and_is_idempotent(tmp_path, monkeypatch, patch_refs):
    monkeypatch.chdir(tmp_path)
    rc = main(["create"])
    assert rc == 0
    root = tmp_path / "cookbook"
    assert (root / "index.md").exists()
    assert (root / "description.md").exists()
    assert (root / "recipes" / ".gitkeep").exists()
    assert (root / "reference" / ".gitkeep").exists()

    # Idempotent: second run touches nothing.
    desc_before = (root / "description.md").read_text()
    rc2 = main(["create"])
    assert rc2 == 0
    assert (root / "description.md").read_text() == desc_before
