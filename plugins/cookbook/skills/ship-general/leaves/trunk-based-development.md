<!-- leaf: ship-general/trunk-based-development · source: guidelines/shipping/trunk-based-development.md -->

**Rules** (cite as `ship-general/trunk-based-development#<slug>`):

- `single-trunk` MUST
- `integrate-daily` SHOULD
- `short-lived-branches` MUST
- `flag-incomplete-work` MUST
- `trunk-stays-releasable` MUST
- `rebase-don-t-drift` SHOULD — Before opening or updating a PR, the agent SHOULD rebase the branch onto the latest main so the diff reflects current …
- `don-t-sit-on-it` MUST — The agent MUST NOT accumulate days of work on a branch "until it's complete." Land enabling-but-disabled increments …
- `green-trunk` MUST
- `revertable-merges` SHOULD
- `no-freeze` MUST

# Trunk-based development

Integrate every change into a single shared trunk in small, frequent increments. Branches are short-lived, and incomplete work is hidden behind feature flags rather than held on a long-running branch. Frequent integration keeps merges cheap and trunk releasable, so rigor stays affordable.

## Core practices

- **single-trunk**: There MUST be one shared mainline branch (`main`) that is the integration point for all work. Long-lived parallel development branches (`develop`, `release/*` kept open for weeks) MUST NOT be used as the primary integration target.
- **integrate-daily**: Work SHOULD be integrated into trunk at least once per day. If a unit of work cannot reach trunk within a day, it SHOULD be decomposed into smaller, independently mergeable steps.
- **short-lived-branches**: Branches SHOULD live no more than 1-2 days before merging. The agent MUST prefer many small merges over one large merge.
- **flag-incomplete-work**: Incomplete or not-yet-enabled work MUST be hidden behind a feature flag and merged to trunk in a disabled state, rather than parked on a branch until "done." See the feature-flags guideline.
- **trunk-stays-releasable**: Trunk MUST remain in a releasable state at all times. A merge that would break the build or fail required checks MUST NOT land.

## Why frequency beats branch isolation

The DORA research program (Accelerate / State of DevOps) identifies trunk-based development as a capability that predicts higher software delivery performance — fewer active branches, branches that live less than a day, and no code-freeze/integration phases. Treat this as a validated *correlation with* delivery performance, not a guarantee; the mechanism is that small, frequent integrations shrink merge conflicts and keep feedback fast.

- Long-lived feature branches accumulate divergence; the eventual merge is large, risky, and hard to review — the opposite of small-reversible-decisions.
- Daily integration surfaces conflicts while they are small and the context is fresh.
- A continuously releasable trunk decouples *merging* from *releasing*: code ships dark, then is enabled via a flag.

## How an agent should work on trunk

1. **Branch small.** Cut a short-lived branch from current `main` for one logical change.
2. **Keep work shippable.** If the change is partial, gate the new behavior behind a feature flag (default off). Add code paths that are inert until the flag is enabled.
3. **Commit atomically.** One logical change per commit (see atomic-commits), running the build and tests before each commit.
4. **Rebase, don't drift.** Before opening or updating a PR, the agent SHOULD rebase the branch onto the latest `main` so the diff reflects current trunk.
5. **Merge fast.** Open the PR, get checks green, and merge within a day. Prefer squash merges to keep trunk history linear and each merge a single revertible unit.
6. **Don't sit on it.** The agent MUST NOT accumulate days of work on a branch "until it's complete." Land enabling-but-disabled increments instead.

## Required protections

- **green-trunk**: Required status checks (build, tests, lint) MUST pass before any merge to trunk. Trunk MUST NOT be left red.
- **revertable-merges**: Each merge SHOULD be a single squashed commit so a regression can be reverted as one atomic unit.
- **no-freeze**: Integration MUST NOT be deferred to a batched "integration" or "stabilization" phase; integrate continuously.

## Anti-patterns

- **DO NOT** open a branch and let it diverge from trunk for a week, then attempt a large merge.
- **DO NOT** use a `develop` branch as a staging trunk that periodically merges into `main`; this is GitFlow, not trunk-based development, and reintroduces batched integration.
- **DO NOT** hold finished-but-unreleased code on a branch — merge it disabled behind a flag.
- **DO NOT** disable or bypass required checks to land a merge faster.

## Caveats

- Trunk-based development assumes strong automated checks and a fast CI feedback loop; without them, frequent merges to a shared trunk amplify breakage. Establish green-trunk gating first.
- Heavily regulated contexts may require a release branch for a tagged, audited build. That is a release artifact cut *from* trunk, not a long-lived integration branch — trunk remains the single integration point.
