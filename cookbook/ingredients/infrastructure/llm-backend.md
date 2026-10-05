---
id: 597E9CD0-453A-42B8-A464-8BA8D31A6EFC
title: "LLM Backend"
domain: agenticdevelopercookbook://ingredients/infrastructure/llm-backend
type: ingredient
version: 1.0.0
status: review
language: en
created: 2026-10-04
modified: 2026-10-04
author: Mike Fullerton
copyright: 2026 Mike Fullerton
license: MIT
summary: "Configuration-selected inference backend (OpenAI-compatible HTTP endpoint or CLI subprocess) that returns schema-constrained structured output to job handlers"
platforms:
  - swift
  - typescript
tags:
  - infrastructure
  - ai-jobs
  - llm
  - structured-output
depends-on: []
related:
  - agenticdevelopercookbook://recipes/infrastructure/ai-processing-node
  - agenticdevelopercookbook://ingredients/infrastructure/job-worker
references:
  - https://datatracker.ietf.org/doc/html/rfc2119
approved-by: "approve-artifact v1.1.0"
approved-date: "2026-10-04"
---

# LLM Backend

## Overview

An LLM backend is the inference provider a handler uses for its model step: a local model server, a hosted API, or a CLI tool run as a subprocess. This ingredient makes the provider a configured dependency rather than a code decision, so the same handler runs unmodified against a local model on a development machine and a hosted API in production, and can be tested against a stub. It also fixes how handlers obtain results: as schema-constrained structured output validated before the handler returns, never as free-form text parsed after the fact.

Use it in any worker or service where handlers call a language model and the deployment environment decides which model that is.

## Behavioral Requirements

- **llm-backend-selectable**: The node MUST support selecting which LLM backend executes a handler's inference step via configuration (e.g., an environment variable or config file), with no code changes required to switch. Supported backend kinds include at minimum: an OpenAI-compatible HTTP API endpoint (local model server or hosted), and a CLI-based inference tool invoked as a subprocess.
- **structured-output**: Handlers that invoke the LLM MUST request schema-constrained (structured) output from the backend rather than parsing free-form text. The output schema MUST be defined per handler and validated before the handler returns its result.
- **backend-injected**: The backend MUST be supplied to handlers as an injected dependency so handler code never names a provider and can be exercised with a stub backend.
- **invalid-output-fails-retryable**: If the backend returns output that does not validate against the handler's schema, the handler MUST fail the job as retryable rather than passing a malformed result onward.

## Appearance

Not applicable — an LLM backend is infrastructure with no visual surface.

## States

| State | Behavior |
|-------|----------|
| Unconfigured | No backend kind is configured; startup reports a configuration error rather than defaulting silently |
| Ready | A backend kind and its endpoint or command are configured and selected |
| Inferring | A handler request is in flight to the backend |
| Output invalid | The backend responded but the output failed schema validation; the handler reports a retryable failure |

## Accessibility

Not applicable — an LLM backend has no user-facing surface.

## Conformance Test Vectors

| ID | Requirements | Input | Expected |
|----|-------------|-------|----------|
| llm-backend-001 | llm-backend-selectable | Switch the configured backend kind from an HTTP endpoint to a CLI tool and restart | Handlers run against the new backend with no code change |
| llm-backend-002 | structured-output | A handler requests inference with a result schema | The request carries the schema or equivalent structured-output constraint; the result is validated against it |
| llm-backend-003 | invalid-output-fails-retryable | Stub backend returns output missing a required field | Handler fails the job with `retryable: true`; no malformed result is reported |
| llm-backend-004 | backend-injected | Run a handler with a stub backend | Handler produces its result without any network or subprocess call |

## Edge Cases

- **LLM backend returns invalid schema**: The handler MUST fail the job with `retryable: true` rather than passing a malformed result to complete (invalid-output-fails-retryable).
- **Model without native structured-output support**: Fall back to a JSON-object response mode with the schema injected into the system prompt, and still validate the output before returning.
- **CLI backend exits non-zero**: The handler treats this as a handler error and fails the job as retryable.
- **Unknown backend kind in configuration**: Startup MUST fail with a clear configuration error rather than choosing a default provider.

## Configuration

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `llmBackendKind` | enum | (required) | One of `openai-compatible` or `cli` |
| `llmBackendUrl` | string | (none) | Endpoint for the `openai-compatible` kind |
| `llmBackendCommand` | string | (none) | Executable for the `cli` kind |
| `llmBackendModel` | string | (backend default) | Model identifier passed to the backend |

## Logging

Subsystem: `{{bundle_id}}` | Category: `LLMBackend`

| Event | Level | Message |
|-------|-------|---------|
| Backend selected | info | `LLMBackend: using {{kind}} backend` |
| Inference started | debug | `LLMBackend: request started for job {{jobId}}` |
| Inference completed | debug | `LLMBackend: request completed in {{duration}}s` |
| Output failed validation | warning | `LLMBackend: output for job {{jobId}} failed schema validation: {{error}}` |
| Backend error | error | `LLMBackend: backend failed: {{error}}` |

## Platform Notes

SwiftUI, Compose, and React/Web do not apply: an LLM backend has no view layer.

- **Swift macOS (development node)**: Read the backend from a `.env` file or the `UserDefaults` key `com.adh.node.llmBackend`. A local model server (e.g., Ollama via its OpenAI-compatible endpoint) is the default for development. Use the `/v1/chat/completions` endpoint with `response_format: { type: "json_schema", json_schema: { schema: ... } }` when the model supports it; fall back to a `json_object` response type with system-prompt schema injection.
- **TypeScript (production node)**: Read `LLM_BACKEND_KIND` and `LLM_BACKEND_URL` environment variables. Production uses a hosted API (e.g., the Anthropic API via an OpenAI-compatible shim, or the native Anthropic SDK). Use the provider's native structured-output parameter (`response_format` or `tools` with a single schema-constrained tool) to avoid parsing free text.

## Design Decisions

**Decision**: LLM backend selected by configuration, not by handler code.
**Rationale**: Handlers must run unmodified on both the Swift dev node (local model) and the TypeScript prod node (hosted API). Injecting the backend as a configured dependency keeps handler code platform-agnostic and testable with a stub.
**Approved**: pending

## Compliance

| Check | Status | Category |
|-------|--------|----------|
| [explicit-error-handling](agenticdevelopercookbook://compliance/best-practices#explicit-error-handling) | partial | Best Practices |
| [fault-tolerance](agenticdevelopercookbook://compliance/reliability#fault-tolerance) | partial | Reliability |

> Status is `partial`: this ingredient specifies the requirements that satisfy these checks, but compliance is verified per concrete backend implementation, not at the ingredient level.

## Change History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 1.0.0 | 2026-10-04 | Mike Fullerton | Extracted from the AI Processing Node recipe |
