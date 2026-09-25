---
name: cookr
version: "0.1.0"
description: "Inventory, coverage and extraction prompts for component recipes in a repo that carries a .cookr.json. Wraps the `cookr` CLI at ~/.local/bin/cookr. Use when the user asks which components have recipes, what is left to write for a tier, or to write the recipe for a component."
argument-hint: "[--help] [-p <repo-root>] <inventory|coverage|prompt extract <name>|--tier <tier>> [...]"
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
| write the recipe for X | `cookr prompt extract X --out-dir <dir>` → dispatch (below) |
| write everything a tier still needs | extraction workflow (below) |
| is the tier written | `cookr prompt extract --tier <tier> --out-dir <dir>` lists nothing to write |
| is the phase done | `cookr coverage --tier <tier> --require complete` then `cookbook validate -p <recipes_dir>` |
| no args / `--help` | `cookr --help`, present the module table verbatim |

Forward `-p <repo-root>` to every `cookr` call when the user supplies one;
otherwise run from cwd and let the CLI find `.cookr.json`. Never pass a
cwd-relative `recipes` to `cookbook`: take `recipes_dir` (absolute) from the
worklist JSON below, which honors `.cookr.json`'s `recipes` and repo root.

## Extraction workflow

1. `cookr prompt extract --tier <tier> --out-dir <scratch dir> --json` — the
   worklist. It writes one brief per recipe that still needs a writer, already
   de-duplicated by slug (aliased names share one brief), and prints
   `repo_root`, `recipes_dir`, `write` (one entry per brief: `slug`, `name`,
   `recipe_file`, `domain`, `existing`, `brief`) and `awaiting_review`. Use a scratch
   directory outside the repo, e.g. `$TMPDIR/cookr-briefs/<tier>`.
2. For each `write` entry, dispatch a subagent pinned to `claude-sonnet-4-6`
   whose whole prompt is: ``Read `<brief>` in full and do exactly what it says.``
   Never paste the brief into the prompt. For a composite, first rebuild its
   brief with `cookr prompt extract <name> --type recipe --out-dir <scratch dir>`.
   Run up to 8 subagents at a time.
3. `cookbook update -p <recipes_dir> --author "<user>"` — fills empty
   frontmatter. A writer that rewrote an existing recipe (`existing: true`)
   has already recorded it with `cookbook bump`, as its brief says; never bump
   it again, and never hand-edit `version`, `modified` or Change History.
4. `cookbook validate -p <recipes_dir>` and `cookr coverage --tier <tier>`.
   Coverage grades each recipe's `domain` against the one its path derives
   (the worklist's `domain`), so a wrong scheme or directory shows up in
   `problems` like any other gap.
5. Rerun step 1. Every recipe still in `write` goes back to step 2; its brief
   now includes the existing recipe, so the subagent completes rather than
   restarts. Stop when `write` is empty.
6. Verify pass (below) on every recipe written in the batch.
7. `cookbook lint -p <recipes_dir> --since main` before committing.

`awaiting_review` lists recipes whose only problem is a `NEEDS REVIEW`
marker: finished work waiting on a reviewer's decision, never a rewrite target.
Report them to the user. `cookr coverage --require complete` stays red until
the reviewer settles each marker, so the phase is written when `write` is empty
and done only when that gate passes.

## Verify pass

Writers assert behavior the source does not have — a MUST claiming validation
the code never does, "may be null" where the type forbids it, a branch that
does not exist, a helper called "not in source" when it is imported from a real
path — and Platform Notes repeat the same errors. After each batch, dispatch one
subagent per new recipe, pinned to `claude-sonnet-4-6`, with this brief:

- Read every source file in full, and every imported helper the recipe
  describes (search the repo for it).
- Check each Behavioral Requirement, test vector, edge case, configuration row,
  Platform Notes claim and Design Decision against source; fix inaccuracies in
  place with minimal edits. Keep the section order and the `- **name**:` form.
- Re-read every kept `NEEDS REVIEW` marker against the marker rules in
  `<brief>` (the writer's brief from the worklist: its preamble's
  `NEEDS REVIEW` bullets and, for a non-UI component, its
  `## non-UI component` section). Restate as fact every marker those rules do
  not allow; keep every one they call a genuine gap.
- Do not commit and do not touch any other file. Reply
  `<slug> fixed N claims, markers M`.

Then check the kept markers yourself against those same rules in the brief
before accepting them: a verify agent is still a writer. The brief is the only
statement of the marker rules; never judge markers by a shorter list of your
own.

## Interpreting coverage

Rows are keyed by `slug`, the recipe stem each name resolves to through
`aliases`; de-duplicate by `slug`. The `problems` column names exactly what
keeps a recipe at `partial`. Quote it to the subagent; do not re-derive it.
Every graded rule (the Compliance checks every component cites, the minimum
test vectors, the Design Decision lines, frontmatter `platforms`) is stated
once, in the writer rules of `modules/prompt/prompts/extract/module.md`,
which every brief carries as its preamble; point at the brief, never restate
the rules.

A recipe listed under "recipes with no inventory match" is not an error: it is
a vocabulary or composite recipe with no single source file. Check `.cookr.json`
`aliases` only if the name looks like a typo of a component.

A row whose problems include `name collision across tiers` has `paths` that
span two unrelated components (a landing-page `Card.tsx` and a primitives
`card.tsx`). Give the odd one out its own name in `.cookr.json` `renames`
(`{"packages/landing/src/blocks/Card.tsx": "landing-card"}`); coverage then
shows two rows and `prompt extract landing-card` takes only that source. When
the two really are one component, list every path in `renames` under the
shared name; that records the merge as deliberate and clears the problem.

A `renames` key can also be a directory: `{"packages/chat/src/hooks": "chat-hooks"}`
makes every source file below it one component, including files added later.
Use a directory key to group a module; a file key beats it, and the longest
directory key wins.

## Non-UI code

Shared code with no visual surface — models, clients, engines — goes under a
root marked `"kind": "logic"` in `.cookr.json`. It uses the same `ingredient`
template; `prompt extract` adds the non-UI guidance (contract, errors,
concurrency, persistence; Appearance, States and Accessibility as one
`Not applicable` line each). Python sources use `"platform": "python"`. A directory that mixes view and
model files takes a root-scoped `"ignore"` list (`["**/*ViewController.swift"]`)
so the top-level `ignore` never drops files a UI root needs.

## Behavior notes

- Never edit files in `~/.local/bin/_cookr_pkg/`. Edit `skills/cookr/cli/` in agenticcookbook and re-run `./install.sh`.
- Never `pip install` from this skill.
- `.cookr.json` lives at the target repo's root. Add roots, ignores and aliases there; never in a recipe.
