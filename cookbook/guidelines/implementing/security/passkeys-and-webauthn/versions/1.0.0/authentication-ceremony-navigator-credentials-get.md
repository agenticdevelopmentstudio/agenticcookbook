
- Issue a fresh server-side `challenge` per attempt; verify origin, `rp.id`, UP flag, and signature against the stored public key.
- If the stored signature counter is non-zero, a **non-increasing** counter **SHOULD** be treated as possible cloning and flagged.
- Prefer **discoverable credentials** (resident keys) so users authenticate without first entering a username.

