> [!WARNING]
> **ARCHIVED — HISTORICAL RECORD, NOT CURRENT.** Captured 2026-11-10. This document reflects a
> past state or decision and may no longer describe how things work. Do not treat it as live
> documentation.

# cookr adoption Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Move every cookbook to UUID identity with an rdid index, per-implementation conformance, in-source versions and per-repo routed skills, enforced in opted-in repos by a cookr hook; then convert adc, adhsdk and adkitchen.

**Architecture:** New pure modules in `cookr/core/` (identity, index, links, repo config, conformance, versions, scope, hook check, upgrade) underneath the existing commands; the existing commands move from `domain` and `## Reference Implementations` onto the index. Old formats are read only by the upgrader, which every cookr command runs on contact. skill-router gains per-entry repo scopes; cookr registers each cookbook's set under them.

**Tech Stack:** Python 3.11 stdlib, pytest, rich (already used), git CLI.

**Spec:** `docs/superpowers/specs/2026-11-09-cookr-adoption-design.md` (read it before any task; section numbers below are its §s)

## Global Constraints

- Every format carries a whole-number `"format": 2`: `artifact.json`, `cookbook.json`, `index.json`, `.cookr.json`. Only `cookr/core/upgrade.py` reads format 1 or legacy files.
- Identity is the UUID. No `domain` field anywhere after this work. rdids are labels, held only in `index.json` (and cached labels).
- rdid grammar: `^[a-z][a-z0-9-]*(\.[a-z0-9][a-z0-9-]*)+$`. Artifact rdid = `<cookbook-rdid>.<type>.<folder path below the cookbook, type dir stripped, "/"→".">`. Check rdid = `<cookbook-rdid>.check.<document path "/"→".">.<check name>`.
- Link forms: local `"<artifact-uuid>"`; foreign `"<cookbook-uuid>/<artifact-uuid>"`; in-text `[<rdid>](cookbook:<uuid>)` or `[<rdid>](cookbook:<cookbook-uuid>/<uuid>)`.
- Conformance states exactly: `planned`, `unverified`, `needs-validation`, `confirmed`.
- Platforms: `macos`, `ios`, `apple`, `web`, `android`, `windows`, `linux`, `python`.
- Hook escape hatch: `CC_ALLOW_COOKR=1` inside the command; findings capped at 15 plus "… and N more"; exit 2 blocks.
- Scripts are Python. No new runtime dependencies. `index.json` is written only by cookr.
- Every task runs the unit suite: `cd skills/cookr/cli && python3 -m pytest tests/unit -q` — the 4 `tests/functional` failures that exist today (installed-shim environment) are not regressions.
- Commit and push after each task (`git push`), stage only the task's files. Commit messages end with `Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`.

## Review Focus

1. **A repo mid-edit when the upgrade fires** — dirty work tree: the upgrade must refuse with the exact list of dirty paths and never half-write; the command that triggered it exits non-zero with "commit or stash, then rerun". Test in Task 6.
2. **An offline or missing dependency cookbook** — foreign links resolve to `unreachable` (warning), never a crash or an error that fails every command. Test in Task 2.
3. **Paths with spaces, renames across roots and deleted directories in the hook's change set** — `git diff --name-status -z` parsing; a rename out of a root counts as a delete there and an add elsewhere. Test in Task 11.
4. **An rdid collision** (two folders deriving the same rdid, or `rename` onto an existing rdid) — refused with both paths named. Test in Task 1 and Task 7.
5. **A hook payload that isn't a commit or has no `.cookr.json` up the tree** — exit 0 silently and fast (no cookr import cost beyond the config probe). Test in Task 12.

---

## Phase 1 — cookr core model

### Task 1: Identity, cookbook manifest and index

**Files:**
- Create: `skills/cookr/cli/cookr/core/identity.py`, `skills/cookr/cli/cookr/core/index.py`
- Test: `skills/cookr/cli/tests/unit/test_identity.py`, `skills/cookr/cli/tests/unit/test_index.py`

**Interfaces:**
- Produces (`identity.py`):
  - `RDID_RE: re.Pattern`; `is_rdid(s: str) -> bool`; `is_uuid(s: str) -> bool`
  - `TYPE_DIRS = {"principles": "principle", "guidelines": "guideline", "ingredients": "ingredient", "recipes": "recipe"}`
  - `artifact_rdid(cookbook_rdid: str, type_: str, rel: str) -> str` — `rel` is the folder path below the cookbook (`guidelines/testing/test-pyramid`); a leading type dir is stripped.
  - `check_rdid(cookbook_rdid: str, document: str, name: str) -> str`
  - `check_uuid(cookbook_id: str, document: str, name: str) -> str` — `uuid5(UUID(cookbook_id), f"check:{document}#{name}")`, deterministic.
  - `@dataclass(frozen) CookbookIdentity(id: str, rdid: str)`; `read_manifest(cookbook_dir: Path) -> CookbookIdentity` (format 2 `cookbook.json`: `{"format": 2, "id", "rdid", ...other keys kept}`); `write_manifest(cookbook_dir: Path, identity: CookbookIdentity, extra: dict | None = None) -> None`. Raises `IdentityError(CookbookError)`.
- Produces (`index.py`):
  - `@dataclass Conformance(state: str, version: str | None = None, hash: str | None = None)`
  - `@dataclass Implementation(platform: str, location: str | None, conformance: Conformance)` — `location is None` only when `state == "planned"`.
  - `@dataclass Entry(id: str, kind: str, rdid: str, path: str, implementations: list[Implementation])` — `kind` ∈ principle/guideline/ingredient/recipe/check; a check's `path` is `<document>#<name>`.
  - `@dataclass Index(cookbook: CookbookIdentity, entries: dict[str, Entry], foreign: dict[str, str], catalog: str | None)` — `catalog` is the compliance catalog dir relative to the cookbook dir.
  - Methods: `get(key: str) -> Entry | None` (UUID or rdid); `by_path(path: str) -> Entry | None`; `owners(rel: str) -> list[tuple[Entry, Implementation]]` (file row beats directory row, deepest directory wins — today's `inventory.owners` rule).
  - `load_index(cookbook_dir: Path) -> Index`; `save_index(index: Index, cookbook_dir: Path) -> None` (sorted keys, 2-space indent, trailing newline, atomic replace).
  - `sync_from_folders(index: Index, cookbook_dir: Path) -> list[str]` — adds entries for new folders (UUID from `artifact.json` `meta.id`), rewrites `path` for moved folders (matched by UUID), drops entries whose folder is gone, keeps `rdid` of existing entries; returns change lines. Raises `IndexError_` (name it `IndexFileError`) on two entries with one rdid.
- Consumes: `cookr.core.artifact.find_folders`, `load_folder`; `cookr.core.errors.CookbookError`.

- [ ] **Step 1: Write failing tests**

```python
def test_artifact_rdid_strips_type_dir():
    assert artifact_rdid("adc", "guideline", "guidelines/testing/test-pyramid") == "adc.guideline.testing.test-pyramid"
    assert artifact_rdid("adhsdk", "recipe", "ui/navigation/htdv") == "adhsdk.recipe.ui.navigation.htdv"

def test_check_identity_is_deterministic():
    cid = "5b1e0000-0000-4000-8000-000000000000"
    assert check_uuid(cid, "best-practices", "unit-test-coverage") == check_uuid(cid, "best-practices", "unit-test-coverage")
    assert check_rdid("adc", "artifact-formatting/recipe-formatting", "has-frontmatter") == "adc.check.artifact-formatting.recipe-formatting.has-frontmatter"

def test_index_round_trip(tmp_path): ...            # save_index then load_index equals the original
def test_owners_file_beats_dir_deepest_dir_wins(): ...
def test_sync_adds_moves_drops(tmp_path): ...       # folder moved → path updated, rdid unchanged
def test_sync_refuses_rdid_collision(tmp_path): ... # message names both paths
def test_get_by_uuid_or_rdid(): ...
```

- [ ] **Step 2: Run, verify they fail** — `python3 -m pytest tests/unit/test_identity.py tests/unit/test_index.py -q` → import errors.
- [ ] **Step 3: Implement both modules** to the interfaces above.
- [ ] **Step 4: Run, verify pass**, plus the full unit suite.
- [ ] **Step 5: Commit** `feat(cookr): UUID identity, rdid names and the cookbook index`.

### Task 2: Links and foreign resolution

**Files:**
- Create: `skills/cookr/cli/cookr/core/links.py`
- Test: `skills/cookr/cli/tests/unit/test_links.py`

**Interfaces:**
- Produces:
  - `@dataclass(frozen) Link(cookbook: str | None, artifact: str)`; `parse_link(s: str) -> Link`; `format_link(link: Link) -> str`
  - `IN_TEXT = re.compile(r"\[([^\]]+)\]\(cookbook:([0-9a-f-]{36}(?:/[0-9a-f-]{36})?)\)")`
  - `in_text_links(text: str) -> list[tuple[str, Link]]` (label, link); `relabel(text: str, labels: dict[Link, str]) -> str`
  - `LOCATIONS = Path("~/.cookr/locations.json")` (overridable by `COOKR_HOME`); `read_locations() -> dict[str, dict]` (`{uuid: {"rdid", "path", "legacy_scheme"?}}`); `remember_location(identity: CookbookIdentity, path: Path, legacy_scheme: str | None) -> None`
  - `@dataclass Resolved(link: Link, state: str, rdid: str | None, entry: Entry | None)` — `state` ∈ `ok`, `missing` (cookbook reachable, UUID absent), `unreachable`.
  - `class Resolver(repo_root: Path, own: Index, dependencies: dict[str, Dependency])` with `resolve(link: Link) -> Resolved` and `index_for(cookbook_id: str) -> Index | None` (cached). Order: own index; `.cookr.json` dependency `location` relative to `repo_root` when it exists; `locations.json`; else unreachable. A dependency cookbook still on format 1 is read through `upgrade.derive_index` (Task 4) in memory.
  - `stale_labels(own: Index, resolver: Resolver) -> dict[str, tuple[str, str]]` — foreign key → (cached rdid, current rdid).
- Consumes: Task 1 `Index`, `Entry`, `load_index`; Task 3 `Dependency` (define `Dependency` here if Task 3 is not merged yet — it moves to `repoconfig.py` in Task 3 and is re-exported).

- [ ] **Step 1: Failing tests** — `test_parse_and_format_round_trip`, `test_in_text_links_and_relabel`, `test_resolve_local_ok_and_missing`, `test_resolve_dependency_by_relative_location`, `test_resolve_falls_back_to_locations_json` (with `COOKR_HOME` in `tmp_path`), `test_unreachable_cookbook_is_not_an_error`, `test_stale_label_detected`.
- [ ] **Step 2: Run, fail.** **Step 3: Implement.** **Step 4: Run, pass + suite.**
- [ ] **Step 5: Commit** `feat(cookr): UUID links and cross-cookbook resolution`.

### Task 3: `.cookr.json` format 2 as the repo config

**Files:**
- Create: `skills/cookr/cli/cookr/core/repoconfig.py`
- Modify: `skills/cookr/cli/cookr/core/config.py` (becomes a thin re-export of `repoconfig` names used elsewhere: `Config`, `Root`, `ConfigError`, `find_cookbook`, `load_config`, `COOKBOOK_DIR`, `MANIFEST`), `skills/cookr/cli/cookr/cli.py` (`_find`/`_context` read `.cookr.json` v2 and the cookbook it names; a cookbook with no `.cookr.json`, like adc's, gets `Config` with no roots), `skills/cookr/cli/cookr/core/roots.py` (drop its duplicate `MANIFEST`, import it)
- Test: `skills/cookr/cli/tests/unit/test_repoconfig.py`; update `tests/unit/test_config.py`

**Interfaces:**
- Produces:
  - `PLATFORMS = ("macos","ios","apple","web","android","windows","linux","python")`, `KINDS = ("ui","logic")`, `CONFIG_NAME = ".cookr.json"`
  - `@dataclass(frozen) Dependency(id: str, rdid: str, location: str | None)`
  - `@dataclass(frozen) Root(path: str, platform: str, kind: str = "ui", group: str = "", ignore: tuple = ())` — `group` replaces `recipes`; property `tier` (top segment of `group`).
  - `@dataclass(frozen) Config(repo_root: Path, cookbook_dir: Path, identity: CookbookIdentity, roots: list[Root], ignore: list[str], dependencies: dict[str, Dependency], config_file: Path | None)` with `root_for(rel) -> Root | None`, `is_group(tier) -> bool`, `tiers`. `domain()` and `scheme` are gone.
  - `load_repo_config(repo_root: Path) -> Config` (requires format 2; a format-1/legacy file raises `NeedsUpgrade(ConfigError)` carrying the path); `config_for_cookbook(cookbook_dir: Path) -> Config` (no `.cookr.json`); `find_repo(start: Path) -> Path | None` (walks up to the first dir holding `.cookr.json` or `cookbook/cookbook.json`).
  - `write_repo_config(config: Config) -> None` — key order `format, cookbook, dependencies, roots, ignore`.
- Consumes: Task 1 `read_manifest`.
- Callers updated to `group`: `core/inventory.py:expected_name`, `core/arrangement.py`.

- [ ] **Step 1: Failing tests** — `test_load_v2_config`, `test_unknown_platform_rejected`, `test_v1_cookbook_json_code_block_raises_needs_upgrade`, `test_legacy_cookr_json_raises_needs_upgrade`, `test_cookbook_without_repo_config_has_no_roots`, `test_write_round_trip`.
- [ ] **Step 2–4:** fail, implement, pass + suite (fixture-dependent tests that still read v1 are switched in Task 5; mark nothing skipped — if a test needs v2 fixtures, move it with Task 5's fixture conversion and say so in the commit).
- [ ] **Step 5: Commit** `feat(cookr): .cookr.json format 2 is the repo config`.

### Task 4: The upgrader

**Files:**
- Create: `skills/cookr/cli/cookr/core/upgrade.py`, `skills/cookr/cli/cookr/modules/upgrade.py`
- Create fixture: `skills/cookr/cli/tests/fixtures/v1-repo/` — a copy of today's `tests/fixtures/mini-repo` converted to source folders (`cookr convert`), unchanged otherwise; and keep `tests/fixtures/legacy-repo` as the `.cookr.json` + `recipes/` case.
- Test: `skills/cookr/cli/tests/unit/test_upgrade.py`

**Interfaces:**
- Produces:
  - `@dataclass UpgradeReport(cookbook_dir: Path, identity: CookbookIdentity, artifacts: int, links_rewritten: int, needs_review: list[str], dropped_roots: list[str], missing_paths: list[str], moved_legacy: int, files: list[Path])`
  - `needs_upgrade(repo_root: Path) -> list[Path]` — every cookbook dir under the repo (own cookbook only, not submodules) whose `cookbook.json`/`artifact.json`/`index.json`/`.cookr.json` is not format 2, or whose repo still has a legacy `.cookr.json` or `recipes/`.
  - `derive_index(cookbook_dir: Path) -> Index` — the in-memory index of a format-1 cookbook, same rules as the upgrade, no writes; raises `NeedsUpgrade` when the cookbook has no readable identity (no `cookbook.json` id).
  - `upgrade(repo_root: Path, *, rdid: str | None = None, dry_run: bool = False) -> list[UpgradeReport]` — refuses a dirty tree (`git status --porcelain` non-empty) with the dirty paths listed; idempotent (a format-2 repo returns `[]`).
- Behaviour (spec §5), in order:
  1. Cookbook identity: keep `cookbook.json` `id` when present, else `uuid4`; rdid from `--rdid`, else the domain scheme (`agenticdevelopercookbook` → `adc`, anything else as-is). Write format-2 `cookbook.json` (drop `schema_version`, `code`, `structure`; keep the rest).
  2. Legacy `recipes/` (adhsdk): each `.md` with no `cookbook/` counterpart by UUID or name is placed with `core/organize.plan`'s placement into a source folder in its group (`cookr convert` rules), keeps its UUID; a counterpart's legacy file is deleted after its `## Reference Implementations` rows are merged into the counterpart's index implementations. `recipes/` is removed.
  3. `index.json`: every artifact (UUID, `artifact_rdid`, path, implementations from its Reference Implementations table, which is deleted from the artifact; rows whose path is gone are dropped and listed in `missing_paths`; every implementation `unverified`); every compliance check as a `check` entry (`check_uuid`, `check_rdid`), with `catalog` set when the repo has a compliance catalog (adc: `tbd/compliance`, relative to the cookbook dir).
  4. Links: every `depends-on`/`related` value and every in-text `scheme://…` URI rewritten to UUID form. Resolution: own domains by path (domain path minus a leading cookbook-dir segment = index path); pre-move domains via the legacy `renames`/`aliases`; foreign schemes via `locations.json` `legacy_scheme`; `…/compliance/<doc>#<name>` to the check entry; bare names by unique folder basename. In-text replacements become `[<rdid>](cookbook:<uuid>)`. Unresolved → left in place, wrapped `NEEDS REVIEW: unresolved link <old>`, listed in `needs_review`. Foreign cookbooks referenced get a `.cookr.json` dependency (rdid, no location) and an `index.json` `foreign` label.
  5. Each artifact: drop `domain`, `"format": 2`, `versions/` not created.
  6. `.cookr.json` format 2 from the legacy file or the `cookbook.json` `code` block (`recipes` → `group`; roots whose paths are gone dropped → `dropped_roots`; `apple` → `macos`/`ios` when the root path contains a `macOS`/`iOS` segment, case-insensitive). No `.cookr.json` written when there were no roots (adc).
  7. `remember_location(identity, cookbook_dir, legacy_scheme)`.
- `cookr upgrade [--rdid R] [--dry-run] [--json]` prints the report.

- [ ] **Step 1: Failing tests** (against copies of `v1-repo` and `legacy-repo`, in a git-initialized tmp dir with everything committed):
  - `test_upgrade_writes_format_2_everywhere`
  - `test_upgrade_keeps_artifact_uuids_and_cookbook_id`
  - `test_upgrade_moves_reference_implementations_into_index_unverified`
  - `test_upgrade_rewrites_links_to_uuids` (a `depends-on` domain and an in-text URI)
  - `test_upgrade_marks_unresolvable_link_needs_review`
  - `test_upgrade_resolves_pre_move_domain_through_renames` (legacy-repo)
  - `test_upgrade_moves_legacy_recipes_into_cookbook` (legacy-repo: `recipes/` gone, folders exist, same UUIDs)
  - `test_upgrade_splits_apple_root_by_path`
  - `test_upgrade_refuses_dirty_tree` (message lists the dirty file)
  - `test_upgrade_is_idempotent`
  - `test_derive_index_matches_upgrade` (same UUID→rdid/path map as the real upgrade)
- [ ] **Step 2–4:** fail, implement, pass + suite.
- [ ] **Step 5: Commit** `feat(cookr): format-2 upgrader`.

### Task 5: Move cookr onto format 2

**Files:**
- Modify: `core/artifact.py` (`FORMAT = 2`; `load_folder` refuses 1 with "run cookr upgrade"; a `_load_any(folder)` used only by `upgrade.py`), `core/frontmatter.py` (drop `domain` from `REQUIRED_FIELDS` and `fill_defaults`), `core/artifact_types.py` (drop `domain` from `COMMON_FIELDS`), `core/checks.py` (remove `domain-matches-path` and `_Schemes`; links: every `depends-on`/`related`/in-text link must resolve via `Resolver` — `missing` is an issue, `unreachable` a warning; Reference Implementations checks move to index implementations: platform in `PLATFORMS`, location exists unless URL or `planned`), `core/completeness.py` (remove rule 15 and the `domain` param; rename `_unfenced` use to `unfenced`), `core/compliance.py` (citations are check links: `unknown_citations` resolves `cookbook:` links of kind `check`), `core/coverage.py`, `core/inventory.py`, `core/arrangement.py`, `core/relink.py` (all read implementations from `Index.owners`/`Entry.implementations`; `relink` rewrites index `location`s and moved folder `path`s, no bump — an index-only change is not a content change), `core/skill.py` (`metadata.source` = rdid; the compiled body renders a `## Reference Implementations` table and dependency rdids from the index; `cookbook:` links render as their rdid label), `core/artifact_build.py` (`compile_doc` renders Reference Implementations from the index the same way), `modules/prompt/prompt_cli.py` (rdid instead of domain; implementations from the index; the brief tells the writer to record rows with `cookr implements`), `modules/update.py` (no domain fill; runs `sync_from_folders` and `save_index`), `indexing/*` (generated `index.md` frontmatter loses `domain`), `core/organize.py` (its `plan` placement stays, reused by the upgrader; `apply` and the `organize` module are deleted — the upgrader replaces them), `core/scheme.py` (delete; move `repo_top` to `core/repo.py` if still used), `core/legacy.py` (only `upgrade.py` imports it), `core/refimpl.py` (keep `parse`/`implementations` for the upgrader; `render` reused by compile; delete `with_section`)
- Fix layering: `core/relink.py` and `core/organize.py` stop importing `cookr.modules.bump`; move `plan`, `bumped`, `BumpError`, `git_user` to `core/bumping.py` and have `modules/bump.py` use it.
- Fixtures: regenerate `tests/fixtures/mini-repo` as format 2 by running the Task 4 upgrader over `v1-repo` and committing the result; update `tests/fixtures/artifacts/folders/*` to format 2 without `domain`.
- Test: update every test that asserted domains or Reference Implementations tables; add `test_validate_reports_missing_link`, `test_validate_warns_unreachable_cookbook`, `test_compile_doc_renders_implementations_from_index`, `test_skill_metadata_source_is_rdid`, `test_relink_rewrites_index_locations_without_bump`, `test_load_folder_refuses_format_1`.

- [ ] **Step 1:** Make the fixture changes and the new failing tests.
- [ ] **Step 2:** Run the suite; record the failures.
- [ ] **Step 3:** Implement module by module; `grep -rn "domain\|scheme" cookr/` must leave only the upgrader, `links.py` (`legacy_scheme`) and comments that describe the old format for the upgrader.
- [ ] **Step 4:** Full unit suite green.
- [ ] **Step 5: Commit** `refactor(cookr): artifacts, checks, coverage and compile read format 2 and the index`.

### Task 6: Upgrade on contact

**Files:**
- Modify: `skills/cookr/cli/cookr/cli.py` (`_context` runs `upgrade.needs_upgrade` on the repo it found; non-empty → run `upgrade.upgrade`, print the report, exit 3 with "cookr upgraded <cookbook>: commit the upgrade on its own (`git add -A <cookbook> .cookr.json && git commit -m 'chore: cookr format 2 upgrade'`), then rerun"; the `upgrade` module itself and `--help`/`--version` skip this), `context.py` (carry `repo_root`)
- Test: `skills/cookr/cli/tests/unit/test_upgrade_on_contact.py`

**Interfaces:** Consumes Task 4 `needs_upgrade`, `upgrade`. Exit code `3` = "upgraded, commit and rerun" (distinct from 1 failure / 2 usage).

- [ ] **Step 1: Failing tests** — `test_any_command_upgrades_a_v1_repo_and_exits_3`, `test_dirty_v1_repo_refuses_and_lists_paths` (exit 1, nothing written), `test_v2_repo_runs_command_normally`, `test_upgrade_module_does_not_recurse`.
- [ ] **Step 2–4.** **Step 5: Commit** `feat(cookr): upgrade on contact`.

## Phase 2 — commands

### Task 7: `id`, `rename`, `implements`

**Files:**
- Create: `skills/cookr/cli/cookr/modules/id.py`, `rename.py`, `implements.py`
- Test: `tests/unit/test_modules_id_rename_implements.py`

**Interfaces:**
- `cookr id <uuid|rdid> [--json]` → prints `uuid rdid path kind` (local, else foreign via `Resolver`).
- `cookr rename <uuid|rdid> <new-rdid>` → validates `is_rdid`, refuses an existing rdid (names its path), rewrites the index entry, refreshes in-text labels (`links.relabel`) across this cookbook, prints changed files.
- `cookr implements <uuid|rdid> <location> --platform P [--planned]` adds a row (`unverified`, or `planned` with `--planned` and no location check); `--remove <location>` removes it; a location already owned by another entry is refused naming the owner.
- Shared helper for authoring by rdid: `links.to_stored(value: str, resolver) -> str` — accepts rdid or UUID (or `<cookbook-rdid-or-uuid>/<…>`) and returns the stored UUID form; `update` (Task 5's `modules/update.py`) applies it to every `depends-on`/`related` value and to in-text `[label](cookbook:<rdid>)` targets, so authors may write rdids.

- [ ] **Steps 1–5** as usual: tests `test_id_both_directions`, `test_rename_refuses_collision`, `test_rename_relabels_in_text_links`, `test_implements_add_remove_and_refuse_owned`, `test_update_rewrites_rdid_links_to_uuids`. Commit `feat(cookr): id, rename, implements`.

### Task 8: Conformance, `confirm`, `status`

**Files:**
- Create: `skills/cookr/cli/cookr/core/conformance.py`, `modules/confirm.py`, `modules/status.py`
- Test: `tests/unit/test_conformance.py`, `tests/unit/test_modules_status.py`

**Interfaces:**
- `location_hash(repo_root: Path, location: str, ignore: IgnoreSet) -> str` — `"sha256:" + hexdigest` over sorted `(relpath, sha256(file bytes))` lines of every non-ignored file under a directory location, or the one file.
- `effective_state(impl: Implementation, current_version: str, current_hash: str | None) -> str` — `planned`/`unverified` as stored; `needs-validation` when stored so, when the hash differs, or when `level_between(impl.conformance.version, current_version)` is `minor` or `major`; else `confirmed`.
- `level_between(old: str, new: str) -> str` — `none|patch|minor|major`.
- `recipe_state(entry: Entry, ...) -> str` — the weakest implementation's (order: planned < unverified < needs-validation < confirmed; an entry with no implementations is `unplaced`, reported separately).
- `cookr confirm <uuid|rdid> [--platform P] [--location L]` → sets `confirmed` with current version and hash on the matching implementations (all when no filter).
- `cookr status [--json]` → per root: uncovered files (from `coverage`), then implementations by effective state; final line `fully conformant` or `N uncovered · N unverified · N needs-validation · N planned`. Exit 0 always (informational).

- [ ] **Steps 1–5**: tests `test_hash_changes_when_file_changes`, `test_hash_ignores_ignored_files`, `test_confirmed_flips_on_code_change`, `test_patch_bump_keeps_confirmed`, `test_minor_bump_needs_validation`, `test_status_fully_conformant`, `test_status_lists_uncovered_and_states`. Commit `feat(cookr): conformance states, confirm and status`.

### Task 9: Versions — `versions/`, level-proposing `bump`, `diff`

**Files:**
- Create: `skills/cookr/cli/cookr/core/versions.py`, `modules/diff.py`
- Modify: `core/bumping.py` (from Task 5), `modules/bump.py`, `core/history.py` (add `replace_newest_row(history, version, cells) -> str`), `core/markdown.py` (`versions` added to `SKIP_NAMES` so walks and compiles never see it), `core/artifact.py` (`find_folders` skips `versions/`)
- Test: `tests/unit/test_versions.py`, update `tests/unit/test_modules_bump.py`

**Interfaces:**
- `requirements(text: str) -> dict[str, str]` — every line matching `^\s*[-*]?\s*\*\*([a-z0-9][a-z0-9-]*)\*\*:\s*(.+)$` outside fences, name → normalized text (whitespace collapsed).
- `@dataclass RequirementDiff(added: list[str], changed: list[str], removed: list[str])`; `diff(old: str, new: str) -> RequirementDiff`; `propose_level(d: RequirementDiff, content_changed: bool) -> str` (`major` if changed or removed; `minor` if added; `patch` if only content changed; `none` otherwise).
- `base_ref(repo_root: Path) -> str` — `git merge-base HEAD origin/main`, falling back to `main`.
- `base_text(repo_root: Path, folder: Path, ref: str) -> str | None` — the artifact's composed doc at `ref` (`git show` of `artifact.json` and parts), `None` if absent.
- `freeze(folder: Path, version: str, files: dict[str, bytes]) -> Path` → writes `folder/versions/<version>/` (refuses if it exists with different bytes).
- `cookr bump <paths> --summary S [--level L] ...`: level defaults to `propose_level` against the base; the new version is computed from the **base** version; when the branch already bumped: same or lower level → no-op "already bumped to X"; higher → `replace_newest_row` and re-set the version. Freezes the base version into `versions/<base-version>/` when the artifact existed at base and the folder differs.
- `cookr diff <uuid|rdid> <from> [<to>]` — prints added/changed/removed requirements with their text; `<to>` defaults to current; versions read from `versions/` or the working copy.

- [ ] **Steps 1–5**: tests `test_requirements_parsed_outside_fences`, `test_propose_level_rules`, `test_bump_freezes_base_version`, `test_second_bump_same_level_is_noop`, `test_second_bump_higher_level_relevels`, `test_versions_dir_not_compiled`, `test_diff_between_versions`. Commit `feat(cookr): in-source versions, level-proposing bump, diff`.

### Task 10: `scope`

**Files:**
- Create: `skills/cookr/cli/cookr/core/scope.py`, `modules/scope.py`
- Create: `skills/cookr/cli/cookr/core/changes.py` (shared with Task 11)
- Test: `tests/unit/test_scope.py`, `tests/unit/test_changes.py`

**Interfaces:**
- `changes.py`: `@dataclass(frozen) Change(status: str, path: str, old_path: str | None)` (status `A|M|D|R`, `R` only for 100% similarity); `staged(repo_root) -> list[Change]` (`git diff --cached --name-status -z -M100%`); `branch(repo_root, base: str) -> list[Change]` (merge-base…working tree plus untracked: `git diff --name-status -z -M100% <base>` + `git ls-files --others --exclude-standard -z`); `planned(paths: list[str]) -> list[Change]` (all `M`, or `A` when the file doesn't exist).
- `scope.py`: `@dataclass ScopeItem(id: str, rdid: str, state: str, via: str | None)`; `@dataclass Scope(minimum: list[ScopeItem], further: list[ScopeItem], siblings: list[ScopeItem], uncovered: list[str])`; `compute(config: Config, index: Index, resolver: Resolver, changes: list[Change]) -> Scope` — rules exactly as spec §6 (walk only recipe/ingredient kinds; minimum = owners of touched in-root files + their direct recipe/ingredient deps; further = deeper levels; siblings = recipes/ingredients sharing a direct dep with a minimum item, not in minimum).
- `cookr scope [paths…] [--since REF] [--json]` — no paths: `branch(base_ref)`.

- [ ] **Steps 1–5**: tests `test_changes_parse_spaces_and_renames`, `test_rename_out_of_root_is_delete_plus_add`, `test_minimum_is_owner_plus_direct_deps`, `test_guidelines_never_walked`, `test_siblings_share_a_direct_dep`, `test_uncovered_touched_file_listed`, `test_foreign_dependency_in_minimum`. Commit `feat(cookr): scope`.

### Task 11: `check --hook`

**Files:**
- Create: `skills/cookr/cli/cookr/core/hookcheck.py`, `modules/check.py`
- Test: `tests/unit/test_hookcheck.py`

**Interfaces:**
- `@dataclass(frozen) Finding(kind: str, subject: str, message: str)`; kinds: `update`, `create`, `validate`, `dependency`, `bump`.
- `run(config: Config, index: Index, resolver: Resolver, changes: list[Change], base: str) -> list[Finding]` — rules exactly as spec §7, including: pure rename whose index location was updated → nothing; changed content in a covered file with no change in the owner's folder → `update`; uncovered added/modified file → `create`; deleted covered file → `update`; touched implementation not `confirmed` at the current version after the change → `validate` (message includes `cookr diff <rdid> <confirmed-version>` when there is one); unresolvable `depends-on` (state `missing`) → `dependency`; artifact content changed vs base with version equal to base → `bump`.
- `cookr check [--staged | --branch] [--hook] [--json]` — `--hook` prints `cookr: recipe work to do before this lands:` then up to 15 `  - <message>` lines, `  … and N more`, then the procedure line `Do this work now and continue; do not stop to ask. (cookr scope shows the full picture.)`, and exits 2 when there are findings; otherwise exits 0 silently. Without `--hook`: a table, exit 1 on findings.

- [ ] **Steps 1–5**: tests one per rule plus `test_hook_output_capped_at_15`, `test_hook_silent_when_clean`. Commit `feat(cookr): check --hook`.

### Task 12: The hook, its installer and the skill text

**Files:**
- Create: `skills/cookr/hooks/cc-cookr-hook.py`, `skills/cookr/hooks/hook_payload.py` (copy of abstractr's, trimmed to what this hook uses)
- Modify: `skills/cookr/setup/install` (copy `hooks/` to `~/.claude/skills/cookr/hooks/`, and register idempotently in `~/.claude/settings.json`: `SessionStart` and `UserPromptSubmit` with no matcher, `PreToolUse` matcher `Bash`, `Stop` — each `"/usr/bin/python3 ~/.claude/skills/cookr/hooks/cc-cookr-hook.py"` with the absolute home path; existing entries for the same command are not duplicated), `skills/cookr/setup/uninstall` if present (remove them), `skills/cookr/SKILL.md` (new **Working in a cookr repo** section = spec §8 steps; routing rows for `upgrade`, `id`, `rename`, `implements`, `confirm`, `status`, `scope`, `check`, `diff`; remove the organize workflow, the `domain` text and the Reference Implementations table text; bump the skill version)
- Test: `skills/cookr/cli/tests/unit/test_hook_script.py` (runs the script with a JSON payload on stdin via `subprocess`, `COOKR_BIN` env pointing at `python3 -m cookr` from the source tree)

**Interfaces:**
- The hook reads `hook_event_name`; finds the repo from payload `cwd` (or `git -C` target of a commit) by walking up for `.cookr.json`; none → exit 0.
- `SessionStart`/`UserPromptSubmit`: once per session (marker file `~/.cookr/sessions/<session_id>`), print to stdout a JSON `{"hookSpecificOutput": {"hookEventName": ..., "additionalContext": "<reminder>"}}` naming `cookr scope` and the cookr skill's procedure; also runs `cookr skills sync` (Task 13) and reports a failure as one context line, never blocking.
- `PreToolUse` on `Bash`: only when the command is a `git commit` (parse like abstractr's `parse_commit_command`, including `git -C <dir>`); `CC_ALLOW_COOKR=1` in the command → exit 0; runs `cookr check --staged --hook -p <repo>`; passes its exit code and stderr through. Exit 3 (upgrade happened) → exit 2 with the upgrade message.
- `Stop`: `cookr check --branch --hook`; exit 2 blocks with stderr; `stop_hook_active: true` in the payload → exit 0 (no loop).
- Runs cookr as `$COOKR_BIN` if set, else `cookr` on PATH; cookr missing → exit 0.

- [ ] **Steps 1–5**: tests `test_non_cookr_repo_exits_0`, `test_non_commit_bash_exits_0`, `test_commit_with_findings_blocks`, `test_override_env_in_command_allows`, `test_stop_hook_active_does_not_loop`, `test_session_reminder_once`. Commit `feat(cookr): recipes-first hook and installer registration`.

### Task 13: Per-cookbook skill sets, compile on contact, repo scope

**Files:**
- Modify: `core/install.py` (`Installer` gains `scopes: tuple[str, ...]`, persisted per library in the receipt; `Router.register` passes `--scope <path>` for each; `ROUTER_MIN` = the skill-router version from Task 14), `core/skill.py` (default library = the cookbook rdid; the no-prefix exemption stays only for the literal `cookbook`), `modules/install.py` (`--scope PATH` repeatable, `--scope-add PATH`)
- Create: `modules/skills.py` (`cookr skills sync [-p REPO] [--json]`)
- Test: `tests/unit/test_skills_sync.py`, update `tests/unit/test_install.py`

**Interfaces:**
- `cookr skills sync`: for the repo's cookbook and each reachable dependency cookbook: `compile --target skill --check` against `$COOKR_HOME/sets/<rdid>`; stale or missing → install that library with scopes = its receipt scopes ∪ {this repo's main-checkout root (`git rev-parse --path-format=absolute --git-common-dir`'s parent)}. A cookbook with no `.cookr.json` (adc) is installed unscoped. Prints one line per library: `ok|compiled|registered <rdid> (<n> skills)`. Never touches the always-on skill.
- Routes for repo cookbooks: `components/<rdid>/…` plus `components/<rdid>/platform/<p>/…` as today.

- [ ] **Steps 1–5**: tests with a fake router (`COOKR_SKILL_ROUTER` pointing at a recording script in `tmp_path`): `test_sync_compiles_and_registers_with_scope`, `test_sync_adds_dependent_repo_to_dependency_scopes`, `test_sync_noop_when_current`, `test_unscoped_cookbook_has_no_scope_args`. Commit `feat(cookr): per-cookbook skill sets synced on contact, scoped to their repos`.

### Task 14: skill-router per-entry repo scope (peer repo)

**Where:** `/Users/mfullerton/Development/projects/tools/skill-router`, in a peer worktree: `proj -C /Users/mfullerton/Development/projects/tools/skill-router wt create cookr-scopes --no-enter`; work by absolute path in `<repo>/.claude/worktrees/cookr-scopes`; commit, push, open a PR there with `gh pr create --draft`, mark ready when green.

**Files:**
- Modify: `src/skill_router/core/registry.py` (`Entry.scopes: Tuple[str, ...] = ()`, JSON `scopes` written only when non-empty; `register(..., scopes=())` replaces an entry's scopes), `src/skill_router/core/search.py` (`build_view` drops an entry with scopes unless the config's start dir resolves under one of them — pass the cwd through), `src/skill_router/cli/registry.py` (`register --scope PATH`, repeatable, stored resolved and absolute; `list --json` includes `scopes`), version bump (minor) in `pyproject.toml`/`__init__.py`
- Test: `tests/test_registry.py`, `tests/test_cli_router.py` — `test_scoped_entry_hidden_outside_scope`, `test_scoped_entry_visible_in_scope_and_worktrees_below_it`, `test_register_replaces_scopes`, `test_unscoped_entries_unchanged`.

- [ ] **Steps 1–5** in that repo (`python3 -m pytest -q`). Commit `feat: per-entry repo scopes`. Reinstall skill-router from that worktree is **not** done here (install is confirmed with Mike separately); Task 13's tests use the fake router.

### Task 15: `create` and `adopt`

**Files:**
- Modify: `modules/create.py` (format 2: `cookbook/cookbook.json` with new UUID and `--rdid` (required), empty `index.json`, no `recipes/`/`reference/` dirs, no `index.md`/`description.md`)
- Create: `modules/adopt.py`
- Test: update `tests/unit/test_modules_create.py`; `tests/unit/test_modules_adopt.py`

**Interfaces:**
- `cookr create --rdid R [--in DIR]` — idempotent.
- `cookr adopt --rdid R --root PATH:PLATFORM[:KIND[:GROUP]]… [--dependency LOCATION]…` — runs `create`, writes `.cookr.json` (dependencies read from each location's `cookbook.json`, format 1 via `derive_index`), prints `cookr status`.

- [ ] **Steps 1–5**: `test_create_v2_cookbook`, `test_adopt_writes_repo_config_with_dependency`, `test_adopt_refuses_unknown_platform`. Commit `feat(cookr): create and adopt for format 2`.

## Phase 3 — conversions

### Task 16: Convert adc (this repo)

**Files:** everything under `cookbook/` (by the upgrader), `cookbook/cookbook.json` (new), `cookbook/index.json` (new), `tbd/compliance/artifact-formatting/*.md`, `guide/introduction/conventions.md`, `guide/introduction/glossary.md`, `references/*.schema.json` (+ new `index.schema.json`, `cookr-config.schema.json`; `cookbook.schema.json` → format 2), `.claude/skills/{create-artifact,lint-artifact,repair-cookbook,add-artifact,approve-artifact}/`, `.claude/rules/*.md`, `.claude/CLAUDE.md`, `README.md`, `cookbook/ingredients/_template.md`, `cookbook/recipes/_template.md`.

- [ ] **Step 1:** From the worktree root, with a clean tree: `PYTHONPATH=skills/cookr/cli python3 -m cookr upgrade --rdid adc -p .` — expect a report with 486 artifacts, the check entries, and `needs_review` (record the list).
- [ ] **Step 2:** Resolve every `needs_review` link by hand (find the intended artifact, write its rdid, run `update` to store the UUID); `grep -rn "NEEDS REVIEW: unresolved link" cookbook` → nothing.
- [ ] **Step 3:** `PYTHONPATH=skills/cookr/cli python3 -m cookr validate` → green; `… compile --target skill --check --out <scratch>` → green.
- [ ] **Step 4:** Commit the upgrade alone: `chore(adc): cookr format 2 upgrade`.
- [ ] **Step 5:** Rewrite the docs, schemas, skills and rules listed above from `domain`/Reference-Implementations-table/`agenticdevelopercookbook://` to UUID links, rdids, the index and `cookr implements`/`confirm`/`bump`. `grep -rn "agenticdevelopercookbook://\|^domain:\|\"domain\"" --include=*.md --include=*.json . | grep -v docs/` → nothing outside history docs. Update `.claude/rules/after-adding-an-artifact.md` verification to `cookr validate` (links resolve) instead of domain URI checks.
- [ ] **Step 6:** Check the readers outside this repo: `grep -rln "\"domain\"\|domain:" ~/Development/projects/adh/websites/cookbook ~/Development/projects/myagenticteams/agenticdevteam` (and the dev-team plugin repo if separate). Any reader of artifact `domain` is converted in its own peer worktree + PR (`proj -C <repo> wt create cookr-format-2 --no-enter`), reading rdids from `index.json`.
- [ ] **Step 7:** Commit (`docs(adc): conventions, schemas, skills and rules for UUID identity`), push.

### Task 17: Converge and verify the tooling

- [ ] **Step 1:** Full unit suites green in this repo and the skill-router worktree.
- [ ] **Step 2:** Run the hook script by hand against this worktree with a sample commit payload (`echo '{"hook_event_name":"PreToolUse","tool_name":"Bash","tool_input":{"command":"git commit -m x"},"cwd":"<adkitchen worktree>"}' | COOKR_BIN="python3 -m cookr" PYTHONPATH=skills/cookr/cli python3 skills/cookr/hooks/cc-cookr-hook.py`) after Task 19 — expected exit 2 listing work, or 0 when clean.
- [ ] **Step 3:** Mark PR #74 ready: update its description (summary of all tasks + test plan), `gh pr ready`.
- [ ] Global install of cookr, the hook and skill-router is confirmed with Mike before running `skills/cookr/setup/install` and skill-router's `./install` (Build vs. Install rule).

### Task 18: Convert adhsdk (peer repo)

**Where:** `proj -C /Users/mfullerton/Development/projects/shared/adhsdk wt create cookr-format-2 --no-enter`; `<adhsdk>/.claude/worktrees/cookr-format-2`.

- [ ] **Step 1:** `PYTHONPATH=<this worktree>/skills/cookr/cli python3 -m cookr upgrade --rdid adhsdk -p <adhsdk worktree>` — expect 443 + 256 artifacts, the legacy `recipes/` removed, `.cookr.json` format 2 (dropped roots listed), adc as a dependency (resolved via `locations.json`, written by Task 16's upgrade), the 16 + 15 pre-move links resolved through `renames`, the 4 bare names resolved or marked.
- [ ] **Step 2:** Resolve every `needs_review` link as in Task 16 Step 2.
- [ ] **Step 3:** `cookr validate`, `cookr status` (expect everything `unverified`, uncovered files listed) and `cookr skills sync --dry-run` equivalent (`compile --target skill --check`) green.
- [ ] **Step 4:** Commit `chore: cookr format 2 upgrade (UUID links, index, legacy recipes moved in)`, push, `gh pr create --draft`, then `gh pr ready` once validate is green.

### Task 19: Adopt cookr in adkitchen (peer repo)

**Where:** `proj -C /Users/mfullerton/Development/projects/apps/adkitchen wt create cookr-adopt --no-enter`.

- [ ] **Step 1:** `PYTHONPATH=<this worktree>/skills/cookr/cli python3 -m cookr adopt -p <adkitchen worktree> --rdid adkitchen --root App/Sources:macos:ui:app --root ADTerminal:macos:ui:adterminal --root App/adkd:macos:logic:daemon --root App/adk:macos:logic:daemon --dependency external/adhsdk/cookbook` — `.cookr.json` ignores `**/Generated/**` and `**/*.xcodeproj/**`; adhsdk resolves through the submodule (format 1 there until adhsdk's PR merges, read through `derive_index`).
- [ ] **Step 2:** `cookr status` lists everything uncovered; `cookr validate` green.
- [ ] **Step 3:** Commit `chore: adopt cookr (recipes-first)`, push, draft PR, ready.

---

## Self-review notes

- Spec coverage: §1 → T1/T2/T7; §2 → T1/T5/T7; §3 → T2; §4 → T3/T8; §5 → T4/T6; §6 → T10; §7 → T11/T12; §8 → T12; §9 → T8; §10 → T9; §11 → T13/T14; §12 rollout → T16–T19.
- Decisions this plan adds (Claude's): check UUIDs are uuid5 of the cookbook id so a derived index agrees with the real one; an existing `cookbook.json` `id` is kept as the cookbook UUID; a format-1 cookbook with no identity can't be derived and says "upgrade it first" (rollout order makes adc first); `organize` is retired into the upgrader; repo cookbooks' skills are named and routed by rdid (adc's become `adc-…`); exit 3 means "upgraded, commit and rerun"; bump computes from the base version so a branch carries one bump.
