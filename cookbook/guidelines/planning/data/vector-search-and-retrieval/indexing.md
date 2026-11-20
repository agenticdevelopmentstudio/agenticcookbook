
- pgvector HNSW build defaults are `m = 16` and `ef_construction = 64`; the query-time `hnsw.ef_search` default is `40`.
- Distance operators: cosine (`<=>`) for most normalized text embeddings, inner product (`<#>`) or L2 (`<->`) when the model specifies it.
