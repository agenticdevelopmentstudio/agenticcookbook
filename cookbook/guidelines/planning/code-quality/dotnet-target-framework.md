---
id: 80915bd6-f18c-4a51-b293-50cef7ead49f
title: "Choosing a .NET target framework"
domain: agenticdevelopercookbook://guidelines/planning/code-quality/dotnet-target-framework
type: guideline
version: 1.0.0
status: accepted
language: en
created: 2026-06-09
modified: 2026-06-09
author: Mike Fullerton
copyright: 2026 Mike Fullerton
license: MIT
summary: "Pick a .NET target framework from the documented support cadence: LTS for apps, multi-target libraries, pin the SDK."
platforms:
  - csharp
tags:
  - dotnet
  - versioning
  - build
depends-on: []
related:
  - agenticdevelopercookbook://principles/small-reversible-decisions
references:
  - https://dotnet.microsoft.com/en-us/platform/support/policy/dotnet-core
approved-by: "approve-artifact v1.0.0"
approved-date: "2026-06-09"
triggers:
  - new-module
  - configuration
---

# Choosing a .NET target framework

The `TargetFramework` (TFM) you pick determines which runtime, API surface, and support window a project gets. Choose it from the published support cadence, not from habit. State the exact version and its end-of-support date in the project so the decision is auditable and reversible.

## Support cadence (pinned: .NET support policy, verified 2026-06-09)

.NET ships a major version every November. Support tiers:

- **LTS (Long Term Support)** — even-numbered releases, supported **3 years**.
- **STS (Standard Term Support)** — odd-numbered releases, supported **24 months** (extended from 18 starting with .NET 9).

Current versions and end-of-support dates (per the support policy reference):

| Version | Tier | Released | End of support |
|---------|------|----------|----------------|
| .NET 10 | LTS  | 2025-11-11 | 2028-11-14 |
| .NET 9  | STS  | 2024-11-12 | 2026-11-10 |
| .NET 8  | LTS  | 2023-11-14 | 2026-11-10 |

Note: .NET 8 (LTS) and .NET 9 (STS) **both reach end of support on 2026-11-10**, so neither is a durable target for new work as of 2026. Re-verify these dates against the reference URL — Microsoft updates them.

## Requirements

- **target-current-lts-for-apps**: New applications and services **SHOULD** target the current LTS (`.NET 10` / `net10.0` as of 2026-06-09) to maximize the support runway with predictable upgrades.
- **sts-only-when-needed**: A project **MAY** target an STS release only when it needs an STS-exclusive feature AND the team commits to upgrading before the 24-month window closes. Otherwise prefer LTS.
- **multi-target-libraries**: A reusable library **SHOULD** multi-target the TFMs its consumers actually require (e.g. `<TargetFrameworks>net8.0;net10.0</TargetFrameworks>`), not the newest available. Add a `netstandard2.0` target only when a concrete consumer needs it.
- **pin-the-sdk**: Every repo **MUST** pin the SDK with a `global.json` (`"sdk": { "version": "10.0.x", "rollForward": "latestFeature" }`) so local, CI, and agent builds resolve the same toolchain.
- **state-version-explicitly**: The `TargetFramework(s)` value **MUST** be explicit in the `.csproj`; do not rely on an implicit or inherited default. Do not assume "latest" — name the version.
- **avoid-eol-targets**: A project **MUST NOT** newly target a framework whose end-of-support date has passed or is within the project's planned delivery window. Check the date before committing the TFM.
- **separate-tfm-from-langversion**: Treat `<LangVersion>` as a separate decision from the TFM; raising the language version does not change the runtime or its support window.

## Decision steps (for an agent)

1. Re-read the support policy reference and confirm today's LTS/STS versions and dates.
2. App or service: set `<TargetFramework>` to the current LTS unless an explicit, documented STS need exists.
3. Library: set `<TargetFrameworks>` to the union of consumer requirements; justify each TFM in a comment.
4. Add or update `global.json` to pin the SDK feature band.
5. Record the chosen version and its end-of-support date in the PR description.

This keeps the choice a small, reversible decision (per `agenticdevelopercookbook://principles/small-reversible-decisions`): a TFM bump is a single property edit plus a rebuild.

## Change History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 1.0.0 | 2026-06-09 | Mike Fullerton | Initial creation |
