
# Errors as values

Represent expected, recoverable failures as values in the type system — `Result`/`Either`, sealed error types — so that failure paths appear in function signatures and the compiler forces every caller to handle them. Reserve exceptions and panics for truly unrecoverable conditions. This makes the failure surface visible and exhaustiveness-checkable instead of hidden in control flow.

- Expected vs exceptional: model recoverable outcomes (not-found, validation-failed, conflict) as returned values; let exceptions signal bugs and unrecoverable states.
- Put the failure in the signature: a function that can fail should say so in its return type, not through an undeclared throw a caller can't see.
- Choose a boundary policy deliberately and keep it consistent per layer: Rust `Result`, Go explicit error returns, Kotlin sealed `Result`, Swift `Result`/`throws`, TypeScript Result-style libraries.
- Never swallow: log-and-continue, a silent `null`, or a default that masks failure is the documented failure mode — propagate or handle explicitly.
- Complements the wire format: HTTP error responses (RFC 9457) describe failure on the wire; this principle governs how failure is represented *in code*.

