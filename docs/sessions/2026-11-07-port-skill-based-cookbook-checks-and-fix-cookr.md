# Session: port the skill-based-cookbook checks, fix `cookr install`, and route lookups through skill-router hooks

- **Date:** 2026-11-07
- **Session:** `801493db-92cb-4ac4-bce9-f3156e265e32`
- **Branch:** `port-changes-fix-main`

## Orientation

This session started by comparing the old `skill-based-cookbook` branch with main. It then
ported that branch's useful checks into cookr on a fresh worktree (`port-changes-fix-main`) and
fixed the problems found on main: `cookr install` was broken against skill-router 0.4.0 and against
the repo rearrangement, and 30 compiled guideline docs had been committed beside their source
folders. The work merged as PR #72 in two commits: `dd2e4670` (checks plus the corpus fixes) and
`44c510bf` (install fix). The live install was run: 486 routed skills are registered with
skill-router for Claude and Codex. The session ended by working out how a model gets pointed at
those routed skills. The answer is skill-router's prompt hook, which Mike's own skill-router
change (`371f3b3`) now always installs.

## Decisions

- **Port the checks rather than merge the branch.** `skill-based-cookbook` had diverged too far from
  main. Its value was three `cookr validate` checks: guideline-twin drift, rule-less
  guidelines, and over-long skills. They were re-implemented on current main in
  `cookr/core/twins.py`, and the corpus was fixed to pass them. Twins that differ on purpose
  record `twin_differs`, and purely informational guidelines record `informational`, so each
  exception carries its reason in the artifact itself.
- **Compile references from source folders at install time.** Folders have been the only committed
  form since `971a6490`, so the reference manifests could not copy docs that no longer exist. Two new
  manifest entry types, `artifact` and `artifacts`, compose the docs during `./install`. Dependencies
  install first because composing needs PyYAML.
- **Delete the 30 stale compiled docs, and add a test.** Each was checked as identical to its
  folder before deletion. `test_no_compiled_doc_is_committed_beside_its_folder` keeps them from
  coming back, following the standing rule to remove the old form after a conversion.
- **Leave the hand-edited always-on `general-principles` skill alone.** `install --replace`
  reported DRIFT because Mike edited it by hand. Overwriting it with `--force` is Mike's call.
- **Squash PR #72 into two logical commits, not one.** The port and the install fix are
  independent. A reviewer could revert either alone. Mike approved the grouping.

## Considered and rejected

- **Merging `skill-based-cookbook` directly.** Rejected: it predates the folder conversion and
  the repo rearrangement, so a merge would have reintroduced docs and old paths.
- **Running `cookr update` on the repo.** Rejected: `update` still reads docs, so on a
  folders-only repo it would rebuild the indexes from nothing.
- **Relying only on the always-on skill or a global CLAUDE.md line to make the model use the
  router.** Superseded by skill-router's prompt hook. The hook injects a route hint per prompt,
  which is more targeted than a standing instruction.

## Research / findings

- skill-router is installed editable from `~/Development/projects/tools/skill-router`. It is not
  `adh/skill-router`, which was wrongly stated once in this session.
- The skill-router hooks are a prompt hint (`skill-router: likely <route> (<n> skills) — run:
  skill-router route <route> --host claude`), a lookup marker, and gate-once. A repo's
  `.skill-router.json` sets `enforcement` to `off`, `nudge` (the default) or `gate-once`. Every hook
  lets work through if it fails.
- Probing the prompt hook from this repo:
  - "add a new guideline about error handling" and "review this swiftui view for accessibility"
    each produced a route hint.
  - "write a pytest test for the manifest materializer" produced nothing, because matching uses
    route keywords only.
- Routed lookups serve the set compiled from the main checkout at install time, not a worktree's
  edits.

## Open threads

- `cookr validate` and `cookr update` still read docs, not folders. On this repo, validate reports
  every doc missing. They need porting to folders.
- The receipt for the always-on `general-principles` skill names the old `adh/agenticcookbook`
  checkout, so `cookr install --check` reports `library:cookbook` BROKEN. Mike decides whether to
  run `--force` or keep his edit.
- Whether this repo should set `{"enforcement": "gate-once"}` in a `.skill-router.json`. This is
  Mike's call.
- Prompt-hook coverage depends on the route keywords cookr writes. Prompts like the pytest one get
  no hint.

## Pointers

- PR #72: https://github.com/agenticdevelopmentstudio/agenticcookbook/pull/72
- Status: [docs/project/STATUS.md](../project/STATUS.md)
- Code: `skills/cookr/cli/cookr/core/twins.py`, `cookr/core/manifest.py`, `cookr/core/install.py`,
  `skills/cookr/cli/reference-manifest.json`
- Earlier session: [2026-10-04 compiled artifacts and routed skills](2026-10-04-compiled-artifacts-and-routed-skills.md)
