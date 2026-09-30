<!-- leaf: recipes-infrastructure/ai-processing-node · source: recipes/infrastructure/ai-processing-node.md -->

**Rules** (cite as `recipes-infrastructure/ai-processing-node#<slug>`):

- `poll-claim` MUST
- `supported-types-static` MUST
- `loop-continuity` MUST
- `poll-interval` SHOULD
- `lease-heartbeat` MUST
- `lost-lease-abort` MUST
- `heartbeat-stop-on-terminal` MUST
- `run-handler` MUST
- `unknown-type-fail` MUST
- `handler-timeout` MUST
- `complete-on-success` MUST
- `fail-with-backoff` MUST
- `idempotency` MUST
- `llm-backend-selectable` MUST
- `structured-output` MUST
- `schema-constrained-output-rule` MUST (`structured-output`) — the handler MUST pass a JSON Schema (or equivalent structured-output constraint) for the result object when invoking …
- `idempotency-rule` MUST (`idempotency`) — categorizing the same (title, body) pair a second time MUST produce no additional writes if the backend already holds a …

# AI Processing Node

## Overview

An AI processing node is a long-running worker that continuously pulls AI jobs from the `adh` backend, executes each job through a registered handler, renews the job's server-side lease while working, and reports either a structured result or a retryable failure.

This recipe specifies **shared business logic only** — it is intentionally platform-agnostic. Two implementations satisfy it simultaneously: a Swift macOS daemon used as a development node, and a TypeScript service deployed as the production node. Neither implementation language appears in the requirements below; platform-specific guidance lives in [Platform Notes](#platform-notes).

**Scope:** this recipe covers the poll-claim loop, lease heartbeat, handler dispatch, result reporting, idempotency contract, and LLM backend selection. It does not cover job schema evolution, backend authentication/credential rotation, or the backend API itself.

## Terminology

| Term | Definition |
|------|-----------|
| Node | A single running instance of this worker |
| Job | A unit of work queued on the backend, identified by a UUID `id` and a string `type` |
| Claim | The act of atomically reserving one or more jobs for exclusive processing |
| Lease | A server-managed time window during which the node has exclusive ownership of a claimed job |
| Heartbeat | A periodic renewal call that extends the current lease |
| Handler | A function registered for a specific job type that accepts a typed payload and returns a typed result |
| Dead-letter | A terminal failure state the backend applies after a job exceeds its max retry attempts |
| LLM backend | The inference provider a handler uses: a local model server, a hosted API, or a CLI tool |

## Behavioral Requirements

### Poll-Claim Loop

- **poll-claim**: The node MUST claim work by sending a batch claim request to the backend (pull model), passing the set of job types it supports and a maximum batch size. The backend atomically reserves and returns up to that many matching pending jobs. An empty result (zero jobs returned) MUST be treated as a no-op — the loop continues without producing side effects or logging spurious errors.

- **supported-types-static**: The set of job types a node can handle MUST be declared at startup from configuration and MUST NOT change during a run. The node MUST NOT claim a job whose type it cannot handle.

- **loop-continuity**: The poll-claim loop MUST run continuously. A single job failure, a lease loss, or a handler panic MUST NOT terminate the loop; the node logs the incident and continues to the next poll iteration.

- **poll-interval**: Between claim attempts that return zero jobs, the node SHOULD wait a configurable backoff interval (default 5 seconds) before polling again to avoid hammering an idle queue.

### Lease Heartbeat

- **lease-heartbeat**: While processing a claimed job, the node MUST renew the job's lease by sending a heartbeat to the backend at an interval of approximately one-third of the lease duration. The heartbeat interval MUST be derived from the lease duration returned with the claim response, not hardcoded.

- **lost-lease-abort**: If a heartbeat response indicates the lease is no longer valid (expired, stolen, or cancelled), the node MUST stop all work on that job immediately, discard any partial result, and NOT call the complete or fail endpoint. The job will be re-queued by the backend.

- **heartbeat-stop-on-terminal**: The node MUST stop sending heartbeats as soon as it calls complete or fail for a job.

### Handler Dispatch

- **run-handler**: The node MUST dispatch each claimed job to a handler registered for that job's `type` field. The handler receives the job's `payload` deserialized to the handler's declared input type. The dispatch table MUST be populated at startup from registered handlers; runtime registration is not required.

- **unknown-type-fail**: If no handler is registered for a job's `type`, the node MUST immediately report failure with `retryable: false`. The job MUST NOT be retried and MUST be sent to dead-letter by the backend. The node MUST NOT crash or halt the loop.

- **handler-timeout**: Each handler invocation SHOULD be subject to a configurable per-handler timeout. If a handler exceeds its timeout, the node MUST treat the invocation as a handler error (see `fail-with-backoff`).

### Result Reporting

- **complete-on-success**: On handler success, the node MUST report job completion to the backend, passing the handler's structured result as the job result payload. The node MUST wait for the backend's acknowledgement before releasing the job from local tracking.

- **fail-with-backoff**: On handler error (exception, timeout, or non-recoverable condition), the node MUST report job failure to the backend with `retryable: true`. The backend is solely responsible for applying exponential backoff and enforcing the max-attempts dead-letter policy; the node MUST NOT implement retry logic locally. One failing job MUST NOT halt the poll-claim loop.

### Idempotency

- **idempotency**: Handlers MUST be safe to run more than once for the same job ID and target (leases can expire mid-run and the same job may be re-claimed by any node). A handler MUST produce no duplicate side effects on repeated invocation — if the operation was already applied, the handler MUST detect this and return the same result without re-applying. Calling complete or fail for a job that has already reached a terminal state MUST be accepted gracefully; the node MUST NOT treat such a response as an error.

### LLM Backend

- **llm-backend-selectable**: The node MUST support selecting which LLM backend executes a handler's inference step via configuration (e.g., an environment variable or config file), with no code changes required to switch. Supported backend kinds include at minimum: an OpenAI-compatible HTTP API endpoint (local model server or hosted), and a CLI-based inference tool invoked as a subprocess.

- **structured-output**: Handlers that invoke the LLM MUST request schema-constrained (structured) output from the backend rather than parsing free-form text. The output schema MUST be defined per handler and validated before the handler returns its result.

## The `categorize_and_tag` Handler

This is the primary concrete handler shipped with the node. It categorizes and tags a piece of content using the configured LLM backend.

### Input (job payload)

```json
{
  "title": "string",
  "body":  "string"
}
```

### Output (job result)

```json
{
  "category":   "string",
  "tags":       ["string"],
  "confidence": 0.0
}
```

| Field | Required | Description |
|-------|----------|-------------|
| `category` | Yes | The single best-fit category string. The backend maps this to its categories store. |
| `tags` | Yes | Zero or more keyword strings. The backend maps these to its keywords store. |
| `confidence` | No | Advisory float in [0,1] expressing the LLM's self-reported confidence. The backend treats this as informational only. |

**Schema-constrained output rule** (`structured-output`): the handler MUST pass a JSON Schema (or equivalent structured-output constraint) for the result object when invoking the LLM. It MUST NOT parse category or tags from free-form text.

**Idempotency rule** (`idempotency`): categorizing the same `(title, body)` pair a second time MUST produce no additional writes if the backend already holds a result for this job ID.

## Integration Test Vectors

| ID | Requirements | Input | Expected |
|----|-------------|-------|----------|
| `apn-001` | `poll-claim`, `run-handler`, `complete-on-success` | Backend queue contains one `categorize_and_tag` job with `{ "title": "How to prune roses", "body": "..." }` | Node claims the job, handler executes, node calls complete with `{ category, tags, confidence? }`, job moves to done state on backend |
| `apn-002` | `run-handler`, `fail-with-backoff`, `loop-continuity` | Handler for `categorize_and_tag` throws an unrecoverable error | Node calls fail with `retryable: true`; loop continues; next poll iteration proceeds normally |
| `apn-003` | `unknown-type-fail` | Backend queue contains a job with `type: "transcribe_audio"` and node has no handler for that type | Node immediately calls fail with `retryable: false`; job goes to dead-letter; loop continues |
| `apn-004` | `lease-heartbeat`, `complete-on-success` | Handler takes longer than one heartbeat interval (e.g., 40s LLM call on a 30s lease) | At least one heartbeat is sent before the complete call; job lease remains valid throughout; complete succeeds |
| `apn-005` | `idempotency` | Same job is claimed twice (simulated lease expiry mid-run); handler completes on the second claim | Backend result is identical to first completion; no duplicate category or tag entries created |
| `apn-006` | `poll-claim`, `loop-continuity` | Backend queue is empty | Claim returns zero jobs; no complete/fail calls made; loop waits the poll interval and polls again |
| `apn-007` | `lost-lease-abort` | Heartbeat response returns lease-invalid (e.g. 409 Conflict) mid-handler | Node cancels handler execution, does NOT call complete or fail, logs lease loss, continues loop |

