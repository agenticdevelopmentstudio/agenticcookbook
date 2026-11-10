
| State | Source | Consumer | Direction | Mechanism |
|-------|--------|----------|-----------|-----------|
| Fix preference | Contributor via `/contribute-to-cookbook` | PR fix agent | one-way | HTML comment in the PR body: `<!-- fix-preference: auto -->` or `<!-- fix-preference: review -->`; default `auto` |
| Phase result (approve or request changes) | Each phase bot | The next phase, branch protection, the human reviewer | one-way | GitHub PR review under the phase bot's identity |
| Phase findings | Phase 1 and Phase 2 | Phase 3 and the fix agent | one-way | Findings carried within the isolated session run and summarized in the PR review |
| Refactoring proposal | Phase 2 | Human reviewer, then the fix agent | one-way | Posted in the Phase 2 review; applied only after the human approves it |
| Rejection and appeal thread | Rejecting phase and contributor | Pipeline and human reviewer | two-way | PR review comments; a contributor reply disputing the decision flags the PR for human review |
| Commit SHA under review | PR branch | All phases | one-way | A new push cancels the current run and restarts from Phase 1 on the latest commit |

