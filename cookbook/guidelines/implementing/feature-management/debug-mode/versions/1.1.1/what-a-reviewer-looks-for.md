
- An app with no debug panel, or a panel missing flag overrides, the analytics event log, the A/B test variant picker or environment info
- Panel code, its entry point or a debug library reachable in a release build; a runtime check (a flag, `android:exported="false"`, an unlinked route) standing in for a compile-time guard
- A platform's panel reached or guarded other than its access method names, without a recorded reason
- A Swift `#if DEBUG` guard in a project whose Release configuration also defines `DEBUG`
- An internal-build configuration that carries the panel and is also the one submitted to the App Store, or a test build sent to Apple testers other than through TestFlight
- An Android release build type that is debuggable, or WebView debugging, `Log` or `Debug` tracing calls left in release
- Android panel code in `src/main/`, even behind `BuildConfig.DEBUG`; `BuildConfig.DEBUG` in a module on AGP 8+ that does not enable `buildConfig`
- Debug-only libraries declared with `implementation` instead of `debugImplementation`, or a library's no-op release artifact not declared under `releaseImplementation`
- A C# `[Conditional("DEBUG")]` helper whose body references panel code outside `#if DEBUG`
- Debug or verbose logging active in release; Authorization or Cookie headers, tokens or bodies shown unredacted in the panel or a network inspector; a network inspector in a release build
- A flag SDK's dev mode, ASP.NET Core's Developer Exception Page or another SDK developer mode enabled in production
- API keys or secrets in client-side debug configuration or shown by the panel
- No developer-traffic filter on analytics that receives debug-mode events
- A production override by cookie, header or query parameter that is neither signed nor authenticated, or not recorded as attack surface
- A new access gesture or shortcut that redefines a system or browser one
- A Node.js server deployed with `NODE_ENV` other than `production`, server-side debug features gated on `NODE_ENV === 'development'`, or a server debug endpoint deployed to production behind a runtime switch
- A debug feature that bypasses payment, subscription or authentication, or reads system or user data, with no test that needs it
- A panel section that duplicates the platform's developer tools; a React Native panel built on Flipper's native integration

