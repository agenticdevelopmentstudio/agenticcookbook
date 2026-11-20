
- `should-use-attestation-none-for-consumers`, `should-request-attestation-only-when-needed`: Note: **synced passkeys do not provide attestation**; enforcing attestation excludes them.
- `must-not-reuse-or-omit-challenge-verification`, `should-not-set-rp-id-outside-auth-origin`, `should-not-treat-passkey-as-bearer-secret`: These are anti-patterns.
