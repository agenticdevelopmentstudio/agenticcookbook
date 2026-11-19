
- `should-implement-syncable-interface`: Benefits: sync logic is tested once in the orchestrator; adding a new entity is a single interface implementation; entity-specific quirks are contained.
- `should-complete-cycle-in-one-round-trip`: Combining push and pull into one HTTP request halves network round trips compared to separate push and pull calls — significant on mobile networks with 200–800ms latency.
- `must-surface-persistent-sync-failures`: A status indicator showing "Sync paused — check connection" is acceptable; silently losing changes is not.

