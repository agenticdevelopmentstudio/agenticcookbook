
1. **TLS version** — TLS 1.2 minimum is REQUIRED, TLS 1.3 SHOULD be preferred. Verify TLS 1.0 and 1.1 are disabled entirely.
2. **HSTS** — all production domains MUST have the header: `Strict-Transport-Security: max-age=31536000; includeSubDomains; preload`. Submit to the [HSTS preload list](https://hstspreload.org/).
3. **Cipher suites** — verify the server uses Mozilla's "Intermediate" or "Modern" TLS configuration. Prefer AEAD ciphers (AES-GCM, ChaCha20-Poly1305).
4. **Certificate pinning** (mobile apps only) — pin to the intermediate CA (not the leaf). Verify backup pins are included and a recovery plan exists. Consider Certificate Transparency monitoring as a lighter alternative.

