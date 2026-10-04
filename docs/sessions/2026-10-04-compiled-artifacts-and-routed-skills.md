# Session: cookbook artifacts as source folders, compiled into routed skills

- **Date:** 2026-10-04
- **Session:** `7c571d03-8f17-49c6-b3e9-35e397d0245d`
- **Branch:** `skills` (agenticcookbook, PR #64), `skills` (skill-router, PR #2)

## Orientation

Mike wanted the cookbook's principles, guidelines, ingredients and recipes to
be usable as skills too, at the scale of about 1,000 skills once adtoolkit's
library is recipe-conformant. Over this session we planned that work, built
it in phases P1–P8 across cookr and skill-router, ran a whole-branch
`/code-review max`, fixed all 15 findings, and shipped both branches on
2026-10-04. The agenticcookbook branch merged as `226f310` and the skill-router
branch as `2ac4109` (0.2.0). The work is done and merged. What remains is the
live install, which waits for Mike's OK. See
[STATUS](../project/STATUS.md).

## Decisions

The plan's decision table (D1–D6) holds the main design decisions and their
reasons; they are not repeated here. Decisions made later, during the build
and the review:

- **Keep the compiled `.md` committed beside every folder.** Readers (index,
  website sync, dev-team) keep reading the single-file doc unchanged, so the
  migration touched no reader.
- **Add a sync record (`synced` in `artifact.json`).** The review found that
  `compile` could overwrite a hand-edited `.md`, and `convert --update` could
  overwrite a folder edit, with no warning. A digest of the last doc cookr
  wrote tells which side changed. A guard refuses the destructive direction
  unless `--force` is given, and the editing tools (`bump`, `update`,
  `relink`, `organize`) start from whichever side is newer. All 427 manifests
  were backfilled in one commit.
- **The install refuses anything destructive by default.** It refuses a
  missing folder set, another library's paths (`--replace` overrides), an
  edited always-on skill (`--force` overrides) and a render the host would not
  load. The receipt is written atomically under a lock. `uninstall` removes
  one library unless given `--every-library`. Each of these came from a
  review finding about losing an installed set.
- **cookr checks `skill-router-registry --version`.** An older router would
  misread the flags cookr passes, so skill-router gained `--version` (0.2.0)
  and cookr refuses anything older.
- **Name tuning files `<target>.add.{md,yaml}`.** A file named `claude.md` is
  the same file as `CLAUDE.md` on a case-insensitive filesystem.
- **adtoolkit stays untouched.** P8 was verified on a scratch copy only.
  Making adtoolkit recipe-conformant, and registering it, is separate later
  work. It is not part of this effort.

## Considered and rejected

- **Importing mydevsetup's renderer** for host tuning. cookr owns a small
  renderer instead, so neither the cookbook nor skill-router depends on a
  personal setup repo (plan D4).
- **Installing every compiled skill straight into the host's skills dir.**
  With about 1,000 skills, every description would load into every session.
  They go through skill-router instead; only the principles skill is
  always-on (plan D6).
- **Tuning wording while authoring.** Tuning happens at compile time, per host
  and model version (plan D2, D5).
- **Moving a doc that has a folder (`organize`).** Moving the doc alone would
  orphan its folder, so `organize` now refuses it.

## Open threads

- **Live install.** Running `./install` of cookr, a live `cookr install`, and
  replacing `~/.claude/skills/general-principles` all wait for Mike's explicit
  OK. The skill-router registry and its install and CI also need his OK.
- **adtoolkit to 100% recipe conformance**, then registering it as source
  `adtoolkit`.

## Pointers

- Plan: [compiled artifacts and skills](../superpowers/plans/2026-10-03-compiled-artifacts-and-skills.md)
- Spec: [artifact source folder](../superpowers/specs/2026-10-03-artifact-source-folder.md),
  including the *Sync record* section
- Status: [STATUS](../project/STATUS.md)
- Code: `skills/cookr/cli/cookr/` (`core/artifact.py`, `core/artifact_build.py`,
  `core/install.py`, `modules/`)
- The PR #64 comment maps each of the 15 review findings to its fix
