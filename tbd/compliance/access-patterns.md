---
id: 2FF8FEE9-3EAC-4CF3-9B0E-F88BD3CAFF58
title: "Access Patterns"
type: compliance
version: 1.0.1
status: draft
language: en
created: 2026-03-28
modified: 2026-06-09
author: Mike Fullerton
copyright: 2026 Mike Fullerton
license: MIT
summary: "Compliance checks for network communication, API design, and data access patterns."
platforms: []
tags: [compliance, access-patterns]
depends-on: []
related:
  - tbd/compliance/reliability.md
  - tbd/compliance/performance.md
  - tbd/compliance/security.md
references: []
---

# Access Patterns

Compliance checks that govern how components communicate over the network, design their APIs, and handle the inherent unreliability of distributed access. These checks ensure consistent, resilient, and well-behaved network interactions across all platforms.

## Applicability

Recipes or guidelines involving network communication, API calls, data synchronization, or client-server interaction.

## Checks

### api-design-conventions

APIs MUST follow RESTful conventions with consistent naming and versioning.

**Applies when:** a component exposes or consumes an HTTP API.

**Guidelines:**
- [adc.guideline.implementing.networking.api-design](cookbook:49399746-a81f-4163-8b07-0cfa11d87c2e)

---

### offline-behavior

Components MUST define behavior when network is unavailable.

**Applies when:** a feature depends on network connectivity to function.

**Guidelines:**
- [adc.guideline.implementing.networking.offline-and-connectivity](cookbook:67c59594-a5dc-46f2-aa61-3436921294c7)

---

### retry-with-backoff

Failed network requests MUST implement retry with exponential backoff and jitter.

**Applies when:** a component makes network requests that may transiently fail.

**Guidelines:**
- [adc.guideline.implementing.networking.retry-and-resilience](cookbook:cef41f52-bfc6-4ff0-bb67-eb52521c7391)

---

### timeout-configuration

All network requests MUST have configured timeouts; MUST NOT wait indefinitely.

**Applies when:** a component initiates any network request.

**Guidelines:**
- [adc.guideline.implementing.networking.timeouts](cookbook:c3883e6e-3bce-4bb9-a3be-61509a139288)

---

### rate-limit-handling

Clients MUST handle HTTP 429 responses and respect Retry-After headers.

**Applies when:** a component calls rate-limited APIs or services.

**Guidelines:**
- [adc.guideline.implementing.networking.rate-limiting](cookbook:c84400d9-83b3-4c4c-83d4-325dfa989202)

---

### pagination-support

Endpoints returning collections MUST support pagination.

**Applies when:** an API endpoint returns a list of resources.

**Guidelines:**
- [adc.guideline.implementing.networking.pagination](cookbook:49acdf9f-e4cb-4492-a620-809438eefb37)

---

### reconnection-strategy

Real-time connections MUST define reconnection behavior with backoff.

**Applies when:** a component uses WebSockets, server-sent events, or other persistent connections.

**Guidelines:**
- [adc.guideline.implementing.networking.real-time-communication](cookbook:2e317c68-384d-46b8-b3b3-0bcc6602e545)

---

### error-response-handling

Clients MUST handle all documented error response codes gracefully.

**Applies when:** a component consumes an API that defines error responses.

**Guidelines:**
- [adc.guideline.implementing.networking.error-responses](cookbook:631b7b61-985a-4f5d-9c44-2cfbfdb9091b)

## Change History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 1.0.1 | 2026-06-09 | Mike Fullerton | Repair stale cross-reference link scheme |
| 1.0.0 | 2026-03-28 | Mike Fullerton | Initial creation |
