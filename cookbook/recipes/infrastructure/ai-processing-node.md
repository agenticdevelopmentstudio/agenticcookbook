---
id: 61ca76a4-0188-488b-9ac6-1144ca8ed506
title: "AI Processing Node"
domain: agenticdevelopercookbook://recipes/infrastructure/ai-processing-node
type: recipe
version: 2.0.0
status: review
language: en
created: 2026-06-28
modified: 2026-10-04
author: Mike Fullerton
copyright: 2026 Mike Fullerton
license: MIT
summary: "Platform-agnostic spec for a pull-model AI job worker that claims jobs from the adh backend, runs handlers, renews leases, and reports results with at-least-once idempotency."
platforms:
  - macos
  - swift
  - typescript
tags:
  - infrastructure
  - ai-jobs
  - worker
  - polling
ingredients:
  - agenticdevelopercookbook://ingredients/infrastructure/job-worker
  - agenticdevelopercookbook://ingredients/infrastructure/llm-backend
  - agenticdevelopercookbook://ingredients/infrastructure/categorize-and-tag-handler
depends-on: []
related:
  - agenticdevelopercookbook://recipes/infrastructure/directory-sync
references:
  - https://datatracker.ietf.org/doc/html/rfc2119
approved-by: "approve-artifact v1.1.0"
approved-date: "2026-10-04"
---

# AI Processing Node

## Overview

An AI processing node is a long-running worker that continuously pulls AI jobs from the `adh` backend, executes each job through a registered handler, renews the job's server-side lease while working, and reports either a structured result or a retryable failure. This recipe composes three ingredients: the job worker (poll-claim loop, lease heartbeat, handler dispatch, result reporting, idempotency), the LLM backend (configuration-selected inference with schema-constrained output), and the `categorize_and_tag` handler (the primary concrete handler).

This recipe specifies **shared business logic only** — it is intentionally platform-agnostic. Two implementations satisfy it simultaneously: a Swift macOS daemon used as a development node, and a TypeScript service deployed as the production node. Neither implementation language appears in the requirements below; platform-specific guidance lives in [Platform Notes](#platform-notes).

**Scope:** this recipe covers the poll-claim loop, lease heartbeat, handler dispatch, result reporting, idempotency contract, and LLM backend selection. It does not cover job schema evolution, backend authentication/credential rotation, or the backend API itself.

### Terminology

The node-level terms (Node, Job, Claim, Lease, Heartbeat, Handler, Dead-letter) are defined in the job-worker ingredient, and the LLM backend term in the llm-backend ingredient. The recipe uses them unchanged.

### Pipeline

A job flows through the three ingredients in one direction: the job worker claims it, hands its payload to the handler registered for its type, the handler asks the LLM backend for schema-constrained output, and the job worker reports the validated result (or a failure) to the backend.

## Ingredients

| Name | Domain | Role | Required | Configuration |
|------|--------|------|----------|---------------|
| Job worker | `agenticdevelopercookbook://ingredients/infrastructure/job-worker` | Owns the poll-claim loop, lease heartbeat, handler dispatch table, result reporting, and the idempotency contract | Yes | Supported job types, batch size, poll interval (default 5 seconds), per-handler timeout, concurrency limit |
| LLM backend | `agenticdevelopercookbook://ingredients/infrastructure/llm-backend` | Executes each handler's inference step with schema-constrained output through a configured provider | Yes | Backend kind (OpenAI-compatible HTTP endpoint or CLI subprocess) and endpoint, selected by environment variable or config file |
| Categorize and tag handler | `agenticdevelopercookbook://ingredients/infrastructure/categorize-and-tag-handler` | The concrete handler registered for the `categorize_and_tag` job type | Yes | Registered in the job worker's dispatch table at startup; receives the LLM backend by injection |

## Integration Requirements

- **register-handler-at-startup**: The `categorize_and_tag` handler MUST be registered in the job worker's dispatch table at startup, and the job worker's supported-types set MUST include `categorize_and_tag` if and only if that handler is registered.
- **inject-llm-backend**: The node MUST construct the LLM backend from configuration at startup and inject it into every handler that performs inference. A handler MUST NOT select or construct its own backend, so the same handler runs unmodified on the Swift development node and the TypeScript production node.
- **backend-failure-is-job-failure**: When the LLM backend fails or returns output that does not validate against the handler's schema, the handler MUST fail and the job worker MUST report the job as failed with `retryable: true`. A malformed result MUST NOT be passed to the complete call.
- **handler-result-reported-by-worker**: The job worker, not the handler, MUST report the handler's validated result to the backend, and MUST do so only after the handler's schema validation has passed.
- **idempotent-end-to-end**: A job re-claimed after a lease expiry MUST produce the same backend result as the first completion, with no duplicate category or tag entries. The job worker's duplicate-terminal-state tolerance and the handler's idempotent-categorization requirement together satisfy this.
- **stub-backend-testable**: The composition MUST be runnable with a stub LLM backend and a stub job source, so the integration vectors can run without network access to a model or to the `adh` backend.

## Layout

The node is a linear pipeline of three components arranged around one control loop:

```
 adh backend ──claim (types, batch)──▶ ┌─────────────────────────────┐
     ▲                                  │ Job worker                   │
     │  heartbeat / complete / fail     │  poll-claim loop             │
     └───────────────────────────────── │  lease heartbeat per job     │
                                        │  dispatch table (type → fn)  │
                                        └──────────────┬──────────────┘
                                                       │ payload
                                        ┌──────────────▼──────────────┐
                                        │ categorize_and_tag handler   │
                                        └──────────────┬──────────────┘
                                                       │ schema + prompt
                                        ┌──────────────▼──────────────┐
                                        │ LLM backend (configured)     │
                                        │  HTTP API  or  CLI process   │
                                        └─────────────────────────────┘
```

This is a non-UI recipe: the arrangement is the logical dataflow above, not a visual layout.

## Shared State

| State | Source | Consumer | Direction | Mechanism |
|-------|--------|----------|-----------|-----------|
| Supported job types | Handler registry built at startup | Job worker claim request | one-way | The set is derived once from registered handlers and sent with every claim |
| Claimed job (id, type, payload, lease duration) | Backend claim response | Job worker, handler, heartbeat timer | one-way | Held in the worker's local tracking until the terminal call is acknowledged |
| Lease validity | Backend heartbeat response | Job worker | one-way | A lease-invalid response cancels the handler and suppresses complete and fail |
| LLM backend configuration | Environment variable or config file | LLM backend, injected into the handler | one-way | Read once at startup; no code change needed to switch |
| Handler result | Categorize and tag handler | Job worker | one-way | The validated `{ category, tags, confidence? }` object returned from the handler |

## Integration Test Vectors

| ID | Requirements | Input | Expected |
|----|-------------|-------|----------|
| `apn-001` | `poll-claim`, `run-handler`, `complete-on-success` | Backend queue contains one `categorize_and_tag` job with `{ "title": "How to prune roses", "body": "..." }` | Node claims the job, handler executes, node calls complete with `{ category, tags, confidence? }`, job moves to done state on backend |
| `apn-002` | `run-handler`, `fail-with-backoff`, `loop-continuity` | Handler for `categorize_and_tag` throws an unrecoverable error | Node calls fail with `retryable: true`; loop continues; next poll iteration proceeds normally |
| `apn-003` | `unknown-type-fail` | Backend queue contains a job with `type: "transcribe_audio"` and node has no handler for that type | Node immediately calls fail with `retryable: false`; job goes to dead-letter; loop continues |
| `apn-004` | `lease-heartbeat`, `complete-on-success` | Handler takes longer than one heartbeat interval (e.g., 40s LLM call on a 30s lease) | At least one heartbeat is sent before the complete call; job lease remains valid throughout; complete succeeds |
| `apn-005` | `idempotency`, `idempotent-end-to-end` | Same job is claimed twice (simulated lease expiry mid-run); handler completes on the second claim | Backend result is identical to first completion; no duplicate category or tag entries created |
| `apn-006` | `poll-claim`, `loop-continuity` | Backend queue is empty | Claim returns zero jobs; no complete/fail calls made; loop waits the poll interval and polls again |
| `apn-007` | `lost-lease-abort` | Heartbeat response returns lease-invalid (e.g. 409 Conflict) mid-handler | Node cancels handler execution, does NOT call complete or fail, logs lease loss, continues loop |
| `apn-008` | `backend-failure-is-job-failure`, `inject-llm-backend` | Stub LLM backend returns a result missing `category` | Handler fails; node calls fail with `retryable: true`; no complete call is made |
| `apn-009` | `register-handler-at-startup` | Start the node with the handler registry populated | The claim request lists exactly `categorize_and_tag` as the supported type |

## Edge Cases

- **LLM backend returns invalid schema**: the handler MUST fail the job with `retryable: true` rather than passing a malformed result to complete (backend-failure-is-job-failure).
- **Startup with empty handler registry**: the node MUST log a warning and start normally; it will claim no jobs (no supported types), poll an empty result, and idle.
- **Large batch with mixed types**: the node SHOULD process jobs in the batch concurrently up to a configurable concurrency limit, with each job's heartbeat running independently.
- **Backend slower than the lease**: a long LLM call that outlasts one heartbeat interval relies on the job worker's heartbeat running independently of the handler, so the lease stays valid while inference runs.
- **Component-level cases**: network partition during complete, heartbeat firing after a terminal call, and clock skew are specified in the job-worker ingredient's edge cases; they apply to this composition unchanged.

## Platform Notes

- **SwiftUI / Compose / React/Web**: Not applicable. The node is a background worker with no view layer. The two implementations are a Swift macOS daemon and a TypeScript service.
- **Swift macOS daemon (development node)**: Runs as a launchd-managed background process with a local model server as the default LLM backend. Detailed daemon, heartbeat, structured-output, and logging guidance is in the job-worker and llm-backend ingredients.
- **TypeScript service (production node)**: Runs as a containerized Node.js process using a hosted API as the LLM backend. The backend is selected by the `LLM_BACKEND_KIND` and `LLM_BACKEND_URL` environment variables; see the llm-backend ingredient and the Design Decision on LLM backend selection below.

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

**Decision**: LLM backend selected by configuration, not by handler code.
**Rationale**: The `categorize_and_tag` handler (and future handlers) must run unmodified on both the Swift dev node (local model) and the TypeScript prod node (hosted API). Injecting the backend as a configured dependency keeps handler code platform-agnostic and testable with a stub.
**Approved**: pending

**Decision**: Idempotency is a handler contract, not enforced by the node framework.
**Rationale**: Only the handler knows what constitutes a duplicate side effect for its domain. The node framework can detect a duplicate job ID (already in terminal state on the backend) and skip re-running, but fine-grained deduplication (e.g., "did I already write this category?") requires handler-level logic.
**Approved**: pending

## Compliance

| Check | Status | Category |
|-------|--------|----------|
| [secure-log-output](agenticdevelopercookbook://compliance/security#secure-log-output) | partial | Security |
| [idempotent-operations](agenticdevelopercookbook://compliance/reliability#idempotent-operations) | partial | Reliability |
| [error-recovery](agenticdevelopercookbook://compliance/reliability#error-recovery) | partial | Reliability |

> Status is `partial`: this recipe specifies the integration-level requirements that satisfy these checks, but compliance is verified per concrete node implementation, not at the recipe level.

## Change History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 2.0.0 | 2026-10-04 | Mike Fullerton | Restructure into recipe shape; extract component behavior into ingredients |
| 1.0.0 | 2026-06-28 | Mike Fullerton | Initial recipe — platform-agnostic spec for the AI processing node with poll-claim, heartbeat, handler dispatch, idempotency, and categorize_and_tag handler |
