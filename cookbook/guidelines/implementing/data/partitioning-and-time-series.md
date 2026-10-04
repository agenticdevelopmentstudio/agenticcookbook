---
id: 2b9b576c-1e17-4a15-b347-febf2ea3c312
title: "Table partitioning and time-series data"
domain: agenticdevelopercookbook://guidelines/implementing/data/partitioning-and-time-series
type: guideline
version: 1.0.0
status: accepted
language: en
created: 2026-06-09
modified: 2026-06-09
author: Mike Fullerton
copyright: 2026 Mike Fullerton
license: MIT
summary: "Partition large tables only when a measured size or retention need justifies the operational cost, and apply time-series patterns deliberately."
platforms: []
tags:
  - database
  - partitioning
  - time-series
depends-on: []
related:
  - agenticdevelopercookbook://guidelines/implementing/data/advanced-indexing
references:
  - https://www.postgresql.org/docs/current/ddl-partitioning.html
approved-by: "approve-artifact v1.0.0"
approved-date: "2026-06-09"
triggers:
  - database-operations
  - schema-design
---

# Table partitioning and time-series data

Partitioning splits one logical table into physical child partitions so the planner can prune irrelevant data and you can drop whole partitions cheaply. It adds real operational complexity, so treat it as a measured-need optimization, not a default.

## When to partition (measured-need guardrail)

Per **YAGNI** and **make-it-work-make-it-right-make-it-fast**, do NOT partition by default. A normal indexed table serves most workloads.

- You **MUST** justify partitioning with a concrete, measured need — typically a table at real scale (commonly cited thresholds: tens of millions of rows or roughly 50-100 GB; treat these as rules of thumb, not hard limits — verify against your workload) **or** a retention requirement where you periodically purge old data.
- You **SHOULD** confirm the win with `EXPLAIN (ANALYZE)` before and after: partitioning helps only when queries filter on the partition key so the planner prunes partitions.
- You **SHOULD NOT** create partitions smaller than ~10k rows or accumulate thousands of partitions; both add planning overhead. Aim for a few dozen to a few hundred partitions.

## Choosing a partition strategy

PostgreSQL declarative partitioning (PostgreSQL 10+; mature in 14-18) supports three kinds. You **MUST** partition on column(s) that appear in the WHERE clause of hot queries, or pruning cannot fire.

| Strategy | Use when | Example key |
|----------|----------|-------------|
| RANGE | Time-series, sequential IDs, retention by window | `created_at` per month |
| LIST | Discrete categories with bounded cardinality | `region`, `tenant_id` |
| HASH | Even spread with no natural range/list key | `user_id` mod N |

- You **SHOULD** prefer native declarative partitioning over legacy inheritance + triggers.
- You **MUST** include the partition key in primary keys and unique constraints (a PostgreSQL constraint).

## Time-series patterns

- **Range partition by time** (e.g. one partition per day/week/month sized so each holds a workable row count).
- **Retention by dropping partitions**: `DROP TABLE`/`DETACH PARTITION` on an old partition is near-instant and reclaims space, unlike a bulk `DELETE` that bloats the table and stresses autovacuum. You **SHOULD** automate partition creation and dropping (e.g. `pg_partman`).
- **BRIN indexes** on the time column suit naturally-ordered append-only data and are far smaller than B-tree; you **SHOULD** evaluate BRIN for large time-ordered partitions.
- **Rollups / continuous aggregates**: precompute summaries for queries spanning long history instead of scanning raw rows. Plain materialized views require manual refresh; some extensions refresh incrementally.

## Extension vs. native (a deliberate decision)

A time-series extension (e.g. TimescaleDB/TigerData) automates chunking, retention, columnar compression, and incrementally-maintained aggregates. This is a deliberate trade-off, not a mandate.

- You **SHOULD** stay on native partitioning when its capabilities suffice — fewer operational dependencies.
- You **MAY** adopt an extension ONLY when a measured need (compression ratio, automated lifecycle, query speedup on large history) justifies the added dependency and operational surface.

> FORECAST / version-sensitive: PostgreSQL partition-pruning behavior and extension feature sets evolve per release. Pin to your deployed major version and re-verify `EXPLAIN` plans after upgrades. Specifics above reflect PostgreSQL 18-era docs (current as of 2026-06).

## Change History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 1.0.0 | 2026-06-09 | Mike Fullerton | Initial creation |
