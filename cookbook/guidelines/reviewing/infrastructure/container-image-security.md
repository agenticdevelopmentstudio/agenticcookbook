---
id: 9f07e740-097e-4814-badf-fa3ae8d7d1e9
title: "Container image security"
domain: agenticdevelopercookbook://guidelines/reviewing/infrastructure/container-image-security
type: guideline
version: 1.0.1
status: accepted
language: en
created: 2026-06-09
modified: 2026-06-10
author: Mike Fullerton
copyright: 2026 Mike Fullerton
license: MIT
summary: "Scan, pin, sign, and slim container images so they ship without known-exploited vulnerabilities, embedded secrets, or root runtimes."
platforms: []
tags:
  - security
  - containers
  - supply-chain
depends-on: []
related:
  - agenticdevelopercookbook://guidelines/shipping/supply-chain-integrity
  - agenticdevelopercookbook://guidelines/reviewing/security/vulnerability-prioritization
  - agenticdevelopercookbook://guidelines/implementing/infrastructure/containerization
references:
  - https://github.com/aquasecurity/trivy
  - https://docs.sigstore.dev/cosign/signing/signing_with_containers/
  - https://slsa.dev/spec/v1.0/provenance
  - https://nvlpubs.nist.gov/nistpubs/specialpublications/nist.sp.800-190.pdf
approved-by: "approve-artifact v1.0.0"
approved-date: "2026-06-10"
triggers:
  - security-review
  - dependency-management
---

# Container image security

A container image is a deployable supply-chain artifact: its layers carry every OS package, language dependency, and file that runs in production. Securing it means scanning for known vulnerabilities, pinning and slimming its base, signing it, and keeping secrets and root out of the runtime.

## Scan and gate

- Images **MUST** be scanned for vulnerabilities in CI before any push to a registry, using a maintained scanner (e.g. Trivy, Grype, or Snyk).
- Gate on exploitability, not raw severity. Cross-reference `agenticdevelopercookbook://guidelines/reviewing/security/vulnerability-prioritization`: builds **MUST** fail on findings in the CISA KEV catalog and **SHOULD** fail on high EPSS scores, rather than blocking on every high-CVSS CVE.
- Images **MUST NOT** ship with unaddressed known-exploited (KEV) vulnerabilities.
- Re-scan published images on a schedule (e.g. daily). New CVEs are disclosed against images that were clean at build time, so point-in-time scanning is insufficient.
- Suppressions (`.trivyignore` and equivalents) **MUST** carry a justification and an expiry/review date; permanent blanket ignores are forbidden.

## Pin and slim the base

- Base images **MUST** be pinned by immutable digest (`FROM image@sha256:...`), not by a mutable tag like `latest`. Tags are reassignable; digests are not.
- Prefer a minimal or distroless base (e.g. `distroless`, `alpine`, `wolfi`, or `scratch`) to shrink the attack surface — fewer packages means fewer CVEs and a smaller blast radius.
- Use multi-stage builds so compilers, build tools, and dev dependencies stay out of the final image.
- Rebuild on a cadence so base-image security patches actually reach production; a digest pin freezes patches as well as drift.

## Sign and verify provenance

- Images **MUST** be signed (e.g. with Sigstore cosign, keyless via OIDC where available) and signatures **MUST** be verified at deploy time before the workload is admitted.
- Each image **MUST** emit an SBOM (SPDX or CycloneDX) recording its contents. Cross-reference `agenticdevelopercookbook://guidelines/shipping/supply-chain-integrity` for SBOM and attestation handling.
- Generate SLSA build provenance attestations and require them at admission where the platform supports it.
- Admission enforcement (e.g. an admission controller verifying signature and provenance policy) is **adopt-when-measured-need-justifies** per YAGNI — start with deploy-time `cosign verify`, and add cluster-level enforcement when the threat model warrants it.

## Harden the runtime

- The runtime **MUST** run as a non-root user; set an explicit `USER` and avoid UID 0.
- Secrets **MUST NOT** be baked into any layer — not in `ENV`, build args, or copied files. Layers are world-readable to anyone who pulls the image; inject secrets at runtime instead. Scan layer history (e.g. with a secret scanner) to confirm.
- Set a read-only root filesystem and drop unneeded Linux capabilities where the workload allows.
- Do not embed long-lived registry or cloud credentials in the image; use workload identity or short-lived tokens.

> Privacy and data-handling expectations around image contents are engineering guidance, not legal advice; consult counsel for regulatory obligations.

## Change History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 1.0.1 | 2026-06-10 | Mike Fullerton | Add cosign signing, SLSA provenance, NIST SP 800-190 sources |
| 1.0.0 | 2026-06-09 | Mike Fullerton | Initial creation |
