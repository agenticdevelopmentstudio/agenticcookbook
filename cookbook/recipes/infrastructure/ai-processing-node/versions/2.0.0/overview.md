
An AI processing node is a long-running worker that continuously pulls AI jobs from the `adh` backend, executes each job through a registered handler, renews the job's server-side lease while working, and reports either a structured result or a retryable failure. This recipe composes three ingredients: the job worker (poll-claim loop, lease heartbeat, handler dispatch, result reporting, idempotency), the LLM backend (configuration-selected inference with schema-constrained output), and the `categorize_and_tag` handler (the primary concrete handler).

This recipe specifies **shared business logic only** — it is intentionally platform-agnostic. Two implementations satisfy it simultaneously: a Swift macOS daemon used as a development node, and a TypeScript service deployed as the production node. Neither implementation language appears in the requirements below; platform-specific guidance lives in [Platform Notes](#platform-notes).

**Scope:** this recipe covers the poll-claim loop, lease heartbeat, handler dispatch, result reporting, idempotency contract, and LLM backend selection. It does not cover job schema evolution, backend authentication/credential rotation, or the backend API itself.

### Terminology

The node-level terms (Node, Job, Claim, Lease, Heartbeat, Handler, Dead-letter) are defined in the job-worker ingredient, and the LLM backend term in the llm-backend ingredient. The recipe uses them unchanged.

### Pipeline

A job flows through the three ingredients in one direction: the job worker claims it, hands its payload to the handler registered for its type, the handler asks the LLM backend for schema-constrained output, and the job worker reports the validated result (or a failure) to the backend.

