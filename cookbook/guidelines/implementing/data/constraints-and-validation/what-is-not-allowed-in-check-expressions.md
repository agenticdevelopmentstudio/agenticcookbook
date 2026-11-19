
A CHECK expression MUST NOT use these; they are explicitly prohibited:

| Prohibited | Alternative |
|------------|-------------|
| Subqueries (`SELECT ...`) | Use triggers for cross-row validation |
| `CURRENT_TIME` | Application-level validation |
| `CURRENT_DATE` | Application-level validation |
| `CURRENT_TIMESTAMP` | Application-level validation |

