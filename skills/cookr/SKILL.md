---
name: cookr
version: "0.2.0"
description: "Inventory, coverage, extraction prompts and arrangement for the specs of a library cookbook (a repo's cookbook/ directory with cookbook.json). Wraps the `cookr` CLI at ~/.local/bin/cookr. Use when the user asks which components have specs, what is left to write for a group, to write the spec for a component, to convert a .cookr.json repo into a cookbook, or to relink specs after code moved."
argument-hint: "[--help] [-p <repo-root>] <inventory|coverage|arrangement|relink|organize plan|apply|prompt extract <name>|--tier <group>> [...]"
allowed-tools: Bash(cookr *), Bash(cookbook *), Bash(command -v cookr)
model: sonnet
---

# cookr v0.2.0

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

## The library cookbook

A repo's specs live in `<repo>/cookbook/`, arranged in directories that mirror
the code (`cookbook/ai-plugin-kit/chat/chat-context.md`). A spec's name is its
path there without `.md`; its `domain` is `<scheme>://cookbook/<name>`. Each
spec lists its code in a `## Reference Implementations` table of repo-relative
paths (a trailing `/` claims a whole directory). `cookbook/cookbook.json`'s
`code` block lists the source roots, so a file no spec claims yet still shows
up, named where the code's arrangement puts it. A "tier" or group is any
directory of the cookbook (`--tier ai-plugin-kit/chat`).

## Routing

| Request | Command |
|---|---|
| what components exist / what groups there are | `cookr inventory [--tier <group>]` |
| what is left to write | `cookr coverage [--tier <group>]` |
| write the recipe for X | `cookr prompt extract X --out-dir <dir>` → dispatch (below) |
| write everything a group still needs | extraction workflow (below) |
| does the cookbook still mirror the code | `cookr arrangement [--tier <group>]` |
| code moved (`git mv`) | `cookr relink [--since <ref>] [--dry-run]` |
| convert a `.cookr.json` repo | organize workflow (below) |
| is the group written | `cookr prompt extract --tier <group> --out-dir <dir>` lists nothing to write |
| is the phase done | `cookr coverage --tier <group> --require complete` then `cookbook validate -p <cookbook_dir>` |
| no args / `--help` | `cookr --help`, present the module table verbatim |

Forward `-p <repo-root>` to every `cookr` call when the user supplies one;
otherwise run from cwd and let the CLI find `cookbook/cookbook.json`. Pass
`cookbook` the absolute `cookbook_dir` from the worklist JSON below, never a
cwd-relative path.

## Extraction workflow

1. `cookr prompt extract --tier <group> --out-dir <scratch dir> --json` — the
   worklist. It writes one brief per spec that still needs a writer and prints
   `repo_root`, `cookbook_dir`, `write` (one entry per brief: `name`,
   `recipe_file`, `domain`, `reference_implementations`, `existing`, `brief`)
   and `awaiting_review`. Use a scratch directory outside the repo, e.g.
   `$TMPDIR/cookr-briefs/<group>`.
2. For each `write` entry, dispatch a subagent pinned to `claude-sonnet-4-6`
   whose whole prompt is: ``Read `<brief>` in full and do exactly what it says.``
   Never paste the brief into the prompt. For a composite, first rebuild its
   brief with `cookr prompt extract <name> --type recipe --out-dir <scratch dir>`.
   Run up to 8 subagents at a time.
3. `cookbook update -p <cookbook_dir> --author "<user>"` — fills empty
   frontmatter. A writer that rewrote an existing recipe (`existing: true`)
   has already recorded it with `cookbook bump`, as its brief says; never bump
   it again, and never hand-edit `version`, `modified` or Change History.
4. `cookbook validate -p <cookbook_dir>` and `cookr coverage --tier <group>`.
   Coverage grades each recipe's `domain` against the one its path derives
   (the worklist's `domain`), so a wrong scheme or directory shows up in
   `problems` like any other gap.
5. Rerun step 1. Every recipe still in `write` goes back to step 2; its brief
   now includes the existing recipe, so the subagent completes rather than
   restarts. Stop when `write` is empty.
6. Verify pass (below) on every recipe written in the batch.
7. `cookbook lint -p <cookbook_dir> --since main` before committing.

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
  `<name> fixed N claims, markers M`.

Then check the kept markers yourself against those same rules in the brief
before accepting them: a verify agent is still a writer. The brief is the only
statement of the marker rules; never judge markers by a shorter list of your
own.

## Interpreting coverage

Rows are keyed by spec name. The `problems` column names exactly what keeps a
spec at `partial`. Quote it to the subagent; do not re-derive it. Every graded
rule (the Compliance checks every component cites, the minimum test vectors,
the Design Decision lines, frontmatter `platforms`, the Reference
Implementations rows) is stated once, in the writer rules of
`modules/prompt/prompts/extract/module.md`, which every brief carries as its
preamble; point at the brief, never restate the rules.

A spec listed under "specs with no source file" is not an error: it is a
vocabulary or composite spec with no source of its own.

Reference Implementations problems:

- A row naming a missing path: the code moved or was deleted. After a
  `git mv`, run `cookr relink`; otherwise fix the row.
- A path claimed by another spec too: two specs list the same path. Keep it
  in one; the other lists the files it really describes.
- An unclaimed file shows up as its own row, named by where it sits. To fold
  it into an existing spec, add its path (or its directory, with a trailing
  `/`) to that spec's table; a file row beats a directory row, and the deepest
  directory wins.
- A name collision across roots: two unclaimed files from different roots
  land on one name. Claim each in a spec, or ignore one.

## Arrangement

`cookr arrangement` reports each spec as `aligned` (it sits where its code's
arrangement puts it), `drifted`, `unplaced` (no rows) or `outside` (a row
under no root). A drifted spec either moves in the cookbook (move the spec,
fix its `domain`, then `cookbook bump` it), or its code moves and
`cookr relink` follows. Rearranging the code is the user's call: propose it,
never do it unasked.

## Organize workflow

Converts a repo still on `.cookr.json` and a flat recipes directory.

1. `cookr organize plan --out <scratch>/plan.json` proposes each recipe's
   place and rows, and the `code` block. Show the user the group table it
   prints; they may edit `moves[].to` or the rows before applying.
2. `cookr organize apply --plan <scratch>/plan.json` in a clean work tree
   moves every recipe into `cookbook/`, rewrites domains and references
   repo-wide, writes each Reference Implementations table, patch-bumps each
   spec, writes `cookbook/cookbook.json` and removes `.cookr.json`.
3. `cookbook validate -p <repo>/cookbook`, `cookr coverage`, `cookr arrangement`.

## Non-UI code

Shared code with no visual surface — models, clients, engines — goes under a
root marked `"kind": "logic"` in `cookbook.json`'s `code.roots`. It uses the same `ingredient`
template; `prompt extract` adds the non-UI guidance (contract, errors,
concurrency, persistence; Appearance, States and Accessibility as one
`Not applicable` line each). Python sources use `"platform": "python"`. A directory that mixes view and
model files takes a root-scoped `"ignore"` list (`["**/*ViewController.swift"]`)
so the top-level `ignore` never drops files a UI root needs.

## Behavior notes

- Never edit files in `~/.local/bin/_cookr_pkg/`. Edit `skills/cookr/cli/` in agenticcookbook and re-run `./install.sh`.
- Never `pip install` from this skill.
- `cookbook/cookbook.json` holds the roots and ignores; a spec's own table holds what it claims. Never put either in the other.
