
A job worker is a long-running loop that continuously pulls jobs from a backend queue, executes each job through a handler registered for the job's type, renews the job's server-side lease while it works, and reports either a structured result or a retryable failure. It is the platform-agnostic core of a node: the shared business logic, independent of the language it is implemented in. Use it whenever a process must take work from a queue it does not own, tolerate crashes and restarts without losing jobs, and report outcomes with at-least-once semantics.

The ingredient covers the poll-claim loop, lease heartbeat, handler dispatch, result reporting, and the idempotency contract. It does not cover job schema evolution, backend authentication or credential rotation, the backend API itself, or which inference provider a handler uses (see the `llm-backend` ingredient).

### Terminology

| Term | Definition |
|------|-----------|
| Node | A single running instance of the worker |
| Job | A unit of work queued on the backend, identified by a UUID `id` and a string `type` |
| Claim | The act of atomically reserving one or more jobs for exclusive processing |
| Lease | A server-managed time window during which the node has exclusive ownership of a claimed job |
| Heartbeat | A periodic renewal call that extends the current lease |
| Handler | A function registered for a specific job type that accepts a typed payload and returns a typed result |
| Dead-letter | A terminal failure state the backend applies after a job exceeds its max retry attempts |

