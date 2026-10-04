
Adopt **CQRS** when one of these is concretely true:

- Read and write workloads have **sharply divergent scaling or shape** — e.g., heavy denormalized read fan-out vs. low-volume transactional writes — and you have measured (or contractually know) the imbalance.
- The read side needs **independent storage or indexing** (search engine, cache, materialized view) that the write model cannot serve efficiently.

Adopt **event sourcing** when one of these is concretely true:

- You have a **replay/audit requirement**: a regulatory, debugging, or temporal-query need to reconstruct exactly how state reached its current value (e.g., finance, ledgers).
- You need to **derive new read models retroactively** from past behavior that was not captured at write time.

If no trigger holds, **MUST NOT** adopt; revisit when one does (`small-reversible-decisions` — CRUD is the cheapest to reverse from).

