
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

