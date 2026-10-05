---
id: 22FBF585-C5A3-425A-94F1-BA9B570EBFDE
title: "Job Worker"
domain: agenticdevelopercookbook://ingredients/infrastructure/job-worker
type: ingredient
version: 1.0.0
status: review
language: en
created: 2026-10-04
modified: 2026-10-04
author: Mike Fullerton
copyright: 2026 Mike Fullerton
license: MIT
summary: "Pull-model job worker loop that claims typed jobs from a backend, renews leases with heartbeats, dispatches to handlers, and reports results with at-least-once idempotency"
platforms:
  - swift
  - typescript
tags:
  - infrastructure
  - ai-jobs
  - worker
  - polling
depends-on: []
related:
  - agenticdevelopercookbook://recipes/infrastructure/ai-processing-node
  - agenticdevelopercookbook://ingredients/infrastructure/logging
references:
  - https://datatracker.ietf.org/doc/html/rfc2119
approved-by: "approve-artifact v1.1.0"
approved-date: "2026-10-04"
---

# Job Worker

## Overview

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

## Appearance

Not applicable — a job worker is a headless background process with no visual surface.

## States

| State | Behavior |
|-------|----------|
| Idle | A claim returned zero jobs; the node waits the poll interval and polls again |
| Claiming | A batch claim request is in flight to the backend |
| Processing | A job is claimed, its handler is running, and its heartbeat is active |
| Reporting | The handler finished; the node is calling complete or fail and the heartbeat has stopped |
| Lease lost | A heartbeat indicated the lease is invalid; work on the job is cancelled and nothing is reported |

## Accessibility

Not applicable — a job worker has no user-facing surface. Operators observe it through logs and backend job state.

## Conformance Test Vectors

| ID | Requirements | Input | Expected |
|----|-------------|-------|----------|
| job-worker-001 | poll-claim, run-handler, complete-on-success | Queue contains one job of a supported type with a valid payload | Node claims the job, the handler executes, node calls complete with the handler's result, job moves to done state on the backend |
| job-worker-002 | run-handler, fail-with-backoff, loop-continuity | The handler throws an unrecoverable error | Node calls fail with `retryable: true`; loop continues; next poll iteration proceeds normally |
| job-worker-003 | unknown-type-fail | Queue contains a job whose type has no registered handler | Node immediately calls fail with `retryable: false`; job goes to dead-letter; loop continues |
| job-worker-004 | lease-heartbeat, complete-on-success | Handler takes longer than one heartbeat interval (e.g., 40s call on a 30s lease) | At least one heartbeat is sent before the complete call; the lease remains valid throughout; complete succeeds |
| job-worker-005 | idempotency | Same job is claimed twice (simulated lease expiry mid-run); handler completes on the second claim | Backend result is identical to the first completion; no duplicate side effects are created |
| job-worker-006 | poll-claim, loop-continuity, poll-interval | Backend queue is empty | Claim returns zero jobs; no complete or fail calls are made; loop waits the poll interval and polls again |
| job-worker-007 | lost-lease-abort | Heartbeat response returns lease-invalid (e.g., 409 Conflict) mid-handler | Node cancels handler execution, does NOT call complete or fail, logs lease loss, continues loop |
| job-worker-008 | handler-timeout, fail-with-backoff | Handler exceeds its configured timeout | Invocation is treated as a handler error; node calls fail with `retryable: true` |
| job-worker-009 | heartbeat-stop-on-terminal | Handler completes and node calls complete | No heartbeat is sent after the terminal call |
| job-worker-010 | supported-types-static | Backend holds jobs of types the node does not list in its configuration | Node's claim request names only its configured types; those jobs are never claimed |

## Edge Cases

- **Network partition during complete**: If the complete or fail call fails with a transient network error, the node SHOULD retry that specific HTTP call with limited exponential backoff before giving up. Abandoning without reporting is preferable to a tight retry storm; the job will eventually be re-queued when the lease expires.
- **Handler returns before first heartbeat interval**: The heartbeat timer MUST be cancelled before calling complete so no heartbeat fires after the terminal call.
- **Startup with empty handler registry**: The node MUST log a warning and start normally; it will claim no jobs (no supported types), poll an empty result, and idle.
- **Clock skew between node and backend**: The heartbeat interval MUST be derived from the backend-reported lease duration, not the node's wall clock, to tolerate moderate skew.
- **Large batch with mixed types**: The node SHOULD process jobs in the batch concurrently up to a configurable concurrency limit, with each job's heartbeat running independently.
- **Terminal state already reached**: A complete or fail call that the backend answers with "already terminal" is accepted without error (see `idempotency`).

## Configuration

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `supportedJobTypes` | string[] | (required) | Job types the node claims; fixed for the life of the process |
| `batchSize` | integer | 1 | Maximum jobs requested per claim |
| `pollIntervalSeconds` | number | 5 | Wait between claims that return zero jobs |
| `handlerTimeoutSeconds` | number | (none) | Per-handler timeout; unset means no timeout |
| `concurrency` | integer | 1 | Maximum jobs processed at once from a batch |

## Logging

Subsystem: `{{bundle_id}}` | Category: `JobWorker`

| Event | Level | Message |
|-------|-------|---------|
| Node started | info | `JobWorker: started with {{handlerCount}} handlers for types {{types}}` |
| Empty registry | warning | `JobWorker: no handlers registered, node will idle` |
| Claim returned jobs | debug | `JobWorker: claimed {{count}} jobs` |
| Claim returned none | debug | `JobWorker: no jobs, waiting {{seconds}}s` |
| Job completed | info | `JobWorker: job {{jobId}} completed in {{duration}}s` |
| Job failed | warning | `JobWorker: job {{jobId}} failed (retryable={{retryable}}): {{error}}` |
| Lease lost | warning | `JobWorker: lease lost for job {{jobId}}, work aborted` |
| Unknown type | error | `JobWorker: no handler for type "{{type}}" (job {{jobId}})` |
| Report retry | warning | `JobWorker: retrying {{endpoint}} for job {{jobId}} after {{error}}` |

## Platform Notes

SwiftUI, Compose, and React/Web do not apply: a job worker has no view layer. Two implementations satisfy this ingredient simultaneously.

### Swift macOS Daemon (Development Node)

- Implemented as a launchd-managed background process (`launchd` plist, `KeepAlive: true`).
- The poll-claim loop runs on a dedicated `Task` (Swift Concurrency). Each job is processed in its own child `Task`, bounded by a `TaskGroup` limited to the configured concurrency ceiling.
- Lease heartbeat: a `Task` that loops `try await Task.sleep(for: heartbeatInterval)` until cancelled. Cancel it by calling `.cancel()` on the heartbeat task before reporting complete or fail.
- Logging: use `os.Logger` with subsystem `com.adh.node` and category per handler.

### TypeScript Service (Production Node)

- Implemented as a Node.js long-running process, containerized and managed by the deployment platform (e.g., Docker / Kubernetes Deployment).
- The poll-claim loop runs as an `async` loop with `await`-based polling. Each job is dispatched to a `Promise`-based handler; a `p-limit` semaphore or equivalent caps concurrency.
- Lease heartbeat: a `setInterval` timer started immediately after claim, cleared in a `finally` block that fires whether complete, fail, or error terminates the handler.
- Logging: structured JSON to stdout (`pino` or equivalent), consumed by the deployment platform's log aggregator.

## Design Decisions

**Decision**: Pull model (node polls for jobs) rather than push model (backend pushes to node).
**Rationale**: Pull tolerates node restarts without message loss, scales horizontally without a broker, and lets each node self-throttle by controlling its batch size. At the scale of a development or small production node, the polling overhead is negligible.
**Approved**: pending

**Decision**: Lease + heartbeat rather than a one-shot acknowledgement.
**Rationale**: Long-running LLM inference can take tens of seconds to minutes. A one-shot ack with no keepalive would require the backend to set an unrealistically long timeout or risk never detecting a crashed node. Heartbeats let the backend detect node loss in one heartbeat interval.
**Approved**: pending

**Decision**: Heartbeat interval is one-third of the lease duration (not one-half or fixed).
**Rationale**: One-third gives two missed heartbeats before the lease expires, tolerating transient network hiccups without prematurely losing the lease. One-half leaves only one miss, which is too tight; fixed intervals couple the node to backend config.
**Approved**: pending

**Decision**: `retryable: false` on unknown job type (immediate dead-letter).
**Rationale**: An unknown type means no handler will ever exist on this node for that job. Retrying would exhaust the max-attempts counter with no chance of success and delay the operator seeing the misconfiguration. Dead-letter with a clear error is faster feedback.
**Approved**: pending

**Decision**: Idempotency is a handler contract, not enforced by the node framework.
**Rationale**: Only the handler knows what constitutes a duplicate side effect for its domain. The node framework can detect a duplicate job ID (already in terminal state on the backend) and skip re-running, but fine-grained deduplication (e.g., "did I already write this category?") requires handler-level logic.
**Approved**: pending

## Compliance

| Check | Status | Category |
|-------|--------|----------|
| [idempotent-operations](agenticdevelopercookbook://compliance/reliability#idempotent-operations) | partial | Reliability |
| [fault-tolerance](agenticdevelopercookbook://compliance/reliability#fault-tolerance) | partial | Reliability |
| [secure-log-output](agenticdevelopercookbook://compliance/security#secure-log-output) | partial | Security |

> Status is `partial`: this ingredient specifies the requirements that satisfy these checks, but compliance is verified per concrete worker implementation, not at the ingredient level.

## Change History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 1.0.0 | 2026-10-04 | Mike Fullerton | Extracted from the AI Processing Node recipe |
