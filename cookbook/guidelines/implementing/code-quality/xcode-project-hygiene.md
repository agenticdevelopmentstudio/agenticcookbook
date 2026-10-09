---
id: 187a80eb-e2e5-4a6c-8d14-aa591840abe6
title: "Xcode project hygiene"
domain: agenticdevelopercookbook://guidelines/implementing/code-quality/xcode-project-hygiene
type: guideline
version: 1.0.0
status: accepted
language: en
created: 2026-10-09
modified: 2026-10-09
author: Mike Fullerton
copyright: 2026 Mike Fullerton
license: MIT
summary: "Keep Xcode build settings in xcconfig files, targets and schemes shared and minimal, entitlements and Info.plist keys deliberate, and signing reproducible, using a project generator where the repository already has one."
platforms:
  - ios
  - macos
languages:
  - swift
  - objective-c
tags:
  - xcode
  - xcconfig
  - schemes
  - entitlements
  - info-plist
  - signing
  - xcodegen
depends-on: []
related:
  - agenticdevelopercookbook://guidelines/implementing/code-quality/linting
  - agenticdevelopercookbook://guidelines/reviewing/code-quality/xcode-project-hygiene
  - agenticdevelopercookbook://principles/explicit-over-implicit
  - agenticdevelopercookbook://principles/dry
references:
  - https://developer.apple.com/documentation/xcode/adding-a-build-configuration-file-to-your-project
  - https://developer.apple.com/documentation/xcode/build-settings-reference
  - https://developer.apple.com/documentation/bundleresources/entitlements
  - https://developer.apple.com/documentation/bundleresources/information-property-list
  - https://raw.githubusercontent.com/yonaskolb/XcodeGen/master/Docs/ProjectSpec.md
approved-by: "approve-artifact v1.0.0"
approved-date: "2026-10-09"
triggers:
  - configuration
  - new-module
  - pre-commit
---

# Xcode project hygiene

An Xcode project is source code. Treat its settings, schemes and plists the way you treat any other file: small, reviewable in a diff, and defined once.

## Build settings live in xcconfig files

- Put build settings in `.xcconfig` files, not in the project editor's Build Settings tab. A configuration file is plain text, so a setting change is a one-line diff, and the file can be edited without Xcode.
- Keep one shared file for settings common to every target and one per configuration or target for the differences. Add only the settings you want to change.
- Xcode applies the project's settings, then the configuration file's settings, then the target's settings. Leave the target-level Build Settings tab empty for any setting an xcconfig already owns, or the target value silently wins.
- The format is `SettingName = value`, one per line. If a setting appears twice in a file, the last one wins.
- Create the file with "Configuration Settings File" and deselect all targets so Xcode does not embed it in the bundle.
- Look up each setting name in the build settings reference before you use it. Do not guess a name; an unknown setting is ignored without an error.

## Targets and schemes

- Schemes MUST be shared (stored in the project's shared data, not in a user's private data) and checked in, so command-line builds and CI use the same schemes as the IDE.
- One scheme per thing a person builds, runs or tests. Delete schemes that no longer build.
- Name targets and schemes after what they produce. Do not leave `Untitled`, a copied target's `copy` suffix or a stale product name.
- Keep test targets separate from app targets, and set each target's deployment target explicitly in the xcconfig, not by default.

## Entitlements

- Entitlements are a declaration of what the app is allowed to do. Add one only for a capability the app uses, and review every added key as a security change.
- Keep one `.entitlements` file per target and configuration need (for example a sandboxed macOS app and its helper), referenced through the `CODE_SIGN_ENTITLEMENTS` setting.
- Never copy an entitlements file from another app wholesale. A leftover key grants capability nobody remembers.

## Info.plist

- Keep the Info.plist small. Prefer build-setting substitution (`$(PRODUCT_NAME)`, `$(MARKETING_VERSION)`) over literals, so a version or name is set once in the xcconfig.
- Every privacy usage-description key an API needs (camera, microphone, location and so on) MUST be present with text that tells the user why. A missing key crashes the app when it asks for access.
- Remove keys for features the app no longer has.

## Signing

- Put the team ID and signing style in the xcconfig. Use automatic signing for local development and an explicit, documented identity for release builds.
- Never check in a certificate, a private key or a provisioning profile. CI supplies them from its secret store.

## Project generators

- Where the repository already uses XcodeGen (a `project.yml` spec), treat the spec as the source and the generated `.xcodeproj` as an output: regenerate it, do not hand-edit it, and either ignore it in version control or verify in CI that it matches the spec.
- XcodeGen's spec points targets at xcconfig files through its `configFiles` option and at settings through its `settings` key; keep real values in the xcconfig and use the spec for structure.
- Do not introduce a generator into a repository that has none as part of an unrelated change.

## Why this matters

Project files are merged by many hands and rarely read. Settings scattered across the editor, hidden in per-user schemes or left over from copied targets cause builds that work on one machine and not on CI, and entitlement or plist drift that surfaces at review time or in production. Moving them into small text files makes every change visible.

## Change History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 1.0.0 | 2026-10-09 | Mike Fullerton | Initial creation |
