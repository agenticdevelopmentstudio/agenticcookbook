
- `must-not-store-computed-values`: Computed columns become stale and require maintenance triggers.
- `should-not-store-lists-in-a-column`: A comma-separated list of IDs in a single column is a normalization violation.
- `must-maintain-denormalized-column-via-trigger`, `must-include-denormalized-column-in-sync-payloads`, `should-treat-normalized-source-as-authoritative`, `should-prefer-denormalizing-stable-data`: Denormalization in a sync-capable schema puts a redundant copy on every device and on the server, so each copy needs a trigger to keep it, a sync payload to carry it and a normalized source to be checked against.

