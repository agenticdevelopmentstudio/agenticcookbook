---
id: 544b36cb-2778-4b60-a31e-b55ff789eada
title: "Xcode project hygiene"
domain: agenticdevelopercookbook://guidelines/reviewing/code-quality/xcode-project-hygiene
type: guideline
version: 1.0.0
status: accepted
language: en
created: 2026-10-09
modified: 2026-10-09
author: Mike Fullerton
copyright: 2026 Mike Fullerton
license: MIT
summary: "Review Xcode project changes for settings kept in xcconfig files, shared schemes, justified entitlements, privacy keys, signing material and generator drift."
platforms:
  - ios
  - macos
languages:
  - swift
  - objective-c
tags:
  - xcode
  - xcconfig
  - review
  - entitlements
  - signing
depends-on: []
related:
  - agenticdevelopercookbook://guidelines/implementing/code-quality/xcode-project-hygiene
references:
  - https://developer.apple.com/documentation/xcode/adding-a-build-configuration-file-to-your-project
  - https://developer.apple.com/documentation/bundleresources/entitlements
  - https://developer.apple.com/documentation/bundleresources/information-property-list
approved-by: "approve-artifact v1.0.0"
approved-date: "2026-10-09"
triggers:
  - code-review
  - pre-commit
---

# Xcode project hygiene

Review project-file changes against [Xcode project hygiene](agenticdevelopercookbook://guidelines/implementing/code-quality/xcode-project-hygiene). Read the xcconfig, plist and entitlements diffs first; a large `project.pbxproj` diff is the symptom, not the change.

## Build settings

- A new or changed setting is in an `.xcconfig` file. Flag a setting added only through the project editor.
- A target-level override hides an xcconfig value. Flag a setting defined at both levels.
- Each setting name exists in the build settings reference.

## Schemes and targets

- Every scheme a build or CI job uses is shared and checked in.
- No leftover `copy`, `Untitled` or dead scheme or target.
- Deployment targets are explicit.

## Entitlements

- Every added or changed entitlement key has a reason in the change description and matches a capability the code uses.
- No key was copied in from another app. Removed capabilities have their keys removed.

## Info.plist

- Versions and names come from build settings, not literals.
- Every API the diff starts to use has its usage-description key, with user-facing text.
- Keys for removed features are gone.

## Signing

- No certificate, private key or provisioning profile is added. Team ID and signing style are in the xcconfig.

## Generated projects

- If a project spec drives the project, the generated project is not hand-edited, and it matches the spec after regeneration.

## Why this matters

The risky parts of a project change are small text edits buried in a noisy file. Naming where to look keeps review on the lines that matter.

## Change History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 1.0.0 | 2026-10-09 | Mike Fullerton | Initial creation |
