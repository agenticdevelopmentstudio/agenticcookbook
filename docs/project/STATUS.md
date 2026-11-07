# Status — compiled artifacts and routed skills

*Updated:* 2026-11-07. *Derives from:* `226f310` (PR #64, agenticcookbook),
`2ac4109` (PR #2, skill-router), PR #66 (`revise-corpus-conformance`), and
PR #72 (`dd2e4670`, `44c510bf`).

Read this first to resume the work. The design lives in the
[plan](../superpowers/plans/2026-10-03-compiled-artifacts-and-skills.md) and the
[source folder spec](../superpowers/specs/2026-10-03-artifact-source-folder.md).

## Where things stand

Every cookbook artifact (456 of them: 44 principles, 351 guideline files — 258
unique — 48 ingredients, 13 recipes) is a **source folder**
(`<name>/artifact.json` plus one `.md` per section). Since `971a6490` the
folder is the only committed form; no compiled `<name>.md` sits beside it, and
readers that want a doc compile one (./install compiles cookr's references).

**Open:** cookr's `validate` and `update` still read docs, not folders. On this
repo, validate reports every artifact's doc `missing` and its frontmatter checks
see 0 artifacts. `update` would rebuild the indexes from no docs, so do not run
it here until they read folders.

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
  record (doc vs. folder; see the spec's *Sync record*). Since PR #72 it also
  runs two guideline censuses (`cookr/core/twins.py`):
  - **Twins**: a guideline filed under several use cases (same path below
    `guidelines/<use-case>/`) must match its twins, ignoring history and links
    to its own use case. A twin rewritten on purpose records why in
    `twin_differs` in its artifact.json. Findings: `drift`, `stale` (a reason on
    a twin that matches), `short` (reason under 16 characters).
  - **Rules**: every guideline states at least one RFC 2119 rule
    (MUST/SHOULD/MAY), or records `informational` in its artifact.json.
  - Compiling warns (does not fail) on a SKILL.md over 500 lines
    (`LINES_MAX` in `cookr/core/skill.py`).
  These came from the abandoned `skill-based-cookbook` branch; the corpus was
  fixed to pass them in the same PR.
- `organize` — writes a library manifest whose `structure` is
  `{"kind": "library"}`, which `cookbook.schema.json` allows.

skill-router reads cookr's `metadata:` routes, picks
`targets/<target>.SKILL.md` variants, enforces a fan-out cap of 50, and
reports `--version`. Since 0.4.0 it is one CLI (`skill-router`) that registers
one skill at a time and keeps per-host copies under `~/.skill-router/<host>/`;
it has no `register-dir` or `--source` sets. cookr registers each skill of a
set and finds the set again by the skills' registered origin (2026-11-07).

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

## Installed (2026-11-07, on Mike's instruction)

- `./install --cli-only` of cookr: `~/.local/bin/cookr`. Its references are
  compiled from the source folders.
- Live `cookr -p <main checkout> install --replace`: the set `cookbook`
  (`~/.cookr/sets/cookbook`, 486 skills) is compiled from this repo's main
  checkout and registered with skill-router 0.4.0 for Claude and Codex. The
  receipt is `~/.cookr/install.json`.
- The always-on `general-principles` skill for Claude and Codex was edited by
  hand after its 2026-10-04 install, so it was not overwritten. Its receipt
  still names the old `adh/agenticcookbook` checkout, so `install --check`
  reports `library:cookbook` BROKEN until `--force` rewrites it or it is kept
  as it is.
- skill-router's hooks are installed (since skill-router `371f3b3`, `./install`
  always writes them). The prompt hook adds a `skill-router: likely <route>`
  hint when a prompt matches a route's keywords, which is now the main pointer
  from a session to the routed cookbook skills. It matches by keyword only (a
  prompt such as "write a pytest test" gets no hint). This repo has no
  `.skill-router.json`, so enforcement is `nudge`: nothing is gated.
- Routed lookups serve the installed set compiled from the main checkout, not a
  worktree's edits; re-run `cookr -p <main checkout> install --replace` after
  artifact changes merge.

## Verified

- cookr test suite at PR #72: 814 passed, 5 skipped.
- `cookr validate` passed on 2026-10-04; since folders became the only
  committed form it reports every doc missing (see **Open** above).
- adtoolkit (P8) was verified on a scratch copy: 387/387 convert and
  round-trip, compile under the cap, register beside the cookbook, and route
  correctly.
- All 15 findings from a whole-branch `/code-review max` of PR #64 are fixed
  with tests; the mapping is in a comment on PR #64.

## Not done — each needs Mike's explicit OK

- **skill-router CI** — the repo has no `.github/workflows/`, so its test
  suite runs on no push or PR. (Install is done: skill-router 0.2.0 is a uv
  tool installed editable from its main, and its `./install --dry-run` reports
  nothing to change for Claude and Codex.)
- **Registering adtoolkit** with the live skill-router registry.

## Done — adtoolkit recipe conformance (2026-10-04)

- adtoolkit main is 100% recipe conformant. The work landed as adtoolkit
  PR #13 (`95f9f187a`) and a follow-up (`661425b16`).
- On adtoolkit main, all three cookr gates pass:
  - `cookr coverage -p . --require complete`: 443 complete, 0 unmatched;
  - `cookr validate -p .`;
  - `cookr compile -p . --check`: 443 of 443 current.
- Every spec is a source folder. Fifteen record `names_hosts` reasons.
- Every known defect from the 2026-09-29 review is fixed. adtoolkit's
  `docs/project/cookbook-organization.md` maps each defect to its commits.
- This needed one cookr fix, PR #68: child specs grouped under a plain
  subdirectory of a parent's source folder stay in the corpus.
