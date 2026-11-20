
# Privacy and security by default

Collect only what you need, prefer on-device processing, and require opt-in for non-essential data. Store secrets in platform keystores, never in plaintext.

### Data minimization

Collect only what is needed. Prefer on-device processing.

### Consent

Opt-in for non-essential data collection. Honor "deny" gracefully — the app must remain functional.

### Secure storage

Tokens and credentials MUST use platform secure storage (Keychain, EncryptedSharedPreferences, DPAPI, HttpOnly cookies).

### No PII logging

Never log personally identifiable information, even at debug level.

### TLS only

All network communication MUST use HTTPS.

### Input sanitization

Sanitize all user input before display (prevent XSS, injection).

Each spec SHOULD include a **Privacy** section documenting data collected and how it is stored.

---

# Privacy

Privacy and security must be built in from day one. Collect only what is needed. Prefer on-device processing. Opt-in for non-essential data collection. Honor "deny" gracefully — the app must remain functional. No PII in logs, even at debug level. All network communication MUST use HTTPS.

