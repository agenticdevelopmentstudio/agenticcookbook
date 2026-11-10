> [!WARNING]
> **ARCHIVED — HISTORICAL RECORD, NOT CURRENT.** Captured 2026-11-10. This document reflects a
> past state or decision and may no longer describe how things work. Do not treat it as live
> documentation.

# `cookbook prompt` module — design

**Status:** draft
**Date:** 2026-05-22
**Branch:** `worktree-prompt`

## Purpose

Add a new module to the `cookbook` CLI that lets a user invoke a domain-specialist
prompt for a specific task. The CLI assembles an expert-loaded prompt
(role header + module preamble + bundled cookbook references + action template +
the user's free-text task) and prints it to stdout. The parent Claude Code
session treats the printed prompt as its working brief for the turn. The CLI
itself does not call any LLM — it is a deterministic prompt builder.

While we are here, move the existing `cookbook` CLI source from `scripts/cookbook/`
into the `cookbook` skill at `skills/cookbook/cli/`. The CLI source is owned by
the skill that wraps it; the current split between `scripts/` and `skills/` is
incidental and worth removing.

## Non-goals

- Symlink-based install mode. Deferred. Install continues to copy.
- Touching the other 7 repo-local skills under `.claude/skills/`. Out of scope.
- Editing the plugin / marketplace registration logic in `install.sh` beyond the
  minimum needed for the source move.
- Calling an LLM from inside the CLI. The CLI emits text; Claude executes.
- `cookbook prompt` modules beyond the initial `database` module.

## Invocation

- CLI: `cookbook prompt <module> <action> [--formal-flags ...] [free-text task ...]`
- Slash: `/adh:cookbook prompt <module> <action> [--formal-flags ...] [free-text task ...]`

`argparse` peels off declared `--flags`; all remaining positional words are
joined with single spaces and bound to `{{task}}` in the template.

Example:

```
cookbook prompt database design --target sqlite \
    design a schema for a markdown editing app with unlimited undo
```

Resolves to `target=sqlite`, `task="design a schema for a markdown editing app with unlimited undo"`,
and prints the assembled prompt to stdout.

## Source-move

| Before                              | After                                            |
|-------------------------------------|--------------------------------------------------|
| `scripts/cookbook/cookbook/`        | `skills/cookbook/cli/cookbook/`                  |
| `scripts/cookbook/reference-manifest.json` | `skills/cookbook/cli/reference-manifest.json` |
| `scripts/cookbook/references/`      | `skills/cookbook/cli/references/`                |
| `scripts/cookbook/references-src/`  | `skills/cookbook/cli/references-src/`            |
| `scripts/tests/cookbook/`           | `skills/cookbook/cli/tests/`                     |
| (n/a)                               | `skills/cookbook/bin/cookbook` (the shim)        |

`scripts/cookbook/` and `scripts/tests/cookbook/` are deleted after the move.
The shim that previously lived inline in `install.sh` (written to
`~/.local/bin/cookbook` on install) is extracted into a source file under
`skills/cookbook/bin/cookbook` so the install step becomes
`cp skills/cookbook/bin/cookbook ${BIN_DIR}/cookbook` + `chmod +x`. The shim
itself still sets `PYTHONPATH` to `~/.local/bin/_cookbook_pkg/` and execs
`python3 -m cookbook "$@"`.

`install.sh` path variables update accordingly:

```bash
MANIFEST="${REPO_ROOT}/skills/cookbook/cli/reference-manifest.json"
PKG_SRC="${REPO_ROOT}/skills/cookbook/cli"
```

## Plugin assembly: exclude CLI artifacts

Step 7 of `install.sh` (Assembling plugin) currently does:

```bash
cp -R "${skill}" "${PLUGIN_SKILLS_DIR}/${name}"
```

Because the cookbook skill now contains `cli/` and `bin/` — neither of
which is Claude-facing skill content — the assembly must skip them.
Replace the raw `cp -R` with a small inline Python block that walks each
`./skills/<name>/` and copies every entry except an exclude list:

```python
EXCLUDE = {"cli", "bin"}
```

The exclude list applies uniformly to every skill under `./skills/<name>/`.
The other 6 repo-local skills (well, the other skills that ship under
`./skills/`) currently have none of these subdirs, so the exclusion is a
no-op for them. The cookbook skill ends up with only `SKILL.md` in the
assembled `plugins/adh/skills/cookbook/` — which is the right outcome:
Claude Code only reads `SKILL.md` from a skill dir, and the CLI source has
no business being shipped twice (once via the plugin, once via
`~/.local/bin/_cookbook_pkg/`).

## Where the `prompt` module lives in the CLI package

```
skills/cookbook/cli/cookbook/modules/prompt/
  __init__.py
  prompt_cli.py                       # argparse subparser, action dispatch
  render.py                           # assembles final prompt string
  prompts/
    database/
      module.md                       # module-level preamble + frontmatter
      reference-manifest.json         # cookbook paths to bundle
      references/                     # materialized at install
        .gitkeep
      actions/
        design.md
        review.md
```

The `prompt` module is a subpackage (not a single .py file like
`create.py`/`update.py`/etc.) because it has its own sub-hierarchy of
modules-and-actions and ships data files (`.md`, `.json`) alongside the code.

The top-level CLI dispatcher (`cookbook/cli.py`) gains one entry pointing
`prompt` at `cookbook.modules.prompt.prompt_cli:main`.

## Action file format

Each action is one markdown file with YAML frontmatter. Example
`prompts/database/actions/design.md`:

```markdown
---
description: "Design a database schema for the given application."
params:
  target:
    description: "SQL flavor (sqlite|postgres|mysql)"
    default: "postgres"
---
# Database design — {{target}}

You are a database design specialist...

[prompt body, can reference {{target}} and {{task}}]

## Task

{{task}}
```

Rules:

- Frontmatter is parsed with `pyyaml`. `description` is required (used by
  `cookbook prompt <module> --help`).
- `params` is a dict of `{name: {description, default}}`. Missing `default`
  means the param is required.
- Body interpolation is a simple `{{name}}` substitution. The only reserved
  name is `{{task}}` (the free-text remainder).
- Unknown `{{...}}` placeholders cause a runtime error with a clear message.

## Module file format

`prompts/<module>/module.md`:

```markdown
---
domain: database
role: "database design specialist"
---
Operate as a database design specialist. Prefer correctness over cleverness.
Call out normalization tradeoffs explicitly. ...
```

The frontmatter `role` is used to build the role header at the top of the
assembled prompt:

```
You are a database design specialist.
```

The body is the module-level preamble, included verbatim after the role
header in every prompt assembled from this module.

## Prompt assembly order

The CLI assembles and prints, in order:

1. Role header: `You are a {role from module.md frontmatter}.`
2. Module preamble: the body of `module.md` (frontmatter stripped).
3. References: each materialized file under `prompts/<module>/references/`,
   in alphabetical-by-relative-path order, each prefixed by
   `## reference: <relative-path>` as an h2 header.
4. Action template body, with `{{param}}` and `{{task}}` interpolated.
5. A final block `\n\n## Your task\n\n{task}\n` to make the ask unambiguous
   even if the template doesn't end with `{{task}}`.

The five sections are separated by blank lines. No other formatting is
applied. The output is plain markdown.

## Reference manifest for a prompt sub-module

`prompts/<module>/reference-manifest.json` has the same shape as the
existing top-level `reference-manifest.json`, with one small generalization:
`source_root` and `destination` are interpreted relative to the **repo
root**, not to a hardcoded `scripts/cookbook/` prefix. Example:

```json
{
  "source_root": "cookbook",
  "destination": "skills/cookbook/cli/cookbook/modules/prompt/prompts/database/references",
  "files": [
    { "type": "file", "src": "principles/explicit-over-implicit.md",
      "dst": "principles/explicit-over-implicit.md" },
    { "type": "file", "src": "principles/fail-fast.md",
      "dst": "principles/fail-fast.md" }
  ]
}
```

The materialization Python block in `install.sh` currently does:

```python
source_root = (repo_root / "scripts/cookbook" / manifest["source_root"]).resolve()
```

Change to:

```python
source_root = (repo_root / manifest["source_root"]).resolve()
```

The existing top-level manifest at
`skills/cookbook/cli/reference-manifest.json` is updated in the same change
to set `source_root: "cookbook"` (or wherever its sources actually live) so
its paths are repo-relative too. This eliminates the hardcoded
`scripts/cookbook/` prefix that's about to disappear anyway.

Materialization is run once per manifest. After materializing the top-level
manifest, `install.sh` globs
`skills/cookbook/cli/cookbook/modules/prompt/prompts/*/reference-manifest.json`
and materializes each in the same loop. Same Python block, called N times.

For the initial `database` module, the manifest bundles a small curated set
of cookbook artifacts — final picks land during implementation, not in this
spec. Candidates include:

- `cookbook/principles/explicit-over-implicit.md`
- `cookbook/principles/fail-fast.md`
- `cookbook/principles/simplicity.md`
- Any `cookbook/guidelines/` that touches data modeling, migrations, or
  indexing (TBD during implementation — selected from what actually exists
  in the cookbook at the time)

## `SKILL.md` routing addition

Add one bullet under the existing `## Routing` section of
`skills/cookbook/SKILL.md`:

> - **`prompt <module> <action> ...`** → run `cookbook prompt <module> <action> ...`
>   and treat the printed prompt as your working brief for this turn. The CLI
>   does not call an LLM; it emits the prompt for you to act on.

## Initial `database` module content

### `database/module.md`

Role: `database design specialist`. Body framing:

- Prefer correctness over cleverness.
- Always call out normalization tradeoffs explicitly.
- Account for indexing, migration safety, and concurrency.
- Surface constraints, nullability, and foreign keys deliberately.
- Identify the top query patterns the schema is optimized for.

### `database/actions/design.md`

Frontmatter:

```yaml
description: "Design a database schema for the given application."
params:
  target:
    description: "SQL flavor (sqlite|postgres|mysql)"
    default: "postgres"
```

Template instructs the responding Claude to deliver:

1. Complete schema: tables, columns, types, primary/foreign keys, indexes.
2. Sample DDL in the target dialect.
3. Explicit list of denormalization tradeoffs and rationale.
4. The top 3 query patterns the schema is optimized for.
5. Migration risks if applicable.

### `database/actions/review.md`

Frontmatter:

```yaml
description: "Review a database schema and flag risks."
params:
  target:
    description: "SQL flavor (sqlite|postgres|mysql), optional"
```

Template instructs the responding Claude to review the schema (supplied as
the free-text task) and produce a numbered findings list with severity tags,
covering:

- Missing constraints (PK, FK, UNIQUE, CHECK, NOT NULL)
- Dangerous nullability
- Index gaps (or excess) relative to likely query patterns
- Normalization violations and their cost
- Migration risk (locking, backfills, default values on large tables)
- Type-correctness for the chosen `--target` dialect (if supplied)

## Failure modes (CLI-side, not LLM-side)

- Unknown module: exit 2 with `cookbook prompt: unknown module '<name>'.`
- Unknown action: exit 2 with `cookbook prompt <module>: unknown action '<name>'.`
- Missing required formal param: exit 2 with argparse's standard message.
- Unrenderable template (unknown `{{placeholder}}` not in frontmatter `params`
  and not `{{task}}`): exit 1 with file path + offending placeholder.
- Missing module/action file on disk: exit 1 with the absolute path that was
  expected.
- Empty `{{task}}` with no positional task text: warn (stderr) but still
  emit; the assembled prompt is technically valid, just lower quality.

## Tests

Under `skills/cookbook/cli/tests/test_prompt.py`:

- Action discovery: lists modules and actions correctly from the disk layout.
- Frontmatter parsing: required `description`, optional `params` with defaults.
- Param peeling: argparse picks up declared `--flags`; remaining positionals
  bind to `{{task}}`.
- Template rendering: `{{param}}` and `{{task}}` substitute; unknown
  placeholder raises.
- Assembly order: role → preamble → references → template → task block.
- Reference inclusion: materialized files are interpolated in alphabetical
  order with the `## reference: <path>` header.
- Failure modes match the table above.

No LLM integration tests — the CLI never calls a model.

## Implementation order (rough sketch — final plan comes from writing-plans)

1. Move `scripts/cookbook/` → `skills/cookbook/cli/`. Update `install.sh`
   path variables. Update CLAUDE.md path references. Run existing tests to
   confirm nothing else broke.
2. Add the plugin-assembly exclude list (Python block replaces `cp -R`).
3. Add `cookbook.modules.prompt` subpackage skeleton (no actions yet) and
   wire `prompt` into the top-level CLI dispatcher.
4. Implement `render.py` with the assembly order above.
5. Author the `database/module.md`, `database/reference-manifest.json`,
   `actions/design.md`, `actions/review.md`.
6. Extend `install.sh` to glob and materialize each prompt sub-module's
   manifest.
7. Add `SKILL.md` routing line.
8. Tests under `skills/cookbook/cli/tests/test_prompt.py`.
9. Smoke test: `./install.sh` then `cookbook prompt database design --target sqlite design a schema for a markdown editing app with unlimited undo` and verify the assembled prompt is well-formed.

## Open implementation-time choices (not blocking the spec)

- Final set of cookbook references to bundle in `database/reference-manifest.json`.
- Whether `module.md` should declare formal params shared across all actions
  in the module (e.g., a `--target` default that actions inherit). Current
  spec: no inheritance, each action declares its own. We can add inheritance
  later if a second module wants it.
- Whether `cookbook prompt --help` (no module) should list every module +
  action discovered on disk. Recommended yes, but trivial.
