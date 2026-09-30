<!-- leaf: ship-general/msix-packaging · source: guidelines/shipping/msix-packaging.md -->

**Rules** (cite as `ship-general/msix-packaging#<slug>`):

- `capabilities-declared-minimally-package-appxmanifest` MUST — Capabilities MUST be declared minimally in Package.appxmanifest
- `packages-signed-trusted-certificate-sideloading` MUST — Packages MUST be signed with a trusted certificate for sideloading
- `version-numbering-use-major-minor-build` MUST — Version numbering MUST use Major.Minor.Build.Revision, monotonically increasing

# MSIX Packaging

Package Windows apps with the single-project MSIX model, declare minimal capabilities, and sign with a trusted certificate.

- Use the single-project MSIX packaging model
- Capabilities MUST be declared minimally in `Package.appxmanifest`
- Packages MUST be signed with a trusted certificate for sideloading
- Version numbering MUST use `Major.Minor.Build.Revision`, monotonically increasing
