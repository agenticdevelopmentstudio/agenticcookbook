
- Generate the key **once per logical operation**, before the first attempt, and reuse the *same* key for every retry of that operation.
- **MUST NOT** mutate the request body between retries that share a key — that triggers the `422` rejection above.
- A fresh user-initiated action gets a fresh key.

