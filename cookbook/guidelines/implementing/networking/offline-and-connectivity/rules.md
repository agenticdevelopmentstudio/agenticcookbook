
- **should-design-local-first**: For apps that must work offline, the app SHOULD be designed for local-first with background sync.
- **should-roll-back-failed-optimistic-updates**: An app using **optimistic updates** SHOULD apply changes to local UI immediately, sync in background, and roll back on server failure.
- **should-keep-failed-items-queued**: In **queue-based sync**, failed items SHOULD stay in queue for retry.
- **should-detect-conflicts-with-versions**: For **conflict resolution**, an app SHOULD use ETags or version numbers to detect conflicts.
- **should-return-409-with-both-versions**: On a detected conflict, the server SHOULD return 409 with both versions.
- **should-fit-resolution-to-collaboration**: Simple apps SHOULD use server-wins; collaborative apps SHOULD use merge UI or CRDTs.

**Practical defaults:**
- **should-track-last-synced-at**: The app SHOULD track `last_synced_at` per entity for delta sync.
- **should-show-connectivity-status**: The app SHOULD show clear connectivity status to the user.
- **must-queue-mutations-and-keep-user-work**: Mutations MUST be queued locally; user work MUST NOT be silently discarded
- **should-test-offline-scenarios**: Offline scenarios SHOULD be tested — airplane mode, flaky connections, long offline periods
