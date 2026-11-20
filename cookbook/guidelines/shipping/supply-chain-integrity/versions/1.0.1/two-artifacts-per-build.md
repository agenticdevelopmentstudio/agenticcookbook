
Every release build **MUST** produce, alongside the binary/package:

- **An SBOM** (Software Bill of Materials) listing every component and version. Use **CycloneDX** or **SPDX** — both are widely tooled; pick one and stay consistent.
- **Signed build provenance** describing *what* built the artifact, *how*, and from *which* inputs (source commit, builder identity, parameters).

