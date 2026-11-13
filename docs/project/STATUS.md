# Status — compiled artifacts and routed skills

*Updated:* 2026-11-13. *Derives from:* `226f310` (PR #64, agenticcookbook),
`2ac4109` (PR #2, skill-router), PR #66 (`revise-corpus-conformance`),
PR #72 (`dd2e4670`, `44c510bf`), PR #74 (`689ab01`, `e75c550`), PR #78
(`48d460aa`, `40c02a7f`, `63522f3f`), `52df843b` (cookr 0.13.1), and
skill-router `a7a9177` (0.6.0), `262439a` (0.7.0), `cb1207a`.

Read this first to resume the work. The design lives in the
[plan](../superpowers/plans/2026-10-03-compiled-artifacts-and-skills.md) and the
[source folder spec](../superpowers/specs/2026-10-03-artifact-source-folder.md);
format 2 and recipes-first adoption live in the
[adoption design](../superpowers/specs/2026-11-09-cookr-adoption-design.md) and its
[plan](../superpowers/plans/2026-11-09-cookr-adoption.md).

## Concise compiled skills and the recompile (PR #78, 2026-11-13)

PR #78 landed as three commits on main:

- `48d460aa` repaired 23 artifact summaries that a line wrap had cut off.
- `40c02a7f`, cookr skill 0.13.0: compiled skills follow **progressive
  disclosure**. SKILL.md keeps what doing the task needs (rules, edge cases,
  accessibility). Each type template's `refer` list moves rationale into
  `<name>/references/<file>.md`, and SKILL.md ends with a `## More` list that
  links each file with a line saying when to read it. History is dropped.
  Skills carry the artifact's platforms as `metadata.platforms`, and
  descriptions lose their bold markers. A `cookr skills build` command that
  generated rule-skill plugins was built and dropped before merge, because
  skill-router already routes skills. The unused `cookr/core/rules.py` and its
  test were deleted.
- `63522f3f`: `cookbook/index/triggers.yaml` is deterministic, so it is now
  committed instead of gitignored. Without it on a fresh checkout, `cookr
  validate` failed.

skill-router, on its main: 0.6.0 (`a7a9177`) filters routes on
`metadata.platforms`. 0.7.0 (`262439a`) serves a skill's `references/` beside
its SKILL.md. `cb1207a` fixed the frontmatter parser so a nested mapping is
read as a mapping, which lets a malformed `platforms` be rejected (259 tests
pass). `./install` put 0.7.0 and its hooks in place for Claude and Codex.

`52df843b`, cookr 0.13.1: an explicit `--library cookbook` is honoured. The
argument parser had turned the literal `cookbook` into None, so `cookr
install` fell back to the cookbook's rdid (`adc`), and the unprefixed set
could not be rebuilt. The CLI still reports `cookr 0.10.0`, its own version.

**Recompiled and registered on 2026-11-13** (cookr installed from `52df843b`):

| Set | Skills | With references | Median lines | Max | Over 500 |
|---|---|---|---|---|---|
| `adc` (scoped to adhsdk) | 486 | 98 | 51 | 255 | 0 |
| `cookbook` (unprefixed, global) | 486 | 98 | 51 | 255 | 0 |
| `adhsdk` | 699 | 699 | 139 | 856 | 12 |

`adc` and `cookbook` are the same 486 artifacts twice, once prefixed and
scoped to adhsdk and once unprefixed and routed everywhere.

**Skills over 500 lines.** Compiling only warns about them (`LINES_MAX` in
`cookr/core/skill.py`). On 2026-11-13 the 12 routed ones were all adhsdk
artifacts, and their length is core content rather than rationale: Behavioral
Requirements of 340 to 520 lines, plus a 421-line Overview in
hierarchical-topic-detail (856). Shrinking them means splitting those adhsdk
artifacts, not changing the compiler. Nine skills installed directly in
`~/.claude/skills` are also over 500 lines (slack-bot, humanize, webinitor,
feishu-lark, ship, discord-bot, telegram-bot, release, extract-to-new-repo),
plus three in `~/.codex/skills`. None of them comes from a cookbook.

## Format 2 and recipes-first adoption (PR #74, 2026-11-10)

Landed on main as `689ab01` (the feature) and `e75c550` (`__pycache__/` ignored).

- **Identity is a UUID.** `cookbook/index.json` (`format`, `cookbook`, `catalog`,
  `entries`, `foreign`) maps each artifact UUID to its rdid
  (`adc.guideline.testing.test-pyramid`) and folder path, maintained by
  `cookr update`. The `domain` field is gone.
- **Links store UUIDs**: `depends-on`, `related` and `ingredients` in meta
  (`<cookbook-uuid>/<uuid>` across cookbooks), `[rdid](cookbook:uuid)` in text.
  `cookr rename <uuid> <rdid>` and folder moves never break a link.
- **`.cookr.json` format 2** is the per-repo config (code roots, ignores,
  dependencies). `cookr upgrade` converts a format-1 cookbook in one pass, only
  when run explicitly (PR #76 removed the upgrade-on-contact; see below).
- **New commands:** `id`, `rename`, `implements`, `confirm`, `status`, `diff`,
  `scope`, `create`, `adopt`. `bump` proposes the level and freezes versions in
  `versions/`.
- **Recipes-first reminders:** a global hook reminds the agent once per
  session and, on a commit, passes on what `cookr check --hook` finds ("create a
  recipe covering ...") as advice. It never blocks (PR #76). Per-cookbook skill
  sets compile through `cookr skills sync` and are scoped per repo through
  skill-router (skill-router#4, per-entry repo scope).
- **adc is fully converted** and `cookr validate` is green on it: every meta and
  in-text link resolves and the index matches the folders. Validate and update
  now read folders, which closes the 2026-11-07 *Open* item.
- cookr unit suite: 1103 passed (`cd skills/cookr/cli && python3 -m pytest tests/unit -q`).

Peer repos shipped the same day: agenticdevteam#2 (dev-team readers on format 2,
`external/agenticcookbook` at `e75c550`), adhsdk#46 (adhsdk converted),
adkitchen#103 (cookr adopted; hook dry-run verified), adcookbookwebsite#21
(website readers).

**The hook incident, 2026-11-10 (PR #76).** The first global install of the hook
(09:46) upgraded format-1 cookbooks on contact and then blocked commits and turn
ends until the rewrite was committed; in adhsdk that was 7531 files. Two
adkitchen sessions committed the rewrites to get unblocked. The hook was
uninstalled from `~/.claude/settings.json` and `~/.claude/skills/cookr/hooks/`,
and both commits were reverted on `adkitchen/browser-plugins` and
`adkitchen/browser-additions` (adhsdk reverts plus submodule-pointer commits).
PR #76 makes the design what it was meant to be: the hook only reminds (exit 0
everywhere, no Stop entry, no `skills sync`, no writes), and only an explicit
`cookr upgrade` converts a cookbook. On Mike's OK the fixed cookr and hook were
installed the same day (see Installed, below).

**Closed 2026-11-13:** the installed skill sets and skill-router were
re-run since format 2 (see the recompile above).

pipeline#4 merged as `70e80366` (its subject on main reads `## Summary`: the PR
body was passed as the merge summary, and main refuses force-pushes, so it
stays) and teamtesting#19 as `0916aa5`, after Mike had the untracked
`pipeline/testing/` (bytecode caches, SQLite side files, never-committed
generated prompts) deleted.

## Where things stand

Every cookbook artifact (456 of them: 44 principles, 351 guideline files — 258
unique — 48 ingredients, 13 recipes) is a **source folder**
(`<name>/artifact.json` plus one `.md` per section). Since `971a6490` the
folder is the only committed form; no compiled `<name>.md` sits beside it, and
readers that want a doc compile one (./install compiles cookr's references).

**Closed by PR #74:** cookr's `validate` and `update` read folders now (on
2026-11-07 they still read docs).

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
  These came from an earlier `skill-based-cookbook` branch; the corpus was
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

- **2026-11-10, on Mike's OK:** `skills/cookr/setup/install` from main
  (`06f3926`). It reinstalled `~/.local/bin/cookr` with the PR #76 fix (a
  format-1 repo gets a stderr notice and is never converted),
  `~/.claude/skills/cookr/` (SKILL.md and the hook), and registered the
  remind-only hook for SessionStart, UserPromptSubmit and PreToolUse:Bash, with
  no Stop entry. A smoke test on a scratch format-1 repo: `cookr validate` and
  `status` printed the notice and changed nothing; the hook exited 0 and wrote
  nothing to the repo.

- `./install --cli-only` of cookr: `~/.local/bin/cookr`. Its references are
  compiled from the source folders.
- The routed sets `adc`, `adhsdk` and `cookbook` (`~/.cookr/sets/<library>`)
  were recompiled on 2026-11-13 and registered with skill-router 0.7.0 for
  Claude and Codex. The `cookbook` set needs `--library cookbook`, because this
  cookbook's rdid is `adc`. The receipt is `~/.cookr/install.json`.
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
  worktree's edits. After artifact changes merge, re-run
  `cookr install --library cookbook --target routed --replace <main>/cookbook`
  and the same without `--library` for `adc`.

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
