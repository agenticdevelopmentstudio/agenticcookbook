
- The agent **MUST** record the chosen store and the one-line requirement that justifies it (in an ADR or the plan).
- The agent **MUST NOT** introduce a second datastore "for scale" without a measured limit on the first; YAGNI applies.
- The agent **SHOULD** prefer a single relational store with extensions over polyglot persistence until a specific store earns its operational cost.
- For semi-structured data, the agent **SHOULD** evaluate `jsonb` in the relational store before adopting a separate document database.
- The agent **SHOULD** keep derived stores (search index, cache, vector index) as **secondary** projections of the relational system of record, not as the source of truth.
- When scale is asserted as the reason for a non-relational store, the agent **MUST** cite an expected workload (writes/sec, dataset size, read pattern), not a generic claim.

