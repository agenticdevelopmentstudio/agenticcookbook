
# Flaky Test Prevention

Flaky tests destroy confidence. Quarantine them immediately — fix or delete, never ignore.

**Rules:**
- Tests MUST NOT share mutable state (each test arranges its own)
- Tests MUST NOT depend on execution order
- Unit tests MUST NOT make real network calls (use fakes or stubs)
- Tests MUST NOT use `sleep()` or timing-dependent assertions — use deterministic waits or callbacks
- Unit tests MUST NOT produce filesystem side effects (use temp directories, clean up in teardown)
- Tests SHOULD NOT rely on system clock — inject time as a dependency
- If a test fails intermittently, it is broken. It MUST be treated as a P1 bug.

References:
- [Martin Fowler: Eradicating Non-Determinism in Tests](https://martinfowler.com/articles/nonDeterminism.html)
- [Google Testing Blog: Flaky Tests](https://testing.googleblog.com/)

