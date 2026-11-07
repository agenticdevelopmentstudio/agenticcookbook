---
id: 9ed898fe-ba86-44be-9911-d24fea60dc90
title: "Visual Studio project files"
domain: agenticdevelopercookbook://guidelines/implementing/code-quality/visual-studio-project-files
type: guideline
version: 1.0.1
status: accepted
language: en
created: 2026-10-09
modified: 2026-11-07
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

- Every project MUST use an SDK-style `.csproj` whose root element is `<Project Sdk="Microsoft.NET.Sdk">` (or the SDK that matches the project type). The SDK imports its props and targets implicitly.
- A project MUST NOT list source files. The SDK includes `Compile`, `EmbeddedResource` and `None` items by glob and leaves out `bin` and `obj`. Listing a default item again fails with error NETSDK1022. An item MUST be added only to include something the glob misses, and `Remove` MUST be used to exclude.
- Code MUST NOT hand-edit the old-style project format. Convert it.
- Implicit global usings (from .NET 6) are an SDK feature; a project SHOULD turn them on or off explicitly with a property rather than relying on a template.

## Shared properties

- Properties shared by every project SHOULD live in a `Directory.Build.props` at the repository or solution root: `TargetFramework`, `LangVersion`, `Nullable`, `TreatWarningsAsErrors`, analyzers. MSBuild imports it early, so the project can still override a value. `Directory.Build.targets` is imported late and is the place for logic that must see the project's final values.
- The file name MUST match exactly, including case, because Linux file systems are case-sensitive. `Directory.Build.props` is not `directory.build.props`.
- CI builds SHOULD set `ContinuousIntegrationBuild` to `true` for reproducible output.
- Code MUST NOT set `OutDir` to change output folders, because it bypasses the per-project subfolders. Use `BaseOutputPath`.

## Central package management

- Projects SHOULD turn on central versions with a `Directory.Packages.props` at the root containing `<ManagePackageVersionsCentrally>true</ManagePackageVersionsCentrally>` and one `<PackageVersion Include="..." Version="..." />` per package. Project files then use `<PackageReference Include="..." />` with no `Version`.
- Only the nearest `Directory.Packages.props` applies. A nested one MUST import its parent explicitly with `GetPathOfFileAbove`.
- `VersionOverride` on one reference MUST be used only for a documented exception, and a project MAY set `CentralPackageVersionOverrideEnabled` to `false` to forbid it. `CentralPackageTransitivePinningEnabled` pins transitive versions, and `GlobalPackageReference` adds a package (an analyzer, for example) to every project.

## Solution files

- The solution SHOULD be managed with `dotnet sln` (`add`, `list`, `remove`, `migrate`) rather than hand edits. Accepted formats are `.sln`, `.slnx` and the filtered `.slnf`; from .NET 10 `dotnet new sln` produces `.slnx`, before that `.sln`.
- There SHOULD be one solution per deployable unit, and it MUST list every project, so a clean checkout builds.
- A project or solution file MUST NOT contain anything machine-specific (absolute paths, user folders).

## Why this matters

A solution with fifty hand-maintained project files drifts: one project on a different language version, another on an older package, a third ignoring nullable checks. Putting each decision in one shared file turns that drift into a one-line change.

## Change History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 1.0.1 | 2026-11-07 | Mike Fullerton | State the rules with RFC 2119 keywords |
| 1.0.0 | 2026-10-09 | Mike Fullerton | Initial creation |
