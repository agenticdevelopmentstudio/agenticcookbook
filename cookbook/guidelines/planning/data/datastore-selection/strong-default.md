
- For a new server backend, the agent **SHOULD** default to a **relational database** (PostgreSQL is the recommended default).
- A **non-relational primary store MUST be justified by a specific, stated requirement** (a query pattern, scale ceiling, or access shape the relational option cannot meet), not by a default preference, hype, or "it scales better."
- Caveat: "just use Postgres" essays are common, but they are **advocacy, not consensus**. Treat the relational default as a strong starting point that a real requirement can override — not as a universal law.

