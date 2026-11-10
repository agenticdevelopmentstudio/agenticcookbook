from __future__ import annotations

import pytest
from cookr.core.errors import CookbookError

from cookr.core.recipes import load_corpus, spec_id

from .cookbook_helpers import add_spec


def test_corpus_keys_are_cookbook_relative_paths(mini_repo):
    corpus = load_corpus(mini_repo / "cookbook")
    assert set(corpus) == {"components/button", "blocks/stat-card", "components/chat-composer", "site-menu"}


def test_corpus_reads_type_and_status(mini_repo):
    corpus = load_corpus(mini_repo / "cookbook")
    assert corpus["components/button"].type == "ingredient"
    assert corpus["components/button"].status == "accepted"
    assert corpus["site-menu"].type == "recipe"


def test_corpus_carries_the_parsed_frontmatter(mini_repo):
    # completeness grades `platforms`/`modified` from info.data instead of re-parsing the file
    info = load_corpus(mini_repo / "cookbook")["components/button"]
    assert info.data["type"] == "ingredient"
    assert info.data["status"] == "accepted"


def test_recipe_infos_slug_matches_its_corpus_key(mini_repo):
    corpus = load_corpus(mini_repo / "cookbook")
    assert corpus["components/button"].slug == "components/button"
    assert corpus["blocks/stat-card"].slug == "blocks/stat-card"


def test_spec_id_is_the_folders_cookbook_relative_path(mini_repo):
    cookbook = mini_repo / "cookbook"
    assert spec_id(cookbook / "components" / "button", cookbook) == "components/button"
    assert spec_id(cookbook / "site-menu", cookbook) == "site-menu"


def test_same_named_folders_in_different_directories_do_not_collide(mini_repo):
    # Corpus keys are full cookbook-relative paths, so two folders that share a
    # name in different directories are two distinct specs, not a collision.
    add_spec(mini_repo, "components/sub/button")
    corpus = load_corpus(mini_repo / "cookbook")
    assert {"components/button", "components/sub/button"} <= set(corpus)
    assert corpus["components/sub/button"].rdid == "mini-repo.ingredient.components.sub.button"


def test_corpus_carries_each_specs_rdid_and_implementations(mini_repo):
    info = load_corpus(mini_repo / "cookbook")["components/chat-composer"]
    assert info.rdid == "mini-repo.ingredient.components.chat-composer"
    assert [(i.platform, i.location) for i in info.implementations] == [
        ("web", "web/components/chat-composer.tsx")]


def test_corpus_skips_index_and_template(mini_repo):
    (mini_repo / "cookbook" / "INDEX.md").write_text("# index\n", encoding="utf-8")
    (mini_repo / "cookbook" / "_template.md").write_text("---\ntype: ingredient\n---\n", encoding="utf-8")
    corpus = load_corpus(mini_repo / "cookbook")
    assert "INDEX" not in corpus
    assert "_template" not in corpus


def test_unreadable_artifact_is_a_cookbook_error_naming_the_folder(mini_repo):
    extra = mini_repo / "cookbook" / "extra"
    extra.mkdir()
    (extra / "artifact.json").write_text("{not json", encoding="utf-8")
    with pytest.raises(CookbookError, match="extra"):
        load_corpus(mini_repo / "cookbook")


def test_non_utf8_part_is_a_cookbook_error_naming_the_folder(mini_repo):
    (mini_repo / "cookbook" / "site-menu" / "intro.md").write_bytes(b"# caf\xe9\n")
    with pytest.raises(CookbookError, match="site-menu"):
        load_corpus(mini_repo / "cookbook")
