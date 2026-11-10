"""The format-2 upgrader (core/upgrade.py) and `cookr upgrade`."""

from __future__ import annotations

import json
import shutil
import subprocess
from pathlib import Path

import pytest

from cookr.cli import main
from cookr.core import upgrade as up
from cookr.core.errors import CookbookError
from cookr.core.identity import CookbookIdentity, check_uuid
from cookr.core.index import Index, load_index
from cookr.core.links import Dependency, Resolver, remember_location
from cookr.core.repoconfig import load_repo_config

FIXTURES = Path(__file__).resolve().parents[1] / "fixtures"
COOKBOOK_ID = "d8069120-7274-4094-bfb9-6d03d97e8d55"
BUTTON = "6f1c2a4e-0b3d-4c5e-9f10-a1b2c3d4e501"
COMPOSER = "6f1c2a4e-0b3d-4c5e-9f10-a1b2c3d4e502"
STAT_CARD = "6f1c2a4e-0b3d-4c5e-9f10-a1b2c3d4e503"
SITE_MENU = "6f1c2a4e-0b3d-4c5e-9f10-a1b2c3d4e504"
ADC_ID = "e7a40000-0000-4000-8000-000000000000"

LEGACY_IDS = {"button": "7a000000-0000-4000-8000-000000000001",
              "chat-composer": "7a000000-0000-4000-8000-000000000002",
              "site-menu": "7a000000-0000-4000-8000-000000000003",
              "stat-card": "7a000000-0000-4000-8000-000000000004"}


@pytest.fixture(autouse=True)
def home(tmp_path, monkeypatch):
    monkeypatch.setenv("COOKR_HOME", str(tmp_path / "cookr-home"))
    return tmp_path / "cookr-home"


def _git(repo, *args):
    return subprocess.run(["git", "-C", str(repo), *args], capture_output=True, text=True, check=True)


def _commit_all(repo: Path) -> None:
    _git(repo, "config", "user.email", "test@example.com")
    _git(repo, "config", "user.name", "Test Author")
    _git(repo, "add", "-A")
    _git(repo, "commit", "-q", "-m", "fixture")


def _repo(git_tmp_path: Path, name: str, mutate=None) -> Path:
    """A committed copy of fixtures/<name> in a git work tree."""
    repo = git_tmp_path
    shutil.copytree(FIXTURES / name, repo, dirs_exist_ok=True)
    if mutate:
        mutate(repo)
    _commit_all(repo)
    return repo


def _meta(folder: Path) -> dict:
    return json.loads((folder / "artifact.json").read_text(encoding="utf-8"))


def _set_meta(folder: Path, **values) -> None:
    data = _meta(folder)
    data["meta"].update(values)
    (folder / "artifact.json").write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")


def _append(path: Path, text: str) -> None:
    path.write_text(path.read_text(encoding="utf-8") + text, encoding="utf-8")


def _linked(repo: Path) -> None:
    cb = repo / "cookbook"
    _set_meta(cb / "site-menu", **{"depends-on": ["mini-repo://cookbook/components/button"],
                                   "related": ["chat-composer", "mini-repo://cookbook/nope"]})
    _append(cb / "site-menu" / "overview.md",
            "\nStats come from mini-repo://cookbook/blocks/stat-card. "
            "Press the [button](mini-repo://cookbook/components/button).\n"
            "Gone: mini-repo://cookbook/gone.\n")


def _status(repo: Path) -> str:
    return _git(repo, "status", "--porcelain").stdout


# ── format 2 everywhere ──────────────────────────────────────────────────────

def test_upgrade_writes_format_2_everywhere(git_tmp_path):
    repo = _repo(git_tmp_path, "v1-repo")
    reports = up.upgrade(repo)
    assert len(reports) == 1
    cb = repo / "cookbook"
    manifest = json.loads((cb / "cookbook.json").read_text(encoding="utf-8"))
    assert manifest["format"] == 2 and manifest["rdid"] == "mini-repo"
    assert not {"schema_version", "code", "cookbook"} & set(manifest)
    assert manifest["name"] == "mini-repo"
    assert manifest["structure"] == {"name": "mini-repo", "kind": "library"}
    assert json.loads((cb / "index.json").read_text(encoding="utf-8"))["format"] == 2
    for f in cb.rglob("artifact.json"):
        data = json.loads(f.read_text(encoding="utf-8"))
        assert data["format"] == 2
        assert "domain" not in data["meta"]
        assert not (f.parent / "versions").exists()
    config = load_repo_config(repo)
    assert config.identity.id == COOKBOOK_ID
    assert [(r.path, r.platform, r.group) for r in config.roots] == [
        ("web/components", "web", "components"), ("web/blocks", "web", "blocks"),
        ("apple/UI", "apple", "ui")]
    assert config.ignore == ["**/*.stories.tsx", "**/index.ts"]
    assert up.needs_upgrade(repo) == []


# references/cookbook.schema.json in this repo: tests/unit -> tests -> cli -> cookr -> skills -> root
COOKBOOK_SCHEMA = Path(__file__).resolve().parents[5] / "references" / "cookbook.schema.json"


def test_upgrade_keeps_every_manifest_key_the_format_2_schema_allows():
    schema = json.loads(COOKBOOK_SCHEMA.read_text(encoding="utf-8"))
    allowed = set(schema["properties"]) - {"format", "id", "rdid"}
    assert set(up.KEPT_MANIFEST_KEYS) == allowed


def test_upgrade_drops_manifest_keys_the_schema_does_not_allow(git_tmp_path):
    repo = _repo(git_tmp_path, "v1-repo")
    path = repo / "cookbook" / "cookbook.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    data["context"] = {"audience": "fixture"}
    data["invented"] = True
    path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    _git(repo, "commit", "-qam", "more manifest keys")
    up.upgrade(repo)
    manifest = json.loads(path.read_text(encoding="utf-8"))
    assert manifest["context"] == {"audience": "fixture"}
    assert "invented" not in manifest


def test_upgrade_keeps_artifact_uuids_and_cookbook_id(git_tmp_path):
    repo = _repo(git_tmp_path, "v1-repo")
    [report] = up.upgrade(repo)
    assert report.identity == CookbookIdentity(COOKBOOK_ID, "mini-repo")
    index = load_index(repo / "cookbook")
    arts = {k: (e.rdid, e.path) for k, e in index.entries.items() if e.kind != "check"}
    assert arts == {
        BUTTON: ("mini-repo.ingredient.components.button", "components/button"),
        COMPOSER: ("mini-repo.ingredient.components.chat-composer", "components/chat-composer"),
        STAT_CARD: ("mini-repo.ingredient.blocks.stat-card", "blocks/stat-card"),
        SITE_MENU: ("mini-repo.recipe.site-menu", "site-menu"),
    }
    assert report.artifacts == 4
    assert _meta(repo / "cookbook" / "components" / "button")["meta"]["id"] == BUTTON


def test_upgrade_moves_reference_implementations_into_index_unverified(git_tmp_path):
    def mutate(repo):
        _append(repo / "cookbook" / "components" / "chat-composer" / "reference-implementations.md",
                "| web | `web/components/Gone.tsx` |\n")
    repo = _repo(git_tmp_path, "v1-repo", mutate)
    [report] = up.upgrade(repo)
    index = load_index(repo / "cookbook")
    rows = [(i.platform, i.location, i.conformance.state) for i in index.entries[BUTTON].implementations]
    assert rows == [("web", "web/components/Button.tsx", "unverified"),
                    ("apple", "apple/UI/", "unverified")]
    assert [i.location for i in index.entries[COMPOSER].implementations] == [
        "web/components/chat-composer.tsx"]
    assert report.missing_paths == ["components/chat-composer: web/components/Gone.tsx"]
    for folder in (repo / "cookbook").rglob("artifact.json"):
        data = json.loads(folder.read_text(encoding="utf-8"))
        assert all(p.get("heading") != "Reference Implementations" for p in data["parts"])
        assert not (folder.parent / "reference-implementations.md").exists()


def test_upgrade_rewrites_links_to_uuids(git_tmp_path):
    repo = _repo(git_tmp_path, "v1-repo", _linked)
    [report] = up.upgrade(repo)
    meta = _meta(repo / "cookbook" / "site-menu")["meta"]
    assert meta["depends-on"] == [BUTTON]
    assert meta["related"][0] == COMPOSER
    text = (repo / "cookbook" / "site-menu" / "overview.md").read_text(encoding="utf-8")
    assert f"[mini-repo.ingredient.blocks.stat-card](cookbook:{STAT_CARD})." in text
    assert f"Press the [mini-repo.ingredient.components.button](cookbook:{BUTTON})." in text
    assert "mini-repo://cookbook/blocks/stat-card" not in text
    assert report.links_rewritten >= 4



def test_upgrade_drops_a_self_link_from_meta_link_lists(git_tmp_path):
    # Merging a legacy recipe into its artifact can leave it naming itself.
    def mutate(repo):
        _set_meta(repo / "cookbook" / "components" / "button",
                  **{"depends-on": [BUTTON],
                     "related": ["mini-repo://cookbook/components/button",
                                 "mini-repo://cookbook/components/chat-composer"]})
    repo = _repo(git_tmp_path, "v1-repo", mutate)
    [report] = up.upgrade(repo)
    meta = _meta(repo / "cookbook" / "components" / "button")["meta"]
    assert meta["depends-on"] == []
    assert meta["related"] == [COMPOSER]
    assert report.self_links_dropped == [
        f"components/button: depends-on {BUTTON}",
        "components/button: related mini-repo://cookbook/components/button"]


def test_upgrade_moves_a_cookbook_uri_in_references_to_a_related_link(git_tmp_path):
    # `references` holds external URLs; a cookbook URI there is a link, so it
    # becomes a `related` UUID (once, never a self-link). One that cannot be
    # placed is dropped and reported; URLs and plain text stay.
    def mutate(repo):
        _set_meta(repo / "cookbook" / "site-menu",
                  related=["mini-repo://cookbook/components/button"],
                  references=["https://example.com/doc",
                              "mini-repo://cookbook/components/button",
                              "mini-repo://cookbook/blocks/stat-card",
                              "mini-repo://cookbook/site-menu",
                              "mini-repo://cookbook/nope",
                              "RFC 2119"])
    repo = _repo(git_tmp_path, "v1-repo", mutate)
    [report] = up.upgrade(repo)
    meta = _meta(repo / "cookbook" / "site-menu")["meta"]
    assert meta["references"] == ["https://example.com/doc", "RFC 2119"]
    assert meta["related"] == [BUTTON, STAT_CARD]
    assert "site-menu: references mini-repo://cookbook/nope (dropped)" in report.needs_review
    assert "site-menu: references mini-repo://cookbook/site-menu" in report.self_links_dropped


def test_upgrade_keeps_a_named_label_as_text_beside_the_rdid(git_tmp_path):
    # The label of a rewritten link is the rdid; an old label that named
    # something else (a requirement, a check) would be lost, so it is kept.
    def mutate(repo):
        _append(repo / "cookbook" / "site-menu" / "overview.md",
                "\n| Check | Status |\n|-------|--------|\n"
                "| [no-token-passthrough](mini-repo://cookbook/components/button) | partial |\n"
                "| [validate-audience](mini-repo://cookbook/components/button) | partial |\n")
    repo = _repo(git_tmp_path, "v1-repo", mutate)
    up.upgrade(repo)
    text = (repo / "cookbook" / "site-menu" / "overview.md").read_text(encoding="utf-8")
    link = f"[mini-repo.ingredient.components.button](cookbook:{BUTTON})"
    assert f"| no-token-passthrough ({link}) | partial |\n" in text
    assert f"| validate-audience ({link}) | partial |\n" in text


def test_upgrade_rewrites_a_link_whose_label_wraps_across_lines(git_tmp_path):
    # A label wrapped onto the next line is one label (a blank line would end it).
    def mutate(repo):
        cb = repo / "cookbook"
        _append(cb / "site-menu" / "overview.md",
                "\nUse [Monitor Deploy\nStatus](mini-repo://cookbook/components/button).\n")
        _append(cb / "components" / "chat-composer" / "overview.md",
                "\nSee [the stat\ncard](../blocks/stat-card.md).\n")
    repo = _repo(git_tmp_path, "v1-repo", mutate)
    up.upgrade(repo)
    cb = repo / "cookbook"
    text = (cb / "site-menu" / "overview.md").read_text(encoding="utf-8")
    button = f"[mini-repo.ingredient.components.button](cookbook:{BUTTON})"
    card = f"[mini-repo.ingredient.blocks.stat-card](cookbook:{STAT_CARD})"
    assert f"Use Monitor Deploy\nStatus ({button}).\n" in text
    assert "](" + "[" not in text
    composer = (cb / "components" / "chat-composer" / "overview.md").read_text(encoding="utf-8")
    assert f"See the stat\ncard ({card}).\n" in composer


@pytest.mark.parametrize("before", ["a [stray\nline ", "```\nfoo[\n```\n"])
def test_a_stray_bracket_before_a_link_is_not_swallowed_into_its_label(git_tmp_path, before):
    # A label holds no `[`, so an unclosed bracket (or one inside a fence) on an
    # earlier line never stretches the link's label back to it.
    def mutate(repo):
        _append(repo / "cookbook" / "site-menu" / "overview.md",
                f"\n{before}[B](mini-repo://cookbook/components/button)\n")
    repo = _repo(git_tmp_path, "v1-repo", mutate)
    up.upgrade(repo)
    text = (repo / "cookbook" / "site-menu" / "overview.md").read_text(encoding="utf-8")
    button = f"[mini-repo.ingredient.components.button](cookbook:{BUTTON})"
    assert f"\n{before}B ({button})\n" in text


@pytest.mark.parametrize("label", ["button", "BUTTON", "mini-repo://cookbook/components/button",
                                   "mini-repo.ingredient.components.button", ""])
def test_upgrade_collapses_a_label_that_is_the_targets_own_name(git_tmp_path, label):
    # Its last path segment, its old domain or its rdid, compared case-insensitively.
    def mutate(repo):
        _append(repo / "cookbook" / "site-menu" / "overview.md",
                f"\n| Uses |\n|------|\n| [{label}](mini-repo://cookbook/components/button) |\n")
    repo = _repo(git_tmp_path, "v1-repo", mutate)
    up.upgrade(repo)
    text = (repo / "cookbook" / "site-menu" / "overview.md").read_text(encoding="utf-8")
    assert f"\n| [mini-repo.ingredient.components.button](cookbook:{BUTTON}) |\n" in text

def test_upgrade_resolves_a_section_or_requirement_fragment_to_its_artifact(git_tmp_path):
    # "#fragment only within a document": a link into another artifact's section
    # (or named requirement) becomes a link to that artifact, and the section's
    # name stays in the text when nothing else names it.
    def mutate(repo):
        cb = repo / "cookbook"
        _append(cb / "components" / "button" / "behavioral-requirements.md",
                "\n- **click-fires-once**: A click MUST fire one action.\n")
        _append(cb / "site-menu" / "overview.md",
                "\nA: mini-repo://cookbook/components/button#accessibility-options.\n"
                "B: [the keyboard rules](mini-repo://cookbook/components/button#accessibility).\n"
                "C: [states](mini-repo://cookbook/components/button#states).\n"
                "D: [button](mini-repo://cookbook/components/button#appearance).\n"
                "E: <mini-repo://cookbook/components/button#click-fires-once>.\n"
                "F: mini-repo://cookbook/components/button#Edge-Cases.\n"
                "G: mini-repo://cookbook/components/button#no-such-section.\n")
        _set_meta(cb / "site-menu",
                  related=["mini-repo://cookbook/components/button#states", "chat-composer"])
    repo = _repo(git_tmp_path, "v1-repo", mutate)
    [report] = up.upgrade(repo)
    text = (repo / "cookbook" / "site-menu" / "overview.md").read_text(encoding="utf-8")
    link = f"[mini-repo.ingredient.components.button](cookbook:{BUTTON})"
    assert f"A: accessibility-options ({link}).\n" in text
    assert f"B: the keyboard rules ({link}).\n" in text
    assert f"C: states ({link}).\n" in text
    assert f"D: appearance ({link}).\n" in text
    assert f"E: click-fires-once ({link}).\n" in text
    assert f"F: Edge-Cases ({link}).\n" in text
    assert ("G: NEEDS REVIEW: unresolved link "
            "mini-repo://cookbook/components/button#no-such-section.\n") in text
    assert _meta(repo / "cookbook" / "site-menu")["meta"]["related"][0] == BUTTON
    assert [n for n in report.needs_review if "button#" in n] == [
        "site-menu: mini-repo://cookbook/components/button#no-such-section"]


def test_upgrade_resolves_a_nested_fragment_and_leaves_no_tail(git_tmp_path):
    # A fragment with `/` (`#section/requirement`, `#requirements/<name>`) is one
    # fragment: tried whole, then its last segment, then its first. The label
    # keeps the most specific name matched; no tail of the old URI stays glued.
    def mutate(repo):
        cb = repo / "cookbook"
        _append(cb / "components" / "button" / "behavioral-requirements.md",
                "\n- **click-fires-once**: A click MUST fire one action.\n")
        _append(cb / "site-menu" / "overview.md",
                "\nA: mini-repo://cookbook/components/button#accessibility/click-fires-once.\n"
                "B: mini-repo://cookbook/components/button#requirements/click-fires-once.\n"
                "C: mini-repo://cookbook/components/button#accessibility/no-such-thing.\n"
                "D: [the rules](mini-repo://cookbook/components/button#accessibility/click-fires-once).\n"
                "E: <mini-repo://cookbook/components/button#requirements/click-fires-once>.\n"
                "F: mini-repo://cookbook/components/button#nope/also-nope.\n"
                "G: [accessibility/click-fires-once]"
                "(mini-repo://cookbook/components/button#accessibility/click-fires-once).\n")
        _set_meta(cb / "site-menu", related=[
            "mini-repo://cookbook/components/button#requirements/click-fires-once"])
    repo = _repo(git_tmp_path, "v1-repo", mutate)
    [report] = up.upgrade(repo)
    text = (repo / "cookbook" / "site-menu" / "overview.md").read_text(encoding="utf-8")
    link = f"[mini-repo.ingredient.components.button](cookbook:{BUTTON})"
    assert f"A: click-fires-once ({link}).\n" in text
    assert f"B: click-fires-once ({link}).\n" in text
    assert f"C: accessibility ({link}).\n" in text
    assert f"D: the rules ({link}).\n" in text
    assert f"E: click-fires-once ({link}).\n" in text
    assert ("F: NEEDS REVIEW: unresolved link "
            "mini-repo://cookbook/components/button#nope/also-nope.\n") in text
    assert f"G: click-fires-once ({link}).\n" in text
    assert ")/" not in text and ")#" not in text
    assert _meta(repo / "cookbook" / "site-menu")["meta"]["related"] == [BUTTON]
    assert [n for n in report.needs_review if "button#" in n] == [
        "site-menu: mini-repo://cookbook/components/button#nope/also-nope"]


def test_upgrade_absorbs_a_trailing_slash_after_a_fragment(git_tmp_path):
    def mutate(repo):
        _append(repo / "cookbook" / "site-menu" / "overview.md",
                "\nA: [x](mini-repo://cookbook/components/button#states/).\n"
                "B: mini-repo://cookbook/components/button#states/ end.\n")
    repo = _repo(git_tmp_path, "v1-repo", mutate)
    [report] = up.upgrade(repo)
    text = (repo / "cookbook" / "site-menu" / "overview.md").read_text(encoding="utf-8")
    link = f"[mini-repo.ingredient.components.button](cookbook:{BUTTON})"
    assert f"A: x ({link}).\n" in text
    assert f"B: states ({link}) end.\n" in text
    assert ")/" not in text
    assert not any("button#" in n for n in report.needs_review)


def test_upgrade_resolves_a_section_fragment_in_a_foreign_cookbook(git_tmp_path, tmp_path_factory):
    cb = _foreign_adc(tmp_path_factory.mktemp("elsewhere"))
    guide = cb / "guidelines" / "a11y.md"
    guide.parent.mkdir(parents=True)
    guide.write_text("---\nid: e7a40000-0000-4000-8000-0000000000aa\ntype: guideline\n"
                     "domain: agenticdevelopercookbook://guidelines/a11y\n---\n\n# A11y\n\n"
                     "## Rules\n\n- **respect-display-options**: Views MUST respect them.\n",
                     encoding="utf-8")

    def mutate(repo):
        _append(repo / "cookbook" / "site-menu" / "overview.md",
                "\nSee agenticdevelopercookbook://guidelines/a11y#respect-display-options.\n"
                "And [the rules](agenticdevelopercookbook://guidelines/a11y#rules).\n")
    repo = _repo(git_tmp_path, "v1-repo", mutate)
    [report] = up.upgrade(repo)
    text = (repo / "cookbook" / "site-menu" / "overview.md").read_text(encoding="utf-8")
    link = (f"[adc.guideline.a11y](cookbook:{ADC_ID}/e7a40000-0000-4000-8000-0000000000aa)")
    assert f"See respect-display-options ({link}).\n" in text
    assert f"And the rules ({link}).\n" in text
    assert not any("a11y" in n for n in report.needs_review)


def test_upgrade_leaves_a_uri_that_names_no_artifact_as_text(git_tmp_path, tmp_path_factory):
    # A bare scheme or folder mention in prose links to nothing: wrapping it as
    # NEEDS REVIEW mid-sentence garbles the row, so it stays, listed apart.
    _foreign_adc(tmp_path_factory.mktemp("elsewhere"))
    row = ("| 1.2.2 | Moved specs out of mini-repo://recipes/ and mini-repo://cookbook/components, "
           "citing agenticdevelopercookbook://compliance/ and mini-repo://cookbook/ |\n")

    def mutate(repo):
        _append(repo / "cookbook" / "site-menu" / "history.md", row +
                "| 1.2.3 | See mini-repo://cookbook/components/button/ and mini-repo://nope/ "
                "but mini-repo://cookbook/nope |\n")
    repo = _repo(git_tmp_path, "v1-repo", mutate)
    [report] = up.upgrade(repo)
    text = (repo / "cookbook" / "site-menu" / "history.md").read_text(encoding="utf-8")
    assert row in text
    assert (f"| 1.2.3 | See [mini-repo.ingredient.components.button](cookbook:{BUTTON}) "
            "and mini-repo://nope/ but NEEDS REVIEW: unresolved link mini-repo://cookbook/nope |\n"
            ) in text
    assert report.left_as_text == [
        "site-menu: mini-repo://recipes/", "site-menu: mini-repo://cookbook/components",
        "site-menu: agenticdevelopercookbook://compliance/", "site-menu: mini-repo://cookbook/",
        "site-menu: mini-repo://nope/"]
    assert "site-menu: mini-repo://cookbook/nope" in report.needs_review
    assert not any("recipes/" in n or "compliance/" in n or "cookbook/c" in n
                   for n in report.needs_review)


def test_upgrade_rewrites_relative_links_to_artifact_docs(git_tmp_path):
    # Compiled docs are not committed, so a link to a sibling's `.md` breaks;
    # it is resolved from where this artifact's own doc sits and stored by UUID.
    def mutate(repo):
        cb = repo / "cookbook"
        _append(cb / "components" / "chat-composer" / "overview.md",
                "\nSee [button](button.md) and [the card](../blocks/stat-card.md). "
                "Keep [notes](../notes.md), [a section](button.md#states) "
                "and [a site](https://x.test/a.md).\n")
    repo = _repo(git_tmp_path, "v1-repo", mutate)
    [report] = up.upgrade(repo)
    text = (repo / "cookbook" / "components" / "chat-composer" / "overview.md").read_text(
        encoding="utf-8")
    assert f"See [mini-repo.ingredient.components.button](cookbook:{BUTTON}) and " in text
    # A label that says more than the target's name stays, as text beside the link.
    assert f"the card ([mini-repo.ingredient.blocks.stat-card](cookbook:{STAT_CARD})). " in text
    assert "Keep [notes](../notes.md), [a section](button.md#states) " in text
    assert "[a site](https://x.test/a.md)" in text
    assert not any("notes.md" in n for n in report.needs_review)


def test_upgrade_resolves_dotted_pre_move_names(git_tmp_path):
    def mutate(repo):
        _set_meta(repo / "cookbook" / "site-menu",
                  related=["ingredient.ui.component.chat-composer", "recipe.x.button"])
    repo = _repo(git_tmp_path, "v1-repo", mutate)
    [report] = up.upgrade(repo)
    assert _meta(repo / "cookbook" / "site-menu")["meta"]["related"][0] == COMPOSER
    assert "site-menu: recipe.x.button" in report.needs_review  # wrong kind: not a match


def test_upgrade_summarises_unknown_schemes(git_tmp_path):
    repo = _repo(git_tmp_path, "v1-repo")
    [report] = up.upgrade(repo, dry_run=True)
    line = ("scheme 'agenticdevelopercookbook' is not known — "
            "upgrade that cookbook first, then rerun")
    assert report.needs_review.count(line) == 1
    assert any(n.startswith("site-menu: agenticdevelopercookbook://") for n in report.needs_review)
    assert not any("scheme 'mini-repo'" in n for n in report.needs_review)


def test_upgrade_marks_unresolvable_link_needs_review(git_tmp_path):
    repo = _repo(git_tmp_path, "v1-repo", _linked)
    [report] = up.upgrade(repo)
    meta = _meta(repo / "cookbook" / "site-menu")["meta"]
    assert meta["related"][1] == "NEEDS REVIEW: unresolved link mini-repo://cookbook/nope"
    text = (repo / "cookbook" / "site-menu" / "overview.md").read_text(encoding="utf-8")
    assert "Gone: NEEDS REVIEW: unresolved link mini-repo://cookbook/gone.\n" in text
    assert "site-menu: mini-repo://cookbook/nope" in report.needs_review
    assert "site-menu: mini-repo://cookbook/gone" in report.needs_review
    # No catalog is reachable for the adc compliance citations: they are flagged, not guessed.
    compliance = (repo / "cookbook" / "site-menu" / "compliance.md").read_text(encoding="utf-8")
    assert ("NEEDS REVIEW: unresolved link [separation-of-concerns](agenticdevelopercookbook://"
            "compliance/best-practices#separation-of-concerns)") in compliance


def _foreign_adc(tmp_path: Path) -> Path:
    """A format-1 cookbook (no index.json) with a compliance catalog, remembered by scheme."""
    root = tmp_path / "adc-checkout"
    cb = root / "cookbook"
    cb.mkdir(parents=True)
    (cb / "cookbook.json").write_text(json.dumps({"id": ADC_ID}), encoding="utf-8")
    catalog = root / "tbd" / "compliance"
    catalog.mkdir(parents=True)
    (catalog / "best-practices.md").write_text(
        "# Best practices\n\n### separation-of-concerns\n\nx\n\n### unit-test-coverage\n\ny\n",
        encoding="utf-8")
    remember_location(CookbookIdentity(ADC_ID, "adc"), cb, "agenticdevelopercookbook")
    return cb


def test_upgrade_resolves_foreign_scheme_through_locations(git_tmp_path, tmp_path_factory):
    _foreign_adc(tmp_path_factory.mktemp("elsewhere"))
    repo = _repo(git_tmp_path, "v1-repo")
    [report] = up.upgrade(repo)
    check = check_uuid(ADC_ID, "best-practices", "unit-test-coverage")
    text = (repo / "cookbook" / "site-menu" / "compliance.md").read_text(encoding="utf-8")
    assert (f"[adc.check.best-practices.unit-test-coverage](cookbook:{ADC_ID}/{check})"
            in text)
    assert not any("agenticdevelopercookbook" in n for n in report.needs_review)
    index = load_index(repo / "cookbook")
    assert index.foreign[f"{ADC_ID}/{check}"] == "adc.check.best-practices.unit-test-coverage"
    config = load_repo_config(repo)
    assert config.dependencies == {ADC_ID: Dependency(ADC_ID, "adc", None)}



def test_upgrade_keeps_a_named_label_on_a_foreign_link(git_tmp_path, tmp_path_factory):
    _foreign_adc(tmp_path_factory.mktemp("elsewhere"))

    def mutate(repo):
        p = repo / "cookbook" / "site-menu" / "compliance.md"
        p.write_text(p.read_text(encoding="utf-8").replace(
            "[unit-test-coverage](", "[tests cover it](", 1), encoding="utf-8")
    repo = _repo(git_tmp_path, "v1-repo", mutate)
    up.upgrade(repo)
    check = check_uuid(ADC_ID, "best-practices", "unit-test-coverage")
    text = (repo / "cookbook" / "site-menu" / "compliance.md").read_text(encoding="utf-8")
    assert (f"| tests cover it ([adc.check.best-practices.unit-test-coverage]"
            f"(cookbook:{ADC_ID}/{check})) |") in text
    # The fragment is the check's own name: that label collapses.
    sep = check_uuid(ADC_ID, "best-practices", "separation-of-concerns")
    assert f"| [adc.check.best-practices.separation-of-concerns](cookbook:{ADC_ID}/{sep}) |" in text

def test_resolver_derives_a_format_1_dependency_index(tmp_path):
    cb = _foreign_adc(tmp_path)
    own = Index(CookbookIdentity(COOKBOOK_ID, "mini-repo"))
    resolver = Resolver(tmp_path, own, {})
    found = resolver.index_for(ADC_ID)
    assert found is not None and found.cookbook == CookbookIdentity(ADC_ID, "adc")
    assert check_uuid(ADC_ID, "best-practices", "separation-of-concerns") in found.entries
    assert not (cb / "index.json").exists()


def test_resolver_treats_an_underivable_dependency_as_unreachable(tmp_path):
    cb = tmp_path / "noid" / "cookbook"
    cb.mkdir(parents=True)
    other = "abcdef00-0000-4000-8000-000000000000"
    resolver = Resolver(tmp_path, Index(CookbookIdentity(COOKBOOK_ID, "mini-repo")),
                        {other: Dependency(other, "x", "noid/cookbook")})
    assert resolver.index_for(other) is None


# ── legacy repo (.cookr.json + recipes/) ─────────────────────────────────────

def _legacy(repo: Path) -> None:
    for slug, uid in LEGACY_IDS.items():
        p = repo / "recipes" / f"{slug}.md"
        p.write_text(p.read_text(encoding="utf-8").replace("---\n", f"---\nid: {uid}\n", 1),
                     encoding="utf-8")
    site = repo / "recipes" / "site-menu.md"
    site.write_text(site.read_text(encoding="utf-8").replace(
        "status: accepted\n",
        "status: accepted\ndepends-on: [mini-repo://recipes/toolbar-button, mini-repo://recipes/composer]\n", 1)
        + "\nSee mini-repo://recipes/stat-card.\n", encoding="utf-8")
    config = json.loads((repo / ".cookr.json").read_text(encoding="utf-8"))
    config["renames"] = {"web/components/chat-composer.tsx": "composer"}
    config["aliases"]["composer"] = "chat-composer"
    config["roots"].append({"path": "web/moved-away", "tier": "gone", "platform": "web"})
    (repo / ".cookr.json").write_text(json.dumps(config, indent=2), encoding="utf-8")


def test_upgrade_resolves_pre_move_domain_through_aliases(git_tmp_path, tmp_path_factory):
    _foreign_adc(tmp_path_factory.mktemp("elsewhere"))  # button.md cites adc compliance checks
    repo = _repo(git_tmp_path, "legacy-repo", _legacy)
    [report] = up.upgrade(repo)
    index = load_index(repo / "cookbook")
    site = repo / "cookbook" / index.entries[LEGACY_IDS["site-menu"]].path
    meta = _meta(site)["meta"]
    assert meta["depends-on"] == [LEGACY_IDS["button"], LEGACY_IDS["chat-composer"]]
    body = "".join(f.read_text(encoding="utf-8") for f in sorted(site.glob("*.md")))
    assert f"See [mini-repo.ingredient.blocks.stat-card](cookbook:{LEGACY_IDS['stat-card']})." in body
    assert report.needs_review == []


def test_dry_run_reports_what_the_real_run_reports(git_tmp_path, tmp_path_factory):
    def mutate(repo):
        _legacy(repo)
        (repo / "recipes" / "notes.txt").write_text("keep me\n", encoding="utf-8")
    _foreign_adc(tmp_path_factory.mktemp("elsewhere"))
    repo = _repo(git_tmp_path, "legacy-repo", mutate)
    [dry] = up.upgrade(repo, dry_run=True)
    assert _status(repo) == ""
    [real] = up.upgrade(repo)
    assert "recipes/notes.txt: left in the legacy recipes dir" in dry.needs_review
    assert dry.needs_review == real.needs_review
    assert (dry.artifacts, dry.links_rewritten, dry.moved_legacy, dry.dropped_roots) == (
        real.artifacts, real.links_rewritten, real.moved_legacy, real.dropped_roots)
    assert (repo / "recipes" / "notes.txt").is_file()


def test_upgrade_moves_legacy_recipes_into_cookbook(git_tmp_path):
    repo = _repo(git_tmp_path, "legacy-repo", _legacy)
    [report] = up.upgrade(repo)
    assert not (repo / "recipes").exists()
    index = load_index(repo / "cookbook")
    paths = {k: e.path for k, e in index.entries.items() if e.kind != "check"}
    assert paths == {LEGACY_IDS["button"]: "ui", LEGACY_IDS["chat-composer"]: "components/chat-composer",
                     LEGACY_IDS["site-menu"]: "site-menu", LEGACY_IDS["stat-card"]: "blocks/stat-card"}
    for uid, path in paths.items():
        assert _meta(repo / "cookbook" / path)["meta"]["id"] == uid
    button = [(i.platform, i.location) for i in index.entries[LEGACY_IDS["button"]].implementations]
    assert button == [("apple", "apple/UI/"), ("web", "web/components/Button.tsx")]
    assert report.moved_legacy == 4
    assert report.dropped_roots == ["web/moved-away"]
    config = load_repo_config(repo)
    assert [r.path for r in config.roots] == ["web/components", "web/blocks", "apple/UI"]
    assert json.loads((repo / ".cookr.json").read_text(encoding="utf-8"))["format"] == 2
    assert config.identity == report.identity
    assert not list(repo.rglob("*.md.tmp"))


def test_upgrade_merges_legacy_rows_into_a_counterpart(git_tmp_path):
    def mutate(repo):
        _legacy(repo)
        # button already lives in cookbook/ (same UUID); its legacy copy only adds a row.
        shutil.copytree(FIXTURES / "v1-repo" / "cookbook", repo / "cookbook")
        _set_meta(repo / "cookbook" / "components" / "button", id=LEGACY_IDS["button"])
        (repo / "web" / "extra.tsx").write_text("x\n", encoding="utf-8")
        p = repo / "recipes" / "button.md"
        _append(p, "\n## Reference Implementations\n\n| Platform | Path |\n|---|---|\n"
                   "| web | `web/extra.tsx` |\n")
        for slug in ("chat-composer", "stat-card", "site-menu"):
            (repo / "recipes" / f"{slug}.md").unlink()
    repo = _repo(git_tmp_path, "legacy-repo", mutate)
    [report] = up.upgrade(repo)
    index = load_index(repo / "cookbook")
    entry = index.entries[LEGACY_IDS["button"]]
    assert entry.path == "components/button"
    assert [i.location for i in entry.implementations] == [
        "web/components/Button.tsx", "apple/UI/", "web/extra.tsx"]
    assert not (repo / "cookbook" / "ui").exists()
    assert not (repo / "recipes").exists()
    assert report.moved_legacy == 1


# ── repo config ──────────────────────────────────────────────────────────────

def test_upgrade_splits_apple_root_by_path(git_tmp_path):
    def mutate(repo):
        for d in ("apple/macOS/Views", "apple/Shared/iOS"):
            (repo / d).mkdir(parents=True)
            (repo / d / "View.swift").write_text("struct V {}\n", encoding="utf-8")
        manifest = repo / "cookbook" / "cookbook.json"
        data = json.loads(manifest.read_text(encoding="utf-8"))
        data["code"]["roots"] += [
            {"path": "apple/macOS/Views", "platform": "apple", "kind": "ui", "recipes": "ui"},
            {"path": "apple/Shared/iOS", "platform": "apple", "kind": "logic", "recipes": "ui"},
            {"path": "apple/Gone", "platform": "apple", "kind": "ui", "recipes": "ui"},
        ]
        manifest.write_text(json.dumps(data, indent=2), encoding="utf-8")
    repo = _repo(git_tmp_path, "v1-repo", mutate)
    [report] = up.upgrade(repo)
    platforms = {r.path: r.platform for r in load_repo_config(repo).roots}
    assert platforms["apple/macOS/Views"] == "macos"
    assert platforms["apple/Shared/iOS"] == "ios"
    assert platforms["apple/UI"] == "apple"
    assert report.dropped_roots == ["apple/Gone"]


def test_upgrade_merges_code_roots_with_legacy_roots(git_tmp_path):
    def mutate(repo):
        _legacy(repo)
        (repo / "web" / "extra").mkdir()
        (repo / "web" / "extra" / "Extra.tsx").write_text("x\n", encoding="utf-8")
        (repo / "cookbook").mkdir()
        (repo / "cookbook" / "cookbook.json").write_text(json.dumps({"code": {
            "roots": [
                {"path": "web/extra", "platform": "web", "kind": "ui", "recipes": "extra",
                 "ignore": ["*.gen.tsx"]},
                # Also a legacy root, with another kind and group: the code block wins.
                {"path": "web/components", "platform": "web", "kind": "logic",
                 "recipes": "widgets", "ignore": ["*.old.tsx"]},
                {"path": "web/gone", "platform": "web", "kind": "ui", "recipes": "gone"},
            ],
            "ignore": ["**/Generated/**", "**/index.ts"]}}), encoding="utf-8")
        config = json.loads((repo / ".cookr.json").read_text(encoding="utf-8"))
        config["roots"][0]["ignore"] = ["*.draft.tsx"]  # web/components, root-scoped
        (repo / ".cookr.json").write_text(json.dumps(config, indent=2), encoding="utf-8")
    repo = _repo(git_tmp_path, "legacy-repo", mutate)
    [report] = up.upgrade(repo)
    config = load_repo_config(repo)
    roots = {r.path: r for r in config.roots}
    assert list(roots) == ["web/extra", "web/components", "web/blocks", "apple/UI"]
    assert (roots["web/components"].kind, roots["web/components"].group) == ("logic", "widgets")
    assert roots["web/components"].ignore == ("*.old.tsx", "*.draft.tsx")
    assert roots["web/extra"].ignore == ("*.gen.tsx",)
    assert roots["web/blocks"].ignore == ()
    # A legacy root's group is where the upgrade placed its recipes (organize's placement).
    assert (roots["web/blocks"].platform, roots["web/blocks"].group) == ("web", "blocks")
    assert (roots["apple/UI"].platform, roots["apple/UI"].kind) == ("apple", "ui")
    assert config.ignore == ["**/Generated/**", "**/index.ts", "**/*.stories.tsx"]
    assert sorted(report.dropped_roots) == ["web/gone", "web/moved-away"]
    assert report.root_conflicts == [
        "web/components: kind logic (cookbook.json code) over ui (legacy .cookr.json)",
        "web/components: group widgets (cookbook.json code) over components (legacy .cookr.json)"]


def test_a_root_listed_twice_in_one_source_says_so(git_tmp_path):
    def mutate(repo):
        _legacy(repo)
        (repo / "cookbook").mkdir()
        (repo / "cookbook" / "cookbook.json").write_text(json.dumps({"code": {"roots": [
            {"path": "web/components", "platform": "web", "kind": "logic"},
            {"path": "web/components", "platform": "web", "kind": "ui"}]}}), encoding="utf-8")
    repo = _repo(git_tmp_path, "legacy-repo", mutate)
    [report] = up.upgrade(repo)
    assert ("web/components: kind logic over ui, listed twice in cookbook.json code; "
            "kept the first") in report.root_conflicts


def test_upgrade_recompiles_a_committed_doc_and_writes_none_where_none_was(git_tmp_path):
    # The repo's choice stands: a compiled doc committed beside its folder is
    # rewritten as `cookr compile --target doc` writes it (with the index's
    # Reference Implementations, `synced` recorded); a folder without one gets none.
    from cookr.core.artifact import CURRENT, compose_document, doc_path, sync_state
    from cookr.core.artifact_build import compile_doc

    def mutate(repo):
        _linked(repo)
        for rel in ("components/button", "site-menu"):
            folder = repo / "cookbook" / rel
            doc_path(folder).write_text(compose_document(up._load_folder(folder)),
                                        encoding="utf-8")
    repo = _repo(git_tmp_path, "v1-repo", mutate)
    [report] = up.upgrade(repo)
    cb = repo / "cookbook"
    with_doc = [cb / "components" / "button", cb / "site-menu"]
    results = compile_doc(with_doc, base=repo, write=False)
    assert [r.status for r in results] == ["unchanged", "unchanged"]
    assert [sync_state(f) for f in with_doc] == [CURRENT, CURRENT]
    assert "web/components/Button.tsx" in doc_path(with_doc[0]).read_text(encoding="utf-8")
    assert f"(cookbook:{BUTTON})" in doc_path(with_doc[1]).read_text(encoding="utf-8")
    assert not doc_path(cb / "components" / "chat-composer").exists()
    assert not doc_path(cb / "blocks" / "stat-card").exists()
    assert set(map(doc_path, with_doc)) <= set(report.files)


def test_upgrade_writes_no_repo_config_without_roots(git_tmp_path):
    def mutate(repo):
        manifest = repo / "cookbook" / "cookbook.json"
        data = json.loads(manifest.read_text(encoding="utf-8"))
        del data["code"]
        manifest.write_text(json.dumps(data, indent=2), encoding="utf-8")
    repo = _repo(git_tmp_path, "v1-repo", mutate)
    up.upgrade(repo)
    assert not (repo / ".cookr.json").exists()


# ── safety ───────────────────────────────────────────────────────────────────

def test_upgrade_refuses_dirty_tree(git_tmp_path):
    repo = _repo(git_tmp_path, "v1-repo")
    (repo / "cookbook" / "stray.txt").write_text("wip\n", encoding="utf-8")
    before = (repo / "cookbook" / "cookbook.json").read_text(encoding="utf-8")
    with pytest.raises(up.UpgradeError) as e:
        up.upgrade(repo)
    assert "cookbook/stray.txt" in str(e.value)
    assert (repo / "cookbook" / "cookbook.json").read_text(encoding="utf-8") == before
    assert not (repo / "cookbook" / "index.json").exists()


def test_upgrade_dirty_listing_names_untracked_files_exactly(git_tmp_path):
    repo = _repo(git_tmp_path, "v1-repo")
    (repo / "new dir").mkdir()
    (repo / "new dir" / "file.txt").write_text("wip\n", encoding="utf-8")
    _git(repo, "mv", "web", "web moved")
    with pytest.raises(up.UpgradeError) as e:
        up.upgrade(repo)
    lines = [ln.strip() for ln in str(e.value).splitlines()[1:]]
    assert "new dir/file.txt" in lines
    assert "web moved/components/Button.tsx" in lines and "web/components/Button.tsx" in lines


def test_upgrade_is_idempotent(git_tmp_path):
    repo = _repo(git_tmp_path, "v1-repo", _linked)
    assert up.upgrade(repo)
    _commit_all(repo)
    assert up.upgrade(repo) == []
    assert _status(repo) == ""
    assert up.needs_upgrade(repo) == []


def test_dry_run_writes_nothing(git_tmp_path, home):
    repo = _repo(git_tmp_path, "v1-repo", _linked)
    [report] = up.upgrade(repo, dry_run=True)
    assert report.artifacts == 4 and report.needs_review
    assert _status(repo) == ""
    assert not (home / "locations.json").exists()


def test_upgrade_remembers_the_cookbook_location(git_tmp_path, home):
    repo = _repo(git_tmp_path, "v1-repo")
    up.upgrade(repo)
    locs = json.loads((home / "locations.json").read_text(encoding="utf-8"))
    assert locs[COOKBOOK_ID]["rdid"] == "mini-repo"
    assert locs[COOKBOOK_ID]["legacy_scheme"] == "mini-repo"
    assert Path(locs[COOKBOOK_ID]["path"]) == (repo / "cookbook").resolve()


def test_upgrade_converts_an_md_only_cookbook(git_tmp_path):
    repo = _repo(git_tmp_path, "md-repo")
    [report] = up.upgrade(repo, rdid="mini")
    cb = repo / "cookbook"
    assert not (cb / "components" / "button.md").exists()
    assert (cb / "components" / "button" / "artifact.json").is_file()
    index = load_index(cb)
    assert report.artifacts == 4
    assert {e.rdid for e in index.entries.values()} >= {"mini.ingredient.components.button"}
    # The docs carried no id: each gets a stable one derived from the cookbook and its path.
    again = up.derive_index(FIXTURES / "md-repo" / "cookbook")
    assert set(again.entries) == set(index.entries)


def test_needs_upgrade_lists_the_cookbook(git_tmp_path):
    repo = _repo(git_tmp_path, "v1-repo")
    assert up.needs_upgrade(repo) == [repo / "cookbook"]


def test_needs_upgrade_lists_a_legacy_repo(git_tmp_path):
    repo = _repo(git_tmp_path, "legacy-repo")
    assert up.needs_upgrade(repo) == [repo / "cookbook"]


def test_needs_upgrade_ignores_a_repo_without_a_cookbook(tmp_path):
    (tmp_path / "src").mkdir()
    assert up.needs_upgrade(tmp_path) == []


# ── derive_index ─────────────────────────────────────────────────────────────

def _map(index: Index) -> dict:
    return {k: (e.kind, e.rdid, e.path) for k, e in index.entries.items()}


def test_derive_index_matches_upgrade(git_tmp_path):
    derived = up.derive_index(FIXTURES / "v1-repo" / "cookbook")
    repo = _repo(git_tmp_path, "v1-repo")
    up.upgrade(repo)
    assert _map(derived) == _map(load_index(repo / "cookbook"))
    assert derived.cookbook == CookbookIdentity(COOKBOOK_ID, "mini-repo")


def test_derive_index_without_an_identity_needs_upgrade(tmp_path):
    cb = tmp_path / "cookbook"
    cb.mkdir()
    with pytest.raises(up.NeedsUpgrade):
        up.derive_index(cb)


# ── CLI ──────────────────────────────────────────────────────────────────────

def test_cli_upgrade_json(git_tmp_path, capsys):
    repo = _repo(git_tmp_path, "v1-repo")
    assert main(["-p", str(repo), "upgrade", "--json"]) == 0
    [data] = json.loads(capsys.readouterr().out)
    assert data["artifacts"] == 4 and data["identity"] == {"id": COOKBOOK_ID, "rdid": "mini-repo"}
    assert "cookbook/index.json" in data["files"]
    assert data["root_conflicts"] == [] and data["left_as_text"] == []
    assert data["self_links_dropped"] == []


def test_cli_upgrade_dry_run_and_up_to_date(git_tmp_path, capsys):
    repo = _repo(git_tmp_path, "v1-repo")
    assert main(["-p", str(repo), "upgrade", "--dry-run"]) == 0
    assert "dry run" in capsys.readouterr().out
    assert _status(repo) == ""
    assert main(["-p", str(repo), "upgrade"]) == 0
    _commit_all(repo)
    assert main(["-p", str(repo), "upgrade"]) == 0
    assert "up to date" in capsys.readouterr().out


def test_cli_upgrade_refuses_dirty_tree(git_tmp_path, capsys):
    repo = _repo(git_tmp_path, "v1-repo")
    (repo / "stray.txt").write_text("x\n", encoding="utf-8")
    assert main(["-p", str(repo), "upgrade"]) == 2
    out = " ".join(capsys.readouterr().out.split())
    assert "stray.txt" in out
    assert "WIP commit" in out and "stash" not in out


def test_a_compile_failure_mid_write_says_how_to_restore(git_tmp_path, monkeypatch):
    """Files were already written: the error must not claim otherwise, and the
    restore it names must bring back the clean tree the upgrade started from."""
    from types import SimpleNamespace

    repo = _repo(git_tmp_path, "v1-repo")
    failed = SimpleNamespace(status="error", source=repo / "cookbook" / "x", detail="boom",
                             dest=None)
    monkeypatch.setattr(up, "compile_doc", lambda *a, **k: [failed])
    with pytest.raises(up.UpgradeError) as e:
        up.upgrade(repo)
    message = str(e.value)
    assert "already written" in message
    assert "git checkout -- . && git clean -fd" in message
    assert _status(repo) != ""
    _git(repo, "checkout", "--", ".")
    _git(repo, "clean", "-fd")
    assert _status(repo) == ""


# ── a format-2 .cookr.json is kept ───────────────────────────────────────────

DEP_ID = "0d000000-0000-4000-8000-0000000000d1"


def _moved_cookbook(repo: Path, name: str, config: dict) -> None:
    """v1-repo with its cookbook at `name`, named by a format-2 `.cookr.json`."""
    (repo / name).parent.mkdir(parents=True, exist_ok=True)
    shutil.move(str(repo / "cookbook"), str(repo / name))
    (repo / ".cookr.json").write_text(json.dumps({"format": 2, **config}), encoding="utf-8")


def test_upgrade_keeps_a_config_naming_a_custom_cookbook_dir(git_tmp_path, capsys):
    repo = _repo(git_tmp_path, "v1-repo", lambda r: _moved_cookbook(r, "docs/cb", {
        "cookbook": "docs/cb", "ignore": ["extra/**"],
        "dependencies": {DEP_ID: {"rdid": "dep", "location": "vendor/dep/cookbook"}}}))
    [report] = up.upgrade(repo)
    assert report.cookbook_dir == repo / "docs" / "cb"
    assert not (repo / "cookbook").exists()
    cfg = load_repo_config(repo)
    assert cfg.cookbook == "docs/cb"
    assert cfg.identity.id == COOKBOOK_ID  # the existing cookbook, never a new one
    assert cfg.dependencies[DEP_ID].location == "vendor/dep/cookbook"
    assert "extra/**" in cfg.ignore and "**/index.ts" in cfg.ignore
    assert {r.path for r in cfg.roots} == {"web/components", "web/blocks", "apple/UI"}
    assert repo / ".cookr.json" in report.files
    _commit_all(repo)
    # Every command finds the cookbook where the config says it is.
    assert main(["-p", str(repo), "inventory"]) == 0
    capsys.readouterr()
    main(["-p", str(repo), "validate"])
    out = " ".join(capsys.readouterr().out.split())
    assert "Could not find a cookbook root" not in out
    assert "All 4 source folders compile" in out


def test_upgrade_keeps_the_format_2_config_roots_over_the_code_block(git_tmp_path):
    root = {"path": "web/components", "platform": "web", "kind": "logic", "group": "widgets"}
    repo = _repo(git_tmp_path, "v1-repo", lambda r: (r / ".cookr.json").write_text(
        json.dumps({"format": 2, "roots": [root]}), encoding="utf-8"))
    [report] = up.upgrade(repo)
    kept = next(r for r in load_repo_config(repo).roots if r.path == "web/components")
    assert (kept.kind, kept.group) == ("logic", "widgets")
    assert any("format-2 .cookr.json" in c for c in report.root_conflicts)


def test_upgrade_keeps_an_ignore_only_config(git_tmp_path):
    def strip_code(r):
        m = r / "cookbook" / "cookbook.json"
        data = json.loads(m.read_text())
        data.pop("code")
        m.write_text(json.dumps(data))
        (r / ".cookr.json").write_text(json.dumps({"format": 2, "ignore": ["gen/**"]}))
    repo = _repo(git_tmp_path, "v1-repo", strip_code)
    up.upgrade(repo)
    assert load_repo_config(repo).ignore == ["gen/**"]


@pytest.mark.parametrize("name", ["nope/missing", "../outside", "/abs/cb"])
def test_upgrade_refuses_a_config_naming_no_cookbook(git_tmp_path, name, capsys):
    repo = _repo(git_tmp_path, "v1-repo", lambda r: (r / ".cookr.json").write_text(
        json.dumps({"format": 2, "cookbook": name}), encoding="utf-8"))
    before = (repo / ".cookr.json").read_text()
    with pytest.raises(CookbookError) as e:
        up.upgrade(repo)
    assert "`cookbook`" in str(e.value)
    assert main(["-p", str(repo), "validate"]) == 2  # upgrade-on-contact refuses too
    assert "`cookbook`" in " ".join(capsys.readouterr().out.split())
    assert main(["-p", str(repo), "check", "--staged", "--hook"]) == 2  # the hook's run
    assert "`cookbook`" in " ".join(capsys.readouterr().err.split())
    assert (repo / ".cookr.json").read_text() == before
    assert not (repo / "nope").exists() and not (repo.parent / "outside").exists()
    assert _status(repo) == ""
