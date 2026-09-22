---
name: cookr
version: "0.1.0"
description: "Inventory, coverage and extraction prompts for component recipes in a repo that carries a .cookr.json. Wraps the `cookr` CLI at ~/.local/bin/cookr. Use when the user asks which components have recipes, what is left to write for a tier, or to write the recipe for a component."
argument-hint: "[--help] [-p <repo-root>] <inventory|coverage|prompt extract <name>> [...]"
allowed-tools: Bash(cookr *), Bash(cookbook *), Bash(command -v cookr)
model: sonnet
---

# cookr v0.1.0

Thin wrapper around the `cookr` CLI at `~/.local/bin/cookr`. All work goes
through the CLI — never duplicate its logic in this skill. Recipe frontmatter,
indexes, validation and lint belong to the `cookbook` CLI; call it, never
re-implement it.

## Startup

```bash
command -v cookr
```

If missing, tell the user:

> The `cookr` CLI is not installed. Run `./install.sh` from the agenticcookbook repo, then re-invoke me.

…and stop.

## Routing

| Request | Command |
|---|---|
| what components exist / what tiers there are | `cookr inventory [--tier <tier>]` |
| what is left to write | `cookr coverage [--tier <tier>]` |
| write the recipe for X | `cookr prompt extract X` → dispatch (below) |
| is the phase done | `cookr coverage --tier <tier> --require complete` then `cookbook validate -p recipes` |
| no args / `--help` | `cookr --help`, present the module table verbatim |

Forward `-p <repo-root>` when the user supplies one; otherwise run from cwd and let the CLI find `.cookr.json`.

## Extraction workflow

1. `cookr coverage --tier <tier> --json` — collect every row whose `state` is `missing` or `partial`. A row is one component name and carries `tiers` (plural): the same name can appear in several tiers, and it is still one recipe.
2. De-duplicate the work list by the row's `recipe` slug, falling back to `name` when `recipe` is null, so no two subagents in a batch write the same `recipes/<slug>.md`. Then for each remaining row, run `cookr prompt extract <name>` (add `--type recipe` for a composite) and dispatch the printed prompt verbatim to a subagent pinned to `claude-sonnet-4-6`. The subagent writes `recipes/<slug>.md`. Run up to 8 subagents at a time.
3. `cookbook update -p recipes --author "<user>"` — fills frontmatter.
4. `cookbook validate -p recipes` and `cookr coverage --tier <tier>`.
5. Any row still `partial`: rerun step 2 for it. The prompt includes the existing recipe, so the subagent completes rather than restarts.
6. `cookbook lint -p recipes --since main` before committing.

## Interpreting coverage

The `problems` column names exactly what keeps a recipe at `partial`:
a `status` below `review`, a `NEEDS REVIEW` marker, a missing or empty required
section, or an unfilled `WinUI 3` bullet. Quote it to the subagent; do not
re-derive it.

A recipe listed under "recipes with no inventory match" is not an error: it is
a vocabulary or composite recipe with no single source file. Check `.cookr.json`
`aliases` only if the name looks like a typo of a component.

One row whose `paths` span two unrelated components (a landing-page `Card.tsx`
and a primitives `card.tsx`) is a name collision, not one component. Give the
odd one out its own name in `.cookr.json` `renames`
(`{"packages/landing/src/blocks/Card.tsx": "landing-card"}`); coverage then
shows two rows and `prompt extract landing-card` takes only that source.

## Behavior notes

- Never edit files in `~/.local/bin/_cookr_pkg/`. Edit `skills/cookr/cli/` in agenticcookbook and re-run `./install.sh`.
- Never `pip install` from this skill.
- `.cookr.json` lives at the target repo's root. Add roots, ignores and aliases there; never in a recipe.
