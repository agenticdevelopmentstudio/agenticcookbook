
- `must-keep-private-keys-non-exportable`, `should-combine-with-other-token-controls`: Sender-constraining fails if the attacker steals **both** the token and the key material (e.g., full client compromise or XSS reading key storage); per RFC 9700 it is one layer, not a substitute for protecting the key.
