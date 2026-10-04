
Attestation complements — does not replace — the controls in the dependency-security guideline (`agenticdevelopercookbook://guidelines/shipping/dependency-security`):

- Commit lockfiles; install with the frozen/locked flag in CI so resolution is deterministic.
- Pin dependencies (and CI actions) by version, ideally by digest/hash, not floating tags.
- Keep scanning for known-vulnerable components — it answers a different question (*is this version exploitable?*) than provenance (*did this come from where I think?*).

