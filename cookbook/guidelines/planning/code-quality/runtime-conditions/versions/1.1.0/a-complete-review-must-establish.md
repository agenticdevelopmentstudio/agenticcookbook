
- `should-group-permission-gated-code`: whether code gated by the same permission sits in one group
- `should-separate-entitlement-groups`: whether groups differing in a required entitlement are kept as distinct operational units
- `should-flag-version-gated-features`: whether every OS version gate is flagged as a version-gated feature in its group
- `may-give-large-version-gated-code-own-group`: whether any version-gated code given its own group is a large portion of its group
- `should-group-environment-specific-code`: whether environment-specific code sits in one configuration group
- `should-document-feature-flags`: whether every feature flag is documented
- `should-not-group-unenabled-code-paths`: whether any scope group is built around unenabled code paths
- `should-note-remote-config-ordering`: whether every remote config dependency is noted as an operational ordering constraint
