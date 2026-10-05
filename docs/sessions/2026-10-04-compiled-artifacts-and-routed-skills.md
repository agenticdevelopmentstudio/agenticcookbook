# Session: cookbook artifacts as routed skills, corpus conformance, and adtoolkit conformance

- **Date:** 2026-10-04
- **Session:** `7c571d03-8f17-49c6-b3e9-35e397d0245d`
- **Branch:** `skills` (agenticcookbook, PR #64), `skills` (skill-router, PR #2), `revise-corpus-conformance` (agenticcookbook, PR #66), `recipe-conformance` (adtoolkit, in progress)

## Orientation

Mike wanted the cookbook's principles, guidelines, ingredients and recipes to be usable as skills as well. The target scale is about 1,000 skills once adtoolkit's library is recipe-conformant.

So far in this session:

- We planned the work and built it in phases P1–P8 across cookr and skill-router.
- We ran a whole-branch `/code-review max`, fixed all 15 findings, and shipped:
  - agenticcookbook as `226f310`;
  - skill-router as `2ac4109` (0.2.0).
- On Mike's instruction ("install cookr, keep going finish all this start the adtoolkit in a worktree when you get to that step"):
  - cookr is installed live;
  - the cookbook corpus was brought to its own type formats (PR #66, merged as `f813f6a1`);
  - the live install was refreshed afterwards, with all 456 skills registered.

**In progress:** adtoolkit's specs are being made 100% `complete` under `cookr coverage` on the adtoolkit branch `recipe-conformance`, in batches. See [STATUS](../project/STATUS.md).

## Decisions

The plan's decision table (D1–D6) holds the main design decisions and their reasons; they are not repeated here. Decisions made later, during the build, the review and the conformance work:

### Compiled artifacts

- **Keep the compiled `.md` committed beside every folder.** Readers (index, website sync, dev-team) keep reading the single-file doc unchanged, so the migration touched no reader.
- **Add a sync record (`synced` in `artifact.json`).**
  - The review found two silent overwrites: `compile` could overwrite a hand-edited `.md`, and `convert --update` could overwrite a folder edit.
  - A digest of the last doc cookr wrote tells which side changed.
  - A guard refuses the destructive direction unless `--force` is given.
  - The editing tools (`bump`, `update`, `relink`, `organize`) start from whichever side is newer.
- **The install refuses anything destructive by default.**
  - It refuses a missing folder set, another library's paths (unless `--replace`), an edited always-on skill (unless `--force`), and a render the host would not load.
  - The receipt is written atomically under a lock.
  - `uninstall` removes one library unless given `--every-library`.
- **cookr checks `skill-router-registry --version`.** An older router would misread the flags cookr passes, so cookr refuses any version below 0.2.0.
- **Name tuning files `<target>.add.{md,yaml}`.** A file named `claude.md` is the same file as `CLAUDE.md` on a case-insensitive filesystem.

### Corpus conformance (PR #66)

- **Restructure the old recipes into compositions of ingredients**, rather than relaxing the recipe format.
  - 12 recipes held component-level behavior directly, so that behavior was extracted into 29 new ingredients.
  - Each recipe now wires its ingredients together and moved to 2.0.0.
  - This keeps a single rule set (recipe = composition) for compile and routing.
- **`cookr organize` writes `structure: {"kind": "library"}`.** `cookbook.schema.json` rejects the `name` key that organize used to write.

### adtoolkit conformance

- **Resolve each `NEEDS REVIEW` marker by reading the code, never by deleting it.**
  - If the behavior is implemented, it becomes a normal requirement.
  - If it is not, the requirement is restated as current behavior, and a Design Decision with `**Approved**: pending` records the gap.
  - A marker is never left in place, because any marker keeps the spec `partial`.
- **Judge Compliance statuses from the code.** `unit-test-coverage` is `failed` when no tests exist, rather than claimed as passed.
- **Leave adtoolkit's legacy `recipes/` and `.cookr.json` alone.** Their fate is Mike's open decision (D4).

## Considered and rejected

- **Importing mydevsetup's renderer** for host tuning. cookr owns a small renderer instead, so neither the cookbook nor skill-router depends on a personal setup repo (plan D4).
- **Installing every compiled skill straight into the host's skills dir.** With about 1,000 skills, every description would load into every session. They go through skill-router instead; only the principles skill is always-on (plan D6).
- **Tuning wording while authoring.** Tuning happens at compile time, per host and model version (plan D2, D5).
- **Moving a doc that has a folder (`organize`).** Moving the doc alone would orphan its folder, so `organize` now refuses it.
- **Following `cookr prompt extract`'s instruction to emit `NEEDS REVIEW` markers for gaps** when writing missing adtoolkit specs. A marker keeps the spec incomplete, so gaps become pending decisions instead.
- **Large subagent fan-out for the adtoolkit batches.** Batches run at most 4 agents at once, after an earlier 20-agent fan-out exhausted the weekly limit.

## Open threads

- **adtoolkit `recipe-conformance`:**
  - Batches 01 and 02 are committed; batches 03–11 remain.
  - After the batches:
    - re-grade with all specs complete and no unmatched recipes;
    - convert the specs to source folders and run `cookr validate`;
    - update adtoolkit's `docs/project/cookbook-organization.md`;
    - open the PR and land it.
- **Needs Mike's explicit OK:**
  - registering adtoolkit with the live skill-router registry;
  - skill-router's install and CI.
- **Stale skills:** the lint-artifact and approve-artifact skills have stale recipe checks and no ingredient section, so the cookr validator was used instead.

## Pointers

- Plan: [compiled artifacts and skills](../superpowers/plans/2026-10-03-compiled-artifacts-and-skills.md)
- Spec: [artifact source folder](../superpowers/specs/2026-10-03-artifact-source-folder.md), including the *Sync record* section
- Status: [STATUS](../project/STATUS.md)
- Code: `skills/cookr/cli/cookr/` (`core/artifact.py`, `core/artifact_build.py`, `core/install.py`, `core/organize.py`, `core/completeness.py`, `modules/`)
- The PR #64 comment maps each of the 15 review findings to its fix. PR #66 holds the corpus conformance.
