
- **One store covers more than it appears.** A modern relational engine absorbs many "specialist" needs in-place: PostgreSQL handles semi-structured data with `jsonb` (and SQL/JSON `JSON_TABLE` as of v17), full-text search, geospatial via PostGIS, and vector similarity via the `pgvector` extension. Reaching for a second engine before exhausting these is premature.
- **Transactions and integrity.** ACID transactions, foreign keys, and constraints are hard to bolt on later and easy to lose with an eventually-consistent store.
- **Optionality (optimize-for-change).** A relational schema with normalized data is the easiest base to migrate *out of* later; a denormalized document model is far harder to reshape.

