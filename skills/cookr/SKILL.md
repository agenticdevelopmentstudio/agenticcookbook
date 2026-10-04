---
name: cookr
version: "0.11.0"
description: "Inventory, coverage, extraction prompts and arrangement for the specs of a library cookbook (a repo's cookbook/ directory with cookbook.json). Wraps the `cookr` CLI at ~/.local/bin/cookr. Use when the user asks which components have specs, what is left to write for a group, to write the spec for a component, to convert a .cookr.json repo into a cookbook, to relink specs after code moved, to convert artifacts into source folders and compile them back into docs, to compile them into routed skills for skill-router, to install, check or uninstall the compiled skills (the routed set and the always-on principles skill), or to tune them for the host and model you are running as (payload, stamp)."
argument-hint: "[--help] [-p <repo-root>] <inventory|coverage|arrangement|relink|convert|compile|install|uninstall|payload|stamp|organize plan|apply|prompt extract <name>|--tier <group>> [...]"
allowed-tools: Bash(cookr *), Bash(command -v cookr)
model: sonnet
---

# cookr v0.11.0

Thin wrapper around the `cookr` CLI at `~/.local/bin/cookr`. All work goes
through the CLI — never duplicate its logic in this skill, including recipe
frontmatter, indexes, validation and lint (`cookr update`, `cookr validate`,
`cookr lint`, `cookr bump`).

## Startup

```bash
command -v cookr
```

If missing, tell the user:

> The `cookr` CLI is not installed. Run `skills/cookr/setup/install` from the agenticcookbook repo, then re-invoke me.

…and stop.

## The library cookbook

A repo's specs live in `<repo>/cookbook/`, grouped by concept, general to
specific (`cookbook/ai/chat/chat-context.md`), never by platform. A spec's name is its
path there without `.md`; its `domain` is `<scheme>://cookbook/<name>`. Each
spec lists its code in a `## Reference Implementations` table of repo-relative
paths (a trailing `/` claims a whole directory). `cookbook/cookbook.json`'s
`code` block lists the source roots, so a file no spec claims yet still shows
up, named inside its root's `recipes` group. A "tier" or group is any
directory of the cookbook (`--tier ai-plugin-kit/chat`).

## Routing

| Request | Command |
|---|---|
| what components exist / what groups there are | `cookr inventory [--tier <group>]` |
| what is left to write | `cookr coverage [--tier <group>]` |
| write the recipe for X | `cookr prompt extract X --out-dir <dir>` → dispatch (below) |
| write everything a group still needs | extraction workflow (below) |
| is every spec in its code's concept group | `cookr arrangement [--tier <group>]` |
| code moved (`git mv`) | `cookr relink [--since <ref>] [--dry-run]` |
| convert a `.cookr.json` repo | organize workflow (below) |
| turn `.md` artifacts into source folders | `cookr convert [paths] [--dry-run] [--out <dir>] [--remove-source]` |
| fold an edited `.md` back into its folder | `cookr convert --update [--force] <paths>` |
| build the single-file docs from source folders | `cookr compile --target doc [paths] [--out <dir>] [--check] [--force]` |
| compile artifacts into routed skills | `cookr compile --target skill [paths] --out <set-dir> [--library L] [--check]` |
| which hosts / models cookr tunes for | `cookr targets [--host H] [--model M] [--json]` |
| what a skill looks like on a host / model, and does it load | `cookr render <skill-dir> --host H [--model M] [--out <file>] [--check]` |
| is the group written | `cookr prompt extract --tier <group> --out-dir <dir>` lists nothing to write |
| is the phase done | `cookr coverage --tier <group> --require complete` then `cookr validate -p <cookbook_dir>` |
| no args / `--help` | `cookr --help`, present the module table verbatim |

Forward `-p <repo-root>` to every `cookr` call when the user supplies one;
otherwise run from cwd and let the CLI find `cookbook/cookbook.json`. Pass
`cookr` the absolute `cookbook_dir` from the worklist JSON below, never a
cwd-relative path.

## Source folders

An artifact source folder is `<name>/artifact.json` plus one `<part>.md` per
section. The spec is `docs/superpowers/specs/2026-10-03-artifact-source-folder.md`
in the agenticcookbook repo. `convert` refuses any file that would not compose
back byte for byte. It reports type-shape problems (missing or out-of-order
sections) without failing. `compile --check` exits 1 when a doc is missing or
stale, and `cookr validate` runs the same check. Once an artifact has a folder,
the folder is the source: edit its parts and run `cookr compile`, or edit the
`.md` and run `cookr convert --update` on it. A plain `convert` skips an
artifact that already has a folder, and a doc with no folder fails `validate`,
`compile` and `install`.

`artifact.json` records `synced`, the digest of the doc cookr last wrote, so
cookr knows which side changed when a doc and its folder disagree:
- **Doc edited:** `compile` refuses to overwrite it. `convert --update` folds the
  edit in; `compile --force` discards it.
- **Folder edited:** `compile` writes the doc. `convert --update` refuses to
  fold over the folder's edit; `convert --update --force` discards it.
- **Both edited** (or no record and they differ): both refuse. Keep one side
  with `convert --update --force` (the doc) or `compile --force` (the folder).

`bump`, `update`, `relink` and `organize` edit from the newer side, write
through the folder and record the sync; they refuse an artifact edited on both
sides. `organize` refuses to move a doc that already has a folder.

A spec with child specs (`telemetry.md` beside `telemetry/sources.md`) shares
its folder with them: `telemetry/` holds the parent's `artifact.json` and parts
next to the children's docs and folders. An artifact owns only its manifest and
its parts, so writing it never removes anything else, and `convert` refuses a
part that would overwrite another file (rename the section or the child).

## Host tuning

Shared text names no host or model. Wording true for one host, family or model
goes in a `hosts/` addition beside the source: `hosts/<target>.add.md` is appended
to the body, and `hosts/<target>.add.yaml` (flat `key: value` lines) is merged into
the frontmatter. A target is `claude`, `claude.opus` or `claude.opus-5-5`; the
host list ships in cookr (`cookr targets`). `cookr render` applies the additions
host → family → version and reports BROKEN, exiting 1, when the result would not
load on that host (Codex accepts only `name`, `description`, `license`,
`allowed-tools` and `metadata` in frontmatter). `cookr validate` fails an
artifact whose shared text names a host unless its `artifact.json` gives the
reason in `names_hosts`, fails an addition it cannot apply, and warns when a
stamped addition was written against an older source.

## Tuning workflow

A model tunes the cookbook for itself. Nobody can tune for a model they are not.

1. **Identity.** State your host and exact model ID from your own context, for
   example the system prompt's "the exact model ID is …". Never infer it from
   tooling or from which CLI is installed. The target is `<host>.<version>`,
   for example `claude.opus-5-5` or `codex.gpt-5-codex`. If your context does
   not show your model ID (Codex's first pass could not see it), your target is
   the bare host, for example `codex`, and you write only `<host>.add.*`
   additions, never a family or version one.
2. **Survey.** Run `cookr payload --target <target> --json`. For each level it
   prints `source_sha256` and the additions it already has along your chain,
   with `stale` set on any written against an older source. Templates come with
   their `text`. A template level is `template:<kind>` (every skill of one type)
   or `always:principles` (the always-on principles skill).
3. **Templates first.** For each template, ask four questions:
   - Is anything here false for me?
   - Is anything true only for me?
   - What can I do that the general version cannot assume?
   - Does the general version already work?

   If it already works, write nothing; an empty pass is a valid result. Otherwise
   write the addition at the **least specific level where it holds**: true for
   every Claude model goes in `<hosts_dir>/claude.add.md`, true for every Opus
   model in `claude.opus.add.md`, true only for you in `claude.opus-5-5.add.md`. A `.md`
   addition is appended to the body; a `.yaml` addition merges frontmatter keys.
   Keep each one short. It is read every time the skill loads.
4. **Exceptions.** Run `cookr payload --target <target> --out-dir <scratch dir>
   --batch-size 25` to write worklists. Each entry holds the skill as you
   receive it today (`text`) and the file to write (`write_to`). Ask the same
   four questions per artifact, and write only where the artifact itself needs
   more than its template's addition. Work the worklists with subagents running
   **your own model**. Pinning them to a cheaper model would tune for the wrong
   model. Run up to 8 at a time.
5. **Stamp.** Run `cookr stamp <addition>...` on every addition you wrote or
   re-checked, then run `cookr validate` (it warns about stale additions and
   fails on ones it cannot apply). Render a sample with `cookr render` or
   `cookr compile --target skill --check` to confirm each host still loads.

## Skills

`compile --target skill --out <set-dir>` makes one skill per artifact.
- **Name:** the path below the type directory, joined with `-` (a one-segment
  path keeps its type: `principle-simplicity`). `--library L` prefixes it. A
  library cookbook grouped by concept rather than type uses the path below its
  root (the directory holding `cookbook.json`): `ui/settings/rows/button-view`
  becomes `adtoolkit-ui-settings-rows-button-view`.
- **Routes:** derived from the type:
  - guidelines: `coding/<phase>[/<category>]`, plus
    `coding/when/<trigger>/...` for each trigger;
  - principles: `principles`;
  - ingredients and recipes: `components/<library>/...`, plus a platform branch.
  `routes` in `artifact.json` overrides them.
- **Text:** the type's template in `cookr/data/templates/skill/` decides which
  sections stay. Rationale and history are left out. Templates are read from
  `$COOKR_TEMPLATES` when set, else from the cookbook's own repo
  (`skills/cookr/cli/cookr/data/templates/`) when it has one, else from the
  installed cookr.
- **Frontmatter:** `name` and `description` only. Every cookr key goes under
  `metadata:`, so the shared SKILL.md loads on every host.
- **Variants:** a host or model that reads differently gets
  `targets/<target>.SKILL.md`. `targets.json` (the host table) sits at the set's root,
  next to `skills.json` (the receipt).

A recompile prunes only what the receipt lists. `--check` exits 1 when anything
is stale or missing. The set fails on a duplicate name, a rendering a host would
refuse, or a route level over 50 entries.

Register the set with skill-router as one source:
`skill-router-registry register-dir <set-dir> --source cookbook --replace`.
`cookr install` does this for you. It passes `--new-keyword`: a set's
keywords are its library's directory names, so a near-duplicate such as
`service` beside `services` is accepted and listed in the `routed:` detail
rather than refused.

## Install

`cookr install [paths] [--target T]... [--library L] [--adopt] [--force] [--replace] [--dry-run] [--check] [--json]`
puts a compiled cookbook where agents reach it. There are three items:
- **`set:<library>`**: the routed skills, compiled into `$COOKR_HOME/sets/<library>`
  (`$COOKR_HOME` defaults to `~/.cookr`).
- **`routed:<library>`**: that set, registered with skill-router as source `<library>`
  through `skill-router-registry`, or the command in `$COOKR_SKILL_ROUTER_REGISTRY`.
- **`always-on:<host>:<name>`**: the principles skill, rendered for one target into
  the host's skills dir. It is `general-principles` for this cookbook and
  `<library>-principles` for a library. It lists every principle with its gist
  and routed skill, then the pipeline concerns from `workflows/pipeline-concerns.json`
  (`--concerns` overrides that path).

`--target` is `routed`, or a host target: `claude` (its default model), a
family such as `claude.opus`, or a model such as `claude.opus-5-5`. You may give
one target per host. With no `--target`, cookr installs the routed set and the
always-on skill for every host whose home directory exists.

Each item is OK, MISSING, DRIFT or BROKEN. `--check` changes nothing and exits 1
unless everything is OK. Install is idempotent.

A skill dir that cookr did not install is BROKEN and is left alone. `--adopt`
moves it to `$COOKR_HOME/backup/`, and uninstall puts it back. If you edit the
always-on file after install, it is DRIFT, and install will not overwrite it
unless you pass `--force`. A library already installed from other paths is
refused; `--replace` installs it over them, replacing every skill it installed.

`$COOKR_HOME/install.json` is the receipt. `cookr uninstall [--target T]
[--library L | --every-library] [--force] [--dry-run]` removes only what the
receipt lists, for `--library`'s library (default `cookbook`) or, with
`--every-library`, every library it lists. It unregisters the routed set,
deletes the set, removes the always-on skill (restoring any adopted original)
and removes any dirs install created. An edited always-on file stays unless you
pass `--force`.

Never adopt or replace the user's live `general-principles` without their OK.

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
3. `cookr update -p <cookbook_dir> --author "<user>"` — fills empty
   frontmatter. A writer that rewrote an existing recipe (`existing: true`)
   has already recorded it with `cookr bump`, as its brief says; never bump
   it again, and never hand-edit `version`, `modified` or Change History.
4. `cookr validate -p <cookbook_dir>` and `cookr coverage --tier <group>`.
   Coverage grades each recipe's `domain` against the one its path derives
   (the worklist's `domain`), so a wrong scheme or directory shows up in
   `problems` like any other gap.
5. Rerun step 1. Every recipe still in `write` goes back to step 2; its brief
   now includes the existing recipe, so the subagent completes rather than
   restarts. Stop when `write` is empty.
6. Verify pass (below) on every recipe written in the batch.
7. `cookr lint -p <cookbook_dir> --since main` before committing.

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

`cookr arrangement` reports each spec as `aligned` (it sits in, or anywhere
below, the `recipes` group of the root its code is under), `drifted`,
`unplaced` (no rows) or `outside` (a row under no root). A drifted spec either
moves into its group in the cookbook (move the spec, fix its `domain`, then
`cookr bump` it), or its root's `recipes` changes. Rearranging the code is the user's call: propose it,
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
3. `cookr validate -p <repo>/cookbook`, `cookr coverage`, `cookr arrangement`.

## Non-UI code

Shared code with no visual surface — models, clients, engines — goes under a
root marked `"kind": "logic"` in `cookbook.json`'s `code.roots`. It uses the same `ingredient`
template; `prompt extract` adds the non-UI guidance (contract, errors,
concurrency, persistence; Appearance, States and Accessibility as one
`Not applicable` line each). Python sources use `"platform": "python"`. A directory that mixes view and
model files takes a root-scoped `"ignore"` list (`["**/*ViewController.swift"]`)
so the top-level `ignore` never drops files a UI root needs.

## Behavior notes

- Never edit files in `~/.local/bin/_cookr_pkg/`. Edit `skills/cookr/cli/` in agenticcookbook and re-run `skills/cookr/setup/install`.
- Never `pip install` from this skill.
- `cookbook/cookbook.json` holds the roots and ignores; a spec's own table holds what it claims. Never put either in the other.
