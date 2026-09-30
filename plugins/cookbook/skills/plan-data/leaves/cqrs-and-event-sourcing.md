<!-- leaf: plan-data/cqrs-and-event-sourcing · source: guidelines/planning/data/cqrs-and-event-sourcing.md -->

**Rules** (cite as `plan-data/cqrs-and-event-sourcing#<slug>`):

- `make-fast-you-not-default-them` MUST — These patterns add real, ongoing complexity. Per yagni and make-it-work-make-it-right-make-it-fast, you MUST NOT …
- `you-justify-adoption-concrete-present` MUST — You MUST justify adoption with a concrete, present requirement — not a forecast that the system "might" need to scale …
- `data-capture-log-evaluated-first-usually-suffices` SHOULD — Default to a single model (CRUD over one datastore). When history is the only driver, an audit/history table or …
- `you-treat-choice-deliberate-documented` MUST — You MUST treat the choice as a deliberate, documented decision (record the triggering requirement), not a mandate or a …
- `trigger-holds-not-adopt-revisit-one-does` MUST — If no trigger holds, MUST NOT adopt; revisit when one does (small-reversible-decisions — CRUD is the cheapest to …
- `idempotency` MUST

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
