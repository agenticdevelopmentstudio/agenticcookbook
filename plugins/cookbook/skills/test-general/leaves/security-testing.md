<!-- leaf: test-general/security-testing · source: guidelines/testing/security-testing.md -->

**Rules** (cite as `test-general/security-testing#<slug>`):

- `security-scans-run-part-post-generation` MUST — Security scans MUST be run as part of post-generation verification …

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
