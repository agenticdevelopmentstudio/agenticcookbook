# Compiled cookbook artifacts: source folders, host/model tuning, routed skills

*Created:* 2026-10-03. *Status:* in progress; P1–P4 done.

## Goal

Make every cookbook artifact (principle, guideline, ingredient, recipe), in this
repo and in library cookbooks such as adtoolkit, usable as a skill, without
making "skill" its only form.

An artifact becomes a **source folder**. A **compiler** builds exactly what each
consumer needs from it, and nothing more. One output is a skill. The others are
the reading document, writer briefs and checklists. Wording is tuned **per host
and per model version** at compile time. Authors never tune while writing.

Scale: this repo has about 450 artifacts (45 principles, 351 guidelines, 25
ingredients, 27 recipes). adtoolkit will have about 440 ingredients and 40–70
recipes once it is fully recipe-conformant. That makes about 1,000 skills, so
they are reached through skill-router rather than installed into a host's
skills dir.

## Decisions

| # | Decision | Why |
|---|---|---|
| D1 | Every artifact is a folder with the same layout, whatever its size. | The folder makes room for parts that used to cost too much, such as fuller attribution, rationale and examples. Every artifact having the same layout keeps the tools simple. |
| D2 | Optimize wording at compile time, not when authoring. | Lesson from myagenticteams participants: they are source folders, and a compile step produces only what the team needs. |
| D3 | The compiler is cookr. | The `cookbook` CLI is on its way out (Mike will deal with that later), so new work goes in cookr. |
| D4 | Tuning is shared, neutral source plus opt-in `hosts/` additions. A model reads the repo and writes the additions for itself. cookr owns the renderer; nothing here imports or needs mydevsetup. | The pattern is proven for Claude and Codex elsewhere, and the renderer is small (merge keys, append text). Owning it keeps the cookbook, cookr and skill-router free of a dependency on a personal setup repo. |
| D5 | Tuning targets go down to the model version, not just the host. Example: `claude.opus-5` and `claude.opus-5-5` may differ. | Wording that suits one model version can be wrong for the next. |
| D6 | Routed skills are delivered through skill-router. A few always-on items install into the host directly. | 1,000 skill descriptions in `~/.claude/skills` would load into every session. |

## 1. The artifact source folder

*Built in P1; full spec:*
[artifact source folder](../specs/2026-10-03-artifact-source-folder.md).

```
cookbook/guidelines/implementing/data/transactions-and-concurrency/
  artifact.json                  # format, meta (today's frontmatter), ordered part list
  intro.md                       # `# Title` and its statement
  use-wal-mode-by-default.md     # one part per `## ` section
  ...
  history.md                     # change history
  attribution.md                 # reserved: sources, authors, credit
  examples/                      # reserved: good and bad samples
  hosts/                         # reserved: tuning additions, written by the host/model itself (§3)
    claude.add.md
    claude.opus-5-5.add.md
    codex.add.yaml
```

- **`artifact.json`** replaces the YAML frontmatter. Its `meta` keeps every
  current field, in order, for example `id`, `domain`, `type`, `version`,
  `status`, `summary`, `platforms`, `tags`, `triggers` and `ingredients`.
  - `parts` lists, in order, the files that compose the body. Each entry
    carries its section heading.
  - **One part per section, not semantic parts.** Guidelines use 743
    distinct headings, so a mechanical split into requirements, guidance and
    rationale would lose information. Splitting at the sections is lossless.
  - Files the list doesn't name (attribution, examples, `hosts/`) are extra
    source that the `doc` target ignores.
  - `routes` is optional. If it is absent, routes are derived (§5).
- **Requirements stay single-sourced.** Every target carries the named
  requirements exactly as written. Only the text around them is tuned.
- **Types define the parts.** Each artifact type has a part schema in cookr's
  type registry, derived from today's formatting files.
  - Ingredient parts follow its required section order (Overview, Behavioral
    Requirements, Appearance, States, …).
  - Recipe parts follow its own section order.
- **`agenticdevelopercookbook://` addresses and `#fragment` references keep
  working.** The domain names the folder, and a fragment names a part plus an
  anchor.

## 2. Targets: what the compiler builds

| Target | Output | Consumer |
|---|---|---|
| `doc` | The single `.md` that exists today (frontmatter + sections) | Website, humans, every reader that has not been moved yet |
| `skill` | `SKILL.md` (name, description, `routes:`) + body, rendered per host and model | skill-router; always-on items go into host skills dirs |
| `brief` | Writer and reviewer briefs | cookr's extraction subagents |
| `check` | Lint and review checklist | Reviews, conformance passes |

Each target picks its parts through a **type template** (`templates/<target>/<type>.md`
in cookr). For example, the skill template for a guideline uses the summary
and triggers as the description and the requirements and guidance as the body.
It leaves rationale and history out.

## 3. Tuning: host, model, version

**Target identity.** A dotted chain, from least to most specific:

```
claude  →  claude.opus  →  claude.opus-5-5
codex   →  codex.gpt-5  →  codex.gpt-5-codex
```

**Layering.** The shared source is composed first. Then each matching addition
is applied in order: host, then family, then version. Additions come in
two kinds:

- `<target>.add.yaml` merges frontmatter keys. A key that is already present is
  replaced in place. A new key is appended.
- `<target>.add.md` is appended to the body.

No tuning file is ever named `<target>.md`. On a case-insensitive filesystem
`claude.md` is `CLAUDE.md`, which Claude Code loads as instructions. Compiled
variants are `targets/<target>.SKILL.md` for the same reason.

With no additions, the output is byte-identical to the shared composition.

**Two tuning levels**, because 1,000 artifacts × N targets can't be tuned one
by one:

1. **Type templates per target.** These live at
   `templates/<target-kind>/<type>/hosts/<target>.add.{yaml,md}`. A model tunes
   about ten templates, not a thousand files. This level does most of the work.
2. **Per-artifact exceptions.** An artifact's own `hosts/` additions are written
   only where that artifact reads wrong for that target.

**Host manifest** (cookr data, owned by cookr).
Each host declares:

- its destinations: skills dir, instructions file, router registration;
- its frontmatter dialect;
- its load-time rules, for example Codex's limits on frontmatter keys, name
  length and description length;
- the model families and versions it knows about.

A rendered skill that breaks a load rule makes the install BROKEN. Adding a
host is a manifest entry plus additions, with no code change.

**Model version is resolved at runtime, not install time.** A Claude Code
session can switch models, so routed skills are rendered **lazily** when they
are looked up:

- The router skill tells the model to pass its own identity, for example
  `skill-router show NAME --host claude --model claude-opus-5-5`.
- cookr pre-renders each routed skill for every target in its host manifest.
  The router stores the variants and serves the most specific one that
  matches; it never renders a compiled skill itself.
- Always-on items installed straight into a host dir are rendered for the
  host's configured default model and re-rendered by `cookr install`.

**Self-tuning workflow.** This is a `cookr tune` skill flow.

1. **Identity.** The model states its host and exact model ID from its own
   context. It never guesses from tooling.
2. **Survey.** `cookr payload --target claude.opus-5-5 [--json]` lists each
   template and artifact, the additions it already has at each level, and
   whether those additions are stale.
3. **Templates first.** For each type template, the model asks four questions:
   - Is anything false for me?
   - Is anything true only for me?
   - What can I do that the general version can't assume?
   - Does the general version already work?

   It writes additions at the least specific level where they hold. Something
   true for all Opus models goes in `claude.opus`, not `claude.opus-5-5`.
4. **Exceptions.** Per-artifact additions are written in batched worklists by
   pinned subagents, the same way cookr extraction already works.
5. **Provenance.** Each generated addition records the hash of the source parts
   it was written against (a `cookr:source sha256:` stamp on the addition's
   first line), and `cookr validate` warns about additions that went stale
   after a source edit. Additions are generated in bulk, so a stale addition
   must be visible.

**Neutrality guard.** This is a census in `cookr validate`: shared parts may not
name a host or model family unless the artifact's `artifact.json` gives the
reason in `names_hosts`. A reason with nothing left to explain fails too.

**Codex frontmatter.** Codex loads only `name`, `description`, `license`,
`allowed-tools` and `metadata`. The `skill` target therefore puts `version`,
`routes` and every other cookr key under `metadata`, so one shared rendering
loads on every host without a per-host key move.

## 4. Install: the compiler's other half

`cookr install [--check | --adopt] [--target T] [--dry-run]` and
`cookr uninstall [--target T] [--force] [--dry-run]` have this contract (a check
is `install --check`, as with `compile --check`):

- It is idempotent.
- Each item is in one of four states: OK, MISSING, DRIFT or BROKEN.
- A receipt records what was shipped, so stale output is pruned and nothing
  outside the receipt is touched.

Destinations:

- **Routed** (almost everything): register with skill-router as a named
  **source set**. Refreshing the set replaces it and removes skills that no
  longer exist.
- **Always-on**: a compiled principles skill replaces the hand-maintained
  `general-principles`, which lists 21 principles when 45 exist. It also covers
  the pipeline concerns list. These render into each host's skills dir.

## 5. Routes and naming

- **Names** come from the full artifact path, for example
  `implementing-data-transactions-and-concurrency`. This matters because 85
  guideline basenames repeat across phases with different IDs. Library
  cookbooks are prefixed with the library name, for example `adtoolkit-ui-controls-badge`.
- **Derived routes**, with synonym tiers:

  | Artifact | Route |
  |---|---|
  | Guideline | `coding/<phase>/<category>` |
  | Guideline trigger | Extra route `coding/<trigger>` |
  | Ingredient or recipe | `components/<library>/<group>/<subgroup>`, with the platform as a synonym |
  | Principle | `principles` |

  `routes` in `artifact.json` overrides the derived routes.
- **Vocabulary.** cookr keeps a synonym table, and the router's near-duplicate
  keyword check applies to it.
- **Fan-out.** Each tier is capped so a step shows a navigable list. A test
  over the full compiled set enforces the cap.

## 6. Work by repo

### cookr (this repo, `skills/cookr/`)

- **Type registry:** part schemas per artifact type, derived from
  `cookbook/compliance/artifact-formatting/*`.
- **`cookr convert`:** turns a single-file artifact into a folder.
  - Frontmatter becomes `artifact.json`.
  - Sections become parts.
  - Change History becomes `history.md`.
- **`cookr compile --target <kind> [--for <target>]`:** builds the `doc`,
  `skill`, `brief` and `check` outputs, with layering, templates and load rules.
- **`cookr payload`, `cookr tune` (skill flow), `cookr install [--check]`, `cookr uninstall`.**
- **Library cookbooks** (adtoolkit) use the same code path.
  - cookr reads `cookbook.json`.
  - This repo's top-level `cookbook/` needs a manifest, or a mode that
    `find_cookbook` accepts.
- **Renderer:** cookr's own, in `core/`: chained layering (host → family →
  version) of `.yaml` key merges and `.md` appends. No import from mydevsetup.

### skill-router (peer worktree `skill-router/.claude/worktrees/skills`)

- **Source sets.** `register-dir --source NAME --replace` and
  `unregister --source NAME`. Entries record their source.
- **Per-target variants.** A source set carries cookr's pre-rendered variant
  per target; `show --host H --model M` returns the most specific one, falling
  back model → family → host. Compiled skills ship no `hosts/` folder, so the
  router's existing optional mydevsetup path is never involved. The router skill and its
  `hosts/` additions tell the model to pass its own model ID.
- **Bulk-registration fixes** (from STATUS "deferred minors"):
  - check near-duplicate keywords among the new keywords in a batch;
  - refuse one path under two names;
  - make `show` honour `hide`.
- **Scale.** Fixtures with about 1,000 entries for `route`, `find` and `check`,
  plus a fan-out report in `check`.
- Its tests now run (182 passed, first run 2026-10-03, with Mike's OK).

## 7. Phases

Each phase ends with its tests passing and is merged before the next starts.

| Phase | Deliverable | Done when |
|---|---|---|
| P1 Format ✅ | Type registry, `artifact.json` schema, part layout, written spec | Done 2026-10-03: the schema and registry validate one sample of each type; all 427 artifacts round-trip |
| P2 Convert + `doc` ✅ | `cookr convert`, `cookr compile --target doc` | Done 2026-10-03: all 427 artifacts convert → compile to their normalized source; `compile --check` gates staleness |
| P3 Migrate ✅ | Mechanical conversion of this repo's `cookbook/`; readers switched to the compiled `doc` (index, website sync) | Done 2026-10-03: all 427 converted in one mechanical commit. The compiled `.md` stays committed beside each folder, so readers (indexes, website sync, dev-team) read the `doc` unchanged. Walks skip folder parts; `bump`/`update` write through the folder; `convert --update` folds a `.md` edit back; `validate` fails on a stale doc |
| P4 Tuning engine ✅ | Host manifest, target chain, layered render (cookr's own renderer), load rules, neutrality census, provenance hashes | Done 2026-10-04: `cookr targets`, `cookr render` (BROKEN on a load-rule breach, exit 1), `validate` neutrality + addition checks; 32 artifacts that name a host as subject matter carry `names_hosts` |
| P5 `skill` target + router ✅ | Type skill templates, derived routes and names, skill-router source sets, per-target variants, bulk fixes, scale fixtures | Done 2026-10-04: `cookr compile --target skill` compiles all 427 artifacts (widest node `principles` at 44, cap 50). skill-router 0.2.0 (branch `skills`) reads `metadata.routes`, resolves `--host/--model` to the most specific `targets/` variant without mydevsetup, registers the set with `register-dir --source cookbook --replace` in under a second, and `check` fails any level over 50. Its suite (200) includes a 1,000-skill scale test |
| P6 Install ✅ | `cookr install [--check]` / `cookr uninstall`, receipts, compiled principles skill replacing `general-principles` | Done 2026-10-04: in a scratch HOME against the real skill-router CLI, install compiles and registers all 427 skills and writes the principles skill for `claude.opus-5-5` and `codex.gpt-5-codex`; a hand-kept `general-principles` is BROKEN until `--adopt`; a rerun is a no-op; `--check` is all OK; uninstall restores the original and leaves nothing else. Replacing the live `general-principles` waits for Mike's OK |
| P7 Self-tune ✅ Done 2026-10-04 | `cookr payload`, `cookr stamp` and the Tuning workflow in the cookr skill; first passes as `claude.opus-5-5` (3 template additions) and `codex` (empty: it cannot see its model ID, and the templates already work for it). Additions are `<target>.add.{md,yaml}` and variants `targets/<target>.SKILL.md`, because `claude.md` is `CLAUDE.md` on a case-insensitive filesystem | Templates carry additions; stale-addition check works after a source edit |
| P8 adtoolkit ✅ Done 2026-10-04 | Its cookbook converted to folders, compiled, registered as source `adtoolkit`. Verified on a scratch copy with a scratch registry: 387/387 convert and round-trip, compile with no node over the cap, register beside the cookbook's 427, and route correctly ("add a settings row on macOS" → `platform/macos/ui/settings/rows`). Fixes it needed: convert had deleted child specs when a parent spec's folder was their directory, and now shares that folder; a concept-organized library is placed below its `cookbook.json`; and sets register with `--new-keyword`, reporting near-duplicates such as `service`/`services`. The adtoolkit repo itself is unchanged until the conformance work | Routing finds the right ingredient for real requests, e.g. "add a settings row on macOS" |

**Next, outside this plan:** bring adtoolkit to 100% recipe conformance. Today
it has 6 recipes, 62 components with no spec and 380 with partial specs.

## Risks

- **Pre-rendered variants grow with targets.** Each routed skill is rendered
  once per manifest target; a model the manifest doesn't list falls back to
  its family or host until it is added.
- **Cost of bulk tuning.** Template-first tuning keeps per-artifact passes rare.
  Each pass is a pinned-subagent worklist with a cost estimate printed before it
  runs.
- **Migration blast radius.** P3 touches every artifact. The `doc` round trip
  in P2 is the gate, and the conversion is one mechanical commit, separate from
  any content edits.
