# implement-feature-management — leaves

- [`implement-feature-management/ab-testing`](leaves/ab-testing.md) — A/B testing · Features that may need experimentation SHOULD support variant assignment via an `ExperimentProvider` interface (`vari... · triggers: feature-flags, logging · rules: 1 SHOULD
- [`implement-feature-management/debug-mode`](leaves/debug-mode.md) — Debug mode · Apps MUST include a debug-only configuration panel (not in release builds): · platforms: ios, kotlin, macos, typescript, web, windows · triggers: feature-flags, logging · rules: 2 MUST
- [`implement-feature-management/feature-flags`](leaves/feature-flags.md) — Feature flags · All features MUST be gated behind feature flags from initial implementation. Define a `FeatureFlagProvider` interface... · platforms: csharp, kotlin, swift, typescript · triggers: feature-flags, new-module · rules: 2 MUST 1 SHOULD
