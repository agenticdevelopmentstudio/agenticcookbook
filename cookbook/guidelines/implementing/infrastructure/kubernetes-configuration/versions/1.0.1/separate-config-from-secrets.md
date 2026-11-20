
- **non-sensitive-config**: Non-sensitive configuration (feature flags, URLs, tuning values) **MUST** live in ConfigMaps, not baked into images.
- **sensitive-in-secrets**: Credentials, tokens, TLS keys, and connection strings **MUST** be stored as Secrets (or sourced from an external manager), never as ConfigMaps.
- **no-plaintext-in-vcs**: Plaintext secret values **MUST NOT** be committed to manifests, Helm values, or any file in version control, and **MUST NOT** be baked into image layers or build args.

