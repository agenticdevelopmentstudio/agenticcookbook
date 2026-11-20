
1. **Permission-gated code clusters.** Files that all request or check the same permission belong together — they share an operational prerequisite and a failure mode when the permission is denied.
2. **Entitlements define hard boundaries.** Code that requires an entitlement cannot run without it. If one candidate group requires an entitlement that others do not, they are distinct operational units.
3. **OS version gates mark optional feature envelopes.** Code behind `@available(iOS 16.0, *)` is conditionally executable — flag it as a version-gated feature within its scope group. If it constitutes a large portion of the group, it may warrant its own scope group.
4. **Environment-specific code belongs in a configuration scope group.** Code that reads environment variables, loads config files, or applies build-time conditionals is configuration infrastructure — it typically belongs in one scope group rather than scattered.
5. **Feature-flagged code is pre-production.** Large blocks of feature-flagged code indicate in-flight work. Document the flags but do not create scope groups around unenabled code paths.
6. **Remote config dependencies imply a network prerequisite.** Code that requires a remote config fetch before it can function has an implicit startup dependency — note this as an operational ordering constraint.

