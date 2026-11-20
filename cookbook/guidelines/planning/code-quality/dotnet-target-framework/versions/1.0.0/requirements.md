
- **target-current-lts-for-apps**: New applications and services **SHOULD** target the current LTS (`.NET 10` / `net10.0` as of 2026-06-09) to maximize the support runway with predictable upgrades.
- **sts-only-when-needed**: A project **MAY** target an STS release only when it needs an STS-exclusive feature AND the team commits to upgrading before the 24-month window closes. Otherwise prefer LTS.
- **multi-target-libraries**: A reusable library **SHOULD** multi-target the TFMs its consumers actually require (e.g. `<TargetFrameworks>net8.0;net10.0</TargetFrameworks>`), not the newest available. Add a `netstandard2.0` target only when a concrete consumer needs it.
- **pin-the-sdk**: Every repo **MUST** pin the SDK with a `global.json` (`"sdk": { "version": "10.0.x", "rollForward": "latestFeature" }`) so local, CI, and agent builds resolve the same toolchain.
- **state-version-explicitly**: The `TargetFramework(s)` value **MUST** be explicit in the `.csproj`; do not rely on an implicit or inherited default. Do not assume "latest" — name the version.
- **avoid-eol-targets**: A project **MUST NOT** newly target a framework whose end-of-support date has passed or is within the project's planned delivery window. Check the date before committing the TFM.
- **separate-tfm-from-langversion**: Treat `<LangVersion>` as a separate decision from the TFM; raising the language version does not change the runtime or its support window.

