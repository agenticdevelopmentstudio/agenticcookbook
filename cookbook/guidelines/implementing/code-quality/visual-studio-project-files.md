---
id: 9ed898fe-ba86-44be-9911-d24fea60dc90
title: "Visual Studio project files"
domain: agenticdevelopercookbook://guidelines/implementing/code-quality/visual-studio-project-files
type: guideline
version: 1.0.0
status: accepted
language: en
created: 2026-10-09
modified: 2026-10-09
author: Mike Fullerton
copyright: 2026 Mike Fullerton
license: MIT
summary: "Keep .NET and Visual Studio projects SDK-style and small, share properties through Directory.Build.props, manage package versions centrally and keep solution files tidy."
platforms:
  - windows
  - linux
  - macos
languages:
  - csharp
tags:
  - visual-studio
  - msbuild
  - csproj
  - dotnet
  - nuget
  - solution
depends-on: []
related:
  - agenticdevelopercookbook://guidelines/implementing/code-quality/nullable-reference-types
  - agenticdevelopercookbook://guidelines/implementing/code-quality/linting
  - agenticdevelopercookbook://guidelines/implementing/platform-integration/wsl
  - agenticdevelopercookbook://guidelines/reviewing/code-quality/visual-studio-project-files
  - agenticdevelopercookbook://principles/dry
references:
  - https://learn.microsoft.com/en-us/dotnet/core/project-sdk/overview
  - https://learn.microsoft.com/en-us/visualstudio/msbuild/customize-by-directory
  - https://learn.microsoft.com/en-us/nuget/consume-packages/central-package-management
  - https://learn.microsoft.com/en-us/dotnet/core/tools/dotnet-sln
  - https://learn.microsoft.com/en-us/dotnet/core/project-sdk/msbuild-props
approved-by: "approve-artifact v1.0.0"
approved-date: "2026-10-09"
triggers:
  - configuration
  - new-module
  - dependency-management
---

# Visual Studio project files

.NET projects are MSBuild files. The rules keep them short, identical across projects and reviewable.

## SDK-style projects

- Every project uses an SDK-style `.csproj` whose root element is `<Project Sdk="Microsoft.NET.Sdk">` (or the SDK that matches the project type). The SDK imports its props and targets implicitly.
- Do not list source files. The SDK includes `Compile`, `EmbeddedResource` and `None` items by glob and leaves out `bin` and `obj`. Listing a default item again fails with error NETSDK1022. Add an item only to include something the glob misses, and use `Remove` to exclude.
- Do not hand-edit the old-style project format. Convert it.
- Implicit global usings (from .NET 6) are an SDK feature; turn them on or off explicitly with a property rather than relying on a template.

## Shared properties

- Put properties shared by every project in a `Directory.Build.props` at the repository or solution root: `TargetFramework`, `LangVersion`, `Nullable`, `TreatWarningsAsErrors`, analyzers. MSBuild imports it early, so the project can still override a value. `Directory.Build.targets` is imported late and is the place for logic that must see the project's final values.
- The file name must match exactly, including case, because Linux file systems are case-sensitive. `Directory.Build.props` is not `directory.build.props`.
- Set `ContinuousIntegrationBuild` to `true` in CI builds for reproducible output.
- Do not set `OutDir` to change output folders, because it bypasses the per-project subfolders. Use `BaseOutputPath`.

## Central package management

- Turn on central versions with a `Directory.Packages.props` at the root containing `<ManagePackageVersionsCentrally>true</ManagePackageVersionsCentrally>` and one `<PackageVersion Include="..." Version="..." />` per package. Project files then use `<PackageReference Include="..." />` with no `Version`.
- Only the nearest `Directory.Packages.props` applies. A nested one must import its parent explicitly with `GetPathOfFileAbove`.
- Use `VersionOverride` on one reference only for a documented exception, and consider setting `CentralPackageVersionOverrideEnabled` to `false` to forbid it. `CentralPackageTransitivePinningEnabled` pins transitive versions, and `GlobalPackageReference` adds a package (an analyzer, for example) to every project.

## Solution files

- Manage the solution with `dotnet sln` (`add`, `list`, `remove`, `migrate`) rather than hand edits. Accepted formats are `.sln`, `.slnx` and the filtered `.slnf`; from .NET 10 `dotnet new sln` produces `.slnx`, before that `.sln`.
- Keep one solution per deployable unit and list every project in it, so a clean checkout builds.
- Nothing machine-specific (absolute paths, user folders) belongs in a project or solution file.

## Why this matters

A solution with fifty hand-maintained project files drifts: one project on a different language version, another on an older package, a third ignoring nullable checks. Putting each decision in one shared file turns that drift into a one-line change.

## Change History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 1.0.0 | 2026-10-09 | Mike Fullerton | Initial creation |
