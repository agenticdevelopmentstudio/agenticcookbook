"""`cookr roles gaps`: the sentences of a reference text that an artifact's
topic does not hold (core/gaps.py)."""

from __future__ import annotations

import json

import pytest

from cookr.cli import main
from cookr.core import gaps

from .cookbook_helpers import add_doc, new_repo

pytestmark = pytest.mark.usefixtures("git_tmp_path")

REL = "guidelines/implementing/data/keys"
BODY = """# Keys

Every foreign key column must carry an index of its own.

Primary keys are chosen once and never reused for another row.

## Change History

x
"""


def topic(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    new_repo(tmp_path)
    return add_doc(tmp_path, REL, BODY, type="guideline")


def reference(tmp_path, text, name="reference.txt"):
    path = tmp_path / name
    path.write_text(text, encoding="utf-8")
    return path


def run_gaps(capsys, monkeypatch, *argv):
    monkeypatch.setenv("COLUMNS", "300")
    capsys.readouterr()
    code = main(["roles", "gaps", *map(str, argv)])
    cap = capsys.readouterr()
    return code, cap.out, cap.err


def only(data):
    [ref] = data["references"]
    return ref


def test_gaps_counts_a_sentence_the_topic_lacks(tmp_path, monkeypatch, capsys):
    folder = topic(tmp_path, monkeypatch)
    ref = reference(tmp_path, "Every foreign key column must carry an index of its own.\n"
                              "Cascade deletes are declared explicitly on every relationship.\n")
    code, out, _ = run_gaps(capsys, monkeypatch, folder, "--against", ref, "--json")
    assert code == 0
    r = only(json.loads(out))
    assert (r["sentences"], r["held"], r["lacking"]) == (2, 1, 1)
    assert r["lacking_sentences"] == ["Cascade deletes are declared explicitly on every relationship."]


def test_gaps_counts_a_reworded_sentence_as_held(tmp_path, monkeypatch, capsys):
    # Not a substring of the topic, and one word of nine ("always") is not in it: 8/9 >= 80 %.
    folder = topic(tmp_path, monkeypatch)
    sentence = "Every key column must carry its own index always."
    assert "always" not in gaps.topic_text(folder).split()
    assert gaps.normalise(sentence) not in gaps.topic_text(folder)
    ref = reference(tmp_path, sentence + "\n")
    code, out, _ = run_gaps(capsys, monkeypatch, folder, "--against", ref, "--json")
    r = only(json.loads(out))
    assert code == 0 and (r["sentences"], r["held"], r["lacking"]) == (1, 1, 0)


def test_gaps_ignores_a_sentence_under_six_words(tmp_path, monkeypatch, capsys):
    folder = topic(tmp_path, monkeypatch)
    ref = reference(tmp_path, "Shard the whole cluster.\nCascade deletes are declared explicitly on every "
                              "relationship.\n")
    code, out, _ = run_gaps(capsys, monkeypatch, folder, "--against", ref, "--json")
    r = only(json.loads(out))
    assert (r["sentences"], r["lacking"]) == (1, 1)


@pytest.mark.parametrize("fence", ["```", "~~~", "````"])
def test_gaps_ignores_a_code_fence(tmp_path, monkeypatch, capsys, fence):
    # ~~~ and longer fences too (review f7): a fence is what history.without_fences says it is
    folder = topic(tmp_path, monkeypatch)
    ref = reference(tmp_path, f"{fence}sql\nCREATE INDEX child_parent_idx ON child (parent_id, created_at, x);\n{fence}\n")
    code, out, _ = run_gaps(capsys, monkeypatch, folder, "--against", ref, "--json")
    r = only(json.loads(out))
    assert code == 0 and r["sentences"] == 0


def test_gaps_does_not_read_the_research_folder(tmp_path, monkeypatch, capsys):
    folder = topic(tmp_path, monkeypatch)
    sentence = "Cascade deletes are declared explicitly on every relationship."
    (folder / "research").mkdir()
    (folder / "research" / "research.md").write_text(sentence + "\n", encoding="utf-8")
    ref = reference(tmp_path, sentence + "\n")
    code, out, _ = run_gaps(capsys, monkeypatch, folder, "--against", ref, "--json")
    assert only(json.loads(out))["lacking"] == 1


def test_gaps_reports_the_original_wording(tmp_path, monkeypatch, capsys):
    folder = topic(tmp_path, monkeypatch)
    original = "- **Cascade** deletes are declared EXPLICITLY on every relationship (always)!"
    ref = reference(tmp_path, original + "\n")
    code, out, _ = run_gaps(capsys, monkeypatch, folder, "--against", ref, "--json")
    assert only(json.loads(out))["lacking_sentences"] == [original]
    code, out, _ = run_gaps(capsys, monkeypatch, folder, "--against", ref)
    assert code == 0 and original in out


def test_gaps_reports_each_reference_file(tmp_path, monkeypatch, capsys):
    folder = topic(tmp_path, monkeypatch)
    one = reference(tmp_path, "Every foreign key column must carry an index of its own.\n", "one.txt")
    two = reference(tmp_path, "Cascade deletes are declared explicitly on every relationship.\n", "two.txt")
    code, out, _ = run_gaps(capsys, monkeypatch, folder, "--against", one, "--against", two, "--json")
    data = json.loads(out)
    assert code == 0
    assert [(r["file"], r["lacking"]) for r in data["references"]] == [(str(one), 0), (str(two), 1)]
    code, out, _ = run_gaps(capsys, monkeypatch, folder, "--against", one, "--against", two)
    assert code == 0 and str(one) in out and str(two) in out


def test_gaps_on_a_path_that_is_not_an_artifact_exits_2(tmp_path, monkeypatch, capsys):
    folder = topic(tmp_path, monkeypatch)
    ref = reference(tmp_path, "Cascade deletes are declared explicitly on every relationship.\n")
    typo = folder.parent / "kyes"
    code, out, err = run_gaps(capsys, monkeypatch, typo, "--against", ref, "--json")
    assert code == 2 and "kyes" in out + err


def test_gaps_on_a_missing_reference_file_exits_2(tmp_path, monkeypatch, capsys):
    folder = topic(tmp_path, monkeypatch)
    code, out, err = run_gaps(capsys, monkeypatch, folder, "--against", tmp_path / "nope.txt")
    assert code == 2 and "nope.txt" in out + err


def test_gaps_needs_a_reference(tmp_path, monkeypatch, capsys):
    folder = topic(tmp_path, monkeypatch)
    with pytest.raises(SystemExit) as e:
        main(["roles", "gaps", str(folder)])
    assert e.value.code == 2


# --- The measure's rules, each pinned at its boundary -------------------------

def measured(tmp_path, monkeypatch, capsys, text):
    folder = topic(tmp_path, monkeypatch)
    ref = reference(tmp_path, text)
    code, out, _ = run_gaps(capsys, monkeypatch, folder, "--against", ref, "--json")
    assert code == 0
    return folder, only(json.loads(out))


def test_gaps_holds_a_sentence_with_exactly_eight_of_ten_words(tmp_path, monkeypatch, capsys):
    sentence = "Every foreign key column must carry an index zebra yak."
    folder, r = measured(tmp_path, monkeypatch, capsys, sentence + "\n")
    words = set(gaps.topic_text(folder).split())
    norm = gaps.normalise(sentence)
    assert sum(w in words for w in norm.split()) == 8 and len(norm.split()) == 10
    assert norm not in gaps.topic_text(folder)
    assert (r["sentences"], r["held"], r["lacking"]) == (1, 1, 0)


def test_gaps_lacks_a_sentence_with_seven_of_ten_words(tmp_path, monkeypatch, capsys):
    sentence = "Every foreign key column must carry an zebra yak gnu."
    folder, r = measured(tmp_path, monkeypatch, capsys, sentence + "\n")
    words = set(gaps.topic_text(folder).split())
    norm = gaps.normalise(sentence)
    assert sum(w in words for w in norm.split()) == 7 and len(norm.split()) == 10
    assert (r["sentences"], r["held"], r["lacking"]) == (1, 0, 1)


def test_gaps_drops_a_five_word_sentence(tmp_path, monkeypatch, capsys):
    _, r = measured(tmp_path, monkeypatch, capsys, "Cascade deletes declared every relationship.\n")
    assert r["sentences"] == 0


def test_gaps_counts_a_six_word_sentence(tmp_path, monkeypatch, capsys):
    _, r = measured(tmp_path, monkeypatch, capsys, "Cascade deletes declared on every relationship.\n")
    assert (r["sentences"], r["lacking"]) == (1, 1)


def test_gaps_splits_after_a_semicolon_and_a_colon(tmp_path, monkeypatch, capsys):
    _, r = measured(tmp_path, monkeypatch, capsys, "a b c d e f; g h i j k l: m n o p q r\n")
    assert r["lacking_sentences"] == ["a b c d e f;", "g h i j k l:", "m n o p q r"]


def test_gaps_reads_a_wrapped_sentence_as_one(tmp_path, monkeypatch, capsys):
    # A single newline inside a paragraph is not the end of a sentence.
    _, r = measured(tmp_path, monkeypatch, capsys,
                    "Cascade deletes are declared explicitly on every relationship and\n"
                    "are reviewed with the schema\n")
    assert r["lacking_sentences"] == [
        "Cascade deletes are declared explicitly on every relationship and are reviewed with the schema"]


def test_gaps_splits_at_a_blank_line_without_punctuation(tmp_path, monkeypatch, capsys):
    _, r = measured(tmp_path, monkeypatch, capsys,
                    "Cascade deletes are declared explicitly everywhere\n\n"
                    "Orphaned rows are swept by a nightly job\n")
    assert r["lacking_sentences"] == ["Cascade deletes are declared explicitly everywhere",
                                      "Orphaned rows are swept by a nightly job"]


def test_gaps_splits_at_each_list_item(tmp_path, monkeypatch, capsys):
    # A numbered item's "2." is cut off by the punctuation rule, a one-word piece that is dropped.
    _, r = measured(tmp_path, monkeypatch, capsys,
                    "Cascade deletes are declared explicitly everywhere\n"
                    "- Orphaned rows are swept by a nightly job\n"
                    "  that runs after the backup\n"
                    "2. Soft deletes keep a tombstone column always\n")
    assert r["lacking_sentences"] == ["Cascade deletes are declared explicitly everywhere",
                                      "- Orphaned rows are swept by a nightly job that runs after the backup",
                                      "Soft deletes keep a tombstone column always"]


def test_gaps_splits_at_a_heading(tmp_path, monkeypatch, capsys):
    _, r = measured(tmp_path, monkeypatch, capsys,
                    "Cascade deletes are declared explicitly everywhere\n"
                    "## Orphaned rows are swept by nightly jobs\n"
                    "Soft deletes keep a tombstone column always\n")
    assert r["lacking_sentences"] == ["Cascade deletes are declared explicitly everywhere",
                                      "## Orphaned rows are swept by nightly jobs",
                                      "Soft deletes keep a tombstone column always"]


def test_gaps_holds_a_substring_whose_edge_words_are_partial(tmp_path, monkeypatch, capsys):
    # Only "of its own primary" are topic words (4 of 6), so only the substring rule holds it.
    sentence = "Ex of its own primary ke."
    folder, r = measured(tmp_path, monkeypatch, capsys, sentence + "\n")
    text = gaps.topic_text(folder)
    assert gaps.normalise(sentence) in text
    assert sum(w in set(text.split()) for w in gaps.normalise(sentence).split()) == 4
    assert (r["sentences"], r["held"]) == (1, 1)


def test_gaps_prints_each_lacking_sentence_on_its_own_line(tmp_path, monkeypatch, capsys):
    folder = topic(tmp_path, monkeypatch)
    one = "Cascade deletes are declared explicitly on every relationship."
    two = "Orphaned rows are swept by a nightly job."
    ref = reference(tmp_path, f"{one}\n{two}\n")
    code, out, _ = run_gaps(capsys, monkeypatch, folder, "--against", ref)
    lines = out.splitlines()
    assert code == 0
    assert f"{ref}: 2 sentence(s), 0 held, 2 lacking" in lines
    assert f"  lacking: {one}" in lines and f"  lacking: {two}" in lines


def test_gaps_reads_each_table_row_as_its_own_block(tmp_path, monkeypatch, capsys):
    _, r = measured(tmp_path, monkeypatch, capsys,
                    "Cascade deletes are declared explicitly everywhere\n"
                    "| Rule | Why it matters to every table |\n"
                    "|---|---|\n"
                    "| Orphaned rows swept nightly | they leak storage over time |\n")
    assert r["lacking_sentences"] == ["Cascade deletes are declared explicitly everywhere",
                                      "| Rule | Why it matters to every table |",
                                      "| Orphaned rows swept nightly | they leak storage over time |"]
