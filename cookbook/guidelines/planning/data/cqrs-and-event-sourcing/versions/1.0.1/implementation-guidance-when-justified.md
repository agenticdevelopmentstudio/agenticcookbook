
- **explicit-over-implicit**: model commands and events as named, versioned types; never overload one generic "update" event.
- **idempotency**: command handlers and projectors **MUST** be idempotent — events may be redelivered; dedupe on a stable event id.
- Keep CQRS **without** event sourcing as a valid stopping point: separating read/write models in one database is far cheaper than a full event store, and often enough.
- Start in-process and single-store; introduce separate read stores or message infrastructure **only** when the triggering requirement demands it.
- Define the consistency contract per use case (which reads may be stale, which must be strongly consistent) and surface it in the API.

