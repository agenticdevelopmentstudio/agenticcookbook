
- `should-group-permission-gated-code`: Files that request or check the same permission share an operational prerequisite and a failure mode when the permission is denied.
- `should-separate-entitlement-groups`: Code that requires an entitlement cannot run without it.
- `should-flag-version-gated-features`: Code behind `@available(iOS 16.0, *)` is conditionally executable.
- `should-group-environment-specific-code`: Environment-specific code is configuration infrastructure.
- `should-not-group-unenabled-code-paths`: Large blocks of feature-flagged code indicate in-flight work.
- `should-note-remote-config-ordering`: Code that requires a remote config fetch before it can function has an implicit startup dependency.
