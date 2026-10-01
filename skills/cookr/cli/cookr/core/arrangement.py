"""Does each spec sit in the concept group its code's roots map to?

A library cookbook groups specs by concept, not by the code's directory layout,
so a spec's place follows from the `recipes` group of each `code.roots` entry
its first platform's Reference Implementations rows fall under. A spec is
`aligned` when its name is that group or sits anywhere inside it (at any depth,
since a concept group has its own sub-groups), `drifted` when it is inside none
of them, `unplaced` when it has no row, and `outside` when a row is under no
`code.roots` entry. A drifted spec either moves into its group in the cookbook,
or its root's `recipes` changes.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from .config import Config
from .inventory import in_group
from .recipes import RecipeInfo, load_corpus

STATES = ("aligned", "drifted", "unplaced", "outside")


@dataclass(frozen=True)
class Placement:
    name: str
    state: str
    expected: str  # the expected groups, each ending `/`, comma-separated; "" when unknown


def _under(name: str, group: str) -> bool:
    return not group or name == group or name.startswith(group + "/")


def place(config: Config, name: str, info: RecipeInfo) -> Placement:
    impls = info.implementations
    if not impls:
        return Placement(name, "unplaced", "")
    groups: list[str] = []
    for row in (i for i in impls if i.platform == impls[0].platform):
        root = config.root_for(row.path.rstrip("/"))
        if root is None:
            return Placement(name, "outside", "")
        if root.recipes not in groups:
            groups.append(root.recipes)
    expected = ", ".join(g + "/" for g in groups)
    return Placement(name, "aligned" if any(_under(name, g) for g in groups) else "drifted", expected)


def report(config: Config, tier: Optional[str] = None,
           corpus: Optional[dict[str, RecipeInfo]] = None) -> list[Placement]:
    corpus = load_corpus(config.cookbook_dir) if corpus is None else corpus
    return [place(config, name, info) for name, info in sorted(corpus.items())
            if in_group(name, tier)]
