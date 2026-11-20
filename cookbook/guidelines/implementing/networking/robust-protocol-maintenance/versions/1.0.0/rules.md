
- Inputs **SHOULD** be parsed strictly against a dated, pinned version of the spec or schema, and violations **SHOULD** be rejected clearly rather than silently coerced (ties to `parse-dont-validate` and `fail-fast`).
- Implementations **MUST NOT** silently "fix up" or guess intent for malformed protocol or API messages on machine-to-machine paths.
- Rejections **SHOULD** emit an explicit, actionable error (what failed, which rule, expected shape) so the sending party gets visible feedback — RFC 9413 calls this "virtuous intolerance".
- Protocols and APIs **SHOULD** carry an explicit **version** so strictness can evolve without breaking peers; pin the revision you validate against.
- Stateless or unauthenticated endpoints **MAY** soften loud rejection where verbose errors enable amplification or DoS (RFC 9413 notes this exception) — log internally instead.
- You **SHOULD** treat each tolerated deviation as a tracked maintenance item: file it, decide whether the spec or the sender is wrong, and close the gap — do not let it become permanent behavior.

