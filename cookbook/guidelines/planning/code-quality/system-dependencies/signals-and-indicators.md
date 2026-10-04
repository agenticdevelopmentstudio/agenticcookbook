
**OS and platform framework imports:**

- iOS/macOS: `UIKit`, `AppKit`, `SwiftUI`, `CoreData`, `CoreLocation`, `CoreMotion`, `AVFoundation`, `ARKit`, `HealthKit`, `HomeKit`, `MapKit`, `StoreKit`, `UserNotifications`, `LocalAuthentication`, `CryptoKit`, `Network`, `Combine`
- Android/Kotlin: `android.hardware.*`, `android.location.*`, `android.media.*`, `android.bluetooth.*`, `android.nfc.*`, `android.telephony.*`, `com.google.android.gms.*` (Google Play Services), `androidx.camera.*`, `androidx.biometric.*`
- Windows: `Windows.UI.*`, `Windows.Devices.*`, `Windows.Media.*`, `Windows.Storage.*`, `Windows.Security.*`, `Windows.Networking.*`, `System.IO.*`, `System.Net.*`, `System.Security.*`
- Web: `navigator.geolocation`, `navigator.mediaDevices`, `navigator.bluetooth`, `window.indexedDB`, `window.localStorage`, `window.sessionStorage`, `ServiceWorker`, `WebSockets`, `WebRTC`, `WebGL`, `WebAssembly`
- C#: `System.IO`, `System.Net`, `System.Security.Cryptography`, `System.Runtime.InteropServices`, `Microsoft.Win32`

**Hardware access APIs:**

- Camera: `AVCaptureSession` (iOS), `CameraX` (Android), `MediaDevices.getUserMedia()` (Web), `Windows.Media.Capture`
- GPS/Location: `CLLocationManager` (iOS), `FusedLocationProviderClient` (Android), `Geolocation API` (Web), `Windows.Devices.Geolocation`
- Bluetooth: `CoreBluetooth` (iOS), `android.bluetooth` (Android), `Web Bluetooth API`, `Windows.Devices.Bluetooth`
- Biometrics: `LocalAuthentication` (iOS), `BiometricPrompt` (Android), `WebAuthn` (Web), `Windows.Security.Credentials`
- Sensors: `CoreMotion` (iOS), `SensorManager` (Android), `DeviceMotionEvent` (Web)

**System service calls:**

- Keychain/Credential storage: `SecItemAdd/SecItemCopyMatching` (iOS/macOS), `EncryptedSharedPreferences` (Android), `Windows.Security.Credentials.PasswordVault`, Web Credentials Management API
- File system: Direct `FileManager` usage (iOS), `java.io.File` (Android/JVM), `System.IO.File` (C#), `fs` module (Node.js), `File System Access API` (Web)
- Network stack: `URLSession` (iOS), `OkHttp`/`Retrofit` (Android), `HttpClient` (C#), `fetch`/`XMLHttpRequest` (Web), `axios`/`node-fetch` (Node.js)
- Push notifications: `UNUserNotificationCenter` (iOS), `FirebaseMessaging` (Android), Web Push API
- In-app purchases: `StoreKit` (iOS), `BillingClient` (Android), Web Payments API

**Third-party SDK usage:**

- Analytics: Firebase Analytics, Mixpanel, Amplitude, Segment, AppsFlyer
- Crash reporting: Crashlytics, Sentry, Bugsnag
- Maps: Google Maps SDK, Mapbox, Apple MapKit
- Payments: Stripe SDK, Braintree, Square
- Authentication: Auth0 SDK, Firebase Auth, Okta
- Database: Realm, SQLite (direct), Room (Android), Core Data (iOS)

