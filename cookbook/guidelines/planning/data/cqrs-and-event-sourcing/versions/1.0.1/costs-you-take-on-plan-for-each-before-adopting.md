
| Cost | What it requires |
|------|------------------|
| Eventual consistency | Read models lag writes; UI/API **MUST** tolerate the delay (optimistic update, loading state, or read-your-writes routing). |
| Projection rebuilds | A documented, tested procedure to rebuild read models from the log; **MUST** be runnable without downtime for large stores. |
| Event versioning | Events are immutable once written; you **MUST** have an upcasting/versioning plan before the first event ships — schema changes are not retroactive edits. |
| Operational surface | Command handlers, event store, projectors, and read stores each add deployment, monitoring, and failure modes (`manage-complexity-through-boundaries`). |

