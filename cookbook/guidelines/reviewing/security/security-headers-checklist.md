---
id: c82c02a1-ec15-4892-94b9-0a936eaf2ba7
title: "Security Headers Checklist"
domain: agenticdevelopercookbook://guidelines/reviewing/security/security-headers-checklist
type: guideline
version: 1.0.3
status: accepted
language: en
created: 2026-03-27
modified: 2026-10-04
author: Mike Fullerton
copyright: 2026 Mike Fullerton
license: MIT
summary: "Every web application MUST set the standard security response headers: HSTS, Content-Security-Policy, X-Content-Type-Options, X-Frame-Options, Referrer-Policy, Permissions-Policy, and Cache-Control."
platforms:
  - web
tags:
  - security
  - security-headers-checklist
depends-on: []
related: []
references: []
approved-by: "approve-artifact v1.0.0"
approved-date: "2026-04-04"
triggers:
  - security-review
  - pre-pr
---

# Security Headers Checklist

Every web application MUST set these response headers:

```
Strict-Transport-Security: max-age=31536000; includeSubDomains; preload
Content-Security-Policy: default-src 'none'; script-src 'nonce-{random}' 'strict-dynamic'; ...
X-Content-Type-Options: nosniff
X-Frame-Options: DENY
Referrer-Policy: strict-origin-when-cross-origin
Permissions-Policy: camera=(), microphone=(), geolocation=()
Cache-Control: no-store  (for sensitive responses)
```

## Change History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 1.0.3 | 2026-10-04 | Mike Fullerton | Complete the summary, which was cut off |
| 1.0.2 | 2026-04-09 | Mike Fullerton | Add trigger tags |
| 1.0.1 | 2026-04-09 | Mike Fullerton | Reorganize into use-case directory |
| 1.0.0 | 2026-03-27 | Mike Fullerton | Initial creation |
