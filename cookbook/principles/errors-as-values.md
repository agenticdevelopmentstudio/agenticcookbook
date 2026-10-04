---
id: 51e1f37a-919e-4e42-b439-ffdf0c2ef2e8
title: "Errors as values"
domain: agenticdevelopercookbook://principles/errors-as-values
type: principle
version: 1.0.1
status: accepted
language: en
created: 2026-06-09
modified: 2026-06-10
author: Mike Fullerton
copyright: 2026 Mike Fullerton
license: MIT
summary: "Represent expected, recoverable failures as values so failure paths show up in signatures and must be handled."
platforms: []
tags:
  - errors-as-values
  - error-handling
depends-on: []
related:
  - agenticdevelopercookbook://principles/fail-fast
  - agenticdevelopercookbook://principles/explicit-over-implicit
  - agenticdevelopercookbook://principles/parse-dont-validate
references:
  - https://doc.rust-lang.org/book/ch09-00-error-handling.html
  - https://fsharpforfunandprofit.com/rop/
  - https://blog.kinto-technologies.com/posts/2025-12-13-rust-railway-oriented-programming-en/
  - https://returns.readthedocs.io/en/latest/pages/railway.html
approved-by: "approve-artifact v1.0.0"
approved-date: "2026-06-10"
---

# Errors as values

Represent expected, recoverable failures as values in the type system — `Result`/`Either`, sealed error types — so that failure paths appear in function signatures and the compiler forces every caller to handle them. Reserve exceptions and panics for truly unrecoverable conditions. This makes the failure surface visible and exhaustiveness-checkable instead of hidden in control flow.

- Expected vs exceptional: model recoverable outcomes (not-found, validation-failed, conflict) as returned values; let exceptions signal bugs and unrecoverable states.
- Put the failure in the signature: a function that can fail should say so in its return type, not through an undeclared throw a caller can't see.
- Choose a boundary policy deliberately and keep it consistent per layer: Rust `Result`, Go explicit error returns, Kotlin sealed `Result`, Swift `Result`/`throws`, TypeScript Result-style libraries.
- Never swallow: log-and-continue, a silent `null`, or a default that masks failure is the documented failure mode — propagate or handle explicitly.
- Complements the wire format: HTTP error responses (RFC 9457) describe failure on the wire; this principle governs how failure is represented *in code*.

## Change History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 1.0.1 | 2026-06-10 | Mike Fullerton | Cite recovered Tier-1 research sources (adversarially-audited) |
| 1.0.0 | 2026-06-09 | Mike Fullerton | Initial creation |
