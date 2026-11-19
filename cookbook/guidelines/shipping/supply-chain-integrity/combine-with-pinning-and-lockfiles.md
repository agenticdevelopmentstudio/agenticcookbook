
Attestation complements — does not replace — the controls in the dependency-security guideline ([adc.guideline.implementing.security.dependency-security](cookbook:b712c766-af1f-4716-b8fb-34bf0bbb13eb)):

- Commit lockfiles; install with the frozen/locked flag in CI so resolution is deterministic.
- Pin dependencies (and CI actions) by version, ideally by digest/hash, not floating tags.
- Keep scanning for known-vulnerable components — it answers a different question (*is this version exploitable?*) than provenance (*did this come from where I think?*).

