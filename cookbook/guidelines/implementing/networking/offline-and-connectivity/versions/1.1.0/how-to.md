
**Patterns (in order of complexity):**
1. **Optimistic updates** — apply changes to local UI immediately, sync in background. Roll
   back on server failure. Sufficient for most apps.
2. **Queue-based sync** — mutations go into an outbox queue, drained when connectivity returns.
   Failed items stay in queue for retry.
3. **Conflict resolution** — use ETags or version numbers to detect conflicts. Return 409 with
   both versions. Simple apps use server-wins; collaborative apps need merge UI or CRDTs.
