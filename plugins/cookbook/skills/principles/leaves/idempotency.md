<!-- leaf: principles/idempotency · source: principles/idempotency.md -->

# Idempotency

User actions and system operations should be safe to repeat without duplicate side effects:

- Debounce or disable buttons during async operations
- Use idempotency keys for API calls with side effects
- Database migrations must be safe to run multiple times
- Check current state before applying state transitions
