
- Target the **W3C WebAuthn Level 2 Recommendation** (`webauthn-2`) for stable, broadly-implemented behavior.
- **WebAuthn Level 3** (`webauthn-3`) is a **W3C Candidate Recommendation (2026-01-13)** — FORECAST: treat its newer features (e.g. refined attestation, related-origin requests) as evolving; do not depend on them as universally available until they reach Recommendation.
- Authenticator protocol is **FIDO CTAP 2.x**; security keys speak CTAP, platform authenticators are reached via the OS (Android Credential Manager, iOS/macOS AutoFill, Windows Hello).

