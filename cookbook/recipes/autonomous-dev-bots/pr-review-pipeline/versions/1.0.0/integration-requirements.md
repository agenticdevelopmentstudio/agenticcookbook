
### Trigger and execution

- **webhook-trigger**: The pipeline MUST trigger when a GitHub `pull_request` event (opened, synchronize, reopened) is received at the OpenClaw webhook endpoint (`POST /hooks/agent`).
- **poll-fallback**: The pipeline SHOULD fall back to polling via `gh pr list` on a cron schedule if webhooks are unavailable.
- **isolated-session**: Each pipeline run MUST execute in an isolated OpenClaw agent session to prevent cross-contamination between PR reviews.
- **sequential-phases**: Phases MUST run sequentially: Phase 1 → Phase 2 → Phase 3.
- **short-circuit**: The pipeline MUST stop and not run subsequent phases if a phase posts "Request Changes".
- **rerun-on-update**: The pipeline MUST rerun from Phase 1 when new commits are pushed to the PR branch.

### Rejection and appeal

- **rejection-format**: A rejecting phase MUST post a PR review with "Request Changes" status, including per-issue explanation of what failed and why.
- **branch-protection**: The repository MUST be configured to require approval from all three phase bot GitHub Apps plus a human reviewer before merging is allowed.
- **appeal-process**: If a contributor replies to a rejection comment disputing the decision, the pipeline MUST flag the PR for human review rather than re-running automatically.
- **rerun-after-fix**: After the refactoring agent applies fixes, the pipeline MUST rerun from Phase 1 on the updated content.

### Cross-ingredient wiring

- **phase-findings-flow-forward**: Phase 2 MUST receive the cleaned content and findings from Phase 1, and Phase 3 MUST receive the findings of both prior phases, since Phase 3's quality score depends on how clean the Phase 1 and Phase 2 passes were.
- **fixes-come-from-fix-agent**: Every automated change, whether a Phase 1 structural fix or a human-approved Phase 2 refactoring proposal, MUST be applied by the PR fix agent, and the three phase bots MUST remain read-only reviewers.
- **fix-preference-read-at-fix-time**: The fix agent MUST read the contributor's stored fix preference from the PR body on each run and MUST NOT cache it across PRs.

