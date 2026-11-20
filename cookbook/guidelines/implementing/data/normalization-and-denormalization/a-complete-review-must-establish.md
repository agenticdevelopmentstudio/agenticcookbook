
- Schema design starts from 3NF baseline; normalization violations documented if intentional
- Any denormalized data justified by measured query performance bottleneck (benchmark provided, not assumed)
- Denormalization maintenance strategy documented: triggers for automatic sync, or explicit application logic for batch updates
- Denormalized data never used for primary filtering (query logic doesn't depend on correctness of denormalized values)
- If column is denormalized, single source of truth identified (original table where it can be reconstructed)
- For synced tables: denormalization strategy compatible with sync direction and frequency
- Triggers used to maintain denormalized data are wrapped in transaction and tested
- No "just in case" denormalization; measure the query before denormalizing
- Every MUST rule is kept, with no exception: `must-denormalize-only-when-measured-read-heavy-and-synced`, `must-propagate-source-writes-to-denormalized-copies`, `must-maintain-denormalized-column-via-trigger`, `must-include-denormalized-column-in-sync-payloads`, `must-not-store-computed-values`
- Every SHOULD rule is kept, or the change says why not: `should-start-at-3nf`, `should-prefer-normalized-unless-benchmarked`, `should-treat-normalized-source-as-authoritative`, `should-prefer-denormalizing-stable-data`, `should-not-store-narratives-in-columns`, `should-not-store-lists-in-a-column`


A review passes when it establishes every item above.
