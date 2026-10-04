
# Offline and Connectivity

For apps that must work offline, design for local-first with background sync.

**Patterns (in order of complexity):**
1. **Optimistic updates** — apply changes to local UI immediately, sync in background. Roll
   back on server failure. Sufficient for most apps.
2. **Queue-based sync** — mutations go into an outbox queue, drained when connectivity returns.
   Failed items stay in queue for retry.
3. **Conflict resolution** — use ETags or version numbers to detect conflicts. Return 409 with
   both versions. Simple apps use server-wins; collaborative apps need merge UI or CRDTs.

**Practical defaults:**
- Track `last_synced_at` per entity for delta sync
- Show clear connectivity status to the user
- Mutations MUST be queued locally; user work MUST NOT be silently discarded
- Offline scenarios SHOULD be tested — airplane mode, flaky connections, long offline periods

References:
- [web.dev: Offline Cookbook](https://web.dev/articles/offline-cookbook)
- [CRDTs](https://crdt.tech/)

