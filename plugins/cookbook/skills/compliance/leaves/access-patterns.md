<!-- leaf: compliance/access-patterns · source: compliance/access-patterns.md -->

**Rules** (cite as `compliance/access-patterns#<slug>`):

- `apis-follow-restful-conventions-consistent` MUST — APIs MUST follow RESTful conventions with consistent naming and versioning.
- `components-define-behavior-network-unavailable` MUST — Components MUST define behavior when network is unavailable.
- `failed-network-requests-implement-retry-exponential-backoff` MUST — Failed network requests MUST implement retry with exponential backoff and jitter.
- `network-requests-have-configured-timeouts-wait` MUST — All network requests MUST have configured timeouts; MUST NOT wait indefinitely.
- `clients-handle-http-429-responses` MUST — Clients MUST handle HTTP 429 responses and respect Retry-After headers.
- `endpoints-returning-collections-support-pagination` MUST — Endpoints returning collections MUST support pagination.
- `real-time-connections-define-reconnection-behavior-backoff` MUST — Real-time connections MUST define reconnection behavior with backoff.
- `clients-handle-documented-error-response` MUST — Clients MUST handle all documented error response codes gracefully.

# Access Patterns

Compliance checks that govern how components communicate over the network, design their APIs, and handle the inherent unreliability of distributed access. These checks ensure consistent, resilient, and well-behaved network interactions across all platforms.

## Applicability

Recipes or guidelines involving network communication, API calls, data synchronization, or client-server interaction.

## Checks

### api-design-conventions

APIs MUST follow RESTful conventions with consistent naming and versioning.

**Applies when:** a component exposes or consumes an HTTP API.

**Guidelines:**
- API Design

---

### offline-behavior

Components MUST define behavior when network is unavailable.

**Applies when:** a feature depends on network connectivity to function.

**Guidelines:**
- Offline and Connectivity

---

### retry-with-backoff

Failed network requests MUST implement retry with exponential backoff and jitter.

**Applies when:** a component makes network requests that may transiently fail.

**Guidelines:**
- Retry and Resilience

---

### timeout-configuration

All network requests MUST have configured timeouts; MUST NOT wait indefinitely.

**Applies when:** a component initiates any network request.

**Guidelines:**
- Timeouts

---

### rate-limit-handling

Clients MUST handle HTTP 429 responses and respect Retry-After headers.

**Applies when:** a component calls rate-limited APIs or services.

**Guidelines:**
- Rate Limiting

---

### pagination-support

Endpoints returning collections MUST support pagination.

**Applies when:** an API endpoint returns a list of resources.

**Guidelines:**
- Pagination

---

### reconnection-strategy

Real-time connections MUST define reconnection behavior with backoff.

**Applies when:** a component uses WebSockets, server-sent events, or other persistent connections.

**Guidelines:**
- Real-Time Communication

---

### error-response-handling

Clients MUST handle all documented error response codes gracefully.

**Applies when:** a component consumes an API that defines error responses.

**Guidelines:**
- Error Responses
