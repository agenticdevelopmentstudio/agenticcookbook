<!-- leaf: implement-security/passkeys-and-webauthn · source: guidelines/implementing/security/passkeys-and-webauthn.md -->

**Rules** (cite as `implement-security/passkeys-and-webauthn#<slug>`):

- `key-new-apps-offer-passkeys-primary-authenticator` SHOULD — Passkeys are FIDO2/WebAuthn public-key credentials that replace passwords with phishing-resistant, origin-bound key …
- `rp-backend-generate-cryptographically-random-challenge` MUST — The RP backend MUST generate a cryptographically random challenge (≥16 bytes), bind it to the session, and verify it …
- `server-verification-confirm-challenge-match-origin` MUST — Server verification MUST confirm: challenge match, origin, rp.id hash, the user-present (UP) flag, and signature over …
- `non-increasing-counter-treated-possible-cloning-flagged` SHOULD — If the stored signature counter is non-zero, a non-increasing counter SHOULD be treated as possible cloning and flagged.
- `users-synced-passkeys-default-admin-high-privilege` SHOULD — For most users, synced passkeys SHOULD be the default. For admin/high-privilege accounts, a device-bound authenticator …
- `users-encouraged-register-least-two` SHOULD — Users SHOULD be encouraged to register at least two authenticators so loss of one does not lock them out.
- `passkeys-primary-factor-passwords-kept` SHOULD — Passkeys SHOULD be the primary factor; passwords, if kept, are a fallback — never the inverse.
- `apps-not-rely-sms-otp-security` SHOULD — Apps SHOULD NOT rely on SMS-OTP as a security factor (SIM-swap and interception risk); use it at most for low-risk …
- `verification-replay-risk-not` MUST — Reusing or omitting server-side challenge verification (replay risk) — MUST NOT.

# Passkeys and WebAuthn

Passkeys are FIDO2/WebAuthn public-key credentials that replace passwords with phishing-resistant, origin-bound key pairs. The private key never leaves the authenticator; the relying party (RP) stores only the public key. New apps **SHOULD** offer passkeys as the primary authenticator.

## Standards baseline (pin and track)

- Target the **W3C WebAuthn Level 2 Recommendation** (`webauthn-2`) for stable, broadly-implemented behavior.
- **WebAuthn Level 3** (`webauthn-3`) is a **W3C Candidate Recommendation (2026-01-13)** — FORECAST: treat its newer features (e.g. refined attestation, related-origin requests) as evolving; do not depend on them as universally available until they reach Recommendation.
- Authenticator protocol is **FIDO CTAP 2.x**; security keys speak CTAP, platform authenticators are reached via the OS (Android Credential Manager, iOS/macOS AutoFill, Windows Hello).

## Registration ceremony (`navigator.credentials.create`)

- The RP backend **MUST** generate a cryptographically random `challenge` (≥16 bytes), bind it to the session, and verify it server-side on return.
- Set `rp.id` to the registrable domain; set `user.id` to an opaque, stable, non-PII handle (not an email).
- Server verification **MUST** confirm: challenge match, `origin`, `rp.id` hash, the user-present (UP) flag, and signature over `authenticatorData`+`clientDataHash`.
- Store the credential id, public key, signature counter, transports, and the AAGUID for later UX.

## Authentication ceremony (`navigator.credentials.get`)

- Issue a fresh server-side `challenge` per attempt; verify origin, `rp.id`, UP flag, and signature against the stored public key.
- If the stored signature counter is non-zero, a **non-increasing** counter **SHOULD** be treated as possible cloning and flagged.
- Prefer **discoverable credentials** (resident keys) so users authenticate without first entering a username.

## Authenticator and passkey types

- **Platform authenticators** (Face ID, Windows Hello) vs **roaming authenticators** (FIDO2 security keys via USB/NFC/BLE).
- **Synced passkeys** replicate via a provider (iCloud Keychain, Google Password Manager); convenient, recover across devices. **Device-bound passkeys** never leave one device; highest assurance.
- For most users, synced passkeys **SHOULD** be the default. For admin/high-privilege accounts, a **device-bound** authenticator (security key) **SHOULD** be required.
- Users **SHOULD** be encouraged to register **at least two** authenticators so loss of one does not lock them out.

## Attestation

- Request attestation (`attestation: "direct"`) **only** when policy needs to verify authenticator make/model. MEASURED-NEED: adopt attestation verification ONLY when a concrete requirement (e.g. regulated environment, hardware allowlist) justifies it (per YAGNI).
- Note: **synced passkeys do not provide attestation**; enforcing attestation excludes them. Use `attestation: "none"` for consumer flows.

## Fallback and recovery

- Passkeys **SHOULD** be the primary factor; passwords, if kept, are a fallback — never the inverse.
- Apps **SHOULD NOT** rely on **SMS-OTP** as a security factor (SIM-swap and interception risk); use it at most for low-risk recovery, never as the sole step-up.
- Provide an explicit, rate-limited account-recovery path (e.g. verified email magic link plus identity proofing) for users who lose all authenticators.
- Always allow registering additional passkeys from an authenticated session.

## Anti-patterns

- Reusing or omitting server-side challenge verification (replay risk) — **MUST NOT**.
- Setting `rp.id` to a host that doesn't cover the auth origin.
- Treating a passkey as a bearer secret or syncing the RP private key (there is none server-side).
