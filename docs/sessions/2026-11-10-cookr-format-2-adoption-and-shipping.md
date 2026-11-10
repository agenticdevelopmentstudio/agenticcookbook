# Session: recipes first in every repo: cookr format 2, adoption, and the ship

- **Date:** 2026-11-10
- **Session:** `3d6537c4-fa37-40ec-9a1f-0bd9225039ed`
- **Branch:** `more-cookr` (PR #74), `docs-update-kaiser`

## Orientation

Mike wants cookr expanded so that every repo that opts in works **recipes first**. The reasoning is
about multi-platform work. Mike separates *multi-platform* (native code on each platform, all built
from one shared design, the recipe) from *cross-platform* (one tool compiles down to native code, as
React Native does). Cross-platform tooling exists so humans can write code once. Agents can write
native code for each platform, and the result is better. So the recipe, plus a reference
implementation, is the spec that makes a port fast. Each port then refines the recipe, and recipes
fold back into the cookbook over time.

This session brainstormed the design and wrote it up
(`docs/superpowers/specs/2026-11-09-cookr-adoption-design.md`, approved). It then wrote the plan and
ran it Subagent-Driven, and shipped it across eight repos with `/ship` in squash mode, using squashr.
Six repos are merged. pipeline#4 and teamtesting#19 are blocked (see *Open threads*). The docs fold
for PR #74 is this branch.

## Decisions

- **Extend the existing `.cookr.json`; don't add a new file.** It holds only what the cookbook
  project doesn't describe: code roots, which directories must have recipes, ignore rules,
  dependencies on other cookbooks, and a list of "not done" exceptions that shrinks as backfill
  proceeds. *Why:* the cookbook project must not know about cookr, because cookr is a tool for the
  user and the agent. A repo that is fully converted has no backfill left, so its config gets simpler.
- **References are general, not file paths.** A reference can be a relative path today and a GitHub
  URL tomorrow. *Why:* hard-coded paths break whenever code moves.
- **A recipe lives in the repo of the code it describes.** An app-specific window's recipe is in the
  app's cookbook. The shared pieces' recipes are in the shared repo, and the app recipe links to them.
- **Identity is a UUID, with a separate index mapping each UUID to its rdid and location**
  (`cookbook/index.json`). This follows the adhub backend's model. Other cookbooks are identified the
  same way, as `<cookbook-uuid>/<uuid>`. A cached rdid is there only for readability, and the index
  refreshes it when it changes. *Why:* renaming or moving an artifact must never break the projects
  that reference it.
- **Enforcement nudges and never halts.** When source changes have no recipe to match them, the hook
  blocks the commit or the end of the turn, and tells the agent to update the recipe. *Why:* Mike's
  rule is "it doesn't stop the work, it just reminds the agent to also do that work."
- **Update whatever you touch, nothing more by default.** If you change the Safari web panel, the
  web-panel abstraction and the Safari panel both become conformant. The Chrome sibling does not.
  The agent reports the minimum required set (`cookr scope`) and asks whether siblings should follow.
- **Convert fully, and convert on contact.** adc and adhsdk were converted outright. cookr's
  upgrader converts any format-1 cookbook it meets in a repo it works in.
- **Recipes have a state** (`confirmed`, `pending`, `needs validating`, and so on; see
  `cookr confirm` and `cookr status`). A repo is fully conformant when all of its code has recipes
  and every recipe is confirmed. *Why:* recipes can be moved now and validated later without stalling
  the work.
- **Artifacts compile to agent-facing skills with versions frozen.** Each artifact has one master
  copy, the source folder. That copy compiles into a minimal routed skill, and per-cookbook skill
  sets are scoped per repo through skill-router. `cookr bump` freezes earlier versions in
  `versions/`, so every version stays in the source.
- **Execution was Subagent-Driven.** That handoff is already decided in CLAUDE.md.
- **Ship:** `/ship squash` through squashr in every repo. Cookbook PR #74 kept two logical commits:
  the format-2 feature and the `__pycache__/` ignore, an unrelated chore. The website kept its two
  commits. Every other repo squashed to one.

## Considered and rejected

- **Putting every mapped entry in `.cookr.json`.** Rejected because the cookbook project already
  describes those entries, so a second copy would drift.
- **Paths as identity.** Rejected because any reorganization breaks every link.
- **Moving recipes into the adh backend database now.** Out of scope for now. Mike expects this to
  happen eventually, but it is a long way off.

## Open threads

- **pipeline#4 is not merged.** Its branch `cookr-format-2` has been squashed and rebased (one commit,
  `c58dd884`). `proj wt merge` refuses to run because the pipeline main checkout has an untracked
  `testing/` directory. That directory is left over from `d2f20f6f` (1104 files, 18 of them not
  `__pycache__`). It isn't this session's, so it's Mike's call. Once it's cleared:
  1. Re-run `proj -C <pipeline main> wt merge cookr-format-2 --summary-file <msg> --squash
     --auto-resolve-conflicts false`.
  2. Point teamtesting#19's `external/pipeline` at the merge commit.
  3. Ship teamtesting#19.
- **Global install of the new cookr is not done.** This covers `cookr install` and skill-router's
  `./install`, and it needs Mike's OK. Until it runs, routed lookups serve the format-1 set.
- **The hand-edited `general-principles` skill** must not be adopted or replaced without Mike's OK.

## Pointers

- Design: `docs/superpowers/specs/2026-11-09-cookr-adoption-design.md`
- Plan: `docs/superpowers/plans/2026-11-09-cookr-adoption.md`
- Status: `docs/project/STATUS.md`, section *Format 2 and recipes-first adoption*
- PRs:
  - agenticcookbook#74 (`689ab01`, `e75c550`)
  - skill-router#4
  - adhsdk#46
  - adcookbookwebsite#21
  - agenticdevteam#2
  - adkitchen#103
  - pipeline#4 (blocked)
  - teamtesting#19 (blocked)
