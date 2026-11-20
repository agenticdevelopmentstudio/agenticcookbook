
- **rate-metric**: Each service **MUST** emit request rate as a counter (requests over time), labeled by route/operation.
- **errors-metric**: Each service **MUST** emit a count of failed requests as a separate counter (or as an `error`/`status` label on the rate counter) so error ratio is computable.
- **duration-metric**: Each service **MUST** emit request duration as a histogram (not just a mean) so percentiles (p50/p95/p99) are derivable; means hide tail latency.
- **error-definition**: Each service **MUST** document what counts as an error (e.g., HTTP 5xx, gRPC non-OK, business-level failure) — error ratio is meaningless without an explicit definition.
- **cardinality-limit**: Labels **MUST NOT** include unbounded values (raw user IDs, full URLs, request bodies). Use bounded route templates (`/users/{id}`, not `/users/42`) to keep time-series cardinality manageable.

