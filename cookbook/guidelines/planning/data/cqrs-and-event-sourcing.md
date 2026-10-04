---
id: b5a1b4b6-c61c-4b45-825f-730bd782d0f3
title: "CQRS and event sourcing"
domain: agenticdevelopercookbook://guidelines/planning/data/cqrs-and-event-sourcing
type: guideline
version: 1.0.1
status: accepted
language: en
created: 2026-06-09
modified: 2026-06-10
author: Mike Fullerton
copyright: 2026 Mike Fullerton
license: MIT
summary: "Adopt CQRS or event sourcing ONLY when audit/replay or independent read/write scaling justifies their substantial complexity cost."
platforms: []
tags:
  - architecture
  - cqrs
  - event-sourcing
depends-on: []
related:
  - agenticdevelopercookbook://guidelines/planning/data/datastore-selection
  - agenticdevelopercookbook://principles/manage-complexity-through-boundaries
references:
  - https://martinfowler.com/bliki/CQRS.html
  - https://microservices.io/patterns/data/event-sourcing.html
  - https://www.usefulfunctions.co.uk/2025/11/06/cqrs-and-event-sourcing-when-to-use/
  - https://www.ashrafmageed.com/cqrs-eventsourcing-and-the-cost-of-tooling-constraints/
approved-by: "approve-artifact v1.0.0"
approved-date: "2026-06-10"
triggers:
  - data-modeling
  - schema-design
---

# CQRS and event sourcing

CQRS (Command Query Responsibility Segregation) splits the write model (commands that mutate state) from the read model (queries that return data), letting each evolve and scale separately. Event sourcing stores state as an append-only log of immutable events; current state is derived by replaying or projecting those events into read models. They are independent patterns that are often, but not necessarily, combined.

## MEASURED-NEED guardrail (strong)

These patterns add real, ongoing complexity. Per `yagni` and `make-it-work-make-it-right-make-it-fast`, you **MUST NOT** default to them.

- You **MUST** justify adoption with a concrete, present requirement — not a forecast that the system "might" need to scale or "might" want history later.
- Default to a single model (CRUD over one datastore). When history is the only driver, an audit/history table or change-data-capture log **SHOULD** be evaluated first and usually suffices.
- You **MUST** treat the choice as a deliberate, documented decision (record the triggering requirement), not a mandate or a resume-driven default.

## Adopt ONLY when a trigger holds

Adopt **CQRS** when one of these is concretely true:

- Read and write workloads have **sharply divergent scaling or shape** — e.g., heavy denormalized read fan-out vs. low-volume transactional writes — and you have measured (or contractually know) the imbalance.
- The read side needs **independent storage or indexing** (search engine, cache, materialized view) that the write model cannot serve efficiently.

Adopt **event sourcing** when one of these is concretely true:

- You have a **replay/audit requirement**: a regulatory, debugging, or temporal-query need to reconstruct exactly how state reached its current value (e.g., finance, ledgers).
- You need to **derive new read models retroactively** from past behavior that was not captured at write time.

If no trigger holds, **MUST NOT** adopt; revisit when one does (`small-reversible-decisions` — CRUD is the cheapest to reverse from).

## Costs you take on (plan for each before adopting)

| Cost | What it requires |
|------|------------------|
| Eventual consistency | Read models lag writes; UI/API **MUST** tolerate the delay (optimistic update, loading state, or read-your-writes routing). |
| Projection rebuilds | A documented, tested procedure to rebuild read models from the log; **MUST** be runnable without downtime for large stores. |
| Event versioning | Events are immutable once written; you **MUST** have an upcasting/versioning plan before the first event ships — schema changes are not retroactive edits. |
| Operational surface | Command handlers, event store, projectors, and read stores each add deployment, monitoring, and failure modes (`manage-complexity-through-boundaries`). |

## Implementation guidance (when justified)

- **explicit-over-implicit**: model commands and events as named, versioned types; never overload one generic "update" event.
- **idempotency**: command handlers and projectors **MUST** be idempotent — events may be redelivered; dedupe on a stable event id.
- Keep CQRS **without** event sourcing as a valid stopping point: separating read/write models in one database is far cheaper than a full event store, and often enough.
- Start in-process and single-store; introduce separate read stores or message infrastructure **only** when the triggering requirement demands it.
- Define the consistency contract per use case (which reads may be stale, which must be strongly consistent) and surface it in the API.

## Change History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 1.0.1 | 2026-06-10 | Mike Fullerton | Add recovered Tier-1 research sources (adversarially-audited) |
| 1.0.0 | 2026-06-09 | Mike Fullerton | Initial creation |
