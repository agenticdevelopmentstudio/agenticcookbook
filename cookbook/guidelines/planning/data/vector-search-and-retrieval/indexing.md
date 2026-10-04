
- Use an **HNSW** index as the default. It gives a better speed/recall tradeoff than IVFFlat and needs no training step; the cost is slower build time and higher memory. (Source: pgvector README, 2026.)
- pgvector HNSW build defaults are `m = 16` and `ef_construction = 64`; the query-time `hnsw.ef_search` default is `40`. Raise `ef_search` to trade latency for recall. Verify current defaults against the pinned pgvector version before relying on them.
- Pick the distance operator that matches how the embedding model was trained — cosine (`<=>`) for most normalized text embeddings, inner product (`<#>`) or L2 (`<->`) when the model specifies it. **MUST** be consistent between indexing and querying.
- IVFFlat **MAY** be used when build time and memory dominate and a slight recall hit is acceptable.

