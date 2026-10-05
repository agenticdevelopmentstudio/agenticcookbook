---
id: 7C0B4381-0A41-4D8C-8B90-1614038B1A94
title: "Categorize and Tag Handler"
domain: agenticdevelopercookbook://ingredients/infrastructure/categorize-and-tag-handler
type: ingredient
version: 1.0.0
status: review
language: en
created: 2026-10-04
modified: 2026-10-04
author: Mike Fullerton
copyright: 2026 Mike Fullerton
license: MIT
summary: "Job handler that categorizes and tags a title and body with schema-constrained LLM output, idempotent per job ID"
platforms:
  - swift
  - typescript
tags:
  - infrastructure
  - ai-jobs
  - handler
  - categorization
depends-on:
  - agenticdevelopercookbook://ingredients/infrastructure/llm-backend
related:
  - agenticdevelopercookbook://recipes/infrastructure/ai-processing-node
  - agenticdevelopercookbook://ingredients/infrastructure/job-worker
references:
  - https://datatracker.ietf.org/doc/html/rfc2119
approved-by: "approve-artifact v1.1.0"
approved-date: "2026-10-04"
---

# Categorize and Tag Handler

## Overview

The `categorize_and_tag` handler is the primary concrete job handler shipped with the AI processing node. Given a piece of content (title and body), it uses the configured LLM backend to choose the single best-fit category and a set of keyword tags, and returns them as a structured result the backend maps onto its categories and keywords stores. Use it as the reference handler when adding new job types: it shows the payload contract, the schema-constrained output rule, and the idempotency rule in one small unit.

## Behavioral Requirements

- **handler-job-type**: The handler MUST register under the job type `categorize_and_tag`.
- **input-payload**: The handler MUST accept a job payload of the shape `{ "title": string, "body": string }`.
- **output-result**: The handler MUST return a result of the shape `{ "category": string, "tags": string[], "confidence": number }`, where `category` and `tags` are required and `confidence` is optional.
- **category-single-best-fit**: `category` MUST be the single best-fit category string; the backend maps it to its categories store.
- **tags-keywords**: `tags` MUST contain zero or more keyword strings; the backend maps them to its keywords store.
- **confidence-advisory**: `confidence`, when present, MUST be a float in [0,1] expressing the LLM's self-reported confidence. The backend treats it as informational only.
- **schema-constrained-output**: The handler MUST pass a JSON Schema (or equivalent structured-output constraint) for the result object when invoking the LLM, and MUST NOT parse category or tags from free-form text.
- **idempotent-categorization**: Categorizing the same `(title, body)` pair a second time MUST produce no additional writes if the backend already holds a result for this job ID.

## Appearance

Not applicable — a job handler is headless and has no visual surface.

## States

| State | Behavior |
|-------|----------|
| Received | Payload validated against the input shape |
| Inferring | LLM request in flight with the result schema |
| Validated | LLM output conforms to the result schema |
| Rejected | Output failed validation; the handler reports a retryable failure |

## Accessibility

Not applicable — a job handler has no user-facing surface.

## Conformance Test Vectors

| ID | Requirements | Input | Expected |
|----|-------------|-------|----------|
| categorize-handler-001 | handler-job-type, input-payload, output-result | Job of type `categorize_and_tag` with `{ "title": "How to prune roses", "body": "..." }` | Handler returns `{ category, tags }` with an optional `confidence` |
| categorize-handler-002 | schema-constrained-output | Inspect the LLM request the handler builds | The request carries the result JSON Schema; no free-text parsing step exists |
| categorize-handler-003 | confidence-advisory | LLM returns `confidence: 1.4` | Output fails validation; handler reports a retryable failure |
| categorize-handler-004 | idempotent-categorization | Same job is processed twice | The second run produces no additional category or tag writes |
| categorize-handler-005 | category-single-best-fit, tags-keywords | LLM returns a category and an empty tag list | Result is accepted; `tags` is an empty array |

## Edge Cases

- **Empty body**: A payload with a title and an empty body is still valid; the handler categorizes from the title.
- **Missing payload field**: A payload missing `title` or `body` MUST be reported as a failure rather than sent to the LLM.
- **Result already held by the backend**: The handler returns the held result without re-applying it (idempotent-categorization).

## Configuration

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `categorizeTimeoutSeconds` | number | (job worker default) | Per-handler timeout for this handler |

## Logging

Subsystem: `{{bundle_id}}` | Category: `CategorizeAndTag`

| Event | Level | Message |
|-------|-------|---------|
| Handler started | debug | `CategorizeAndTag: job {{jobId}} started` |
| Handler succeeded | info | `CategorizeAndTag: job {{jobId}} categorized as "{{category}}" with {{tagCount}} tags` |
| Duplicate result skipped | debug | `CategorizeAndTag: job {{jobId}} already has a result, skipping writes` |
| Handler failed | warning | `CategorizeAndTag: job {{jobId}} failed: {{error}}` |

## Platform Notes

SwiftUI, Compose, and React/Web do not apply: the handler has no view layer. The handler logic is identical in the Swift macOS development node and the TypeScript production node; only the LLM backend wiring differs (see the `llm-backend` ingredient). In Swift, log through `os.Logger` with a category per handler; in TypeScript, log structured JSON to stdout.

## Design Decisions

**Decision**: The handler is specified as its own ingredient rather than inside the worker.
**Rationale**: The worker is generic across job types; a handler is a unit that varies per job type. Keeping them separate lets new handlers be added without touching the worker contract.
**Approved**: pending

## Compliance

| Check | Status | Category |
|-------|--------|----------|
| [idempotent-operations](agenticdevelopercookbook://compliance/reliability#idempotent-operations) | partial | Reliability |
| [data-integrity](agenticdevelopercookbook://compliance/reliability#data-integrity) | partial | Reliability |

> Status is `partial`: this ingredient specifies the requirements that satisfy these checks, but compliance is verified per concrete handler implementation, not at the ingredient level.

## Change History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 1.0.0 | 2026-10-04 | Mike Fullerton | Extracted from the AI Processing Node recipe |
