
- Schema design starts from 3NF baseline; normalization violations documented if intentional
- Any denormalized data justified by measured query performance bottleneck (benchmark provided, not assumed)
- Denormalization maintenance strategy documented: triggers for automatic sync, or explicit application logic for batch updates
- Denormalized data never used for primary filtering (query logic doesn't depend on correctness of denormalized values)
- If column is denormalized, single source of truth identified (original table where it can be reconstructed)
- For synced tables: denormalization strategy compatible with sync direction and frequency
- Triggers used to maintain denormalized data are wrapped in transaction and tested
- No "just in case" denormalization; measure the query before denormalizing

