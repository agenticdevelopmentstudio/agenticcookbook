
- `should-make-operations-safe-to-repeat`: a user action or system operation that produces a duplicate side effect when repeated
- `should-debounce-buttons-during-async`: a button that stays live and re-triggers while its async operation is in flight
- `should-use-idempotency-keys`: an API call with side effects sent without an idempotency key
- `must-make-migrations-rerunnable`: a database migration that fails or corrupts data when run a second time
- `should-check-state-before-transitions`: a state transition applied without first checking the current state
