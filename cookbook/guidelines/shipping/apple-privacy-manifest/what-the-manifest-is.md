
- A property-list resource named exactly **`PrivacyInfo.xcprivacy`**, added to the app target (and to each framework/SDK target that needs its own).
- For an app, place it at the top level of the app bundle. For a framework or SDK, place it inside the bundle so it ships with the binary.
- The file declares four things via these top-level keys:
  - **`NSPrivacyTracking`** (Boolean) — whether the app/SDK uses data for tracking as defined by App Tracking Transparency.
  - **`NSPrivacyTrackingDomains`** (array) — internet domains the app connects to for tracking; required if `NSPrivacyTracking` is `true`.
  - **`NSPrivacyCollectedDataTypes`** (array) — each data type collected, its purposes, whether linked to identity, and whether used for tracking.
  - **`NSPrivacyAccessedAPITypes`** (array) — required-reason APIs the code calls, each paired with an approved reason code.

