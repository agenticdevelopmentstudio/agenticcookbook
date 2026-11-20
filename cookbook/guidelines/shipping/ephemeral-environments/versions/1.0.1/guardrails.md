
- Preview environments MUST NOT have write access to production data stores, queues, or third-party prod accounts; point them at sandbox credentials.
- Spin-up and teardown jobs SHOULD be idempotent so a re-run or retried webhook does not duplicate or orphan resources.
- Note: managed-platform feature names and DB-branching capabilities evolve quickly — verify current behavior against the vendor's docs before relying on a specific guarantee. FORECAST: treat any "instant branch" or per-PR-cost claim as vendor-specific and unverified until measured in your own pipeline.

