---
id: b0ee38ef-8256-418f-95a8-495264d282fc
title: "Visual Studio project files"
domain: agenticdevelopercookbook://guidelines/reviewing/code-quality/visual-studio-project-files
type: guideline
version: 1.0.0
status: accepted
language: en
created: 2026-10-09
modified: 2026-10-09
author: Mike Fullerton
copyright: 2026 Mike Fullerton
license: MIT
summary: "Review .NET project and solution changes for SDK-style structure, shared properties, central package versions and solution hygiene."
platforms:
  - windows
  - linux
  - macos
languages:
  - csharp
tags:
  - visual-studio
  - msbuild
  - review
  - nuget
depends-on: []
related:
  - agenticdevelopercookbook://guidelines/implementing/code-quality/visual-studio-project-files
references:
  - https://learn.microsoft.com/en-us/dotnet/core/project-sdk/overview
  - https://learn.microsoft.com/en-us/nuget/consume-packages/central-package-management
approved-by: "approve-artifact v1.0.0"
approved-date: "2026-10-09"
triggers:
  - code-review
  - pre-commit
---

# Visual Studio project files

Review project-file changes against [Visual Studio project files](agenticdevelopercookbook://guidelines/implementing/code-quality/visual-studio-project-files).

## Project structure

- Projects are SDK-style and do not enumerate source files that the SDK already includes.
- Added items are for files the default globs miss.

## Shared properties

- A property that applies to every project is in `Directory.Build.props`, not repeated in each project.
- The `Directory.Build.props` file name has exact casing.
- CI sets `ContinuousIntegrationBuild`. Output folders use `BaseOutputPath`, not `OutDir`.

## Packages

- `PackageReference` has no `Version` when central management is on, and the version is in `Directory.Packages.props`.
- Every `VersionOverride` has a reason.
- A nested `Directory.Packages.props` imports its parent.

## Solutions

- Solution edits were made with `dotnet sln` and list every project.
- The diff has no absolute or user-specific path.

## Why this matters

Project-file diffs are noisy and rarely read closely. Checking only these items catches the drift that causes inconsistent builds.

## Change History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 1.0.0 | 2026-10-09 | Mike Fullerton | Initial creation |
