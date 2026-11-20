
Process a write request carrying a key as follows:

1. **Fingerprint the request.** Compute a hash of the request payload (and any semantically significant headers). Store it alongside the key.
2. **Look up the key.**
   - **New key:** acquire a lock on the key, then execute the operation. On completion, persist the key → `{request-fingerprint, status-code, response-body}` and release the lock.
   - **Known key, request still in flight:** a concurrent retry **MUST** be blocked or rejected (return `409 Conflict`) rather than executed a second time. Use a row lock, advisory lock, or atomic conditional insert — not a read-then-write race.
   - **Known key, completed, same fingerprint:** **MUST** replay the stored response (same status and body) without re-executing the operation.
   - **Known key, completed, different fingerprint:** the client reused a key with different parameters. The server **MUST** reject it — return `422 Unprocessable Content` — rather than silently re-executing or overwriting. Failing fast here surfaces a client bug instead of double-charging.

