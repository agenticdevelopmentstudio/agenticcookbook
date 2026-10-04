---
id: b9da0bd1-a7e4-491f-beb0-46f7b5c19d86
title: "Security Testing"
domain: agenticdevelopercookbook://guidelines/reviewing/testing/security-testing
type: guideline
version: 1.0.4
status: accepted
language: en
created: 2026-03-27
modified: 2026-10-04
author: Mike Fullerton
copyright: 2026 Mike Fullerton
license: MIT
summary: "Run security scans as part of post-generation verification: static analysis (SAST), dependency scanning, and dynamic analysis (DAST), using CLI tools Claude Code can invoke directly."
platforms:
  - csharp
  - kotlin
  - python
  - swift
  - typescript
  - web
tags:
  - security-testing
  - testing
depends-on: []
related:
  - agenticdevelopercookbook://guidelines/testing/post-generation-verification
references:
  - https://codeql.github.com/
  - https://github.com/PyCQA/bandit
  - https://semgrep.dev/
  - https://snyk.io/
  - https://www.zaproxy.org/
approved-by: "approve-artifact v1.0.0"
approved-date: "2026-06-09"
triggers:
  - writing-tests
  - security-review
---

# Security Testing

Security scans MUST be run as part of post-generation verification (agenticdevelopercookbook://guidelines/testing/post-generation-verification). These are CLI tools
Claude Code can invoke directly.

**Static Analysis (SAST):**
- [Semgrep](https://semgrep.dev/) — all languages: `semgrep scan --config=auto .`
- [Bandit](https://github.com/PyCQA/bandit) — Python: `bandit -r src/`
- [CodeQL](https://codeql.github.com/) — deep analysis (Swift, Kotlin, C#, Python, TS, Go)

**Dependency Scanning:**
- Python: `pip-audit`
- Node.js: `npm audit`
- .NET: `dotnet list package --vulnerable`
- All: [Snyk](https://snyk.io/) CLI (`snyk test`)

**Dynamic Analysis (DAST):**
- [OWASP ZAP](https://www.zaproxy.org/) — scan running web services: `zap-cli quick-scan http://localhost:8888`

See agenticdevelopercookbook://guidelines/implementing/security/* (Security Guidelines) for the full security reference.

## Change History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 1.0.4 | 2026-10-04 | Mike Fullerton | Complete the summary, which was cut off |
| 1.0.3 | 2026-06-09 | Mike Fullerton | Repair stale cross-reference link scheme |
| 1.0.2 | 2026-04-09 | Mike Fullerton | Add trigger tags |
| 1.0.1 | 2026-04-09 | Mike Fullerton | Reorganize into use-case directory |
| 1.0.0 | 2026-03-27 | Mike Fullerton | Initial creation |
