
- **Distinct from idempotency keys.** `If-Match` rejects a write against a stale version; an idempotency key lets the SAME write be retried safely after a network failure. Use both: `If-Match` for correctness under concurrent edits, idempotency keys for retry safety. See the related guidelines.
- Agents **MUST NOT** strip or blindly default `If-Match` to `*` to "make the 412 go away" — that reintroduces the lost-update bug it prevents.
- Surface `412` distinctly from `409 Conflict`: 412 means the client's precondition failed (refetch and retry); 409 signals a domain-level conflict that may not be resolvable by retry.
- Behind proxies/CDNs, ensure ETags are passed through unmodified; some intermediaries rewrite or drop them.

