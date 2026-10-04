
Four GitHub App identities are required:

| App | Purpose | Posts as |
|-----|---------|---------|
| Cookbook Review Bot | Phase 1: structural, prose, completeness, conventions | `@cookbook-review-bot[bot]` |
| Cookbook Scope Bot | Phase 2: placement, granularity, overlap, ecosystem fit | `@cookbook-scope-bot[bot]` |
| Cookbook Eval Bot | Phase 3: value, risk, recommendation | `@cookbook-eval-bot[bot]` |
| Cookbook Fix Bot | Refactoring agent: applies all automated fixes | `@cookbook-fix-bot[bot]` |

Each app requires:
- `checks:write` permission (to create check runs)
- `pull_requests:write` permission (to post reviews and suggested changes)
- `contents:write` permission (Fix Bot only — to push commits)
- Private key PEM stored on the execution Mac
- Installation tokens generated per run via `gh-token` extension

