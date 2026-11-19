---
id: e446ee3e-b8f2-40e7-b93d-3113e6a95e5d
title: "Debug mode"
type: guideline
version: 1.0.3
status: accepted
language: en
created: 2026-03-27
modified: 2026-10-04
author: Mike Fullerton
copyright: 2026 Mike Fullerton
license: MIT
summary: "A debug panel (flag overrides, analytics event log, A/B variant picker, environment info) MUST be compiled out of release builds."
platforms:
  - csharp
  - ios
  - kotlin
  - macos
  - swift
  - typescript
  - web
  - windows
tags:
  - debug-mode
  - feature-management
depends-on: []
related:
  - ac616d81-16c2-4f33-9ae4-139d5c24318d
  - d991b992-07aa-47b9-9d36-4fd1ca81435f
references: []
approved-by: "approve-artifact v1.0.0"
approved-date: "2026-04-04"
triggers:
  - feature-flags
  - logging
---

# Debug mode

An app's debug configuration panel (feature flag overrides, analytics event log, A/B test variant picker, environment info) MUST be compiled out of release builds, not hidden in them. Guard it with the platform's compile-time condition, keep debug logging off in release (and Android release builds non-debuggable), and keep secrets, developer modes and unguarded overrides out of production.

## Rules

- **debug-only-config-panel**: An app MAY include a debug configuration panel; when it does, the panel MUST NOT be in release builds and SHOULD hold:
  - Feature flag overrides
  - Analytics event log
  - A/B test variant picker
  - Environment info (version, build, OS, device) (claims: debug-features-out-of-production, hidden-menus-are-debug-features, growthbook-devtools-overrides, analytics-debug-event-stream, expose-build-and-flag-state, rn-dev-menu-disabled-in-release)
- **platform-access-methods**: Each platform SHOULD open the panel and guard it as follows:
  - **Apple (iOS)**: Shake gesture, guarded by `#if DEBUG`
  - **Apple (macOS)**: Debug menu item, guarded by `#if DEBUG`
  - **Android**: Shake gesture, guarded by `BuildConfig.DEBUG` (with `buildConfig = true`) or the `src/debug/` source set
  - **Web**: `/debug` route, guarded by `NODE_ENV === 'development'` in bundled client code
  - **Windows**: Debug-only settings page, guarded by `#if DEBUG` (claims: uikit-motion-ended-shake, swift-conditional-compilation, xcode-active-compilation-conditions, flex-in-app-debugger-debug-only, hyperion-shake-plugin-drawer, rn-dev-menu-disabled-in-release, android-debug-build-type-defaults, dotnet-if-debug, webpack-mode-defines-node-env, agp8-buildconfig-not-generated, debug-only-source-set, typescript-debug-access-prior)
- **typescript-debug-access**: In TypeScript, the panel MUST be reached this way: Access via `/debug` route or keyboard shortcut (`Ctrl+Shift+D`), guarded by `process.env.NODE_ENV === 'development'`. (claim: typescript-debug-access-prior)
- **windows-debug-settings-page**: On Windows, the panel MUST be guarded by `#if DEBUG`, and SHOULD be a dev-only settings page holding feature flag overrides, the analytics event log, the A/B test variant picker that `debug-only-config-panel` lists, and environment info (app version, build, OS version, device), reached through a navigation menu item visible only in debug builds; a debug-only `void` helper the page calls MAY instead be marked `[Conditional("DEBUG")]`. (claims: dotnet-if-debug, dotnet-conditional-attribute)
- **release-exclusion-guard**: The panel, its entry point and every call into it MUST be excluded from the release build at compile time: behind `#if DEBUG` in Swift (with `DEBUG` in the Debug configuration's Active Compilation Conditions) and in C#; behind `import.meta.env.DEV` under Vite or `process.env.NODE_ENV === 'development'` under webpack in bundled web code; on Android, behind `BuildConfig.DEBUG` with `buildConfig = true`, or kept in the `src/debug/` source set or a `debugImplementation` dependency. (claims: swift-conditional-compilation, xcode-active-compilation-conditions, dotnet-if-debug, vite-dev-flag-tree-shaken, webpack-mode-defines-node-env, remove-debug-code-before-deploy, agp8-buildconfig-not-generated, debug-only-source-set, variant-scoped-dependencies)
- **compile-out-not-hide**: Debug code, debug-only libraries and debug UI MUST be absent from the release binary: excluded by conditional compilation, a debug-only source set, or a variant-scoped dependency (`debugImplementation`, with the library's no-op release artifact where it ships one); a hidden menu, an unexported component, a runtime flag turned off, or obfuscation MUST NOT be relied on to keep them out of reach. (claims: runtime-hiding-is-not-protection, app-review-no-hidden-features, flex-excluded-or-rejected, debug-only-source-set, variant-scoped-dependencies, chucker-no-op-release-artifact, debug-statements-never-in-release, remove-debug-code-before-deploy)
- **panel-in-internal-builds**: When testers outside development need the panel, it MAY also be compiled into a dedicated internal or staging build configuration distributed only to developers and testers (on Apple platforms, through TestFlight); that configuration MUST NOT be the one that produces the store or production build. (claims: dedicated-debug-or-staging-build, pulse-console-in-test-builds, app-review-betas-use-testflight)
- **release-build-not-debuggable**: On Android, the release build type SHOULD NOT be debuggable (`isDebuggable = false`, `debuggable false` in Groovy, the release default), and log files and static test files created in the project SHOULD be removed before the release build. (claims: android-release-not-debuggable, android-release-turn-off-logging)
- **debug-logging-off-and-redacted**: Debug and verbose log levels MUST be disabled in release builds, and the panel's event log and any in-app network inspector MUST redact sensitive values such as `Authorization` and `Cookie` headers, tokens and personal data. (claims: debug-logs-hold-sensitive-data, chucker-data-is-sensitive, android-release-turn-off-logging)
- **sdk-dev-modes-off-in-production**: ASP.NET Core's developer exception page MUST NOT be enabled outside the `Development` environment, and a feature-flag SDK's dev mode (for example GrowthBook's `enableDevMode`) and framework dev menus SHOULD be off in production. (claims: sdk-dev-mode-off-in-production, aspnet-dev-page-development-only, rn-dev-menu-disabled-in-release)
- **no-secrets-in-debug-panel**: The panel's configuration and environment info MUST NOT contain API keys, secrets or credentials compiled into client code, and data the panel captures MUST be redacted and kept out of release builds. (claims: no-secrets-in-client-bundle, chucker-data-is-sensitive, debug-logs-hold-sensitive-data)
- **exclude-debug-traffic-from-analytics**: Events logged from development and test devices (analytics debug mode, panel-driven test events) SHOULD be excluded from reports and exports with the analytics vendor's developer-traffic filter. (claims: exclude-debug-traffic-from-analytics, analytics-debug-event-stream)
- **production-overrides-are-guarded**: A feature-flag or variant override reachable in a production build (a cookie, header or query parameter) SHOULD be authenticated or cryptographically signed and SHOULD be documented as added attack surface; where no such override is needed, production SHOULD accept none. (claims: production-overrides-widen-attack-surface, sdk-dev-mode-off-in-production)
- **access-gesture-avoids-system-gestures**: The gesture or shortcut that opens the panel SHOULD NOT be one the system or browser already binds (Chrome binds `Ctrl+Shift+D`); the one exception is the iOS shake that `platform-access-methods` names, which MAY stay because the panel exists only in debug builds, though shake is the iPhone's undo gesture. On Android, shake detection SHOULD use the accelerometer. (claims: hig-shake-is-system-undo, chrome-binds-ctrl-shift-d, android-shake-needs-sensors)
- **android-guard-needs-buildconfig**: On Android Gradle Plugin 8.0 or later, a module that guards debug code with `BuildConfig.DEBUG` MUST enable `buildFeatures { buildConfig = true }`; debug-only code SHOULD instead live in the `src/debug/` source set, which needs no runtime guard. (claims: agp8-buildconfig-not-generated, debug-only-source-set)
- **node-env-production-on-servers**: Node.js servers SHOULD run with `NODE_ENV=production` in every deployed environment, staging included, so server-side debug features SHOULD NOT be enabled by setting `NODE_ENV` to anything else. (claim: node-env-only-production-on-servers)
- **debug-impact-scales-with-permissions**: Each debug control SHOULD hold only the permissions it needs, and a control that can bypass payment, subscription or authentication, or read system or user data, MUST be kept out of every production build. (claims: debug-feature-impact, debug-features-out-of-production, runtime-hiding-is-not-protection)
- **complement-platform-devtools**: The panel SHOULD hold the app-specific controls the platform's own developer tools lack (flags, variants, the analytics log, environment info) and SHOULD NOT rebuild what those tools provide (browser DevTools, React Native DevTools); new React Native debugging SHOULD NOT depend on the Flipper integration React Native removed. (claims: browser-devtools-built-in, flipper-decoupled-from-react-native)

## How to keep the rules

- Start from the four panel sections: flag overrides, the analytics event log, the A/B variant picker and environment info (version, build, OS, device). Show the current flag configuration and the build metadata side by side, so a tester can say exactly what is running.
- Put the whole panel, its registration and its entry point inside one guarded unit per platform: one `#if DEBUG` block or file in Swift and C#, the `src/debug/` source set on Android, a dynamic import behind `import.meta.env.DEV` under Vite or `process.env.NODE_ENV === 'development'` under webpack on the web. A guard around the entry point alone leaves the panel's code in the binary.
- Add debug-only libraries (in-app inspectors, loggers, plugin drawers) with variant-scoped dependencies, and use a library's no-op release artifact where it ships one.
- Check the release artifact, not the source: search the release binary or bundle for the panel's strings and class names; none should be found.
- If testers need the panel, define a separate build configuration (for example `Staging`) that sets its own compilation condition, rather than enabling the panel in Release.
- Turn the analytics vendor's debug mode on per device (launch argument or `adb`), and add a developer-traffic filter to the analytics property before testers start.
- Choose the panel's entry point after checking the platform's reserved gestures and the browser's shortcuts; a debug menu item or a `/debug` route collides with nothing.
- Leave DOM, network and JavaScript debugging to the platform's developer tools; the panel is for what only the app knows.

## Examples

Swift (iOS), shake to open, compiled only into Debug:

```swift
#if DEBUG
extension UIWindow {
    open override func motionEnded(_ motion: UIEvent.EventSubtype, with event: UIEvent?) {
        if motion == .motionShake {
            DebugPanel.present(from: rootViewController)
        }
        super.motionEnded(motion, with: event)
    }
}
#endif
```

Android (Kotlin DSL), the guard and the debug-only dependency:

```kotlin
android {
    buildFeatures { buildConfig = true } // AGP 8+: BuildConfig is not generated by default
    buildTypes {
        release { isDebuggable = false }
    }
}
dependencies {
    debugImplementation("com.github.chuckerteam.chucker:library:<version>")
    releaseImplementation("com.github.chuckerteam.chucker:library-no-op:<version>")
}
```

Web (Vite), the panel's code removed from the production bundle. It uses the Vite guard that `release-exclusion-guard` allows, which departs from the `NODE_ENV === 'development'` guard that `platform-access-methods` (Web) and `typescript-debug-access` name: the reason is that Vite replaces `import.meta.env.DEV` at build time, so the panel is tree-shaken from the production bundle as it is under webpack's `NODE_ENV` guard; under webpack, write `if (process.env.NODE_ENV === 'development')` instead:

```ts
if (import.meta.env.DEV) {
  const { mountDebugPanel } = await import('./debug/panel');
  mountDebugPanel({ route: '/debug' });
}
```

C# (Windows), the page and a debug-only helper:

```csharp
#if DEBUG
NavView.MenuItems.Add(new NavigationViewItem { Content = "Debug", Tag = "debug" });
#endif

[Conditional("DEBUG")]
static void LogFlagOverride(string key, bool value) => DebugLog.Write($"{key}={value}");
```

## What a reviewer looks for

- A debug panel in a release build, or one missing one of its four sections (flag overrides, the analytics event log, the A/B variant picker or environment info) with no reason given in the code
- An entry point or guard that differs from the one `platform-access-methods` or `windows-debug-settings-page` lists, with no reason given in the code
- The panel enabled in the Release configuration for testers, or an internal configuration that also produces the store build
- Debug panels, menus, inspectors or test hooks reachable in a release build, or kept out only by a runtime flag, an unexported component or a hidden gesture
- Panel code, debug-only libraries or their strings present in the release binary or bundle
- Guards that are not compile-time: a `NODE_ENV` check on a Node server, a `BuildConfig.DEBUG` check in an AGP 8+ module without `buildConfig = true`, a `DEBUG` condition missing from the Debug configuration
- Android release build types left debuggable, or log files and static test files left in the project for the release build, with no reason given in the code
- Verbose or debug logging enabled in release, and logs or inspectors that record `Authorization`/`Cookie` headers, tokens or personal data unredacted
- ASP.NET Core's developer exception page enabled outside `Development`; flag-SDK dev modes or framework dev menus on in production with no reason given in the code
- API keys or secrets in the panel's configuration or any client bundle, and data the panel captures left unredacted or reachable in a release build
- Production-reachable flag overrides by cookie, header or query parameter that are not documented as attack surface, or have no authentication or signing, with no reason given in the code
- A deployed Node.js server whose `NODE_ENV` is not `production`, or a server debug feature switched on by `NODE_ENV`, with no reason given in the code
- Panel entry points that reuse a system or browser binding (`Ctrl+Shift+D` in Chrome), other than the debug-only iOS shake; an Android shake not detected from the accelerometer, with no reason given in the code
- Analytics properties with no developer-traffic filter while debug-mode events are sent, with no reason given in the code
- Debug controls that bypass payment, subscription or authentication, or hold more permissions than they need with no reason given in the code
- A panel that rebuilds the platform's developer tools, or new React Native work wired to Flipper, with no reason given in the code

## A complete review must establish

- Every debug panel, menu and inspector in the change is shown to be absent from the release build, by a compile-time guard, source set or variant-scoped dependency, with no runtime-only hiding
- Any panel present offers flag overrides, the analytics event log, the A/B variant picker and environment info on the platforms in scope, or a stated reason for a missing section was noted
- Each platform's entry method and guard was checked against the list in `platform-access-methods` (and `windows-debug-settings-page`, `typescript-debug-access`), with any difference's stated reason noted
- Any internal or staging configuration that carries the panel was confirmed not to produce the store or production build
- Every guard in use is confirmed to evaluate false for release: the build setting, Gradle feature, bundler mode or environment it depends on was checked
- Debug logging is confirmed off in release, and on Android the release build type was checked for being non-debuggable and for log files or static test files left for it, with any stated reason for a difference noted
- Each log, event view and network inspector the panel shows was checked for redaction of sensitive values
- Every SDK or framework dev mode, and any ASP.NET Core developer exception page, was checked for its production setting
- The panel's configuration and the client bundle were checked for secrets, and the data the panel captures for redaction and for absence from release builds
- Any override reachable in production was checked for documentation as attack surface and for authentication or signing, or found absent
- The panel's entry gesture or shortcut was checked against system and browser bindings, and any Android shake for accelerometer detection
- The `NODE_ENV` of each deployed Node.js server was checked, and no server debug feature was found to depend on another value
- Every debug control was checked for payment, subscription or authentication bypass and for access to system or user data, and its permissions were checked against what it needs
- The panel was checked for rebuilt platform devtools, and new React Native debugging for dependence on Flipper
- Analytics developer-traffic filtering was confirmed, or its absence reported
- Each finding names the rule it breaks

## A build must establish

- `debug-only-config-panel`: any debug panel the app has is not in release builds; it holds flag overrides, an analytics event log, an A/B variant picker and environment info (version, build, OS, device), or the code says why a section is missing
- `platform-access-methods`: each platform opens the panel by its listed method behind its listed guard, or the code says why it differs
- `typescript-debug-access`: the TypeScript panel is reached by a `/debug` route or keyboard shortcut, guarded by `process.env.NODE_ENV === 'development'`
- `windows-debug-settings-page`: the Windows panel is under `#if DEBUG`; it is a settings page with flag overrides, the analytics log, the A/B variant picker and environment info (app version, build, OS version, device), reached from a menu item that exists only in debug builds, or the code says why not
- `release-exclusion-guard`: the panel, its entry point and every call into it are inside a compile-time condition, debug-only source set or variant-scoped dependency that is excluded from release
- `compile-out-not-hide`: a search of the release binary or bundle finds none of the panel's code, strings or debug-only libraries, and no debug feature relies on runtime hiding
- `panel-in-internal-builds`: if the panel ships to testers, it does so from a dedicated internal or staging configuration that never produces the store build
- `release-build-not-debuggable`: on Android, the release build type is not debuggable, and no log files or static test files are left in the project for it, or the code says why not
- `debug-logging-off-and-redacted`: debug and verbose logging are off in release, and the panel's logs and inspectors redact sensitive headers, tokens and personal data
- `sdk-dev-modes-off-in-production`: ASP.NET Core's developer exception page is enabled only in `Development`; every SDK dev mode and framework dev menu is off in production, or the code says why not
- `no-secrets-in-debug-panel`: no API key, secret or credential appears in the panel's configuration or the client bundle, and the data the panel captures is redacted and absent from release builds
- `exclude-debug-traffic-from-analytics`: the analytics property filters developer and test traffic, or the code says why not
- `production-overrides-are-guarded`: production accepts no override, or every override reachable there is documented as attack surface and is authenticated or signed, or the code says why not
- `access-gesture-avoids-system-gestures`: the panel's gesture or shortcut is not one the system or browser binds, other than the debug-only iOS shake, and an Android shake is detected from the accelerometer, or the code says why not
- `android-guard-needs-buildconfig`: every Android module that reads `BuildConfig.DEBUG` enables `buildConfig = true`, or keeps its debug code in `src/debug/`
- `node-env-production-on-servers`: every deployed Node.js server runs with `NODE_ENV=production`, and no server debug feature depends on another value, or the code says why not
- `debug-impact-scales-with-permissions`: each debug control holds only the permissions it needs, or the code says why not, and none that bypasses payment, subscription or authentication or reads system or user data is in a production build
- `complement-platform-devtools`: the panel does not rebuild what the platform's developer tools provide, and no new React Native code depends on Flipper, or the code says why not

## Rationale

- `debug-only-config-panel`: Test and debug features, hidden menus among them, must not be reachable in production because they alter the app's flow or expose system information; the panel's four sections are the functions existing tools provide (flag and variant overrides, an event stream, build and flag state). No source requires every app to have a panel, so the rule makes the panel optional and binds it only once it exists.
- `platform-access-methods`, `release-exclusion-guard`: Swift's `#if` and C#'s `#if DEBUG` are evaluated at compile time; Xcode's Debug configuration supplies `DEBUG`; on Android the debug build type is the debuggable one, `BuildConfig.DEBUG` exists on AGP 8+ only once `buildConfig` is enabled, and a `src/debug/` source set is compiled only into debug variants; Vite and webpack replace their environment constants at build time so the guarded code is tree-shaken. CWE-489's mitigation is to remove debug code before deployment.
- `typescript-debug-access`: Kept as written for the owner to decide: Chrome binds `Ctrl+Shift+D` to bookmarking all open tabs, so the named shortcut collides with a browser command. The `NODE_ENV` guard itself holds for bundled client code.
- `windows-debug-settings-page`: The `DEBUG` symbol follows the Debug/Release configuration, and `[Conditional("DEBUG")]` removes calls to void methods, which Microsoft calls less error-prone than `#if` blocks. No Windows-specific guidance on debug settings pages was found, so the settings-page shape and its debug-only menu item are a SHOULD. The A/B variant picker and the build are listed so the Windows panel holds every section `debug-only-config-panel` lists.
- `compile-out-not-hide`, `debug-impact-scales-with-permissions`: Google warns that marking a debug component not exported is no protection, since ADB on a rooted device can still run it; Apple's guideline 2.5.19 forbids hidden or dormant features in the binary; a reachable debug feature can bypass paywalls and protections with impact proportional to its permissions.
- `panel-in-internal-builds`: Google recommends a dedicated staging build for test and debug features, Pulse aims its console at test builds, and Apple routes betas through TestFlight. The rule therefore allows such a configuration (MAY) and forbids it only from producing the store build.
- `release-build-not-debuggable`, `debug-logging-off-and-redacted`: Android's release checklist (Android only, so the debuggable rule names Android) sets release non-debuggable, deactivates logging and removes log and static test files; it is a checklist, not a stated requirement, and the release build type is non-debuggable by default, so the debuggable and test-file clauses are SHOULD; OWASP MASWE-0005 and Chucker's maintainers warn that debug logs and inspectors capture sensitive data.
- `sdk-dev-modes-off-in-production`, `production-overrides-are-guarded`: A flag SDK's dev mode exposes every internal flag and experiment, a developer exception page leaks exception detail, and per-request overrides let curious or malicious users flip features; signing reduces but does not remove that risk.
- `no-secrets-in-debug-panel`: Values compiled into a client bundle are public; OWASP MASWE-0005 calls for redacting sensitive values that debug tooling captures, and Chucker's maintainers warn that inspectors hold sensitive data and belong in development only.
- `exclude-debug-traffic-from-analytics`: Analytics debug-mode events reach reports and exports unless filtered.
- `access-gesture-avoids-system-gestures`, `platform-access-methods`: Apple's HIG names shake as a standard undo gesture on iPhone and warns against redefining standard gestures; the iOS shake is kept as the rule's one exception because in a Debug-only build the collision affects only developers. Android's motion sensors report shake, so shake detection uses the accelerometer.
- `android-guard-needs-buildconfig`: AGP 8.0 stopped generating `BuildConfig` by default, so a `BuildConfig.DEBUG` guard fails to compile without opting in; a debug source set needs no guard at all.
- `node-env-production-on-servers`: Node.js says servers should always run with `NODE_ENV=production` and calls any other value an antipattern, because it makes environments behave differently; that is advice, so the rule is a SHOULD.
- `sdk-dev-modes-off-in-production`, `production-overrides-are-guarded` (strength): Microsoft says not to enable ASP.NET Core's developer exception page outside `Development`, a MUST scoped to ASP.NET Core; GrowthBook recommends dev mode off in production "in most cases", and Hodgson offers signing as one option and names the added attack surface without requiring that it be documented, so those clauses are SHOULD.
- `complement-platform-devtools`: Chrome ships its developer tools built into the browser, and React Native moved from Flipper to a Chrome-DevTools-based debugger.

## References

- [Test and debug features (Android, OWASP MASVS-CODE)](https://developer.android.com/privacy-and-security/risks/test-debug)
- [CWE-489: Active Debug Code](https://cwe.mitre.org/data/definitions/489.html)
- [App Review Guidelines (Apple)](https://developer.apple.com/app-store/review/guidelines/)
- [Undo and redo (Apple Human Interface Guidelines)](https://developer.apple.com/design/human-interface-guidelines/undo-and-redo)
- [motionEnded(_:with:) (UIKit)](https://developer.apple.com/documentation/uikit/uiresponder/motionended(_:with:))
- [Statements: Conditional Compilation Block (The Swift Programming Language)](https://raw.githubusercontent.com/swiftlang/swift-book/main/TSPL.docc/ReferenceManual/Statements.md)
- [Build settings reference (Xcode)](https://developer.apple.com/documentation/xcode/build-settings-reference)
- [Conditional Compilation, Part 1: Precise Feature Flags (Dave DeLong)](https://davedelong.com/blog/2018/07/25/conditional-compilation-in-swift-part-1/)
- [Configure build variants (Android)](https://developer.android.com/build/build-variants)
- [Add build dependencies (Android)](https://developer.android.com/build/dependencies)
- [Prepare your app for release (Android)](https://developer.android.com/studio/publish/preparing)
- [Android Gradle plugin 8.0.0 release notes](https://developer.android.com/build/releases/past-releases/agp-8-0-0-release-notes)
- [Motion sensors (Android)](https://developer.android.com/develop/sensors-and-location/sensors/sensors_motion)
- [MASTG-TEST-0039: Testing whether the App is Debuggable](https://mas.owasp.org/MASTG/tests/android/MASVS-RESILIENCE/MASTG-TEST-0039/)
- [MASTG-TEST-0084: Testing for Debugging Code and Verbose Error Logging](https://mas.owasp.org/MASTG/tests/ios/MASVS-RESILIENCE/MASTG-TEST-0084/)
- [MASWE-0005: Insertion of Sensitive Data into Logs](https://mas.owasp.org/MASWE/MASVS-STORAGE/MASWE-0005/)
- [C# preprocessor directives](https://raw.githubusercontent.com/dotnet/docs/main/docs/csharp/language-reference/preprocessor-directives.md)
- [Attributes interpreted by the C# compiler: Conditional](https://raw.githubusercontent.com/dotnet/docs/main/docs/csharp/language-reference/attributes/general.md)
- [Handle errors in ASP.NET Core: Developer exception page](https://raw.githubusercontent.com/dotnet/AspNetCore.Docs/main/aspnetcore/includes/developer-exception-page.md)
- [Env Variables and Modes (Vite)](https://raw.githubusercontent.com/vitejs/vite/main/docs/guide/env-and-mode.md)
- [Mode (webpack)](https://raw.githubusercontent.com/webpack/webpack.js.org/main/src/content/configuration/mode.mdx)
- [Node.js, the difference between development and production](https://nodejs.org/en/learn/getting-started/nodejs-the-difference-between-development-and-production)
- [Chrome keyboard shortcuts](https://support.google.com/chrome/answer/157179?hl=en&co=GENIE.Platform%3DDesktop)
- [Chrome DevTools overview](https://developer.chrome.com/docs/devtools/overview)
- [Debugging Basics (React Native)](https://raw.githubusercontent.com/facebook/react-native-website/main/docs/debugging.md)
- [React Native 0.73 - Debugging Improvements](https://raw.githubusercontent.com/facebook/react-native-website/main/website/blog/2023-12-06-0.73-debugging-improvements-stable-symlinks.mdx)
- [FLEX README](https://raw.githubusercontent.com/FLEXTool/FLEX/master/README.md)
- [Pulse README](https://raw.githubusercontent.com/kean/Pulse/main/README.md)
- [Chucker README](https://raw.githubusercontent.com/ChuckerTeam/chucker/develop/README.md)
- [Hyperion-Android README](https://raw.githubusercontent.com/willowtreeapps/Hyperion-Android/develop/README.md)
- [GrowthBook DevTools (Chrome extension)](https://docs.growthbook.io/tools/chrome-extension.md)
- [GrowthBook JavaScript SDK](https://docs.growthbook.io/lib/js.md)
- [Monitor collected events and user properties using DebugView (Firebase)](https://firebase.google.com/docs/analytics/debugview)
- [Feature Toggles (aka Feature Flags) (Pete Hodgson, martinfowler.com)](https://martinfowler.com/articles/feature-toggles.html)

## Change History

| Version | Date | Author | Summary |
|---------|------|--------|---------|
| 1.0.3 | 2026-10-04 | Mike Fullerton | Complete the summary, which was cut off |
| 1.0.2 | 2026-04-09 | Mike Fullerton | Add trigger tags |
| 1.0.1 | 2026-04-09 | Mike Fullerton | Reorganize into use-case directory |
| 1.0.0 | 2026-03-27 | Mike Fullerton | Initial creation |
