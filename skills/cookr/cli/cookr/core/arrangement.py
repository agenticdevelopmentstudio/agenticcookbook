"""Does each spec sit where its code's arrangement puts it?

A spec's place follows from its first platform's Reference Implementations
(`inventory.expected_name`): one source file is `<group of its directory>/<its
stem>`, one directory is the module's own name, and several rows share the
group their paths have in common, with any leaf (or none, when
`inventory.join_name` collapsed it). A spec is `aligned` when its name (one
row) or its group (several rows) matches, `drifted` when it does not,
`unplaced` when it has no row, and `outside` when a row is under no `code.roots`
entry. A drifted spec either moves in the cookbook, or its code moves and
`cookr relink` follows.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from .config import Config
from .inventory import expected_name, in_group
from .recipes import RecipeInfo, load_corpus

STATES = ("aligned", "drifted", "unplaced", "outside")


@dataclass(frozen=True)
class Placement:
    name: str
    state: str
    expected: str  # the expected name (one row) or group (several, ending `/`); "" when unknown


def _common(names: list[str]) -> str:
    split = [n.split("/") for n in names]
    out = []
    for column in zip(*split):
        if len(set(column)) != 1:
            break
        out.append(column[0])
    return "/".join(out)


def place(config: Config, name: str, info: RecipeInfo) -> Placement:
    impls = info.implementations
    if not impls:
        return Placement(name, "unplaced", "")
    rows = [i for i in impls if i.platform == impls[0].platform]
    expected = []
    for row in rows:
        root = config.root_for(row.path.rstrip("/"))
        if root is None:
            return Placement(name, "outside", "")
        expected.append(expected_name(root, row.path))
    if len(expected) == 1:
        return Placement(name, "aligned" if name == expected[0] else "drifted", expected[0])
    # Several rows: each file's group, each directory's module name.
    groups = [e if r.is_dir else e.rsplit("/", 1)[0] if "/" in e else ""
              for r, e in zip(rows, expected)]
    group = _common(groups)
    here = name.rsplit("/", 1)[0] if "/" in name else ""
    # A leaf that repeated the group's last directory collapsed into it (`join_name`).
    return Placement(name, "aligned" if group in (here, name) else "drifted", group + "/")


def report(config: Config, tier: Optional[str] = None,
           corpus: Optional[dict[str, RecipeInfo]] = None) -> list[Placement]:
    corpus = load_corpus(config.cookbook_dir) if corpus is None else corpus
    return [place(config, name, info) for name, info in sorted(corpus.items())
            if in_group(name, tier)]
