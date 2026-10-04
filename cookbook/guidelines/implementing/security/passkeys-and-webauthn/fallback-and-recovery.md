
- Passkeys **SHOULD** be the primary factor; passwords, if kept, are a fallback — never the inverse.
- Apps **SHOULD NOT** rely on **SMS-OTP** as a security factor (SIM-swap and interception risk); use it at most for low-risk recovery, never as the sole step-up.
- Provide an explicit, rate-limited account-recovery path (e.g. verified email magic link plus identity proofing) for users who lose all authenticators.
- Always allow registering additional passkeys from an authenticated session.

