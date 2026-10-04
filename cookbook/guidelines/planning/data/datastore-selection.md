---
id: 6a653107-929d-418e-865d-636373a27b02
title: "Choosing a primary datastore"
domain: agenticdevelopercookbook://guidelines/planning/data/datastore-selection
type: guideline
version: 1.0.1
status: accepted
language: en
created: 2026-06-09
modified: 2026-06-10
author: Mike Fullerton
copyright: 2026 Mike Fullerton
license: MIT
summary: "Default to a relational database for a server backend; adopt a specialist store only for a concrete, measured requirement."
platforms: []
tags:
  - database
  - architecture
  - backend
depends-on: []
related:
  - agenticdevelopercookbook://principles/yagni
  - agenticdevelopercookbook://principles/simplicity
  - agenticdevelopercookbook://guidelines/planning/data/database
references:
  - https://www.postgresql.org/docs/
  - https://www.tigerdata.com/blog/its-2026-just-use-postgres
  - https://news.ycombinator.com/item?id=46905555
  - https://www.cockroachlabs.com/blog/document-store-vs-relational-database/
  - https://aerospike.com/blog/sql-vs-nosql/
approved-by: "approve-artifact v1.0.0"
approved-date: "2026-06-10"
triggers:
  - data-modeling
  - schema-design
---

# Choosing a primary datastore

This guideline governs the **primary datastore for a server backend** — the system of record. It is distinct from the cookbook's embedded/local-storage guidance (e.g., on-device SQLite). Pick the store from data shape, query patterns, and measured scale.

## Strong default

- For a new server backend, the agent **SHOULD** default to a **relational database** (PostgreSQL is the recommended default).
- A **non-relational primary store MUST be justified by a specific, stated requirement** (a query pattern, scale ceiling, or access shape the relational option cannot meet), not by a default preference, hype, or "it scales better."
- Caveat: "just use Postgres" essays are common, but they are **advocacy, not consensus**. Treat the relational default as a strong starting point that a real requirement can override — not as a universal law.

## Why relational is the default

- **One store covers more than it appears.** A modern relational engine absorbs many "specialist" needs in-place: PostgreSQL handles semi-structured data with `jsonb` (and SQL/JSON `JSON_TABLE` as of v17), full-text search, geospatial via PostGIS, and vector similarity via the `pgvector` extension. Reaching for a second engine before exhausting these is premature.
- **Transactions and integrity.** ACID transactions, foreign keys, and constraints are hard to bolt on later and easy to lose with an eventually-consistent store.
- **Optionality (optimize-for-change).** A relational schema with normalized data is the easiest base to migrate *out of* later; a denormalized document model is far harder to reshape.

## Decision criteria

Choose a specialist primary store **only** when a requirement below is concrete and, where possible, measured:

| Need | Signal that justifies it | Candidate store |
|------|--------------------------|-----------------|
| Relational, transactional, mixed queries | Default — entities with relationships, joins, integrity | Relational (Postgres) |
| Schema-fluid documents, per-record variance | Shapes genuinely differ per record AND joins are rare | Document store |
| Simple key lookups, cache, session, ultra-low latency | Access is `get`/`set` by key at high throughput | Key-value store |
| Full-text / faceted search at scale | Relevance ranking, fuzzy match beyond DB full-text | Search engine |
| High-frequency time-stamped writes + time-range queries | Metrics/telemetry/IoT with retention and downsampling | Time-series store |
| Deep multi-hop relationship traversal | Queries are mostly graph walks (friend-of-friend, paths) | Graph store |
| Semantic / embedding similarity | Vector search is core; `pgvector` insufficient at scale | Vector store |

## Rules

- The agent **MUST** record the chosen store and the one-line requirement that justifies it (in an ADR or the plan).
- The agent **MUST NOT** introduce a second datastore "for scale" without a measured limit on the first; YAGNI applies.
- The agent **SHOULD** prefer a single relational store with extensions over polyglot persistence until a specific store earns its operational cost.
- For semi-structured data, the agent **SHOULD** evaluate `jsonb` in the relational store before adopting a separate document database.
- The agent **SHOULD** keep derived stores (search index, cache, vector index) as **secondary** projections of the relational system of record, not as the source of truth.
- When scale is asserted as the reason for a non-relational store, the agent **MUST** cite an expected workload (writes/sec, dataset size, read pattern), not a generic claim.

## Change History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 1.0.1 | 2026-06-10 | Mike Fullerton | Add recovered Tier-1 research sources (adversarially-audited) |
| 1.0.0 | 2026-06-09 | Mike Fullerton | Initial creation |
