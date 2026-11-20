
- **single-trunk**: There MUST be one shared mainline branch (`main`) that is the integration point for all work. Long-lived parallel development branches (`develop`, `release/*` kept open for weeks) MUST NOT be used as the primary integration target.
- **integrate-daily**: Work SHOULD be integrated into trunk at least once per day. If a unit of work cannot reach trunk within a day, it SHOULD be decomposed into smaller, independently mergeable steps.
- **short-lived-branches**: Branches SHOULD live no more than 1-2 days before merging. The agent MUST prefer many small merges over one large merge.
- **flag-incomplete-work**: Incomplete or not-yet-enabled work MUST be hidden behind a feature flag and merged to trunk in a disabled state, rather than parked on a branch until "done." See the feature-flags guideline.
- **trunk-stays-releasable**: Trunk MUST remain in a releasable state at all times. A merge that would break the build or fail required checks MUST NOT land.


- **green-trunk**: Required status checks (build, tests, lint) MUST pass before any merge to trunk. Trunk MUST NOT be left red.
- **revertable-merges**: Each merge SHOULD be a single squashed commit so a regression can be reverted as one atomic unit.
- **no-freeze**: Integration MUST NOT be deferred to a batched "integration" or "stabilization" phase; integrate continuously.

- **should-branch-small**: The agent SHOULD cut a short-lived branch from current `main` for one logical change.
- **should-flag-partial-change**: If the change is partial, the agent SHOULD gate the new behavior behind a feature flag (default off), adding code paths that are inert until the flag is enabled.
- **should-commit-atomically**: The agent SHOULD make one logical change per commit (see atomic-commits), running the build and tests before each commit.
- **should-rebase-onto-main**: Before opening or updating a PR, the agent SHOULD rebase the branch onto the latest `main` so the diff reflects current trunk.
- **should-merge-within-a-day**: The agent SHOULD open the PR, get checks green, and merge within a day.
- **should-prefer-squash-merges**: The agent SHOULD prefer squash merges to keep trunk history linear and each merge a single revertible unit.
- **must-not-sit-on-work**: The agent MUST NOT accumulate days of work on a branch "until it's complete." Land enabling-but-disabled increments instead.
- **must-not-let-branch-diverge**: MUST NOT open a branch and let it diverge from trunk for a week, then attempt a large merge.
- **must-not-use-develop-as-staging-trunk**: MUST NOT use a `develop` branch as a staging trunk that periodically merges into `main`; this is GitFlow, not trunk-based development, and reintroduces batched integration.
- **must-not-park-finished-code-on-branch**: MUST NOT hold finished-but-unreleased code on a branch — merge it disabled behind a flag.
- **must-not-bypass-required-checks**: MUST NOT disable or bypass required checks to land a merge faster.
- **should-establish-green-trunk-gating-first**: Trunk-based development assumes strong automated checks and a fast CI feedback loop; without them, frequent merges to a shared trunk amplify breakage. Green-trunk gating SHOULD be established first.
- **may-cut-release-branch-for-audited-build**: Heavily regulated contexts MAY require a release branch for a tagged, audited build. That is a release artifact cut *from* trunk, not a long-lived integration branch — trunk remains the single integration point.
- **should-treat-dora-as-correlation**: The DORA finding SHOULD be treated as a validated *correlation with* delivery performance, not a guarantee.
