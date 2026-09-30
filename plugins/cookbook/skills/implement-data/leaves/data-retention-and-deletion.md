<!-- leaf: implement-data/data-retention-and-deletion · source: guidelines/implementing/data/data-retention-and-deletion.md -->

**Rules** (cite as `implement-data/data-retention-and-deletion#<slug>`):

- `category-have-defined-retention-period` MUST — Every category MUST have a defined retention period; absence of a period is itself a decision and MUST be justified …
- `category-have-automated-expiry-scheduled` SHOULD — Each category SHOULD have automated expiry — a scheduled job, TTL index, or partition-drop — rather than manual cleanup.
- `deletions-cascade-from-source-truth` SHOULD — Deletions SHOULD cascade from the source of truth to every derived store: denormalized tables, read replicas, caches …
- `partially-failed-cascade-detectable-resumable-silently-abandoned` MUST — Make cascade steps idempotent and retryable; a partially failed cascade MUST be detectable and resumable, not silently …
- `globally-erasure-obligations-resolve-hard-delete-true` MUST — Decide soft vs. hard per category, not globally. Erasure obligations MUST resolve to hard delete or true anonymization …
- `backups-immutable-logs-excluded-from-immediate-cascade` SHOULD — Backups and immutable logs SHOULD be excluded from immediate cascade; instead document the lag — deleted data persists …
- `rotation-residual-copies-not-restore-deleted-records-from` MUST — For an erasure request, suppress the data from active systems immediately and rely on backup rotation for residual …

# Data retention and deletion

Data is a liability as much as an asset. Do not keep it forever: define how long each category lives, then automate its expiry or anonymization and propagate every deletion to all derived copies. This is engineering guidance, not legal advice — confirm concrete retention periods with counsel.

## Retention schedule

Storage limitation (GDPR Art. 5(1)(e), as of the 2016 regulation) requires that data be kept no longer than necessary for its purpose.

- Maintain a **retention schedule** as code or config that maps each **data category** (user profile, auth tokens, audit logs, analytics events, PII, derived ML features) to a maximum retention period and a disposition (delete vs. anonymize).
- Every category **MUST** have a defined retention period; absence of a period is itself a decision and **MUST** be justified (e.g., legal-hold or financial records with a statutory minimum).
- Each category **SHOULD** have **automated expiry** — a scheduled job, TTL index, or partition-drop — rather than manual cleanup.
- Record a `created_at` (and where relevant `expires_at`) timestamp on every retained record so expiry is computable and auditable.

## Cascading deletion

A deletion that misses a copy is not a deletion.

- Deletions **SHOULD cascade** from the source of truth to every derived store: denormalized tables, read replicas, caches (Redis/CDN), search indexes (Elasticsearch/OpenSearch), data-warehouse/analytics copies, message-queue payloads, and object storage (S3/blob).
- Maintain an explicit inventory of where each category is copied; treat the inventory as the cascade checklist and keep it in version control.
- Prefer **event-driven** cascade (emit a `deletion-requested` event; each store subscribes) over a monolithic delete that must know every downstream — this keeps stores decoupled and the design open to new sinks (optimize for change).
- Make cascade steps **idempotent** and retryable; a partially failed cascade **MUST** be detectable and resumable, not silently abandoned.

## Soft vs. hard delete

| Choice | When to use | Caution |
|---|---|---|
| Soft delete (tombstone flag) | Undo windows, referential integrity, short-lived audit needs | Data still present — **MUST NOT** count as erasure for a privacy request |
| Hard delete (row removed) | Erasure requests, PII past retention | Irreversible; verify cascade first |
| Anonymize / pseudonymize | Keep aggregates/analytics without identifying a person | **MUST** be irreversible (no re-identification key retained) |

- Decide soft vs. hard **per category**, not globally. Erasure obligations **MUST** resolve to hard delete or true anonymization within the source and all derived stores.

## Backups and erasure requests

- Backups and immutable logs **SHOULD** be excluded from immediate cascade; instead **document the lag** — deleted data persists until the backup rotates out of its retention window.
- Define and publish a backup retention/purge policy so the maximum lag between an erasure request and full physical removal is bounded and known.
- For an erasure request, suppress the data from active systems immediately and rely on backup rotation for residual copies; **MUST NOT** restore deleted records from an old backup without re-applying pending deletions.

## Auditing

- Log every deletion (who/what/when, category, request reference) to a tamper-evident, separately retained **audit trail** — the log of a deletion is not the deleted data.
- Reconcile periodically: scan for records past their `expires_at` that were not purged, and alert. Treat a reconciliation miss as a defect (fail fast).
