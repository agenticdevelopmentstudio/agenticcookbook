---
id: 57ece0cf-b285-4cb2-ab7a-c0b6dd148695
title: "Dependency Security"
domain: agenticdevelopercookbook://guidelines/reviewing/security/dependency-security
type: guideline
version: 1.0.3
status: accepted
language: en
created: 2026-03-27
modified: 2026-06-10
author: Mike Fullerton
copyright: 2026 Mike Fullerton
license: MIT
summary: "Your dependencies are your attack surface. Manage them actively."
platforms:
  - python
  - typescript
tags:
  - dependency-security
  - security
depends-on: []
related: []
references:
  - https://owasp.org/www-project-dependency-check/
  - https://slsa.dev/
  - https://www.sigstore.dev/
  - https://www.first.org/epss/
  - https://www.cisa.gov/known-exploited-vulnerabilities-catalog
  - https://about.gitlab.com/blog/2025/01/07/reduce-supply-chain-risk-with-smarter-vulnerability-prioritization/
approved-by: "approve-artifact v1.0.0"
approved-date: "2026-06-10"
triggers:
  - dependency-management
  - security-review
---

# Dependency Security

Your dependencies are your attack surface. Manage them actively.

- **Lockfiles are mandatory** — `package-lock.json`, `Podfile.lock`, `gradle.lockfile`,
  `poetry.lock`, `Cargo.lock`, `packages.lock.json`. Lockfiles MUST be committed. Use `--frozen-lockfile` /
  `npm ci` / `dotnet restore --locked-mode` in CI.
- **Automated scanning** — CI MUST run `npm audit`, `pip-audit`, Dependabot, Snyk, or `dotnet list
  package --vulnerable`. Builds MUST fail on critical/high vulnerabilities.
- **Pin dependencies** — exact versions or narrow ranges. Wildcard (`*`) or overly broad semver MUST NOT be used.
- **Subresource Integrity (SRI)** — for any CDN-hosted scripts/styles, use `integrity`
  attributes with SHA-384/SHA-512 hashes.
- **Watch for supply chain attacks** — typosquatting, maintainer compromise, malicious
  post-install scripts, dependency confusion (internal/public name collisions).

References:
- [OWASP Dependency-Check](https://owasp.org/www-project-dependency-check/)
- [SLSA Framework](https://slsa.dev/)
- [Sigstore](https://www.sigstore.dev/)

## Change History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 1.0.3 | 2026-06-10 | Mike Fullerton | Add recovered Tier-1 research sources (adversarially-audited) |
| 1.0.2 | 2026-04-09 | Mike Fullerton | Add trigger tags |
| 1.0.1 | 2026-04-09 | Mike Fullerton | Reorganize into use-case directory |
| 1.0.0 | 2026-03-27 | Mike Fullerton | Initial creation |
