# Status — compiled artifacts and routed skills

*Updated:* 2026-10-04. *Derives from:* `226f310` (PR #64, agenticcookbook) and
`2ac4109` (PR #2, skill-router), both merged 2026-10-04.

Read this first to resume the work. The design lives in the
[plan](../superpowers/plans/2026-10-03-compiled-artifacts-and-skills.md) and the
[source folder spec](../superpowers/specs/2026-10-03-artifact-source-folder.md).

## Where things stand

Every cookbook artifact (427 of them: principles, guidelines, ingredients,
recipes) is now a **source folder** (`<name>/artifact.json` plus one `.md` per
section). The `<name>.md` beside it is compiled from the folder and stays
committed, so readers (index, website sync, dev-team) are unchanged.

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

skill-router 0.2.0 reads cookr's `metadata:` routes, picks
`targets/<target>.SKILL.md` variants, registers whole sets with
`register-dir --source <name> --replace`, enforces a fan-out cap of 50, and
reports `--version`.

The old `cookbook` CLI is absorbed into cookr; the adh plugin was dropped.

## Verified

- cookr unit tests: 779 passed (Python 3.9: 775 passed, 4 skipped).
- `cookr validate` passes on the repo.
- Install and uninstall were exercised only in a scratch HOME against a scratch
  skill-router registry, never against the live one.
- adtoolkit (P8) was verified on a scratch copy: 387/387 convert and
  round-trip, compile under the cap, register beside the cookbook, and route
  correctly. The adtoolkit repo itself was not changed.
- All 15 findings from a whole-branch `/code-review max` are fixed with tests;
  the mapping is in a comment on PR #64.

## Not done — each needs Mike's explicit OK

- **Live install.** Neither `./install` of cookr nor a live `cookr install`
  has run. The live `~/.claude/skills/general-principles` and the live
  skill-router registry are untouched; replacing `general-principles` with the
  compiled principles skill happens at that install.
- **skill-router install, CI and live registration** — none done.

## Next

- Bring adtoolkit to 100% recipe conformance (6 recipes, 62 components with no
  spec and 380 with partial specs), then convert, compile and register it as
  source `adtoolkit`. This is separate work, not part of the plan above.
- The corpus conformance gaps listed at the end of the spec (recipes that
  predate the section order, ingredients missing `## Compliance`) are still
  open. Those artifacts convert and compile regardless.
