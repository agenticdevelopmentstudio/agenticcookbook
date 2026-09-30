"""Write the skillgen source fixtures: a tiny cookbook and a tiny recipes repo.

The trees are generated rather than committed file by file so that each doc's
purpose sits next to its content. Run it after changing a fixture, then
regenerate the golden output with `UPDATE_GOLDEN=1 pytest tests/unit/test_skillgen_build.py`.
"""

from __future__ import annotations

import json
import shutil
from pathlib import Path

HERE = Path(__file__).resolve().parent


def fm(title: str, doc_type: str, summary: str, **extra: object) -> str:
    lines = ["---", f"title: {title}", f"type: {doc_type}", f"summary: {summary}"]
    for key, value in extra.items():
        if isinstance(value, list):
            lines.append(f"{key}:")
            lines += [f"  - {v}" for v in value]
        else:
            lines.append(f"{key}: {value}")
    return "\n".join(lines + ["---", ""])


INPUT_VALIDATION = """\
# Input validation

Validate at the boundary.

- **validate-at-boundary**: Every handler MUST validate its input before use.
- **reject-unknown-fields** (api): Parsers SHOULD reject fields they do not know.
- Error messages MUST NOT echo raw input back to the caller.

| ID | Requirements |
|----|--------------|
| iv-1 | `validate-at-boundary` |
| iv-2 | `reject-unknown-fields`, `validate-at-boundary` |

## Change History

| Version | Date | Change |
|---------|------|--------|
| 1.0.0 | 2026-01-01 | Initial |
"""

COOKBOOK = {
    "principles/simplicity.md": fm("Simplicity", "principle", "Prefer fewer moving parts.")
    + "# Simplicity\n\nPrefer the design with fewer moving parts.\n",
    "guidelines/reviewing/security/input-validation.md": fm(
        "Input validation", "guideline", "Validate untrusted input at the boundary.",
        platforms=["web", "macos"], triggers=["handler", "parser"],
    ) + INPUT_VALIDATION,
    # Identical body under another use case: emitted once, aliased here.
    "guidelines/implementing/security/input-validation.md": fm(
        "Input validation", "guideline", "Validate untrusted input at the boundary.",
    ) + INPUT_VALIDATION,
    # Same guideline, different body: drift, emitted separately and reported.
    "guidelines/testing/security/input-validation.md": fm(
        "Input validation", "guideline", "Test the validation boundary.",
    ) + "# Input validation\n\nTests MUST cover a rejected payload.\n",
    "guidelines/reviewing/naming.md": fm("Naming", "guideline", "Names say what, not how.")
    + "# Naming\n\n1. Names SHOULD say what a thing is.\n2. Abbreviations MAY be used when universal.\n\n"
    "See [the glossary](../../introduction/glossary.md) for terms.\n",
    "recipes/ui/login-form.md": fm("Login form", "recipe", "A sign-in form with states.")
    + "# Login form\n\n## Overview\n\nThe form MUST submit on Return.\n\n"
    "## States\n\n- **empty**: The submit button MUST be disabled.\n- **error**: The error SHOULD name the field.\n\n"
    "## Accessibility\n\n_None yet._\n\n## Change History\n\n- 1.0.0 initial\n",
    "introduction/conventions.md": fm("Conventions", "reference", "How the cookbook is written.")
    + "# Conventions\n\nFiles MUST have frontmatter.\n",
    "guidelines/reviewing/README.md": "# Reviewing\n\nNo frontmatter here.\n",
}

RECIPES = {
    **{
        f"recipes/status-server-{name}.md": fm(f"Status server {name}", "recipe", f"The {name} endpoint.",
                                               references=[f"src/server/{name}.ts (toolkit)"])
        + f"# Status server {name}\n\nThe {name} endpoint MUST return JSON.\n"
        for name in ("health", "metrics", "sessions", "events")
    },
    "recipes/tab-view.md": fm("Tab view", "recipe", "A tab strip.") + "# Tab view\n\nTabs SHOULD scroll.\n",
    "recipes/notes.md": fm("Notes", "recipe", "Loose notes.") + "# Notes\n\nNothing normative.\n",
}


def write_tree(root: Path, files: dict[str, str]) -> None:
    if root.exists():
        shutil.rmtree(root)
    for rel, text in files.items():
        path = root / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")


def main() -> None:
    write_tree(HERE / "cookbook-src" / "cookbook", COOKBOOK)
    write_tree(HERE / "recipes-src", RECIPES)
    (HERE / "recipes-src" / ".cookr.json").write_text(
        json.dumps({"recipes": "recipes", "scheme": "toolkit", "roots": ["src"]}, indent=2) + "\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
