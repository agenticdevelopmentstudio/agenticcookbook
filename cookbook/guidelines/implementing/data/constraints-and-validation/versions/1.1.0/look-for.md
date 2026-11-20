
Validates CHECK constraint syntax and evaluation semantics, ensures boolean columns use `INTEGER CHECK(col IN (0,1))` pattern, enforces enum-like constraints via `CHECK(col IN (...))` with documented values, and confirms NULL truthiness is never relied upon in constraint logic.

