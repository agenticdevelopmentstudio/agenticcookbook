---
id: db55507a-42ce-4c6d-bd8a-6ccdb6b2d152
title: "HTTP conditional requests and optimistic concurrency"
domain: agenticdevelopercookbook://guidelines/implementing/networking/http-conditional-requests
type: guideline
version: 1.0.0
status: accepted
language: en
created: 2026-06-09
modified: 2026-06-09
author: Mike Fullerton
copyright: 2026 Mike Fullerton
license: MIT
summary: "Use ETags with If-None-Match for efficient reads and If-Match for optimistic concurrency on writes to prevent lost updates."
platforms: []
tags:
  - api
  - http
  - concurrency
depends-on: []
related:
  - agenticdevelopercookbook://guidelines/implementing/networking/caching
  - agenticdevelopercookbook://guidelines/implementing/networking/idempotency-keys
references:
  - https://www.rfc-editor.org/rfc/rfc9110.html
approved-by: "approve-artifact v1.0.0"
approved-date: "2026-06-09"
triggers:
  - api-integration
  - networking
---

# HTTP conditional requests and optimistic concurrency

Conditional requests attach a precondition (an ETag validator) to a request so the server can short-circuit a read or reject a stale write. Per RFC 9110 (June 2022), use `If-None-Match` for cache-efficient reads and `If-Match` for optimistic concurrency on mutations. This prevents lost updates without server-side locking and is distinct from idempotency keys (which make retries safe).

## ETags as validators

- The server **MUST** return an `ETag` response header on representations that participate in conditional requests. An ETag is an opaque token identifying a specific resource version.
- Strong ETags (`"abc"`) assert byte-for-byte equivalence; weak ETags (`W/"abc"`) assert only semantic equivalence. The server **SHOULD** emit strong ETags for write concurrency, since `If-Match` uses the strong comparison.
- Clients **MUST** treat ETag values as opaque — do not parse, compare substrings of, or derive meaning from them.

## Efficient reads — If-None-Match / 304

- Clients **SHOULD** send `If-None-Match: <etag>` (echoing the ETag from a prior response) on repeat GET/HEAD requests.
- If the resource is unchanged, the server **MUST** return `304 Not Modified` with no body, including `ETag`, `Cache-Control`, and `Vary` if present. The client reuses its cached representation.
- `If-None-Match` uses weak comparison and **SHOULD** be preferred over `If-Modified-Since` (1-second granularity) when an ETag exists.

## Optimistic concurrency on writes — If-Match / 412

- For PUT/PATCH/DELETE on shared, mutable resources, clients **SHOULD** send `If-Match: <etag>` carrying the ETag they last read.
- The server **MUST** apply the change only if the current ETag matches (strong comparison); otherwise it **MUST** reject with `412 Precondition Failed` and make no change. The client refetches, rebases its edit, and retries.
- This is the read-modify-write guard against lost updates: two clients editing the same version cannot both succeed.
- `If-Match: *` requires the resource to exist; `If-None-Match: *` on a write requires it to NOT exist (create-only, guarding against accidental overwrite).
- Mutating endpoints on shared resources **SHOULD** support `If-Match` and **MAY** require it (returning `428 Precondition Required`, RFC 6585) to force callers to opt into concurrency safety.

## Boundaries and pitfalls

- **Distinct from idempotency keys.** `If-Match` rejects a write against a stale version; an idempotency key lets the SAME write be retried safely after a network failure. Use both: `If-Match` for correctness under concurrent edits, idempotency keys for retry safety. See the related guidelines.
- Agents **MUST NOT** strip or blindly default `If-Match` to `*` to "make the 412 go away" — that reintroduces the lost-update bug it prevents.
- Surface `412` distinctly from `409 Conflict`: 412 means the client's precondition failed (refetch and retry); 409 signals a domain-level conflict that may not be resolvable by retry.
- Behind proxies/CDNs, ensure ETags are passed through unmodified; some intermediaries rewrite or drop them.

## Change History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 1.0.0 | 2026-06-09 | Mike Fullerton | Initial creation |
