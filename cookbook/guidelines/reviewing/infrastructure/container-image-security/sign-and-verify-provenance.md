
- Images **MUST** be signed (e.g. with Sigstore cosign, keyless via OIDC where available) and signatures **MUST** be verified at deploy time before the workload is admitted.
- Each image **MUST** emit an SBOM (SPDX or CycloneDX) recording its contents. Cross-reference `agenticdevelopercookbook://guidelines/shipping/supply-chain-integrity` for SBOM and attestation handling.
- Generate SLSA build provenance attestations and require them at admission where the platform supports it.
- Admission enforcement (e.g. an admission controller verifying signature and provenance policy) is **adopt-when-measured-need-justifies** per YAGNI — start with deploy-time `cosign verify`, and add cluster-level enforcement when the threat model warrants it.

