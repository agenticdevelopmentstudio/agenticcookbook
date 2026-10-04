---
id: 8a1d8274-cc46-4449-a824-7c7a79c0b1e2
title: "Advanced database indexing"
domain: agenticdevelopercookbook://guidelines/implementing/data/advanced-indexing
type: guideline
version: 1.0.0
status: accepted
language: en
created: 2026-06-09
modified: 2026-06-09
author: Mike Fullerton
copyright: 2026 Mike Fullerton
license: MIT
summary: "Match the Postgres index type to the access pattern, build on live tables with CONCURRENTLY, and validate with EXPLAIN ANALYZE."
platforms: []
tags:
  - database
  - indexing
  - postgres
depends-on: []
related:
  - agenticdevelopercookbook://guidelines/implementing/data/transaction-isolation
  - agenticdevelopercookbook://guidelines/implementing/data/query-optimization
references:
  - https://www.postgresql.org/docs/current/indexes.html
approved-by: "approve-artifact v1.0.0"
approved-date: "2026-06-09"
triggers:
  - database-operations
  - performance-optimization
---

# Advanced database indexing

An index is a deliberate trade: faster reads for slower writes and more storage. Add one only when a measured query needs it, pick the type that matches the access pattern, and prove the gain with `EXPLAIN (ANALYZE, BUFFERS)`. Examples below assume PostgreSQL 16/17; pin behavior to your server's version.

## Build safely on live tables

- **concurrent-build**: Indexes on large live tables **MUST** be created with `CREATE INDEX CONCURRENTLY` so writes are not blocked by a long `ACCESS EXCLUSIVE` lock. It runs slower and cannot run inside a transaction block.
- **failed-index-cleanup**: A `CONCURRENTLY` build that fails leaves an `INVALID` index. The author **MUST** detect it (`pg_index.indisvalid = false`) and `DROP INDEX CONCURRENTLY` before retrying.
- **rebuild-without-lock**: To rebuild a bloated index, you **SHOULD** use `REINDEX INDEX CONCURRENTLY` rather than drop-and-recreate, preserving query coverage throughout.

## Choose the type by access pattern

- **type-matches-query**: The index type **SHOULD** match how the column is queried, not default to B-tree reflexively:

| Type | Use when | Notes |
|------|----------|-------|
| B-tree | Equality, ranges, `ORDER BY`, `=`/`<`/`>`/`BETWEEN` | The default; supports unique constraints and sorted output |
| GIN | JSONB containment, arrays, full-text (`tsvector`) | Multiple keys per row; expensive to maintain on write-heavy columns |
| GiST | Ranges, geometry, nearest-neighbor, exclusion constraints | Lossy; basis for PostGIS and `tstzrange` overlap |
| BRIN | Very large, naturally-ordered or append-only tables | Stores per-block min/max; tiny and cheap, but only helps correlated data |
| Hash | Equality only | Rarely worth it over B-tree; no range or ordering support |

## Targeted index shapes

- **partial-index**: When queries filter on a stable predicate (e.g. `WHERE status = 'active'`), a partial index (`CREATE INDEX ... WHERE status = 'active'`) **SHOULD** be used to shrink the index and skip indexing irrelevant rows.
- **expression-index**: When a query filters on a computed value (`lower(email)`, `(payload->>'tenant')`), the author **MUST** index the matching expression — a plain column index will not be used.
- **composite-column-order**: In a multi-column B-tree, columns **MUST** be ordered most-selective-and-equality-first; the leading column(s) must appear in the predicate for the index to apply.
- **covering-index**: To enable index-only scans for hot read paths, you **MAY** add `INCLUDE (...)` columns so the heap is not visited; confirm the gain with `EXPLAIN` showing `Index Only Scan`.

## Indexing JSONB

- **jsonb-gin**: For containment queries (`@>`, key existence) on JSONB, a GIN index **SHOULD** be used.
- **jsonb-path-ops**: When only containment (`@>`) is needed, the `jsonb_path_ops` operator class **SHOULD** be preferred — it produces a smaller, faster index than the default `jsonb_ops` at the cost of dropping key-existence operators (`?`, `?|`, `?&`).
- **jsonb-write-cost**: GIN maintenance decomposes the whole document on every write, which can materially reduce insert throughput on write-heavy JSONB columns. The author **SHOULD** measure write impact before adding one, and **SHOULD** prefer an expression index on a single extracted scalar key when that is all queries need.

## Validate, then keep honest

- **explain-before-after**: Every new index **MUST** be justified by `EXPLAIN (ANALYZE, BUFFERS)` showing the planner uses it and the cost drops; a created-but-unused index is pure write overhead.
- **drop-unused**: Indexes with near-zero scans in `pg_stat_user_indexes.idx_scan` over a representative window **SHOULD** be dropped.
- **measured-need**: Specialized strategies — BRIN on huge append-only tables, table partitioning, custom operator classes — are adopt-only-when-a-concrete-measured-need-justifies-it, not defaults (YAGNI; make-it-work, make-it-right, make-it-fast).

## Change History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 1.0.0 | 2026-06-09 | Mike Fullerton | Initial creation |
