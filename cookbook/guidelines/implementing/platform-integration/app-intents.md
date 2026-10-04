---
id: e5768eed-0f7f-41d0-bcf7-5a4c18964032
title: "App Intents"
domain: agenticdevelopercookbook://guidelines/implementing/platform-integration/app-intents
type: guideline
version: 1.0.1
status: accepted
language: en
created: 2026-06-09
modified: 2026-06-10
author: Mike Fullerton
copyright: 2026 Mike Fullerton
license: MIT
summary: "Expose key app actions and data as App Intents so Siri, Shortcuts, Spotlight, widgets, and the system can invoke them."
platforms:
  - swift
  - ios
  - macos
tags:
  - apple
  - app-intents
  - automation
depends-on: []
related:
  - agenticdevelopercookbook://guidelines/implementing/platform-integration/shortcuts-and-automation
  - agenticdevelopercookbook://principles/support-automation
references:
  - https://developer.apple.com/documentation/appintents
  - https://developer.apple.com/videos/play/wwdc2025/275/
  - https://developer.apple.com/documentation/appintents/integrating-actions-with-siri-and-apple-intelligence
approved-by: "approve-artifact v1.0.0"
approved-date: "2026-06-10"
triggers:
  - platform-integration
---

# App Intents

The App Intents framework exposes app actions and data to the system so Siri, Shortcuts, Spotlight, widgets, the Action Button, Control Center, and Apple Intelligence can discover and invoke them. It is the modern, code-first path for most apps. Key user-facing actions **SHOULD** be modeled as App Intents.

## Define an AppIntent

A unit of app behavior is a type conforming to `AppIntent`. It needs a `title` and a `perform()` method; expose user-supplied inputs as `@Parameter` properties.

- An intent type **MUST** conform to `AppIntent` and implement `func perform() async throws -> some IntentResult`.
- Each intent **MUST** declare a static `title: LocalizedStringResource` and **SHOULD** set `description` so the action reads clearly in Shortcuts and Spotlight.
- User inputs **MUST** use `@Parameter` with a typed, `IntentParameter`-supported type (primitives, `AppEnum`, or an `AppEntity`).
- `perform()` **MUST** be idempotent-safe where the system may retry, and **MUST** throw a typed error rather than failing silently.
- Return value **SHOULD** use the most specific `IntentResult` (e.g. `.result(value:)`, `&ProvidesDialog`, `&ReturnsValue`) so results chain into other actions.

## Zero-config discovery with AppShortcuts

`AppShortcutsProvider` registers shortcuts that work the moment the app is installed — no user setup required.

- Conform one type to `AppShortcutsProvider` and return `AppShortcut` values from the `appShortcuts` builder.
- Each `AppShortcut` **MUST** supply `phrases` containing `\(.applicationName)` so Siri can resolve the invocation.
- High-value actions **SHOULD** ship as `AppShortcut`s so users get voice and Spotlight access with no configuration.

## Model app data with AppEntity and EntityQuery

To let intents accept or return your domain objects, make them discoverable.

- A domain type exposed to intents **MUST** conform to `AppEntity` (stable `id`, `displayRepresentation`, and a `defaultQuery`).
- Provide an `EntityQuery` (or `EntityStringQuery`/`EnumerableEntityQuery`) so the system can resolve entities by id, by search string, or by enumeration.
- Queries **SHOULD** be backed by your real data layer, not hardcoded — they are how Siri and Shortcuts fetch live values.

## Choosing App Intents over legacy SiriKit

- For new work, prefer the App Intents framework. The older SiriKit Intents (Intents.framework, `.intentdefinition` files, intent extensions) remains for specific domains (messaging, payments, CarPlay-style domains) but is legacy for general app actions.
- Do **NOT** add a new SiriKit custom intent for an action that App Intents can express; migrate existing custom intents when touched.

## FORECASTS (verify against current docs)

- Apple Intelligence / on-device-model surfaces for App Intents evolve release-to-release. Treat any "App Intents power feature X" capability beyond Siri, Shortcuts, Spotlight, widgets, Control Center, and the Action Button as a FORECAST and confirm against the [App Intents documentation](https://developer.apple.com/documentation/appintents) for the OS version you target.

## Change History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 1.0.1 | 2026-06-10 | Mike Fullerton | Add recovered Tier-1 research sources (adversarially-audited) |
| 1.0.0 | 2026-06-09 | Mike Fullerton | Initial creation |
