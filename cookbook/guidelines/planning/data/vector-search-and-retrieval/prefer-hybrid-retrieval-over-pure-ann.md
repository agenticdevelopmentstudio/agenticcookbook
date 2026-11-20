
1. **Dense** — vector similarity over embeddings (semantic recall).
2. **Lexical** — keyword/BM25 search over the text (exact and rare-term recall). In Postgres this is full-text search or a BM25 extension.
3. **Fuse** — combine the two ranked lists. Reciprocal Rank Fusion (RRF) is the common default because it merges rankings without needing the two score scales to be comparable.
4. **Rerank** — optionally re-score the fused top-N with a cross-encoder reranker for final precision.
