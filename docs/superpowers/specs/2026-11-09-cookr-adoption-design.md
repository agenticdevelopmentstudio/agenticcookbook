# cookr adoption: recipes first, in every repo

- **Date:** 2026-11-09
- **Status:** draft for Mike's approval
- **Builds on:** `2026-10-05-cookbook-project-format.md` (its rdid names and project index,
  reworked here: identity stays the UUID and the rdid is a readable name kept in the index),
  `2026-09-21-cookr-design.md`

## Intent

Mike separates **multi-platform** (native code per platform, each using that platform's best
APIs and tools, built from one shared design) from **cross-platform** (a tool such as React
Native that compiles one codebase down to every platform). Cross-platform tools exist because
humans want to write code once. An agent can write native code for every platform, so the
result is better and cross-platform tooling stops being worth it.

The shared design is the **recipe**. When a feature is built on macOS and its
platform-agnostic recipe lives in the same repo's cookbook, the Windows port starts with a
spec and a reference implementation already in hand. As the Windows version is written, the
recipe is corrected, so over time each recipe has been proven on several platforms.

Until now work has been written for the platform in front of us (mostly macOS, web
frontends and backends) without that habit. This project changes the default: **in a repo
that opts in, recipes come first and stay current**, and tooling enforces it without
interrupting the work.

## Goals

1. A repo opts in with a small `.cookr.json` that says only what the cookbook can't: where the
   cookbook is, where the cookbooks it depends on are, which code folders need recipes, and the
   list of known gaps still to backfill.
2. Every reference (between artifacts, to other cookbooks, to reference implementations) is
   **by UUID**, resolved through the cookbook's index, which also holds each thing's readable
   rdid and current location. Renaming or moving anything changes one index entry and breaks
   nothing. This is the model the adhub backend already uses.
3. A recipe in one repo can depend on a recipe in another (an adkitchen recipe on an adhsdk
   recipe).
4. A global agent hook, active only in opted-in repos, **blocks** commits and turn ends that
   change covered code without its recipe, and tells the agent exactly which recipe to
   create or update. The agent does that and carries on; Mike isn't interrupted.
5. Backfill happens as we go: what we touch gets brought up to date (plus what it is directly
   built on), siblings only if Mike says so. cookr computes that list so the agent doesn't
   re-derive it.
6. Every format is versioned, and cookr upgrades an old-format cookbook the moment it meets
   one, in whatever repo we are working in.
7. adhsdk, adkitchen and the agenticcookbook are fully converted (see Rollout).
8. Every implementation has a **conformance state** against its recipe. A repo is fully
   conformant when every file in its roots is covered and every implementation is `confirmed`.
   That makes it safe to move recipes in fast and verify them later.
9. Every artifact is **versioned in source**: enhancing a recipe makes a new version, and every
   earlier version stays in the source folder. Agents get only the current version, compiled.
10. Every cookr repo's cookbook is **compiled into routed skills** and registered with
    skill-router, so "create an error alert" lands an agent on that repo's error-alert recipe
    with its platform's additions, and nothing else.

## Non-goals

- Folding recipes back into the agenticcookbook, or moving them into the adh backend
  database. That comes later.
- Backfilling everything at once. Gaps are tracked and closed when work touches them.
- The rest of the 2026-10-05 format change (single `artifact.md`, `platforms/`, `ai/`
  folders, removal of author/license fields). That stays its own project.
- Enforcing that a recipe's *prose* is accurate. A script can see that a recipe was touched,
  exists and resolves; it can't judge the content. Accuracy is the agent's job, guided by
  the plan step and the existing verify pass.
- Fetching cookbooks from URLs. A URL location is recorded; fetching it is later work.

## Anti-goals (failure even if it works)

- **Getting bogged down.** If recipe work routinely balloons a feature beyond what it touches,
  the design has failed. The minimum is mechanical and small; anything beyond it is Mike's
  explicit choice.
- **Stopping the work.** The hook must never need Mike to step in. Its message says what to
  do; the agent does it and continues.
- **The cookbook knowing about cookr.** A cookbook holds artifacts and its index (ids, names,
  where artifacts and their implementations are). Tool configuration lives in `.cookr.json`.
- **Names or paths as identity.** Links carry UUIDs. An rdid or a path appears as identity
  nowhere; it is a label or a location, held once in an index.
- **Silent debt.** A gap nobody fixes stays visible in `cookr status`, never forgotten.
- **A second router.** cookr compiles and registers skills; skill-router routes them. cookr
  never routes.

## Current state (found 2026-11-09)

- **Formats.** All 929 `artifact.json` files (486 here, 443 in adhsdk) carry `"format": 1`, and
  cookr refuses any other value (`core/artifact.py`). adhsdk's `cookbook.json` has
  `"schema_version": "1.0.0"` (a semver string); this repo's cookbook has no `cookbook.json`;
  `.cookr.json` has no version; adhsdk's legacy `recipes/*.md` have none.
- **Identity.** Each artifact has a UUID `id` that nothing links to, and a path-derived
  `domain` (`adhsdk://cookbook/ui/navigation/htdv`) that every link uses. A move changes the
  domain and breaks links; in adhsdk 16 of 139 `depends-on` and 15 of 625 `related` links
  already point at pre-move addresses (`adhsdk://recipes/button`), and 4 `related` entries are
  bare names (`site-wordmark`). adhsdk has 149 links into this repo. Recipes also cite
  compliance checks thousands of times
  (`agenticdevelopercookbook://compliance/best-practices#unit-test-coverage`: 886); checks
  are not artifacts and have no UUID.
- **adhsdk** is halfway through a migration: a legacy `.cookr.json` (54 roots, 47 ignores,
  aliases, renames; several roots name paths that have since moved, such as
  `packages/web/packages/ui` against today's `adh-ui`), a legacy flat `recipes/` folder (261
  files), and the converted `cookbook/` (443 artifacts, `cookbook.json` with a 107-entry
  `code` block). Implementations are listed per recipe in a `## Reference Implementations`
  table (595 rows).
- **adkitchen** (`apps/adkitchen`) has no cookbook and no `.cookr.json`. It has
  `.abstractr.json`, and adhsdk as a submodule at `external/adhsdk`.
- **agenticcookbook** (this repo): `cookbook/` with `agenticdevelopercookbook://` domains and
  no code to cover. `domain` and the UUID are required by the formatting compliance checks
  (`tbd/compliance/artifact-formatting/`), `guide/introduction/conventions.md`, the glossary,
  `references/*.schema.json`, the create-artifact, lint-artifact and repair-cookbook skills,
  `.claude/rules/`, and cookr's own scheme code (`twins.py`, `scheme.py`, `compliance.py`, the
  `source:` line in compiled skills). The website (adh monorepo) and the dev-team plugin may
  read them too.
- **Hooks:** abstractr's two hooks (`cc-abstractr-placement-hook.py` on Write/Edit,
  `cc-abstractr-commit-hook.py` on Bash) are the model to copy: exit 2 blocks with stderr
  fed to the agent, an in-command env var (`CC_ALLOW_ABSTRACTR=1`) is the user-only escape
  hatch, and output is capped so a big change doesn't flood context.

## Design

### 1. Identity: UUID, with the rdid as a name

- **The UUID is the identity**, for artifacts and for cookbooks. Artifacts keep the UUIDs they
  already have. Every link stores UUIDs.
- **The rdid is a readable name** (`adhsdk.recipe.ui.web-panel`), held in the index next to the
  UUID. It can be renamed at will (`cookr rename <uuid|rdid> <new-rdid>`): that rewrites one
  index entry and refreshes cached labels; no link changes.
- **A cookbook** has the same pair in `cookbook.json`: `id` (UUID) and `rdid` (`adhsdk`,
  `adkitchen`, `adc` for this repo). The cookbook's rdid is the first segment of its artifacts'
  rdids.
- **`domain` is removed** from every artifact, in every cookbook including this one.
- **People and agents write rdids; cookr stores UUIDs.** Wherever a link is authored
  (`depends-on`, `related`, an in-text link), an rdid is accepted and cookr rewrites it to the
  UUID when it writes the file. `cookr id <rdid|uuid>` looks one up in either direction.
  Compiled docs and skills show rdids.

Link forms:

| Where | Local | Foreign |
|---|---|---|
| `depends-on`, `related` | `"<artifact-uuid>"` | `"<cookbook-uuid>/<artifact-uuid>"` |
| In-text | `[<rdid>](cookbook:<artifact-uuid>)` | `[<rdid>](cookbook:<cookbook-uuid>/<artifact-uuid>)` |

The in-text label is a cached rdid for the reader; cookr refreshes it.

**Compliance checks get identity too.** Each named check (`best-practices#unit-test-coverage`)
becomes an index entry of kind `check` with its own UUID and rdid
(`adc.check.best-practices.unit-test-coverage`), so the thousands of citations become UUID
links like everything else.

### 2. The index

Each cookbook has `index.json`. It is edited only through cookr commands, never by hand:

- `rdid` and `path` are written by cookr from the folders and by `rename`;
- `implementations` are authored data (nothing else holds them), written with
  `cookr implements <id> <location> --platform <p>` and `cookr implements --remove <id>
  <location>`, rewritten by `relink` and the upgrader, and checked by `validate`;
- `foreign` caches the rdid of every foreign UUID this cookbook links to.

```json
{
  "format": 2,
  "cookbook": {"id": "5b1e…", "rdid": "adkitchen"},
  "entries": {
    "c41a4778-…": {
      "kind": "recipe",
      "rdid": "adkitchen.recipe.app.project-window",
      "path": "app/project-window",
      "implementations": [
        {"platform": "macos", "location": "App/Sources/ProjectWindow/",
         "conformance": {"state": "confirmed", "version": "1.4.0", "hash": "sha256:9f2c…"}},
        {"platform": "macos", "location": "App/Sources/ProjectWindow/ProjectWindowController.swift",
         "conformance": {"state": "unverified"}}
      ]
    }
  },
  "foreign": {
    "9d02…/17d2fa7e-…": "adhsdk.recipe.ui.web-panel"
  }
}
```

- `path` is the artifact folder relative to the cookbook. A `check` entry's `path` names its
  compliance file and check name.
- `implementations` replaces the `## Reference Implementations` table. Each `location` is a
  repo-relative path (a trailing `/` claims a directory; a file row beats a directory row and
  the deepest directory wins, as today). A location may also be a URL, which cookr records
  and reports but doesn't check against the filesystem.
- **The index is the only place a path appears.** The compiled doc and compiled skill render a
  Reference Implementations section *from* the index, so agents still read one.
- The index belongs to the cookbook: it is the cookbook's own table of contents, not cookr
  configuration.

Moves are absorbed in one place: `cookr relink` (extended) reads git's renames and rewrites
the index's `location`s; moving an artifact folder rewrites its `path`. No artifact file
changes.

### 3. Cross-cookbook references

A foreign link names the cookbook's UUID and the artifact's UUID, so cookr knows which index
to read and never searches. The cookbook's location comes from:

1. The repo's `.cookr.json` `dependencies` entry for that cookbook UUID, when its location is a
   path relative to the repo that exists. A submodule is the normal case (adkitchen's
   `external/adhsdk/cookbook`): it is the version the repo builds against, so links are checked
   against that version.
2. Otherwise `~/.cookr/locations.json`, per machine and never committed, keyed by cookbook UUID.
   This covers a cookbook that isn't a submodule and sits in a different place on each machine.
3. A URL location is recorded but not fetched: the cookbook counts as unreachable unless
   `locations.json` names a local copy.

**Cached rdids refresh themselves.** Whenever cookr reads a target index (`validate`, `scope`,
`update`, `check`) it compares the cached rdids (the dependency's rdid in `.cookr.json`, the
`foreign` labels in the index, in-text labels) with the target's current ones. `update` and
`relink` rewrite stale labels; `validate` reports a stale label as a warning, since the UUID
still resolves. A UUID missing from a reachable cookbook is an error; an unreachable cookbook is
a warning, so being offline or lacking a checkout doesn't fail every check.

### 4. `.cookr.json`

Committed at the repo root. Its presence opts the repo in. It holds only what the cookbook
doesn't:

```json
{
  "format": 2,
  "cookbook": "cookbook",
  "dependencies": {
    "9d02…": {"rdid": "adhsdk", "location": "external/adhsdk/cookbook"},
    "e7a4…": {"rdid": "adc"}
  },
  "roots": [
    {"path": "App/Sources", "platform": "macos", "kind": "ui", "group": "app"},
    {"path": "App/Core", "platform": "macos", "kind": "logic", "group": "core"}
  ],
  "ignore": ["**/Generated/**", "**/*Tests*/**"]
}
```

- `dependencies` is keyed by cookbook UUID; `rdid` is a cached label; `location` is optional
  (absent means "look in `locations.json`").
- `roots` are the folders where **every file must be covered** by some artifact's
  implementations. `platform` and `kind` (ui or logic) feed `prompt extract`. Platforms become
  finer-grained for multi-platform work: `macos`, `ios`, `web`, `android`, `windows`, `linux`,
  `python`, and `apple` kept for code shared across Apple platforms (adhsdk's `Shared/`
  folders). The upgrader rewrites `apple` to `macos` or `ios` where a root's path says which
  (`SourcesUI/macOS/…`) and leaves it otherwise. `group` is the cookbook folder that root's
  recipes belong in, used by `arrangement`. (These move here from `cookbook.json`'s `code`
  block, which is removed.)
- `ignore` is root-relative or repo-relative globs excluded from coverage. A root may carry its
  own `ignore`, as today.
- `aliases` and `renames` in the legacy file are dropped: UUIDs make aliases unnecessary, and
  the index replaces renames.

**The "not done" list is computed, not kept.** Mike asked for a list of exceptions to whittle
down. Both halves of it are facts cookr can work out, so neither is stored by hand: code with
no recipe is what `coverage` finds in the roots, and recipes not yet checked against their code
are the implementations not `confirmed` (§9). `cookr status` prints that list, grouped by root
and by state, and says "fully conformant" when it is empty. A hand-kept list would drift from
both the code and the index.

**The list exempts nothing that is touched.** It lets `validate` and `coverage` pass during the
transition (gaps are reported, not failed) and keeps the debt visible. When work touches an
uncovered file or an implementation that isn't `confirmed`, the hook still requires the recipe
work (§7).

### 5. Formats and upgrade on contact

- **Every format carries a whole-number `format`:** `artifact.json`, `cookbook.json`,
  `index.json`, `.cookr.json`. This project moves all four to `2`. adhsdk's
  `"schema_version": "1.0.0"` becomes `"format"`.
- **cookr upgrades on contact.** Any cookr command, including `cookr check` run by the hook,
  that meets an older format in the repo it is working in upgrades that whole cookbook in
  place before doing anything else, then reports what changed so the agent commits the upgrade
  as its own commit ahead of the feature work. It upgrades per cookbook, never per artifact,
  because rewriting links needs the complete index.
- **The upgrader** (also runnable directly as `cookr upgrade`):
  - writes `cookbook.json` format 2 with a new cookbook UUID and its rdid (from the domain
    scheme: `adhsdk`, `agenticdevelopercookbook` → `adc`);
  - writes `index.json`: each artifact's existing UUID, an rdid derived from its domain path
    (`adhsdk://cookbook/adh/hub/teams` → `adhsdk.recipe.adh.hub.teams`, type from the
    artifact), its path, and its implementations (from the Reference Implementations table,
    which is then deleted); a `check` entry for every named compliance check;
  - rewrites every `depends-on`, `related` and in-text `scheme://…` link to UUID form,
    resolving current domains directly and pre-move domains through the legacy `renames` and
    `aliases`; a link it can't resolve is listed in its report and left as a `NEEDS REVIEW`
    marker, never guessed;
  - turns a legacy `.cookr.json` or a `cookbook.json` `code` block into a format-2
    `.cookr.json`, dropping roots whose paths no longer exist (listed in its report);
  - marks every existing implementation `unverified` (none were maintained against current
    code) and moves every artifact's Change History into `versions/` form (§10);
  - removes `domain` and sets `"format": 2` on every artifact;
  - is idempotent and refuses a dirty work tree.
- Old formats are read **only** by the upgrader; every other cookr path reads format 2.
- Links into a cookbook that hasn't been upgraded yet are resolved by deriving that cookbook's
  index in memory with the same rules, so cookbooks can be upgraded in any order.

### 6. Scope: the minimum and the siblings

New command `cookr scope [paths | ids…] [--since <ref>] [--json]`. Given planned or changed
files (default: the branch diff from its merge-base plus the working tree), it outputs:

- **minimum**: each artifact covering a touched file, plus its **direct** recipe and ingredient
  dependencies (across cookbooks), each with its conformance state (§9), or `missing` (touched
  file uncovered, or a dependency that should exist and doesn't), or `unresolvable` (a malformed
  link), or `unreachable` (a dependency in a cookbook that can't be reached, §3). Anything
  in the minimum that isn't `confirmed` is required work: it gets brought up to date and
  confirmed. That is Mike's Safari example: the panel and the abstraction it is built on.
- **further up** (informational): dependencies beyond the first level. Listed so Mike can pull
  any of them in; never required, so one edit can't drag in a whole tree.
- **siblings**: recipes and ingredients that aren't in the minimum but share a direct recipe or
  ingredient dependency with one that is (the Chrome web panel beside the Safari web panel,
  both depending on the web panel abstraction).
- The walk follows only recipes and ingredients. Guidelines, principles and checks in
  `depends-on` are the rules the code follows, not code it is built on: they are never in the
  minimum and never make siblings. (In adhsdk, `retry-and-resilience` alone has 15 dependents;
  counting it would list 15 siblings for one networking edit.)

The agent runs it during planning and tells Mike, before any code: "Minimum recipe work:
… Siblings: … Update any of those?" Mike's answer goes into the plan. A sibling Mike declines
keeps whatever conformance state it has; if it isn't `confirmed` it is already on the
`cookr status` list.

### 7. The hook

`cc-cookr-hook.py`, source in this repo at `skills/cookr/hooks/`, installed globally by
`skills/cookr/setup/install` (which registers it in `~/.claude/settings.json`, as abstractr's
install does). One script, three events:

- **SessionStart / UserPromptSubmit** (first prompt only per session) in a repo with
  `.cookr.json`: injects a short reminder that the repo is recipes-first, naming
  `cookr scope` and the procedure in the cookr skill. In a repo without one, it does nothing.
- **PreToolUse:Bash** on `git commit`: checks the staged set.
- **Stop**: checks the branch diff plus the working tree.

The check (`cookr check --hook`, a deterministic cookr command the hook shells out to so the
logic lives in cookr and is testable). It first upgrades an old-format cookbook (§5) and
blocks with "commit the cookr upgrade first" if it did. Then:

- For each changed file inside a root and not ignored:
  - **pure rename or move** (git reports it as a 100% similar rename) whose index `location` was
    updated in the same set → nothing; that is what `relink` absorbs;
  - **added or modified**, covered by artifact X, and nothing in X's folder changed in the
    same set → **"update X"**. An `implementations` change in the index alone does not count:
    new or changed code means the recipe's content is checked against it;
  - **added or modified**, covered by nothing → **"create a recipe covering this file"** (or
    claim it into an existing recipe with `cookr implements` and update that recipe);
  - **deleted**, covered by X → **"update X"** (its index row is removed and its content checked);
    **deleted** and covered by nothing → nothing.
- For each implementation whose code changed (or that the change claims), its conformance
  must end the set `confirmed` at the recipe's current version → otherwise **"validate X
  against <version>"**, with the requirement diff from the version it was confirmed at (§10)
  when there is one. This is what makes an implementation behind on a **minor or major**
  version block when touched; behind only on a patch, it is still `confirmed`. Implementations
  nobody touched never block.
- For each changed artifact, every `depends-on` UUID must resolve → otherwise **"create or fix
  dependency Y"**.
- For each artifact whose content changed on the branch, its version must have moved past the
  version on the base → otherwise **"bump X"** (§10).

Any finding blocks (exit 2) with one message listing what to do by rdid, capped at 15 entries
plus a count. It never asks the agent to stop or check in with Mike. Escape hatch:
`CC_ALLOW_COOKR=1` in the command itself, for Mike's use only.

The hook doesn't run cross-repo: adhsdk code edited in an adhsdk worktree is checked by the
same hook in that worktree.

### 8. Agent procedure

The cookr skill gains a **Working in a cookr repo** section:

1. During planning, run `cookr scope` on the planned files and give Mike the minimum and the
   siblings; record his answer in the plan.
2. Write or update the recipes in the worktree **before** the code, as the shared design.
3. Keep them updated as the code changes; a missing recipe is written with the existing
   `prompt extract` brief and verify pass.
4. When an implementation matches its recipe, `cookr confirm` it.
5. `cookr bump` each recipe it changed, then `cookr validate` before the work is done.

### 9. Conformance

The existing `status` field (wip, draft, review, accepted, deprecated) is the recipe's
**authoring** lifecycle: is the spec itself finished. Conformance is a separate axis: **does
this code match this spec**. It is per implementation, because the macOS code can match the
error-alert recipe while the Windows code doesn't, and it lives on the implementation row in
the index (§2), not in the recipe.

| State | Meaning |
|---|---|
| `planned` | the recipe names a platform with no code yet: the port to come |
| `unverified` | code and recipe exist; nobody has checked one against the other |
| `needs-validation` | was confirmed, and since then the code changed or the recipe gained a minor or major version |
| `confirmed` | checked: the code meets the recipe at the recorded `version` |

- **`cookr confirm <id|rdid> [--platform p] [--location l]`** records `confirmed` with the
  recipe's current `version` and a hash of the implementation's files. The agent runs it after
  checking the code against the recipe (the existing verify pass, or by reading both).
- **Drift is automatic.** cookr recomputes the hash on read: a different hash means the code
  changed, and the state reads `needs-validation`. A recipe bump past the confirmed version
  does the same unless it was a patch. Nobody has to remember to downgrade a state.
- **A recipe's overall state** is its weakest implementation's. A repo is **fully
  conformant** when every file in its roots is covered and every implementation is
  `confirmed`; `cookr status` says which it is.
- New code written with its recipe in the same change is `confirm`ed as part of that change.
- Moving recipes in fast is cheap: they arrive `unverified`, which costs nothing until the code
  is touched.

### 10. Versions

- **Semver means something for a recipe.** `patch`: wording only, no behavior change. `minor`:
  a requirement added. `major`: a requirement changed or removed. (Ingredients, guidelines and
  principles use the same rule for their requirements.)
- **One bump per change.** All edits to an artifact on a branch are one new version, set by
  `cookr bump`. cookr proposes the level from what changed in the Requirements section (an
  added named requirement → minor; a changed or removed one → major; otherwise patch) and the
  agent or Mike can override it. The hook requires the bump (§7). A version is immutable once
  on main, as today.
- **Every version stays in source.** The source folder is the current version. Bumping freezes
  the previous version's parts into the folder's `versions/<semver>/`, byte for byte, with its
  own `artifact.json`. Change History rows stay as they are. The upgrader starts each artifact's
  `versions/` empty: earlier versions are only in git history and aren't reconstructed.
- **Compiled output is the current version only.** Docs, skills and the always-on principles
  never include `versions/`.
- **The point of keeping them:** `cookr diff <id> <from> [<to>]` prints the requirement-level
  difference between two versions. The hook (§7) and `cookr scope` hand it to the agent
  validating an implementation confirmed at 1.2 against a recipe now at 1.4, so the agent reads
  two added requirements, not the whole recipe. A port starts from the current version and bumps
  it if the port changes the spec; the other platforms then show `needs-validation` until
  someone checks them, which is the to-do list a spec change creates.
- **References are unpinned.** `depends-on` and `related` mean the current version of the
  target. Version pinning lives only in conformance.

### 11. Skills

Every cookbook artifact already compiles to a routed skill (`cookr compile --target skill`)
and `cookr install` registers adc's set with skill-router, which suggests routes from the
prompt. This project extends that to every cookr repo instead of building a second router:

- **A set per cookbook.** Each cookbook (adhsdk, adkitchen) compiles to its own set in
  `$COOKR_HOME/sets/<cookbook-rdid>` and registers with skill-router as source
  `<cookbook-rdid>`.
- **Compiled on contact.** The hook's session-start step runs `compile --target skill --check`
  for the repo's cookbook and its dependencies and recompiles and re-registers a stale set
  before the first prompt, the same way formats upgrade on contact.
- **Scoped to the repo.** A repo's recipes route only in that repo and in repos that depend on
  its cookbook: adkitchen's recipes never appear in an unrelated repo; adhsdk's appear in
  adhsdk and adkitchen. skill-router already has a per-repo root route and `.skill-router.json`
  (`root`, `hide`, `enforcement`); the set registers under its repo's root and other repos hide
  it. Where skill-router can't yet express this, the builder extends skill-router.
- **Platform from the repo.** The skill an agent reaches is the shared recipe plus that
  platform's additions, compiled into one file; the platform comes from the `.cookr.json` root
  the work is in, so in a macOS root the route goes straight to the macOS skill.
- **Minimal content.** The type's skill template keeps only what the agent acts on
  (requirements, states, test vectors, the Reference Implementations rendered from the index,
  dependencies by rdid); rationale, history and `versions/` stay in source.

So "create an error alert for this condition" in adkitchen gives the prompt hint
`adkitchen…/macos`, the agent routes to `error-alert`, reads one skill and builds from it.

### 12. Rollout

1. **cookr**: UUID links and rdid names, `index.json`, cookbook identity, foreign resolution
   and label refresh, format 2 everywhere, the upgrader and upgrade on contact, `.cookr.json`
   format 2, `scope`, `check`, `status`, `id`, `rename`, `implements`, `confirm`, `diff`;
   conformance and its drift detection; `versions/` and level-proposing `bump`; `relink`,
   `compile`, `validate`, `coverage`, `arrangement`, `prompt extract` and `bump` moved onto the
   index; per-cookbook skill sets, compile on contact and repo scoping (with any skill-router
   change that needs); the hook; skill and install changes; tests.
2. **agenticcookbook** (`adc`): `cookr upgrade` on `cookbook/`; then convert everything that
   reads `domain` or the UUID to the new model: the formatting compliance checks,
   `conventions.md`, the glossary, `references/*.schema.json` (plus new schemas for
   `index.json`, `cookbook.json` and `.cookr.json` format 2), the create-artifact,
   lint-artifact and repair-cookbook skills, `.claude/rules/`, `.claude/CLAUDE.md`, and cookr's
   scheme code. Check the adh website and the dev-team plugin for readers of `domain` and
   convert those too. No roots, so no `.cookr.json`.
3. **adhsdk**: `cookr upgrade`; the legacy `.cookr.json` becomes format 2; then move the legacy
   `recipes/` folder in. 256 of its 261 files have no counterpart in `cookbook/` (by UUID or
   name); 183 name code that still exists, 72 name no code, 1 names only code that's gone. Each
   is converted to a source folder in its concept group (`cookr organize`'s placement), keeps its
   UUID, gets an rdid, has its paths turned into index implementations (missing paths reported,
   not kept), and is `unverified`. The 5 with a counterpart are compared with it and the legacy
   file is deleted. `recipes/` is then removed. No recipe is rewritten during the move; each is
   brought up to date when work touches its code.
4. **adkitchen**: `cookr create` its cookbook (rdid `adkitchen`) and a `.cookr.json` whose roots
   are its app source folders, with adhsdk as a dependency through `external/adhsdk/cookbook`;
   everything starts uncovered and shows in `cookr status`.
5. Every other repo is upgraded on contact, or opts in with `cookr adopt`, which writes a
   `.cookr.json`.

## Left to the builder

- Exact JSON schemas.
- How `check` decides "a file in X's folder changed" for staged vs branch sets, as long as both
  match the rules above.
- Output formats of `scope`, `check`, `status` and the upgrader's report beyond the fields
  named.
- Which adkitchen folders are roots (read the app's layout and `.abstractr.json`).

## My calls (Claude's, not Mike's; check these)

- Only the rdid naming and the index idea come from the 2026-10-05 draft; the rest of its
  format change stays out.
- Implementations live in the cookbook's index rather than in each recipe; compiled forms
  render them back. `index.json` is edited only through cookr commands; `cookr implements`
  writes implementation rows. An index-only change never satisfies "update X", except for a
  pure rename.
- Link forms: bare artifact UUID locally, `<cookbook-uuid>/<artifact-uuid>` across cookbooks,
  in-text as a markdown link with an rdid label and a `cookbook:` target.
- Compliance checks become `check` entries with UUIDs.
- A committed in-repo dependency location (the submodule) wins; `~/.cookr/locations.json` is
  the fallback. URLs aren't fetched.
- The upgrade happens per cookbook, is committed on its own ahead of feature work, and leaves
  unresolvable links as `NEEDS REVIEW` markers rather than guessing.
- No hand-kept "not done" list in `.cookr.json`: uncovered code and unconfirmed
  implementations are computed and shown by `cookr status`. Nothing on that list is exempt
  once touched. Existing implementations start `unverified`.
- Conformance is per implementation, stored in the index with the confirmed version and a code
  hash; drift flips it to `needs-validation` automatically.
- Behind on a minor or a major version blocks when that code is touched; a patch never does;
  untouched code never blocks.
- Semver levels are defined by requirement changes and proposed by `bump`; every prior version
  is kept in `versions/`; references are unpinned.
- skill-router stays the only router; each cookbook gets its own set, compiled on contact and
  scoped to its repo and its dependents.
- All 256 unmatched legacy adhsdk recipes move in as-is, `unverified`.
- `scope`'s minimum is touched artifacts plus their direct recipe/ingredient dependencies;
  deeper levels are listed but not required; guidelines, principles and checks are never
  walked.
- Platforms split into `macos`/`ios`/…, with `apple` kept for shared Apple code.
- The hook fires on commit and on Stop, not on every edit; the session reminder fires once.
- Claude Code is the only host the hook targets now; the script parses the payload the way
  abstractr's `hook_payload.py` does so another host can be added later.
