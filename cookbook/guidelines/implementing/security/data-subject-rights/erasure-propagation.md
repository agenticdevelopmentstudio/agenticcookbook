
Deletion **MUST** reach every derived copy, not just the primary row:

- Caches, search indexes, denormalized read models, and analytics aggregates.
- Third-party processors — call their deletion APIs and record completion.
- Logs and event streams: prefer pseudonymization or crypto-shredding (delete the per-subject key) where immutable append-only logs make row deletion impractical.
- Backups: full purge is often infeasible; document the rotation window after which restored backups are re-scrubbed, and treat that window as part of the SLA.

