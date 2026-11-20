
- `should-make-operations-safe-to-repeat`: whether each user action and system operation is safe to repeat without duplicate side effects
- `should-debounce-buttons-during-async`: whether buttons are debounced or disabled during async operations
- `should-use-idempotency-keys`: whether API calls with side effects carry idempotency keys
- `must-make-migrations-rerunnable`: whether every database migration is safe to run multiple times
- `should-check-state-before-transitions`: whether current state is checked before each state transition is applied
