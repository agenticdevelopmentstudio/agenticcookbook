
- `should-combine-push-and-pull`: Separate push and pull calls double the round trips, which is costly on high-latency mobile networks.
- `should-use-hlc-for-timestamp-sync`: Timestamp-based delta sync is simpler but vulnerable to clock skew.
- `must-paginate-by-sync-version-cursor`: Offset-based pagination skips records if new changes arrive during sync.
- `must-make-sync-operations-replayable`: Network failures mean the same batch may be delivered multiple times.
- `must-write-data-and-queue-atomically`: This guarantees the outbox always reflects local state — there is no window where a change is visible on screen but not queued for sync.

