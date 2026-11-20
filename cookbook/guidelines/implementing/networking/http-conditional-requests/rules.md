
**ETags as validators**
- **must-return-etags**: The server **MUST** return an `ETag` response header on representations that participate in conditional requests.
  - An ETag is an opaque token identifying a specific resource version.
- **should-emit-strong-etags-for-writes**: The server **SHOULD** emit strong ETags for write concurrency, since `If-Match` uses the strong comparison.
  - Strong ETags (`"abc"`) assert byte-for-byte equivalence; weak ETags (`W/"abc"`) assert only semantic equivalence.
- **must-treat-etags-as-opaque**: Clients **MUST** treat ETag values as opaque — do not parse, compare substrings of, or derive meaning from them.

**Efficient reads — If-None-Match / 304**
- **should-send-if-none-match-on-repeat-reads**: Clients **SHOULD** send `If-None-Match: <etag>` (echoing the ETag from a prior response) on repeat GET/HEAD requests.
- **must-return-304-when-unchanged**: If the resource is unchanged, the server **MUST** return `304 Not Modified` with no body, including `ETag`, `Cache-Control`, and `Vary` if present.
  - The client reuses its cached representation.
- **should-prefer-if-none-match-over-if-modified-since**: `If-None-Match` uses weak comparison and **SHOULD** be preferred over `If-Modified-Since` (1-second granularity) when an ETag exists.

**Optimistic concurrency on writes — If-Match / 412**
- **should-send-if-match-on-shared-writes**: For PUT/PATCH/DELETE on shared, mutable resources, clients **SHOULD** send `If-Match: <etag>` carrying the ETag they last read.
- **must-apply-writes-only-on-matching-etag**: The server **MUST** apply the change only if the current ETag matches (strong comparison); otherwise it **MUST** reject with `412 Precondition Failed` and make no change.
  - The client refetches, rebases its edit, and retries.
- **should-support-and-may-require-if-match**: Mutating endpoints on shared resources **SHOULD** support `If-Match` and **MAY** require it (returning `428 Precondition Required`, RFC 6585) to force callers to opt into concurrency safety.

**Boundaries and pitfalls**
- **should-use-if-match-and-idempotency-keys-together**: Writes SHOULD use both: `If-Match` for correctness under concurrent edits, idempotency keys for retry safety.
  - See the related guidelines.
- **must-not-default-if-match-to-star**: Agents **MUST NOT** strip or blindly default `If-Match` to `*` to "make the 412 go away" — that reintroduces the lost-update bug it prevents.
- **should-surface-412-apart-from-409**: Clients and servers SHOULD surface `412` distinctly from `409 Conflict`: 412 means the client's precondition failed (refetch and retry); 409 signals a domain-level conflict that may not be resolvable by retry.
- **should-pass-etags-through-intermediaries**: Behind proxies/CDNs, deployments SHOULD ensure ETags are passed through unmodified; some intermediaries rewrite or drop them.
