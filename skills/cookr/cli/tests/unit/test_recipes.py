from __future__ import annotations

import pytest
from cookbook.core.errors import CookbookError

from cookr.core.recipes import load_corpus, spec_id


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


def test_spec_id_is_the_relative_path_without_the_md_suffix(mini_repo):
    cookbook = mini_repo / "cookbook"
    assert spec_id(cookbook / "components" / "button.md", cookbook) == "components/button"
    assert spec_id(cookbook / "site-menu.md", cookbook) == "site-menu"


def test_same_named_files_in_different_directories_do_not_collide(mini_repo):
    # Corpus keys are full cookbook-relative paths, so two files that share a
    # stem in different directories are two distinct specs, not a collision.
    (mini_repo / "cookbook" / "components" / "sub").mkdir()
    (mini_repo / "cookbook" / "components" / "sub" / "button.md").write_text(
        "---\ntype: ingredient\nstatus: draft\n---\n", encoding="utf-8")
    corpus = load_corpus(mini_repo / "cookbook")
    assert {"components/button", "components/sub/button"} <= set(corpus)


def test_corpus_skips_index_and_template(mini_repo):
    (mini_repo / "cookbook" / "INDEX.md").write_text("# index\n", encoding="utf-8")
    (mini_repo / "cookbook" / "_template.md").write_text("---\ntype: ingredient\n---\n", encoding="utf-8")
    corpus = load_corpus(mini_repo / "cookbook")
    assert "INDEX" not in corpus
    assert "_template" not in corpus


def test_invalid_yaml_frontmatter_is_a_cookbook_error_naming_the_file(mini_repo):
    (mini_repo / "cookbook" / "extra.md").write_text("---\ntitle: a: b\n---\n# x\n", encoding="utf-8")
    with pytest.raises(CookbookError, match="extra.md"):
        load_corpus(mini_repo / "cookbook")


def test_non_utf8_recipe_is_a_cookbook_error_naming_the_file(mini_repo):
    (mini_repo / "cookbook" / "latin.md").write_bytes(b"---\ntitle: caf\xe9\n---\n")
    with pytest.raises(CookbookError, match="latin.md"):
        load_corpus(mini_repo / "cookbook")
