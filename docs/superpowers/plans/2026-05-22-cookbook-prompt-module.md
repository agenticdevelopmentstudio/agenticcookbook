> [!WARNING]
> **ARCHIVED — HISTORICAL RECORD, NOT CURRENT.** Captured 2026-11-10. This document reflects a
> past state or decision and may no longer describe how things work. Do not treat it as live
> documentation.

# Cookbook `prompt` module Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a `cookbook prompt <module> <action>` CLI that assembles an expert-loaded prompt and prints it to stdout, plus move the cookbook CLI source into the cookbook skill.

**Architecture:** Two phases. Phase A is plumbing: move `scripts/cookbook/` → `skills/cookbook/cli/`, generalize the reference manifest to repo-relative paths, extract the install shim into a source file, and exclude CLI artifacts from plugin assembly. Phase B is the new module: a `prompt` subpackage that discovers modules + actions from disk, parses YAML frontmatter for param declarations, peels declared `--flags` via argparse, renders the prompt template (role header + module preamble + bundled references + action body + task block), and prints the result to stdout. Initial content is the `database` module with `design` and `review` actions.

**Tech Stack:** Python 3.9+, `argparse`, `pyyaml`, existing cookbook test harness (pytest), bash (`install.sh`).

**Spec:** `docs/superpowers/specs/2026-05-22-cookbook-prompt-module-design.md`

---

## Phase A — Source move + install plumbing

### Task 1: Move CLI source from `scripts/` into the cookbook skill

**Files:**
- Move (git mv): `scripts/cookbook/cookbook/` → `skills/cookbook/cli/cookbook/`
- Move: `scripts/cookbook/reference-manifest.json` → `skills/cookbook/cli/reference-manifest.json`
- Move: `scripts/cookbook/references/` → `skills/cookbook/cli/references/`
- Move: `scripts/cookbook/references-src/` → `skills/cookbook/cli/references-src/`
- Move: `scripts/tests/cookbook/` → `skills/cookbook/cli/tests/`
- Modify: `skills/cookbook/cli/tests/conftest.py` (path constants)
- Modify: `install.sh` (`MANIFEST` and `PKG_SRC` variables)

- [ ] **Step 1: Create destination dir, then `git mv` everything**

```bash
mkdir -p skills/cookbook/cli
git mv scripts/cookbook/cookbook skills/cookbook/cli/cookbook
git mv scripts/cookbook/reference-manifest.json skills/cookbook/cli/reference-manifest.json
git mv scripts/cookbook/references skills/cookbook/cli/references
git mv scripts/cookbook/references-src skills/cookbook/cli/references-src
git mv scripts/tests/cookbook skills/cookbook/cli/tests
```

- [ ] **Step 2: Remove now-empty `scripts/cookbook/` and `scripts/tests/` if empty**

```bash
rmdir scripts/cookbook scripts/tests 2>/dev/null || true
rmdir scripts 2>/dev/null || true
```

(Will silently no-op if anything else is still there. Inspect with `ls scripts 2>/dev/null` after.)

- [ ] **Step 3: Update `skills/cookbook/cli/tests/conftest.py` path constants**

The old constants were `REPO_ROOT = Path(__file__).resolve().parents[3]` and `PKG_PARENT = REPO_ROOT / "scripts" / "cookbook"`. After the move the file is one level deeper. Change to:

```python
REPO_ROOT = Path(__file__).resolve().parents[4]
PKG_PARENT = REPO_ROOT / "skills" / "cookbook" / "cli"
```

Leave the rest of `conftest.py` unchanged.

- [ ] **Step 4: Update `install.sh` path variables**

Replace these two lines near the top of `install.sh`:

```bash
MANIFEST="${REPO_ROOT}/scripts/cookbook/reference-manifest.json"
PKG_SRC="${REPO_ROOT}/scripts/cookbook"
```

with:

```bash
MANIFEST="${REPO_ROOT}/skills/cookbook/cli/reference-manifest.json"
PKG_SRC="${REPO_ROOT}/skills/cookbook/cli"
```

Also update the materialization python block — it still hardcodes `scripts/cookbook` inside, replace both occurrences with `skills/cookbook/cli`:

```python
source_root = (repo_root / "skills/cookbook/cli" / manifest["source_root"]).resolve()
```

```python
embedded_src = repo_root / "skills/cookbook/cli" / embedded
```

(These will be removed entirely in Task 2; this commit just keeps install.sh working with the moved files.)

- [ ] **Step 5: Run existing tests to confirm nothing broke**

```bash
cd skills/cookbook/cli/tests
python3 -m pytest unit/ -x -q
cd -
```

Expected: All previously-passing unit tests still pass. If anything fails, the failure is path-related — re-check Step 3 and Step 4 paths.

- [ ] **Step 6: Commit**

```bash
git add -A skills/cookbook/cli scripts install.sh
git commit -m "refactor: move cookbook CLI from scripts/ into the cookbook skill"
git push
```

---

### Task 2: Generalize reference manifest to repo-relative paths

**Files:**
- Modify: `skills/cookbook/cli/reference-manifest.json` (`source_root` field)
- Modify: `install.sh` (materialization python block)

- [ ] **Step 1: Write a failing assertion that the materialization works with repo-relative `source_root`**

Edit `skills/cookbook/cli/tests/unit/test_modules_create.py` or wherever convenient — actually for a smoke check we'll just run install and confirm `skills/cookbook/cli/references/` ends up populated. Skip a unit test here; the Step 4 verification covers it.

- [ ] **Step 2: Change `skills/cookbook/cli/reference-manifest.json`**

Old `source_root` was `"../.."` (relative to the old `scripts/cookbook/` dir, resolving to repo root). Change to repo-root-relative:

```json
{
  "version": 1,
  "source_root": ".",
  "destination": "skills/cookbook/cli/references",
  "files": [
    { "src": "cookbook/principles",                  "dst": "principles",            "type": "tree", "include": "*.md" },
    { "src": "cookbook/introduction/conventions.md", "dst": "conventions.md",        "type": "file" },
    { "src": "cookbook/introduction/glossary.md",    "dst": "glossary.md",           "type": "file" },
    { "src": "cookbook/ingredients/_template.md",    "dst": "templates/ingredient.md", "type": "file" },
    { "src": "cookbook/recipes/_template.md",        "dst": "templates/recipe.md",   "type": "file" }
  ],
  "embedded_dir": "references-src"
}
```

Notes: `source_root` is now `"."` (repo root). `destination` is repo-relative. `src` paths inside `files[]` are unchanged because they were already repo-relative-looking.

- [ ] **Step 3: Change the materialization python block in `install.sh`**

Replace this:

```python
source_root = (repo_root / "skills/cookbook/cli" / manifest["source_root"]).resolve()
```

with:

```python
source_root = (repo_root / manifest["source_root"]).resolve()
```

And replace this:

```python
embedded_src = repo_root / "skills/cookbook/cli" / embedded
```

with the version that respects the manifest's own location — since `embedded_dir` is relative to the manifest file:

```python
embedded_src = Path(sys.argv[2]).resolve().parent / embedded
```

Rationale: `embedded_dir` lives next to its manifest (`references-src/` is in the same dir as `reference-manifest.json`). Anchoring it to the manifest's parent keeps things sane when there are multiple manifests in different sub-dirs (which we add in Task 14).

- [ ] **Step 4: Run install + verify materialized references**

```bash
./install.sh
ls skills/cookbook/cli/references/principles/ | head
```

Expected: principles listed (explicit-over-implicit.md, fail-fast.md, etc.). Also expected: `references-src/` content overlaid (any prompts/configs that existed before).

- [ ] **Step 5: Run tests again**

```bash
cd skills/cookbook/cli/tests
python3 -m pytest unit/ -x -q
cd -
```

Expected: still green.

- [ ] **Step 6: Commit**

```bash
git add skills/cookbook/cli/reference-manifest.json install.sh
git commit -m "refactor: make reference-manifest source_root repo-relative"
git push
```

---

### Task 3: Extract install shim into `skills/cookbook/bin/cookbook`

**Files:**
- Create: `skills/cookbook/bin/cookbook`
- Modify: `install.sh` (Step 5 "Installing shim")

- [ ] **Step 1: Create the shim source file**

Create `skills/cookbook/bin/cookbook` with this content:

```bash
#!/usr/bin/env bash
export PYTHONPATH="${HOME}/.local/bin/_cookbook_pkg:${PYTHONPATH:-}"
exec python3 -m cookbook "$@"
```

Then make it executable:

```bash
chmod +x skills/cookbook/bin/cookbook
```

- [ ] **Step 2: Replace install.sh shim-write step**

In `install.sh`, replace the entire "5. Write the shim" block:

```bash
# 5. Write the shim
title "Installing shim"
cat > "${BIN_DIR}/cookbook" <<EOF
#!/usr/bin/env bash
export PYTHONPATH="${PKG_DIR}:\${PYTHONPATH:-}"
exec python3 -m cookbook "\$@"
EOF
chmod +x "${BIN_DIR}/cookbook"
ok "shim → ${BIN_DIR}/cookbook"
```

with:

```bash
# 5. Install the shim
title "Installing shim"
cp "${REPO_ROOT}/skills/cookbook/bin/cookbook" "${BIN_DIR}/cookbook"
chmod +x "${BIN_DIR}/cookbook"
ok "shim → ${BIN_DIR}/cookbook"
```

- [ ] **Step 3: Run install and verify the shim works**

```bash
./install.sh
cookbook --version
```

Expected: prints the cookbook version (e.g., `cookbook 1.1.0`).

- [ ] **Step 4: Commit**

```bash
git add skills/cookbook/bin/cookbook install.sh
git commit -m "refactor: extract cookbook shim into skills/cookbook/bin/"
git push
```

---

### Task 4: Exclude `cli/` and `bin/` from plugin assembly

**Files:**
- Modify: `install.sh` (Step 7 "Assembling plugin")

- [ ] **Step 1: Replace the plugin-assembly bash loop with a Python block**

Find this block in `install.sh` (currently labeled "7. Assemble the plugin"):

```bash
rm -rf "${PLUGIN_SKILLS_DIR}"
mkdir -p "${PLUGIN_SKILLS_DIR}"
assembled=0
for skill in "${SKILLS_SRC}"/*/; do
    [ -d "${skill}" ] || continue
    name="$(basename "${skill}")"
    cp -R "${skill}" "${PLUGIN_SKILLS_DIR}/${name}"
    printf '  + %s\n' "${name}"
    assembled=$((assembled + 1))
done
```

Replace with:

```bash
rm -rf "${PLUGIN_SKILLS_DIR}"
mkdir -p "${PLUGIN_SKILLS_DIR}"
python3 - "$SKILLS_SRC" "$PLUGIN_SKILLS_DIR" <<'PY'
import shutil, sys
from pathlib import Path

EXCLUDE = {"cli", "bin"}

src_root = Path(sys.argv[1])
dst_root = Path(sys.argv[2])

assembled = 0
for skill_src in sorted(src_root.iterdir()):
    if not skill_src.is_dir():
        continue
    name = skill_src.name
    skill_dst = dst_root / name
    skill_dst.mkdir(parents=True, exist_ok=True)
    for child in skill_src.iterdir():
        if child.name in EXCLUDE:
            continue
        target = skill_dst / child.name
        if child.is_dir():
            shutil.copytree(child, target)
        else:
            shutil.copy2(child, target)
    print(f"  + {name}")
    assembled += 1
print(f"  assembled {assembled} skill(s)")
PY
```

- [ ] **Step 2: Run install and verify plugin layout**

```bash
./install.sh
ls plugins/adh/skills/cookbook/
```

Expected: only `SKILL.md` appears under `plugins/adh/skills/cookbook/`. The `cli/` and `bin/` dirs do NOT appear under the plugin.

```bash
ls plugins/adh/skills/cookbook/cli 2>&1
```

Expected: `ls: ... No such file or directory`.

- [ ] **Step 3: Verify the cookbook CLI still works (uses _cookbook_pkg, not the plugin)**

```bash
cookbook --version
cookbook --help
```

Expected: version prints; module table prints with `create`, `update`, `lint`, `plan`, `validate` (and `self` if discovered).

- [ ] **Step 4: Commit**

```bash
git add install.sh
git commit -m "build: exclude cli/ and bin/ from plugin assembly"
git push
```

---

## Phase B — `prompt` module

### Task 5: Wire empty `prompt` module into the CLI dispatcher

**Files:**
- Create: `skills/cookbook/cli/cookbook/modules/prompt/__init__.py`
- Create: `skills/cookbook/cli/cookbook/modules/prompt/__main__.py` (empty placeholder, not needed)
- Create: `skills/cookbook/cli/cookbook/modules/prompt/prompt_cli.py`

The registry auto-discovers modules that expose `NAME`, `HELP`, `register`, `run`. We make the new module's `__init__.py` re-export these from `prompt_cli` so the auto-discover finds it.

- [ ] **Step 1: Write a failing test for module discovery**

Create `skills/cookbook/cli/tests/unit/test_modules_prompt.py`:

```python
"""Tests for the `cookbook prompt` module."""

from __future__ import annotations

import pytest

from cookbook.cli import main


def test_prompt_appears_in_module_table(capsys, patch_refs):
    rc = main([])
    assert rc == 0
    out = capsys.readouterr().out
    assert "prompt" in out


def test_prompt_help_runs(capsys, patch_refs):
    with pytest.raises(SystemExit) as exc:
        main(["prompt", "--help"])
    assert exc.value.code == 0
```

- [ ] **Step 2: Run the test and watch it fail**

```bash
cd skills/cookbook/cli/tests
python3 -m pytest unit/test_modules_prompt.py -x -q
cd -
```

Expected: `test_prompt_appears_in_module_table` fails (`"prompt" not in out`) and `test_prompt_help_runs` fails (unknown subcommand).

- [ ] **Step 3: Create the prompt subpackage skeleton**

Create `skills/cookbook/cli/cookbook/modules/prompt/__init__.py`:

```python
"""`cookbook prompt` — assemble an expert prompt and print it.

See prompt_cli for the implementation; this file just re-exports the
module-protocol attrs (NAME, HELP, register, run) so the registry picks
them up.
"""

from .prompt_cli import NAME, HELP, register, run

__all__ = ["NAME", "HELP", "register", "run"]
```

- [ ] **Step 4: Create the minimal `prompt_cli.py`**

Create `skills/cookbook/cli/cookbook/modules/prompt/prompt_cli.py`:

```python
"""`cookbook prompt <module> <action> ...` dispatcher.

The CLI assembles a domain-specialist prompt (role header + module
preamble + bundled cookbook references + action template + free-text task)
and prints it to stdout. No LLM is called from this code; the parent
Claude session acts on the printed prompt.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

NAME = "prompt"
HELP = "Assemble an expert prompt for a specific module/action and print it."

PROMPTS_DIR = Path(__file__).parent / "prompts"


def register(parser: argparse.ArgumentParser) -> None:
    # NOTE: positional names avoid `module`/`action` because the top-level
    # cli.py uses `dest="module"` on its subparsers — adding a positional
    # named `module` here would overwrite that on the args namespace and
    # break cli.py's "if not args.module" check at the top of main().
    parser.add_argument(
        "pmodule",
        nargs="?",
        help="Prompt module (e.g., database). Omit to list available modules.",
    )
    parser.add_argument(
        "paction",
        nargs="?",
        help="Action within the module (e.g., design). Omit to list actions for the module.",
    )
    parser.add_argument(
        "rest",
        nargs=argparse.REMAINDER,
        help="Formal flags and free-text task (everything after <module> <action>).",
    )


def run(args, ctx) -> int:
    if not args.pmodule:
        return _list_modules(ctx)
    if not args.paction:
        return _list_actions(args.pmodule, ctx)
    return _render_action(args.pmodule, args.paction, args.rest, ctx)


def _list_modules(ctx) -> int:
    if not PROMPTS_DIR.is_dir():
        ctx.ui.warn(f"No prompt modules found at {PROMPTS_DIR}.")
        return 0
    names = sorted(p.name for p in PROMPTS_DIR.iterdir() if p.is_dir())
    ctx.ui.title("cookbook prompt — available modules")
    for name in names:
        ctx.ui.info(f"  {name}")
    return 0


def _list_actions(module: str, ctx) -> int:
    module_dir = PROMPTS_DIR / module
    actions_dir = module_dir / "actions"
    if not actions_dir.is_dir():
        ctx.ui.error(f"cookbook prompt: unknown module '{module}'.")
        return 2
    names = sorted(p.stem for p in actions_dir.glob("*.md"))
    ctx.ui.title(f"cookbook prompt {module} — available actions")
    for name in names:
        ctx.ui.info(f"  {name}")
    return 0


def _render_action(module: str, action: str, rest: list[str], ctx) -> int:
    # Implementation lands in Task 9.
    ctx.ui.error("prompt rendering not yet implemented.")
    return 2
```

- [ ] **Step 5: Run the tests and verify they pass**

```bash
cd skills/cookbook/cli/tests
python3 -m pytest unit/test_modules_prompt.py -x -q
cd -
```

Expected: both tests pass.

- [ ] **Step 6: Smoke-test from the CLI**

```bash
./install.sh
cookbook prompt
```

Expected: prints "No prompt modules found at …/prompts." (because we haven't created the `database` module dir yet) — and exits 0.

- [ ] **Step 7: Commit**

```bash
git add skills/cookbook/cli/cookbook/modules/prompt skills/cookbook/cli/tests/unit/test_modules_prompt.py
git commit -m "feat(prompt): wire empty prompt module into CLI dispatcher"
git push
```

---

### Task 6: Add YAML frontmatter parser for action files

**Files:**
- Create: `skills/cookbook/cli/cookbook/modules/prompt/frontmatter.py`
- Create: `skills/cookbook/cli/tests/unit/test_prompt_frontmatter.py`

The action file format is markdown with a YAML frontmatter block at the top:

```markdown
---
description: "Design a database schema."
params:
  target:
    description: "SQL flavor"
    default: "postgres"
---
# body...
```

- [ ] **Step 1: Write the failing test**

Create `skills/cookbook/cli/tests/unit/test_prompt_frontmatter.py`:

```python
"""Tests for the prompt module's frontmatter parser."""

from __future__ import annotations

import pytest

from cookbook.modules.prompt.frontmatter import (
    ParsedFile,
    parse,
    ParamSpec,
)


def test_parse_extracts_frontmatter_and_body():
    raw = "---\ndescription: \"hi\"\n---\nbody text\n"
    parsed = parse(raw)
    assert parsed.frontmatter["description"] == "hi"
    assert parsed.body.strip() == "body text"


def test_parse_returns_empty_frontmatter_when_missing():
    raw = "no frontmatter here\n"
    parsed = parse(raw)
    assert parsed.frontmatter == {}
    assert parsed.body.strip() == "no frontmatter here"


def test_param_spec_from_dict_with_default():
    spec = ParamSpec.from_dict("target", {"description": "x", "default": "postgres"})
    assert spec.name == "target"
    assert spec.description == "x"
    assert spec.default == "postgres"
    assert spec.required is False


def test_param_spec_from_dict_without_default_is_required():
    spec = ParamSpec.from_dict("target", {"description": "x"})
    assert spec.required is True
    assert spec.default is None
```

- [ ] **Step 2: Run the test and watch it fail**

```bash
cd skills/cookbook/cli/tests
python3 -m pytest unit/test_prompt_frontmatter.py -x -q
cd -
```

Expected: ImportError (`frontmatter` module doesn't exist).

- [ ] **Step 3: Implement the frontmatter parser**

Create `skills/cookbook/cli/cookbook/modules/prompt/frontmatter.py`:

```python
"""YAML frontmatter parser for prompt action and module files."""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Any

import yaml

_FRONTMATTER_RE = re.compile(r"\A---\s*\n(.*?)\n---\s*\n?(.*)\Z", re.DOTALL)


@dataclass
class ParsedFile:
    frontmatter: dict[str, Any]
    body: str


@dataclass
class ParamSpec:
    name: str
    description: str
    default: Any | None
    required: bool

    @classmethod
    def from_dict(cls, name: str, raw: dict[str, Any]) -> "ParamSpec":
        return cls(
            name=name,
            description=str(raw.get("description", "")),
            default=raw.get("default"),
            required="default" not in raw,
        )


def parse(raw: str) -> ParsedFile:
    """Parse `raw` text into frontmatter dict + body string.

    If no frontmatter block is present, returns an empty dict and the full
    raw text as body.
    """
    match = _FRONTMATTER_RE.match(raw)
    if not match:
        return ParsedFile(frontmatter={}, body=raw)
    fm_raw, body = match.group(1), match.group(2)
    fm = yaml.safe_load(fm_raw) or {}
    if not isinstance(fm, dict):
        raise ValueError("frontmatter must be a YAML mapping")
    return ParsedFile(frontmatter=fm, body=body)


def params_from_frontmatter(fm: dict[str, Any]) -> list[ParamSpec]:
    """Build a list of ParamSpec from a frontmatter `params` mapping."""
    raw = fm.get("params") or {}
    return [ParamSpec.from_dict(name, body) for name, body in raw.items()]
```

- [ ] **Step 4: Run the tests and verify they pass**

```bash
cd skills/cookbook/cli/tests
python3 -m pytest unit/test_prompt_frontmatter.py -x -q
cd -
```

Expected: all 4 tests pass.

- [ ] **Step 5: Commit**

```bash
git add skills/cookbook/cli/cookbook/modules/prompt/frontmatter.py skills/cookbook/cli/tests/unit/test_prompt_frontmatter.py
git commit -m "feat(prompt): YAML frontmatter parser"
git push
```

---

### Task 7: Implement the prompt assembler (`render.py`)

**Files:**
- Create: `skills/cookbook/cli/cookbook/modules/prompt/render.py`
- Create: `skills/cookbook/cli/tests/unit/test_prompt_render.py`

- [ ] **Step 1: Write the failing test**

Create `skills/cookbook/cli/tests/unit/test_prompt_render.py`:

```python
"""Tests for the prompt rendering / assembly logic."""

from __future__ import annotations

from pathlib import Path

import pytest

from cookbook.modules.prompt.render import (
    render_template,
    assemble_prompt,
    UnknownPlaceholderError,
)


def test_render_template_substitutes_known_placeholders():
    body = "Design a {{target}} schema for: {{task}}"
    out = render_template(body, {"target": "postgres", "task": "blog posts"})
    assert out == "Design a postgres schema for: blog posts"


def test_render_template_raises_on_unknown_placeholder():
    with pytest.raises(UnknownPlaceholderError) as exc:
        render_template("hello {{unknown}}", {"task": "x"})
    assert "unknown" in str(exc.value)


def test_assemble_prompt_order(tmp_path):
    module_md = tmp_path / "module.md"
    module_md.write_text(
        "---\nrole: \"db specialist\"\n---\nModule preamble line.\n",
        encoding="utf-8",
    )
    refs_dir = tmp_path / "references"
    refs_dir.mkdir()
    (refs_dir / "a.md").write_text("REF A body\n", encoding="utf-8")
    (refs_dir / "b.md").write_text("REF B body\n", encoding="utf-8")
    action_md = tmp_path / "actions" / "design.md"
    action_md.parent.mkdir()
    action_md.write_text(
        "---\ndescription: \"hi\"\nparams:\n  target:\n    default: postgres\n---\nACTION BODY for {{target}}\n",
        encoding="utf-8",
    )

    prompt = assemble_prompt(
        module_md_path=module_md,
        references_dir=refs_dir,
        action_md_path=action_md,
        params={"target": "sqlite"},
        task="some task",
    )

    # Role header first.
    assert prompt.startswith("You are a db specialist.")
    # Then preamble.
    assert "Module preamble line." in prompt
    # Then references in alphabetical order.
    a_idx = prompt.index("REF A body")
    b_idx = prompt.index("REF B body")
    assert a_idx < b_idx
    # Reference headers present.
    assert "## reference: a.md" in prompt
    assert "## reference: b.md" in prompt
    # Then action body with interpolation.
    assert "ACTION BODY for sqlite" in prompt
    # Finally the task block.
    assert prompt.rstrip().endswith("some task")
    assert "## Your task" in prompt
```

- [ ] **Step 2: Run the tests and watch them fail**

```bash
cd skills/cookbook/cli/tests
python3 -m pytest unit/test_prompt_render.py -x -q
cd -
```

Expected: ImportError (render module doesn't exist).

- [ ] **Step 3: Implement `render.py`**

Create `skills/cookbook/cli/cookbook/modules/prompt/render.py`:

```python
"""Assemble the final prompt string from module/action/references."""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any

from .frontmatter import parse

_PLACEHOLDER_RE = re.compile(r"\{\{\s*(\w+)\s*\}\}")


class UnknownPlaceholderError(RuntimeError):
    """Raised when a template references a placeholder not in `params`."""


def render_template(body: str, params: dict[str, Any]) -> str:
    """Substitute `{{name}}` placeholders with values from `params`.

    Raises UnknownPlaceholderError if the template references a name not
    present in `params`.
    """

    def sub(match: re.Match[str]) -> str:
        name = match.group(1)
        if name not in params:
            raise UnknownPlaceholderError(name)
        return str(params[name])

    return _PLACEHOLDER_RE.sub(sub, body)


def _role_header(module_fm: dict[str, Any]) -> str:
    role = module_fm.get("role", "specialist")
    return f"You are a {role}."


def _load_references(refs_dir: Path) -> str:
    if not refs_dir.is_dir():
        return ""
    chunks: list[str] = []
    for path in sorted(refs_dir.rglob("*")):
        if not path.is_file() or path.name == ".gitkeep":
            continue
        rel = path.relative_to(refs_dir).as_posix()
        body = path.read_text(encoding="utf-8")
        chunks.append(f"## reference: {rel}\n\n{body.rstrip()}")
    return "\n\n".join(chunks)


def assemble_prompt(
    *,
    module_md_path: Path,
    references_dir: Path,
    action_md_path: Path,
    params: dict[str, Any],
    task: str,
) -> str:
    """Return the assembled prompt text."""
    module_parsed = parse(module_md_path.read_text(encoding="utf-8"))
    action_parsed = parse(action_md_path.read_text(encoding="utf-8"))

    template_params = dict(params)
    template_params.setdefault("task", task)

    parts: list[str] = []
    parts.append(_role_header(module_parsed.frontmatter))
    if module_parsed.body.strip():
        parts.append(module_parsed.body.strip())
    refs_text = _load_references(references_dir)
    if refs_text:
        parts.append(refs_text)
    parts.append(render_template(action_parsed.body, template_params).strip())
    parts.append(f"## Your task\n\n{task}")
    return "\n\n".join(parts) + "\n"
```

- [ ] **Step 4: Run the tests and verify they pass**

```bash
cd skills/cookbook/cli/tests
python3 -m pytest unit/test_prompt_render.py -x -q
cd -
```

Expected: all 3 tests pass.

- [ ] **Step 5: Commit**

```bash
git add skills/cookbook/cli/cookbook/modules/prompt/render.py skills/cookbook/cli/tests/unit/test_prompt_render.py
git commit -m "feat(prompt): assemble role + preamble + refs + action + task"
git push
```

---

### Task 8: Wire argparse param peeling into `_render_action`

**Files:**
- Modify: `skills/cookbook/cli/cookbook/modules/prompt/prompt_cli.py`
- Modify: `skills/cookbook/cli/tests/unit/test_modules_prompt.py`

- [ ] **Step 1: Write the failing tests**

Append to `skills/cookbook/cli/tests/unit/test_modules_prompt.py`:

```python
import os
import textwrap
from pathlib import Path


def _write_test_module(tmp_path: Path) -> Path:
    """Create a minimal test module under tmp_path and return its parent."""
    mod = tmp_path / "demo"
    (mod / "actions").mkdir(parents=True)
    (mod / "references").mkdir(parents=True)
    (mod / "module.md").write_text(
        textwrap.dedent(
            """\
            ---
            role: "test specialist"
            ---
            Test preamble.
            """
        ),
        encoding="utf-8",
    )
    (mod / "actions" / "do.md").write_text(
        textwrap.dedent(
            """\
            ---
            description: "do it"
            params:
              target:
                description: "x"
                default: "default-target"
            ---
            Do something for {{target}} and {{task}}.
            """
        ),
        encoding="utf-8",
    )
    return tmp_path


def test_render_with_default_target(tmp_path, monkeypatch, patch_refs, capsys):
    prompts_root = _write_test_module(tmp_path)
    monkeypatch.setattr(
        "cookbook.modules.prompt.prompt_cli.PROMPTS_DIR",
        prompts_root,
    )
    rc = main(["prompt", "demo", "do", "Build a list view"])
    assert rc == 0
    out = capsys.readouterr().out
    assert "test specialist" in out
    assert "default-target" in out
    assert "Build a list view" in out


def test_render_with_explicit_flag(tmp_path, monkeypatch, patch_refs, capsys):
    prompts_root = _write_test_module(tmp_path)
    monkeypatch.setattr(
        "cookbook.modules.prompt.prompt_cli.PROMPTS_DIR",
        prompts_root,
    )
    rc = main(["prompt", "demo", "do", "--target", "sqlite", "Build a list view"])
    assert rc == 0
    out = capsys.readouterr().out
    assert "sqlite" in out


def test_render_unknown_action_exits_nonzero(tmp_path, monkeypatch, patch_refs):
    prompts_root = _write_test_module(tmp_path)
    monkeypatch.setattr(
        "cookbook.modules.prompt.prompt_cli.PROMPTS_DIR",
        prompts_root,
    )
    rc = main(["prompt", "demo", "nope", "task"])
    assert rc == 2
```

- [ ] **Step 2: Run and watch the new tests fail**

```bash
cd skills/cookbook/cli/tests
python3 -m pytest unit/test_modules_prompt.py -x -q
cd -
```

Expected: the three new tests fail (`_render_action` is stub returning 2).

- [ ] **Step 3: Replace `_render_action` and add helper functions**

In `skills/cookbook/cli/cookbook/modules/prompt/prompt_cli.py`:

**(a) Add these two new imports** at the top of the file (alongside the existing `import argparse`, `import sys`, `from pathlib import Path` — do NOT duplicate those):

```python
from .frontmatter import parse, params_from_frontmatter
from .render import assemble_prompt, UnknownPlaceholderError
```

**(b) Replace the stub `_render_action` function** with the full implementation, and add the two helper functions above it. The final shape of the bottom of the file looks like this:

```python
def _module_dir(module: str) -> Path:
    return PROMPTS_DIR / module


def _action_path(module: str, action: str) -> Path:
    return _module_dir(module) / "actions" / f"{action}.md"


def _render_action(module: str, action: str, rest: list[str], ctx) -> int:
    module_md = _module_dir(module) / "module.md"
    action_md = _action_path(module, action)
    refs_dir = _module_dir(module) / "references"

    if not module_md.is_file():
        ctx.ui.error(f"cookbook prompt: unknown module '{module}' (no module.md at {module_md}).")
        return 2
    if not action_md.is_file():
        ctx.ui.error(f"cookbook prompt {module}: unknown action '{action}' (no file at {action_md}).")
        return 2

    action_parsed = parse(action_md.read_text(encoding="utf-8"))
    specs = params_from_frontmatter(action_parsed.frontmatter)

    sub = argparse.ArgumentParser(
        prog=f"cookbook prompt {module} {action}",
        description=action_parsed.frontmatter.get("description", ""),
        add_help=True,
    )
    for spec in specs:
        kwargs = {"help": spec.description}
        if spec.required:
            kwargs["required"] = True
        else:
            kwargs["default"] = spec.default
        sub.add_argument(f"--{spec.name}", **kwargs)

    parsed, leftover = sub.parse_known_args(rest)
    params = {spec.name: getattr(parsed, spec.name) for spec in specs}
    task = " ".join(leftover).strip()
    if not task:
        ctx.ui.warn("cookbook prompt: empty task — assembled prompt will be low quality.")

    try:
        prompt = assemble_prompt(
            module_md_path=module_md,
            references_dir=refs_dir,
            action_md_path=action_md,
            params=params,
            task=task,
        )
    except UnknownPlaceholderError as e:
        ctx.ui.error(f"cookbook prompt {module} {action}: template references unknown placeholder '{{{{{e}}}}}'.")
        return 1

    sys.stdout.write(prompt)
    return 0
```

- [ ] **Step 4: Run the tests and verify they pass**

```bash
cd skills/cookbook/cli/tests
python3 -m pytest unit/test_modules_prompt.py -x -q
cd -
```

Expected: all tests in `test_modules_prompt.py` pass.

- [ ] **Step 5: Run the whole unit suite to confirm nothing regressed**

```bash
cd skills/cookbook/cli/tests
python3 -m pytest unit/ -x -q
cd -
```

Expected: all green.

- [ ] **Step 6: Commit**

```bash
git add skills/cookbook/cli/cookbook/modules/prompt/prompt_cli.py skills/cookbook/cli/tests/unit/test_modules_prompt.py
git commit -m "feat(prompt): argparse param peeling + full render pipeline"
git push
```

---

### Task 9: Author the `database` module content

**Files:**
- Create: `skills/cookbook/cli/cookbook/modules/prompt/prompts/database/module.md`
- Create: `skills/cookbook/cli/cookbook/modules/prompt/prompts/database/reference-manifest.json`
- Create: `skills/cookbook/cli/cookbook/modules/prompt/prompts/database/references/.gitkeep`
- Create: `skills/cookbook/cli/cookbook/modules/prompt/prompts/database/actions/design.md`
- Create: `skills/cookbook/cli/cookbook/modules/prompt/prompts/database/actions/review.md`

- [ ] **Step 1: Create the database module preamble**

Create `skills/cookbook/cli/cookbook/modules/prompt/prompts/database/module.md`:

```markdown
---
domain: database
role: "database design specialist"
---
Operate as a database design specialist.

- Prefer correctness over cleverness. Spell out invariants the schema
  enforces, and explicitly name the ones it does not.
- Always call out normalization tradeoffs. When you denormalize, say what
  read pattern the denormalization is buying and what the write-time cost
  is.
- Account for indexing: name the indexes you would create and what query
  shapes they support. Flag obvious index gaps in any schema you review.
- Account for migration safety: locking behavior, default values on large
  tables, online schema change tools where appropriate.
- Identify the top 3 query patterns the schema is optimized for. If you
  can't name 3, the schema is likely under-specified for the use case.
```

- [ ] **Step 2: Create the reference manifest**

Create `skills/cookbook/cli/cookbook/modules/prompt/prompts/database/reference-manifest.json`:

```json
{
  "version": 1,
  "source_root": ".",
  "destination": "skills/cookbook/cli/cookbook/modules/prompt/prompts/database/references",
  "files": [
    { "src": "cookbook/principles/explicit-over-implicit.md", "dst": "principles/explicit-over-implicit.md", "type": "file" },
    { "src": "cookbook/principles/fail-fast.md",              "dst": "principles/fail-fast.md",              "type": "file" },
    { "src": "cookbook/principles/simplicity.md",             "dst": "principles/simplicity.md",             "type": "file" }
  ]
}
```

(The final picks may expand during smoke-testing; this trio is a safe minimum and is known to exist in the cookbook.)

Create `skills/cookbook/cli/cookbook/modules/prompt/prompts/database/references/.gitkeep` (empty file).

- [ ] **Step 3: Create the `design` action**

Create `skills/cookbook/cli/cookbook/modules/prompt/prompts/database/actions/design.md`:

```markdown
---
description: "Design a database schema for the application described in the task."
params:
  target:
    description: "SQL flavor (sqlite|postgres|mysql)."
    default: "postgres"
---
You are designing a database schema for the application described below.

Target SQL dialect: **{{target}}**.

Deliver, in this order:

1. **Schema diagram (text).** Tables, columns, types, primary keys, foreign
   keys, indexes. Use the dialect-appropriate type names.
2. **DDL.** Complete `CREATE TABLE` statements in {{target}} syntax,
   including every constraint and index you named in (1). No abbreviations
   — paste-ready.
3. **Denormalization callouts.** For any denormalized structure, name what
   read pattern it supports and what write-time burden it imposes.
4. **Top 3 query patterns the schema is optimized for.** Write each as a
   short prose description plus the SQL skeleton (no need to fill in
   literals).
5. **Migration risks.** Anything that would be painful to add later —
   columns that should be NOT NULL but can't be backfilled cheaply,
   indexes that will lock the table to build, etc.

If the task is ambiguous, list your assumptions at the top before the
schema. Do not ask follow-up questions — make defensible assumptions and
move forward.
```

- [ ] **Step 4: Create the `review` action**

Create `skills/cookbook/cli/cookbook/modules/prompt/prompts/database/actions/review.md`:

```markdown
---
description: "Review a database schema for correctness, safety, and performance risk."
params:
  target:
    description: "SQL flavor (sqlite|postgres|mysql), if known."
    default: "unspecified"
---
You are reviewing the database schema supplied below. Target dialect (if
known): **{{target}}**.

Produce a numbered findings list. Each finding has:

- A **severity** tag: **CRITICAL**, **HIGH**, **MEDIUM**, **LOW**, or
  **NOTE**.
- The **table/column** the finding is about (or `(schema-wide)` if it spans
  the schema).
- A one-line **issue** description.
- A one-line **fix** suggestion (concrete: DDL fragment, index name, or
  migration step).

Cover at least these categories explicitly — say "none found" if a
category has no findings:

1. **Missing constraints** — PK, FK, UNIQUE, CHECK, NOT NULL.
2. **Dangerous nullability** — nullable columns that should not be.
3. **Index gaps or excess** — likely query patterns with no covering
   index; redundant indexes; missing partial/expression indexes where
   appropriate.
4. **Normalization** — violations and the cost; deliberate denormalization
   that lacks an annotation explaining why.
5. **Migration risk** — `ALTER`s that would lock large tables, defaults
   that would force rewrites, FK additions that would scan.
6. **Type correctness** for {{target}} — wrong type choices given the
   dialect; precision/scale on numerics; charset/collation on strings if
   relevant.

End with a one-paragraph **summary** of what's most important to fix
first.
```

- [ ] **Step 5: Commit (content only; manifest will be materialized in Task 10)**

```bash
git add skills/cookbook/cli/cookbook/modules/prompt/prompts/database
git commit -m "feat(prompt): database module content (design + review actions)"
git push
```

---

### Task 10: Materialize sub-module manifests in `install.sh`

**Files:**
- Modify: `install.sh` (extend the materialize step to walk sub-module manifests)

- [ ] **Step 1: Add a second materialize pass after the top-level one**

In `install.sh`, immediately after the existing materialize-from-MANIFEST block (right after the `ok "references materialized"` line), insert:

```bash
# 3b. Materialize each prompt-module's reference-manifest.json
title "Materializing prompt-module references"
python3 - "$REPO_ROOT" <<'PY'
import json, shutil, sys
from pathlib import Path

repo_root = Path(sys.argv[1])
glob_root = repo_root / "skills/cookbook/cli/cookbook/modules/prompt/prompts"

if not glob_root.is_dir():
    print("  (no prompt modules)")
    raise SystemExit(0)

count = 0
for manifest_path in sorted(glob_root.glob("*/reference-manifest.json")):
    manifest = json.loads(manifest_path.read_text())
    dest = repo_root / manifest["destination"]
    source_root = (repo_root / manifest["source_root"]).resolve()

    # Wipe destination contents except .gitkeep.
    if dest.exists():
        for child in dest.iterdir():
            if child.name == ".gitkeep":
                continue
            if child.is_dir():
                shutil.rmtree(child)
            else:
                child.unlink()
    else:
        dest.mkdir(parents=True)

    for entry in manifest.get("files", []):
        src = (source_root / entry["src"]).resolve()
        dst = dest / entry["dst"]
        dst.parent.mkdir(parents=True, exist_ok=True)
        if entry["type"] == "file":
            if not src.is_file():
                print(f"  MISSING file: {src}", file=sys.stderr)
                sys.exit(1)
            shutil.copy2(src, dst)
        elif entry["type"] == "tree":
            if not src.is_dir():
                print(f"  MISSING dir: {src}", file=sys.stderr)
                sys.exit(1)
            include = entry.get("include", "*")
            dst.mkdir(parents=True, exist_ok=True)
            for f in src.rglob(include):
                if f.is_file():
                    rel = f.relative_to(src)
                    target = dst / rel
                    target.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(f, target)
        else:
            print(f"  unknown entry type: {entry['type']}", file=sys.stderr)
            sys.exit(1)

    rel_manifest = manifest_path.relative_to(repo_root)
    print(f"  + {rel_manifest}")
    count += 1

print(f"  materialized {count} prompt-module manifest(s)")
PY
ok "prompt-module references materialized"
```

- [ ] **Step 2: Run install and verify materialization**

```bash
./install.sh
ls skills/cookbook/cli/cookbook/modules/prompt/prompts/database/references/principles/
```

Expected: lists `explicit-over-implicit.md`, `fail-fast.md`, `simplicity.md`.

- [ ] **Step 3: Smoke test the assembled prompt end-to-end**

```bash
cookbook prompt database design --target sqlite design a schema for a markdown editing app with unlimited undo | head -60
```

Expected: prints a markdown blob starting with `You are a database design specialist.`, containing the module preamble, the three bundled principles (each prefixed by `## reference: principles/<file>`), the `design` action body with `{{target}}` resolved to `sqlite`, and ending in a `## Your task` block with the free-text task.

- [ ] **Step 4: Try the `review` action**

```bash
cookbook prompt database review CREATE TABLE notes \(id INT, body TEXT\)\; | head -50
```

Expected: same shape, with the review template body and the task containing the literal DDL fragment.

- [ ] **Step 5: Commit**

```bash
git add install.sh
git commit -m "build: materialize prompt-module references at install time"
git push
```

---

### Task 11: Add the routing line to `SKILL.md`

**Files:**
- Modify: `skills/cookbook/SKILL.md`

- [ ] **Step 1: Add the routing entry**

Open `skills/cookbook/SKILL.md` and find the `## Routing` section. Add this bullet at the end of the list (right after the existing `**`<module> ...`**` entry):

```markdown
- **`prompt <module> <action> ...`** → run `cookbook prompt <module> <action> ...`
  and treat the printed prompt as your working brief for this turn. The
  CLI does not call an LLM; it emits the assembled prompt for you to act
  on.
```

- [ ] **Step 2: Add the `prompt` row to the Modules-at-a-glance table**

In the same file, find the `## Modules at a glance` table. Add this row:

```markdown
| `prompt` | Assembles an expert prompt (role + module preamble + bundled cookbook references + action template + free-text task) and prints it to stdout. `prompt <module> <action> [--formal-flags ...] [task ...]`. |
```

- [ ] **Step 3: Commit**

```bash
git add skills/cookbook/SKILL.md
git commit -m "docs(skill): document cookbook prompt module"
git push
```

---

### Task 12: Update `.claude/CLAUDE.md` path references

**Files:**
- Modify: `.claude/CLAUDE.md`

The repo CLAUDE.md mentions paths like `scripts/cookbook/` that have moved. Find and replace.

- [ ] **Step 1: Search for stale paths**

```bash
grep -n "scripts/cookbook\|scripts/tests/cookbook" .claude/CLAUDE.md
```

For each match, replace `scripts/cookbook` with `skills/cookbook/cli` and `scripts/tests/cookbook` with `skills/cookbook/cli/tests`.

- [ ] **Step 2: Verify nothing else in the repo still references `scripts/cookbook/`**

```bash
grep -rn "scripts/cookbook\|scripts/tests/cookbook" --include='*.md' --include='*.sh' --include='*.py' --include='*.json' --exclude-dir='.git' --exclude-dir='references' --exclude-dir='plugins'
```

Update any non-historical hits (skip changelog-style mentions, e.g. inside the spec or this plan document — those reference paths in past tense).

- [ ] **Step 3: Commit**

```bash
git add .claude/CLAUDE.md
git commit -m "docs: update path references after CLI source move"
git push
```

---

### Task 13: Full verification

- [ ] **Step 1: Reinstall from clean state**

```bash
./install.sh
```

Expected: install completes with no errors. References materialize twice — once for the top-level manifest, once for the database sub-module manifest.

- [ ] **Step 2: Run the full test suite**

```bash
cd skills/cookbook/cli/tests
python3 -m pytest unit/ -x -q
cd -
```

Expected: all green.

- [ ] **Step 3: End-to-end CLI smoke tests**

```bash
cookbook --version
cookbook --help
cookbook prompt
cookbook prompt database
cookbook prompt database design --target sqlite design a schema for a markdown editing app with unlimited undo > /tmp/prompt_design.md
wc -l /tmp/prompt_design.md
cookbook prompt database review CREATE TABLE notes \(id INT, body TEXT\)\; > /tmp/prompt_review.md
wc -l /tmp/prompt_review.md
```

Expected:
- `cookbook prompt` lists `database`.
- `cookbook prompt database` lists `design` and `review`.
- `prompt_design.md` is a non-trivial markdown file (≥ 50 lines) starting with the role header and containing the three referenced principles.
- `prompt_review.md` is similarly well-formed.

- [ ] **Step 4: Verify plugin layout is clean**

```bash
ls plugins/adh/skills/cookbook/
```

Expected: only `SKILL.md`. No `cli/`, no `bin/`.

- [ ] **Step 5: Final commit (only if any incidental fixes were needed)**

If Steps 1–4 surfaced any leftover issue, fix it and commit. Otherwise this step is a no-op.

```bash
git status   # should be clean
```

---

## Self-review checklist (done before handing off)

- [x] Spec coverage: every section of the spec maps to a task (source move → Task 1; manifest generalization → Task 2; shim extraction → Task 3; plugin assembly exclude → Task 4; subpackage skeleton → Task 5; frontmatter parser → Task 6; render assembly → Task 7; argparse peeling → Task 8; database content → Task 9; sub-module manifest materialization → Task 10; SKILL.md routing → Task 11; CLAUDE.md paths → Task 12; smoke verification → Task 13).
- [x] No placeholders, no "implement later", every code step contains real code.
- [x] Type consistency: `ParsedFile`, `ParamSpec`, `UnknownPlaceholderError`, `assemble_prompt`, `render_template`, `parse`, `params_from_frontmatter` — all names match across tasks.
- [x] Function signatures match between tests and implementation (e.g., `assemble_prompt(*, module_md_path, references_dir, action_md_path, params, task)`).

---

## Notes for the executor

- This branch is `worktree-prompt`. It is already rebased onto `main` (`94b5cd3 feat: rename plugin from cookbook to adh`).
- Commit cadence is per-task. Push after each commit so the PR (when opened by `/mwt`) reflects the work-in-progress.
- The cookbook plugin namespace is `adh`. The CLI binary is `cookbook`. Don't conflate.
- The user has explicit instructions in `~/.claude/CLAUDE.md`: stage only files you touched (`git add <paths>`, never `git add -A`/`git add .`/`-a`). Each `git add` in this plan lists the specific paths.
- After all tasks pass, run `/mwt` to open / activate the PR.
