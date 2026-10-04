
- Servers that implement authorization **MUST** verify all inbound requests and **MUST NOT** use sessions for authentication.
- Session IDs **MUST** be non-deterministic (CSPRNG-generated, e.g. UUIDv4); avoid sequential or guessable IDs.
- Session-scoped data **SHOULD** be keyed as `<user_id>:<session_id>`, binding the session to identity derived from the token (not client-supplied), so a guessed ID cannot impersonate another user.

