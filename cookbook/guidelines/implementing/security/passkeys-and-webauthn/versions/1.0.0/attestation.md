
- Request attestation (`attestation: "direct"`) **only** when policy needs to verify authenticator make/model. MEASURED-NEED: adopt attestation verification ONLY when a concrete requirement (e.g. regulated environment, hardware allowlist) justifies it (per YAGNI).
- Note: **synced passkeys do not provide attestation**; enforcing attestation excludes them. Use `attestation: "none"` for consumer flows.

