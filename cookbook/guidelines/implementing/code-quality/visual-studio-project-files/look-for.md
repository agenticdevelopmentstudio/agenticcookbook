
Review project-file changes against Visual Studio project files ([adc.guideline.implementing.code-quality.visual-studio-project-files](cookbook:9ed898fe-ba86-44be-9911-d24fea60dc90)).

- `must-use-sdk-style-csproj`: a `.csproj` whose root element is not `<Project Sdk="...">` for the project's SDK
- `must-not-list-source-files`: Projects are SDK-style and do not enumerate source files that the SDK already includes.
- `must-add-items-only-for-glob-misses`: Added items are for files the default globs miss.
- `must-not-hand-edit-old-style-projects`: a hand edit to an old-style project file instead of a conversion
- `should-set-implicit-usings-explicitly`: implicit global usings left to the template's default with no explicit property
- `should-share-properties-in-directory-build-props`: A property that applies to every project is in `Directory.Build.props`, not repeated in each project.
- `should-put-late-logic-in-directory-build-targets`: logic that needs the project's final values placed in `Directory.Build.props` or a project file instead of `Directory.Build.targets`
- `must-match-directory-build-props-case`: The `Directory.Build.props` file name has exact casing.
- `should-set-continuous-integration-build`: CI sets `ContinuousIntegrationBuild`.
- `must-not-set-outdir`: Output folders use `BaseOutputPath`, not `OutDir`.
- `should-manage-package-versions-centrally`: `PackageReference` has no `Version` when central management is on, and the version is in `Directory.Packages.props`.
- `must-import-parent-packages-props`: A nested `Directory.Packages.props` imports its parent.
- `must-use-version-override-only-for-documented-exception`: Every `VersionOverride` has a reason.
- `may-forbid-version-override`: nothing to flag in itself; where `CentralPackageVersionOverrideEnabled` is `false`, no `VersionOverride` appears
- `should-manage-solution-with-dotnet-sln`: Solution edits were made with `dotnet sln` and list every project.
- `should-have-one-solution-per-deployable-unit`: a deployable unit with no solution of its own, or several solutions for one unit
- `must-list-every-project-in-solution`: a project in the repository missing from its solution
- `must-not-contain-machine-specific-content`: The diff has no absolute or user-specific path.
