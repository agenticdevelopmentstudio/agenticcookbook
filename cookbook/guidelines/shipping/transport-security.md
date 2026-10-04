---
id: b76e80c2-7e24-43cf-b971-5d405e80e748
title: "Transport Security"
domain: agenticdevelopercookbook://guidelines/shipping/transport-security
type: guideline
version: 1.1.1
status: accepted
language: en
created: 2026-03-27
modified: 2026-04-09
author: Mike Fullerton
copyright: 2026 Mike Fullerton
license: MIT
summary: "Pre-deploy transport security verification: TLS 1.2+, HSTS enabled, cipher suites audited, certificate pinning validated."
platforms:
  - typescript
  - web
tags:
  - security
  - transport-security
depends-on: []
related: []
references:
  - https://cheatsheetseries.owasp.org/cheatsheets/Transport_Layer_Security_Cheat_Sheet.html
  - https://datatracker.ietf.org/doc/html/rfc8446
  - https://hstspreload.org/
  - https://wiki.mozilla.org/Security/Server_Side_TLS
approved-by: "approve-artifact v1.0.0"
approved-date: "2026-04-04"
triggers:
  - networking
  - security-review
---

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

## Change History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 1.1.1 | 2026-04-09 | Mike Fullerton | Add trigger tags |
| 1.1.0 | 2026-04-09 | Mike Fullerton | Tailor for shipping use case — focus on pre-deploy verification checklist |
| 1.0.1 | 2026-04-09 | Mike Fullerton | Reorganize into use-case directory |
| 1.0.0 | 2026-03-27 | Mike Fullerton | Initial creation |
