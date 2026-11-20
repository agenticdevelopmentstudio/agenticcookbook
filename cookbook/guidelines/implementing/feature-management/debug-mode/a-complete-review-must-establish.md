
- The app has a debug-only panel with flag overrides, an analytics event log, an A/B test variant picker and environment info, and the panel is not in release builds
- Each platform reaches and guards the panel by its access method, or a recorded reason says why not; on Windows, a dev-only settings page reached through a debug-only navigation item
- Every panel code path is behind a compile-time guard that removes it from release builds (Swift and C# `#if DEBUG`, Android's debug source set and `debugImplementation`, a bundler-replaced constant), Swift's `DEBUG` condition is set only in the Debug configuration, and every C# `[Conditional("DEBUG")]` helper keeps its panel references inside `#if DEBUG`
- No debug code or debug library is in the release binary; nothing relies on runtime hiding; on Android, the panel's code is in the debug source set and debug libraries are in `debugImplementation`
- Where an Android debug library ships a no-op release artifact, it is declared under `releaseImplementation`, or a recorded reason says why not
- Any internal build that carries the panel goes only to developers and testers and is not the production build
- On Apple platforms, a test or internal build carrying the panel goes through TestFlight and is never submitted to the App Store
- The Android release build is non-debuggable, WebView debugging is off and `Log` and `Debug` tracing calls are removed in it, or a recorded reason says why not
- Debug and verbose logging are disabled in release, and the panel redacts sensitive values from what it records, shows or shares
- Network inspectors are absent from release builds, and redact Authorization and Cookie headers or a recorded reason says why not
- SDK and framework developer modes are off in production, or a recorded reason says why not
- No secret is compiled into client-side debug configuration, the panel's environment section included
- Debug and test traffic is filtered out of analytics reports and exports, or a recorded reason says why not
- Every override reachable in production is signed or authenticated and recorded as attack surface, or a recorded reason says why not
- Access gestures and shortcuts beyond the named access methods redefine no system or browser gesture, and Android shake detection uses the accelerometer, or a recorded reason says why not
- On Android, no panel code is in `src/main/`; a `BuildConfig.DEBUG` check there wraps only the call into the panel's entry point; and on AGP 8+ every module that reads `BuildConfig.DEBUG` enables `buildConfig`
- Node.js servers run with `NODE_ENV=production` in every deployed environment, `NODE_ENV` guards only bundled client code, and server-side debug endpoints are left out of the production deploy, or a recorded reason says why not
- Debug features that bypass payment, subscription or authentication, or read system or user data, exist only where a test needs them, or a recorded reason says why not
- The panel adds what the platform's developer tools do not show, and a React Native panel does not depend on Flipper's native integration, or a recorded reason says why not
- Every MUST rule is kept, with no exception: `debug-only-config-panel`, `release-exclusion-guard`, `compile-out-not-hide`, `internal-build-not-on-the-store`, `debug-logging-off-and-redacted`, `no-secrets-in-debug-panel`, `android-guard-needs-buildconfig`
- Every SHOULD rule is kept, or the change says why not: `platform-access-methods`, `typescript-debug-access`, `windows-debug-settings-page`, `release-no-op-artifact`, `panel-in-internal-builds`, `release-build-not-debuggable`, `network-inspector-redacts-headers`, `sdk-dev-modes-off-in-production`, `exclude-debug-traffic-from-analytics`, `production-overrides-are-guarded`, `access-gesture-avoids-system-gestures`, `node-env-production-on-servers`, `debug-impact-scales-with-permissions`, `complement-platform-devtools`


A review passes when it establishes every item above.
