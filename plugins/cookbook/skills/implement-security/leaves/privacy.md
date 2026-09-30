<!-- leaf: implement-security/privacy · source: guidelines/implementing/security/privacy.md -->

**Rules** (cite as `implement-security/privacy#<slug>`):

- `tokens-credentials-use-platform-secure-storage` MUST — Tokens and credentials MUST use platform secure storage (Keychain, EncryptedSharedPreferences, DPAPI, HttpOnly cookies).
- `network-communication-use-https` MUST — All network communication MUST use HTTPS.
- `spec-include-privacy-section-documenting` SHOULD — Each spec SHOULD include a Privacy section documenting data collected and how it is stored.
- `level-network-communication-use-https` MUST — Privacy and security must be built in from day one. Collect only what is needed. Prefer on-device processing. Opt-in …
- `tls-only` MUST — All network communication MUST use HTTPS.

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

## Swift

Support App Tracking Transparency, App Privacy Report, and Private Relay compatibility. Include `NS*UsageDescription` keys with human-readable explanations for all permission prompts.

## Kotlin

Respect scoped storage, support per-app language preferences, and honor permission denials gracefully. Show rationale dialogs before runtime permission requests.

## TypeScript

1. **Content Security Policy**: Configure CSP headers to restrict script sources and prevent XSS.
2. **HttpOnly cookies**: Use HttpOnly secure cookies for authentication tokens. Never store tokens in `localStorage`.
3. **Input sanitization**: Sanitize all user input before display to prevent XSS and injection.
4. **TLS only**: All network communication MUST use HTTPS.
5. Minimize third-party scripts. Respect the Do Not Track header.

## C#

- Declare only required capabilities in `Package.appxmanifest` — avoid `broadFileSystemAccess` unless essential
- Use DPAPI for local secret storage (see secure-storage.md)
- No PII in logs, even at debug level
- Respect user consent: app must remain functional if optional data collection is denied
