
# Security Testing

Security scans MUST be run as part of post-generation verification ([adc.guideline.testing.post-generation-verification](cookbook:563aebde-52bf-4011-8907-ecc473fd942c)). These are CLI tools
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

See the security guidelines under `guidelines/implementing/security/` for the full security reference.

