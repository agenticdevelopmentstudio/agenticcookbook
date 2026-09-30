<!-- leaf: ship-general/transport-security · source: guidelines/shipping/transport-security.md -->

**Rules** (cite as `ship-general/transport-security#<slug>`):

- `tls-version` MUST — TLS 1.2 minimum is REQUIRED, TLS 1.3 SHOULD be preferred. Verify TLS 1.0 and 1.1 are disabled entirely.
- `hsts` MUST — all production domains MUST have the header: Strict-Transport-Security: max-age=31536000; includeSubDomains; preload. …

# Transport Security

Before deploying, verify transport security meets these requirements.

## Pre-deploy checklist

1. **TLS version** — TLS 1.2 minimum is REQUIRED, TLS 1.3 SHOULD be preferred. Verify TLS 1.0 and 1.1 are disabled entirely.
2. **HSTS** — all production domains MUST have the header: `Strict-Transport-Security: max-age=31536000; includeSubDomains; preload`. Submit to the [HSTS preload list](https://hstspreload.org/).
3. **Cipher suites** — verify the server uses Mozilla's "Intermediate" or "Modern" TLS configuration. Prefer AEAD ciphers (AES-GCM, ChaCha20-Poly1305).
4. **Certificate pinning** (mobile apps only) — pin to the intermediate CA (not the leaf). Verify backup pins are included and a recovery plan exists. Consider Certificate Transparency monitoring as a lighter alternative.

## Verification tools

- `curl -vI https://yourdomain.com` — check TLS version and certificate chain
- [SSL Labs Server Test](https://www.ssllabs.com/ssltest/) — comprehensive TLS audit
- Mozilla Observatory — checks HSTS, CSP, and other security headers

References:
- [OWASP TLS Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Transport_Layer_Security_Cheat_Sheet.html)
- [Mozilla Server Side TLS](https://wiki.mozilla.org/Security/Server_Side_TLS)
- [RFC 8446: TLS 1.3](https://datatracker.ietf.org/doc/html/rfc8446)
