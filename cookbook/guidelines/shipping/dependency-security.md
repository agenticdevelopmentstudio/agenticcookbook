---
id: 793bd9f6-b029-4c4e-aca5-d253f9fab48e
title: "Dependency Security"
domain: agenticdevelopercookbook://guidelines/shipping/dependency-security
type: guideline
version: 1.1.1
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
  - https://www.infoq.com/news/2026/05/pip-261-dependency-cooldowns/
  - https://safedep.io/mass-npm-supply-chain-attack-tanstack-mistral/
  - https://dev.to/maxkrivich/ai-coding-agent-security-practical-guardrails-for-claude-code-copilot-and-codex-och
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

## Agent install guardrails

An AI agent MUST NOT freely install packages. Constrain what it can pull:

- **Allowlist, enforced deterministically** — scope an explicit package/registry allowlist to the
  task or session and enforce it through DETERMINISTIC gates (pre-install hooks, CI checks, sandbox
  policy), NOT prompt text. Agents can ignore prompt instructions, so prose alone MUST NOT be the
  only control.
- **Registry cooldown** — apply a cooldown window (e.g. pip's dependency cooldown) so brand-new
  releases are not auto-pulled, reducing exposure to freshly compromised versions.
- **Human-in-the-loop approval** — any NEW dependency MUST require explicit human approval before it
  is added or merged.
- **Verify existence and maintenance (anti-slopsquatting)** — before adding a candidate package,
  confirm it actually exists and is actively maintained; an agent MUST NOT install a hallucinated or
  abandoned name. Cross-reference [reuse-before-build](agenticdevelopercookbook://guidelines/planning/code-quality/reuse-before-build).

References:
- [OWASP Dependency-Check](https://owasp.org/www-project-dependency-check/)
- [SLSA Framework](https://slsa.dev/)
- [Sigstore](https://www.sigstore.dev/)

## Change History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 1.1.1 | 2026-06-10 | Mike Fullerton | Add recovered Tier-1 research sources (adversarially-audited) |
| 1.1.0 | 2026-06-09 | Mike Fullerton | Add agent dependency-install guardrails |
| 1.0.2 | 2026-04-09 | Mike Fullerton | Add trigger tags |
| 1.0.1 | 2026-04-09 | Mike Fullerton | Reorganize into use-case directory |
| 1.0.0 | 2026-03-27 | Mike Fullerton | Initial creation |
