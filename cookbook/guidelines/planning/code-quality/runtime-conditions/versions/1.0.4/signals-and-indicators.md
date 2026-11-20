
**Permission requests:**

- iOS/macOS: `requestWhenInUseAuthorization()` (location), `requestAccess(to:)` (contacts, calendar, photos), `AVCaptureDevice.requestAccess(for:)` (camera/microphone), `requestAuthorization()` (HealthKit, Motion), `UNUserNotificationCenter.requestAuthorization(options:)` (notifications)
- Android: `ActivityCompat.requestPermissions()` calls; manifest `<uses-permission>` declarations; runtime permission checks `ContextCompat.checkSelfPermission()`
- Web: `navigator.permissions.query()`, `navigator.geolocation.getCurrentPosition()`, `navigator.mediaDevices.getUserMedia()`, `Notification.requestPermission()`
- Windows: capability declarations in `Package.appxmanifest`; `DeviceAccessInformation` checks

**Entitlement declarations (iOS/macOS):**

- `.entitlements` file entries: `com.apple.security.network.client`, `com.apple.security.network.server`, `com.apple.developer.healthkit`, `com.apple.developer.icloud-container-identifiers`, `com.apple.developer.associated-domains`, `com.apple.security.app-sandbox`
- App Groups entitlement — code using shared containers requires this entitlement and implies coordination with an app extension

**Minimum OS version checks:**

- Swift: `if #available(iOS 16.0, *)`, `@available(iOS 16.0, *)`, `#unavailable`
- Kotlin/Android: `if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.S)`, `@RequiresApi`
- C#/Windows: `ApiInformation.IsTypePresent()`, `Environment.OSVersion` comparisons
- Web: feature detection — `if ('serviceWorker' in navigator)`, `if (window.PaymentRequest)`, `CSS.supports()`

**Environment variable and configuration checks:**

- Direct `ProcessInfo.processInfo.environment["KEY"]` (Swift), `System.getenv("KEY")` (Java/Kotlin/C), `process.env.KEY` (Node.js), `Environment.GetEnvironmentVariable()` (C#)
- Configuration file loading: `.env` files, `appsettings.json`, `Info.plist` key reads (`Bundle.main.infoDictionary`), `AndroidManifest.xml` metadata reads
- Build-time conditionals: `#if DEBUG`, `#if FEATURE_X`, `BuildConfig.DEBUG` (Android), `#if os(iOS)`, conditional compilation flags

**Feature flag gates:**

- Remote config reads: `RemoteConfig.sharedInstance().configValue(forKey:)` (Firebase), `LaunchDarkly.shared.variation()`, `Unleash`, custom feature flag service calls
- A/B test enrollment checks
- Killswitch patterns — code guarded by `isFeatureEnabled` booleans fetched at startup

**Required configuration values:**

- API key reads that crash or return early if missing — these imply a configuration prerequisite
- Database connection string requirements
- OAuth client ID / redirect URI reads
- SSL certificate pinning configurations

