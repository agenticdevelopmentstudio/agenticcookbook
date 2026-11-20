
- **single-trunk**: There MUST be one shared mainline branch (`main`) that is the integration point for all work. Long-lived parallel development branches (`develop`, `release/*` kept open for weeks) MUST NOT be used as the primary integration target.
- **integrate-daily**: Work SHOULD be integrated into trunk at least once per day. If a unit of work cannot reach trunk within a day, it SHOULD be decomposed into smaller, independently mergeable steps.
- **short-lived-branches**: Branches SHOULD live no more than 1-2 days before merging. The agent MUST prefer many small merges over one large merge.
- **flag-incomplete-work**: Incomplete or not-yet-enabled work MUST be hidden behind a feature flag and merged to trunk in a disabled state, rather than parked on a branch until "done." See the feature-flags guideline.
- **trunk-stays-releasable**: Trunk MUST remain in a releasable state at all times. A merge that would break the build or fail required checks MUST NOT land.

