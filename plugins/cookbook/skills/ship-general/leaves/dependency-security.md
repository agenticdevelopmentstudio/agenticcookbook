<!-- leaf: ship-general/dependency-security · source: guidelines/shipping/dependency-security.md -->

**Rules** (cite as `ship-general/dependency-security#<slug>`):

- `lockfiles-are-mandatory` MUST — package-lock.json, Podfile.lock, gradle.lockfile, poetry.lock, Cargo.lock, packages.lock.json. Lockfiles MUST be …
- `automated-scanning` MUST — CI MUST run npm audit, pip-audit, Dependabot, Snyk, or dotnet list package --vulnerable. Builds MUST fail on …
- `pin-dependencies` MUST — exact versions or narrow ranges. Wildcard (*) or overly broad semver MUST NOT be used.
- `ai-agent-not-freely-install-packages-constrain` MUST — An AI agent MUST NOT freely install packages. Constrain what it can pull:
- `allowlist-enforced-deterministically` MUST — scope an explicit package/registry allowlist to the task or session and enforce it through DETERMINISTIC gates …
- `human-in-the-loop-approval` MUST — any NEW dependency MUST require explicit human approval before it is added or merged.
- `verify-existence-and-maintenance` MUST — before adding a candidate package, confirm it actually exists and is actively maintained; an agent MUST NOT install a …

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
  abandoned name. Cross-reference reuse-before-build.

References:
- [OWASP Dependency-Check](https://owasp.org/www-project-dependency-check/)
- [SLSA Framework](https://slsa.dev/)
- [Sigstore](https://www.sigstore.dev/)
