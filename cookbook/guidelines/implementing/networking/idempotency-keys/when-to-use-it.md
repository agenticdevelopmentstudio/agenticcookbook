
- State-changing endpoints that are not naturally idempotent — `POST` creating a resource, charging a payment, sending a message — **SHOULD** accept an idempotency key.
- `GET`, `HEAD`, `PUT`, and `DELETE` are already idempotent by HTTP semantics and **do not** need a key. Do not add one out of habit (yagni).

