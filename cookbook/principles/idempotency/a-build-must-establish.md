
- `should-make-operations-safe-to-repeat`: every user action and system operation is safe to repeat without duplicate side effects, or the work says why not
- `should-debounce-buttons-during-async`: every button that starts an async operation is debounced or disabled until it finishes, or the work says why not
- `should-use-idempotency-keys`: every API call with side effects carries an idempotency key, or the work says why not
- `must-make-migrations-rerunnable`: every database migration is safe to run multiple times
- `should-check-state-before-transitions`: every state transition checks the current state before it is applied, or the work says why not
