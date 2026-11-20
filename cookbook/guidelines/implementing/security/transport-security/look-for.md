
Before deploying, verify transport security meets these requirements.

- `must-require-tls-1-2-minimum`: **TLS version** — TLS 1.2 minimum is REQUIRED, TLS 1.3 SHOULD be preferred.
- `must-disable-tls-1-0-and-1-1`: Verify TLS 1.0 and 1.1 are disabled entirely.
- `must-enable-hsts-on-production-domains`: **HSTS** — all production domains MUST have the header: `Strict-Transport-Security: max-age=31536000; includeSubDomains; preload`.
- `should-submit-to-hsts-preload-list`: Submit to the [HSTS preload list](https://hstspreload.org/).
- `should-use-mozilla-tls-configuration`: **Cipher suites** — verify the server uses Mozilla's "Intermediate" or "Modern" TLS configuration.
- `should-prefer-aead-ciphers`: Prefer AEAD ciphers (AES-GCM, ChaCha20-Poly1305).
- `should-pin-to-intermediate-ca`: **Certificate pinning** (mobile apps only) — pin to the intermediate CA (not the leaf).
- `must-include-backup-pins-and-recovery-plan`: Verify backup pins are included and a recovery plan exists.
- `should-consider-certificate-transparency-monitoring`: Consider Certificate Transparency monitoring as a lighter alternative.
- `should-pin-only-on-mobile`: certificate pinning in a web app rather than a mobile app
- `must-not-expose-plain-http-endpoints`: a production domain that exposes a plain-HTTP endpoint
