
- **should-group-permission-gated-code**: Files that all request or check the same permission **SHOULD** be in the same scope group — permission-gated code clusters.
- **should-separate-entitlement-groups**: If one candidate group requires an entitlement that others do not, they **SHOULD** be treated as distinct operational units — entitlements define hard boundaries.
- **should-flag-version-gated-features**: Code behind an OS version gate such as `@available(iOS 16.0, *)` **SHOULD** be flagged as a version-gated feature within its scope group — OS version gates mark optional feature envelopes.
- **may-give-large-version-gated-code-own-group**: If version-gated code constitutes a large portion of the group, it **MAY** warrant its own scope group.
- **should-group-environment-specific-code**: Environment-specific code — code that reads environment variables, loads config files, or applies build-time conditionals — **SHOULD** typically belong in one configuration scope group rather than scattered.
- **should-document-feature-flags**: The analysis **SHOULD** document the feature flags in feature-flagged code.
- **should-not-group-unenabled-code-paths**: The analysis **SHOULD NOT** create scope groups around unenabled code paths — feature-flagged code is pre-production.
- **should-note-remote-config-ordering**: Code that requires a remote config fetch before it can function **SHOULD** be noted as an operational ordering constraint — remote config dependencies imply a network prerequisite.
- **must-identify-new-runtime-conditions-with-gated-code**: Every NEW permission or entitlement requirement, environment prerequisite, or feature-flag dependency introduced by the change MUST be identified with the code it gates.
