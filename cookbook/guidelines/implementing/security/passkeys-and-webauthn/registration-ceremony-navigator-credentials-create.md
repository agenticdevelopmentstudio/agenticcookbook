
- The RP backend **MUST** generate a cryptographically random `challenge` (≥16 bytes), bind it to the session, and verify it server-side on return.
- Set `rp.id` to the registrable domain; set `user.id` to an opaque, stable, non-PII handle (not an email).
- Server verification **MUST** confirm: challenge match, `origin`, `rp.id` hash, the user-present (UP) flag, and signature over `authenticatorData`+`clientDataHash`.
- Store the credential id, public key, signature counter, transports, and the AAGUID for later UX.

