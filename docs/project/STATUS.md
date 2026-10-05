# Status — compiled artifacts and routed skills

*Updated:* 2026-10-04. *Derives from:* `226f310` (PR #64, agenticcookbook),
`2ac4109` (PR #2, skill-router), and PR #66 (`revise-corpus-conformance`).

Read this first to resume the work. The design lives in the
[plan](../superpowers/plans/2026-10-03-compiled-artifacts-and-skills.md) and the
[source folder spec](../superpowers/specs/2026-10-03-artifact-source-folder.md).

## Where things stand

Every cookbook artifact (456 of them: 44 principles, 351 guideline files — 258
unique — 48 ingredients, 13 recipes) is a **source folder**
(`<name>/artifact.json` plus one `.md` per section). The `<name>.md` beside it
is compiled from the folder and stays committed, so readers (index, website
sync, dev-team) are unchanged.

cookr (`skills/cookr/`, cookr 0.10.0, cookr skill 0.11.0) is the compiler:

- `convert` / `convert --update` — doc → folder, lossless; folds `.md` edits back.
- `compile --target doc|skill [--for T]` — folder → doc, or → one routed skill
  per artifact with per-host/per-model variants.
- `targets`, `render`, `payload`, `stamp` — the host/model tuning engine and
  the self-tune flow.
- `install [--check|--adopt|--force|--replace]`, `uninstall [--every-library]`
  — register the routed set with skill-router and write the always-on
  principles skill per host, under a receipt.
- `validate` — neutrality census, addition checks, stale docs, and the sync
  record (doc vs. folder; see the spec's *Sync record*).
- `organize` — writes a library manifest whose `structure` is
  `{"kind": "library"}`, which `cookbook.schema.json` allows.

skill-router 0.2.0 reads cookr's `metadata:` routes, picks
`targets/<target>.SKILL.md` variants, registers whole sets with
`register-dir --source <name> --replace`, enforces a fan-out cap of 50, and
reports `--version`.

The old `cookbook` CLI is absorbed into cookr; the adh plugin was dropped.

### Corpus conformance (PR #66)

Every artifact now passes its own type's format (cookr's per-type validation:
zero failing). In particular:

- Guidelines carry the intro statement; the 18 legacy ingredients follow the
  ingredient format.
- The 12 recipes that predated the recipe format were restructured into
  **compositions of ingredients**, extracting 29 new ingredients
  (`ingredients/app/`, `ingredients/autonomous-dev-bots/`,
  `ingredients/ui/windows/`, `ingredients/ui/apps/`, more under
  `infrastructure/` and `developer-tools/claude/`). The restructured recipes
  moved to 2.0.0 (pr-review-pipeline to 1.0.0).
- References into the old recipe files were retargeted to the new ingredients;
  `cookbook/index.md`, section INDEX files, README and CLAUDE.md counts match
  the corpus.

## Installed (2026-10-04, on Mike's instruction)

- `./install` of cookr: `~/.local/bin/cookr` and the `cookr` skill.
- Live `cookr install`: the routed set `cookbook` registered with skill-router
  (`~/.cookr/sets/cookbook`), and the compiled always-on `general-principles`
  skill written for Claude and Codex. The replaced originals are backed up
  under `~/.cookr/backup/`; the receipt is `~/.cookr/install.json`.

## Verified

- cookr unit tests: 779 passed (Python 3.9: 775 passed, 4 skipped), plus the
  organize schema test.
- `cookr validate` passes; `cookr compile --check` reports 456 of 456 current.
- adtoolkit (P8) was verified on a scratch copy: 387/387 convert and
  round-trip, compile under the cap, register beside the cookbook, and route
  correctly.
- All 15 findings from a whole-branch `/code-review max` of PR #64 are fixed
  with tests; the mapping is in a comment on PR #64.

## Not done — each needs Mike's explicit OK

- **skill-router install and CI** — none done.
- **Registering adtoolkit** with the live skill-router registry.

## In progress

- adtoolkit 100% recipe conformance, branch `recipe-conformance` in an
  adtoolkit worktree: every spec under its `cookbook/` must grade `complete` in
  `cookr coverage`, and the specs with empty Reference Implementations must
  name their code. Work proceeds in batches, one commit per batch.
