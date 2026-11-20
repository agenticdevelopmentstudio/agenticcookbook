"""The gap measure: which sentences of a reference text an artifact's topic does
not hold. `cookr roles gaps` runs it; the caller supplies the reference text.

- A text is normalised by lowercasing it and turning every run of characters
  outside `[a-z0-9]` into one space.
- Its sentences are what is left once fenced code blocks are dropped, cut
  into blocks and each block split after `.`, `!`, `?`, `;` or `:` followed by
  whitespace. A block ends at a blank line, before a list item (`-`, `*`, `+`,
  `1.`, `1)`), and around a heading line (`#`) or a table row (`|`), each its
  own block; any other newline is a wrapped line and joins the next with a
  space, so it never ends a sentence. A sentence counts only when its
  normalised form has MIN_WORDS words or more.
- The topic text is every `*.md` directly in the artifact folder, joined and
  normalised (never `research/`, which is not part of the topic).
- A sentence is HELD when its normalised form is a substring of the topic text,
  or at least HELD_SHARE of its words are among the topic's words; otherwise
  the topic LACKS it.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path

from .artifact import ARTIFACT_FILE, is_folder
from .errors import CookbookError
from .history import without_fences

MIN_WORDS = 6
HELD_SHARE = 0.8

_SPLIT = re.compile(r"(?<=[.!?;:])\s+")
_LIST_ITEM = re.compile(r"\s*(?:[-*+]|\d+[.)])\s")
_HEADING = re.compile(r"\s*#{1,6}\s")
_TABLE_ROW = re.compile(r"\s*\|")
_NON_WORD = re.compile(r"[^a-z0-9]+")


class GapsError(CookbookError):
    """An argument the gap measure cannot use; nothing was measured."""


@dataclass
class Gap:
    """One reference file measured against the topic."""
    file: str
    sentences: int = 0
    held: int = 0
    lacking_sentences: list[str] = field(default_factory=list)

    @property
    def lacking(self) -> int:
        return len(self.lacking_sentences)

    def as_json(self) -> dict:
        return {"file": self.file, "sentences": self.sentences, "held": self.held,
                "lacking": self.lacking, "lacking_sentences": list(self.lacking_sentences)}


def normalise(text: str) -> str:
    return _NON_WORD.sub(" ", text.lower()).strip()


def blocks(text: str) -> list[str]:
    """`text` cut at blank lines, list items, headings and table rows, wrapped lines joined."""
    found: list[str] = []
    lines: list[str] = []

    def close() -> None:
        if lines:
            found.append(" ".join(lines))
            lines.clear()

    for line in text.splitlines():
        if not line.strip():
            close()
        elif _HEADING.match(line) or _TABLE_ROW.match(line):
            close()
            found.append(line.strip())
        else:
            if _LIST_ITEM.match(line):
                close()
            lines.append(line.strip())
    close()
    return found


def pieces(text: str) -> list[tuple[str, str]]:
    """(original wording, normalised) for every piece `text` is cut into, in
    order: its prose blocks (fenced code left out) split after each sentence
    mark. A piece with no words is left out; one under MIN_WORDS is kept here,
    for a caller that shows what `sentences` drops (grow-cookbook's run_gaps)."""
    return [(piece.strip(), norm) for block in blocks(without_fences(text))
            for piece in _SPLIT.split(block) if (norm := normalise(piece))]


def sentences(text: str) -> list[tuple[str, str]]:
    """(original wording, normalised) for each counted sentence of `text`."""
    return [(p, norm) for p, norm in pieces(text) if len(norm.split()) >= MIN_WORDS]


def topic_text(folder: Path) -> str:
    """The artifact's own text, normalised: its `*.md` files, not `research/`."""
    return normalise(" ".join(f.read_text(encoding="utf-8") for f in sorted(folder.glob("*.md"))))


def held(sentence: str, topic: str, words: set[str]) -> bool:
    """Whether a normalised sentence is held by the normalised topic text."""
    if sentence in topic:
        return True
    w = sentence.split()
    return sum(1 for x in w if x in words) / len(w) >= HELD_SHARE


def measure(folder: Path, references: list[Path]) -> list[Gap]:
    """Each reference file measured against `folder`'s topic, in order."""
    if not is_folder(folder):
        raise GapsError(f"{folder}: not an artifact source folder (no {ARTIFACT_FILE})")
    texts = []
    for ref in references:
        try:
            texts.append(ref.read_text(encoding="utf-8"))
        except (OSError, UnicodeDecodeError) as e:
            raise GapsError(f"--against {ref}: cannot read it ({e.__class__.__name__})") from e
    topic = topic_text(folder)
    words = set(topic.split())
    result = []
    for ref, text in zip(references, texts):
        gap = Gap(str(ref))
        for original, norm in sentences(text):
            gap.sentences += 1
            if held(norm, topic, words):
                gap.held += 1
            else:
                gap.lacking_sentences.append(original)
        result.append(gap)
    return result
