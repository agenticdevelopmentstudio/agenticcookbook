
- The client **MUST** generate a key pair and send a `DPoP` proof JWT on token requests and on every protected resource request, signed with the private key.
- The proof JWT **MUST** include `htm` (HTTP method), `htu` (HTTP URI), `iat`, and a unique `jti`; for resource requests it **MUST** include `ath` (access-token hash).
- The authorization server **MUST** bind the token to the proof key via the `jkt` (JWK SHA-256 thumbprint) confirmation claim (`cnf.jkt`); the resource server **MUST** verify the presented proof key matches it.
- Resource servers **MUST** reject replayed proofs — enforce a `jti`/`iat` freshness window with a server-provided `nonce` where replay risk is high.
- Private keys **MUST** stay in non-exportable storage (WebCrypto non-extractable keys, OS keystore); never persist them where script can read them.

