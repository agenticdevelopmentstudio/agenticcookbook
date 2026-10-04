
- A request crossing a service boundary **SHOULD** propagate W3C Trace Context: the `traceparent` header (and `tracestate` when present). This is the W3C Trace Context Recommendation (Level 1, dated 6 February 2020). *Level 2 is a Candidate Recommendation Draft as of 2026 — treat its additions as a forecast and pin to Level 1 for interop.*
- Header names **MUST** be treated as ASCII case-insensitive; emit `traceparent` in lowercase.
- Services **MUST NOT** drop an incoming `traceparent`; continue the trace instead of starting a new root, or the trace fragments.
- Inject and extract context at the transport edge (middleware/interceptors), not scattered through business logic.

### Async and messaging boundaries

- Trace context **MUST** travel with the message, not just synchronous calls — inject `traceparent` into message/event metadata when publishing.
- For queues, pub/sub, and event streams, the consumer span **SHOULD** use a **span link** to the producer rather than a parent-child edge. A single message may fan out to many consumers, and processing is often decoupled in time; links express that causal-but-not-nested relationship.

