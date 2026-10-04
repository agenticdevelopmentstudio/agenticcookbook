
1. **Variant assignment works** — the `ExperimentProvider` interface (`variant(key) -> String`) returns valid variants for all experiment keys used by the feature.
2. **Default variant is safe** — when the experiment provider is unavailable or returns an unknown key, the feature SHOULD fall back to the control (default) variant.
3. **Debug panel override works** — verify the debug panel can force each variant locally for QA testing.

