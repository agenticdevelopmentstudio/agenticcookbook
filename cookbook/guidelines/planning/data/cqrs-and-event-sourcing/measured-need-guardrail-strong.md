
These patterns add real, ongoing complexity. Per `yagni` and `make-it-work-make-it-right-make-it-fast`, you **MUST NOT** default to them.

- You **MUST** justify adoption with a concrete, present requirement — not a forecast that the system "might" need to scale or "might" want history later.
- Default to a single model (CRUD over one datastore). When history is the only driver, an audit/history table or change-data-capture log **SHOULD** be evaluated first and usually suffices.
- You **MUST** treat the choice as a deliberate, documented decision (record the triggering requirement), not a mandate or a resume-driven default.

