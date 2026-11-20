
- `should-surface-invalid-state-at-origin`: invalid state is detected and surfaced where it originates, or the work says why not
- `should-assert-preconditions-in-debug`: assertions and preconditions guard the code's assumptions in debug builds, or the work says why not
- `should-validate-inputs-at-boundaries`: every input is validated at the system boundary, or the work says why not
- `should-return-typed-errors`: failures are returned as typed errors, none swallowed, or the work says why not
- `must-not-use-empty-catch-blocks`: no catch block is empty
- `should-fail-gracefully-in-production-loudly-in-debug`: production failures give clear messages and debug failures are loud, or the work says why not
