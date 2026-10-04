
- **MUST NOT** treat end-to-end tests as a substitute for contract tests — they are slower, flakier, and fail far from the cause.
- **MUST NOT** write a "contract" test against a third-party API you own neither side of and expect it to gate *their* deploys; you can only assert your tolerance of their pinned schema.
- **SHOULD NOT** duplicate full business-logic assertions inside contracts — that belongs in unit/integration tests for each service.

