
- Put properties shared by every project in a `Directory.Build.props` at the repository or solution root: `TargetFramework`, `LangVersion`, `Nullable`, `TreatWarningsAsErrors`, analyzers. MSBuild imports it early, so the project can still override a value. `Directory.Build.targets` is imported late and is the place for logic that must see the project's final values.
- The file name must match exactly, including case, because Linux file systems are case-sensitive. `Directory.Build.props` is not `directory.build.props`.
- Set `ContinuousIntegrationBuild` to `true` in CI builds for reproducible output.
- Do not set `OutDir` to change output folders, because it bypasses the per-project subfolders. Use `BaseOutputPath`.

