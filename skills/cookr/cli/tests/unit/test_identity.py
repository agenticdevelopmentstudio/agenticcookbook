import json

import pytest

from cookr.core.identity import (CookbookIdentity, IdentityError, artifact_rdid, check_rdid,
                                 check_uuid, is_rdid, is_uuid, read_manifest, write_manifest)

CID = "5b1e0000-0000-4000-8000-000000000000"


def test_artifact_rdid_strips_type_dir():
    assert artifact_rdid("adc", "guideline", "guidelines/testing/test-pyramid") == "adc.guideline.testing.test-pyramid"
    assert artifact_rdid("adhsdk", "recipe", "ui/navigation/htdv") == "adhsdk.recipe.ui.navigation.htdv"


def test_check_identity_is_deterministic():
    assert check_uuid(CID, "best-practices", "unit-test-coverage") == check_uuid(CID, "best-practices", "unit-test-coverage")
    assert check_uuid(CID, "a", "x") != check_uuid(CID, "a", "y")
    assert is_uuid(check_uuid(CID, "a", "x"))
    assert check_rdid("adc", "artifact-formatting/recipe-formatting", "has-frontmatter") == "adc.check.artifact-formatting.recipe-formatting.has-frontmatter"


def test_validators():
    assert is_rdid("adhsdk.recipe.ui.web-panel")
    assert not is_rdid("Bad.Name") and not is_rdid("a..b") and not is_rdid("")
    assert is_uuid(CID) and not is_uuid("nope")


def test_manifest_round_trip_keeps_extra(tmp_path):
    (tmp_path / "cookbook.json").write_text(json.dumps({"format": 2, "id": CID, "rdid": "adc", "name": "x"}))
    ident = read_manifest(tmp_path)
    assert ident == CookbookIdentity(CID, "adc")
    write_manifest(tmp_path, CookbookIdentity(CID, "adc2"), {"more": 1})
    data = json.loads((tmp_path / "cookbook.json").read_text())
    assert data["name"] == "x" and data["more"] == 1 and data["rdid"] == "adc2"


def test_manifest_without_format_2_raises(tmp_path):
    (tmp_path / "cookbook.json").write_text(json.dumps({"format": 1}))
    with pytest.raises(IdentityError):
        read_manifest(tmp_path)
    with pytest.raises(IdentityError):
        read_manifest(tmp_path / "missing")


def test_rdid_grammar():
    from cookr.core.identity import is_cookbook_rdid
    assert is_rdid("adc.guideline.x") and is_rdid("a.b") and not is_rdid("adc")
    assert not is_rdid("1a.b") and not is_rdid("a.-b") and is_rdid("a.0b-c")
    assert is_cookbook_rdid("adc") and is_cookbook_rdid("ad-hsdk") and not is_cookbook_rdid("a.b")
    assert not is_cookbook_rdid("1a") and not is_cookbook_rdid("")
    with pytest.raises(IdentityError):
        artifact_rdid("adc", "guideline", "Bad Name")
    with pytest.raises(IdentityError):
        check_rdid("adc", "doc", "Bad")


def test_manifest_validates_cookbook_rdid_and_lowercases(tmp_path):
    (tmp_path / "cookbook.json").write_text(json.dumps({"format": 2, "id": CID.upper(), "rdid": "adc"}))
    assert read_manifest(tmp_path).id == CID
    (tmp_path / "cookbook.json").write_text(json.dumps({"format": 2, "id": CID, "rdid": "a.b"}))
    with pytest.raises(IdentityError):
        read_manifest(tmp_path)
    with pytest.raises(IdentityError):
        write_manifest(tmp_path, CookbookIdentity(CID, "a.b"))
