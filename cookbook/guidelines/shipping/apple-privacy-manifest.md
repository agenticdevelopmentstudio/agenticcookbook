---
id: 6168eb9e-50be-4b84-940d-cb97f1e374d1
title: "Ship a privacy manifest and declare required-reason APIs"
domain: agenticdevelopercookbook://guidelines/shipping/apple-privacy-manifest
type: guideline
version: 1.0.1
status: accepted
language: en
created: 2026-06-09
modified: 2026-06-10
author: Mike Fullerton
copyright: 2026 Mike Fullerton
license: MIT
summary: "Ship a PrivacyInfo.xcprivacy manifest declaring data collection and required-reason API usage, or App Store submission is rejected."
platforms:
  - ios
  - macos
  - swift
tags:
  - apple
  - privacy
  - app-store
depends-on: []
related:
  - agenticdevelopercookbook://guidelines/implementing/security/privacy
references:
  - https://developer.apple.com/documentation/bundleresources/privacy-manifest-files
  - https://developer.apple.com/documentation/technotes/tn3183-adding-required-reason-api-entries-to-your-privacy-manifest
  - https://developer.apple.com/news/?id=pvszzano
  - https://bitrise.io/blog/post/enforcement-of-apple-privacy-manifest-starting-from-may-1-2024
approved-by: "approve-artifact v1.0.0"
approved-date: "2026-06-10"
triggers:
  - pre-pr
  - dependency-management
---

# Ship a privacy manifest and declare required-reason APIs

This is an **enforced App Store submission gate**, not best-practice advice. Since **May 1, 2024**, App Store Connect rejects uploads that use a "required-reason" API without a declared reason, or that bundle a listed third-party SDK lacking a signed manifest. Treat a missing or incomplete `PrivacyInfo.xcprivacy` as a build-breaking error, not a warning.

## What the manifest is

- A property-list resource named exactly **`PrivacyInfo.xcprivacy`**, added to the app target (and to each framework/SDK target that needs its own).
- For an app, place it at the top level of the app bundle. For a framework or SDK, place it inside the bundle so it ships with the binary.
- The file declares four things via these top-level keys:
  - **`NSPrivacyTracking`** (Boolean) — whether the app/SDK uses data for tracking as defined by App Tracking Transparency.
  - **`NSPrivacyTrackingDomains`** (array) — internet domains the app connects to for tracking; required if `NSPrivacyTracking` is `true`.
  - **`NSPrivacyCollectedDataTypes`** (array) — each data type collected, its purposes, whether linked to identity, and whether used for tracking.
  - **`NSPrivacyAccessedAPITypes`** (array) — required-reason APIs the code calls, each paired with an approved reason code.

## Required-reason API categories

An agent can call these unknowingly through ordinary Foundation usage. Each category has its own `NSPrivacyAccessedAPIType` string and a fixed set of allowed reason codes (`NSPrivacyAccessedAPITypeReasons`):

| Category | Common triggers an agent writes | Manifest API type |
|---|---|---|
| File timestamp | `attributesOfItem`, `contentModificationDate`, `creationDate`, `stat`, `getattrlist` | `NSPrivacyAccessedAPICategoryFileTimestamp` |
| System boot time | `systemUptime`, `mach_absolute_time` for boot-relative timing | `NSPrivacyAccessedAPICategorySystemBootTime` |
| Disk space | `volumeAvailableCapacityKey`, `statfs`, free-space checks | `NSPrivacyAccessedAPICategoryDiskSpace` |
| Active keyboard | reading the user's active keyboard list | `NSPrivacyAccessedAPICategoryActiveKeyboards` |
| User defaults | `UserDefaults` / `NSUserDefaults` access | `NSPrivacyAccessedAPICategoryUserDefaults` |

- You **MUST** declare every category your own code reaches, with at least one valid reason code per category. Invented reason codes are rejected — use only codes Apple lists for that category (see TN3183).
- You **MUST NOT** add a category you do not actually use to "be safe"; declarations are scoped to real usage.

## Required practice

- The app **MUST** ship a `PrivacyInfo.xcprivacy` manifest declaring required-reason API usage and tracking/data-collection before submission.
- Before opening a PR that touches Foundation file/disk/uptime calls, `UserDefaults`, or adds a dependency, you **MUST** verify the manifest still covers all reached categories.
- You **MUST** match `NSPrivacyCollectedDataTypes` to the data the app actually collects; it **SHOULD** stay consistent with the App Store Connect privacy "nutrition label".
- Third-party SDKs on **Apple's list of commonly used SDKs** **MUST** ship their own signed `PrivacyInfo.xcprivacy`; you **MUST NOT** declare on their behalf. If a pinned SDK lacks one, update to a version that includes it or remove the dependency.

## Finding required-reason usage in code

- Search the source and dependencies for the trigger symbols, e.g. `cc-grep` (or `grep -rE`) for: `contentModificationDate|creationDate|attributesOfItem|systemUptime|volumeAvailableCapacity|statfs|UserDefaults|NSUserDefaults`.
- Inspect compiled SDKs: a manifest's reasons must cover transitively linked binaries, so scan vendored `.framework`/`.xcframework` symbols, not just first-party Swift.
- After a clean Archive build, confer the **Privacy Report** in Xcode's Organizer (or `xcrun` privacy tooling) to aggregate manifests across the app and its bundles, and reconcile gaps before submitting.

## Notes

- The manifest is additive and durable: declaring an unused category or a missing reason both cause rejection, so keep it minimal and accurate.
- Apple may extend the required-reason API list over time; re-check the official docs when adding new low-level Foundation calls. Treat any not-yet-published category change as a **forecast** until it appears in Apple's documentation.

## Change History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 1.0.1 | 2026-06-10 | Mike Fullerton | Add recovered Tier-1 research sources (adversarially-audited) |
| 1.0.0 | 2026-06-09 | Mike Fullerton | Initial creation |
