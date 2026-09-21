# cookr — Design

**Date:** 2026-09-21
**Status:** approved in conversation, awaiting written review

## Purpose

`cookr` is a skill plus CLI that drives the writing of component recipes for
the two toolkit repos, `agenticdevelopertoolkit` (ADT) and `agentictoolkit`
(ATK). A recipe is a markdown file in a repo's `recipes/` directory, in the
agenticcookbook ingredient or recipe template shape, that tells a developer how
to build one UI component on any platform. The immediate goal is a corpus
complete enough that building the components on Windows (WinUI 3) is a
translation exercise, not a design exercise.

cookr answers three questions the `cookbook` CLI does not:

1. Which components exist in a repo? (`cookr inventory`)
2. Which of them have a finished recipe? (`cookr coverage`)
3. What prompt writes the recipe for one component? (`cookr prompt extract`)

Everything else — frontmatter, validation, lint, indexes — is the `cookbook`
CLI's job, and cookr calls it rather than duplicating it.

## Decisions taken in conversation

- cookr is a separate skill and a separate Python package, not a subcommand
  group in the cookbook CLI.
- Recipes carry **no** traceability field pointing at source code. A recipe is
  instructions on how to build something; what it was derived from stays out
  of it. Coverage is matched by **name**, with aliases held outside the recipe.
- Recipes stay in each repo's existing top-level `recipes/` directory. There is
  no move into `cookbook/` and no `adopt` command. ADT's empty `cookbook/`
  scaffold is deleted.
- The ingredient and recipe templates gain WinUI 3 and AppKit/UIKit Platform
  Notes. The WinUI 3 note is mandatory for every recipe cookr counts.
- Extraction is batched to sonnet subagents, one per component, from
  `SKILL.md`.

## Layout in agenticcookbook

```
skills/cookr/
  SKILL.md                    thin wrapper: routing + workflow, no logic
  bin/cookr                   shim: PYTHONPATH=_cookr_pkg, exec python3 -m cookr
  cli/
    cookr/
      __init__.py
      __main__.py             argparse entry, same shape as cookbook's
      registry.py             auto-discovers modules (NAME/HELP/register/run)
      context.py              resolves repo root, loads .cookr.json
      core/
        config.py             .cookr.json schema + loader
        inventory.py          walk roots → list[Component]
        recipes.py            parse recipes/ → dict[slug, RecipeInfo]
        coverage.py           join inventory × recipes → list[CoverageRow]
        completeness.py       the partial/complete rules on one recipe
      modules/
        inventory.py
        coverage.py
        prompt/
          prompt_cli.py       `cookr prompt extract <component>`
          prompts/extract/
            module.md
            actions/extract.md
            reference-manifest.json
    tests/
      conftest.py
      fixtures/mini-repo/     a tiny repo with .cookr.json, a few components, a few recipes
      unit/
      functional/
```

Dependencies point downward only. cookr imports the installed `cookbook`
package for `frontmatter.parse`, `core.markdown.iter_markdown`, and
`core.checks.phase_a`; it shells out to `cookbook validate` and
`cookbook lint`. The cookbook package never learns cookr exists, so cookr is
deletable without touching it (design-for-deletion) and the existing cookbook
tests are untouched.

## Shipping

`install.sh` today special-cases the cookbook skill three times: copy its
package to `~/.local/bin/_cookbook_pkg`, install its shim, and exclude `cli`
and `bin` from its plugin bundle via `EXCLUDE_PER_SKILL = {"cookbook": {"cli",
"bin"}}`. The change is one table of skills that carry a CLI:

```
CLI_SKILLS = (cookbook cookr)
```

For each entry: copy `skills/<name>/cli/<name>` to `~/.local/bin/_<name>_pkg`,
copy `skills/<name>/bin/<name>` to `~/.local/bin/<name>`, and exclude `cli` and
`bin` from that skill's plugin bundle. The plugin then exposes `/adh:cookr`
alongside `/adh:cookbook`. `install.sh` stays a shell script because
`install` is a named exception to the Python-only rule.

## Per-repo configuration: `.cookr.json`

Each target repo carries one file at its root:

```json
{
  "recipes": "recipes",
  "roots": [
    {"path": "packages/web/packages/ui/src/components", "tier": "ui-primitives", "platform": "web"},
    {"path": "packages/web/packages/ui/src/blocks",      "tier": "ui-blocks",     "platform": "web"},
    {"path": "packages/web/packages/controls/src",       "tier": "ui-blocks",     "platform": "web"},
    {"path": "packages/apple/AgenticDeveloperToolkit/SourcesUI", "tier": "apple-ui", "platform": "apple"}
  ],
  "ignore": ["**/*.stories.tsx", "**/*.test.*", "**/index.ts", "**/Resources/**"],
  "aliases": {"toolbar-button": "button"}
}
```

| Key | Meaning |
|---|---|
| `recipes` | Directory holding the recipe corpus, relative to the repo root. |
| `roots[].path` | A directory to scan for components. Scanned recursively. |
| `roots[].tier` | Free-form label used by `--tier`. One tier per phase of the plan. |
| `roots[].platform` | `web`, `apple`, `android`, `windows`. Recorded on each inventory row. |
| `ignore` | Glob patterns (relative to the repo root) removed from the inventory. |
| `aliases` | Component name → recipe slug, for the cases where the file name and the recipe name do not line up. |

The exact `roots` and `ignore` lists for ADT and ATK are decided when the
file is written in each repo, by looking at the trees; the schema is fixed
here.

## Inventory

`cookr inventory [--tier T] [--json]`

Walks every root, keeps files with extensions `.tsx`, `.ts`, `.swift`, `.kt`,
`.cs`, `.xaml`, drops anything matching `ignore`, and emits one row per file:

| Field | Derivation |
|---|---|
| `name` | file stem converted to kebab-case: `Button.tsx` → `button`, `ToolbarButton.swift` → `toolbar-button`, `chat-composer.tsx` → `chat-composer`. |
| `path` | repo-relative path |
| `tier` | from the root that matched |
| `platform` | from the root that matched |

Two files that produce the same `name` (say a web `Button.tsx` and an AppKit
`Button.swift`) are two inventory rows and one component. Coverage treats them
as one entry with two source platforms.

## Coverage

`cookr coverage [--tier T] [--json] [--require partial|complete]`

Reads the recipe corpus: every `*.md` under `recipes/`, skipping the same
names `cookbook` skips (`INDEX.md`, `_template.md`, …). Each recipe's slug is
its file stem. A component is matched to a recipe when the component `name`
equals a recipe slug, or `aliases[name]` equals a recipe slug.

Each component gets one of three states:

| State | Rule |
|---|---|
| `missing` | no recipe matches |
| `partial` | a recipe matches but any completeness rule fails |
| `complete` | a recipe matches and every completeness rule passes |

Completeness rules, evaluated on the recipe file:

1. `status` is `review` or `accepted`.
2. No `NEEDS REVIEW` marker in the body.
3. Every `##` section the template defines for that `type` is present and has
   at least one non-blank line of body before the next heading.
4. The Platform Notes section contains a `WinUI 3` entry with body text.

Output is a table sorted by tier then name, followed by a one-line tally per
tier. `--json` emits the rows as a list of objects. `--require complete` exits
1 if any component in scope is below `complete`; `--require partial` exits 1
only on `missing`. A phase's exit gate is therefore:

```sh
cookr coverage --tier ui-primitives --require complete && cookbook validate -p recipes
```

Recipes with no matching component (a vocabulary recipe such as ATK's
`site-menu`, or a composite) are not an error. They are listed once at the
end under "recipes with no inventory match" so a typo in an alias is visible.

## Prompt assembly

`cookr prompt extract <name> [--json]`

Mirrors the cookbook prompt module. It assembles, in order:

1. `prompts/extract/module.md` — the role and the extraction rules, restating
   source-fidelity in one paragraph: describe the code as it is, invent
   nothing, mark gaps `NEEDS REVIEW: Not implemented in source. Behavior
   undefined.`
2. `prompts/extract/actions/extract.md` — the task, with parameters
   `{{name}}`, `{{recipe_path}}`, `{{type}}`, and `{{platforms}}`.
3. The template for the recipe's type, pulled from the cookbook references
   (`ingredient` by default; `--type recipe` for a composite).
4. The recipe-quality guidelines, pulled from the cookbook references via the
   manifest.
5. The full text of every inventory file whose `name` (or alias) is `<name>`,
   each under a heading giving its repo-relative path and platform.
6. The existing recipe at `recipes/<slug>.md` if there is one, so the
   subagent fills it out rather than starting over.

The output is one markdown document on stdout, ready to be handed to a
subagent verbatim. `--json` wraps it with the resolved paths for scripting.

The template edits (WinUI 3 and AppKit/UIKit notes, below) are what make the
prompt ask for the Windows note; cookr adds no per-platform prose of its own.

## Template changes in agenticcookbook

Both `cookbook/ingredients/_template.md` and `cookbook/recipes/_template.md`
get two new bullets under `## Platform Notes`, in this order after the
existing three:

```
- **AppKit / UIKit**: {{platform_notes_appkit}}
- **WinUI 3**: {{platform_notes_winui}}
```

`skills/cookbook/cli/references/conventions.md` gains one sentence under
Platform Notes saying the WinUI 3 entry is required for any recipe counted by
`cookr coverage`. No change to frontmatter fields.

## SKILL.md

Thin wrapper, same as the cookbook skill's: "all work goes through the CLI".
It routes:

| Request | Command |
|---|---|
| what components exist / what tiers | `cookr inventory` |
| what is left to write | `cookr coverage --tier <tier>` |
| write the recipe for X | `cookr prompt extract X` → subagent |
| is the phase done | `cookr coverage --tier <tier> --require complete` then `cookbook validate -p recipes` |

The extraction workflow it prescribes:

1. `cookr coverage --tier <tier> --json` to get the missing and partial names.
2. For each name, `cookr prompt extract <name>` and dispatch the result to a
   subagent pinned to `claude-sonnet-4-6`, which writes `recipes/<slug>.md`.
   Batches of up to 8 run concurrently.
3. `cookbook update -p recipes --author <user>` to fill frontmatter.
4. `cookbook validate -p recipes` and `cookr coverage --tier <tier>`.
5. Anything still `partial` goes back through step 2 with the existing recipe
   in the prompt.
6. `cookbook lint -p recipes --since main` before commit.

## Changes in the target repos (Phase 0 exit)

In ADT:

- add `.cookr.json`;
- delete the empty `cookbook/` scaffold;
- leave `recipes/`, `tools/check_*.py`, and CI as they are.

In ATK:

- add `.cookr.json`;
- leave `recipes/` and `tools/classify_recipes.py` as they are.

Phase 0 exits when `cookr coverage` runs on both repos and reports every
tier, and `cookbook validate -p recipes` is green in both.

## Testing

pytest under `skills/cookr/cli/tests/`, wired into the same top-level pytest
run as the cookbook tests. `conftest.py` pushes `skills/cookr/cli` and
`skills/cookbook/cli` onto `sys.path` and points the cookbook references dir
at the checked-in references, as the cookbook conftest does.

Unit tests cover the pure functions: kebab-case naming, ignore matching, alias
resolution, each completeness rule in isolation, and the three-state join.

Functional tests run the CLI against `fixtures/mini-repo`, which holds a
`.cookr.json` with two roots and two tiers, five component files (one
ignored, one aliased, two sharing a name across platforms), and three recipes
(one complete, one draft with a `NEEDS REVIEW`, one with no WinUI 3 note).
They assert the table, the `--json` shape, the `--require` exit codes, and
that `prompt extract` includes every source file and the existing recipe.

## Out of scope

- Writing the recipes themselves. That is Phases 1–6 of the plan.
- Any change to what the `cookbook` CLI validates.
- Android or Windows source roots. `.cookr.json` allows them; nothing today
  populates them.
