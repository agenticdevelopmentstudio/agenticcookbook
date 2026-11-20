
- **should-model-recoverable-outcomes-as-values**: Expected vs exceptional: SHOULD model recoverable outcomes (not-found, validation-failed, conflict) as returned values.
- **should-reserve-exceptions-for-unrecoverable**: SHOULD reserve exceptions and panics for truly unrecoverable conditions: let exceptions signal bugs and unrecoverable states.
- **should-put-the-failure-in-the-signature**: Put the failure in the signature: a function that can fail SHOULD say so in its return type, not through an undeclared throw a caller can't see.
- **should-keep-boundary-policy-consistent-per-layer**: SHOULD choose a boundary policy deliberately and keep it consistent per layer: Rust `Result`, Go explicit error returns, Kotlin sealed `Result`, Swift `Result`/`throws`, TypeScript Result-style libraries.
- **must-not-swallow-failures**: MUST NOT swallow: log-and-continue, a silent `null`, or a default that masks failure is the documented failure mode — MUST propagate or handle explicitly.
