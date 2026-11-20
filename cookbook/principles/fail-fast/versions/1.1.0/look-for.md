
- `should-surface-invalid-state-at-origin`: invalid state passed along silently past the point where it arose
- `should-assert-preconditions-in-debug`: an assumption about state with no assertion or precondition checking it in debug builds
- `should-validate-inputs-at-boundaries`: an input accepted at a system boundary without validation
- `should-return-typed-errors`: an exception swallowed where a typed error could be returned
- `must-not-use-empty-catch-blocks`: an empty catch block
- `should-fail-gracefully-in-production-loudly-in-debug`: a production failure with no clear message, or a debug failure that passes quietly
