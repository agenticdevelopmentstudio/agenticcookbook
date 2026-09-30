<!-- leaf: plan-data/vector-search-and-retrieval · source: guidelines/planning/data/vector-search-and-retrieval.md -->

**Rules** (cite as `plan-data/vector-search-and-retrieval#<slug>`):

- `most-applications-retrieval-live-primary-relational-datastore` SHOULD — For most applications, retrieval SHOULD live in the primary relational datastore via the pgvector extension rather than …
- `managed-ann-service-adopted-only-measured-scale` SHOULD — A separate dedicated vector database (e.g., a managed ANN service) SHOULD be adopted only when measured scale or …
- `you-pin-embedding-model-output` MUST — You MUST pin the embedding model and its output dimension as part of the schema. Mixing vectors from different models …
- `l2-model-specifies-consistent-between-indexing-querying` MUST — Pick the distance operator that matches how the embedding model was trained — cosine (<=>) for most normalized text …
- `ivfflat-used-build-time-memory` MAY — IVFFlat MAY be used when build time and memory dominate and a slight recall hit is acceptable.
- `keyword-matches-teams-use-hybrid-retrieval` SHOULD — The key 2026 nuance: pure approximate-nearest-neighbor (dense vector) search is not enough. Semantic search reliably …
- `reranking-adds-latency-rerank-only-top-20` SHOULD — Reranking adds latency. SHOULD rerank only the top ~20–50 candidates and cache results for repeated queries. The …
- `must` MUST — store, with each chunk, a stable reference back to its source document and position so retrieved context is …
- `tenant-permission-filter-applied-query-time-never` MUST — For multi-tenant or access-controlled data, the tenant/permission filter MUST be applied at query time — never rely on …
- `must-2` MUST — maintain a labeled retrieval eval set and measure recall/precision before and after changes to chunking, indexing, or …
- `should` SHOULD — start with pgvector + hybrid retrieval and only adopt a dedicated vector database when an eval or load test …

# Vector search and retrieval

Vector search is the data layer for the **retrieval** step of RAG (retrieval-augmented generation). This guideline covers how to store embeddings, index them, and retrieve relevant context for an LLM. It assumes the broader datastore choice is settled (see `agenticdevelopercookbook://guidelines/planning/data/datastore-selection`).

## Default to pgvector inside Postgres

For most applications, retrieval **SHOULD** live in the primary relational datastore via the `pgvector` extension rather than a separate vector service.

- Keeping embeddings, source rows, and metadata in **one** transactional store avoids dual-write consistency problems and an extra system to operate (simplicity, yagni).
- A separate dedicated vector database (e.g., a managed ANN service) **SHOULD** be adopted only when measured scale or latency forces it — typically tens of millions of vectors, high write throughput, or strict p99 targets pgvector cannot meet. Treat that migration as a reversible, scale-triggered decision, not a default.
- You **MUST** pin the embedding model and its output dimension as part of the schema. Mixing vectors from different models or dimensions in one column produces meaningless distances.

## Indexing

- Use an **HNSW** index as the default. It gives a better speed/recall tradeoff than IVFFlat and needs no training step; the cost is slower build time and higher memory. (Source: pgvector README, 2026.)
- pgvector HNSW build defaults are `m = 16` and `ef_construction = 64`; the query-time `hnsw.ef_search` default is `40`. Raise `ef_search` to trade latency for recall. Verify current defaults against the pinned pgvector version before relying on them.
- Pick the distance operator that matches how the embedding model was trained — cosine (`<=>`) for most normalized text embeddings, inner product (`<#>`) or L2 (`<->`) when the model specifies it. **MUST** be consistent between indexing and querying.
- IVFFlat **MAY** be used when build time and memory dominate and a slight recall hit is acceptable.

## Prefer hybrid retrieval over pure ANN

The key 2026 nuance: **pure approximate-nearest-neighbor (dense vector) search is not enough.** Semantic search reliably misses exact strings, rare tokens, identifiers, and keyword matches. Teams **SHOULD** use **hybrid retrieval**:

1. **Dense** — vector similarity over embeddings (semantic recall).
2. **Lexical** — keyword/BM25 search over the text (exact and rare-term recall). In Postgres this is full-text search or a BM25 extension.
3. **Fuse** — combine the two ranked lists. Reciprocal Rank Fusion (RRF) is the common default because it merges rankings without needing the two score scales to be comparable.
4. **Rerank** — optionally re-score the fused top-N with a cross-encoder reranker for final precision.

Reranking adds latency. **SHOULD** rerank only the top ~20–50 candidates and cache results for repeated queries. The dense-vs-lexical balance is workload-dependent and contested — treat fusion weights and whether to rerank as things to measure on your own eval set, not as fixed constants.

## Chunking

- Chunk documents before embedding; chunk size and overlap directly determine retrieval quality. There is no universal best size — start with a moderate window with small overlap and tune against a retrieval eval set.
- **MUST** store, with each chunk, a stable reference back to its source document and position so retrieved context is attributable and citable.
- Prefer chunking on semantic/structural boundaries (headings, paragraphs, code blocks) over fixed character counts where the source structure allows it.

## Metadata filtering

- Store filterable attributes (tenant, source, document type, timestamp, access scope) as ordinary columns alongside the vector, and filter on them in the same query.
- For multi-tenant or access-controlled data, the tenant/permission filter **MUST** be applied at query time — never rely on the LLM to ignore retrieved context it should not see (fail-fast, security).

## Verification

- **MUST** maintain a labeled retrieval eval set and measure recall/precision before and after changes to chunking, indexing, or fusion.
- **SHOULD** start with pgvector + hybrid retrieval and only adopt a dedicated vector database when an eval or load test demonstrates pgvector cannot meet the target.
