
These are explicitly prohibited:

| Prohibited | Alternative |
|------------|-------------|
| Subqueries (`SELECT ...`) | Use triggers for cross-row validation |
| `CURRENT_TIME` | Application-level validation |
| `CURRENT_DATE` | Application-level validation |
| `CURRENT_TIMESTAMP` | Application-level validation |

Date validation that depends on "now" (e.g., `CHECK (event_date <= CURRENT_DATE)`) cannot be expressed in a schema constraint. Use triggers or application-layer validation instead.

